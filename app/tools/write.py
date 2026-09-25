from openai.types.chat import ChatCompletionFunctionToolParam

class Write:
    def __init__(self, file_path: str, content: str):
        self.file_path = file_path
        self.content = content

    def execute(self):
        try:
            with open(self.file_path, 'w') as file:
                file.write(self.content)
        except Exception as e:
            raise e

    @staticmethod
    def get_tool_param() -> ChatCompletionFunctionToolParam:
        return {
            "type": "function",
            "function": {
                "name": "Write",
                "description": "Write content to a file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The path to the file to write"
                        },
                        "content": {
                            "type": "string",
                            "description": "The content to write to the file"
                        }
                    },
                    "required": ["file_path", "content"]
                }
            }
        }
