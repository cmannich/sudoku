'''
Created on Feb 20, 2022

@author: Christoph Mannich
'''
# Include the PySFML extension
from sfml import sf

focusIndex = -1
font = sf.Font.from_file("/usr/share/fonts/truetype/hack/Hack-Regular.ttf")
font1 = sf.Font.from_file("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
font4 = sf.Font.from_file("/usr/share/fonts/opentype/cantarell/Cantarell-Bold.otf")
font2 = sf.Font.from_file("/usr/share/fonts/truetype/noto/NotoSerifDisplay-Regular.ttf")
font3 = sf.Font.from_file("/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf")
font5 = sf.Font.from_file("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
font6 = sf.Font.from_file("/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf")





# Each sudoku square contains an object defined by the class box which contains all aspects and state of the square
# except the text represented by the value. This was because some early problems with the text font (that still remain)
# Each sudoko contains 81 squares in an 9x9 grid. Each square has an index, 0 is top left and 80 is bottom right
# The rows are numbered 0 -8 and the columns are numbered 0-8.
# Each sudoko has 9 quadrants, each containing 3x3 squares
# 
# Hover over a square and press a number to enter the number into the square.
# Clear a square with space
# Press l to toggle the lock on the square.
# Press p to show possible numbers in empty squares.
# Paint an overlay on a square with mouse button

# Problems:
#    The sfml event handler crashes on scrollwheel events
#    The font renderer creates a point in the beginning of each string. 
#    Some fonts always has an extra character in the beginning of each string 



class box:
    def __init__(self, position: sf.Vector2, size: sf.Vector2, overlay = 0, background = 0 , value = " ", lock = 0, valueText = sf.Text()):
        self.position = position
        self.size = size
        self.overlay = overlay
        self.background = background
        self.value = value
        self.lock = lock
        self.possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.valueText = valueText

# Get the position and size of a square given it index
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
    return sf.Vector2(xpos,ypos), sf.Vector2(xsize,ysize)

# initialize the squares
square = []
def initSquare():
    for index in range(81):
        position, size = index2posSize(index)
        text = sf.Text()
        
        text.font = font1
        text.string = " " 
        text.character_size = 50
        text.color = sf.Color.WHITE
    
    
        xx = position.x + 20
        yy = position.y + 5
        textposition = sf.Vector2(xx,yy)
        text.position = textposition
        
        square.append(box(position, size, 0, 0, " ",valueText = text))

colorSquare = []
def initcolorMenu():
    xorig = 700
    yorig = 200
    step = 60
    color = 0

    for x in range(2):
        for y in range(4):
            position = sf.Vector2(xorig + x*step,yorig + y*step)
            size = sf.Vector2(50,50)
            colorSquare.append(box(position, size, color, 0, " "))
            color += 1

def renderColorMenu(window):
    xorig = 700
    yorig = 200
    step = 60
    color = 0
    
    rectangle = sf.RectangleShape(sf.Vector2(52,52))
    rectangle.position = sf.Vector2(xorig + step -1 ,yorig - step - 1)
    rectangle.fill_color = sf.Color(0,0,0,255)
    rectangle.outline_color = sf.Color(255,255,255,255)
    rectangle.outline_thickness = 1
    window.draw(rectangle)
    
    rectangle = sf.RectangleShape(sf.Vector2(50,50))
    rectangle.outline_thickness = 0
    rectangle.outline_color = getColor(0,255)

    for box in colorSquare:
            rectangle.position = box.position
            rectangle.size = box.size
            rectangle.fill_color = getColor(box.overlay)
            window.draw(rectangle)



# given a mouse position give the index of the square
def coor2index(position: sf.Vector2):
    xx = ((position.x - 11) // 75)
    yy = ((position.y - 11)// 75)
    if xx>8 or yy>8:
        return -1
    return xx + yy * 9

# It seemed a good idea in the beginning but has never been used
def index2coor(index: int):
    yy = index // 9
    xx = index - yy * 9 
    ypos = yy * 75 + 10
    xpos = xx * 75 + 10
    return sf.Vector2(xpos,ypos)

# Paint a square at a position, size and color. Used for background and overlay colors
def paintsquare(window, position: sf.Vector2, size: sf.Vector2, color: sf.Color):
    rectangle = sf.RectangleShape(size)
    rectangle.fill_color = color
    rectangle.position = position    
    window.draw(rectangle)

# The sudoku grid
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

def eventManager(window):
    running = True 
    global focusIndex
    global possible
    global square
    
    for event in window.events:
        if (type(event) == sf.CloseEvent):
            print("CloseEvent")
            running = False
        if (event == sf.MouseEvent):
            pass
        if (event == sf.MouseMoveEvent):
            index = coor2index(event.position)
            focusIndex = index
        if (event == sf.MouseButtonEvent):
            if event.pressed == True:
                index = coor2index(event.position)

                if index == -1: # Outside of the sudoku grid, placeholder for GUI work outside the sudoku
                    #check colormenu
                    checkColorMenu(event.position)
                    pass 
                else:           # Inside the sudoku grid
                    if square[index].overlay == overlayColor:
                        square[index].overlay = 0
                    else:
                        square[index].overlay = overlayColor
 

        if (event == sf.KeyEvent):
            pass
        if (event == sf.TextEvent):  # Keyboard interface
            c = event.unicode
            
            if (c == " " or ascii(c) >= ascii("1") and ascii(c) <= ascii("9")) and focusIndex != -1:
                if square[focusIndex].lock == 0:
                    square[focusIndex].value = c
                    if possible == True:
                        updatePossible()
            
            if c =="L" or c=="l":     # Locking the value, no accidental changes
                if square[focusIndex].lock == 0:
                    square[focusIndex].lock = 1
                    print("Locked")
                else:
                    square[focusIndex].lock = 0
                    print("Unlocked")
            
            if c =="P" or c=="p":     # Show the cheats, possible combinations, rudimentary right now
                if possible == False:
                    updatePossible()
                    possible = True
                else:
                    possible = False
       
    return running        

def checkColorMenu(position):
    global overlayColor
    for box in colorSquare:
        xx = position.x - box.position.x
        yy = position.y - box.position.y
        
        if xx > 0 and xx < box.size.x:
            if yy > 0 and yy < box.size.y:
                overlayColor = box.overlay
                print("Changed to: " + str(overlayColor))
            
        
        
# Just some predefined colors
# right now they are translucent (alfa is 128)
def getColor(color: int, alpha = 128):

    if color == 0:
        return sf.Color(0,0,0,0)
    elif color == 1:
        return sf.Color(255,0,0,alpha)
    elif color == 2:
        return sf.Color(0,255,0,alpha)
    elif color == 3:
        return sf.Color(0,0,255,alpha)
    elif color == 4:
        return sf.Color(255,255,0,alpha)
    elif color == 5:
        return sf.Color(0,255,255,alpha)
    elif color == 6:
        return sf.Color(255,0,255,alpha)
    else:
        return sf.Color(255,255,255,alpha)

# This is where we can paint translucent squares on top of the sudoku grid
def overlaylayer(window):
    for index in range(81):
        position = square[index].position
        size = square[index].size
        paintsquare(window, position, size, getColor(square[index].overlay))

# This is the rendering of the squares value 
def textlayer(window):
    
    for index in range(81):
        #text = textarray[index]
        text = square[index].valueText
        text.string = square[index].value
        if square[index].lock == 1:
            text.color = sf.Color.BLACK
        else:
            text.color = sf.Color.WHITE
        window.draw(text) 
         
# rendering of the background of the square in focus, the square you are hovering over is lighted up
def backgroundlayer(window):
    if focusIndex != -1:
        position = square[focusIndex].position
        size = square[focusIndex].size
        paintsquare(window, position, size, getColor(4))
    return 0

# A nice big square under the whole grid
def bottomColor(window):
    rectangle = sf.RectangleShape(sf.Vector2(679,679))
    rectangle.position = sf.Vector2(8,8)
    rectangle.fill_color = sf.Color(128,128,128,255)
    window.draw(rectangle)
    
# Not used right now
def firstCheat(windows):
    return 0

# Not used right now
def rulesLayer(windows):
    return 0

# Get the row of the square
def getRow(index):
    row = index // 9
    return row

# Get the column of the square
def getColumn(index):
    row = getRow(index)
    column = index - row * 9
    return column

# Get the 3x3 quadrant of the square
def getQuadrant(index):
    row = getRow(index)
    column = getColumn(index)
    quadrant = 3*(row//3) + column//3
    return quadrant

# Generate a list of indexes for a particular row
def getRowList(row):
    rowList = []
    for x in range(9):
        rowList.append(row*9 + x)
    return rowList

# Generate a list of indexes for a particular column
def getColumnList(column):
    columnList = []
    for x in range(9):
        columnList.append(column + x*9)
    return columnList

# Generate a list of indexes for a particular quadrant
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

# get the possible numbers for a specific square, according to sudoku rules
def getPossible(index):
    global square
    possibleList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    # Check 
    if square[index].value != " ":
        value = int(square[index].value)
        for x in range(9):
            possibleList[x] = 0
        possibleList[value - 1] = value
        return possibleList
    
    
    rowIndexList = getRowList(getRow(index))
    columnIndexList = getColumnList(getColumn(index))
    quadrantIndexList = getQuadrantList(getQuadrant(index))
    
    for index in rowIndexList:
        if square[index].value != " ":
            value = int(square[index].value)
            possibleList[value - 1] = 0
    for index in columnIndexList:
        if square[index].value != " ":
            value = int(square[index].value)
            possibleList[value - 1] = 0
    for index in quadrantIndexList:
        if square[index].value != " ":
            value = int(square[index].value)
            possibleList[value - 1] = 0
    
    #print(possibleList)
    return possibleList

# Update each square with the possible numbers        
def updatePossible():
    #global square
    
    for index in range(81):
        square[index].possible = getPossible(index)
        
# And now render the possible number layer        
def possibleLayer(window):
    global square
    
    if possible == False:
        return 0
    
    for index in range(81):
        for x in range(9):
            if square[index].value == " ":
                possibleList = square[index].possible
                value = possibleList[x]
                if value != 0:
                    xx = square[index].position.x
                    yy = square[index].position.y
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

#init square
initSquare()
initcolorMenu()
# Start the game loop
running = True

# we do not want to see possible number at startup
possible = False
overlayColor = 1

while running:

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
    
    renderColorMenu(window)

    window.display()

if __name__ == '__main__':
    pass