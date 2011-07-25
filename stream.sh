# Streaming of a valid mp4 file through RTP:
#vlc -v ~/Videos/documentariesandyou.mp4 --sout \
#"#rtp{dst=139.10.10.1,port=6024-6025,sdp=rtsp://10.73.141.81:5004/vid.sdp}"

# Streaming of DVB:
cvlc -v dvb://frequency=578000000 --sout \
"#transcode{vcodec=mp4v,vb=400,fps=20,scale=0.3,acodec=mp4a,ab=48,channels=2,samplerate=44100}:gather:rtp{dst=139.10.10.1,port=6024-6025,sdp=rtsp://10.73.141.81:5004/vid.sdp}"

# use the following URI on the client:
#rtsp://10.73.141.81:5004/vid.sdp
