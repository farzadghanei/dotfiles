# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)


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

# simple prompt
export PS1="\[\e[32m\]\u\[\e[m\]@\[\e[36m\]\h\[\e[m\] \W \$?$ "

# app specific
# fzf binding
[ -f ~/.fzf.bash ] && source ~/.fzf.bash

# aliases
alias 'll=ls -lF --color'
alias 'la=ls -alF --color'

# env
export VISUAL=vim
export EDITOR=vim
