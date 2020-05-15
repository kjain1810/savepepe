import pygame
from player import *


class _fonts(object):
    def __init__(self):
        # font used
        self.font_used = "dejavusans"
        # colors used
        self.win_col = (66, 135, 245)
        self.lose_col = (170, 65, 250)
        self.draw_col = (255, 255, 255)
        self.lev_col = (106, 179, 235)
        self.header_col = (240, 234, 122)
        self.black = (0, 0, 0)
        # messages
        self.p2_win = 'PLAYER 2 WINS!'
        self.p1_win = 'PLAYER 1 WINS!'
        self.p1 = 'PLAYER 1'
        self.p2 = 'PLAYER 2'
        self.draw = 'ITS A DRAW!!!!'
        self.score = 'Score: '
        self.level = 'LEVEL: '
        # images used
        self.player_alive = 'heart.png'
        self.player_dead = 'broken_heart.png'
        self.dead_avatar = 'dead.png'
        self.win_avatar = 'win.png'
        self.p1_avatar = 'p1.png'
        self.p2_avatar = 'p2.png'


class sounds(object):
    def __init__(self):
        # music and sound effects used
        self.death = 'burn_music.wav'
        self.bg = 'background_music.mp3'
        self.com = 'finish.wav'


def inc_speed(p):
    # increase speed of the player by 1
    p.obstacle_speed += 1
    return p
