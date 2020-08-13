#!/bin/sh
cd $(dirname "$0")

wget -O .screenrc http://git.grml.org/f/grml-etc-core/etc/grml/screenrc_generic
wget -O .tmux.conf http://git.grml.org/f/grml-etc-core/etc/tmux.conf
wget -O .vimrc http://git.grml.org/f/grml-etc-core/etc/vim/vimrc
wget -O .zshrc http://git.grml.org/f/grml-etc-core/etc/zsh/zshrc
wget -O .zshrc.local http://git.grml.org/f/grml-etc-core/etc/skel/.zshrc
