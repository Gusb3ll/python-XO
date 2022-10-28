import json
import turtle

def updateSave(field, data):
    with open('../save.json', 'w') as saveFile:
        save = json.load(saveFile)
    if (field == "player"):
        save["player"] = data
    if (field == "board"):
        save["board"] = data

def draw_screen():
    # Initialize screen settings
    screen.setup(750, 750, starty=0)
    screen.setworldcoordinates(0, screen.window_height(), screen.window_width(), 0)
    screen.title("TicTacToe")
    screen.bgcolor("#346B31")
    gt.pen(shown=False, pendown=False, pencolor="white", pensize=10, speed=0)
    st.pen(pendown=False, pencolor="white", pensize=10, resizemode="user", stretchfactor=(2.5, 2.5))
    st.setheading(90)

    # Draw grid lines
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

def update_board(x, y):
    global player, winner, board
    # Get x, y position in range [0, 2]
    x = sorted((0, int(x // 250), 2))[1]
    y = sorted((0, int(y // 250), 2))[1]

    if st.isdown() or board[y][x] != '':
        return
    screen.onclick(None)
    board[y][x] = player
    # Draw symbol on board
    if player == 'O':
        st.setpos(x * 250 + 225, y * 250 + 125)
        st.pendown()
        st.circle(100, steps=20)
        player = 'X'
    else:
        st.setpos(x * 250 + 25, y * 250 + 25)
        st.pendown()
        st.goto(x * 250 + 225, y * 250 + 225)
        st.penup()
        st.setpos(x * 250 + 225, y * 250 + 25)
        st.pendown()
        st.goto(x * 250 + 25, y * 250 + 225)
        st.penup()
        player = 'O'

    st.penup()
    screen.onclick(update_board)
    check_win_draw()

def check_win_draw():
    global winner
    tie = True
    offset_width = screen.window_width() - st.width()
    for i in range(3):
        # Horizontal
        if board[i][0] == board[i][1] == board[i][2] != '':
            winner = board[i][0]
            show_winner(0, i*250+125, offset_width, i*250+125)
            return
        # Vertical
        if board[0][i] == board[1][i] == board[2][i] != '':
            winner = board[0][i]
            show_winner(i*250+125, 0, i*250+125, offset_width)
            return
        # Draw
        if '' in board[i]:
            tie = False
    # Diagonal (Left-Right)
    if board[0][0] == board[1][1] == board[2][2] != '':
        winner = board[0][0]
        show_winner(0, 0, offset_width, offset_width)
        return
    # Diagonal (Right-Left)
    if board[0][2] == board[1][1] == board[2][0] != '':
        winner = board[0][0]
        show_winner(offset_width, 0, 0, offset_width)
        return
    if tie:
        winner = "tie"
        show_winner(0, 0, 0, 0)
        return

def show_winner(x1=0, y1=0, x2=0, y2=0):
    if not (x1==y1==x2==y2==0):
        st.pencolor("red")
        st.goto(x1, y1)
        st.pendown()
        st.goto(x2, y2)
        st.penup()
    st.goto(screen.window_width()/2, screen.window_height()/2)
    st.pencolor("black")
    st.write(f"{winner} WINS" if winner != "tie" else "TIE", align="center", font=("Arial", 72, "bold"))
    st.pencolor("white")

    screen.onclick(reset_board)

def reset_board(x, y):
    global board, player, winner

    board = [
        ['', '', ''],
        ['', '', ''],
        ['', '', '']
    ]
    st.clear()
    winner = ''
    player = 'O'
    screen.onclick(update_board)


# Main Program
screen = turtle.Screen()
gt = turtle.Turtle() # To tie grid lines
st = turtle.Turtle() # To tie symbols
board = [
    ['', '', ''],
    ['', '', ''],
    ['', '', '']
]
save["board"] = board
player = 'O'
winner = ''

draw_screen()
screen.onclick(update_board)
screen.listen()
screen.mainloop()
