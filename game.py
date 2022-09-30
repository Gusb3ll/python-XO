import turtle as t


def DrawScreen():
    # Initialize screen settings
    t.screensize(750, 750, "gray")
    t.setworldcoordinates(0, 750, 750, 0)
    t.pensize(10)

    # Draw grid lines
    t.color("white")
    t.pu()
    
    for y in range(1, 3):
        t.setpos(0, y * 250)
        t.pendown()
        t.goto(750, y * 250)
        t.penup()
    for x in range(1, 3):
        t.setpos(x * 250, 0)
        t.pendown()
        t.goto(x * 250, 750)
        t.penup()



DrawScreen()
input()