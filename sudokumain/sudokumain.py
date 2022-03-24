'''
Created on Feb 20, 2022

@author: Christoph Mannich
'''
# Include the PySFML extension
from sfml import sf
import json

# ttt = { "Squares" : [
#     { "Id" : 0, "Value" : "0", "Locked" : 0},
#     { "Id" : 1, "Value" : "4", "Locked" : 0},
#     { "Id" : 2, "Value" : "3", "Locked" : 1},
#     { "Id" : 3, "Value" : "5", "Locked" : 0},
#     { "Id" : 4, "Value" : "6", "Locked" : 0}
#     ]}
#
# print(json.dumps(ttt, indent=4))
# exit()



focusIndex = -1

# Start the game loop
running = True

# we do not want to see possible numbers at startup
possible = 0
only = 0
lonely = 0
pair = 0

overlayColor = 1

font = sf.Font.from_file("/usr/share/fonts/truetype/freefont/FreeSans.ttf")
font1 = sf.Font.from_file("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf")
#	font1 = sf.Font.from_file("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
#	font4 = sf.Font.from_file("/usr/share/fonts/opentype/cantarell/Cantarell-Bold.otf")
#	font2 = sf.Font.from_file("/usr/share/fonts/truetype/noto/NotoSerifDisplay-Regular.ttf")
#	font3 = sf.Font.from_file("/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf")
#	font5 = sf.Font.from_file("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
#	font6 = sf.Font.from_file("/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf")


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

saveFile = "sudoku_save.json"

def save():
    saveList = []
    for index in range(len(square)):
        box = square[index]
        value = box.value
        lock = box.lock
        key = {"Index": index, "Value": value, "Lock": lock}
        saveList.append(key)
        
    output = {"Square": saveList}
    f = open(saveFile, "w")
    f.write(json.dumps(output, indent=4))
    f.close()

def load():
    f = open(saveFile)
    y = json.loads(f.read())
    saveList = y["Square"]
    
    for dict in saveList:
        index = dict["Index"]
        value = dict["Value"]
        lock = dict["Lock"]
        square[index].value = value
        square[index].lock = lock

def clear():
    for index in range(len(square)):
        square[index].value = " "
        square[index].lock = 0
        square[index].overlay = 0

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

class fileMenu():
    def __init__(self, xpos = 700, ypos = 10):
        self.position = sf.Vector2(xpos,ypos)
        self.checkBox = []
        
        step = 35
        color = 0  
        xsize = 80
        ysize = 27

        position = sf.Vector2(xpos,ypos)
        size = sf.Vector2(xsize,ysize)
        self.checkBox.append(box(position, size, color, valueText="SAVE"))

        position = sf.Vector2(xpos,ypos + step)
        size = sf.Vector2(xsize,ysize)
        self.checkBox.append(box(position, size, color, valueText="LOAD"))

        position = sf.Vector2(xpos,ypos + 2*step)
        size = sf.Vector2(xsize,ysize)
        self.checkBox.append(box(position, size, color, valueText="CLEAR"))
 
    def render(self,window):
        #checkbox1
        rectangle = sf.RectangleShape(sf.Vector2(27,27))
        
        text = sf.Text()
        text.font = font1
        text.string = "" 
        text.character_size = 23
        text.color = sf.Color.WHITE
        
        for box in self.checkBox:
            # Button rectangle
            rectangle.position = box.position
            rectangle.size = box.size
            rectangle.fill_color = sf.Color.BLACK
            rectangle.outline_color = sf.Color.WHITE
            rectangle.outline_thickness = 1
            window.draw(rectangle)
            
            #Text
            text.position = sf.Vector2(box.position.x + 5, box.position.y)
            text.string = box.valueText
            window.draw(text)
        
    def check(self, position):
        for index in range(len(self.checkBox)):
            box = self.checkBox[index]
            xx = position.x - self.checkBox[index].position.x
            yy = position.y - self.checkBox[index].position.y
            
            if xx > 0 and xx < box.size.x:
                if yy > 0 and yy < box.size.y:
                    if index == 0:
                        save()
                        print("SAVE")            
                    if index == 1:
                        load()
                        print("LOAD")            
                    if index == 2:
                        clear()
                        print("CLEAR")            


class possibleMenu():
    def __init__(self, xpos = 700, ypos = 10):
        self.position = sf.Vector2(xpos,ypos)
        self.checkBox = []

        step = 35
        color = 0  
        xsize = 27
        ysize = 27
        
        position = sf.Vector2(xpos,ypos)
        size = sf.Vector2(xsize,ysize)
        self.checkBox.append(box(position, size, color, valueText="Possible"))

        position = sf.Vector2(xpos,ypos + step)
        size = sf.Vector2(xsize,ysize)
        self.checkBox.append(box(position, size, color, valueText="Only"))

        position = sf.Vector2(xpos,ypos + 2*step)
        size = sf.Vector2(xsize,ysize)
        self.checkBox.append(box(position, size, color, valueText="Lonely"))

        position = sf.Vector2(xpos,ypos + 3*step)
        size = sf.Vector2(xsize,ysize)
        self.checkBox.append(box(position, size, color, valueText="Pair"))
        
    def render(self,window):
        #checkbox1
        rectangle = sf.RectangleShape(sf.Vector2(27,27))
        
        text = sf.Text()
        text.font = font1
        text.string = "" 
        text.character_size = 23
        text.color = sf.Color.WHITE
        
        for box in self.checkBox:
            # checkbox rectangle
            rectangle.position = box.position
            rectangle.size = box.size
            rectangle.fill_color = sf.Color.BLACK
            rectangle.outline_color = sf.Color.WHITE
            rectangle.outline_thickness = 1
            window.draw(rectangle)

            # checkbox filled?
            rectangle.outline_thickness = 0
            rectangle.position = sf.Vector2(box.position.x + 3, box.position.y + 3)
            rectangle.size = sf.Vector2(box.size.x - 6, box.size.y - 6)
            rectangle.fill_color = getColor(box.overlay,255)
            window.draw(rectangle)
            
            #Text
            text.position = sf.Vector2(box.position.x + box.size.x + 5, box.position.y)
            text.string = box.valueText
            window.draw(text)
        
    def check(self, position):
        global possible, only,lonely,pair
        print("Possible =" + str(possible))
        for index in range(len(self.checkBox)):
            box = self.checkBox[index]
            xx = position.x - self.checkBox[index].position.x
            yy = position.y - self.checkBox[index].position.y
            
            if xx > 0 and xx < box.size.x:
                if yy > 0 and yy < box.size.y:
                    if index == 0:
                        if possible == 0:
                            possible = 1
                            self.checkBox[index].overlay = 7
                            print("Possible ON")            
                        else:
                            possible = 0
                            self.checkBox[index].overlay = 0
                            print("Possible OFF")            
                    if index == 1:
                        if only == 0:
                            only = 1
                            self.checkBox[index].overlay = 7
                            print("Possible ON")            
                        else:
                            only = 0
                            self.checkBox[index].overlay = 0
                            print("Possible OFF")            
                    if index == 2:
                        if lonely == 0:
                            lonely = 1
                            self.checkBox[index].overlay = 7
                            print("Possible ON")            
                        else:
                            lonely = 0
                            self.checkBox[index].overlay = 0
                            print("Possible OFF")            
                    if index == 3:
                        if pair == 0:
                            pair = 1
                            self.checkBox[index].overlay = 7
                            print("Possible ON")            
                        else:
                            pair = 0
                            self.checkBox[index].overlay = 0
                            print("Possible OFF")            
                    updatePossible()

    def update(self, index, onOff):
        pass
        if onOff:
            self.checkBox[index].overlay = 7
        else:
            self.checkBox[index].overlay = 0
        
    def test(self,position):
        global possible
        if possible == 0:
            possible = 1
        else:
            possible = 0
             
class colorMenu():
    def __init__(self, xpos = 700, ypos = 200):
        self.position = sf.Vector2(xpos,ypos)
        self.colorSquare = []
        
        self.xorig = xpos
        self.yorig = ypos
        self.step = 60
        color = 0
    
        for x in range(2):
            for y in range(4):
                position = sf.Vector2(self.xorig + x*self.step,self.yorig + y*self.step)
                size = sf.Vector2(50,50)
                self.colorSquare.append(box(position, size, color, 0, " "))
                color += 1

    def render(self, window):
        #global overlayColor
        
        rectangle = sf.RectangleShape(sf.Vector2(52,52))
        rectangle.position = sf.Vector2(self.xorig + self.step -1 ,self.yorig - self.step - 1)
        rectangle.fill_color = sf.Color(0,0,0,255)
        rectangle.outline_color = sf.Color(255,255,255,255)
        rectangle.outline_thickness = 1
        window.draw(rectangle)
        
        #rectangle = sf.RectangleShape(sf.Vector2(50,50))
        rectangle.outline_thickness = 0
        rectangle.fill_color = getColor(overlayColor)
        rectangle.outline_color = getColor(0,255)
        window.draw(rectangle)
        
        
    
        for box in self.colorSquare:
                rectangle.position = box.position
                rectangle.size = box.size
                rectangle.fill_color = getColor(box.overlay)
                window.draw(rectangle)

    def check(self, position):
        global overlayColor
        for box in self.colorSquare:
            xx = position.x - box.position.x
            yy = position.y - box.position.y
            
            if xx > 0 and xx < box.size.x:
                if yy > 0 and yy < box.size.y:
                    overlayColor = box.overlay
                    print("Changed to: " + str(overlayColor))

   
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
    global menu2
    
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
                    
                    menu1.check(event.position) # overlay color
                    menu2.check(event.position) # possibility options
                    menu3.check(event.position)
                     
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
                    menu2.update(0,1)
                    possible = True
                else:
                    menu2.update(0,0)
                    possible = False
       
    return running        


        
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

# check a square if one of the possible numbers in the square
# is the only possible number in its row, column or quadrant
def updateOnly(index):

	for row in range(9):
		rowList = getRowList(row)
		updateOnlyList(rowList)

	for column in range(9):
		columnList = getColumnList(column)
		updateOnlyList(columnList)

	for quadrant in range(9):
		quadrantList = getQuadrantList(quadrant)
		updateOnlyList(quadrantList)
		
	
	#print(rowList)
	
def updateOnlyList(indexList):
	singeltonIndexes = []
	totalCount = [0,0,0,0,0,0,0,0,0]
	for index in indexList:
		possible = square[index].possible
		for value in possible:
			if value > 0:
				totalCount[value - 1] = totalCount[value - 1] + 1
	print(totalCount)
	# we now know how many times each number apears
	# if a number only apears 1 time we must save the index (find it again first)
	numbers = []
	for number in range(9):
		if totalCount[number] != 0 and totalCount[number] < 2:
			numbers.append(number)
	print(numbers)
	
	# OK did we find any?
	if len(numbers):
		# yes
		for x in numbers:
			# find the index, there will only be one index for each found number
			for index in indexList:
				# check if possibility contains number
				possible = square[index].possible
				if possible[x] > 0:
					singeltonIndexes.append(index) # found index
		print(singeltonIndexes)
		
		#Update possible square
		for x in range(len(singeltonIndexes)):
			index = singeltonIndexes[x]
			value = numbers[x]
			square[index].possible = [0,0,0,0,0,0,0,0,0]
			square[index].possible[value] = value + 1
			print(square[index].possible)

	
	
	
		
# Update each square with the possible numbers        
def updatePossible():
    #global square

	for index in range(81):
		square[index].possible = getPossible(index)
	if only == 1:
		updateOnly(13)

# And now render the possible number layer        
def renderPossible(window):
    #global square
    
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

#init menus
menu1 = colorMenu(700, 400)
menu2 = possibleMenu(700, 10)
menu3 = fileMenu(900,10)
#init square
initSquare()

while running:
    try:
        #running = eventManager(window)
        pass
    except:
        pass
    running = eventManager(window)
    # Clear screen, draw the text, and update the window
    window.clear()

    bottomColor(window)
    
    #the sudoku grid
    grid(window)
    
    backgroundlayer(window)
    
    renderPossible(window)
   
    textlayer(window)
    
    overlaylayer(window)
    
    menu1.render(window)
    menu2.render(window)
    menu3.render(window)
    
    
    window.display()

if __name__ == '__main__':
    pass
