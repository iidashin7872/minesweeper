import tkinter
from tkinter import messagebox
import random

BOARD_WIDTH = 20
BOARD_HEIGHT = 10
MINE_NUM = 20

MINE_BG_COLOR = "pink"
FLAG_BG_COLOR = "gold"
EMPTY_BG_COLOR = "lightgray"

fg_color = {
    1:"blue", 
    2:"green", 
    3:"purple", 
    4:"olive", 
    5:"chocolate", 
    6:"magenta", 
    7:"darkorange", 
    8:"red", 
}

MINE = -1

class MineSweeper():
    def __init__(self, app):
        self.app = app
        self.cells = None
        self.labels = None
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        self.mine_num = MINE_NUM
        self.clear_num = self.width * self.height - self.mine_num
        self.open_num = 0
        self.open_mine = False
        self.play_game = False

        self.cells = None
        self.labels = None

        self.init_cells()
        self.place_mines()
        self.set_neighbor_mine_num()

        self.create_widgets()
        self.set_events()
        
        self.play_game = True

    def init_cells(self):
        self.cells = [[0] * self.width for _ in range(self.height)]

    def place_mines(self):
        placed_mine_num = 0

        while placed_mine_num < self.mine_num:
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)

            if self.cells[y][x] != MINE:
                self.cells[y][x] = MINE
                placed_mine_num += 1

    def set_neighbor_mine_num(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.cells[y][x] == MINE:
                    continue

                neighbor_mine_num = 0

                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if dx != 0 or dy != 0:
                            if self.is_mine(x+dx, y+dy):
                                neighbor_mine_num += 1
                
                self.cells[y][x] = neighbor_mine_num

    def is_mine(self, x, y):
        if 0 <= x and x < self.width and 0 <= y and y < self.height:
            if self.cells[y][x] == MINE:
                return True
        return False
    
    def create_widgets(self):
        self.labels = [[None] * self.width for _ in range(self.height)]
        
        for y in range(self.height):
            for x in range(self.width):
                label = tkinter.Label(
                    self.app, 
                    width=4,
                    height=2, 
                    bg=EMPTY_BG_COLOR, 
                    relief=tkinter.RAISED
                )
                label.grid(column=x, row=y)
                self.labels[y][x] = label
    
    def set_events(self):
        for y in range(self.height):
            for x in range(self.width):
                label = self.labels[y][x]
                label.bind("<ButtonPress-1>", self.open_cell)
                label.bind("<ButtonPress-3>", self.raise_flag)

    def open_cell(self, event):
        if not self.play_game:
            return
        
        label = event.widget

        for y in range(self.height):
            for x in range(self.width):
                if self.labels[y][x] == label:
                    cx = x
                    cy = y

        cell = self.cells[cy][cx]

        if label.cget("relief") != tkinter.RAISED:
            return
        
        text, bg, fg = self.get_text_info(cell)

        if cell == MINE:
            self.open_mine = True

        label.config(
            text=text, 
            bg=bg, 
            fg=fg, 
            relief=tkinter.SUNKEN
        )

        self.open_num += 1

        if cell == 0:
            self.open_neighbor(cx-1, cy-1)
            self.open_neighbor(cx, cy-1)
            self.open_neighbor(cx+1, cy-1)
            self.open_neighbor(cx-1, cy)
            self.open_neighbor(cx+1, cy)
            self.open_neighbor(cx-1, cy+1)
            self.open_neighbor(cx, cy+1)
            self.open_neighbor(cx+1, cy+1)

        if self.open_mine:
            self.app.after_idle(self.game_over)
        elif self.open_num == self.clear_num:
            self.app.after_idle(self.game_clear)

    def raise_flag(self, event):
        if not self.play_game:
            return
        
        label = event.widget

        if label.cget("relief") != tkinter.RAISED:
            return
        
        if label.cget("text") != "F":
            label.config(
                text="F", 
                bg=FLAG_BG_COLOR
            )
        else:
            label.config(
                text="", 
                bg=EMPTY_BG_COLOR
            )

    def open_neighbor(self, x, y):
        if self.open_mine:
            return
        
        if not (0 <= x and x < self.width and 0 <= y and y < self.height):
            return
        
        label = self.labels[y][x]

        if label.cget("relief") != tkinter.RAISED:
            return
        
        if self.cells[y][x] == MINE:
            return
        
        text, bg, fg = self.get_text_info(self.cells[y][x])
        label.config(
            text=text, 
            bg=bg, 
            fg=fg, 
            relief=tkinter.SUNKEN
        )

        self.open_num += 1
        if self.cells[y][x] == 0:
            self.open_neighbor(x-1, y-1)
            self.open_neighbor(x, y-1)
            self.open_neighbor(x+1, y-1)
            self.open_neighbor(x-1, y)
            self.open_neighbor(x+1, y)
            self.open_neighbor(x-1, y+1)
            self.open_neighbor(x, y+1)
            self.open_neighbor(x+1, y+1)

    def game_over(self):
        self.open_all()

        self.play_game = False

        messagebox.showerror(
            "GAME OVER!", 
            "地雷マスを開いてしまいました..."
        )
    
    def game_clear(self):
        self.open_all()

        self.play_game = False

        messagebox.showinfo(
            "GAME CLEAR!", 
            "ゲームクリア！"
        )

    def open_all(self):
        for y in range(self.height):
            for x in range(self.width):
                label = self.labels[y][x]
                text, bg, fg = self.get_text_info(self.cells[y][x])
                label.config(
                    text=text, 
                    bg=bg, 
                    fg=fg, 
                    relief=tkinter.SUNKEN
                )

    def get_text_info(self, num):
        if num == MINE:
            text = "X"
            bg = MINE_BG_COLOR
            fg = "darkred"
        elif num == 0:
            text = ""
            bg = EMPTY_BG_COLOR
            fg = "black"
        else:
            text = str(num)
            bg = EMPTY_BG_COLOR
            fg = fg_color[num]

        return(text, bg, fg)
    
app = tkinter.Tk()
app.title("Minesweeper") # ウィンドウタイトル
app.resizable(False, False) # ウィンドウのサイズ変更不可
game = MineSweeper(app)
app.mainloop()
