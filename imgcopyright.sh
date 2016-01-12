#!/bin/sh

#
# imgcopyright.sh - watermark images with a (c) notice
#

# Requires ImageMagick convert & composite

#
# ToDo:
#      Calculate size of notice, based on size of image & size of text
#      Do this programatically in PGslideshow & call watermark() or 
#      equivalent function to generate website images
#

watermark() { WMTEXT="$1"; ORIGFILE="$2"; NEWFILE="$3"
#convert -size 1200x200 xc:none -font /cygdrive/c/Windows/Fonts/arial.ttf -pointsize 72 -kerning 1 -gravity Center -fill black -fill white -annotate 0 "$WMTEXT" -auto-orient /tmp/WATERMARK_FILE.png
convert -size 600x200 xc:none -font /cygdrive/c/Windows/Fonts/arial.ttf -pointsize 72 -kerning 1 -gravity Center -fill black -fill white -annotate 0 "$WMTEXT" -auto-orient /tmp/WATERMARK_FILE.png

composite -gravity SouthEast -dissolve 40% /tmp/WATERMARK_FILE.png "$ORIGFILE" "$NEWFILE"
}

USAGE=0
OWNER="$1"
FILE1="$(cygpath "$2")"
FILE2="$(cygpath "$3")"

if [ "X$OWNER" = "X" ]; then
  printf "No arguments!\n"
  USAGE=1
elif [ -z "$FILE1" ]; then
  printf "No filename specified!\n"
  USAGE=1
elif [ ! -f "$FILE1" ]; then
  printf "Cannot find original file!\n"
  USAGE=1
fi
if [ -f "$FILE2" ]; then
  printf "Destination file already exists!\n"
  USAGE=1
fi
if [ ! -z $4 ]; then
  printf "Too many arguments!\n"
  USAGE=1
fi

if [ $USAGE -gt 0 ]; then
  printf "Usage:\n$0 {Owner's name} {Filename} {New filename}\n"
  exit 1
fi

watermark "© ${OWNER}" "${FILE1}" "${FILE2}"

