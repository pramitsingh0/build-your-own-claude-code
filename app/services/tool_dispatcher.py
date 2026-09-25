import json
import subprocess

from app.tools.read import Read
from app.tools.write import Write


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
