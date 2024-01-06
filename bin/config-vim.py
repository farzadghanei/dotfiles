#!/usr/bin/env python3
"""
Configure VIM with the configurations from this repository.

This script is released under the terms of ISC license.

License:
Copyright (c) 2017 Farzad Ghanei (https://www.ghanei.net)

Permission to use, copy, modify, and/or distribute this software for any purpose
with or without fee is hereby granted, provided that the above copyright notice
and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE
FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER
RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

import sys
import os
import shutil
import subprocess

__version__ = "2.0.0"
dotfiles = os.path.dirname(os.path.dirname(__file__))


def ask_yes_no(msg, default_accept=True):
    default = " [Y/n] " if default_accept else " [y/N] "
    ans = input(msg + default).strip().lower()
    if default_accept:
        return ans != "n"
    return ans == "y"


def configure_vim(target, ask=True):
    if not ask_yes_no("Configure vim on: '{}'?".format(target)):
        return False
    copy_dot_vim(dotfiles, target, ask)
    install_plugins_with_plug(target, ask)


def copy_dot_vim(src, dst, ask=True):
    src_vimrc = os.path.join(src, ".vimrc")
    dst_vimrc = os.path.join(dst, ".vimrc")

    src_dot_vim = os.path.join(src, ".vim")
    dst_dot_vim = os.path.join(dst, ".vim")

    if os.path.exists(dst_vimrc):
        if ask and not ask_yes_no("Replace existing vimrc on '{}'?".format(dst_vimrc)):
            raise IOError("Destination vimrc exists on '{}'".format(dst_vimrc))
        os.remove(dst_vimrc)
    shutil.copy(src_vimrc, dst_vimrc)

    if os.path.exists(dst_dot_vim):
        if ask and not ask_yes_no("Replace existing .vim on '{}'?".format(dst_dot_vim)):
            raise IOError("Destination .vim exists on '{}'".format(dst_dot_vim))
        shutil.rmtree(dst_dot_vim)
    shutil.copytree(src_dot_vim, dst_dot_vim)


def install_plugins_with_plug(target, ask):
    """
    Plugin management tool, used for FZF vim plugin
    https://github.com/junegunn/vim-plug
    """
    if ask and ask_yes_no("Install vim-plug plugins?"):
        vimrc = os.path.join(target, ".vimrc")
        subprocess.call(["vim", "-u", vimrc, "+PlugInstall"])


def main():
    home_path = os.path.expanduser("~")
    target = sys.argv[1] if len(sys.argv) > 1 else home_path
    return configure_vim(target) and 1 or 0


if __name__ == "__main__":
    sys.exit(main())
