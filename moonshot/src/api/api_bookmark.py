
from moonshot.src.bookmark.bookmark_arguments import BookmarkArguments
from moonshot.src.bookmark.bookmark import Bookmark

bookmark_instance = Bookmark()

def api_insert_bookmark(name: str, prompt: str, response: str, context_strategy: str, prompt_template: str, attack_module: str) -> None:
    """
    Inserts a new bookmark.

    This function takes the details for a new bookmark as input. It then creates a new
    BookmarkArguments object with these details. The function then calls the Bookmark's
    add_bookmark method to insert the new bookmark.

    Args:
        name (str): The name of the bookmark, must be unique.
        prompt (str): The prompt text for the bookmark.
        response (str): The response text for the bookmark.
        context_strategy (str): The context strategy for the bookmark.
        prompt_template (str): The prompt template for the bookmark.
        attack_module (str): The attack module for the bookmark.
    """
    # Create a new BookmarkArguments object
    bookmark_args = BookmarkArguments(
        id=0,  # id will be auto-generated by the database
        name=name,
        prompt=prompt,
        response=response,
        context_strategy=context_strategy,
        prompt_template=prompt_template,
        attack_module=attack_module,
        bookmark_time=""  # bookmark_time will be set to current time in add_bookmark method
    )
    bookmark_instance.add_bookmark(bookmark_args)

def api_get_all_bookmarks():
    return bookmark_instance.get_all_bookmarks()

def api_get_bookmark_by_id(bookmark_id: int):
    return bookmark_instance.get_bookmark_by_id(bookmark_id)

def api_delete_bookmark(bookmark_id: int):
    bookmark_instance.delete_bookmark(bookmark_id)

def api_delete_all_bookmark():
    bookmark_instance.delete_all_bookmark()

def api_export_bookmarks():
    bookmark_instance.export_bookmarks()