import pygame
import random
import os
import collections as c
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

# Global variables
board = b = list(range(1, 10))

rows = ['012', '345', '678']
columns = ['036', '147', '258']
X = ['048', '246']

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (211, 211, 211)
DARK_GRAY = (200, 200, 200)
LIGHT_BLUE = (135, 206, 250)

restart = False
# Graphics


class TextObj(pygame.font.Font):
    def __init__(self, text, x, y, font=None, size=32):
        pygame.font.Font.__init__(self, font, size)
        self.SurfObj = self.render(text, True, (0, 0, 0,))
        self.RectObj = self.SurfObj.get_rect()
        self.RectObj.center = (x, y)


def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Image not found: ' + fullname)
    image = image.convert()
    image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


class Button:
    def __init__(self, surf_dest, text, x, y, value):
        self.surf_dest = surf_dest

        self.Surf = pygame.Surface((250, 100))
        self.Rect = self.Surf.get_rect()
        self.Rect.center = (x, y)
        self.Surf.fill(GRAY)

        self.text = TextObj(text, 125, 50)
        self.Surf.blit(self.text.SurfObj, self.text.RectObj)
        self.surf_dest.blit(self.Surf, self.Rect)

        self.value = value

    def hovered(self, target):
        return target.collidepoint(pygame.mouse.get_pos())

    def update(self):
        if self.hovered(self.Rect):
            self.darken()
        else:
            self.lighten()

    def darken(self):
        self.Surf.fill(DARK_GRAY)
        self.Surf.blit(self.text.SurfObj, self.text.RectObj)
        self.surf_dest.blit(self.Surf, self.Rect)

    def lighten(self):
        self.Surf.fill(GRAY)
        self.Surf.blit(self.text.SurfObj, self.text.RectObj)
        self.surf_dest.blit(self.Surf, self.Rect)

    def clicked(self):
        if self.hovered(self.Rect):
            return True

# Game classes and functions


class Space:
    def __init__(self, surface, x, y):
        self.x = x
        self.y = y
        self.screen = surface
        self.rect = pygame.draw.rect(self.screen, WHITE, ((self.x, self.y), (98, 98)))
        self.marked = False

    def update(self):
        self.mouse_hover = self.rect.collidepoint(pygame.mouse.get_pos())
        if not self.marked:
            if self.mouse_hover:
                self.darken()
            else:
                self.lighten()

    def mark_X(self):
        if not self.marked:
            self.lighten()
            mark, rect = load_image('X.jpg', -1)
            mark = pygame.transform.scale(mark, (98, 98))
            self.screen.blit(mark, self.rect)
            self.marked = True

    def mark_O(self):
        if not self.marked:
            self.lighten()
            mark, rect = load_image('O.jpg', -1)
            mark = pygame.transform.scale(mark, (98, 98))
            self.screen.blit(mark, self.rect)
            self.marked = True
        
    def darken(self):
        self.rect = pygame.draw.rect(self.screen, GRAY, ((self.x, self.y),(98, 98)))

    def lighten(self):
        self.rect = pygame.draw.rect(self.screen, WHITE, ((self.x, self.y),(98, 98)))


class Player:
    def __init__(self, mark):
        self.turn = True
        self.mark = mark
        
    def hover(self, target):
        return target.collidepoint(pygame.mouse.get_pos())
            
    def move(self, surface):
        if self.turn:
            if self.mark == 'X':
                for i in range(9):
                    if spaces[i].rect.collidepoint(pygame.mouse.get_pos()):
                        if not spaces[i].marked:
                            spaces[i].mark_X()
                            board[i] = 'X'
                            surface.blit(gameboard, (0,0))
                            global turn
                            turn += 1
                            self.turn = False
                            return True
            if self.mark == 'O':
                for i in range(9):
                    if spaces[i].rect.collidepoint(pygame.mouse.get_pos()):
                        if not spaces[i].marked:
                            spaces[i].mark_O()
                            board[i] = 'O'
                            surface.blit(gameboard, (0,0))
                            turn += 1
                            self.turn = False
                            return True

    def check_win(self, surface, player):
        if win_Check():
            pWin = TextObj(player + " won the game!", 250, 50)
            surface.blit(pWin.SurfObj, pWin.RectObj)
            pygame.display.update()
            return True


def get_row(space): #Gets the row of a space
    for i in range(3):
        if str(space) in rows[i]:
            return(i)


def get_column(space): #Gets the column of a space
    for i in range(3):
        if str(space) in columns[i]:
            return(i)


def get_diagonal(space): #Gets the diagonal of a space, and checks if center
    if space == 4:
        return(2)
    for i in range(2):
        if str(space) in X[i]:
            return(i)


def check_row(space): #Checks for X's and for empty spaces in row
    RS = rows[get_row(space)]
    ARS = []
    if 'X' not in set(b[int(RS[i])] for i in range(3)):
        for i in RS:
            if board[int(i)] != 'O':
                ARS.append(i)
    return(ARS)


def check_column(space): #Checks for X's and for empty spaces in column
    CS = columns[get_column(space)]
    ACS = []
    if 'X' not in set(b[int(CS[i])] for i in range(3)):
        for i in CS:
            if board[int(i)] != 'O':
                ACS.append(i)
    return(ACS)


def check_center(): #Checks for X's and for empty spaces in both diagonals
    ACS = []
    if 'X' not in set(b[int(X[0][i])] for i in range(3)):
        for i in X[0]:
            if board[int(i)] != 'O':
                ACS.append(i)
    if 'X' not in set(b[int(X[1][i])] for i in range(3)):
        for i in X[1]:
            if board[int(i)] != 'O':
                ACS.append(i)
    return(ACS)


def check_diagonals(space): #Checks for X's and for empty spaces in diagonal
    AXS = []
    if get_diagonal(space) == 2:
        for i in check_center():
            AXS.append(i)
        return(AXS)
    
    XS = X[get_diagonal(space)]
    
    if 'X' not in set(b[int(XS[i])] for i in range(3)):
        for i in XS:
            if board[int(i)] != 'O':
                AXS.append(i)
    return(AXS)


def scan_board(): #Checks for open spaces
    openspaces = osp = []
    for space in range(9):
        if board[space] == 'O':
            if check_row(space) != None:
                for i in check_row(space):
                    osp.append(int(i))
            if check_column(space) != None:
                for i in check_column(space):
                    osp.append(int(i))
            if get_diagonal(space) != None:
                if check_diagonals(space) != None:
                    for i in check_diagonals(space):
                        osp.append(int(i))
    if 'O' not in board:
        for space in range(9):
            if board[space] != 'X':
                osp.append(space)
    if (board[0] == 'X' or board[2] == 'X' or board[6] == 'X' or board[8] == 'X') and (board[4] != 'X' and board[4] != 'O'):
        if random.randrange(100) < 75:
            osp.append(4)
    return openspaces


def can_win(player): #Checks if (player) has 2-in-a-row
    for row in rows:
        if list(board[int(row[i])] for i in range(3)).count(player) == 2:
            for i in row:
                if isinstance(board[int(i)], int):
                    return(int(i))
    for column in columns:
        if list(board[int(column[i])] for i in range(3)).count(player) == 2:
            for i in column:
                if isinstance(board[int(i)], int):
                    return(int(i))
    for diag in X:
        if list(board[int(diag[i])] for i in range(3)).count(player) == 2:
            for i in diag:
                if isinstance(board[int(i)], int):
                    return(int(i))          
    return(None)


def win_Check(): #Checks for 3-in-a-row
    for row in rows:
        lst = list(board[int(row[i])] for i in range(3))
        if lst[1:] == lst[:-1]:
            return True
    for column in columns:
        lst = list(board[int(column[i])] for i in range(3))
        if lst[1:] == lst[:-1]:
            return True
    for diag in X:
        lst = list(board[int(diag[i])] for i in range(3))
        if lst[1:] == lst[:-1]:
            return True
    else:
        return False


def com_Move():  # Computer's turn. Computer scans board and picks from the best possible spaces.
    if can_win('O') is not None:  # Go for the win if possible!
        return can_win('O')
    if can_win('X') is not None:  # Block player from winning!
        return can_win('X')
                
    openspaces = osp = scan_board()
    bestspaces = bs = []

    count = c.Counter(osp)  # Counts how many 'points' each space has
    if 3 in count.values():
        for k,v in count.items():
            if v == 3:
                bs.append(k)
        return random.choice(bs)
    if 2 in count.values():
        for k,v in count.items():
            if v == 2:
                bs.append(k)
        return random.choice(bestspaces)
    else:
        return random.choice(openspaces)


# --------------------------------------------------------------------------------
def main():

# Define local variables
    global spaces
    global turn
    global run
    global player
    global gameboard
    
# Initialize
    pygame.init()
    gamescreen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Tic Tac Toe')

# Create Menu
    menuscreen = pygame.Surface(gamescreen.get_size())
    menuscreen.fill(LIGHT_BLUE)

# Prepare Menu Objects
    clock = pygame.time.Clock()

    title = TextObj('Tic-Tac-Toe!', 250, 50, size=100)
    menuscreen.blit(title.SurfObj, title.RectObj)

    btn0 = Button(menuscreen, "One Player", 250, 200, '1p')
    btn1 = Button(menuscreen, "Two Players", 250, 325, '2p')

    buttons = [btn0, btn1]

# Menu Loop
    gamemode = 0
    menu_open = True
    while menu_open:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEMOTION:
                for i in range(2):
                    buttons[i].update()
            elif event.type == MOUSEBUTTONDOWN:
                for i in range(2):
                    if buttons[i].clicked():
                        gamemode = buttons[i].value
                        menu_open = False


        gamescreen.blit(menuscreen, (0, 0))
        pygame.display.update()
# Create Gameboard
    gameboard = pygame.Surface(gamescreen.get_size())
    gameboard.fill(WHITE)
    pygame.draw.aaline(gameboard, BLACK, (200, 100), (200, 400))
    pygame.draw.aaline(gameboard, BLACK, (300, 100), (300, 400))
    pygame.draw.aaline(gameboard, BLACK, (100, 200), (400, 200))
    pygame.draw.aaline(gameboard, BLACK, (100, 300), (400, 300))

# Prepare Game Objects
    player = Player('X')
    player2 = Player('O')
    
    space0 = Space(gameboard, 101, 101)
    space1 = Space(gameboard, 201, 101)
    space2 = Space(gameboard, 301, 101)
    space3 = Space(gameboard, 101, 201)
    space4 = Space(gameboard, 201, 201)
    space5 = Space(gameboard, 301, 201)
    space6 = Space(gameboard, 101, 301)
    space7 = Space(gameboard, 201, 301)
    space8 = Space(gameboard, 301, 301)

    spaces = [space0, space1, space2,
                space3, space4, space5,
                space6, space7, space8]

    gamescreen.blit(gameboard, (0, 0))
# Main Loop
    run = True
    turn = 0
    while run:
        clock.tick(60)

        #Event handler
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
                exit()
            elif event.type == MOUSEMOTION:
                for i in range(9):
                    spaces[i].update()
            elif event.type == MOUSEBUTTONDOWN:
                if player.turn:
                    if player.move(gameboard):
                        player2.turn = True
                    if gamemode == '1p':
                        if player.check_win(gameboard, 'You'):
                            run = False
                            break
                    if gamemode == '2p':
                        if player.check_win(gameboard, 'Player 1'):
                            run = False
                            break
                if player2.turn:
                    if player2.move(gameboard):
                        player.turn = True
                    if player2.check_win(gameboard, 'Player 2'):
                        run = False
                        break
                gamescreen.blit(gameboard, (0, 0))
                pygame.display.update()

        if turn == 9:
            noWin = TextObj("It's a cat's game!", 250, 50)
            gameboard.blit(noWin.SurfObj, noWin.RectObj)
            gamescreen.blit(gameboard, (0, 0))
            pygame.display.update()
            run = False
            break
                                
        if (not player.turn) and (gamemode == '1p') and (not win_Check()):  # Computer Move
            pygame.time.delay(2000)
            comMove = com_Move()
            spaces[comMove].mark_O()
            board[comMove] = 'O'
            if win_Check():
                cWin = TextObj("Computer won the game!", 250, 50)
                gameboard.blit(cWin.SurfObj, cWin.RectObj)
                pygame.display.update()
                run = False
            turn += 1
            player.turn = True

        gamescreen.blit(gameboard, (0, 0))
        pygame.display.update()

# Play again
    pygame.time.wait(3000)
    btn2 = Button(gameboard, "Play again", 250, 250, None)
    global restart
    restart = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEMOTION:
                btn2.update()
            elif event.type == MOUSEBUTTONDOWN:
                if btn2.clicked():
                    restart = True
        if restart:
            break
        gamescreen.blit(gameboard, (0, 0))
        pygame.display.update()

if __name__ == '__main__':
    main()

while True:
    if restart:
        board = b = list(range(1, 10))
        main()