from distutils.core import setup
import pygame
import pygame.freetype
from pygame.locals import *
from pygame import K_q, K_f, K_t, K_s, K_w, K_m, K_n, K_SPACE, K_LEFT, K_RIGHT
import os
import sys
import array
import datetime


def displayimage(imagefile,imagenum,timevar):
    isurf = pygame.image.load(imagefile)
    isurf = aspect_scale(isurf, screen)
    irect = isurf.get_rect()
    imgwidth = isurf.get_width()
    imgheight = isurf.get_height()
    if screenwidth > imgwidth:
        irect.move_ip(int((screenwidth-imgwidth)/2),0)
    if screenheight > imgheight:
        irect.move_ip(0,int((screenheight-imgheight)/2))
    screen.blit(isurf,irect,area=None, special_flags = 0)
    pygame.display.flip()
    pygame.time.wait(30 * timevar)

    myfont.render_to(screen,imagenumpos,"{:0>2d}".format(imagenum+1),pygame.Color('#B0B0B0FF'))
    pygame.display.flip()
    pygame.time.wait(20 * timevar)

    if THUMBS_DONE == 0:
        ithumb = pygame.transform.scale(screen, (thumbwidth,thumbheight))
        blitresult=tsurf.blit(ithumb,(thumbx[imagenum],thumby[imagenum]))
    screen.fill(pygame.Color('#00000000'))
    pygame.display.flip()

def showimage(imagefile):
    isurf = pygame.image.load(imagefile)
    isurf = aspect_scale(isurf, screen)
    irect = isurf.get_rect()
    imgwidth = isurf.get_width()
    imgheight = isurf.get_height()
    if screenwidth > imgwidth:
        irect.move_ip(int((screenwidth-imgwidth)/2),0)
    if screenheight > imgheight:
        irect.move_ip(0,int((screenheight-imgheight)/2))
#    screen.fill(pygame.Color('#00000000'))
    screen.blit(isurf,irect,area=None, special_flags = 0)
    pygame.display.flip()
#    for x in range(8):
#        y = 2**x
#        y = y - 1
##        print(y)
#        isurf.set_alpha(y)
#        screen.fill(pygame.Color(0,0,0))
#        screen.blit(isurf,irect)
#        pygame.display.update()



## Found at https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=80229&p=571235
## - might be useful:
def image_fade(self, image_name):
    background = pygame.image.load(name)
    background = pygame.transform.scale(background,(imgsize[0],imgsize[1])).convert()

    for x in range(0,255):
        background.set_alpha(x)
        screen.fill(pygame.Color(0,0,0))
        screen.blit(background, (0, 0))
        pygame.display.update()
        x += 1
##
##

## Derived from fn at http://www.pygame.org/pcr/transform_scale/
## Takes two surfaces - fit img into disp
def aspect_scale(img, disp):
    bx=disp.get_width()
    by=disp.get_height()
    ix,iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx/float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by/float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx/float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by
    return pygame.transform.scale(img, (int(sx),int(sy)))
##
##

def opj(*args):
    path = os.path.join(*args)
    return os.path.normpath(path)

def find_files(srcdir, extn):
    file_list = []
    for file in sorted(os.listdir(srcdir)):
        if file.endswith(extn):
            file_list.append(opj(srcdir,file))
    return file_list

def find_dirs(srcdir):
    dir_list = []
    for file in sorted(os.listdir(srcdir)):
        if os.path.isdir(opj(srcdir,file)):
            dir_list.append(opj(srcdir,file))
    return dir_list

def display_thumbs(THUMBS_DONE):
    if THUMBS_DONE == 0:
        imgcntr = 0
        for jpgfile in jpgfiles:
            displayimage(jpgfile,imgcntr,0)
            imgcntr += 1
        THUMBS_DONE = 1
    screen.blit(tsurf,(0,0),area=None, special_flags = 0)
    pygame.display.update()
    
def showimages():
    imgcntr = 0
    while True:
        screen.fill(pygame.Color('#00000000'))
        isurf = pygame.image.load(jpgfiles[imgcntr])
        isurf = aspect_scale(isurf, screen)
        irect = isurf.get_rect()
        imgwidth = isurf.get_width()
        imgheight = isurf.get_height()
        if screenwidth > imgwidth:
            irect.move_ip(int((screenwidth-imgwidth)/2),0)
        if screenheight > imgheight:
            irect.move_ip(0,int((screenheight-imgheight)/2))
        screen.blit(isurf,irect,area=None, special_flags = 0)
        pygame.display.update()
        event = pygame.event.wait()
        if event.type == KEYDOWN:
            if event.key in (K_q, K_m):
                break
            elif event.key in (K_SPACE, K_RIGHT):
                imgcntr += 1
            elif event.key == K_LEFT:
                imgcntr -= 1
            if imgcntr >= numfiles:
                imgcntr = numfiles - 1
            if imgcntr < 1:
                imgcntr = 0


def display_menu(logofile):
    menufont=pygame.freetype.SysFont('Consolas',14)
    lsurf = screen.copy()
    lsurf.fill(pygame.Color('#00000000'))
    lsurf = pygame.image.load(logofile)
    screen.blit(lsurf,(0,0),area=None, special_flags = 0)
    def menu_text(menutext,menuitem):
        menupos = (int(screenwidth/2)-100,int(screenheight/2)+(menuitem*20))
        menufont.render_to(screen,menupos,menutext,pygame.Color('#B0B0B0FF'))
        menuitem = menuitem + 1
        return menuitem
    menuitem = 0
    menuitem = menu_text('t ... Thumbnails',menuitem)
    menuitem = menu_text('s ... Slideshow (for voting)',menuitem)
    menuitem = menu_text('n ... Normal Slideshow',menuitem)
    menuitem = menu_text('w ... Write thumbnail image',menuitem)
    menuitem = menu_text('f ... Write index file',menuitem)
    menuitem = menu_text('m ... Return to this Menu',menuitem)
    menuitem = menu_text('q ... Quit',menuitem)
    menuitem = menu_text('Directory: ' + imagedir,menuitem+1)
    pygame.display.flip()

def initialise_thumbs(numthumbs):
    #
    # Setup the thumbnail geometry. Squares will
    # do - this only sacrifices symmetry, not size
    #
    gridsize = 0
    square = 0
    while square < numthumbs:
        gridsize += 1
        square = gridsize ** 2
    thumbx = array.array('i',(0,) * square)
    thumby = array.array('i',(0,) * square)
    thumbwidth = int((screenwidth - (gridsize * 20)) / gridsize)
    thumbheight = int((screenheight - (gridsize * 20)) / gridsize)
    xcount = gridsize
    ycount = gridsize
    imgcntr = 0
    for ty in range(ycount):
        for tx in range(xcount):
            thumbx[imgcntr]=int(10 + ((tx) * (thumbwidth + 20)))
            thumby[imgcntr]=int(10 + ((ty) * (thumbheight + 20)))
            imgcntr += 1
    return (thumbwidth, thumbheight, thumbx, thumby)

##
## Main block starts here
##
if len(sys.argv) > 3:
    otherstuff=list("")
    (myname, logofile, startdir, otherstuff) = sys.argv
    PGdebug=1
    print("Extra args received: " + otherstuff + "\n")
    print("\nDebugging ON\n")
elif len(sys.argv) < 3:
    print("Not enough args! - received:\n")
    for arg in sys.argv:
         print("\t" + arg + "\n")
    sys.exit(1)
else:
    (myname, logofile, startdir) = sys.argv
    PGdebug=0

TIME_DILATION=150

#
# Enumerate dirs and jpg files.
# Assume the filenames already have randomised prefixes for now
#
dirlist=find_dirs(startdir)
if len(dirlist) == 0:
    imagedir = startdir
else:
    imagedir = dirlist[0]
jpgfiles = find_files(imagedir, ".jpg")
numfiles = len(jpgfiles)

#
# Initialisation
#
THUMBS_DONE = 0
pygame.init()
pygame.mouse.set_visible(False)

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen.fill(pygame.Color(0,0,0))
(screenwidth,screenheight) = pygame.Surface.get_size(screen)

# Now scaling img numbers with the display size
#myfont = pygame.freetype.SysFont('Arial',240)
#imagenumpos = (screenwidth-250,20)
imagenumsiz = int(screenheight / 5)
myfont = pygame.freetype.SysFont('Arial',imagenumsiz)
imagenumpos = (screenwidth-int(imagenumsiz * 1.1),20)


#
# Display logo / menu
#
display_menu(logofile)
#
# Setup thumbnail surface
#
tsurf = screen.copy()
tsurf.fill(pygame.Color('#00000000'))
(thumbwidth, thumbheight, thumbx, thumby) = initialise_thumbs(numfiles)

#
# Event handling loop
#
while True:
    event = pygame.event.wait()
    if event.type == KEYDOWN:
        if event.key == K_q:
            break
        elif event.key == K_t:
            screen.blit(tsurf,tsurf.get_rect(),area=None, special_flags = 0)
            display_thumbs(THUMBS_DONE)
        elif event.key == K_m:
            screen.fill(pygame.Color('#00000000'))
            display_menu(logofile)
        elif event.key == K_n:
            showimages()
            screen.fill(pygame.Color('#00000000'))
            display_menu(logofile)
        elif event.key == K_f:
            thumbstamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
            f = open(imagedir + "/00FL-" + thumbstamp + ".txt",'w')
            f.write(imagedir + '\n' + thumbstamp + '\n\n')
            imgcntr = 0
            for jpgfile in jpgfiles:
                f.write(format(imgcntr+1, '02d') + ' ' + os.path.basename(jpgfile) + '\n')
                imgcntr += 1
            f.close()
        elif event.key == K_s:
            screen.fill(pygame.Color('#00000000'))
            imgcntr = 0
            for jpgfile in jpgfiles:
                displayimage(jpgfile,imgcntr,TIME_DILATION)
                imgcntr += 1
            pygame.time.wait(10 * TIME_DILATION)
            THUMBS_DONE = 1
            display_thumbs(THUMBS_DONE)
        elif event.key == K_w:
            thumbstamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
            pygame.image.save(tsurf,imagedir + "/00TN-" + thumbstamp + ".png")
#
# Exit
#
pygame.quit()
sys.exit(PGdebug)

