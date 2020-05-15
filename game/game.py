import pygame
import time
from player import player
from obstacle import obstacle
from random import seed
from random import randint
from config import _fonts
from config import inc_speed
from config import sounds

pygame.init()

pygame.display.set_caption("ISS Assignment 3")

to_play = sounds()

music = pygame.mixer.music.load(to_play.bg)
death = pygame.mixer.Sound(to_play.death)
com = pygame.mixer.Sound(to_play.com)

pygame.mixer.music.play(-1)

window_edge = 900

win = pygame.display.set_mode((window_edge, window_edge))

clock = pygame.time.Clock()

player_edge = 30

# the game is one indexed, hence p[0] is a dummy player
p = [player(0, 0, 0, 0, 0), player(window_edge/2 - player_edge/2, window_edge - player_edge, player_edge,
                                   player_edge, 1), player(window_edge/2 - player_edge/2, window_edge - player_edge, player_edge, player_edge, 1)]

header = ((0, 0), (window_edge, window_edge/10))
which_player = 1

finished = False  # flag to check if game has finished
isdead = False  # flag to check if someone just died
who_died = 0  # if someone died, stores who
did_complete = False  # flag to check if someone just completed the level
who_completed = 0  # if someone completed the level, who

obsheights = [187, 285, 382, 480, 567, 665, 762]


def display_base_board():
    configurations = _fonts()
    pygame.draw.rect(win, (255, 255, 255),
                     ((0, 0), (window_edge, window_edge)))
    pygame.draw.rect(win, (87, 215, 230), header)

    pygame.draw.rect(win, (158, 245, 66),
                     ((0, window_edge/10), (window_edge, player_edge)))
    pygame.draw.rect(win, (158, 245, 66), ((
        0, window_edge-player_edge), (window_edge, player_edge)))

    for i in obsheights:
        pygame.draw.rect(win, (245, 120, 98),
                         ((0, i), (window_edge, player_edge)))

    pygame.font.init()
    myfont = pygame.font.SysFont(configurations.font_used, 60)
    textsurface = myfont.render(
        configurations.level + str(level), False, configurations.header_col)
    win.blit(textsurface, (650, 15))
    myfont = pygame.font.SysFont(configurations.font_used, 60)
    if which_player == 1:
        textsurface = myfont.render(
            configurations.p1, False, configurations.header_col)
    else:
        textsurface = myfont.render(
            configurations.p2, False, configurations.header_col)
    if not p[2].dead:
        win.blit(pygame.image.load(configurations.player_alive), (850, 90))
    else:
        win.blit(pygame.image.load(configurations.player_dead), (850, 90))
    if not p[1].dead:
        win.blit(pygame.image.load(configurations.player_alive), (850, 870))
    else:
        win.blit(pygame.image.load(configurations.player_dead), (850, 870))
    win.blit(textsurface, (10, 15))
    myfont = pygame.font.SysFont(configurations.font_used, 25)
    if p[1].score == p[2].score:  # if scores are tied, both get the color of a draw
        textsurface_1 = myfont.render(
            configurations.score + str(p[1].score), False, configurations.draw_col)
        textsurface_2 = myfont.render(
            configurations.score + str(p[2].score), False, configurations.draw_col)
    elif p[1].score > p[2].score:  # if p1 is in lead, give colors accordingly
        textsurface_1 = myfont.render(
            configurations.score + str(p[1].score), False, configurations.win_col)
        textsurface_2 = myfont.render(
            configurations.score + str(p[2].score), False, configurations.lose_col)
    else:  # if p2 is in lead, give colors accordingly
        textsurface_1 = myfont.render(
            configurations.score + str(p[1].score), False, configurations.lose_col)
        textsurface_2 = myfont.render(
            configurations.score + str(p[2].score), False, configurations.win_col)
    win.blit(textsurface_1, (0, 870))
    win.blit(textsurface_2, (0, 90))


def draw_game_board():
    configurations = _fonts()
    global isdead
    global did_complete
    if isdead:
        death.play()
        display_base_board()
        for x in obs:
            # to decide if the object is moving or stationary
            if which_player == 1 and x.vel_p[1] < 0:
                x.draw(win, True)
            # to decide if the object is moving or stationary
            elif which_player == 2 and x.vel_p[2] < 0:
                x.draw(win, True)
            else:
                x.draw(win, False)
        p[who_died].draw(win, configurations.dead_avatar)
        pygame.display.update()
        time.sleep(2)
        if not p[3-who_died].dead:
            # correct score that is reduced due to the 2 second pause
            p[3-who_died].score += 2
        isdead = False
        # if the other player is still alive, get a new board
        if who_died == 2 and not p[1].dead:
            get_obs()
    elif did_complete:
        com.play()
        display_base_board()
        for x in obs:
            # to decide if the object is moving or stationary
            if which_player == 1 and x.vel_p[1] < 0:
                x.draw(win, True)
            # to decide if the object is moving or stationary
            elif which_player == 2 and x.vel_p[2] < 0:
                x.draw(win, True)
            else:
                x.draw(win, False)
        p[who_completed].draw(win, configurations.win_avatar)
        pygame.display.update()
        time.sleep(2)
        did_complete = False
        if not p[3-who_completed].dead:
            p[3-who_completed].score += 2
        if who_completed == 2:  # get new board if its a new level
            get_obs()
        if who_completed == 1 and p[2].dead:
            get_obs()
        p[who_completed].x = window_edge/2 - \
            player_edge/2  # start from base position now
        if who_completed == 1:
            # deciding y axis based on player
            p[1].y = window_edge - player_edge
        else:
            p[2].y = window_edge/10
    if finished:
        pygame.draw.rect(win, (123, 123, 123),
                         ((0, 0), (window_edge, window_edge)))
        pygame.font.init()
        myfont = pygame.font.SysFont(configurations.font_used, 45, True)
        if p[1].dead and not p[2].dead:
            textsurface = myfont.render(
                configurations.p2_win, False, configurations.black)
        elif not p[1].dead and p[2].dead:
            textsurface = myfont.render(
                configurations.p1_win, False, configurations.black)
        else:
            if p[1].score > p[2].score:
                textsurface = myfont.render(
                    configurations.p1_win, False, configurations.black)
            elif p[2].score > p[1].score:
                textsurface = myfont.render(
                    configurations.p2_win, False, configurations.black)
            else:
                textsurface = myfont.render(
                    configurations.draw, False, configurations.black)
        win.blit(textsurface, (320, 450))
    else:
        display_base_board()
        if which_player == 1:
            p[which_player].draw(win, configurations.p1_avatar)
        else:
            p[which_player].draw(win, configurations.p2_avatar)
        for x in obs:
            # to decide if the object is moving or stationary
            if which_player == 1 and x.vel_p[1] < 0:
                x.draw(win, True)
            # to decide if the object is moving or stationary
            elif which_player == 2 and x.vel_p[2] < 0:
                x.draw(win, True)
            else:
                x.draw(win, False)

    pygame.display.update()


run = True


def exitfromgame():
    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            pygame.quit()

        draw_game_board()


cur_time = time.time()

obs = []


def get_obs():
    global obs
    obs = []
    bullet_per_row = 3
    for i in range(7 * bullet_per_row):
        movdir = randint(0, 1)
        if movdir == 0:
            movdir = -1
        # for even distribution of obstacle across the board, divide x axis into 3 parts
        # ranges will be between (window_edge/bullet_per_row)*x and (window_edge/bullet_per_row)*(x+1) for the xth division
        # did a -player_edge to stop the image from overflowing
        obs_here = obstacle(randint((window_edge // bullet_per_row)*(i % bullet_per_row), (window_edge // bullet_per_row)*(
            i % bullet_per_row+1)-player_edge), obsheights[i//bullet_per_row], 30, 30, p[1].obstacle_speed * movdir, p[2].obstacle_speed * movdir)
        obs.append(obs_here)
    free_space_heights = [120, 217, 315, 412, 510, 597, 695, 792]
    bomb_per_row = 6
    for i in range(bomb_per_row*8):
        obs_here = obstacle(randint((window_edge//bomb_per_row) * (i % bomb_per_row), (window_edge//bomb_per_row) * (
            i % bomb_per_row + 1) - 30), randint(free_space_heights[i//bomb_per_row], free_space_heights[i//bomb_per_row]+30), 30, 30, 0, 0)
        obs.append(obs_here)


get_obs()

level = 1

while run:
    clock.tick(60)

    if p[1].dead and p[2].dead:
        exitfromgame()
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    time_here = time.time()

    if int(time_here - cur_time) != 0:
        p[which_player].score -= int(time_here - cur_time)
        cur_time = time_here

    if keys[pygame.K_SPACE]:
        run = False

    # keys for player one
    if keys[pygame.K_UP] and p[which_player].y > window_edge/10 and which_player == 1:
        p[which_player].y -= p[which_player].vel
    if keys[pygame.K_DOWN] and p[which_player].y < window_edge - player_edge and which_player == 1:
        p[which_player].y += p[which_player].vel
    if keys[pygame.K_LEFT] and p[which_player].x > 0 and which_player == 1:
        p[which_player].x -= p[which_player].vel
    if keys[pygame.K_RIGHT] and p[which_player].x < window_edge - player_edge and which_player == 1:
        p[which_player].x += p[which_player].vel

    # keys for player two
    if keys[pygame.K_w] and p[which_player].y > window_edge/10 and which_player == 2:
        p[which_player].y -= p[which_player].vel
    if keys[pygame.K_s] and p[which_player].y < window_edge - player_edge and which_player == 2:
        p[which_player].y += p[which_player].vel
    if keys[pygame.K_a] and p[which_player].x > 0 and which_player == 2:
        p[which_player].x -= p[which_player].vel
    if keys[pygame.K_d] and p[which_player].x < window_edge - player_edge and which_player == 2:
        p[which_player].x += p[which_player].vel

    # update the player's collision box
    p[which_player].update_pos()

    # updating the obstacles and scores
    for ob in obs:
        ob.x += ob.vel_p[which_player]
        ob.x = min(ob.x, window_edge - player_edge)
        ob.x = max(ob.x, 0)
        # if the obstacle reaches one of the edges, flip the velocity
        if ob.x == 0 or ob.x == window_edge - player_edge:
            ob.vel_p[which_player] *= -1
        # if the player crosses an obstacle it hadn't already crossed, increase score
        # for moving objects, the score change is their speed, for stationary, its 1
        if which_player == 1 and p[which_player].y <= ob.y - player_edge and ob.crossed_p[which_player] == False:
            ob.crossed_p[which_player] = True
            p[which_player].score += max(ob.vel_p[which_player],
                                         max(-ob.vel_p[which_player], 1))
        elif which_player == 2 and p[which_player].y >= ob.y + player_edge and ob.crossed_p[which_player] == False:
            ob.crossed_p[which_player] = True
            p[which_player].score += max(ob.vel_p[which_player],
                                         max(-ob.vel_p[which_player], 1))
        # update the obstacle's collision box
        ob.update_pos()

    for x in obs:  # checking for collisions
        if p[which_player].rect().colliderect(x.rect()):
            p[which_player].dead = True
            who_died = which_player
            if which_player == 1:
                if not p[2].dead:  # if p2 is not dead, we need to continue the game
                    isdead = True
                    which_player = 2
                    #set the starting position as the default position
                    p[which_player].x = window_edge/2 - player_edge/2
                    p[which_player].y = window_edge/10
                    for ob in obs:  # the obstacles should continue running in the same directions from the same positions
                        if ob.vel_p[1] < 0 and ob.vel_p[2] > 0:
                            ob.vel_p[2] *= -1
                        elif ob.vel_p[1] > 0 and ob.vel_p[2] < 0:
                            ob.vel_p[2] *= -1
                else:  # if p2 is dead as well, finish the game
                    isdead = True
                    finished = True
                    exitfromgame()
                break
            else:
                if p[1].dead:  # if p1 is dead as well, finish the game
                    isdead = True
                    finished = True
                    exitfromgame()
                else:  # if p2 is not dead, we need to continue the game
                    #if p2 died but p1 is alive, there is going to be a new board
                    #so we need not update directions here
                    isdead = True
                    which_player = 1
                    p[1].x = window_edge/2 - player_edge/2
                    p[1].y = window_edge - player_edge
                    level += 1

    if which_player == 1 and p[which_player].y <= window_edge/10:
        did_complete = True
        who_completed = 1
        p[1] = inc_speed(p[1])
        if not p[2].dead:  # if p2 is alive, p2 will take the same board
            which_player = 2
            # p2 gets the starting position which was p1's ending position
            p[which_player].x = p[1].x
            # p2 gets the starting position which was p1's ending position
            p[which_player].y = p[1].y
            for ob in obs:  # obstacles should continue running in the same direction
                if ob.vel_p[1] < 0 and ob.vel_p[2] > 0:
                    ob.vel_p[2] *= -1
                elif ob.vel_p[1] > 0 and ob.vel_p[2] < 0:
                    ob.vel_p[2] *= -1
        else:  # if p2 is dead, we will need a new board
            which_player = 1
            level += 1
    elif which_player == 2 and p[which_player].y >= window_edge - player_edge:
        did_complete = True
        who_completed = 2
        p[2] = inc_speed(p[2])
        if not p[1].dead:  # if p1 is alive, p1 will get a new board
            which_player = 1
            # p1 gets the starting position which was p2's ending position
            p[1].x = p[2].x
            # p1 gets the starting position which was p2's ending position
            p[1].y = p[2].y
            level += 1
        else:  # if p1 is dead, p2 will get a new board
            which_player = 2
            level += 1

    draw_game_board()
