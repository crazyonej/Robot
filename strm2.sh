raspivid -o - -n -fps 15 -w 1280 -h 720 -t 0 \ |cvlc -vvv stream:///dev/stdin \ --sout '#rtp{sdp=rtsp://:8554/}' \ :demux=h264 :h264-fps=15