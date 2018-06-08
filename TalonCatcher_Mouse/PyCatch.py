# 1 - Import library
import pygame
import random
import time
import threading
import sys
from threading import Thread
from operator import itemgetter
from pygame.locals import *
import numpy as np
import cv2

#Initial Declarations
red   = 255,   0,   0
green =   0, 255,   0
blue  =   0,   0, 255
white = 255, 255, 255

GAMEPHASE = 0 #0 = menu, 1=game, 2=other menu item
size = width, height = 800, 500
screen = pygame.display.set_mode((width, height))
screen = pygame.display.set_mode((1920, 1080))


background = pygame.image.load("resources/background.jpg")
background_inverted = pygame.image.load("resources/background-inverted.jpg")


pygame.mouse.set_visible(False)

score = 0
newObj = False
lives = 5

Running = True
speed = [0, 20]
inscores = False
invert = False

leveltext = "Easy"

previous_success=0


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# face_cascade = cv2.CascadeClassifier('closed_frontal_palm.xml')
# face_cascade = cv2.CascadeClassifier('cascade.xml')

cap = cv2.VideoCapture(0)

def kek():
    global previous_success
    ret, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    res, res_m = [], []
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        res.append([(x, y), (x+w, y+h),(w,h), w*h])
        res_m.append(w*h)

    biggest = list(filter(lambda x: x[3] == max(res_m), res))
    # print(biggest)
    # print(biggest[0][0][0]+biggest[0][2][0]//2)
    if biggest:
        cv2.circle(img, (biggest[0][0][0]+biggest[0][2][0]//2, biggest[0][0][1]+biggest[0][2][1]//2), 10, (0, 0, 255), -1)
        cv2.rectangle(img, biggest[0][0], biggest[0][1], (0, 255, 0), 2)
        previous_success=biggest[0][0][0]+biggest[0][2][0]//2
        # last_success=previous_success
    # else:
        # last_success=previous_success

    cv2.imshow('img', img)
    return biggest[0][0][0]+biggest[0][2][0]//2 if biggest else previous_success





class Oneup(pygame.sprite.Sprite):
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        if invert:
            self.oneup = pygame.image.load("resources/1up-inverted.png")
        elif not invert:
            self.oneup = pygame.image.load("resources/1up.png")
        self.oneuprect = self.oneup.get_rect()
        self.oneuprect = self.oneuprect.move(x, -50)
        self.rect = self.oneuprect
    def update(self):
        if self.rect.bottom > 920:
            self.kill()
        self.oneuprect = self.oneuprect.move(speed)
        screen.blit(self.oneup, self.oneuprect)
        self.rect = self.oneuprect

class Ball(pygame.sprite.Sprite):
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        if invert:
            self.ball = pygame.image.load("resources/ball-inverted.png")
        elif not invert:
            self.ball = pygame.image.load("resources/ball.png")
        self.ballrect = self.ball.get_rect()
        self.ballrect = self.ballrect.move(x, -50)
        self.rect = self.ballrect
        global newObj
        newObj = False
    def update(self):
        if self.rect.bottom > 920:
            self.kill()
        self.ballrect = self.ballrect.move(speed)
        screen.blit(self.ball, self.ballrect)
        self.rect = self.ballrect

class Bomb(pygame.sprite.Sprite):
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        if invert:
            self.bomb = pygame.image.load("resources/bomb-inverted.png")
        elif not invert:
            self.bomb = pygame.image.load("resources/bomb.png")
        self.bombrect = self.bomb.get_rect()
        self.bombrect = self.bombrect.move(x, -50)
        self.rect = self.bombrect

    def update(self):
        if self.rect.bottom > 920:
            self.kill()
        self.bombrect = self.bombrect.move(speed)
        screen.blit(self.bomb, self.bombrect)
        self.rect = self.bombrect

    def explode(self):
        global explosionobj
        explosionobj = Explosion(self.rect.topleft)
        explosionobj.explode()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, coordinates):
        pygame.sprite.Sprite.__init__(self)
        self.Exploding = False
        self.explosionindex = 0
        self.x, self.y = coordinates
        global explosionimgs
        self.explosionimgs = []
        for i in range(0, 47):
            self.explosionimgs.append(pygame.image.load("resources/explosion2/%d.png" % (i)))
        self.explosionimg = self.explosionimgs[self.explosionindex]
        global explosionfx
        explosionfx = pygame.mixer.Sound("resources/explosion.wav")

    def explode(self):
        explosionfx.play()
        self.Exploding = True
        self.explosionindex = 0

    def update(self):
        if self.Exploding and self.explosionindex < 47:
            screen.blit(self.explosionimgs[self.explosionindex], (self.x-80, self.y-80))
            self.explosionindex += 1
            if self.explosionindex == 47:
                self.kill()

    def stopExploding(self):
        self.Exploding = False
        self.kill()



class Bucket(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        if invert:
            self.bucket = pygame.image.load("resources/bucket-inverted.png")
        elif not invert:
            self.bucket = pygame.image.load("resources/bucket.png")
        self.bucketrect = self.bucket.get_rect()
        #self.bucketrect = self.bucketrect.move(50,50)
        self.rect = self.bucketrect

    def update(self):
        x, y = 1,0
        self.rect.midtop = (2000-3*kek(),800)
        screen.blit(self.bucket, self.rect)
        self.rect = self.bucketrect

class Lives(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.livesimg = pygame.image.load("resources/heart.png")
        self.livesrect = self.livesimg.get_rect()
        self.rect = self.livesrect
    def update(self):
        for i in range(lives):
            screen.blit(self.livesimg, (i*26+1600, 50))


class Timer():
    def __init__(self, seconds):
        print ("Timer started")
        self.seconds = seconds

    def start(self):
        global newObj
        newObj = True
        self.t = threading.Timer(self.seconds,self.start)
        self.t.start()

    def stop(self):
        self.t.cancel()



def blowWind(on):
    global speed
    if on:
        speed[0] = random.choice([-3,3])
    elif not on:
        speed[0] = 0


pygame.mixer.init()
explosionobj = Explosion([0,0])
pygame.mixer.music.load("resources/happy.mp3")


def main():
    #Init screen
    pygame.init()
    global score
    global explosionobj
    global Running
    global lives
    global InGame

    InGame = True
    pygame.key.set_repeat(500, 30)
    bg = background
    myfont = pygame.font.SysFont("monospace", 38)

    ballgroup = pygame.sprite.Group()
    bombgroup = pygame.sprite.Group()
    oneupgroup = pygame.sprite.Group()
    bucketobj = Bucket()
    livesobj = Lives()
    blowWind(False)
    pygame.mixer.music.play(-1)

    while Running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                Running = False
                break

        scoretext = myfont.render("Score {0}".format(score), 1, (0, 0, 0))
        diftext = myfont.render("{0}".format(leveltext), 1, (0, 0, 0))



        if random.randrange(0, 70) < 1:
            ballgroup.add(Ball(random.randint(0,1920)))

        if random.randrange(0,50) < 1:
            bombgroup.add(Bomb(random.randint(0,1920)))

        if random.randrange(0,1000) < 1:
            oneupgroup.add(Oneup(random.randint(0,1920)))

        screen.blit(background, (0, 0))

        screen.blit(scoretext, (5, 10))
        screen.blit(diftext, (1750, 900))

        ballgroup.update()
        bombgroup.update()
        bucketobj.update()
        livesobj.update()
        oneupgroup.update()
        explosionobj.update()
        pygame.display.update()

        if pygame.sprite.spritecollide(bucketobj, oneupgroup, True):
            lives += 1
        if pygame.sprite.spritecollide(bucketobj, ballgroup, True):
            score += 1
        list = pygame.sprite.spritecollide(bucketobj, bombgroup, True)
        for i in list:
            if i is not None:
                i.explode()
                lives -= 1


        if lives == 0:
            InGame = False
            gameovertext = myfont.render("Game Over", 1, (0, 0, 0))

            for i in range(0,47):
                screen.blit(bg, (0, 0))
                explosionobj.update()
                pygame.display.update()
            screen.blit(gameovertext, (350,200))
            explosionobj.stopExploding()
            #Kill Sprites
            for ball in ballgroup:
                ball.kill()
            for bomb in bombgroup:
                bomb.kill()
            for oneups in oneupgroup:
                oneups.kill()

            pygame.display.update()
            time.sleep(2)



if __name__ == '__main__': main()
