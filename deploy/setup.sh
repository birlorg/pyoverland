#!/bin/sh
SERVICE=pyoverlander.service
systemctl link ./${SERVICE}
systemctl enable ${SERVICE}
systemctl start ${SERVICE}
systemctl status ${SERVICE}
