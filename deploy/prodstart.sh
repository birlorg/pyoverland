#!/bin/sh
echo "TODO: use uwsgi or something."
export MODE="PROD"
exec /home/zie/.cargo/bin/uv run ./main.py mydata.db
