#!/bin/bash
find /usr/local/fioul_recuperation/log/log -mtime +30 -name "*.log" -exec rm -rf {} \;
find /usr/local/fioul_recuperation/log/debug -mtime +30 -name "*.log" -exec rm -rf {} \;

pgrep firefox | xargs kill -s 9
pgrep geckodriver | xargs kill -s 9
pgrep python3 | xargs kill -s 9
pgrep begin.sh | xargs kill -s 9

rm -rf /tmp/rust*
rm -rf /tmp/tmp*
rm -rf /usr/local/fioul_recuperation/geckodriver.log
rm -rf /usr/local/fioul_recuperation/console.log

. /etc/profile
. ~/.bash_profile
cd /usr/local/fioul_recuperation/
/usr/bin/python3 lancer_fioul_recuperation.py
