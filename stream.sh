#cvlc dvb://frequency=578000000 -v --sout '#transcode{soverlay,ab=42,samplerate=44100,channels=1,acodec=mp4a,vcodec=h264,width=320,height=180,vfilter="canvas{width=320,height=180,aspect=16:9}",fps=25,vb=200,venc=x264{vbv-bufsize=500,partitions=all,level=12,no-cabac,subme=7,threads=4,ref=2,mixed-refs=1,bframes=0,min-keyint=1,keyint=50,trellis=2,direct=auto,qcomp=0.0,qpmax=51}}:gather:rtp{mp4a-latm,sdp=rtsp://192.168.1.14:5004/vid.sdp}'


#cvlc -v dvb://frequency=578000000 \
#--sout "#transcode{vcodec=h264,vb=600,fps=20,scale=0.25,acodec=mp4a,ab=48,channels=2,samplerate=44100}:gather:std{access=http{mime=video/3gpp},mux=3gp,dst=0.0.0.0:8080/vid.3gp}"

cvlc -v dvb://frequency=578000000 \
--sout "#transcode{vcodec=h264,vb=600,fps=20,scale=0.25,acodec=mp4a,ab=48,channels=2,samplerate=44100}:gather:std{access=http{mime=video/mp4},mux=3gp,dst=0.0.0.0:8080/vid.mp4}"
