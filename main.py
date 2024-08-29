
from turtle import Turtle, Screen
import random

bullets = []
invaders = []
in_bullets = []


class Invader(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape('square')
        self.shapesize(stretch_wid=1, stretch_len=1)
        self.penup()
        self.goto(x, y)
        self.seth(0)
        self.dx = 0.5
        # self.shoot_timer = random.randint(5, 10)
        # self.shoot_delay = 0

    def moving(self):
        self.setx(self.xcor() + self.dx)
        if self.xcor() > screen.window_width() / 2 - 20 or self.xcor() < -screen.window_width() / 2 + 20:
            self.dx *= -1
            self.sety(self.ycor() - 2)

    def shooting(self):
        in_bullet = Bullet(x_pos=self.xcor(), y_pos=self.ycor(), head=-1)
        in_bullets.append(in_bullet)


class Bullet(Turtle):
    def __init__(self, x_pos, y_pos, head):
        super().__init__()
        self.shape('square')
        self.shapesize(stretch_wid=0.2, stretch_len=1)
        self.penup()
        self.goto(x_pos, y_pos)
        self.speed(1)
        self.seth(90)
        self.dy = 15 * head

    def moving(self):
        new_y = self.ycor() + self.dy
        self.goto(self.xcor(), new_y)
        return new_y


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('turtle')
        self.shapesize(1.5, 1.5)
        self.penup()
        self.goto(self.xcor(), -250)
        self.seth(90)

    def move_right(self):
        if self.xcor() < screen.window_width() / 2 - 20:
            self.setx(self.xcor() + 10)
            screen.update()

    def move_left(self):
        if self.xcor() > -screen.window_width() / 2 + 20:
            self.setx(self.xcor() - 10)
            screen.update()

    def shoot(self):
        bullet = Bullet(self.xcor(), self.ycor() + 10, 1)
        bullets.append(bullet)
        screen.update()


def check_collision():
    for bullet in bullets:
        for invader in invaders:
            if bullet.distance(invader) < 20:
                bullet.hideturtle()
                bullet.clear()
                bullets.remove(bullet)
                invader.hideturtle()
                invaders.remove(invader)
                break
        if bullet.ycor() > screen.window_height() / 2:
            bullet.hideturtle()
            bullet.clear()
            bullets.remove(bullet)

    for b in in_bullets:
        if b.distance(player) < 20:
            b.hideturtle()
            b.clear()
            in_bullets.remove(b)
            game_over()

    if any(invader.ycor() < -screen.window_height() / 2 + 50 for invader in invaders):
        game_over()


def game_over():
    global game_is_on
    print('game over')
    game_is_on = False

screen = Screen()
screen.setup(width=800, height=600)
screen.tracer(0)

player = Player()

x_start = -300
y_start = 250
for i in range(4):
    for j in range(7):
        invader = Invader(x=x_start + j * 60, y=y_start - i * 30)
        invaders.append(invader)

screen.listen()
screen.onkeypress(key='d', fun=player.move_right)
screen.onkeypress(key='a', fun=player.move_left)
screen.onkeypress(key='space', fun=player.shoot)
timer = 100

game_is_on = True

while game_is_on:
    for invader in invaders:
        invader.moving()
    timer = timer - 1
    if timer < 0:
        chosen_in = random.choice(invaders)
        chosen_in.shooting()
        timer = 100

    for bullet in in_bullets:
        if bullet.moving() < -screen.window_height() / 2:
            bullet.hideturtle()
            bullet.clear()
            in_bullets.remove(bullet)

    for bullet in bullets:
        if bullet.moving() > screen.window_height() / 2:
            bullet.hideturtle()
            bullet.clear()
            bullets.remove(bullet)

    check_collision()

    screen.update()

screen.exitonclick()
