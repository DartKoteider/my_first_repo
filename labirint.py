from pygame import *
from random import *
 
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
 
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
#класс главного игрока
class Player(GameSprite):
    #метод, в котором реализовано управление спрайтом по кнопкам стрелкам клавиатуры
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        # Вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)
 
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
 
    def update(self):
        ''' перемещает персонажа, применяя текущую горизонтальную и вертикальную скорость'''
        # сначала движение по горизонтали
        if packman.rect.x <= win_width-50 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: # идем направо, правый край персонажа - вплотную к левому краю стены
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) # если коснулись сразу нескольких, то правый край - минимальный из возможных
        elif self.x_speed < 0: # идем налево, ставим левый край персонажа вплотную к правому краю стены
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right) # если коснулись нескольких стен, то левый край - максимальный
        if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: # идем вниз
            for p in platforms_touched:
                self.y_speed = 0
                # Проверяем, какая из платформ снизу самая высокая, выравниваемся по ней, запоминаем её как свою опору:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0: # идем вверх
            for p in platforms_touched:
                self.y_speed = 0  # при столкновении со стеной вертикальная скорость гасится
                self.rect.top = max(self.rect.top, p.rect.bottom) # выравниваем верхний край по нижним краям стенок, на которые наехали
    # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)
 
#класс спрайта-врага   
class Enemy(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        player_speed
        # Вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        
 
  #движение врага
    def update(self):
        if self.rect.x <= 0: #w1.wall_x + w1.wall_width
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        
        
# класс спрайта-пули  
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    # движение врага
    def update(self):
        self.rect.x += self.speed
        # исчезает, если дойдет до края экрана
        if self.rect.x > win_width+10:
            self.kill()
 
#Создаем окошко
win_width = 1000
win_height = 700
display.set_caption("Лабиринт")
window = display.set_mode((win_width, win_height))
back = (0, 255, 120)#задаем цвет согласно цветовой схеме RGB
 
#создаем группу для стен
barriers = sprite.Group()
 
#создаем группу для пуль
bullets = sprite.Group()
 
#создаем группу для монстров
monsters = sprite.Group()
 
#создаем стены картинки
w1 = GameSprite('wall.jpg', 50, 650, 1000, 50)
w2 = GameSprite('wall_v.jpg', 50, 100, 50, 300)
w3 = GameSprite('wall.jpg', 0, 0, 1000, 50)
w4 = GameSprite('wall.jpg', 100, 350, 500, 50)
w5 = GameSprite('wall.jpg', 150, 450, 150, 50)
w6 = GameSprite('wall.jpg', 350, 450, 200, 50)
w7 = GameSprite('wall_v.jpg', 150, 50, 50, 150)
w8 = GameSprite('wall_v.jpg', 250, 100, 50, 100)
w9 = GameSprite('wall_v.jpg', 50, 450, 50, 200)
w10 = GameSprite('wall.jpg', 150, 250, 300, 50)
w11 = GameSprite('wall.jpg', 350, 200, 50, 50)
w12 = GameSprite('wall.jpg', 300, 100, 400, 50)
w13 = GameSprite('wall.jpg', 200, 550, 100, 50)
w14 = GameSprite('wall_v.jpg', 150, 500, 50, 150)
w15 = GameSprite('wall.jpg', 350, 550, 500, 50)
w16 = GameSprite('wall.jpg', 600, 450, 150, 50)
w17 = GameSprite('wall.jpg', 550, 250, 150, 50)
w18 = GameSprite('wall.jpg', 350, 450, 200, 50)
w19 = GameSprite('wall_v.jpg', 400, 500, 50, 50)
w20 = GameSprite('wall_v.jpg', 650, 150, 50, 350)
w21 = GameSprite('wall_v.jpg', 550, 200, 50, 50)
w22 = GameSprite('wall_v.jpg', 450, 150, 50, 150)
w23 = GameSprite('wall.jpg', 850, 100, 100, 100)
w24 = GameSprite('wall_v.jpg', 800, 450, 50, 100)
w25 = GameSprite('wall.jpg', 300, 100, 400, 50)
w26 = GameSprite('wall.jpg', 200, 550, 100, 50)
w27 = GameSprite('wall_v.jpg', 750, 50, 50, 150)
w28 = GameSprite('wall_v.jpg', 750, 250, 50, 150)
w29 = GameSprite('wall.jpg', 850, 450, 100, 50)
w30 = GameSprite('wall.jpg', 900, 550, 50, 50)
w31 = GameSprite('wall.jpg', 800, 350, 150, 50)
w32 = GameSprite('wall.jpg', 850, 250, 100, 50)

#добавляем стены в группу
barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)
barriers.add(w5)
barriers.add(w6)
barriers.add(w7)
barriers.add(w8)
barriers.add(w9)
barriers.add(w10)
barriers.add(w11)
barriers.add(w12)
barriers.add(w13)
barriers.add(w14)
barriers.add(w15)
barriers.add(w16)
barriers.add(w17)
barriers.add(w18)
barriers.add(w19)
barriers.add(w20)
barriers.add(w21)
barriers.add(w22)
barriers.add(w23)
barriers.add(w24)
barriers.add(w25)
barriers.add(w26)
barriers.add(w27)
barriers.add(w28)
barriers.add(w29)
barriers.add(w30)
barriers.add(w31)
barriers.add(w32)

 
#создаем спрайты
packman = Player('pac-5.png', 0, 670, 50, 50, 0, 0)
final_sprite = GameSprite('pac-1.png', 800, 50, 50, 50)
 
monster1 = Enemy('cyborg.png', 450, 300, 50, 50, 5)
monster2 = Enemy('cyborg.png', 850, 200, 50, 50, 5)
monster3 = Enemy('cyborg.png', 200, 500, 50, 50, 5)
#добавляем монстра в группу
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
 
#переменная, отвечающая за то, как кончилась игра
finish = False
#игровой цикл
run = True
while run:
    #цикл срабатывает каждую 0.05 секунд
    time.delay(40)
    #перебираем все события, которые могли произойти
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.fire()
 
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
 
    #проверка, что игра еще не завершена
    if not finish:
        #обновляем фон каждую итерацию
        window.fill(back)#закрашиваем окно цветом
 
        #запускаем движения спрайтов
        packman.update()
        bullets.update()
 
        #обновляем их в новом местоположении при каждой итерации цикла
        packman.reset()
        #рисуем стены 2
        #w1.reset()
        #w2.reset()
        bullets.draw(window)
        barriers.draw(window)
        final_sprite.reset()
 
        if not(sprite.groupcollide(monsters, bullets, True, True)):
            monsters.update()
            monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)
 
        #Проверка столкновения героя с врагом и стенами
        if sprite.spritecollide(packman, monsters, False):
            finish = True
            #вычисляем отношение
            img = image.load('game_over_PNG58.png')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))
 
        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('unnamed.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
    display.update()