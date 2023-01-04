#!/bin/bash

echo "run Xvfb ising 99 screen"
Xvfb $DISPLAY -screen 0 1920x1080x16 &
sleep 5

echo "run browser(firefox) on virtual frame"
# firefox --display=${DISPLAY} --kiosk 'https://recdev.collaborate.center/localrec/?env=staging&userId=124970&conferenceId=816536&recId=17084&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImN0eSI6IkpXVCJ9.eyJjb250ZXh0Ijp7InVzZXIiOnsiYXZhdGFyIjoiKiIsIm5hbWUiOiJyZWNvcmRpbmdOYW1lIiwiZW1haWwiOiJyZWNvcmRpbmdAZ21haWwuY29tIn19LCJhdWQiOiJyZWNvcmRlciIsImlzcyI6ImNvbGxhYm9yYXRlLmNlbnRlciIsInN1YiI6ImNvbmZlcmVuY2UuYnJpZGdlLWRldi5jb2xsYWJvcmF0ZS5jZW50ZXIiLCJyb29tIjoiKiIsImV4cCI6MTY2NjY5NjYwNH0.i6aSPffnvFkx30mFOZD5W_eGQpXd4aBWVgIllpYgTNw' &
firefox --display=$DISPLAY --kiosk 'https://www.webfx.com/tools/whats-my-browser-size/' &
sleep 5

echo "record 30 seconds using ffmpeg (if you want no time limit, remove `-t 30` option)"
ffmpeg -video_size 1920x1080 -framerate 25 -f x11grab -i $DISPLAY -t 30 -f pulse -i v1.monitor -ac 2 output/output.mp4

