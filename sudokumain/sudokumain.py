'''
Created on Feb 20, 2022

@author: crim
'''
# Include the PySFML extension
from sfml import sf
from array import array
#import array as arr
from future.builtins import int
from _operator import index
from ast import Index

focusIndex = -1
font = sf.Font.from_file("/usr/share/fonts/truetype/hack/Hack-Regular.ttf")
font1 = sf.Font.from_file("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
font4 = sf.Font.from_file("/usr/share/fonts/opentype/cantarell/Cantarell-Bold.otf")
font2 = sf.Font.from_file("/usr/share/fonts/truetype/noto/NotoSerifDisplay-Regular.ttf")
font3 = sf.Font.from_file("/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf")
font5 = sf.Font.from_file("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
font6 = sf.Font.from_file("/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf")






class box:
    def __init__(self, position: sf.Vector2, size: sf.Vector2, overlay = 0, background= 0 , value = " ", lock = 0):
        self.position = position
        self.size = size
        self.overlay = overlay
        self.background = background
        self.value = value
        self.lock = lock
        self.possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def index2posSize(index: int):
    yposcomp = 0
    xposcomp = 0
    ysizecomp = 0
    xsizecomp = 0
    
    yy = index // 9
    xx = index - yy * 9
    
    if yy==0 or yy==3 or yy==6:
        yposcomp = 2
        ysizecomp = -2
    if xx==0 or xx==3 or xx==6:
        xposcomp = 2
        xsizecomp = -2
    ypos = yy * 75 + 11 + yposcomp
    xpos = xx * 75 + 10 + xposcomp

    if yy==2 or yy==5 or yy==8:
        ysizecomp = -2
    if xx==2 or xx==5 or xx==8:
        xsizecomp = -2

    ysize = 74 + ysizecomp
    xsize = 74 + xsizecomp

    #print("X:" + str(xpos) + " Y:" + str(ypos))
    return sf.Vector2(xpos,ypos), sf.Vector2(xsize,ysize)

fyrkant = []
for index in range(81):
    position, size = index2posSize(index)
    #size = sf.Vector2(75,75)
    fyrkant.append(box(position, size, 0, 0, " "))

textarray = []
for index in range(81):
    text = sf.Text()
    
    text.font = font1
    text.string = " " # str(fyrkant[index].value)
    text.character_size = 50
    text.color = sf.Color.WHITE

    xx = fyrkant[index].position.x +20
    yy = fyrkant[index].position.y +5
    position = sf.Vector2(xx,yy)

    text.position = position
    
    textarray.append(text)

def coor2index(position: sf.Vector2):
    #print(position)
    xx = ((position.x - 11) // 75)
    yy = ((position.y - 11)// 75)
    if xx>8 or yy>8:
        return -1
    #print("X:" + str(xx) + " Y:" + str(yy))
    return xx + yy * 9

def index2coor(index: int):
    yy = index // 9
    xx = index - yy * 9 
    ypos = yy * 75 + 10
    xpos = xx * 75 + 10
    #print("X:" + str(xpos) + " Y:" + str(ypos))
    return sf.Vector2(xpos,ypos)

def paintFyrkant(window, position: sf.Vector2, size: sf.Vector2, color: sf.Color):
    
    rectangle = sf.RectangleShape(size)
    rectangle.fill_color = color
    rectangle.position = position    
    window.draw(rectangle)


def grid(window):

    
    rectangle = sf.RectangleShape(sf.Vector2(679,5))
    
    xpos = 8
    ypos = 8
    for x in range(4):
        rectangle.position = sf.Vector2(xpos,ypos)
        window.draw(rectangle)
        ypos = ypos + 225

    xpos = 12
    ypos = 8
    
    rectangle.rotate(90)
        
    for x in range(4):
        rectangle.position = sf.Vector2(xpos,ypos)
        window.draw(rectangle)
        xpos = xpos + 225

    rectangle = sf.RectangleShape(sf.Vector2(676,1))
    rectangle.position = sf.Vector2(10,10)
    rectangle.fill_color = sf.Color.RED
    #window.draw(rectangle)
    xpos = 9
    ypos = 10
    
    for y in range(10):
        rectangle.position = sf.Vector2(xpos,ypos)
        window.draw(rectangle)
        ypos = ypos + 75
    
    xpos = 10
    ypos = 10
    rectangle.rotate(90)
    
    for x in range(10):
        rectangle.position = sf.Vector2(xpos,ypos)
        window.draw(rectangle)
        xpos = xpos + 75

#def onsegments(window):
def eventManager(window):
    running = True 
    global focusIndex
    global possible
    global fyrkant
    
    for event in window.events:
        #print(event)
        if (type(event) == sf.CloseEvent):
            print("CloseEvent")
            running = False
    
        if (event == sf.MouseEvent):
            pass#print("MouseEvent")
            
        
        if (event == sf.MouseMoveEvent):
            index = coor2index(event.position)
            focusIndex = index
            #print("Movement:" + str(focusIndex))
            
        if (event == sf.MouseButtonEvent):
            if event.pressed == True:
                #print("Button down ")# + event.button + ":" + event.position)
                #print(event.button)
                
                index = coor2index(event.position)

                if index == -1:
                    pass#print("Outside")
                else:
                    #print("Inside")
                    
                    if fyrkant[index].overlay == 0:
                        #print("Setting fyrkant[" + str(index) + "] = 1")
                        fyrkant[index].overlay = 1
                    else:
                        #print("Setting fyrkant[" + str(index) + "] = 0")
                        fyrkant[index].overlay = 0
                   
            #else:
                #print("Button up")
            #print("MouseButtonEvent")
            #print("X=" + event.y + " , Y=" + event.y)
        if (event == sf.KeyEvent):
            pass#print("KeyEvent")
        if (event == sf.TextEvent):
            c = event.unicode
            
            if (c == " " or ascii(c) >= ascii("1") and ascii(c) <= ascii("9")) and focusIndex != -1:
                if fyrkant[focusIndex].lock == 0:
                    fyrkant[focusIndex].value = c
                    if possible == True:
                        updatePossible()
                    #print(getQuadrant(focusIndex))
                    #print(getQuadrantList(getQuadrant(focusIndex)))
                    #print("KeyText: " + c)
            
            if c =="L" or c=="l":
                if fyrkant[focusIndex].lock == 0:
                    fyrkant[focusIndex].lock = 1
                    print("Locked")
                else:
                    fyrkant[focusIndex].lock = 0
                    print("Unlocked")
            
            if c =="P" or c=="p":
                if possible == False:
                    updatePossible()
                    possible = True
                else:
                    possible = False
       
    return running        

def getColor(color: int):

    if color == 1:
        return sf.Color(255,0,0,128)
    elif color == 2:
        return sf.Color(0,255,0,128)
    elif color == 3:
        return sf.Color(0,0,255,128)
    elif color == 4:
        return sf.Color(255,255,0,128)
    elif color == 5:
        return sf.Color(0,255,255,128)
    elif color == 6:
        return sf.Color(255,0,255,128)
    else:
        return sf.Color(255,255,255,128)
    


def overlaylayer(window):
    for index in range(81):
        if fyrkant[index].overlay == 1:
            #print("Index:" + str(index))
            position = fyrkant[index].position
            size = fyrkant[index].size
            paintFyrkant(window, position, size, getColor(1))

def textlayer(window):
    global font
    global textarray
    global fyrkant
    
    for index in range(81):
        text = textarray[index]
        text.string = fyrkant[index].value
        if fyrkant[index].lock == 1:
            text.color = sf.Color.BLACK
        else:
            text.color = sf.Color.WHITE
        window.draw(text)  
    
    
    

def backgroundlayer(window):
    if focusIndex != -1:
        position = fyrkant[focusIndex].position
        size = fyrkant[focusIndex].size
        paintFyrkant(window, position, size, getColor(4))
    return 0

def bottomColor(window):
    rectangle = sf.RectangleShape(sf.Vector2(679,679))
    rectangle.position = sf.Vector2(8,8)
    rectangle.fill_color = sf.Color(128,128,128,255)
    window.draw(rectangle)
    
def firstCheat(windows):
    return 0

def rulesLayer(windows):
    return 0

def getRow(index):
    row = index // 9
    return row

def getColumn(index):
    row = getRow(index)
    column = index - row * 9
    return column

def getQuadrant(index):
    row = getRow(index)
    column = getColumn(index)
    quadrant = 3*(row//3) + column//3
    return quadrant

def getRowList(row):
    rowList = []
    for x in range(9):
        rowList.append(row*9 + x)
    return rowList

def getColumnList(column):
    columnList = []
    for x in range(9):
        columnList.append(column + x*9)
    return columnList

def getQuadrantList(quadrant):
    quadrantList = []
    topCornerIndex = (quadrant//3)*3*9 # 0-2 => 0, 3-5 => 27, 6-8 => 54
    plusIndex = (quadrant%3)*3 # 0,3,6 => 0, 1,4,7 => 1, 2,5,8 => 2
    #print("Q:" + str(quadrant) + " topCorner:" + str(topCornerIndex) + " plusIndex:" + str(plusIndex))
    for x in range(3):
        quadrantList.append(topCornerIndex + plusIndex + x)
        quadrantList.append(topCornerIndex + plusIndex + x + 9)
        quadrantList.append(topCornerIndex + plusIndex + x + 18)
    return quadrantList


def getPossible(index):
    global fyrkant
    possibleList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    # Check 
    if fyrkant[index].value != " ":
        value = int(fyrkant[index].value)
        for x in range(9):
            possibleList[x] = 0
        possibleList[value - 1] = value
        #print(possibleList)
        return possibleList
    
    
    rowIndexList = getRowList(getRow(index))
    columnIndexList = getColumnList(getColumn(index))
    quadrantIndexList = getQuadrantList(getQuadrant(index))
    
    for index in rowIndexList:
        if fyrkant[index].value != " ":
            value = int(fyrkant[index].value)
            possibleList[value - 1] = 0
    for index in columnIndexList:
        if fyrkant[index].value != " ":
            value = int(fyrkant[index].value)
            possibleList[value - 1] = 0
    for index in quadrantIndexList:
        if fyrkant[index].value != " ":
            value = int(fyrkant[index].value)
            possibleList[value - 1] = 0
    
    #print(possibleList)
    return possibleList

def possibleString(index):
    global fyrkant
    # Check 
    if fyrkant[index].value != " ":
        return ""
    
    possibleList = getPossible(index)
    
    text = ""
    for x in range(9):
        value = possibleList[x]
        if x == 3:
            text = text + "\n"
        if x == 6:
            text = text + "\n"
        if value == 0:
            text = text + " "
        else:
            text = text + str(value)
    
    #print(text)
    return text
        
def updatePossible():
    global fyrkant
    
    for index in range(81):
        fyrkant[index].possible = getPossible(index)
        
        
def possibleLayer(window):
    global fyrkant
    
    if possible == False:
        return 0
    
    for index in range(81):
        for x in range(9):
            if fyrkant[index].value == " ":
                possibleList = fyrkant[index].possible
                value = possibleList[x]
                if value != 0:
                    xx = fyrkant[index].position.x
                    yy = fyrkant[index].position.y
                    xxx = (x%3) * 23 + 5
                    yyy = (x//3) * 22 + 1
                    
                    text = sf.Text()
                    text.font = font1
                    text.string = str(value)
                    text.character_size = 20
                    text.color = sf.Color(255,255,255,100)
                    text.position = sf.Vector2(xx + xxx, yy + yyy)
                    window.draw(text)
        
        
# Create the main window
window = sf.RenderWindow(sf.VideoMode(1024, 768), "PySFML test")
window.vertical_synchronization = True
# Create a graphical string to display



#for index in textarray:
#    window.draw(textarray[index])

text1 = sf.Text()
text1.font = font1
text1.string = "AAAA\nAAAA"
text1.character_size = 100
text1.color = sf.Color(255,255,255,100)
text1.position = sf.Vector2(700,200)
text1.style = sf.Text.UNDERLINED


# Start the game loop
running = True
xsegment = 0
ysegment = 0

possible = False

while running:
    #event = sf.Event()
    running = eventManager(window)
    


    # Clear screen, draw the text, and update the window
    window.clear()

    bottomColor(window)
    
    #the sudoku grid
    grid(window)
    
    backgroundlayer(window)
    
    possibleLayer(window)
   
    textlayer(window)
    
    overlaylayer(window)
    
#    for text in textarray:
#        window.draw(text) 
    
    # window.draw(text1)
    # text1.rotate(90)
    # window.draw(text1)
    # text1.rotate(-90)
    #

    window.display()
    
    #print("*")

if __name__ == '__main__':
    pass