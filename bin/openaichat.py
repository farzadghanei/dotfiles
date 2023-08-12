#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Chat completion using OpenAI APIs
---------------------------------

This script is released under the terms of MIT license.

License:
Copyright (c) 2023 Farzad Ghanei (https://www.ghanei.net)

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the “Software”), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import sys
import os
from time import time
from typing import List, Dict, Optional, Callable
from argparse import Namespace, ArgumentParser
from functools import partial
import json
import logging
import openai


__VERSION__ = "0.1.1"

# defaults
CHAT_MODELS = (
    "gpt-4",
    "gpt-4-0613",
    "gpt-4-32k",
    "gpt-4-32k-0613",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-16k-0613",
)
DEFAULT_CHAT_MODEL = str(os.environ.get("OPENAI_CHAT_MODEL", "gpt-3.5-turbo"))

COMMANDS_QUIT = (":q", "quit")

logger = logging.getLogger()
formatter = logging.Formatter("[%(asctime)s] %(message)s")
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.addHandler(handler)


# types
ChatMessageType = Dict[str, str]
ChatHistoryType = List[ChatMessageType]
ChatCallbackType = Callable[[ChatHistoryType], None]


def send_chat_message(
    model: str,
    chat_history: ChatHistoryType,
) -> str:
    logger.debug(
        "sending {} chat history items",
        len(chat_history),
    )
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Please provide a response completing this conversion.",  # noqa: E501
            }
        ]
        + chat_history,
    )
    logger.debug("received response. choices {}", len(response.choices))
    return response.choices[0]["message"]["content"].strip()


def load_chat_history(file_path: str) -> ChatHistoryType:
    with open(file_path, "r", encoding="utf-8") as file:
        saved_data = json.load(file)
    return saved_data.get("chat_history", [])


def save_chat_history(file_path: str, chat_history: ChatHistoryType) -> None:
    saved_data = {
        "format_verion": 1,
        "prog_verion": __VERSION__,
        "timestamp": int(time()),
        "chat_history": chat_history,
    }
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(saved_data, file)


def read_input() -> str:
    lines = []
    stop = False
    try:
        while not stop:
            line = input()
            lines.append(line)
            if line.strip().lower() in COMMANDS_QUIT and len(lines) == 1:
                break
    except EOFError:
        pass
    return "\n".join(lines)


def start_chat(
    model: str = DEFAULT_CHAT_MODEL,
    chat_history: Optional[ChatHistoryType] = None,
    callback: Optional[ChatCallbackType] = None,
) -> ChatHistoryType:
    print("Press Ctrl+D (EOF) to send the message.", file=sys.stderr)
    print(
        "Enter {}, an empty message, or press Ctrl+C to quit.".format(
            " or ".join(COMMANDS_QUIT)
        ),
        file=sys.stderr,
    )

    if chat_history is None:
        chat_history = []
    while True:
        print("> ", end="", file=sys.stderr)
        user_input = read_input().strip()
        if user_input.lower() in COMMANDS_QUIT or user_input == "":
            break
        message = {"role": "user", "content": user_input}
        chat_history.append(message)

        print("\nsending ...", file=sys.stderr)
        response = send_chat_message(model, chat_history)
        chat_history.append({"role": "assistant", "content": response})
        print(response)
        logger.debug("chat history items: {}", len(chat_history))
        if callback is not None:
            callback(chat_history)
    return chat_history


def main(args: Optional[List[str]] = None) -> int:
    parser = ArgumentParser(description=None)
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s " + __VERSION__,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        dest="verbosity",
        default=0,
        help="openAI library verbosity",
    )
    parser.add_argument("-b", "--api-base", help="API base url")
    parser.add_argument("-k", "--api-key", help="API key")
    parser.add_argument("-p", "--proxy", nargs="+", help="HTTP(s) proxy address")
    parser.add_argument(
        "-m",
        "--model",
        default=DEFAULT_CHAT_MODEL,
        choices=CHAT_MODELS,
        help="Chat model to use",
    )
    parser.add_argument("-s", "--save-file", help="File path to save chat history")
    parser.add_argument("-l", "--load-file", help="File path to load chat history")

    def help(opts):
        parser.print_help()

    parser.set_defaults(func=help)

    opts: Namespace = parser.parse_args(args)
    if opts.verbosity == 1:
        logger.setLevel(logging.INFO)
    elif opts.verbosity >= 2:
        logger.setLevel(logging.DEBUG)

    if opts.api_key is not None:
        openai.api_key = opts.api_key
    elif not os.environ.get("OPENAI_API_KEY"):
        print("Please specify OpenAI API key", file=sys.stderr)
        return os.EX_CONFIG

    openai.debug = True
    if opts.api_base is not None:
        openai.api_base = opts.api_base
    if opts.proxy is not None:
        openai.proxy = {}
        for proxy in opts.proxy:
            if proxy.startswith("https"):
                openai.proxy["https"] = proxy
            elif proxy.startswith("http"):
                openai.proxy["http"] = proxy

    if opts.load_file and os.path.exists(opts.load_file):
        chat_history = load_chat_history(opts.load_file)
    else:
        chat_history = []
    try:
        callback = (
            partial(save_chat_history, opts.save_file) if opts.save_file else None
        )
        start_chat(str(opts.model), chat_history, callback)
    except openai.error.OpenAIError as err:
        logger.exception(err)
        return os.EX_SOFTWARE
    except KeyboardInterrupt:
        return os.EX_TEMPFAIL
    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
