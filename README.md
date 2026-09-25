# CodeLoop

A small Python coding agent built for the [CodeCrafters Build Your Own Claude Code challenge](https://codecrafters.io/challenges/claude-code). Give it a prompt, and it can read files, write files, and run shell commands.

## How it works

The model can request a tool, but the Python program performs the action. CodeLoop sends the result back to the model and keeps the messages in the conversation until the model gives a final answer. Conversation history lasts for one run; it is not saved between runs.

## Run

You need Python 3.14+, `uv`, and an `OPENAI_API_KEY` or `OPENROUTER_API_KEY` in your environment.

```sh
./your_program.sh -p "Summarize app/main.py"
```

Set `OPENAI_MODEL` to choose a different model.

## Tech stack

Python 3.14, OpenAI Python SDK, OpenAI or OpenRouter, and `uv`. The command-line interface and tools use Python's standard library.
