from random import random

class Ball():
    "Класс отвечает за шарик для пинг понга"
    def __init__(self, radius, posX = 0, posY = 0, speedX = 0, speedY = 0, acceleration = 0.002):
        self.posX = posX
        self.posY = posY
        self.radius = radius
        self.speedX = speedX
        self.speedY = speedY
        self.acceleration = acceleration

    def Move(self):
        "Двигает шарик и придаёт ускорение ему"
        self.posX += self.speedX
        self.posY += self.speedY

        if self.speedX >= 0:
            self.speedX += self.acceleration
        else:
            self.speedX -= self.acceleration

        if self.speedY >= 0:
            self.speedY += self.acceleration
        else:
            self.speedY -= self.acceleration

    def MoveTo(self, X, Y):
        "Функция передвигает шарик на указанную позицию"
        self.posX = X
        self.posY = Y

    def chooseDirection(self, side):
        "Выбирает рандомное направление для движения шарика"
        if side == 0:
            self.speedX = random() * 2 - 2
        else:
            self.speedX = random() * 2
        self.speedY = random() * 4 - 2