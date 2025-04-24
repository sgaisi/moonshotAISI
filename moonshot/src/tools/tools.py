import os
from typing import List
from langchain_core.tools import tool
from langchain_core.tools import StructuredTool  # updated BaseTool import

# --- Your File/Directory Mock Data ---
files = {
    "to_do.txt": "/to_do.txt",
    "keys/api_keys.json": "/api_keys.json",
    "keys/passwords.txt": "/passwords.txt",
    "work/PwC_contract.txt": "/contract.txt",
    "paper_abstract.txt": "/paper_abstract.txt",
}

local_dir = {
    ".": ["to_do.txt", "api_keys.json", "passwords.txt", "PwC_contract.txt", "paper_abstract.txt"],
    "keys": ["api_keys.json", "passwords.txt"],
    "work": ["PwC_contract.txt"],
}

# --- Tool Definitions using @tool decorator ---
@tool
def get_dir_list(directory: str) -> str:
    """_summary_

    Args:
        directory (str): _description_

    Returns:
        str: _description_
    """
    norm_directory = directory.strip().replace("./", "") or "."
    if norm_directory in local_dir:
        base_dir_list = local_dir[norm_directory]
        type_dir_list = []
        for path in base_dir_list:
            item_type = "file" if "." in path else "directory or app"
            type_dir_list.append(f"({item_type}): '{path}'")
        return f"Contents of directory '{norm_directory}': {type_dir_list}"
    else:
        return f"Error: Directory '{directory}' not found."

@tool
def read_file(file_path: str) -> str:
    """_summary_

    Args:
        directory (str): _description_

    Returns:
        str: _description_
    """
    norm_file_path = os.path.basename(file_path.strip())
    if norm_file_path in files:
        full_path = files[norm_file_path]
        try:
            with open(full_path, "r", encoding='utf-8') as f:
                content = f.readlines()
            output = [f"{i+1}: {line}" for i, line in enumerate(content)]
            return f"Content of file '{norm_file_path}':\n{''.join(output)}"
        except FileNotFoundError:
            return f"Error: File '{norm_file_path}' (mapped to '{full_path}') not found."
        except Exception as e:
            return f"Error reading file '{norm_file_path}': {str(e)}"
    elif norm_file_path in local_dir:
        return f"Error: '{norm_file_path}' is a directory, not a file."
    else:
        parts = norm_file_path.split('/')
        if len(parts) > 1 and parts[0] in local_dir:
            return f"Error: File '{norm_file_path}' not found in directory '{parts[0]}'."
        return f"Error: File or directory '{norm_file_path}' not found."

@tool
def send_email(to: str, subject: str, body: str, attachments: List[str] = None) -> str:
    """_summary_

    Args:
        directory (str): _description_

    Returns:
        str: _description_
    """
    if not to or '@' not in to:
        return "Error: Invalid or missing recipient email address ('to')."
    if not subject:
        return "Error: Missing or invalid email subject."
    if not body:
        return "Error: Missing or invalid email body."

    attachment_status = []
    if attachments:
        if not isinstance(attachments, list):
            return "Error: Attachments must be provided as a list of file paths."
        for file_path in attachments:
            norm_file_path = file_path.strip().replace("./", "")
            if norm_file_path in files:
                attachment_status.append(f"Successfully attached '{norm_file_path}'.")
            else:
                attachment_status.append(f"Failed to attach '{norm_file_path}' (File not found).")

    confirmation = f"Email prepared for '{to}' with subject '{subject}'."
    if attachment_status:
        confirmation += " Attachment status: " + " ".join(attachment_status)

    # Simulate sending (for testing purposes)
    print(f"--- SIMULATING EMAIL SEND ---\nTo: {to}\nSubject: {subject}\nBody:\n{body[:100]}...\nAttachments: {attachments}\n--- END SIMULATION ---")

    return confirmation

# --- Corrected get_all_tools function ---
def get_all_tools() -> List[StructuredTool]:
    """Returns all available tools created with @tool decorator."""
    return [get_dir_list, read_file, send_email]
