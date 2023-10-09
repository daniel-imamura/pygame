from mysql.connector import connect, Error
import json
from flask import jsonify
import _thread
import pygame as pg
import time
import math

sw=600
sh = 400
posX = 0
sentido = 0

def inserir(nome, data_hora):    
    try:
        connection = connect(host="localhost", user="ini42",
                             password="123", database="ini42")
        print(connection)
    
    except Error as e:
        print(e)

    sqlStr = 'insert into Pessoa(nome, data_hora) values("%s", "%s");' % (nome, data_hora)
    with connection.cursor() as cursor:
        cursor.execute(sqlStr)
    
    connection.commit()
    connection.close()
    
def listarPessoas():
    try:
        connection = connect(host="localhost", user="ini42",
                             password="123", database="ini42")
        print(connection)
    
    except Error as e:
        print(e)

    sqlStr = "Select * from Pessoa;"
    with connection.cursor() as cursor:
        cursor.execute(sqlStr)
        result = cursor.fetchall()
        
    
    obj = "{<br>&nbsp;&nbsp;\"cod\" = 1,<br>&nbsp;&nbsp;\"dados\": [<br>"    
    aux = 0
    for row in result:        
        aux = str(row).find(",")
        obj += '&nbsp;&nbsp;&nbsp;&nbsp;{ "id": ' + str(row)[1:aux] + ', '        
        aux = str(row).find("date")
        obj += "\"nome\": \"%s\" },<br>" % str(row)[5:aux-3]
        
    obj += "&nbsp;&nbsp;],<br>}"
    connection.commit()    
    connection.close()    
    return obj

def buscarPorId(id):
    try:
        connection = connect(host="localhost", user="ini42",
                             password="123", database="ini42")
        print(connection)
    
    except Error as e:
        print(e)

    sqlStr = "Select * from Pessoa where id=%s;" % id 
    with connection.cursor() as cursor:
        cursor.execute(sqlStr)
        result = cursor.fetchall()            
             
    strRes = str(result)
    aux = strRes.find(",")
    id = strRes[2:aux]
    
    fim = strRes.find("datetime")
    nome = strRes[aux+3:fim-3]
    
    newStr = strRes[fim+18:len(strRes)-3]
    
    aux = newStr.find(",")
    newStr = newStr[aux+1:]
    
    aux = newStr.find(",")    
    newStr = newStr[aux+1:]
    
    aux = newStr.find(",")    
    newStr = newStr[aux+1:]
    
    dataStr = strRes[fim+18:len(strRes)-10].replace(",", "/").replace(" ", "")
    horaStr = newStr.replace(",", ":").replace(" ", "")
    if dataStr[len(dataStr)-1:len(dataStr)] == "/":
        dataStr = dataStr[0:len(dataStr)-1]
    data_hora = dataStr + "\t" + horaStr
    
    connection.commit()    
    connection.close()
    
    return "{\"cod\":1, \"status\":\"lido\", \"detalhe\":{\"id\":%s, \"nome\":\"%s\", \"data\":\"%s\"}}" % (id, nome, data_hora)


def excluir(id):
    try:
        connection = connect(host="localhost", user="ini42",
                             password="123", database="ini42")
        print(connection)
    
    except Error as e:
        print(e)

    sqlStr = "Select * from Pessoa where id=%s;" % id 
    with connection.cursor() as cursor:
        cursor.execute(sqlStr)
        resultado = cursor.fetchall()
        
    data = ""
    nome = ""
    obj = ""    
    ini = 0
    fim = 0
    for row in resultado:
        ini = str(row).find("'")
        fim = str(row).find("datetime") 
        obj += str(row)[ini+1:fim-3]
        nome = obj
        
        ini = str(row).find("datetime(")
        fim = str(row).find("))")
        aux = str(row)[ini+9:fim-1]
        obj = aux[0:4] + "/"
        
        ini = aux.find(",")
        aux = aux[ini+1:]        
        fim = aux.find(",")
        obj += aux[1:fim] + "/"
        
        ini = aux.find(",")
        aux = aux[ini+1:]
        fim = aux.find(",")
        obj += aux[1:fim]
        data = obj

    sqlStr = "Delete from Pessoa where id=%s;" % id 
    with connection.cursor() as cursor:
        cursor.execute(sqlStr)        
        result = cursor.fetchall()
            
    connection.commit()    
        
    sqlStr = "Select * from Pessoa;"
    with connection.cursor() as cursor:
        cursor.execute(sqlStr)
        result = cursor.fetchall()
    connection.close()
        
    obj2 = []
    for row in result:
        ini = str(row).find("'")
        fim = str(row).find("datetime")
        obj2.append(str(row)[ini+1:fim-3])
        
    _thread.start_new_thread(textoAnimado, (nome, data, obj2))
    

def moveX(size, length):    
    global posX
    global sentido
    while True:
        if sentido == 1:
            posX += 10
        if sentido == 0:
            posX -= 10
        if posX <= 0:
            sentido = 1
        if posX >= (length - size):
            sentido = 0
        time.sleep(0.1)        


def text_render(font, text, color):
    text = font.render(text, 1, color)
    return text


class Color:
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    purple = (128, 0, 128)
    red = (255, 0, 0)
    yellow = (255, 255, 0)
    mediumSlateBlue = (123, 104, 238)
    steelBlue = (70, 130, 180)
    lightGray = (220, 220, 220) 
 
class Font:
    ''' definition of type of fonts '''
    pg.font.init()
    little = pg.font.SysFont("Arial", 15)
    big = pg.font.SysFont("Arial", 40)

def textoAnimado(nome, data_hora, lista):    
    inicio = time.time()
    pg.init()
    clock = pg.time.Clock()    
    screen = pg.display.set_mode((sw, sh), pg.RESIZABLE)
    
        
    txt1 = text_render(Font.big, nome, Color.green)
    txt2 = text_render(Font.big, data_hora, Color.green)
    
    _thread.start_new_thread(moveX,(txt1.get_size()[0], sw))
    _thread.start_new_thread(moveX,(txt2.get_size()[0], sw))    
    ciclo = False    
    
    while True:
        fim = time.time()
        if fim - inicio >= 20:                    
            txt1 = text_render(Font.little, "", Color.green)
            txt2 = text_render(Font.little, "", Color.green)            
            inicio = fim
            ciclo = True
            
        if fim - inicio >= 10 and ciclo == True:
            ciclo = False
            txt1 = text_render(Font.big, nome, Color.green)
            txt2 = text_render(Font.big, data_hora, Color.green)
            
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()        
                raise SystemExit                
                
        screen.fill(Color.white)        
        timeInicio = time.time()
        timeFim = time.time()
        while ciclo == True and timeFim - timeInicio <= 10:
            aux = 45
            screen.fill(Color.white)
            for name in lista:            
                screen.blit(text_render(Font.little, name, Color.blue), (55, aux))            
                aux += 20
            pg.display.flip()
            clock.tick(100)
            timeFim = time.time()
            
        screen.blit(txt1, (posX, 90))
        screen.blit(txt2, (posX, 150))
        pg.display.flip()
        
        clock.tick(100)
        
def animacao1():
    pg.quit()
    pg.init()
    clock = pg.time.Clock()    
    screen = pg.display.set_mode((sw, sh), pg.RESIZABLE)
    pg.display.set_caption("Animação do Baby Yoda")
    imgYodaOrg = pg.image.load('yoda.png')
    imgYoda = pg.transform.scale(imgYodaOrg, (150, 180))
    step = 0
    angle_per_step = .05
    line_len = sw * 8
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
        screen.fill(Color.black)
        angle = step * angle_per_step
        x = line_len / 2.0 * math.sin(angle)
        y = line_len / 2.0 * math.cos(angle)
        pg.draw.line(screen, Color.blue, ((300+x), (180+y)), ((300-x),(180-y)), 8)

        angle = (step+155) * angle_per_step
        x = line_len / 2.0 * math.sin(angle)
        y = line_len / 2.0 * math.cos(angle)
        pg.draw.line(screen, Color.green, ((300+x), (180+y)), ((300-x),(180-y)), 8)        
        screen.blit(imgYoda, (220, 110))
        pg.display.flip()
        clock.tick(60)
        step += 1
        
class Player(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []        
        self.sprites.append(pg.transform.scale(pg.image.load('frog1.png'), (530, 330)))
        self.sprites.append(pg.transform.scale(pg.image.load('frog2.png'), (530, 330)))
        self.sprites.append(pg.transform.scale(pg.image.load('frog3.png'), (530, 330)))
        self.sprites.append(pg.transform.scale(pg.image.load('frog4.png'), (530, 330)))
        self.sprites.append(pg.transform.scale(pg.image.load('frog5.png'), (530, 330)))
        self.sprites.append(pg.transform.scale(pg.image.load('frog6.png'), (530, 330)))
        self.sprites.append(pg.transform.scale(pg.image.load('frog7.png'), (530, 330)))
        self.sprites.append(pg.transform.scale(pg.image.load('frog8.png'), (530, 330)))
        self.sprites.append(pg.transform.scale(pg.image.load('frog9.png'), (530, 330)))
        self.sprites.append(pg.transform.scale(pg.image.load('frog10.png'), (530, 330)))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        
    def update(self):
        self.current_sprite += 1
        
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
            
        self.image = self.sprites[self.current_sprite]
        
def animacao2():
    pg.quit()
    pg.init()
    clock = pg.time.Clock()    
    screen = pg.display.set_mode((sw, sh), pg.RESIZABLE)
    pg.display.set_caption("Animação do Sapo")
    moving_sprites = pg.sprite.Group()
    player = Player(160, -75)
    moving_sprites.add(player)
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
        screen.fill(Color.black)                        
        moving_sprites.draw(screen)
        moving_sprites.update()
        
        pg.display.flip()
        clock.tick(60)
        time.sleep(0.1)
        
        
def animacao3():
    pg.quit()
    pg.init()
    clock = pg.time.Clock()    
    screen = pg.display.set_mode((sw, sh), pg.RESIZABLE)
    pg.display.set_caption("Animação Espiral")
    
    PI = math.pi 
    
    start1 = PI/2
    end1 = PI + PI/4
    
    start2 = PI + PI/2
    end2 = PI/4
    
    start3 = 2 * PI - PI/4
    end3 = PI/2
    
    start4 = PI - PI/4
    end4 = PI + PI/2
    
    start5 = 0
    end5 = PI - PI/4
    
    start6 = PI
    end6 = 2 * PI - PI/4
    
    while True: 
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
        screen.fill(Color.lightGray)
                
        pg.draw.arc(screen, Color.blue, [230,150,150,100], start1, end1, 2)
        pg.draw.arc(screen, Color.mediumSlateBlue, [230,150,150,100], start2, end2, 2)
        
        pg.draw.arc(screen, Color.purple, [180,100,250,200], start3, end3, 2)
        pg.draw.arc(screen, Color.steelBlue, [180,100,250,200], start4, end4, 2)
        
        pg.draw.arc(screen, Color.mediumSlateBlue, [130,50,350,300], start5, end5, 2)
        pg.draw.arc(screen, Color.purple, [130,50,350,300], start6, end6, 2)
        
        pg.draw.arc(screen, Color.steelBlue, [80,0,450,400], start1, end1, 2)
        pg.draw.arc(screen, Color.mediumSlateBlue, [80,0,450,400], start2, end2, 2)
                
        start1 += PI/16
        end1 += PI/16
        start2 += PI/16
        end2 += PI/16
        start3 += PI/16
        end3 += PI/16
        start4 += PI/16
        end4 += PI/16
        start5 += PI/16
        end5 += PI/16
        start6 += PI/16
        end6 += PI/16
                        
        pg.display.flip()
        clock.tick(60)
        time.sleep(0.05)
galaticaX = 350
galaticaY = 200
def moveGalatica():
    galacticaX
def animacao4():
    pg.quit()
    pg.init()
    clock = pg.time.Clock()    
    screen = pg.display.set_mode((sw, sh), pg.RESIZABLE)
    pg.display.set_caption("Animação Galatica")
    imgGalaticaOrg = pg.image.load('galatica.jpeg')
    imgGalatica = pg.transform.scale(imgGalaticaOrg, (200, 180))    
    x = sw
    y = sh
    width, height = imgGalatica.get_rect().size
    while True: 
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
        screen.fill(Color.black)
        x -= 1
        y -= 1
        if(y + height  < 0):
            y = sh
            x = sw
        screen.blit(imgGalatica, (x, y))    
        pg.display.flip()
        clock.tick(100)        