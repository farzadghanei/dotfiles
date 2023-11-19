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
import platform
from time import time
from typing import List, Dict, Optional, Callable
from argparse import Namespace, ArgumentParser
from functools import partial
import json
import logging
import httpx  # type: ignore
from openai import OpenAI, APIError  # type: ignore


__VERSION__ = "1.0.0"
__LICENSE__ = "OSI Approved :: MIT License"

HELP_MESSAGE = """
Chat completion using OpenAI APIs.

Use --save to store the conversation, and --load to resume a previous one,
or --session to save/load a session (not used with --save or --load).
Type the messages to the standard input after program starts, or send a
file to standard input: "cat question | {prog} --session quest".
Or use prelude to provide context for the first message.
"cat question | {prog} 'explain each line of the text below'".

Environment variables: OPENAI_API_KEY (OpenAI API key),
    OAICHAT_MODEL (default chat model to use),
    OAICHAT_DATA_PATH (path to store chat sessions),
    http_proxy, https_proxy
"""

# defaults
CHAT_MODELS = (
    "gpt-4",
    "gpt-4-0613",
    "gpt-4-32k",
    "gpt-4-32k-0613",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k-0613",
)
DEFAULT_CHAT_MODEL = str(os.environ.get("OAICHAT_MODEL", "gpt-3.5-turbo"))

COMMANDS_QUIT = (":q", "quit")
DATA_PATH = str(os.environ.get("OAICHAT_DATA_PATH", "~/.config/oaichat"))

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
    client: OpenAI,
    model: str,
    chat_history: ChatHistoryType,
) -> str:
    """Send a chat message to OpenAI API and return the response."""
    logger.debug(
        "sending {} chat history items",
        len(chat_history),
    )
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Please provide a response completing this conversion.",  # noqa: E501
            }
        ]
        + chat_history,
        model=model,
    )
    logger.debug("received response. choices {}", len(response.choices))
    choice = response.choices[0]
    return choice.message.content.strip()


def load_chat_history(file_path: str) -> ChatHistoryType:
    """Load chat history from a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        saved_data = json.load(file)
    return saved_data.get("chat_history", [])


def save_chat_history(file_path: str, chat_history: ChatHistoryType) -> None:
    """Save chat history to a file."""
    saved_data = {
        "format_verion": 1,
        "prog_verion": __VERSION__,
        "timestamp": int(time()),
        "chat_history": chat_history,
    }
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(saved_data, file)


def read_input() -> str:
    """Read input from stdin until EOF or a command is received."""
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
    client: OpenAI,
    model: str = DEFAULT_CHAT_MODEL,
    prelude: str = "",
    chat_history: Optional[ChatHistoryType] = None,
    callback: Optional[ChatCallbackType] = None,
) -> ChatHistoryType:
    """Start a chat session."""

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
        if sys.stdin.isatty():
            print("> ", end="", file=sys.stderr)
        user_input = read_input().strip()
        if user_input.lower() in COMMANDS_QUIT or user_input == "":
            break

        message = {"role": "user", "content": "{}\n{}".format(prelude, user_input)}
        chat_history.append(message)

        print("\nsending ...", file=sys.stderr)
        response = send_chat_message(client, model, chat_history)
        chat_history.append({"role": "assistant", "content": response})
        print(response)
        logger.debug("chat history items: {}", len(chat_history))
        if callback is not None:
            callback(chat_history)
    return chat_history


def get_system_info() -> str:
    """Return a string containing system information."""

    free_desktop_release = platform.freedesktop_os_release()
    os_name = free_desktop_release.get("NAME", platform.system())
    os_release = free_desktop_release.get("VERSION", platform.release())
    architecture = platform.machine()
    shell = os.environ.get("SHELL", "unknown")
    return "operating system '{}', release '{}', machine architecture '{}', user shell '{}'".format(  # noqa: E501
        os_name, os_release, architecture, shell
    )


def make_client(opts: Namespace) -> OpenAI:
    """Create OpenAI client confgured with proxy and API key based on the options."""
    proxy_conf = {}
    if opts.proxy is not None:
        proxy_conf["https://"] = opts.proxy
        proxy_conf["http://"] = opts.proxy
    else:
        if os.environ.get("http_proxy"):
            http_proxy = str(os.environ["http_proxy"]).strip()
            if not http_proxy.startswith("http://"):
                http_proxy = "http://" + http_proxy
            proxy_conf["http://"] = http_proxy
        if os.environ.get("https_proxy"):
            https_proxy = str(os.environ["https_proxy"]).strip()
            if not https_proxy.startswith("https://"):
                https_proxy = "https://" + https_proxy
            proxy_conf["https://"] = https_proxy
    client_kwargs = {}
    if opts.api_base is not None:
        client_kwargs["base_url"] = opts.api_base
    if proxy_conf.keys():
        client_kwargs["http_client"] = httpx.Client(proxies=proxy_conf)
    client = OpenAI(api_key=opts.api_key, **client_kwargs)
    return client


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point."""
    data_dir = os.path.expanduser(DATA_PATH)
    desc: str = HELP_MESSAGE.format(prog=sys.argv[0])

    parser = ArgumentParser(description=desc)
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
    parser.add_argument(
        "-p",
        "--proxy",
        help="HTTP(s) proxy address (starts with http(s)://). Applies to both schemes.",
    )
    parser.add_argument(
        "-m",
        "--model",
        default=DEFAULT_CHAT_MODEL,
        choices=CHAT_MODELS,
        help="Chat model to use",
    )
    parser.add_argument("-s", "--save-file", help="File path to save chat history")
    parser.add_argument("-l", "--load-file", help="File path to load chat history")
    parser.add_argument(
        "-n",
        "--session",
        metavar="SESSION_NAME",
        help="Name of the session to save/load chat history (not used with save/load, "
        "stored in {})".format(data_dir),
    )
    parser.add_argument(
        "--sys",
        action="store_true",
        help="Prefix prelude with current system info automatically",
    )
    parser.add_argument(
        "prelude", help="Optional prelude to the 1st message", nargs="?"
    )

    def help(opts):
        parser.print_help()

    parser.set_defaults(func=help)

    opts: Namespace = parser.parse_args(args)
    if opts.verbosity == 1:
        logger.setLevel(logging.INFO)
    elif opts.verbosity >= 2:
        logger.setLevel(logging.DEBUG)

    if opts.api_key is None:
        if os.environ.get("OPENAI_API_KEY"):
            opts.api_key = os.environ["OPENAI_API_KEY"]
        else:
            print("Please specify OpenAI API key", file=sys.stderr)
            return os.EX_CONFIG

    client = make_client(opts)

    chat_callback = None
    # Check if --session argument is passed
    if opts.session:
        if opts.save_file or opts.load_file:
            print("Cannot use --session along with --save or --load.", file=sys.stderr)
            return os.EX_USAGE

        session_name = str(opts.session)
        session_dir = os.path.join(data_dir, "sessions")
        os.makedirs(session_dir, exist_ok=True)
        session_file = f"{session_dir}/{session_name}.json"
        chat_callback = partial(save_chat_history, session_file)
        chat_history = (
            load_chat_history(session_file) if os.path.exists(session_file) else []
        )
    else:  # no session
        if opts.save_file:
            chat_callback = partial(save_chat_history, opts.save_file)
        if opts.load_file and os.path.exists(opts.load_file):
            chat_history = load_chat_history(opts.load_file)
        else:
            chat_history = []

    prelude = str(opts.prelude).strip()
    if opts.sys:
        prelude = "Given current system information is {}, {}".format(
            get_system_info(), prelude
        )

    try:
        start_chat(client, str(opts.model), prelude, chat_history, chat_callback)
    except APIError as err:
        logger.exception(err)
        return os.EX_SOFTWARE
    except KeyboardInterrupt:
        return os.EX_TEMPFAIL
    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
