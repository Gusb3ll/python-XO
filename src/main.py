import json
import turtle


class Model:
    def __init__(self):
        self.screen = turtle.Screen()
        self.gt = turtle.Turtle() # To draw grid lines
        self.st = turtle.Turtle() # To draw symbols
        self.ht = turtle.Turtle() # To draw hints
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.hint = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.player = 1
        self.winner = 0
        self.anim = True

    def change_player(self):
        self.player = -self.player

    def reset_hint(self):
        self.hint = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

    def toggle_anim(self, x, y):
        self.anim = not self.anim
        print("Animation: " + str(self.anim))

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
    def __init__(self, model: Model):
        self.model = model

    def draw_screen(self):
        # Initialize screen settings
        self.model.screen.setup(750, 750, starty=0)
        self.model.screen.setworldcoordinates(0, self.model.screen.window_height(), self.model.screen.window_width(), 0)
        self.model.screen.title("TicTacToe")
        self.model.screen.bgcolor("#346B31")
        self.model.gt.pen(shown=False, pendown=False, pencolor="white", pensize=10, speed=0)
        self.model.st.pen(shown=False, pendown=False, pencolor="white", pensize=10, resizemode="user", stretchfactor=(2.5, 2.5), speed=10)
        self.model.ht.pen(shown=False, pendown=False, pencolor="red", pensize=10, resizemode="user", stretchfactor=(2.5, 2.5), speed=0)
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

    def draw_all_symbols(self): # draw all symbols without animation
        self.model.screen.tracer(False)
        for y in range(3):
            for x in range(3):
                self.draw_new_symbol(self.model.board[y][x], x, y)
        self.model.screen.tracer(True)

    def draw_new_symbol(self, shape, x, y): # draw new symbol with animation
        self.model.ht.clear()
        self.model.screen.tracer(False) if not self.model.anim else None # disable animation
        if shape == 1: # O
            self.model.st.setpos(x * 250 + 225, y * 250 + 125)
            self.model.st.pendown()
            self.model.st.circle(100, steps=20)
        elif shape == -1: # X
            self.model.st.setpos(x * 250 + 25, y * 250 + 25)
            self.model.st.pendown()
            self.model.st.goto(x * 250 + 225, y * 250 + 225)
            self.model.st.penup()
            self.model.st.setpos(x * 250 + 225, y * 250 + 25)
            self.model.st.pendown()
            self.model.st.goto(x * 250 + 25, y * 250 + 225)
            self.model.st.penup()

        self.model.st.penup()
        self.model.screen.tracer(True) if not self.model.anim else None

    def show_winner(self, x1, y1, x2, y2, resetFunc):
        FONT_SIZE = 72
        if not (x1==y1==x2==y2==0): # if not a tie draw red line
            self.model.st.pencolor("red")
            self.model.st.goto(x1, y1)
            self.model.st.pendown()
            self.model.st.goto(x2, y2)
            self.model.st.penup()
        self.model.st.goto(self.model.screen.window_width()/2, self.model.screen.window_height()/2 + FONT_SIZE/2)
        self.model.st.pencolor("black")
        # -1 = X wins, 1 = O wins, 2 = tie
        self.model.st.write(f"{ 'O' if self.model.winner == 1 else 'X' } WINS" if self.model.winner != 2 else "TIE", align="center", font=("Comic Sans MS", FONT_SIZE, "bold"))
        self.model.st.pencolor("white")

        self.model.screen.onclick(resetFunc)

    def show_hint(self): # show ? at the position of the hint
        FONT_SIZE = 72
        self.model.screen.tracer(False)
        self.model.ht.clear()
        for y in range(3):
            for x in range(3):
                if self.model.hint[y][x] == 1:
                    self.model.ht.setpos(x * 250 + 125, y * 250 + 125 + FONT_SIZE)
                    self.model.ht.write("?", align="center", font=("Comic Sans MS", FONT_SIZE, "bold"))
        self.model.screen.tracer(True)


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self.model)

        # Try to load save
        try:
            self.model.load_save()
        except FileNotFoundError:
            self.model.update_save()
        
        # Draw screen and all symbols
        self.view.draw_screen()
        self.view.draw_all_symbols()
        self.model.screen.onclick(self.update_board)
        self.model.screen.onclick(self.model.toggle_anim, btn=3) # toggle animation
        self.check_win_tie()
        self.check_hint()
        self.model.screen.listen()
        self.model.screen.mainloop()

    def update_board(self, x, y):
        # Get x, y position in range [0, 2]
        x = sorted((0, int(x // 250), 2))[1]
        y = sorted((0, int(y // 250), 2))[1]

        if self.model.st.isdown() or self.model.board[y][x] != 0:
            return
        self.model.screen.onclick(None)
        self.model.board[y][x] = self.model.player
        # Draw symbol on board
        self.view.draw_new_symbol(self.model.player, x, y)
        self.model.change_player()
        self.model.update_save()
        self.model.screen.onclick(self.update_board)
        self.check_win_tie()
        self.check_hint()

    def check_win_tie(self):
        tie = True
        offset_width = self.model.screen.window_width() - self.model.st.width()
        for i in range(3):
            # Horizontal
            if abs(sum(self.model.board[i])) == 3:
                self.model.winner = self.model.board[i][0]
                self.view.show_winner(0, i*250+125, offset_width, i*250+125, self.reset_board)
                return
            # Vertical
            if abs(sum(self.model.board[j][i] for j in range(3))) == 3:
                self.model.winner = self.model.board[0][i]
                self.view.show_winner(i*250+125, 0, i*250+125, offset_width, self.reset_board)
                return
            # Tie
            if 0 in self.model.board[i]:
                tie = False
        # Diagonal (Left-Right)
        if abs(sum(self.model.board[i][i] for i in range(3))) == 3:
            self.model.winner = self.model.board[0][0]
            self.view.show_winner(0, 0, offset_width, offset_width, self.reset_board)
            return
        # Diagonal (Right-Left)
        if abs(sum(self.model.board[i][2-i] for i in range(3))) == 3:
            self.model.winner = self.model.board[0][2]
            self.view.show_winner(offset_width, 0, 0, offset_width, self.reset_board)
            return
        if tie:
            self.model.winner = 2
            self.view.show_winner(0, 0, 0, 0, self.reset_board)
            return

    def check_hint(self):
        self.model.reset_hint()
        if self.model.winner != 0:
            return
            
        for i in range(3):
            # Horizontal
            if abs(sum(self.model.board[i])) == 2:
                self.model.hint[i][self.model.board[i].index(0)] = 1
            # Vertical
            vertical = [self.model.board[j][i] for j in range(3)]
            if abs(sum(vertical)) == 2:
                self.model.hint[vertical.index(0)][i] = 1
        # Diagonal (Left-Right)
        dia1 = [self.model.board[i][i] for i in range(3)]
        if abs(sum(dia1)) == 2:
            self.model.hint[dia1.index(0)][dia1.index(0)] = 1
        # Diagonal (Right-Left)
        dia2 = [self.model.board[i][2-i] for i in range(3)]
        if abs(sum(dia2)) == 2:
            self.model.hint[dia2.index(0)][2-dia2.index(0)] = 1
        self.view.show_hint()

    def reset_board(self, x, y):
        self.model.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.model.st.clear()
        self.model.ht.clear()
        self.model.winner = 0
        self.model.player = 1
        self.model.update_save()
        self.model.screen.onclick(self.update_board)


# Main Program
if __name__ == "__main__":
    controller = Controller()
