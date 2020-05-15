import pygame


class obstacle(object):
    def __init__(self, x, y, height, width, vel_1, vel_2):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        # game is 1-indexed, 0 index is dummy
        self.vel_p = [0, vel_1, vel_2]
        # game is 1-indexed, 0 index is dummy
        self.crossed_p = [False, False, False]
        if self.vel_p[1] == 0:  # if velocity is 0, the obstacle is a bomb, otherwise a bullet
            self.img = [pygame.image.load(
                'bomb_correct.png'), pygame.image.load('bomb_correct.png')]
        else:
            self.img = [pygame.image.load(
                'bullet_left.png'), pygame.image.load('bullet_right.png')]
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

    def draw(self, win, left):
        if left:  # get the correct image according to direction
            win.blit(self.img[0], (self.x, self.y))
        else:
            win.blit(self.img[1], (self.x, self.y))

    def rect(self):
        if self.vel_p[1] == 0:  # collision boxes
            return pygame.Rect(self.x, self.y+7, self.width-6, self.height-5)
        else:
            return pygame.Rect(self.x, self.y+12, self.width, self.height-23)

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
