class Platform():
    "Класс отвечает за платформы"
    def __init__(self, width, height, posX, posY, topLimit, bottomLimit, speed = 4):
        self.width = width
        self.height = height
        self.posX = posX
        self.posY = posY
        self.top = topLimit
        self.bottom = bottomLimit

        self.speed = speed

    def Move(self, isToTop):
        "Функция двигает платформу вверх или вниз"
        if isToTop:
            if self.posY - self.speed >= self.top:
                self.posY -= self.speed
            else:
                self.posY = self.top
        else:
            if self.posY + self.speed <= self.bottom:
                self.posY += self.speed
            else:
                self.posY = self.bottom

    def MoveTo(self, posX, posY):
        self.posX = posX
        self.posY = posY
