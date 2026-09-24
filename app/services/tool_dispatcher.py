import json

from app.tools.read import Read


def dispatch_read_tool(args: str) -> str:
    parsed_args = json.loads(args)
    file_path = parsed_args["file_path"]
    reader = Read(file_path)
    return reader.execute()
