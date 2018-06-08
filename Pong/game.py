# import the necessary packages
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
from pygame.locals import *
from random import choice, randint
import pygame
import sys


pygame.init()
fps = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Globals
WIDTH = 600
HEIGHT = 600

window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("Pong")


# game.py --shape-predictor shape_predictor_68_face_landmarks.dat

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
                help="path to facial landmark predictor")
args = vars(ap.parse_args())

# Video capture source
cap = cv2.VideoCapture(0)

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])


class Player:
    def __init__(self):
        self.width = 100
        self.height = 10
        self.color = WHITE
        self.x = 0
        self.y = HEIGHT - 10 - self.height

    def draw(self):
        pygame.draw.rect(window, self.color,
                         Rect((self.x, self.y), (self.width, self.height)))


class Computer:
    def __init__(self):
        self.width = 100
        self.height = 10
        self.color = WHITE
        self.x = WIDTH // 2 - self.width // 2
        self.y = 10

    def draw(self):
        pygame.draw.rect(window, self.color,
                         Rect((self.x, self.y), (self.width, self.height)))


class Ball:
    def __init__(self):
        self.radius = 10
        self.color = (0, 255, 0)
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.vector = [choice([-5, 5]), randint(-5, 5)]


    def draw(self):
        pygame.draw.circle(window, WHITE, (self.x, self.y), self.radius)


class Game:
    def __init__(self):
        self.player = Player()
        self.computer = Computer()
        self.ball = Ball()
        self.status = True

    def draw(self):
        window.fill(BLACK)

        pygame.draw.line(window, WHITE, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 1)
        self.player.draw()
        self.computer.draw()
        self.ball.draw()

    def play(self):
        while self.status:

            ret, image = cap.read()

            image = imutils.resize(image, width=500)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            rects = detector(gray, 1)


            for (i, rect) in enumerate(rects):
                x, y, w, h = face_utils.rect_to_bb(rect)

            cv2.imshow("Output", image)

            self.player.x = x

            self.draw()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # keys = pygame.key.get_pressed()
            # if keys[K_LEFT]:
            #     self.player.x -= 5
            # if keys[K_RIGHT]:
            #     self.player.x += 5

            self.ball.x += self.ball.vector[0]
            self.ball.y += self.ball.vector[1]

            pygame.display.update()
            fps.tick(60)



if __name__ == "__main__":
    game = Game()
    game.play()
