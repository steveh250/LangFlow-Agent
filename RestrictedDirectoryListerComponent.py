import os
from langflow.custom import Component
from langflow.inputs import MessageTextInput
from langflow.template import Output
from langflow.schema import Data

class RestrictedDirectoryListerComponent(Component):
    display_name = "Restricted Directory Lister"
    description = "Lists files in a directory within the restricted root folder."
    icon = "list"

    # Define the root directory to restrict access
    restricted_root = "/home/wwmdevagent007/SF_Local"

    inputs = [
        MessageTextInput(
            name="directory_path",
            display_name="Directory Path",
            info="Provide the path of the directory to list files. Must be within the restricted directory.",
        ),
    ]

    outputs = [
        Output(display_name="File List", name="file_list", method="list_files"),
    ]

    def list_files(self) -> Data:
        directory_path = os.path.abspath(self.directory_path)  # Get the absolute path of the provided directory

        # Ensure the directory path is within the restricted directory
        if not directory_path.startswith(os.path.abspath(self.restricted_root)):
            return Data(data={"error": f"Access denied. Path not within {self.restricted_root}."})

        try:
            # List all files and directories in the given path
            if os.path.isdir(directory_path):
                files = os.listdir(directory_path)
                return Data(data={"files": files})
            else:
                return Data(data={"error": f"Provided path is not a directory: {directory_path}"})
        except FileNotFoundError:
            return Data(data={"error": f"Directory not found: {directory_path}"})
        except PermissionError:
            return Data(data={"error": f"Permission denied: {directory_path}"})
        except Exception as e:
            return Data(data={"error": f"An error occurred: {str(e)}"})
