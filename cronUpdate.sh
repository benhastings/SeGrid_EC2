#!/bin/bash

line="*/5 * * * * python ~/phantomCron.py"
(crontab -u ubuntu -l; echo "$line") | crontab -u ubuntu -
