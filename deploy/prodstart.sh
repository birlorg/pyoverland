#!/bin/sh
echo "TODO: use uwsgi or something."
export MODE="PROD"
exec /home/zie/.local/bin/uv run ./main.py mydata.db
