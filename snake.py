"""Simple Snake Game using Python's built-in turtle module.

Controls: Arrow keys or W/A/S/D to move, Space to restart, Esc to quit.
"""

import random
import turtle

STEP = 20            
LIMIT = 280          
DELAY_MS = 100       

screen = turtle.Screen()
screen.title("Snake Game")
screen.bgcolor("black")
screen.setup(width=600, height=640)
screen.tracer(0)  

head = turtle.Turtle("square")
head.color("lime")
head.penup()

food = turtle.Turtle("circle")
food.color("red")
food.penup()

pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.color("white")

segments = []
state = {"direction": "stop", "score": 0, "high": 0, "alive": True}


def reset_game():
    for seg in segments:
        seg.goto(1000, 1000)  
    segments.clear()
    head.goto(0, 0)
    state.update(direction="stop", score=0, alive=True)
    place_food()
    draw_score()


def place_food():
    while True:
        x = random.randrange(-LIMIT, LIMIT + 1, STEP)
        y = random.randrange(-LIMIT, LIMIT + 1, STEP)
        if all(seg.distance(x, y) > 1 for seg in segments) and head.distance(x, y) > 1:
            food.goto(x, y)
            return


def draw_score(message=""):
    pen.clear()
    pen.goto(0, 295)
    pen.write(
        f"Score: {state['score']}   High Score: {state['high']}",
        align="center", font=("Courier", 18, "bold"),
    )
    if message:
        pen.goto(0, 0)
        pen.write(message, align="center", font=("Courier", 22, "bold"))


def set_direction(new, opposite):
    if state["alive"] and state["direction"] != opposite:
        state["direction"] = new


def go_up():    set_direction("up", "down")
def go_down():  set_direction("down", "up")
def go_left():  set_direction("left", "right")
def go_right(): set_direction("right", "left")


def move_head():
    x, y = head.xcor(), head.ycor()
    d = state["direction"]
    if d == "up":
        head.sety(y + STEP)
    elif d == "down":
        head.sety(y - STEP)
    elif d == "left":
        head.setx(x - STEP)
    elif d == "right":
        head.setx(x + STEP)


def game_over():
    state["alive"] = False
    state["direction"] = "stop"
    draw_score("GAME OVER\nPress SPACE to restart")


def restart():
    if not state["alive"]:
        reset_game()


def quit_game():
    screen.bye()


def game_loop():
    if state["alive"] and state["direction"] != "stop":
        for i in range(len(segments) - 1, 0, -1):
            segments[i].goto(segments[i - 1].pos())
        if segments:
            segments[0].goto(head.pos())

        move_head()

    
        if abs(head.xcor()) > LIMIT or abs(head.ycor()) > LIMIT:
            game_over()
        
        elif any(seg.distance(head) < STEP / 2 for seg in segments):
            game_over()
        
        elif head.distance(food) < STEP / 2:
            seg = turtle.Turtle("square")
            seg.color("green")
            seg.penup()
            seg.goto(1000, 1000)
            segments.append(seg)
            state["score"] += 10
            state["high"] = max(state["high"], state["score"])
            place_food()
            draw_score()

    screen.update()
    screen.ontimer(game_loop, DELAY_MS)


screen.listen()
for key, func in [("Up", go_up), ("w", go_up), ("Down", go_down), ("s", go_down),
                  ("Left", go_left), ("a", go_left), ("Right", go_right), ("d", go_right),
                  ("space", restart), ("Escape", quit_game)]:
    screen.onkeypress(func, key)

reset_game()
game_loop()

try:
    screen.mainloop()
except turtle.Terminator:
    pass