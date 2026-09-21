from openai.types.chat import ChatCompletionFunctionToolParam

class Read:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def execute(self) -> str:
        try:
            with open(self.file_path, 'r') as file:
                return file.read()
        except Exception as e:
            return f"Error reading file: {e}"

    @staticmethod
    def get_tool_param() -> ChatCompletionFunctionToolParam:
        return {
            "type": "function",
            "function": {
                "name": "Read",
                "description": "Read the contents of a file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The path to the file to read"
                        }
                    },
                    "required": ["file_path"]
                }
            }
        }
