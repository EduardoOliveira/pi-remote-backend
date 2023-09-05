#!/bin/bash

base_path='/home/pi/mjpg-streamer/mjpg-streamer-experimental'
export LD_LIBRARY_PATH=$base_path
$base_path/mjpg_streamer -i "input_libcamera.so -r 1920x1080 -f 10 -b 4 -s 4656x3496" -o "output_http.so -w $base_path/www"