import tkinter as tk
import threading, copy, random

class BoardSize:
    Piece = 20
    Width = 10
    Heigh = 22

def light_color( color, light ):
    color_rgb_r = int( color[ 1:3 ], 16 )
    color_rgb_g = int( color[ 3:5 ], 16 )
    color_rgb_b = int( color[ 5:7 ], 16 )

    rgb_r = int( ( 255 - color_rgb_r ) * ( light - 100 ) / 100 + color_rgb_r )
    rgb_g = int( ( 255 - color_rgb_g ) * ( light - 100 ) / 100 + color_rgb_g )
    rgb_b = int( ( 255 - color_rgb_b ) * ( light - 100 ) / 100 + color_rgb_b )

    return '#%02x%02x%02x' % ( rgb_r, rgb_g, rgb_b )


def dark_color( color, dark ):
    color_rgb_r = int ( color [ 1:3 ], 16 )
    color_rgb_g = int ( color [ 3:5 ], 16 )
    color_rgb_b = int ( color [ 5:7 ], 16 )

    rgb_r = int( color_rgb_r * dark / 100 )
    rgb_g = int( color_rgb_g * dark / 100 )
    rgb_b = int( color_rgb_b * dark / 100 )

    return '#%02x%02x%02x' % ( rgb_r, rgb_g, rgb_b )

class Block:
        shapeNo = [ [0, 0], [0, 0], [0, 0], [0, 0] ]
        shapeZ = [ [0, -1], [0, 0], [-1, 0], [-1, 1] ]
        shapeS = [ [0, -1], [0, 0], [1, 0], [1, 1] ]
        shapeLine = [ [0, -1], [0, 0], [0, 1], [0, 2] ]
        shapeT = [ [-1, 0], [0, 0], [1, 0], [0, 1] ]
        shapeSquare = [ [0, 0], [1, 0], [0, 1], [1, 1] ]
        shapeL = [ [-1, -1], [0, -1], [0, 0], [0, 1] ]
        shapeMirroredL = [ [1, -1], [0, -1], [0, 0], [0, 1] ]
        BlockTable = [shapeNo, shapeZ, shapeS,shapeLine, shapeT, \
                        shapeSquare, shapeL, shapeMirroredL]
        sRED = '#ff0000'
        sGREEN = '#00ff00'
        sBLUE = '#0000ff'
        sYELLOW = '#ffff00'
        sCYAN = '#00ffff'
        sLIGHT_BLUE = '#add8e6'
        sVIOLET_RED = '#d02090'
        Colors = ['BLACK', sRED, sGREEN, sBLUE,sYELLOW,sCYAN, sLIGHT_BLUE, sVIOLET_RED]
        light = ['BLACK']
        dark = ['BLACK']
        for i in range(1, 8):
            light.append(light_color(Colors[i], 150))
            dark.append(dark_color(Colors[i], 50))
        light.append(light_color(Colors[1], 150) )
        dark.append(dark_color(Colors[1], 50) )
        Light = light
        Dark = dark

class GameBoard(tk.Canvas):
    def __init__(self, app):
        tk.Canvas.__init__(self, app)
        self.initGameBoard()
        self.OnPaint()
        self.timerStop = False
        self.timeInterval = 0.4
        self.myTimer()
        app.protocol('WM_DELETE_WINDOW', self.windowClose)

    def initGameBoard(self):
        self.BlockTable = Block.BlockTable
        self.colors = Block.Colors
        self.light = Block.Light
        self.dark = Block.Dark
        self.board = []
        for i in range( BoardSize.Heigh ):
            board_row = [ 0 ] * BoardSize.Width
            self.board.append( board_row )

        self.pSize = BoardSize.Piece - 1
        self.pre_board = copy.deepcopy(self.board)
        self.isCurBlock = False

    def SetBlockOnBoard(self, set_board, block_coords, x, y, block_shape):
        for i in range(4):
            piece_x = block_coords[i][0] + x
            piece_y = block_coords[i][1] + y
            set_board[piece_y][piece_x] = block_shape

    def DrawBlock(self, copy_board, block_coords, x, y, block_shape):
        self.SetBlockOnBoard(copy_board, block_coords, x, y, block_shape)
        self.board = copy.deepcopy(copy_board)
        self.curBlockCoords = copy.deepcopy(block_coords)
        [self.curShape, self.curX, self.curY] = [block_shape, x, y]
        try:
            self.OnPaint()
        except:
            pass

    def CheckMoveAvailable(self, check_board, block_coords, x, y):
        for i in range(4):
            piece_x = block_coords[ i ][ 0 ] + x
            piece_y = block_coords[ i ][ 1 ] + y
            if piece_x < 0 or piece_x > BoardSize.Width - 1 or \
                    piece_y < 0 or piece_y > BoardSize.Heigh - 1 or \
                            check_board[ piece_y ][ piece_x ] != 0:
                return False
        return True

    def OnTimer(self):
        copy_board = copy.deepcopy(self.board)
        if not self.isCurBlock:
            newShape = random.randint(1, 7)
            newBlockCoords = copy.deepcopy( self.BlockTable[newShape] )
            [newX, newY] = [int(BoardSize.Width /2), 1]
            if not self.CheckMoveAvailable(copy_board, newBlockCoords, newX, newY):
                self.timerStop = True
            else:
                self.DrawBlock(copy_board, newBlockCoords, newX, newY, newShape)
                self.isCurBlock = True
        else:
            self.SetBlockOnBoard(copy_board, self.curBlockCoords, \
                self.curX, self.curY, 0)
            if not self.CheckMoveAvailable(copy_board, self.curBlockCoords, \
                self.curX, self.curY + 1 ):
                self.isCurBlock = False
            # if self.curY > BoardSize.Heigh -4:
            #     self.timerStop = True
            else:
                self.DrawBlock(copy_board, self.curBlockCoords, \
                self.curX, self.curY + 1, self.curShape)

    def OnPaint(self):
        # x = 5
        # y = 4
        # block_shape = 1
        # block_coords = self.BlockTable[block_shape]
        # for i in range(4):
        #     piece_x = block_coords[i][0] + x
        #     piece_y = block_coords[i][1] + y
        #     self.board[piece_y][piece_x] = block_shape

        # self.SetBlockOnBoard(self.board, self.BlockTable[1],5, 4, 1)
        # self.SetBlockOnBoard(self.board, self.BlockTable[2],1, 10, 2)
        # self.SetBlockOnBoard(self.board, self.BlockTable[3],4, 10, 3)
        # self.SetBlockOnBoard(self.board, self.BlockTable[4],7, 10, 4)
        # self.SetBlockOnBoard(self.board, self.BlockTable[5],1, 16, 5)
        # self.SetBlockOnBoard(self.board, self.BlockTable[6],5, 16, 6)
        # self.SetBlockOnBoard(self.board, self.BlockTable[7],7, 16, 7)

        for i in range( BoardSize.Heigh ):
            for j in range( BoardSize.Width ):
                self.pre_shape = self.pre_board[i][j]
                shape = self.board[ i ][ j ]
                tag_name = 'Piece_' + str( i ) + '_' + str( j )
                if shape != self.pre_shape:
                    if self.pre_shape != 0:
                        self.delete(tag_name)

                if shape != 0:
                    [ x, y ] = [ j * BoardSize.Piece, i * BoardSize.Piece ]
                    self.create_rectangle( \
                        x, y, x + self.pSize, y + self.pSize, fill = self.colors[ shape ], tag = tag_name )

                    self.create_line( x, y, x, y + self.pSize, fill = self.light[ shape ], tag = tag_name )
                    self.create_line( x, y, x + self.pSize, y, fill = self.light[ shape ], tag = tag_name )
                    self.create_line( x, y + self.pSize, x + self.pSize, y + self.pSize, fill = self.dark[ shape ], tag = tag_name )
                    self.create_line( x + self.pSize, y + self.pSize, x + self.pSize, y, fill = self.dark[ shape ], tag = tag_name )
                    self.pre_board = copy.deepcopy(self.board)

    def myTimer(self):
        if self.timerStop == False:
            self.OnTimer()
            self.timer_thread = threading.Timer(self.timeInterval, self.myTimer)
            self.timer_thread.daemon = True
            self.timer_thread.start()

    def windowClose(self):
        self.timerStop = True
        app.destroy()

class TetGame:
    def __init__(self, app):
        self.app = app
        self.w = BoardSize.Piece * BoardSize.Width
        self.h = BoardSize.Piece * BoardSize.Heigh
        gameboard = GameBoard(app)
        gameboard.place(x = 0, y = 0)
        gameboard.config(width = self.w, height = self.h,
                         bg = 'black', highlightthickness = 2)
        self.Center()

    def Center(self):
        ws = self.app.winfo_screenwidth()
        hs = self.app.winfo_screenheight()
        x = int( ( ws / 2 ) - ( ( self.w + 4 ) / 2 ) )
        y = int( ( hs / 2 ) - ( ( self.h + 4 ) / 2 ) )
        self.app.geometry(f'{self.w}x{self.h}+{x}+{y}')

app =tk.Tk()
app.title('TetGame')
tetgame = TetGame(app)
app.mainloop()
