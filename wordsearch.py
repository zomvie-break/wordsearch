#!/home/victor/python_projects/wordsearch/venv/bin/python3
import numpy as np                      #numpy
import copy                             #for deep copy
from string import ascii_lowercase      #for getting random ascii characters to fill the wordsearch

# reportlab imports for working with PDFs
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Frame
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

class Wordsearch:
    def __init__(self, dimension_x, dimension_y):
        # sets a basic list of lists given some dirmensions
        self.dimension_x=dimension_x 
        self.dimension_y=dimension_y
        self.wordsearch=self.create_empty_wordsearch()
        self.def_value = self.wordsearch[0][0].value
    
    def create_empty_wordsearch(self):
        # generates an empty wordsearch given some dimensions
        #  x * y (ys are rows and xs are columns)
        ys = self.dimension_y
        xs = self.dimension_x
        wordsearch = []
        for y in range(ys):
            # for loop to fill in the wordsearch with empty tiles.
            temp = []
            for x in range(xs):
                temp.append(Tile())
            wordsearch.append(temp)
        return wordsearch
        
    def print_wordsearch(self):
        """
        prints the wordsearch to the terminal in an understandable way
        """
        for y in range(len(self.wordsearch)):
            for tile in self.wordsearch[y]:
                print(tile.value, end="  ")
            print()
        print()

    def place_word_h(self, word, loc_x, loc_y, backwards=False):
        """Place a word in the wordsearch, horizontaly"""
        len_word=len(word)
        # check if the word fits in the selected location
        if loc_x+len_word>self.dimension_x:
            print('word is too big!')
            return False
        else:
            # dummy wordsearch to which we make changes before commiting to the real one
            # deepcopy because otherwise we copy the reference, and we dont want that
            fake_wordsearch = copy.deepcopy(self.wordsearch)
            # inverts the word
            if backwards:
                word=word[::-1]
            
            # variable to keep track of the location in the wordsearch 
            temp_loc_x=0
            for char in word:
                if fake_wordsearch[loc_y][loc_x+temp_loc_x].value == self.def_value or fake_wordsearch[loc_y][loc_x+temp_loc_x].value == char:
                    fake_wordsearch[loc_y][loc_x+temp_loc_x].value = char.upper()
                    temp_loc_x += 1
                else:
                    return False
            # if the assignation of characters is complete,
            # point the self.wordsearch to the fake_wordsearch
            self.wordsearch = fake_wordsearch
            return True

    def place_word_v(self, word, loc_x, loc_y, backwards=False):
        """Place a word in the wordsearch, horizontaly"""
        len_word=len(word)
        if loc_y+len_word>self.dimension_y:
            print('word is too big!')
            return False
        else:
            fake_wordsearch = copy.deepcopy(self.wordsearch)
            if backwards:
                word=word[::-1]
            temp_loc_y=0
            for char in word:
                # tile = self.wordsearch[loc_y][loc_x+temp_loc_x]
                # print(f'tile: {tile}\tdefvalue: {self.def_value}')
                if fake_wordsearch[loc_y+temp_loc_y][loc_x].value == self.def_value or  fake_wordsearch[loc_y+temp_loc_y][loc_x].value == char:
                    fake_wordsearch[loc_y+temp_loc_y][loc_x].value = char.upper()
                    temp_loc_y += 1
                else:
                    return False
            self.wordsearch=fake_wordsearch
            return True
    
    def place_word_d1(self, word, loc_x, loc_y, backwards=False):
        """Place a word in the wordsearch diagonally, from left to right"""
        len_word=len(word)
        print(f'loy_y + len_word > dimensions y: {loc_y + len_word > self.dimension_y}')
        print(f'loc_x + len_word > self.dimension_x: {loc_x + len_word > self.dimension_x}')
        print(f'locx: {loc_x}\tloc_y: {loc_y}\tlen_word: {len_word}\tdim_x: {self.dimension_x}\tdim_y: {self.dimension_y}')
        if loc_y + len_word > self.dimension_y or loc_x + len_word > self.dimension_x:
            print('word is too big')
            return False
        else:
            fake_wordsearch = copy.deepcopy(self.wordsearch)
            if backwards:
                word = word[::-1]
            temp_loc_y = 0
            temp_loc_x = 0
            print(f'adding word {word}')
            for char in word:
                if fake_wordsearch[loc_y+temp_loc_y][loc_x+temp_loc_x].value == self.def_value or fake_wordsearch[loc_y+temp_loc_y][loc_x+temp_loc_x].value == char:
                    fake_wordsearch[loc_y+temp_loc_y][loc_x+temp_loc_x].value = char.upper()
                    temp_loc_x += 1
                    temp_loc_y += 1
                    print(f'adding char {char}')
                else:
                    print(f'failed to add char {char}')
                    return False
            self.wordsearch = fake_wordsearch
            self.print_wordsearch()
            return True
    
    def place_word_d2(self, word, loc_x, loc_y, backwards=False):
        """Place a word in the wordsearch diagonally, from right to left"""
        len_word=len(word)
        print(f'loy_y + len_word > dimensions y: {loc_y + len_word > self.dimension_y}')
        print(f'loc_x + len_word > self.dimension_x: {loc_x + len_word > self.dimension_x}')
        print(f'locx: {loc_x}\tloc_y: {loc_y}\tlen_word: {len_word}\tdim_x: {self.dimension_x}\tdim_y: {self.dimension_y}')
        if loc_y + len_word > self.dimension_y or loc_x + len_word > self.dimension_x:
            print('word is too big')
            return False
        else:
            fake_wordsearch = copy.deepcopy(self.wordsearch)
            if backwards:
                word = word[::-1]
            temp_loc_y = 0
            temp_loc_x = loc_x + len_word-1
            print(f'adding word {word}')
            for char in word:
                # try:
                if fake_wordsearch[loc_y + temp_loc_y][temp_loc_x].value == self.def_value or fake_wordsearch[loc_y+temp_loc_y][temp_loc_x].value == char:
                    fake_wordsearch[loc_y+temp_loc_y][temp_loc_x].value = char.upper()
                    temp_loc_x -= 1
                    temp_loc_y += 1
                    print(f'adding char {char}')
                else:
                    print(f'failed to add char {char}')
                    return False
                # except:
                #     print(f'unable to add word: {word}')
                #     self.print_wordsearch()
            self.wordsearch = fake_wordsearch
            self.print_wordsearch()
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
        for i in range(len(self.wordsearch)):
            for j in range(len(self.wordsearch[i])):
                if self.wordsearch[i][j].value == self.def_value:
                    self.wordsearch[i][j].value = np.random.choice([x.upper() for x in ascii_lowercase])

    def addWords(self, txt_file, difficulty = 1):
        with open(txt_file) as f:
             lines = f.readlines()

        lines = [line.strip() for line in lines]
        # depending on the file, it will try to extract the first word befor the '-' char 
        words = [re.findall(r'(.*?) - \(.*\)', line) for line in lines]
        if len(words[0]) == 0:
            words = lines
        print(len(words))
        if type(words[0]) is list:
            words = [x[0] for x in words ]

        # Here is the actual filling of the wordsearch.
        max_attempts = 1000
        failed_words = []
        for word in words:
            for i in range(max_attempts):
                # flag is used to check if the word was succesfully placed in the wordsearch
                flag = False
                # difficulty of 1, i.e. easy.
                if difficulty == 1:
                    direction = np.random.randint(2)
                    loc_x, loc_y = self.get_random_loc()
                    if direction == 0:
                        # horizontal 
                        flag=self.place_word_h(word, loc_x, loc_y)
                    if direction == 1:
                        # vertical
                        flag = self.place_word_v(word, loc_x, loc_y)
                    if flag:
                        self.print_wordsearch()
                        break
            
                # difficulty of 2, i.e. medium
                if difficulty == 2:
                    direction = np.random.randint(3)
                    loc_x, loc_y = self.get_random_loc()
                    if direction == 0:
                        # horizontal 
                        flag=self.place_word_h(word, loc_x, loc_y)
                    if direction == 1:
                        # vertical
                        flag = self.place_word_v(word, loc_x, loc_y)
                    if direction == 2:
                        # diagonal 1
                        flag = self.place_word_d1(word, loc_x, loc_y)
                    if flag:
                        self.print_wordsearch()
                        break

                # difficulty of 3, i.e. hard
                if difficulty == 3:
                    direction = np.random.randint(4)
                    loc_x, loc_y = self.get_random_loc()
                    if direction == 0:
                        # horizontal 
                        flag=self.place_word_h(word, loc_x, loc_y)
                    if direction == 1:
                        # vertical
                        flag = self.place_word_v(word, loc_x, loc_y)
                    if direction == 2:
                        # diagonal 1
                        flag = self.place_word_d1(word, loc_x, loc_y)
                    if direction == 3:
                        # diagonal 2
                        flag = self.place_word_d2(word, loc_x, loc_y)
                    if flag:
                        self.print_wordsearch()
                        break

                # difficulty of 4, i.e. very hard
                if difficulty == 4:
                    direction = np.random.randint(4)
                    loc_x, loc_y = self.get_random_loc()
                    backwards = np.random.choice([True, False])
                    if direction == 0:
                        # horizontal 
                        flag=self.place_word_h(word, loc_x, loc_y, backwards=backwards)
                    if direction == 1:
                        # vertical
                        flag = self.place_word_v(word, loc_x, loc_y, backwards=backwards)
                    if direction == 2:
                        # diagonal 1
                        flag = self.place_word_d1(word, loc_x, loc_y, backwards=backwards)
                    if direction == 3:
                        # diagonal 2
                        flag = self.place_word_d2(word, loc_x, loc_y, backwards=backwards)
                    if flag:
                        self.print_wordsearch()
                        break
                


                if i== max_attempts-1:
                            print(f'failed to add word: {word}')
                            failed_words.append(word)
        print(f'words attepted: {len(words)}\twords failed: {len(failed_words)}')
        print(failed_words)
        self.fill_empty_places()
        self.print_wordsearch()

class PDFHelper:
    def __init__(self):
        pass

    def get_word_box(self, txt_file):
        """
        returns a reportlab flowable element which contain all the words in the txt file
        """
        with open(txt_file, 'r') as f:
            txt = f.readlines()
        txt = ' '.join(txt).replace('\n','<br />')
        # print(txt)
        flow_element = Paragraph(txt)
        return flow_element
    
    def txt2table(self, txt_file):
        # open the text file.
        with open(txt_file, 'r') as f:
            txt = f.readlines()
        # desired number of rows
        drows = 4
        # get the number of words
        num = len(txt)
        # get the number of cells necessary for the table
        if num%drows==0:
            pass
        else:
            num = (num//drows+1)*drows
        # make a list of list of dimensiosn of 2 x N
        temp = []
        lst_of_lsts = []
        for i in range(num+1):
            # if i > len(txt):
            #     temp.append('')
            if i %drows == 0 and i!=0:
                lst_of_lsts.append(temp)
                temp = []
            try:
                temp.append(txt[i].strip())
            except IndexError:
                temp.append('')


        print(lst_of_lsts)
        table = Table(
                        # [[Paragraph(col) for col in df.columns]] + df.values.tolist(), 
                        lst_of_lsts,
                        style=[
                            # ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                            # ('LINEBELOW',(0,0), (-1,0), 1, colors.black),
                            # ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                            ('BOX', (0,0), (-1,-1), 1, colors.grey),
                            ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.lightgrey, colors.white])])
                        # hAlign = 'LEFT')
        return table

    def create_wordsearch(self, wordsearch, txt_file, filename='word_search.pdf', title = ''):
        """
        Takes a wordsearch (an instance of the wordsearch class) and a file name (word_search.pdf as default)
        """
        # initialize the SimpleDocTemplate with som standard values
        doc = SimpleDocTemplate(filename,
                            paper_size=letter,
                            bottomMargin=0.4*inch,
                            topMargin=0.4*inch,
                            rightMargin=0.4*inch,
                            leftMargin=0.4*inch)
        # array used to store the values of the tiles of the wordsearch 
        temp=[]
        # array used to store the arrays to be used as rows in the table
        tab=[]
        for row in range(len(wordsearch.wordsearch)):
            for col in range(len(wordsearch.wordsearch[row])):
                temp.append(wordsearch.wordsearch[row][col].value)
            tab.append(temp)
            temp=[] 

        # style templates from reportlab
        styles = getSampleStyleSheet()
        titleStyle = ParagraphStyle('title_ws',
                           fontName="Helvetica-Bold",
                           fontSize=20,
                           parent=styles['Heading1'],
                           alignment=1,
                           spaceAfter=20)
        # styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        t0 = Paragraph(title, titleStyle)
        
        # print(f'col={wordsearch.dimension_x}\trow={wordsearch.dimension_y}\ttype={type(wordsearch.dimension_x)}')

        # the colWidths and rowHeights are difined as the space beteween cells, and take an array such as [0.2*inch, 0.2*inch ...]
        t1 = Table(tab, colWidths=[0.3*inch]*wordsearch.dimension_x, rowHeights=[0.3*inch]*wordsearch.dimension_y) # dimensions required
        t1.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 2, colors.black), 
                                ('FONT', (0,0),(-1,-1),'Helvetica', 12),
                                ('ALIGN', (0, 0), (-1, -1), "CENTER")]))

        word_box = self.txt2table(txt_file)

        # list to save the elements to be attached in the PDF
        elements = []
        elements.append(t0)
        elements.append(t1)
        # frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height, id='col1')
        # frame2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6, doc.height, id='col2',showBoundary=1)
        # f = Frame(inch, inch, 6*inch, 9*inch, showBoundary=1)
        # frame1.addFromList(elements,doc)
        elements.append(word_box)
        doc.build(elements)


if __name__ == "__main__":
    # set dimensions of the wordsearch (max reasonable dimensions 22, 32 for a whole page)
    cw = Wordsearch(22, 30)
    # print('empty wordsearch')
    cw.print_wordsearch()
    # txt_file = '/home/victor/python_projects/wordsearch/word_list_translations.txt'
    txt_file = '/home/victor/python_projects/wordsearch/word_list_places.txt'

    cw.addWords( txt_file, difficulty=4)
    difficulty = 1

    pdf_helper = PDFHelper()
    pdf_helper.create_wordsearch(cw, txt_file, title='WordSearch' )

    for i in range(15):
        cw = Wordsearch(18, 25)
        cw.addWords( txt_file, difficulty=difficulty)

        pdf_helper.create_wordsearch(cw, txt_file, title='WordSearch', filename=f'word_search_{str(difficulty)}_{i:02}.pdf' )

    
