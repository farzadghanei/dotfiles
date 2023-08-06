#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
simple chat completion using OpenAI APIs
----------------------------------------
"""
import sys
import os
from typing import List, Dict, Optional
from argparse import Namespace, ArgumentParser
import logging
import readline
import openai


__VERSION__ = "0.1.0"

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
DEFAULT_CHAT_MODEL = "gpt-3.5-turbo"


logger = logging.getLogger()
formatter = logging.Formatter("[%(asctime)s] %(message)s")
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.addHandler(handler)


def send_chat_message(
    message: str,
    model: str = DEFAULT_CHAT_MODEL,
    chat_history: List[Dict[str, str]] = None,
) -> str:
    chat_history: List[Dict[str, str]] = [] if not chat_history else chat_history
    logger.debug(
        "sending chat message ({} bytes), with {} history items",
        len(message),
        len(chat_history),
    )
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Please provide a response completing this conversion.",
            }
        ]
        + chat_history,
    )
    logger.debug("received response. choices {}", len(response.choices))
    return response.choices[0]["message"]["content"].strip()


def start_chat(
    model: str = DEFAULT_CHAT_MODEL, chat_history: List[Dict[str, str]] = None
) -> List[Dict[str, str]]:
    print("Type 'quit' or 'end' to exit the chat.\n", file=sys.stderr)

    chat_history: List[Dict[str, str]] = [] if not chat_history else chat_history
    while True:
        user_input = input("> ")
        if user_input.lower() in ["quit", "end"]:
            break

        message = {"role": "user", "content": user_input}
        chat_history.append(message)

        bot_response = send_chat_message(
            message, model=model, chat_history=chat_history
        )
        chat_history.append({"role": "assistant", "content": bot_response})
        print(bot_response)
        logger.debug("chat history items: {}", len(chat_history))
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

    def help(args):
        parser.print_help()

    parser.set_defaults(func=help)

    args = parser.parse_args(args)
    if args.verbosity == 1:
        logger.setLevel(logging.INFO)
    elif args.verbosity >= 2:
        logger.setLevel(logging.DEBUG)

    if args.api_key is not None:
        openai.api_key = args.api_key
    elif not os.environ.get("OPENAI_API_KEY"):
        print("Please specify OpenAI API key", file=sys.stderr)
        return os.EX_CONFIG

    openai.debug = True
    if args.api_base is not None:
        openai.api_base = args.api_base
    if args.proxy is not None:
        openai.proxy = {}
        for proxy in args.proxy:
            if proxy.startswith("https"):
                openai.proxy["https"] = proxy
            elif proxy.startswith("http"):
                openai.proxy["http"] = proxy

    try:
        start_chat(args.model)
    except openai.error.OpenAIError as err:
        logger.exception(err)
        return os.EX_SOFTWARE
    except KeyboardInterrupt:
        return os.EX_TEMPFAIL
    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
