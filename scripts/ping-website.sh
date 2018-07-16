#!/usr/bin/env bash
#
# Checks if website is able to be retrieved. Otherwise sends an email saying it's down.
#

WEBSITE="0xbu.com"
TO_EMAIL="contact@0xbu.com"
FROM_EMAIL="observer@0xbu.com"
MESSAGE="The 0xBU.com website did not properly load for the daily uptime check. This alert was initiated from 'ping-website.sh'"
SUBJECT="$WEBSITE is down!"

if ! wget "$WEBSITE" -O /dev/null; then
    echo "$MESSAGE" | mailx -r "$FROM_EMAIL" -s "$SUBJECT" "$TO_EMAIL"
fi

