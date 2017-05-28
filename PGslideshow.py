#!/usr/bin/env python
"""
A pygame program to show a slideshow of all images buried in a given directory.

Originally Released: 2007.10.31 (Happy halloween!)

# TODO:
- ken burns
- dont scroll if not neccessary


"""
import argparse
import os
import stat
import sys
import time
import random

import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

file_list = []  # a list of all images being shown
title = "pgSlideShow | My Slideshow!"  # caption of the window...
waittime = 1   # default time to wait between images (in seconds)


def walktree(top, callback):
    """recursively descend the directory tree rooted at top, calling the
    callback function for each regular file. Taken from the module-stat
    example at: http://docs.python.org/lib/module-stat.html
    """
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname)[stat.ST_MODE]
        if stat.S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname, callback)
        elif stat.S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print 'Skipping %s' % pathname


def addtolist(file, extensions=['.png', '.jpg', '.jpeg', '.gif', '.bmp']):
    """Add a file to a global list of image files."""
    global file_list  # ugh
    filename, ext = os.path.splitext(file)
    e = ext.lower()
    # Only add common image types to the list.
    if e in extensions:
        print 'Adding to list: ', file
        file_list.append(file)
    else:
        print 'Skipping: ', file, ' (NOT a supported image)'



def input(events):
    """A function to handle keyboard/mouse/device input events. """
    for event in events:  # Hit the ESC key to quit the slideshow.
        if (event.type == QUIT or
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            pygame.quit()



def main(startdir="."):
    global file_list, title, waittime

    pygame.init()

    # Test for image support
    if not pygame.image.get_extended():
        print "Your Pygame isn't built with extended image support."
        print "It's likely this isn't going to work."
        sys.exit(1)

    modes = pygame.display.list_modes()
    pygame.display.set_mode(max(modes), pygame.DOUBLEBUF | pygame.HWSURFACE)
    pygame.display.set_caption(title)
    pygame.display.toggle_fullscreen()
    screen = pygame.display.get_surface()
    pygame.mouse.set_visible(False)

    while (True):
        read_files_and_present(startdir, screen, waittime)

        

def read_files_and_present(startdir, screen, waittime):
    global file_list
    file_list = []
    
    walktree(startdir, addtolist)  # this may take a while...
    if len(file_list) == 0:
        print "Sorry. No images found. Exiting."
        sys.exit(1)

    modes = pygame.display.list_modes()    

    current = 0
    num_files = len(file_list)

    # sort files by filename
    file_list = sorted(file_list)
    # shuffle the images in clusters
    clustered_shuffled_list = []
    cluster_sizes = 8
    c = 0
    cluster_a = []
    cluster_b = []
    for i in range(num_files):
        if c == cluster_sizes:
            clustered_shuffled_list.append(cluster_a)
            clustered_shuffled_list.append(cluster_b)
            cluster_a = []
            cluster_b = []
            c = 0

        if random.random() > 0.5:
            cluster_a.append(file_list[i])
        else:
            cluster_b.append(file_list[i])

        c = c+1

    clustered_shuffled_list.append(cluster_a)
    clustered_shuffled_list.append(cluster_b)

    random.shuffle(clustered_shuffled_list)

    image_filelist = [image for cluster in clustered_shuffled_list for image in cluster]
        
    
    for i in range(100):
        imagefile = image_filelist[current]
        display_image(imagefile, screen, max(modes), waittime)
        pygame.mouse.set_pos(int(random.random()*1000), int(random.random()*1000))
        
        # When we get to the end, re-start at the beginning
        current = (current + 1) % num_files;



def display_image(imagefile, screen, display_mode, waittime):
    try:
        img = pygame.image.load(imagefile).convert(24)
        scroll_steps = waittime/2

        #obtain image properties
        img_w = img.get_width()
        img_h = img.get_height()
        display_w = display_mode[0]
        display_h = display_mode[1]

        # calculate image ratio
        img_r = float(img_w)/float(img_h)
        display_r = float(display_w)/float(display_h)

        smallest_w = min(img_w, display_w)
        smallest_h = min(img_h, display_h)

        offset = 0
        
        if img_r > display_r:
            if (smallest_h < display_h):
                dominant_color = get_dominant_color(img)
                screen.fill(dominant_color)
                offset = (display_h - smallest_h)/2
            img = pygame.transform.smoothscale(img, (int(smallest_h*img_r), smallest_h))
            
            pan_image_horizontally(img, screen, display_mode, scroll_steps, offset, waittime)
        else:
            if (smallest_w < display_w):
                dominant_color = get_dominant_color(img)
                screen.fill(dominant_color)
                offset = (display_w - smallest_w)/2
            img = pygame.transform.smoothscale(img, (smallest_w, int(smallest_w/img_r)))
            pan_image_vertically(img, screen, display_mode, scroll_steps, offset, waittime)      

        input(pygame.event.get())
        #sys.exit(1)
    except pygame.error as err:
        print "Failed to display %s: %s" % (file_list[current], err)

def average(lst):
    return sum(lst)/len(lst)

def median(lst):
    lst = sorted(lst)
    return lst[len(lst)/2]

def close_mean(lst):
    divider = 5
    lst = [int((i-1)/divider) for i in lst]
    mc = most_common(lst)
    return mc*divider + divider/2

def most_common(lst):
    return max(set(lst), key=lst.count)

def get_dominant_color(img):
    pixarray = pygame.PixelArray(img)
    colors = []
    maxcount = 0
    maxcolor = 0
    color_steps = 6
    color_gap = int(256.0/float(color_steps) + 0.5)
    
    for i in range(pixarray.shape[0]):
        if (i % 3 == 0):
            for j in range(pixarray.shape[1]):
                if (j % 3 == 0):
                    #rgbc = pygame.Color(pixarray[i,j]*256 + 255)
                    pixel = img.get_at((i,j))
                    r = pixel[0]
                    g = pixel[1]
                    b = pixel[2]
                    colorint = r/color_gap*color_steps*color_steps + g/color_gap*color_steps + b/color_gap
                    colors.append(colorint)
                    
    fcolor = most_common(colors)

    dominant_color = pygame.Color( ((fcolor/color_steps/color_steps)%color_steps)*color_gap+color_gap/2, ((fcolor/color_steps)%color_steps)*color_gap+color_gap/2, ((fcolor)%color_steps)*color_gap+color_gap/2, 255)

    return dominant_color
            
def milli_time():
    return int(round(time.time() * 1000))

def delay_if_neccessary(elapsed, required):
    if required > elapsed:
        time.sleep(float(required - elapsed)/1000.0)

def pan_image_vertically(img, screen, display_mode, scroll_steps, offset, waittime):
    img_h = img.get_height()
    display_h = display_mode[1]

    overlap_distance = img_h - display_h
    overlap_distance_factor = float(overlap_distance) / scroll_steps
    wait_per_step = float(waittime)*1000.0/scroll_steps
    
    reverse = random.random() > 0.5    
    
    for i in range(scroll_steps):
        ts = milli_time()
        if (reverse):
            screen.blit(img, (offset, 0- overlap_distance + int(i*overlap_distance_factor)))
        else:
            screen.blit(img, (offset, 0-int(i*overlap_distance_factor)))
        input(pygame.event.get())
        pygame.display.update()
        input(pygame.event.get())
        te = milli_time()

        delay_if_neccessary(te-ts, wait_per_step)
        
    


def pan_image_horizontally(img, screen, display_mode, scroll_steps, offset, waittime):
    img_w = img.get_width()
    display_w = display_mode[0]

    overlap_distance = img_w - display_w
    overlap_distance_factor = overlap_distance / scroll_steps
    wait_per_step = float(waittime)*1000.0/scroll_steps

    reverse = random.random() > 0.5    
    
    for i in range(scroll_steps):
        ts = milli_time()
        if (reverse):
            screen.blit(img, (0- overlap_distance + int(i*overlap_distance_factor), offset))
        else:
            screen.blit(img, (0-int(i*overlap_distance_factor), offset))
        input(pygame.event.get())
        pygame.display.update()
        input(pygame.event.get())
        te = milli_time()
        
        delay_if_neccessary(te-ts, wait_per_step)

        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Recursively loads images '
        'from a directory, then displays them in a Slidshow.'
    )

    parser.add_argument(
        'path',
        metavar='ImagePath',
        type=str,
        default='.',
        nargs="?",
        help='Path to a directory that contains images'
    )
    parser.add_argument(
        '--waittime',
        type=int,
        dest='waittime',
        action='store',
        default=600,
        help='Amount of time to wait before showing the next image.'
    )
    parser.add_argument(
        '--title',
        type=str,
        dest='title',
        action='store',
        default="pgSlidShow | My Slideshow!",
        help='Set the title for the display window.'
    )
    args = parser.parse_args()
    waittime = args.waittime
    title = args.title
    main(startdir=args.path)
