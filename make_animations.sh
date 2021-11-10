# generate pallette for conversion to use, avoids weird artifacts in the gradient scale
ffmpeg -pattern_type glob -i 'frames/world_scale/world_*.png' -vf palettegen palette.png
# generate a MP4 and animated GIF for the world map
ffmpeg -f image2 -framerate 4 -pattern_type glob -i  'frames/world_scale/*png' -i palette.png -lavfi paletteuse -pix_fmt yuv420p -c:v libx264  world.mp4
ffmpeg -f image2 -framerate 4 -pattern_type glob -i  'frames/world_scale/*png' -i palette.png -lavfi paletteuse -pix_fmt bgr8 world.gif
# generate a MP4 and animated GIF for the north american map
ffmpeg -f image2 -framerate 4 -pattern_type glob -i  'frames/na_1280/*png' -i palette.png -lavfi paletteuse -pix_fmt yuv420p na.mp4
ffmpeg -f image2 -framerate 4 -pattern_type glob -i  'frames/na_1280/*png' -i palette.png -lavfi paletteuse -pix_fmt bgr8 na.gif
