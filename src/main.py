import turtle
from copy import deepcopy


class game:
    def __init__(self, def_board) -> None:
        self.screen = turtle.Screen()
        self.gt = turtle.Turtle() # To draw grid lines
        self.st = turtle.Turtle() # To draw symbols
        self.def_board = def_board # Default state of the board
        self.board = deepcopy(self.def_board)
        self.player = 'O'
        self.winner = ''

        self.draw_screen()
        self.screen.onclick(self.update_board)
        self.screen.listen()
        self.screen.mainloop()

    def draw_screen(self):
        screen = self.screen
        gt = self.gt
        st = self.st
        # Initialize screen settings
        screen.setup(750, 750, starty=0)
        screen.setworldcoordinates(0, screen.window_height(), screen.window_width(), 0)
        screen.title("TicTacToe for Sophon hua kuy")
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

    def update_board(self, x, y):
        st = self.st
        board = self.board
        # Get x, y position in range [0, 2]
        x = sorted((0, int(x // 250), 2))[1]
        y = sorted((0, int(y // 250), 2))[1]

        if st.isdown() or board[y][x] != '':
            return

        board[y][x] = self.player

        # Draw symbol on board
        if self.player == 'O':
            st.setpos(x * 250 + 225, y * 250 + 125)
            st.pendown()
            st.circle(100, steps=20)
            self.player = 'X'
        else:
            st.setpos(x * 250 + 25, y * 250 + 25)
            st.pendown()
            st.goto(x * 250 + 225, y * 250 + 225)
            st.penup()
            st.setpos(x * 250 + 225, y * 250 + 25)
            st.pendown()
            st.goto(x * 250 + 25, y * 250 + 225)
            st.penup()
            self.player = 'O'

        st.penup()
        self.check_win_draw()

    def check_win_draw(self):
        draw = True
        board = self.board
        offset_width = self.screen.window_width() - self.st.width()
        for i in range(3):
            # Horizontal
            if board[i][0] == board[i][1] == board[i][2] != '':
                self.winner = board[i][0]
                self.show_winner(0, i*250+125, offset_width, i*250+125)
                return
            # Vertical
            if board[0][i] == board[1][i] == board[2][i] != '':
                self.winner = board[0][i]
                self.show_winner(i*250+125, 0, i*250+125, offset_width)
                return
            # Draw
            if '' in board[i]:
                draw = False
        # Diagonal (Left-Right)
        if board[0][0] == board[1][1] == board[2][2] != '':
            self.winner = board[0][0]
            self.show_winner(0, 0, offset_width, offset_width)
            return
        # Diagonal (Right-Left)
        if board[0][2] == board[1][1] == board[2][0] != '':
            self.winner = board[0][0]
            self.show_winner(offset_width, 0, 0, offset_width)
            return
        if draw:
            self.winner = "draw"
            self.show_winner(0, 0, 0, 0)
            return
    
    def show_winner(self, x1=0, y1=0, x2=0, y2=0):
        screen = self.screen
        st = self.st
        if not (x1==y1==x2==y2==0):
            st.pencolor("red")
            st.goto(x1, y1)
            st.pendown()
            st.goto(x2, y2)
            st.penup()
        st.goto(screen.window_width()/2, screen.window_height()/2)
        st.pencolor("black")
        st.write(f"{self.winner} WINS" if self.winner != "draw" else "DRAW", align="center", font=("Arial", 72, "bold"))
        st.pencolor("white")

        screen.onclick(self.reset_board)

    def reset_board(self, x, y):
        self.board = deepcopy(self.def_board)
        self.st.clear()
        self.winner = ''
        self.player = 'O'
        self.screen.onclick(self.update_board)


# Main Program
def_board = [
    ['', '', ''],
    ['', '', ''],
    ['', '', '']
]
g = game(def_board)
