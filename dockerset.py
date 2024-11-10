sudo docker run -it --runtime nvidia \
  --device /dev/video0 \                        
  --device /dev/nvhost-gpu \                     
  --device /dev/nvmap \                         
  -v /home/jetson/data:/workspace \              
  -e DISPLAY=$DISPLAY \                         
  -e QT_X11_NO_MITSHM=1 \                        
  -v /tmp/.X11-unix:/tmp/.X11-unix \            
  --privileged \                                
  ultralytics/ultralytics:latest-jetson-jetpack4 

