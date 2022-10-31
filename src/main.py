import json
import turtle


class Model:
    def __init__(self):
        self.screen = turtle.Screen()
        self.gt = turtle.Turtle() # To draw grid lines
        self.st = turtle.Turtle() # To draw symbols
        self.board = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ]
        self.player = 'O'
        self.winner = ''

    def change_player(self):
        if self.player == 'O':
            self.player = 'X'
        else:
            self.player = 'O'

    def load_save(self):
        with open('save.json', 'r') as saveFile:
            save = json.load(saveFile)
            self.player = save["player"]
            self.board = save["board"]

    def update_save(self):
        with open('save.json', 'w') as saveFile:
            save = {}
            save["player"] = self.player
            save["board"] = self.board
            json.dump(save, saveFile, indent=4)


class View:
    def __init__(self, model):
        self.model = model

    def draw_screen(self):
        # Initialize screen settings
        self.model.screen.setup(750, 750, starty=0)
        self.model.screen.setworldcoordinates(0, self.model.screen.window_height(), self.model.screen.window_width(), 0)
        self.model.screen.title("TicTacToe")
        self.model.screen.bgcolor("#346B31")
        self.model.gt.pen(shown=False, pendown=False, pencolor="white", pensize=10, speed=0)
        self.model.st.pen(shown=False, pendown=False, pencolor="white", pensize=10, resizemode="user", stretchfactor=(2.5, 2.5), speed=10)
        self.model.st.setheading(90)
        self.model.screen.tracer(False)

        # Draw grid lines
        # Horizontal
        for y in range(1, 3):
            self.model.gt.setpos(0, y * 250)
            self.model.gt.pendown()
            self.model.gt.forward(self.model.screen.window_width() - self.model.gt.width())
            self.model.gt.penup()
        # Vertical
        self.model.gt.setheading(90)
        for x in range(1, 3):
            self.model.gt.setpos(x * 250, 0)
            self.model.gt.pendown()
            self.model.gt.forward(self.model.screen.window_height() - self.model.gt.width())
            self.model.gt.penup()

        self.model.screen.tracer(True)

    def draw_loaded_symbol(self):
        self.model.screen.tracer(False)
        for y in range(3):
            for x in range(3):
                self.draw_new_symbol(self.model.board[y][x], x, y)
        self.model.screen.tracer(True)

    def draw_new_symbol(self, shape, x, y):
        if shape == 'O':
            self.model.st.setpos(x * 250 + 225, y * 250 + 125)
            self.model.st.pendown()
            self.model.st.circle(100, steps=20)
        elif shape == 'X':
            self.model.st.setpos(x * 250 + 25, y * 250 + 25)
            self.model.st.pendown()
            self.model.st.goto(x * 250 + 225, y * 250 + 225)
            self.model.st.penup()
            self.model.st.setpos(x * 250 + 225, y * 250 + 25)
            self.model.st.pendown()
            self.model.st.goto(x * 250 + 25, y * 250 + 225)
            self.model.st.penup()

        self.model.st.penup()

    def show_winner(self, x1, y1, x2, y2, resetFunc):
        FONT_SIZE = 72
        if not (x1==y1==x2==y2==0):
            self.model.st.pencolor("red")
            self.model.st.goto(x1, y1)
            self.model.st.pendown()
            self.model.st.goto(x2, y2)
            self.model.st.penup()
        self.model.st.goto(self.model.screen.window_width()/2, self.model.screen.window_height()/2 + FONT_SIZE/2)
        self.model.st.pencolor("black")
        self.model.st.write(f"{self.model.winner} WINS" if self.model.winner != "tie" else "TIE", align="center", font=("Arial", FONT_SIZE, "bold"))
        self.model.st.pencolor("white")

        self.model.screen.onclick(resetFunc)


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        try:
            model.load_save()
        except FileNotFoundError:
            model.update_save()
        
        view.draw_screen()
        view.draw_loaded_symbol()
        model.screen.onclick(self.update_board)
        self.check_win_tie()
        model.screen.listen()
        model.screen.mainloop()

    def update_board(self, x, y):
        # Get x, y position in range [0, 2]
        x = sorted((0, int(x // 250), 2))[1]
        y = sorted((0, int(y // 250), 2))[1]

        if self.model.st.isdown() or self.model.board[y][x] != '':
            return
        self.model.screen.onclick(None)
        self.model.board[y][x] = self.model.player
        # Draw symbol on board
        self.view.draw_new_symbol(self.model.player, x, y)
        self.model.change_player()
        self.model.update_save()
        self.model.screen.onclick(self.update_board)
        self.check_win_tie()

    def check_win_tie(self):
        tie = True
        offset_width = self.model.screen.window_width() - self.model.st.width()
        for i in range(3):
            # Horizontal
            if self.model.board[i][0] == self.model.board[i][1] == self.model.board[i][2] != '':
                self.model.winner = self.model.board[i][0]
                self.view.show_winner(0, i*250+125, offset_width, i*250+125, self.reset_board)
                return
            # Vertical
            if self.model.board[0][i] == self.model.board[1][i] == self.model.board[2][i] != '':
                self.model.winner = self.model.board[0][i]
                self.view.show_winner(i*250+125, 0, i*250+125, offset_width, self.reset_board)
                return
            # Tie
            if '' in self.model.board[i]:
                tie = False
        # Diagonal (Left-Right)
        if self.model.board[0][0] == self.model.board[1][1] == self.model.board[2][2] != '':
            self.model.winner = self.model.board[0][0]
            self.view.show_winner(0, 0, offset_width, offset_width, self.reset_board)
            return
        # Diagonal (Right-Left)
        if self.model.board[0][2] == self.model.board[1][1] == self.model.board[2][0] != '':
            self.model.winner = self.model.board[0][2]
            self.view.show_winner(offset_width, 0, 0, offset_width, self.reset_board)
            return
        if tie:
            self.model.winner = "tie"
            self.view.show_winner(0, 0, 0, 0, self.reset_board)
            return

    def reset_board(self, x, y):
        self.model.board = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ]
        self.model.st.clear()
        self.model.winner = ''
        self.model.player = 'O'
        self.model.update_save()
        self.model.screen.onclick(self.update_board)


# Main Program
if __name__ == "__main__":
    model = Model()
    view = View(model)
    controller = Controller(model, view)
