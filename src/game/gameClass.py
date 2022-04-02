import pygame
from game.ballClass import Ball
from game.platformClass import Platform
from PyQt5 import QtCore
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from random import randint

class Game():
    "Базовый класс для окна"
    def __init__(self, surface, config):
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        #Настройки игры
        self.width = config['WIDTH']
        self.height = config['HEIGHT']
        self.platformWidth = config['PLATFORM_WIDTH']
        self.platformHeight = config['PLATFORM_HEIGHT']
        self.textSize = config['TEXT_SIZE']
        self.firstPlayerScore = 0
        self.secondPlayerScore = 0
        self.numderOfPlayers = 0

        #Инициализируем шарик
        self.ball_side = randint(0, 1)
        self.ball = Ball(10)
        self.restoreBallPos()
        self.ball.chooseDirection(self.ball_side)

        #Инициализируем платформы
        self.platformLeft = Platform(self.platformWidth, self.platformHeight,
                                     0, (self.height - self.platformHeight) / 2,
                                     0, self.height - self.platformHeight)
        self.platformRight = Platform(self.platformWidth, self.platformHeight,
                                     self.width - self.platformWidth,
                                     (self.height - self.platformHeight) / 2,
                                     0, self.height - self.platformHeight)

        #Настройки для клавиш
        self.keys = {
            'IS_KEY_UP_DOWN': False,
            'IS_KEY_DOWN_DOWN': False,
            'IS_KEY_W_DOWN': False,
            'IS_KEY_S_DOWN': False
        }

        pygame.init()
        pygame.mixer.init()
        self.SURFACE = surface

        #Звуки
        self.BOUNCE_SOUND = QMediaPlayer()
        url = QtCore.QUrl.fromLocalFile('game/Audios/bounceSound.mp3')
        content = QMediaContent(url)
        self.BOUNCE_SOUND.setMedia(content)
        self.WIN_SOUND = QMediaPlayer()
        url = QtCore.QUrl.fromLocalFile('game/Audios/winSound.mp3')
        content = QMediaContent(url)
        self.WIN_SOUND.setMedia(content)

        #Шрифты
        self.GAME_FONT = pygame.font.SysFont(
            'Bahnschrift SemiLight SemiConde', self.textSize)

    def setup_settings(self):
        self.ball_side = randint(0, 1)
        self.restoreBallPos()
        self.ball.chooseDirection(self.ball_side)
        self.platformLeft.MoveTo(0, (self.height - self.platformHeight) / 2)
        self.platformRight.MoveTo(self.width - self.platformWidth,
                                  (self.height - self.platformHeight) / 2)
        self.firstPlayerScore = 0
        self.secondPlayerScore = 0

    def set_volume(self, volume):
        self.BOUNCE_SOUND.setVolume(volume)
        self.WIN_SOUND.setVolume(volume)

    def drawCenterLine(self):
        "Рисует центральную линию"
        pygame.draw.line(self.SURFACE, self.WHITE, (self.width / 2 - 1, 0), (self.width / 2 - 1, self.height), 2)

    def drawPlatforms(self):
        pygame.draw.rect(self.SURFACE, self.WHITE, (self.platformLeft.posX,
                                                   self.platformLeft.posY,
                                                   self.platformLeft.width,
                                                   self.platformLeft.height))
        pygame.draw.rect(self.SURFACE, self.WHITE, (self.platformRight.posX,
                                                   self.platformRight.posY,
                                                   self.platformRight.width,
                                                   self.platformRight.height))

    def restoreBallPos(self):
        "Устанавливает шарик в центр поля"
        self.ball.MoveTo(self.width / 2, self.height / 2)

    def drawBall(self):
        "Рисует шарик"
        pygame.draw.circle(self.SURFACE, self.WHITE,
                           (self.ball.posX, self.ball.posY), self.ball.radius)

    def checkBallPos(self):
        "Проверяет позицию шарика и, если надо, отразит его направление движения"
        if self.ball.posY <= self.ball.radius or self.ball.posY >= self.height - self.ball.radius:
            self.ball.speedY *= (-1)
        if self.ball.posX <= self.ball.radius + self.platformWidth:
            if self.ball.posY >= self.platformLeft.posY and self.ball.posY <= self.platformLeft.posY + self.platformHeight:
                #Высчитываем отклонение
                deviation = 2 * (self.ball.posY - self.platformLeft.posY) / self.platformHeight - 1
                self.ball.speedX *= (-1 + deviation * 0.3)
                self.ball.posX = self.ball.radius + self.platformWidth
                #Воспроизводим звук удара от платформу
                self.BOUNCE_SOUND.play()
            elif self.ball.posX <= self.ball.radius:
                return (True, 2)
        elif self.ball.posX >= self.width - self.ball.radius - self.platformWidth:
            if self.ball.posY >= self.platformRight.posY and self.ball.posY <= self.platformRight.posY + self.platformHeight:
                #Высчитываем отклонениеотклонение
                deviation = 2 * (self.ball.posY -self.platformRight.posY) / self.platformHeight - 1
                self.ball.speedX *= (-1 + deviation * 0.3)
                self.ball.posX = self.width - self.ball.radius - self.platformWidth
                #Воспроизводим звук удара от платформу
                self.BOUNCE_SOUND.play()
            elif self.ball.posX >= self.width - self.ball.radius:
                return (True, 1)
        return (False, -1)

    def moveBot(self):
        if self.ball.speedX < 0:
            return 0
        if self.platformRight.posY + self.platformHeight / 2 > self.ball.posY:
            self.platformRight.Move(True)
        else:
            self.platformRight.Move(False)

    def rend_display(self):
        self.SURFACE.fill(self.BLACK)

        self.drawCenterLine()

        self.drawPlatforms()

        #Если игрок 1
        if self.numderOfPlayers == 1:
            if self.keys['IS_KEY_W_DOWN'] or self.keys['IS_KEY_UP_DOWN']:
                self.platformLeft.Move(True)
            elif self.keys['IS_KEY_S_DOWN'] or self.keys['IS_KEY_DOWN_DOWN']:
                self.platformLeft.Move(False)

            self.moveBot()
        else:
            if self.keys['IS_KEY_W_DOWN']:
                self.platformLeft.Move(True)
            elif self.keys['IS_KEY_S_DOWN']:
                self.platformLeft.Move(False)

            if self.keys['IS_KEY_UP_DOWN']:
                self.platformRight.Move(True)
            elif self.keys['IS_KEY_DOWN_DOWN']:
                self.platformRight.Move(False)

        FirstScore = pygame.font.Font.render(
            self.GAME_FONT, str(self.firstPlayerScore), True, self.WHITE)
        SecondScore = pygame.font.Font.render(
            self.GAME_FONT, str(self.secondPlayerScore), True, self.WHITE)
        self.SURFACE.blit(
            FirstScore, ((self.width / 2 - FirstScore.get_width()) / 2, 10))
        self.SURFACE.blit(
            SecondScore, ((3 * self.width / 2 - SecondScore.get_width()) / 2, 10))

        self.drawBall()

        self.ball.Move()

        res = self.checkBallPos()
        if res[0]:
            self.restoreBallPos()
            #Воспроизводим звук победы
            self.WIN_SOUND.play()
            if res[1] == 1:
                self.firstPlayerScore += 1
                self.ball_side = 1
                self.ball.chooseDirection(self.ball_side)
            else:
                self.secondPlayerScore += 1
                self.ball_side = 0
                self.ball.chooseDirection(self.ball_side)

        return self.SURFACE
