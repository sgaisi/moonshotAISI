from typing_extensions import TypedDict
from .base_service import BaseService
from web_api.services.utils.exceptions_handler import SessionException, exception_handler
from web_api.schemas.session_create_dto import SessionCreateDTO
from web_api.schemas.session_response_model import SessionMetadataModel
import moonshot.api as moonshot_api


class PromptDetails(TypedDict):
    chat_id: int
    connection_id: str
    context_strategy: int
    prompt_template: str
    prompt: str
    prepared_prompt: str
    predicted_result: str
    duration: str

class SessionService(BaseService):

    @exception_handler
    def create_session(self, session_create_dto: SessionCreateDTO, set_as_current_session: bool = False) -> SessionMetadataModel:
        new_session = moonshot_api.api_create_session(
            session_create_dto.name,
            session_create_dto.description,
            session_create_dto.endpoints,
            session_create_dto.context_strategy,
            session_create_dto.prompt_template
        )

        return SessionMetadataModel(
            session_id=new_session.session_id,
            name=new_session.name,
            description=new_session.description,
            created_epoch=new_session.created_epoch,
            created_datetime=new_session.created_datetime,
            endpoints=new_session.endpoints,
            prompt_template=new_session.prompt_template,
            context_strategy=new_session.context_strategy,
            chats=[],
            filename="",
            chat_history=None
        )

    @exception_handler
    def get_session(self, session_id: str) -> SessionMetadataModel | None:
        session_data = next((session for session in self.get_sessions() if session.session_id == session_id), None)
        return session_data

    @exception_handler
    def get_sessions(self) -> list[SessionMetadataModel | None]:
        sessions: list[SessionMetadataModel] = moonshot_api.api_get_all_session_details();
        return [SessionMetadataModel.model_validate(session) for session in sessions]

    # @exception_handler
    # def set_current_session(self, session_id: str) -> SessionMetadataModel | None:
    #     session_data = self.get_session(session_id)
    #     session_instance: Session = Session.load_session(session_id)
    #     Session.current_session = session_instance
    #     return session_data

    @exception_handler
    def get_session_chat_history(self, session_id: str, history_length: int | None) -> dict[str, list[PromptDetails]]:
        try:
            all_chats = moonshot_api.api_get_session_chats_by_session_id(session_id)
            # session_previous_prompts: list[PromptDetails] = session.get_session_previous_prompts(history_length)
            # session_chats = session.get_session_chats()
            # all_chats_dict: dict[str, list[PromptDetails]] = {}
            # for i, chat in enumerate(session_chats):
            #     all_chats_dict[chat.get_id()] = session_previous_prompts[i][::-1]
        except Exception as e:
            raise SessionException(f"An unexpected error occurred: {e}", __name__)
        
        return all_chats_dict

    # @exception_handler
    # async def send_prompt(self, session_id: str, user_prompt: str, history_length: int | None) -> dict[str, list[PromptDetails]]:
    #     user_prompt = user_prompt.strip()
    #     try:
    #         session_instance = Session.load_session(session_id)
    #         await session_instance.send_prompt_async(user_prompt)
    #         all_chats_dict = self.get_session_chat_history(session_id, history_length)
    #     except Exception as e:
    #         raise SessionException(f"An unexpected error occurred: {e}", __name__)
        
    #     return all_chats_dict

    # @exception_handler
    # def select_prompt_template(self, prompt_template_name: str = '') -> bool:
    #     # Check if current session exists
    #     if Session.current_session:
    #         if prompt_template_name == '':
    #             Session.current_session.set_prompt_template()
    #         else:
    #             Session.current_session.set_prompt_template(prompt_template_name)
    #         return True

    #     return False

