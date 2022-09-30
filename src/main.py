import turtle


def DrawScreen():
    # Initialize screen settings
    screen.setup(750, 750)
    screen.setworldcoordinates(0, screen.window_height(), screen.window_width(), 0)
    screen.title("TicTacToe for Sophon hua kuy")
    screen.bgcolor("#346B31")
    gt.pensize(10)
    gt.speed(0)
    gt.hideturtle()
    st.setheading(90)
    st.penup()
    st.pensize(10)
    st.speed(10)
    st.hideturtle()
    st.color("white")

    # Draw grid lines
    gt.color("white")
    gt.penup()
    # Horizontal
    for y in range(1, 3):
        gt.setpos(0, y * 250)
        gt.pendown()
        gt.forward(screen.window_width() - gt.width())
        gt.penup()
    # Vertical
    gt.setheading(90)
    for x in range(1, 3):
        gt.setpos(x * 250, 0)
        gt.pendown()
        gt.forward(screen.window_height() - gt.width())
        gt.penup()


def UpdateBoard(x, y):
    global board, player
    x = int(x // 250)
    y = int(y // 250)

    if st.isdown() or board[y][x] != 0:
        return

    board[y][x] = player

    # Draw symbol on board
    if player == 1:
        st.setpos(x * 250 + 225, y * 250 + 125)
        st.pendown()
        st.circle(100, steps=20)
        player = 2
    else:
        st.setpos(x * 250 + 25, y * 250 + 25)
        st.pendown()
        st.goto(x * 250 + 225, y * 250 + 225)
        st.penup()
        st.setpos(x * 250 + 225, y * 250 + 25)
        st.pendown()
        st.goto(x * 250 + 25, y * 250 + 225)
        st.penup()
        player = 1

    st.penup()


screen = turtle.Screen()
gt = turtle.Turtle()
st = turtle.Turtle()
player = 1
def_board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]
board = def_board.copy()
DrawScreen()
screen.onclick(UpdateBoard)
screen.listen()
turtle.mainloop()
