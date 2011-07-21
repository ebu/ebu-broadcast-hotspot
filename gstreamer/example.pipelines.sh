#!/bin/sh

GSTL=gst-launch-0.10

# convert v4l source to h263 + 3gp encoded file
#$GSTL v4l2src num-buffers=50 ! queue ! ffenc_h263 ! gppmux ! filesink location=video.3gp

# get video from dvblast
#$GSTL udpsrc uri=udp://239.10.10.1:2721 ! mpegtsdemux name=demux ! queue max-size-buffers=0 max-size-time=0 ! mpeg2dec ! xvimagesink demux. ! queue max-size-buffers=0 max-size-time=0 ! mad ! alsasink


$GSTL -v  udpsrc uri=udp://239.10.10.1:2721 ! mpegtsdemux name=demux ! queue max-size-buffers=0 max-size-time=0 ! \
    mpeg2dec ! ffenc_h263 ! filesink location=video.h263 # gppmux ! filesink location=video.3gp #\
    #demux. ! queue max-size-buffers=0 max-size-time=0 ! mad ! filesink location=audio.mp3

