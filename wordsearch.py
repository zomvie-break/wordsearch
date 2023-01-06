#!/home/victor/python_projects/crosswords/venv/bin/python3
import numpy as np                      #numpy
import copy                             #for deep copy
from string import ascii_lowercase      #for getting random ascii characters to fill the crossword

# reportlab imports for working with PDFs
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

# usefull when dealing with a text file which contains translations and other info about the word.
import re

class Tile:
    def __init__(self, value="-"):
        """Initialize a tile with the value of - """
        self.value = value

    def __eq__(self, other):
        """overwrites the equals operator"""
        if isinstance(other, Tile):
            return self.value == other.value
        else:
            return False

class Crossword:
    def __init__(self, dimension_x, dimension_y):
        # sets a basic list of lists given some dirmensions
        self.dimension_x=dimension_x 
        self.dimension_y=dimension_y
        self.crossword=self.create_empty_crossword()
        self.def_value = self.crossword[0][0].value
    
    def create_empty_crossword(self):
        # generates an empty crossword given some dimensions
        #  x * y (ys are rows and xs are columns)
        ys = self.dimension_y
        xs = self.dimension_x
        crossword = []
        for y in range(ys):
            # for loop to fill in the crossword with empty tiles.
            temp = []
            for x in range(xs):
                temp.append(Tile())
            crossword.append(temp)
        return crossword
        
    def print_crossword(self):
        """
        prints the crossword to the terminal in an understandable way
        """
        for y in range(len(self.crossword)):
            for tile in self.crossword[y]:
                print(tile.value, end="  ")
            print()
        print()

    def place_word_h(self, word, loc_x, loc_y, backwards=False):
        """Place a word in the crossword, horizontaly"""
        len_word=len(word)
        # check if the word fits in the selected location
        if loc_x+len_word>self.dimension_x:
            print('word is too big!')
            return False
        else:
            # dummy crossword to which we make changes before commiting to the real one
            # deepcopy because otherwise we copy the reference, and we dont want that
            fake_crossword = copy.deepcopy(self.crossword)
            # inverts the word
            if backwards:
                word=word[::-1]
            
            # variable to keep track of the location in the crossword 
            temp_loc_x=0
            for char in word:
                if fake_crossword[loc_y][loc_x+temp_loc_x].value == self.def_value or fake_crossword[loc_y][loc_x+temp_loc_x].value == char:
                    fake_crossword[loc_y][loc_x+temp_loc_x].value = char
                    temp_loc_x += 1
                else:
                    return False
            # if the assignation of characters is complete,
            # point the self.crossword to the fake_crossword
            self.crossword = fake_crossword
            return True

    def place_word_v(self, word, loc_x, loc_y, backwards=False):
        """Place a word in the crossword, horizontaly"""
        len_word=len(word)
        if loc_y+len_word>self.dimension_y:
            print('word is too big!')
        else:
            fake_crossword = copy.deepcopy(self.crossword)
            if backwards:
                word=word[::-1]
            temp_loc_y=0
            for char in word:
                # tile = self.crossword[loc_y][loc_x+temp_loc_x]
                # print(f'tile: {tile}\tdefvalue: {self.def_value}')
                if fake_crossword[loc_y+temp_loc_y][loc_x].value == self.def_value or  fake_crossword[loc_y+temp_loc_y][loc_x].value == char:
                    fake_crossword[loc_y+temp_loc_y][loc_x].value = char
                    temp_loc_y += 1
                else:
                    return False
            self.crossword=fake_crossword
            return True
        
    def get_random_loc(self, x=None, y=None):
        """
        Function that returns a random location within the arra7. El profesor Pastor en el laboratorio.y
        """
        # if no arguments are passed for x or y, dimension_x and dimension_y are used.
        if x==None or y==None:
            x=self.dimension_x
            y=self.dimension_y
        x_loc = np.random.randint(x)
        y_loc = np.random.randint(y)
        return x_loc, y_loc

    def fill_empty_places(self):
        # fill the spaces with the default value with ascii lowercase characters.
        for i in range(len(self.crossword)):
            for j in range(len(self.crossword[i])):
                if self.crossword[i][j].value == self.def_value:
                    self.crossword[i][j].value = np.random.choice([x for x in ascii_lowercase])


    def addWords(self, dimensions, file_name, difficulty = 1):
        with open('/home/victor/python_projects/crosswords/word_list.txt') as f:
             lines = f.readlines()

        lines = [line.strip() for line in lines]

        words = [re.findall(r'(.*) -', line) for line in lines]

        # Here is the actual filling of the crossword.
        max_attempts = 1000
        failed_words = []
        for word in words:
            flag = False
            for i in range(max_attempts):
                loc_x, loc_y = self.get_random_loc()
                if i%3==0:
                    flag =self.place_word_h(word, loc_x, loc_y,backwards=True)
                elif i%2==0:
                    flag = self.place_word_v(word, loc_x, loc_y, backwards=True)
                if flag:
                    self.print_crossword()
                    flag=False
                    break
                if i== max_attempts-1:
                    print(f'failed to add word: {word}')
                    failed_words.append(word)
        print(f'words attepted: {len(words)}\twords failed: {len(failed_words)}')
        print(failed_words)
        self.fill_empty_places()
        self.print_crossword()

class PDFHelper:
    def __init__(self):
        pass

    def create_crossword(self, crossword, filename='crossword.pdf', title = ''):
        """
        Takes a crossword (an instance of the crossword class) and a file name (crossword.pdf as default)
        """
        # initialize the SimpleDocTemplate with som standard values
        doc = SimpleDocTemplate(filename,
                            paper_size=letter,
                            bottomMargin=0.4*inch,
                            topMargin=0.4*inch,
                            rightMargin=0.4*inch,
                            leftMargin=0.4*inch)
        # array used to store the values of the tiles of the crossword 
        temp=[]
        # array used to store the arrays to be used as rows in the table
        tab=[]
        for row in range(len(crossword.crossword)):
            for col in range(len(crossword.crossword[row])):
                temp.append(crossword.crossword[row][col].value)
            tab.append(temp)
            temp=[] 

        # style templates from reportlab
        styles = getSampleStyleSheet()
        # styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        t0 = Paragraph('My User Names\n\n', styles['Heading1'])
        # print(f'col={crossword.dimension_x}\trow={crossword.dimension_y}\ttype={type(crossword.dimension_x)}')

        # the colWidths and rowHeights are difined as the space beteween cells, and take an array such as [0.2*inch, 0.2*inch ...]
        t1 = Table(tab, colWidths=[0.2*inch]*crossword.dimension_x, rowHeights=[0.2*inch]*crossword.dimension_y) # dimensions required
        t1.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 2, colors.black)]))

        # list to save the elements to be attached in the PDF
        elements = []
        elements.append(t0)
        elements.append(t1)
        doc.build(elements)


if __name__ == "__main__":
    with open('/home/victor/python_projects/crosswords/word_list.txt') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    words = [re.findall(r'(.*) -', line) for line in lines]

    # set dimensions of the crossword
    cw = Crossword(20, 30)
    print('empty crossword')
    cw.print_crossword()


    file_name = '/home/victor/python_projects/crosswords/word_list.txt'
    dimensions = [20,30]

    cw.addWords(dimensions, file_name)

    pdf_helper = PDFHelper()
    pdf_helper.create_crossword(cw, title='My crossword')
