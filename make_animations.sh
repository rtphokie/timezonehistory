ffmpeg -r 1/5 -f image2 -s 1920x1080 -pix_fmt yuv420p -pattern_type glob -i 'north_america_*.png' -c:v libx264 na.mp4
ffmpeg -r 1/5 -f image2 -s 1920x1080 -pix_fmt yuv420p -pattern_type glob -i 'world_*.jpg' -c:v libx264 world.mp4
