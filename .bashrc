# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# interactive session settings
[ -z "$PS1" ] && return

# command history tweaks (from soltysh/dotfiles)
# don't record duplicate lines
HISTCONTROL=ignoredups:ignorespace
HISTSIZE=1000
HISTFILESIZE=2000
HISTINGORE='ls:bg:fg:history'
HISTTIMEFORMAT='%F %T '

# append to the history file, don't overwrite it
shopt -s histappend

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
shopt -s globstar

# prompt with hostname
# export PS1="\[\e[32m\]\u\[\e[m\]@\[\e[36m\]\h\[\e[m\] \W \$?$ "
# simple prompt
export PS1="\[\e[36m\]\h\[\e[m\] \W \$?$ "

# aliases
alias ll='ls -lF --color'
alias la='ls -laF --color'

alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# env
export VISUAL=vim
export EDITOR=vim

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# app specific
# fzf binding
[ -f ~/.fzf.bash ] && source ~/.fzf.bash
