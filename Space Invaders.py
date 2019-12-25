import _tkinter
import pygame
import math
import turtle
import random


bullet_state = "ready"
pygame.mixer.init()
bullet_sound = pygame.mixer.Sound("laser.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")


def set_screen_stats():
    wn.screensize(550, 550)
    wn.setup(580,580)
    wn.bgcolor('blue')
    wn.title('Space Invaders: Version 1.0')
    wn.bgpic("space_invaders_background.gif")


def make_border():
    b = turtle.Turtle()
    b.speed(0)
    b.color('white')
    b.penup()
    b.setposition(-255,-253)
    b.pendown()
    b.pensize(5)

    for side in range(4):
        b.forward(510)
        b.left(90)
    b.end_fill()
    b.hideturtle()


# move the player left and right
def move_left():

    x = player.xcor()
    x -= player_speed
    if x >= -240:
        player.setx(x)


def move_right():
    x = player.xcor()
    x += player_speed
    if x <= 240:
        player.setx(x)


def make_bullet():
    m = turtle.Turtle()
    m.hideturtle()
    m.color('blue')
    m.penup()
    m.speed(0)
    m.setheading(90)
    m.shape('triangle')
    m.shapesize(0.5,0.5)
    m.setposition(player.xcor(),player.ycor()-20)

    return m


# fires bullet
def fire_bullet():
    global bullet_state
    if bullet_state == 'ready':
        pygame.mixer.Sound.play(bullet_sound)
        bullet_state = 'fire'
        x = player.xcor()
        y = player.ycor() + 15
        bullet.setposition(x,y)
        bullet.showturtle()


def is_collision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(),2) + math.pow(t1.ycor() - t2.ycor(),2) )
    if distance < 15:
        return True
    else:
        return False


turtle.register_shape("player.gif")
turtle.register_shape("invader.gif")


wn = turtle.Screen()
set_screen_stats()
make_border()

# set score
score = 0

score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color('white')
score_pen.penup()
score_pen.setposition(-250,230)
score_string = "Score: %s" %score
score_pen.write(score_string,False,align='left',font=("Arial",14,"normal"))
score_pen.hideturtle()

# make_player
player = turtle.Turtle()
player.shape('player.gif')
player.penup()
player.speed(0)
player.setheading(90)
player.setposition(0, -170)
player.color('green')

player_speed = 15

# creates keyboard bindings
turtle.listen()
turtle.onkeypress(move_left, 'Left')
turtle.onkeypress(move_right, 'Right')
turtle.onkeypress(fire_bullet, 'space')

# creates enemy

enemy_speed = 1

number_of_enemies = 5
enemies = []

for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())

for enemy in enemies:
    enemy.shape('invader.gif')
    enemy.penup()
    enemy.speed(2)
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.setposition(x, y)
    enemy.color('yellow')


# create bullet
bullet = make_bullet()
bullet_speed = 20


try:
    # main game loop
    while True:
        for enemy in enemies:
            x = enemy.xcor()
            x += enemy_speed
            enemy.setx(x)

            # moves the enemy down
            if enemy.xcor() >= 240:
                # moves all enemies down
                for e in enemies:
                    y = e.ycor()
                    y -= 30
                    e.sety(y)
                enemy_speed *= -1

            if enemy.xcor() <= -240:
                for e in enemies:
                    y = e.ycor()
                    y -= 30
                    e.sety(y)
                enemy_speed *= -1

                # checks for collisions
            if is_collision(bullet, enemy):
                pygame.mixer.Sound.play(explosion_sound)
                # reset bullet
                bullet_state = 'ready'
                bullet.setposition(0, -400)

                # reset enemy
                enemy.hideturtle()
                x = random.randint(-200, 200)
                y = random.randint(100, 250)
                enemy.setposition(x, y)
                score += 10
                score_string = "Score: %s" % score
                score_pen.clear()
                score_pen.write(score_string, False, align='left', font=("Arial", 14, "normal"))
                enemy.showturtle()

            if is_collision(player, enemy):
                player.hideturtle()
                enemy.hideturtle()
                print('Game Over')
                turtle.bye()
                break
        # moves the bullet
        if bullet_state == 'fire':
            y = bullet.ycor()
            y += bullet_speed
            bullet.sety(y)

        # changes state of bullet
        if bullet.ycor() >= 275:
            bullet_state = 'ready'


except _tkinter.TclError:
    print('')









