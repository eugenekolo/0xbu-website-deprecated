#!/usr/bin/env bash

INSTALL_DIR="/home/`whoami`/0xbu-website"
BACKUP="0xbu.bak-$(date +%Y-%m-%d).7z"
MESSAGE="A biweekly backup of 0xBU data is attached. The password is 'backup'"
SUBJECT="Biweekly backup of 0xBU data"
TO_EMAIL="contact@0xbu.com"
FROM_EMAIL="backup@0xbu.com"

# Create a local backup first
7z a "$BACKUP" -mhe -pbackup "$INSTALL_DIR/ghost"
cp "$BACKUP" /home/`whoami`/.0xbu-backups

# Send backup to remote
(uuencode $BACKUP $BACKUP.7zx; echo "$MESSAGE") | mailx -r "$FROM_EMAIL" -s "$SUBJECT" "$TO_EMAIL"

# Clean up
rm "$BACKUP"

