import curses
from curses import KEY_RIGHT, KEY_UP, KEY_DOWN, KEY_LEFT
from random import randint

VIEW_WIDTH = 50
VIEW_HEIGHT = 40
SNAKE_LENGTH = 5
MAX_X = VIEW_WIDTH - 2
MAX_Y = VIEW_HEIGHT - 2
# Assuming snake is horizontal in the begining
SNAKE_X = SNAKE_LENGTH + 1
SNAKE_Y = 3
TIMEOUT = 100


class Snake(object):
    def __init__(self, intialX, initialY, window):
        self.x = intialX
        self.y = initialY
        self.score = 0
        self.window = window
        self.bodyList = []
        self.direction = MoveRight(self)  # Inital Direction
        for i in range(SNAKE_LENGTH, 0, -1):
            self.bodyList.append(Body(self.x - i, self.y, '*'))
        print(self.x, self.y)
        self.bodyList.append(Body(self.x, self.y, '0'))

    def render(self):
        for body in self.bodyList:
            self.window.addstr(body.y, body.x, body.char)

    def updatePosition(self):
        lastBody = self.bodyList.pop(0)
        lastBody.x = self.bodyList[-1].x
        lastBody.y = self.bodyList[-1].y
        self.bodyList.insert(-1, lastBody)
        self.direction.onDirectionChange()

    def changeDirection(self, direction):
        self.direction = direction

    def eat(self, food):
        food.reset()
        self.score += 1
        self.bodyList.insert(-1,
                             Body(self.bodyList[-1].x, self.bodyList[-1].y, "*"))


class Food(object):
    def __init__(self, x, y, window):
        self.xcord = x
        self.ycord = y
        self.window = window

    def reset(self):
        self.xcord = randint(1, MAX_X)
        self.ycord = randint(1, MAX_Y)

    def render(self):
        self.window.addstr(self.ycord, self.xcord, ".")


class Body(object):
    def __init__(self, xCord, yCord, char):
        self.x = xCord
        self.y = yCord
        self.char = char


class Direction():
    def __init__(self, snake):
        self.snake = snake

    def onDirectionChange(self, snake):
        pass


class MoveRight(Direction):
    def onDirectionChange(self):
        self.snake.bodyList[-1].x += 1
        if(self.snake.bodyList[-1].x > MAX_X):
            self.snake.bodyList[-1].x = 1


class MoveLeft(Direction):
    def onDirectionChange(self):
        self.snake.bodyList[-1].x -= 1
        if(self.snake.bodyList[-1].x < 1):
            self.snake.bodyList[-1].x = MAX_X


class MoveUp(Direction):
    def onDirectionChange(self):
        self.snake.bodyList[-1].y -= 1
        if(self.snake.bodyList[-1].y < 1):
            self.snake.bodyList[-1].y = MAX_Y


class MoveDown(Direction):
    def onDirectionChange(self):
        self.snake.bodyList[-1].y += 1
        if(self.snake.bodyList[-1].y > MAX_Y):
            self.snake.bodyList[-1].y = 1


if __name__ == '__main__':

    mainWindow = curses.initscr()
    mainX = mainWindow.getmaxyx()[1]
    mainY = mainWindow.getmaxyx()[0]
    print(str(mainX)+" , "+str(mainY))
    curses.beep()
    curses.beep()
    window = curses.newwin(VIEW_HEIGHT, VIEW_WIDTH,
                           int(mainY/2 - VIEW_HEIGHT/2), int(mainX/2 - VIEW_WIDTH/2))
    window.timeout(200)
    window.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    window.border(0)
    snake = Snake(SNAKE_X, SNAKE_Y, window)
    food = Food(randint(1, MAX_X), randint(1, MAX_Y), window)
    directionMap = {
        KEY_UP: MoveUp(snake),
        KEY_DOWN: MoveDown(snake),
        KEY_LEFT: MoveLeft(snake),
        KEY_RIGHT: MoveRight(snake)
    }
with open('Banner.txt', "r", encoding="utf8") as f:
    lines = f.readlines()
    bannerY = 0
    for a in lines:
        mainWindow.addstr(bannerY, 0, a.rstrip())
        bannerY += 1
    mainWindow.refresh()
    while True:
        window.clear()

        window.border(0)
        snake.render()
        food.render()

        window.addstr(0, 6, "Score : {}".format(snake.score))
        snake.updatePosition()

        if(any([(body.x == snake.bodyList[-1].x and body.y == snake.bodyList[-1].y) for body in snake.bodyList[:-1]])):
            break

        if(snake.bodyList[-1].x == food.xcord and snake.bodyList[-1].y == food.ycord):
            snake.eat(food)
        event = window.getch()
        if event == 27:
            break
        if event in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
            snake.changeDirection(directionMap[event])

    curses.endwin()
