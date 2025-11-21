import turtle
import random

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Разноцветная спираль")

t = turtle.Turtle()
t.speed(0)
t.width(2)

colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink"]

for i in range(100):
    color = colors[i % len(colors)]
    t.color(color)
    t.forward(i * 2)
    t.right(91)

turtle.done()