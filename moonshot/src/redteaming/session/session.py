import time
from ast import literal_eval
from datetime import datetime

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.redteaming.session.chat import Chat
from moonshot.src.storage.db_accessor import DBAccessor
from moonshot.src.storage.storage import Storage
from slugify import slugify


class SessionMetadata:
    def __init__(
        self,
        session_id: str = "",
        name: str = "",
        description: str = "",
        endpoints: str = "",
        created_epoch: float = 0.0,
        created_datetime: str = "",
        context_strategy: str = "",
        prompt_template: str = "",
        chat_ids: str = "",
    ):
        self.session_id = session_id
        self.name = name
        self.description = description
        self.endpoints = endpoints
        self.created_epoch = created_epoch
        self.created_datetime = created_datetime
        self.context_strategy = context_strategy
        self.prompt_template = prompt_template
        self.chat_ids = chat_ids

    def to_dict(self) -> dict[str, str]:
        """
        Converts the SessionMetadata instance into a dictionary.

        Returns:
            dict: A dictionary representation of the SessionMetadata instance.
        """
        return {
            "session_id": self.session_id,
            "name": self.name,
            "description": self.description,
            "endpoints": self.endpoints,
            "created_epoch": str(self.created_epoch),
            "created_datetime": self.created_datetime,
            "context_strategy": self.context_strategy,
            "prompt_template": self.prompt_template,
            "chat_ids": self.chat_ids,
        }


class Session:
    sql_update_session_metadata_chat = """
        UPDATE session_metadata_table SET chat_ids=? WHERE session_id=?
    """
    sql_read_session_metadata = """
            SELECT * from session_metadata_table
    """
    sql_read_session_chat_metadata = """
            SELECT * from chat_metadata_table
    """
    sql_update_prompt_template = """
            UPDATE session_metadata_table SET prompt_template=? WHERE session_id =?
    """
    sql_update_context_strategy = """
            UPDATE session_metadata_table SET context_strategy=? WHERE session_id =?
    """
    sql_create_session_metadata_table = """
            CREATE TABLE IF NOT EXISTS session_metadata_table (
            session_id text PRIMARY KEY NOT NULL,
            name text NOT NULL,
            description text NOT NULL,
            endpoints text NOT NULL,
            created_epoch INTEGER NOT NULL,
            created_datetime text NOT NULL,
            context_strategy text,
            prompt_template text,
            chat_ids text
            );
    """
    sql_create_chat_metadata_table = """
            CREATE TABLE IF NOT EXISTS chat_metadata_table (
            chat_id text PRIMARY KEY,
            endpoint text NOT NULL,
            created_epoch INTEGER NOT NULL,
            created_datetime text NOT NULL
            );
    """

    sql_create_session_metadata_record = """
        INSERT INTO session_metadata_table (
        session_id,name,description,endpoints,created_epoch,created_datetime,context_strategy,prompt_template)
        VALUES(?,?,?,?,?,?,?,?)
    """

    def __init__(
        # TODO system prompt
        self,
        name: str = "",
        description: str = "",
        endpoints: list[str] = [],
        session_id: str = "",
        prompt_template: str = "",
        context_strategy: str = "",
    ):
        # Checks if cs and pt exist if they are specified
        if context_strategy:
            if not Storage.is_object_exists(
                EnvVariables.CONTEXT_STRATEGY.name, context_strategy, "py"
            ):
                raise RuntimeError(
                    f"Unable to find Context Strategy {context_strategy}. Please select another one."
                )
        if prompt_template:
            if not Storage.is_object_exists(
                EnvVariables.PROMPT_TEMPLATES.name, prompt_template, "json"
            ):
                raise RuntimeError(
                    f"Unable to find Prompt Template {prompt_template}. Please select another one."
                )

        # There is an existing session
        if session_id:
            # Check if session_id is valid
            if Storage.is_object_exists(EnvVariables.SESSIONS.name, session_id, "db"):
                self.db_instance = Storage.create_database_connection(
                    obj_type=EnvVariables.DATABASES.name,
                    obj_id=session_id,
                    obj_extension="db",
                )
                self.metadata = self.get_session_metadata_by_id(session_id)
            else:
                raise RuntimeError(
                    f"Unable to resume existing session {session_id}. Please create a new session."
                )

        # New session
        else:
            created_epoch = time.time()
            created_datetime = datetime.fromtimestamp(created_epoch).strftime(
                "%Y%m%d-%H%M%S"
            )
            session_id = f"{slugify(name)}_{created_datetime}"

            if not context_strategy:
                context_strategy = ""
            if not prompt_template:
                prompt_template = ""

            session_meta_tuple = (
                session_id,
                name,
                description,
                str(endpoints),
                created_epoch,
                created_datetime,
                context_strategy,
                prompt_template,
            )
            self.create_new_session(session_meta_tuple, endpoints)
            self.metadata = self.get_session_metadata_by_id(session_id)

    def create_new_session(
        self,
        session_meta_tuple: tuple,
        endpoints: list,
    ) -> None:
        """
        Creates a new session in the database with the provided metadata and endpoints.

        Args:
            session_meta_tuple (tuple): A tuple containing session metadata.
            endpoints (list): A list of endpoints associated with the session.

        Returns:
            None
        """
        try:
            session_id = session_meta_tuple[0]
            created_epoch = session_meta_tuple[4]
            created_datetime = session_meta_tuple[5]
            session_db_instance = Storage.create_database_connection(
                EnvVariables.SESSIONS.name, session_id, "db"
            )

            # creates chat tables, updates chat metadata, and updates session metadata with chat ids
            Storage.create_database_table(
                session_db_instance, Session.sql_create_session_metadata_table
            )
            Storage.create_database_table(
                session_db_instance, Session.sql_create_chat_metadata_table
            )

            Storage.create_database_record(
                session_db_instance,
                session_meta_tuple,
                Session.sql_create_session_metadata_record,
            )
            list_of_chats = [
                Chat(session_db_instance, endpoint, created_epoch, created_datetime)
                for endpoint in endpoints
            ]
            chat_ids = [str(chat.chat_id) for chat in list_of_chats]
            Storage.update_database_record(
                session_db_instance,
                (str(chat_ids), session_id),
                Session.sql_update_session_metadata_chat,
            )
        except Exception:
            raise

    @staticmethod
    def get_connection_instance_by_session_id(session_id: str) -> DBAccessor:
        """
        Creates and returns a database connection instance for a given session ID.

        It is used to access the database to perform operations.

        Args:
            session_id (str): The unique identifier for the session.

        Returns:
            A database connection instance specific to the session identified by session_id.
        """

        session_db_instance = Storage.create_database_connection(
            obj_type=EnvVariables.SESSIONS.name, obj_id=session_id, obj_extension="db"
        )

        return session_db_instance

    @staticmethod
    def get_session_metadata_by_id(session_id: str) -> SessionMetadata:
        """
        Retrieves and returns the session metadata for a given session ID.

        This method fetches the session metadata from the database associated with the specified session ID. It
        establishes a database connection, retrieves the session metadata, and then constructs a SessionMetadata
        object with the retrieved data. Additionally, it converts the 'endpoints' and 'chat_ids' fields from string
        representations to their original data types using literal_eval.

        Args:
            session_id (str): The unique identifier for the session whose metadata is to be retrieved.

        Returns:
            SessionMetadata: An instance of SessionMetadata populated with the session's metadata, including
                            converted 'endpoints' and 'chat_ids' fields.
        """

        session_db_instance = Session.get_connection_instance_by_session_id(session_id)
        session_metadata_records = Storage.read_database_records(
            session_db_instance, Session.sql_read_session_metadata
        )
        if session_metadata_records is not None:
            session_metadata_tuple = session_metadata_records[0]
            session_metadata = SessionMetadata(*session_metadata_tuple)

            # parse string of lists to lists. they are stored as string as the db does not support
            session_metadata.endpoints = literal_eval(session_metadata.endpoints)
            session_metadata.chat_ids = literal_eval(session_metadata.chat_ids)
            return session_metadata
        else:
            raise RuntimeError(
                "Unable to retrieve Session metadata. Please create a new Session"
            )

    @staticmethod
    def get_session_chats_by_session_id(session_id: str) -> list[Chat]:
        """
        Retrieves and returns a list of Chat instances for all chats associated with a given session ID.

        This method establishes a database connection for the specified session ID and fetches the metadata for all
        chats associated with that session. It then creates and returns a list of Chat instances, each initialized
        with the database connection and the metadata for one of the chats. This allows for interaction with and
        manipulation of individual chat sessions within the specified session.

        Args:
            session_id (str): The unique identifier for the session whose chats are to be retrieved.

        Returns:
            list: A list of Chat instances, each representing a chat session associated with the specified session ID.
        """
        session_db_instance = Session.get_connection_instance_by_session_id(session_id)
        list_of_chat_metadata = Storage.read_database_records(
            session_db_instance, Session.sql_read_session_chat_metadata
        )

        if list_of_chat_metadata is not None:
            return [
                Chat.load_chat(
                    session_db_instance, str(chat_metadata[0]), str(chat_metadata[1])
                )
                for chat_metadata in list_of_chat_metadata
            ]
        else:
            raise RuntimeError(
                "Unable to retrieve Chat metadata. Please create a new Session"
            )

    @staticmethod
    def delete_session(session_id: str) -> None:
        """
        Deletes the database file associated with a given session ID.

        Args:
            session_id (str): The unique identifier for the session whose database file is to be deleted.
        """
        try:
            Storage.delete_object(EnvVariables.SESSIONS.name, session_id, "db")
        except OSError as e:
            print(f"Failed to delete Session file: {e.filename} - {e.strerror}")
        else:
            print(f"Successfully deleted Session - {session_id}")

    @staticmethod
    async def send_prompt(session_id: str, user_prompt: str) -> None:
        # get session db connection
        session_db_instance = Session.get_connection_instance_by_session_id(session_id)
        session_metadata_records = Storage.read_database_records(
            session_db_instance, Session.sql_read_session_metadata
        )
        if session_metadata_records is not None:
            session_metadata_tuple = session_metadata_records[0]
            session_metadata = SessionMetadata(*session_metadata_tuple)
            # get cs, pt, endpoint chat ids from session metadata
            context_strategy_name: str = session_metadata.context_strategy
            prompt_template_name: str = session_metadata.prompt_template
            list_of_endpoints: list[str] = literal_eval(session_metadata.endpoints)
            list_of_chat_ids: list[str] = literal_eval(session_metadata.chat_ids)

            # pass required configuration to individual chats to send prompt
            for chat_id, endpoint in zip(list_of_chat_ids, list_of_endpoints):
                await Chat.send_prompt(
                    session_db_instance=session_db_instance,
                    chat_id=chat_id,
                    endpoint=str(endpoint),
                    user_prompt=user_prompt,
                    context_strategy_name=context_strategy_name,
                    prompt_template_name=prompt_template_name,
                )
        else:
            raise RuntimeError(
                "Unable to retrieve Session metadata. Please create a new Session"
            )

    @staticmethod
    def update_prompt_template(session_id: str, prompt_template_name: str) -> None:
        """
        Updates the prompt template for a specific session.

        This method creates a database connection for the session identified by session_id and then calls the
        `StorageManager.update_prompt_template` method to update the prompt template with the provided name.
        It allows for changing the prompt template associated with the session, enabling customization of prompts
        used within the session.

        Args:
            session_id (str): The unique identifier of the session for which the prompt template is to be updated.
            prompt_template_name (str): The new prompt template name to be assigned to the session.

        Returns:
            None: This method does not return a value but updates the prompt template for the specified session.
        """
        if prompt_template_name != "":
            if not Storage.is_object_exists(
                EnvVariables.PROMPT_TEMPLATES.name, prompt_template_name, "json"
            ):
                raise RuntimeError(
                    f"Unable to find Prompt Template {prompt_template_name}. Please select another one."
                )
        session_db_instance = Session.get_connection_instance_by_session_id(session_id)
        Storage.update_database_record(
            session_db_instance,
            (prompt_template_name, session_id),
            Session.sql_update_prompt_template,
        )

    @staticmethod
    def update_context_strategy(session_id: str, context_strategy_name: str) -> None:
        """
        Updates the context strategy for a specific session.

        This method creates a database connection for the session identified by session_id and then calls the
        `StorageManager.update_context_strategy` method to update the context strategy with the provided name.
        It allows for changing the context strategy associated with the session, enabling customization of context
        management within the session.

        Args:
            session_id (str): The unique identifier of the session for which the context strategy is to be updated.
            context_strategy_name (str): The new context strategy name to be assigned to the session.

        Returns:
            None: This method does not return a value but updates the context strategy for the specified session.
        """

        if context_strategy_name != "":
            if not Storage.is_object_exists(
                EnvVariables.CONTEXT_STRATEGY.name, context_strategy_name, "py"
            ):
                raise RuntimeError(
                    f"Unable to find Context Strategy {context_strategy_name}. Please select another one."
                )
        session_db_instance = Session.get_connection_instance_by_session_id(session_id)
        Storage.update_database_record(
            session_db_instance,
            (context_strategy_name, session_id),
            Session.sql_update_context_strategy,
        )
