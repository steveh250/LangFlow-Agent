import os
from langflow.custom import Component
from langflow.inputs import MessageTextInput
from langflow.template import Output
from langflow.schema import Data

class RestrictedFileReaderToolComponent(Component):
    display_name = "Restricted File Reader"
    description = "Reads content from files within a restricted directory."
    icon = "folder"

    # Define the root directory to restrict access
    restricted_root = "/home/wwmdevagent007/SF_Local"

    inputs = [
        MessageTextInput(
            name="file_path",
            display_name="File Path",
            info="Provide the full path of the file to read. Must be within the restricted directory.",
        ),
    ]

    outputs = [
        Output(display_name="File Content", name="file_content", method="read_file"),
    ]

    def read_file(self) -> Data:
        file_path = os.path.abspath(self.file_path)  # Get the absolute path of the provided file

        # Ensure the file path is within the restricted directory
        if not file_path.startswith(os.path.abspath(self.restricted_root)):
            return Data(data={"error": f"Access denied. Path not within {self.restricted_root}."})

        try:
            with open(file_path, "r") as file:
                content = file.read()
            return Data(data={"content": content})
        except FileNotFoundError:
            return Data(data={"error": f"File not found: {file_path}"})
        except PermissionError:
            return Data(data={"error": f"Permission denied: {file_path}"})
        except Exception as e:
            return Data(data={"error": f"An error occurred: {str(e)}"})
