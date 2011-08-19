#!/bin/sh

# OGG
# cvlc -v http://localhost:40003 \
#    --sout "#transcode{vcodec=none,acodec=vorb,ab=256,channels=2,samplerate=48000}:http{dst=:8080/c3.ogg}"

# MP3
cvlc -v http://localhost:40003 \
   --sout "#transcode{vcodec=none,acodec=mp3,ab=320,channels=2,samplerate=48000}:http{dst=:8080/c3.mp3}"
