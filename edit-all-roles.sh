#!/bin/sh

# set -e: exit script immediately upon error
# set -u: treat unset variables as an error
# set -o pipefail: cause a pipeline to fail, if any command within it fails
set -eu -o pipefail

cd ~/.ansible && vi $(grep -rl '^ ' roles |grep -v 'tests/test.yml' |grep -v 'meta/main.yml' |grep -v 'README.md' |grep -v '.travis.yml' |grep -v 'smb.conf' |sort) "$@"

echo ""
cat host_vars/*
echo ""
cat site.yml
echo ""
ls -l *.yml |grep -v site.yml |grep -v test.yml |grep -v uptime.yml
echo ""
ls -alR roles/*/files/*
echo ""
ls -alR roles/*/templates/*
