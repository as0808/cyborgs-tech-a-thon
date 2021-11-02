# SpaceWar by @TokyoEdTech / Written in Python 2.7
# Part VIII: Multiple Enemies/ Multiple Allies

import os
import random
import time
import winsound

# Import the Turtle module
import turtle
wn=turtle.Screen()
# Required by MacOSX to show the window
turtle.fd(0)
# Set the animations speed to the maximum
turtle.speed(0)
# Change the background color
turtle.bgcolor("black")
turtle.bgpic("background.gif")
#changing window title
turtle.title("spacewar")
# Hide the default turtle
turtle.ht()
# This saves memory
turtle.setundobuffer(1)
# This speeds up drawing
turtle.tracer(0)

#class sprite to define basic objects of the game, it inherits turtle module
class Sprite(turtle.Turtle):
    #defining constructor with required parameters
    def __init__(self, spriteshape, color, startx, starty):
        #since it's a child class, parent class ka constructor
        turtle.Turtle.__init__(self, shape=spriteshape)
        #all sprites when the game starts will have these properties
        #speed of animation
        self.speed(0)
        #don't want sprites to draw anything on the screen
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

        #boundary detection
        if self.xcor()>290:
            self.setx(290)
            self.rt(60)
        if self.xcor()<-290:
            self.setx(-290)
            self.rt(60)
        if self.ycor()>290:
            self.sety(290)
            self.rt(60)
        if self.ycor()<-290:
            self.sety(-290)
            self.rt(60)

    def is_collision(self, other):
        if(self.xcor()>=(other.xcor() - 20)) and \
        (self.xcor() <= (other.xcor() + 20)) and \
        (self.ycor() >= (other.ycor() - 20)) and \
        (self.ycor() <= (other.ycor() + 20)):
            return True
        else:
            return False



#since player sprite is unique among other sprites, we'll make it's own class. it's a child class of sprite class
class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
        self.speed=4
        self.lives=3

    def turn_left(self):
        self.lt(45)

    def turn_right(self):
        self.rt(45)

    def accelerate(self):
        self.speed +=1

    def decelerate(self):
        self.speed -=1

class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed=6
        self.setheading(random.randint(0,360))

class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed=8
        self.setheading(random.randint(0,360))

    def move(self):
        self.fd(self.speed)

        #boundary detection
        if self.xcor()>290:
            self.setx(290)
            self.lt(60)
        if self.xcor()<-290:
            self.setx(-290)
            self.lt(60)
        if self.ycor()>290:
            self.sety(290)
            self.lt(60)
        if self.ycor()<-290:
            self.sety(-290)
            self.lt(60)

class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.2, stretch_len=0.4, outline=None)
        self.speed=20
        self.status="ready"
        #will go offscreen
        self.goto(-1000,1000)

    def fire(self):
        if self.status=="ready":
            winsound.PlaySound("fire.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status="firing"

    def move(self):
        if self.status=="ready":
            # will go off screen
            self.goto(-1000,1000)

        if self.status=="firing":
            self.fd(self.speed)

        #Border check
        if self.xcor()<-290 or self.xcor()>290 or \
            self.ycor()<-290 or self.ycor()>290:
            self.goto(-1000,1000)
            self.status="ready"

class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000,-1000)
        self.frame=0

    def explode(self, startx, starty):
        self.goto(startx,starty)
        self.setheading(random.randint(0,360))
        #frame sothat exploded particle goes upto only 20px
        self.frame=1

    def move(self):
        if self.frame>0:
            self.fd(10)
            self.frame+=1

        if self.frame>10:
            self.frame=0
            self.goto(-1000,-1000)



class Game():
    def __init__(self):
        self.level =1
        self.score =0
        self.state ="playing"
        self.pen   =turtle.Turtle()
        self.lives =3

    def draw_border(self):
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        #starts at 0,0
        self.pen.goto(-300,300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        #hide the pen
        self.pen.ht()
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        msg="Score: %s" %(self.score)
        self.pen.penup()
        self.pen.goto(-300,310)
        self.pen.write(msg,font=("Arial",16,"normal"))

#create game object
game=Game()

#draw border
game.draw_border()

#show game status
game.show_status()

#creating sprites
player = Player("triangle","white",0,0)
# enemy  = Enemy("circle","red",-100,0)
missile = Missile("triangle","yellow",0,0)
# ally = Ally("square","blue",100,0)

enemies=[]
for i in range(6):
    enemies.append(Enemy("circle","red",-100,0))

allies=[]
for i in range(3):
    allies.append(Ally("square","blue",100,0))

particles=[]
for i in range(20):
    particles.append(Particle("circle","orange",0,0))

#keyboard bindings
turtle.onkey(player.turn_left,"Left")
turtle.onkey(player.turn_right,"Right")
turtle.onkey(player.accelerate,"Up")
turtle.onkey(player.decelerate,"Down")
turtle.onkey(missile.fire,"space")
turtle.listen()

#main game loop
while True:
    turtle.update()
    time.sleep(0.05)
    player.move()
    # enemy.move()
    missile.move()
    # ally.move()

    for ally in allies:
        ally.move()
        #check for collision
        if missile.is_collision(ally):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            missile.status = "ready"
            game.score -= 50
            game.show_status()

    for enemy in enemies:
        enemy.move()
        # check for conclusion
        if player.is_collision(enemy):
            winsound.PlaySound("explosion.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            game.score -= 100
            game.show_status()

        if missile.is_collision(enemy):
            winsound.PlaySound("explosion.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            missile.status = "ready"
            game.score += 100
            game.show_status()
            #for explosion
            for particle in particles:
                particle.explode(missile.xcor(),missile.ycor())


    for particle in particles:
        particle.move()


delay=input("press enter to finish. >")
