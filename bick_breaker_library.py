# Brick - Breaker LIBRARY
from graphics import *
import random

class Paddle:
    def __init__(self, window, space_from_bottom, paddle_width, paddle_height):
        paddle_x = (window.getWidth()-paddle_width)/2
        paddle_y = window.getHeight() - space_from_bottom
        self.rectangle = Rectangle(Point(paddle_x, paddle_y), Point(paddle_x + paddle_width, paddle_y + paddle_height))
        self.rectangle.setFill("light green")
        self.rectangle.setOutline("white")
        self.rectangle.draw(window)

    def moveByKey(self, key, win_width, offset):
        p1 = self.rectangle.getP1()
        p2 = self.rectangle.getP2()
        if key == 'Right' and p2.getX() < win_width:
                self.rectangle.move(offset,0)
        elif key == 'Left' and p1.getX() > 0:
                self.rectangle.move(-1*offset,0)

    def getSurfaceCenter(self):
        p1 = self.rectangle.getP1()
        p2 = self.rectangle.getP2() 
        self.SurfaceCenter = Point((p1.getX()+p2.getX())/2, p1.getY())
        return(self.SurfaceCenter)
    
    def resetToCenter(self, window):
        center = self.getSurfaceCenter()
        paddle_width = self.rectangle.getP2().getX() - self.rectangle.getP1().getX()
        win_width = window.getWidth()
        self.rectangle.move((win_width - paddle_width)/2 - self.rectangle.getP1().getX(),0)
       
    def getRectangle(self):
        return self.rectangle

class Brick:
    def __init__(self, x, y, width, height, color, window, text):
        self.rectangle = Rectangle(Point(x, y), Point(x+width, y+height))
        self.rectangle.setFill(color)
        self.rectangle.draw(window)
        self.text = text

    def getRectangle(self):
        return self.rectangle

    def getScore(self):
        sum = 0
        for ch in self.text:
            if ch.lower():
                sum = sum + ord(ch)-97
        return(sum)
    
class Ball:
    def __init__(self, window, paddle, radius):
        p = paddle.getSurfaceCenter()
        self.circle = Circle(Point(p.getX(), p.getY()-radius), radius)
        self.circle.setFill("yellow")
        self.circle.draw(window)
        self.direction = []
        
    def moveIt(self):
        di = self.getDirectionSpeed()
        x = di[0]
        y = di[1]
        self.circle.move(x,y)

    def resetToPaddle(self, paddle):
        p = paddle.getSurfaceCenter()
        rad = self.circle.getRadius()
        center = self.circle.getCenter()
        self.circle.move(p.getX() - center.getX(), p.getY() - center.getY()- rad)

    def setRandomDirectionSpeed(self, min_speed=0.85, max_speed=3.0):
        x_offset = random.uniform(min_speed,max_speed)
        t = random.random()
        if x_offset < t:
            x_offset = x_offset*-1
        y_offset = random.uniform(-1*min_speed,-1*max_speed)
        dr = []
        dr.append(x_offset)
        dr.append(y_offset)
        self.setDirectionSpeed(dr)
        
    def getDirectionSpeed(self):
        return self.direction

    def setDirectionSpeed(self, d):
        self.direction = d

    def reverseX(self):          
        dr = self.getDirectionSpeed()
        dr[0] = dr[0]*-1         #negate x - coordinate of initial direction of ball
        
    def reverseY(self):          
        dr = self.getDirectionSpeed()
        dr[1] = dr[1]*-1         #negate y - coordinate of initial direction of ball

    def checkHitWindow(self, window):
        p1 = self.circle.getP1()
        p2 = self.circle.getP2()
        if p1.getX() <= 0:
            return True
        elif p1.getY() <= 0:
            return True
        elif p2.getX() >= window.getWidth():
            return True
        else:
            return False

    def checkHit(self, rectangle):
        ball_p1 = self.circle.getP1()
        ball_p2 = self.circle.getP2()
        center = self.circle.getCenter()
        rad = self.circle.getRadius()
        x = center.getX()
        y = center.getY()

        p1 = rectangle.getP1()
        p2 = rectangle.getP2()
       
        rec_center_x = rectangle.getCenter().getX()
        rec_center_y = rectangle.getCenter().getY()
        
        w = abs(p2.getX() - p1.getX())
        h = abs(p2.getY() - p1.getY())

        dist_x = abs(x - rec_center_x)
        dist_y = abs(y - rec_center_y)

        if dist_x > (w/2 + rad) or dist_y > (h/2 + rad): return False
        if dist_x <= (w/2 + rad) or dist_y <= (h/2 + rad): return True

        elif rad**2 >= ((p2.getX()-x)**2 + (p1.getY()-y)**2) or rad**2 >= ((p2.getX()-x)**2 + (p2.getY()-y)**2)or rad**2 >= ((p1.getX()-x)**2 + (p2.getY()-y)**2) or rad**2 >=((p1.getX()-x)**2 + (p1.getY()-y)**2):
            return True
        
        return False

def setupMessageScoreAndLifeInput(window, offset_from_center_x, offset_from_bottom):
    win_ht = window.getHeight()
    win_center = window.getWidth()/2
    score = Text(Point(win_center + offset_from_center_x,win_ht - offset_from_bottom),"SCORE:   ") 
    score.setTextColor("white")
    score.draw(window)
    score_number = Text(Point(win_center + 2*offset_from_center_x,win_ht - offset_from_bottom),"0")
    score_number.setTextColor("white")
    score_number.draw(window)
    life = Text(Point(win_center - (2*offset_from_center_x),win_ht - offset_from_bottom),"LIFE: ")
    life.setTextColor("white")
    life.draw(window)
    life_box = Entry(Point(win_center - offset_from_center_x,win_ht - offset_from_bottom),3)
    life_box.getText() 
    life_box.draw(window)
    message = Text(Point(win_center,win_ht - 2*offset_from_bottom),"")
    message.setTextColor("red")
    message.draw(window)
    return(message,score_number,life,life_box)

def getLinesOfWords(filename):    #function to convert all words to lowercase and create a list of words with length between 2 and 8 characters 
    final_list = []
    ifile = open(filename,"r")
    for line in ifile:
        brickchar = []     
        for word in line:
            word = word.lower()
            for ch in word: 
                if ch.isalnum() == True:
                    brickchar.append(ch)        
                else:
                    brickchar.append(" ")
        s = "".join(brickchar)
        word_list = []
        for word in s.split():
            if len(word) <= 8 and len(word) >= 2:
                word_list.append(word)
        final_list.append(word_list)
    return(final_list)

def makeLifeStatic(window, life_input): 
    num = int(life_input.getText())
    entry_location = life_input.getAnchor()
    output_life = Text(entry_location,num)
    output_life.setTextColor("white")
    life_input.undraw()
    output_life.draw(window)
    return(num, output_life)

def updateScore(score_offset, score_num_text):
    score = score_num_text.getText()
    score_offset = score_offset + int(score)
    score_string = str(score_offset)
    score_num_text.setText(score_offset)


















