import pygame
import sys
from pygame.locals import *

# Number of frames per second
# Change this value to speed up or slow down the game
FPS = 100
# Global Variables to be used through our program

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
LINETHICKNESS = 10
PADDLESIZE = 50
PADDLEOFFSET = 20
INCREASESPEED = 5

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Draws the starting position of the Arena
def drawArena():
    DISPLAYSURF.fill((0, 0, 0))
    # Draw outline of arena
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0, 0), (WINDOWWIDTH, WINDOWHEIGHT)), LINETHICKNESS * 2)
    # Draw centre line
    pygame.draw.line(DISPLAYSURF, WHITE, ((int(WINDOWWIDTH/2)), 0), (int((WINDOWWIDTH/2)), WINDOWHEIGHT), int((LINETHICKNESS/4)))

# Draws the paddle
def drawPaddle(paddle):
    if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:  # Stops paddle moving too low
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
    # Stops paddle moving too high
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS
    # Draws paddle
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)

# Draws the ball
def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)

# moves the ball and returns new position
def moveBall(ball, ballDirX, ballDirY):
    ball.x += (ballDirX * INCREASESPEED)
    ball.y += (ballDirY * INCREASESPEED)
    return ball

# checks for a collision with a wall, and "bounces" the ball off it
# returns new direction
def checkEdgeCollision(ball, ballDirX, ballDirY):
    if ball.top == (LINETHICKNESS) or ball.bottom == (WINDOWHEIGHT - LINETHICKNESS):
        ballDirY = ballDirY * -1
    if ball.left == (LINETHICKNESS) or ball.right == (WINDOWWIDTH - LINETHICKNESS):
        ballDirX = ballDirX * -1
    return ballDirX, ballDirY

# Checks if the ball hit a paddle, and "bounces" ball off it
def checkHitBall(ball, paddle1, paddle2, ballDirX):
    if ballDirX == -1 and paddle1.right == ball.left and paddle1.top <= ball.top and paddle1.bottom >= ball.bottom:
        return -1
    elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top <= ball.top and paddle2.bottom >= ball.bottom:
        return -1
    else:
        return 1

# Checks to see if a point has been scored and returns the new score
def checkPointScored(paddle1, ball, score, ballDirX):
    # reset points if the ball hits the left wall
    if ball.left == LINETHICKNESS:
        return 0
    # 1 point for hitting the ball
    if ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        score += 1
        return score
    # 5 points for beating the other paddle
    elif ball.right == WINDOWWIDTH - LINETHICKNESS:
        score += 5
        return score
    # if no point scored then score doesnt change
    else:
        return score

# Displays the current score on the screen
def displayScore(score):
    resultSurf = BASICFONT.render('Score: %s' % score, True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 150, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)

# Artificial Intelligence of computer player
def artificialIntelligence(ball, ballDirX, paddle2):
    # If ball is moving away from paddle, center bat
    if ballDirX == -1:
        if paddle2.centery < (WINDOWHEIGHT/2):
            paddle2.y += 4.1
        elif paddle2.centery > (WINDOWHEIGHT/2):
            paddle2.y -= 4.1
    # if ball moving towards bat, track its movement
    elif ballDirX == 1:
        if paddle2.centery < ball.centery:
            paddle2.y += 4.1
        else:
            paddle2.y -= 4.1
    return paddle2

# Main function


def main():
    pygame.init()
    global DISPLAYSURF
    # Font Information
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pong')

    # Initiate variable and set starting positions
    # any future changes made within rectangles
    ballX = (WINDOWWIDTH / 2) - (LINETHICKNESS / 2)
    ballY = (WINDOWHEIGHT / 2)
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) / 2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) / 2
    score = 0

    # Keeps track of ball direction
    ballDirX = -1  # -1 = left, 1 = right
    ballDirY = -1  # -1 = up, 1 = down

    # Creates rectangles for ball and paddles.
    paddle1 = pygame.Rect(PADDLEOFFSET, playerOnePosition, LINETHICKNESS, PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS, PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)

    pygame.mouse.set_visible(0)  # makes cursor invisible

    while True:  # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                paddle1.y = mousey
            print(event)

        # Draws the starting position of the Arena
        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)

        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
        score = checkPointScored(paddle1, ball, score, ballDirX)
        ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX)
        paddle2 = artificialIntelligence(ball, ballDirX, paddle2)

        displayScore(score)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
