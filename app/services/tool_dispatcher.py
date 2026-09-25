import json
import subprocess

from openai.types.chat import ChatCompletionToolMessageParam

from app.tools.read import Read
from app.tools.write import Write


def dispatch_tool_call(tool_call) -> ChatCompletionToolMessageParam:
    if tool_call.type == "function":
        if tool_call.function.name == "Read":
            read_result = dispatch_read_tool(tool_call.function.arguments)
            return {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": read_result,
            }
        elif tool_call.function.name == "Write":
            write_result = dispatch_write_tool(tool_call.function.arguments)
            return {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": write_result,
            }
        elif tool_call.function.name == "Bash":
            bash_result = dispatch_bash_tool(tool_call.function.arguments)
            return {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": bash_result,
            }
    raise ValueError(f"Unknown tool call: {tool_call}")
def dispatch_read_tool(args: str) -> str:
    parsed_args = json.loads(args)
    file_path = parsed_args["file_path"]
    reader = Read(file_path)
    return reader.execute()

def dispatch_write_tool(args: str) -> str:
    parsed_args = json.loads(args)
    file_path = parsed_args["file_path"]
    content = parsed_args["content"]
    writer = Write(file_path, content)
    writer.execute()
    return "Write operation completed successfully."

def dispatch_bash_tool(args: str) -> str:
    parsed_args = json.loads(args)
    command = parsed_args["command"]
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.stderr}"
