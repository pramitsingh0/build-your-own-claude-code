import argparse
import json
import os
import sys

from openai import OpenAI

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

    chat = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": args.p}],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "Read",
                    "description": "Read the contents of a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "The path to the file to read",
                            }
                        },
                        "required": ["file_path"],
                    },
                },
            }
        ],
    )

    if not chat.choices or len(chat.choices) == 0:
        raise RuntimeError("no choices in response")

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    print(chat.choices[0].message.content)


if __name__ == "__main__":
    main()
