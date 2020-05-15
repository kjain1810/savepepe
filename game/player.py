import pygame


class player(object):
    def __init__(self, x, y, width, height, obstacle_speed):
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.vel = 3
        self.score = 0
        self.obstacle_speed = obstacle_speed
        self.dead = False
        self.bottom_range = self.y + self.height
        self.bottom_range = self.y + self.height  # horizontal line at bottom
        self.top_range = self.y  # horizontal line at top
        self.left_range = self.x  # vertical line towards the left
        self.right_range = self.x + self.width  # vertical line towards the right
        self.top_left_x = self.x  # topleft corner - x coordinate
        self.top_left_y = self.y  # topleft corner - y coordinate
        self.top_right_x = self.x + self.width  # topright corner - x coordinate
        self.top_right_y = self.y  # topright corner - y coordinate
        self.bottom_left_x = self.x  # bottomleft corner - x coordinate
        self.bottom_left_y = self.y + self.height  # bottomleft corner - y coordinate
        self.bottom_right_x = self.x + self.width  # bottomright corner - x coordinate
        self.bottom_right_y = self.y + self.height  # bottomright corner - y coordinate

    def draw(self, win, which_image):
        win.blit(pygame.image.load(which_image), (self.x, self.y))

    def rect(self):  # collision boxes
        return pygame.Rect(self.x+3, self.y+2, self.width-6, self.height-4)

    def update_pos(self):  # update collision boxes when the object moves
        self.bottom_range = self.y + self.height
        self.top_range = self.y
        self.left_range = self.x
        self.right_range = self.x + self.width
        self.top_left_x = self.x
        self.top_left_y = self.y
        self.top_right_x = self.x + self.width
        self.top_right_y = self.y
        self.bottom_left_x = self.x
        self.bottom_left_y = self.y + self.height
        self.bottom_right_x = self.x + self.width
        self.bottom_right_y = self.y + self.height
