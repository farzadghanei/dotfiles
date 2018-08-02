#!/usr/bin/env python

import sys
import os
import shutil
import subprocess

dotfiles = os.path.dirname(os.path.dirname(__file__))


def ask_yes_no(msg, default_accept=True):
    default = ' [Y/n] ' if default_accept else ' [y/N] '
    ans = raw_input(msg + default).strip().lower()
    if default_accept:
        return ans != 'n'
    return ans == 'y'


def configure_vim(target, ask=True):
    if not ask_yes_no("Configure vim on: '{}'?".format(target)):
        return False
    copy_dot_vim(dotfiles, target, ask)
    install_plugins_with_plug(target, ask)


def copy_dot_vim(src, dst, ask=True):
    src_vimrc = os.path.join(src, '.vimrc')
    dst_vimrc = os.path.join(dst, '.vimrc')

    src_dot_vim = os.path.join(src, '.vim')
    dst_dot_vim = os.path.join(dst, '.vim')

    if os.path.exists(dst_vimrc):
        if ask and not ask_yes_no(
                "Replace existing vimrc on '{}'?".format(dst_vimrc)):
            raise IOError("Destination vimrc exists on '{}'".format(dst_vimrc))
        os.remove(dst_vimrc)
    shutil.copy(src_vimrc, dst_vimrc)

    if os.path.exists(dst_dot_vim):
        if ask and not ask_yes_no(
                "Replace existing .vim on '{}'?".format(dst_dot_vim)):
            raise IOError(
                "Destination .vim exists on '{}'".format(dst_dot_vim))
        shutil.rmtree(dst_dot_vim)
    shutil.copytree(src_dot_vim, dst_dot_vim)


def install_plugins_with_plug(target, ask):
    """
    Plugin management tool, used for FZF vim plugin
    https://github.com/junegunn/vim-plug
    """
    if ask and ask_yes_no("Install vim-plug plugins?"):
        vimrc = os.path.join(target, '.vimrc')
        subprocess.call(['vim', '-u', vimrc, '+PlugInstall'])


def main():
    home_path = os.path.expanduser('~')
    target = sys.argv[1] if len(sys.argv) > 1 else home_path
    return configure_vim(target) and 1 or 0


if __name__ == '__main__':
    sys.exit(main())
