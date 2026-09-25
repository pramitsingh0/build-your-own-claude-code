import argparse
import json
import os
import sys
from typing import Iterable

from openai import OpenAI
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessage,
    ChatCompletionMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionUserMessageParam,
)

# internal imports
from app.services.tool_dispatcher import dispatch_read_tool, dispatch_write_tool, dispatch_bash_tool
from app.tools.read import Read
from app.tools.write import Write
from app.tools.bash import Bash

# OpenRouter (what the CodeCrafters tester injects) takes priority; fall back to OpenAI locally.
if os.getenv("OPENROUTER_API_KEY"):
    API_KEY = os.getenv("OPENROUTER_API_KEY")
    BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")
    MODEL = os.getenv("OPENAI_MODEL", default="anthropic/claude-haiku-4.5")
else:
    API_KEY = os.getenv("OPENAI_API_KEY")
    BASE_URL = os.getenv("OPENAI_BASE_URL", default="https://api.openai.com/v1")
    MODEL = os.getenv("OPENAI_MODEL", default="gpt-4o-mini")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("neither OPENROUTER_API_KEY nor OPENAI_API_KEY is set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    messages: list[ChatCompletionMessageParam] = [{"role": "user", "content": args.p}]

    while messages:

        chat = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=[
                Read.get_tool_param(),
                Write.get_tool_param(),
                Bash.get_tool_param(),
            ],
        )

        if not chat.choices:
            raise RuntimeError("no choices in response")

        assistant_message: ChatCompletionMessage = chat.choices[0].message

        messages.append(
            ChatCompletionAssistantMessageParam(
                **assistant_message.model_dump(
                    include={"role", "content", "tool_calls"}, exclude_unset=True
                )
            )
        )

        if not assistant_message.tool_calls:
            print(chat.choices[0].message.content)
            break
        else:
            for tool_call in assistant_message.tool_calls:
                if tool_call.type == "function":
                    tool_result: ChatCompletionToolMessageParam
                    if tool_call.function.name == "Read":
                        read_result = dispatch_read_tool(tool_call.function.arguments)
                        tool_result = {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": read_result,
                        }
                    elif tool_call.function.name == "Write":
                        write_result = dispatch_write_tool(tool_call.function.arguments)
                        tool_result = {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": write_result,
                        }
                    elif tool_call.function.name == "Bash":
                        bash_result = dispatch_bash_tool(tool_call.function.arguments)
                        tool_result = {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": bash_result,
                        }
                    messages.append(tool_result)


if __name__ == "__main__":
    main()
