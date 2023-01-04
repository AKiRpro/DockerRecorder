#!/bin/bash

Xvfb :99 -screen 0 1920x1080x16 -nolisten tcp &

pulseaudio -D --exit-idle-time=-1

pulseaudio -D --exit-idle-time=-1 --system

pacmd load-module module-virtual-sink sink_name=v1

pacmd set-default-sink v1

pacmd set-default-source v1.monitor

python3 handler.py

sleep 10000
