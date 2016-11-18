"""
    Info UA
                                                'Djangonize It!'
        Однофайлова утиліта для спрощення процесів роботи із зображеннями для Django розробників. Для використання
    потрібно розмістити файл програми в папку із зображеннями (images) static папки django-проекту. Дане рішення
    одночасно служить підтримкою для рекомендованої структури папок в django-проектах та дозволяє програмі
    та корисувачу уникнути додаткових дій по налаштуванню місця збереження зображень. Також варто мати
    встановлене розширення PyQt4 (якщо встановлена інша версія PyQt, можна спробувати замінити значення в import).
        Дана програма призначена для виконання наступних операцій:
        1. Пошук і заміна посилань зображень в фронтенд-файлах (CSS,HTML) на django-посинання. Пошук здійснюється
           на основі регулярних виразів. В програмі присутні базові регулярні вирази для CSS і HTML, які є
           доступними для редагування користувачем (проте, при редагуванін регулярного виразу для HTML варто 
           знати, що він реалізований за допомогою груп, 1-ша група - замінює текст до назви файлу, 2-га - після). 
           При здійсненні заміни, файл не замінюється, а створюється його копія (у папці із оригіналом) 
           на випадок неточного регулярного виразу. Ім'я копії формується як "[0-9]старе ім'я", що дозволяє 
           простіше знаходити його у папці (він буде зверху, або знизу). Крім того, реалізовано можливість 
           відкриття папки із редагованими файлами напряму із програми, відразу після пошуку.
        2. Завантаження зображення із інтернету за посиланням (у папку images) та надання користувачу валідного
           django-посилання для його проекту. Всі згенеровані посилання архівуються ("db.txt" в папці
           розміщення програми). Також реалізовано класс, для зручної роботи із даним архівом із самої програми,
           який підтримує сортування по імені/django-посиланні/даті. Пошук по архіву можна здійснювати як
           за допомогою звичайних записів, так і регулярних виразів.
        Програма написана в об'єкто-орієнтованому стилі. Кожен клас реалізований графічно через розширення PyQt4
    (в програмі використано як і абсолютне позіционування елементів так і позиціонування через layout-и).
        Структура наслідування є наступною:

     PyQT Parent |          QtGui.QWidget                 QtGui.QSortFilterProxyModel
     Parent      |           DjangoImages                     SortFilterHistory (використовується як екземпляр History)
     1st Child   |   DjangoFiles      History (не наслідує конструктор)
     2nd Child   |    MainMenu

        Програма розроблена і протестована в середовищі Windows, але повинна працювати в Unix-based (не перевірено).
    Також реалізовано валідатори для запобігання найчастіщих помилок і допомоги користувачам які не читають info в
    файлі. Усі налаштування за замовчуванням винесені в Parent клас (DjangoImages).
"""
"""
    Info EN
                                    'Djangonize It!' (A single-file application)
        The purpose of this application is to simplify work with images for Django developers.
        For successful using, you should to install the app into "images" folder inside "static" folder of your
    django project (../static/../images/). This solution simultaneously supporting the recommended file
    structure of django projects and allows to avoid additional user and program activities related with path setting
    for image download. The installed PyQt4 is, also, needed.
        The application allows to perform the next operations:
        1. Search and replacement image links on django-links at frontend (HTML, CSS) files. Search is RegEx driven.
           The application have default regular expressions for CSS and HTML files, which can be changed by user. HTML
           RegEx is realized through two groups (1st group - replace text before filename, 2nd - after).
           When you run the djangonization process for the file, it isn't replaced. The app creates a copy of file
           at folder with original. Copy's name is forming as a "[0-9]old name", which allow to simplify it searching at
           folder (it was at the top or bottom). Also, created file can be opened from the program by os explorer.
        2. Download images from Internet by link (in images folder) and return valid link for user's django project.
           All results of operation are archiving (in "db.txt" at folder with program). Also, the class to simplify
           work with logs is realized. It supports sorting by name/django link/date. Also, searching can be performed
           by normal and RegEx strings.
        The application is created with object-oriented style. Every class is realized graphically by PyQt4 extension
    (both absolute and layout positioning are used).
        The inheritance structure is the following:

     PyQT Parent |          QtGui.QWidget                  QtGui.QSortFilterProxyModel
     Parent      |           DjangoImages                       SortFilterHistory (used as an example for the History)
     1st Child   |   DjangoFiles      History (closed __init__)
     2nd Child   |    MainMenu

        The program is developed and testing in Windows environment, but it should work at Unix-based systems
    (isn't checked). Also validators for most frequently errors and user helping are realised.
        All default settings are placed at the Parent class (DjangoImages).

"""

import os
import sys
import re
from urllib.request import URLopener
from datetime import datetime
from random import randint
from PyQt4 import QtGui, QtCore


class DjangoImages(QtGui.QWidget):
    ''' Parent class of application (contains elements constructors and default variables for other classes).
    Download images from Web, return django-links, log the result.

    '''
    NOW = datetime.now()                # Constant for logs
    PATH = os.getcwd()                  # Constant for link generation and file management
    FILE = "djangonizeit.pyw"           # Constant for internal restart (should be modified with app filename)
    size = 450, 340                     # Default size of application windows (width, height)
    position = 450, 150                 # Default position of application windows (horizontal,vertical)
    bFontSize = 10                      # Default font size for buttons
    bStyle = "color: rgb(0, 85, 255);"  # Default stylesheet for buttons
    lFontSize = 10                      # Default font size for labels
    lStyle = "color: rgb(0, 85, 255);"  # Default stylesheet for labels
    database = "db.txt"                 # Default name of database (for logs)
    defaultCSS = r'\.\..*/images/'      # Default pattern for re.sub function (DjangoFiles().djangonize())(lns 453/459)
    defaultHTML = r'src=\"(.*images/)(.*\.[a-z]{3})\"'  # Default pattern for re.sub function (lines 470/476)

    def __init__(self):
        super(DjangoImages, self).__init__()
        # Buttons
        self.djangonizeButton = self.create_button("Djangonize It!", self.djangonize,
                                            tooltip="Download image,return django link, log the result")
        self.quitButton = self.create_button('Quit', self.quit_app(), tooltip="Close All Windows")
        self.openButton = self.create_button('History', self.open_next(), tooltip="Open window with logs")

        # Lines
        self.linkText = self.create_text_edit()
        self.nameLine = self.create_line_edit()
        self.djangoLine = self.create_line_edit()

    def __call__(self):
        # Give the ability to be opened outside. Contains information about positioning of elements on windows
        linkLayout = QtGui.QGridLayout()
        linkLayout.addWidget(self.linkText, 0, 0)
        nameLayout = QtGui.QGridLayout()
        nameLayout.addWidget(self.nameLine, 1, 0)

        buttonsLayout = QtGui.QGridLayout()
        buttonsLayout.addWidget(self.djangonizeButton, 0, 3)
        buttonsLayout.addWidget(self.quitButton, 2, 5)
        buttonsLayout.addWidget(self.openButton, 2, 0)
        buttonsLayout.addWidget(self.djangoLine, 1, 3)

        linkGroupBox = QtGui.QGroupBox("URL:")
        linkGroupBox.setLayout(linkLayout)
        nameGroupBox = QtGui.QGroupBox("Filename:")
        nameGroupBox.setLayout(nameLayout)
        buttonsGroupBox = QtGui.QGroupBox("Djangonizetion and Control:")
        buttonsGroupBox.setLayout(buttonsLayout)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(linkGroupBox)
        mainLayout.addWidget(nameGroupBox)
        mainLayout.addWidget(buttonsGroupBox)

        self.setLayout(mainLayout)

        self.setWindowTitle("Djangonize image from Web")
        self.resize(*self.size)
        self.move(*self.position)
        self.show()

    # Element constructors
    def create_button(self, text, activity, tooltip=None, fontsize=int(bFontSize), style=bStyle):
        button = QtGui.QPushButton(text, self)
        button.clicked.connect(activity)
        button.setToolTip(tooltip)
        font = QtGui.QFont()
        font.setPointSize(fontsize)
        font.setBold(True)
        font.setWeight(75)
        button.setFont(font)
        button.setStyleSheet(style)
        return button

    def create_label(self, text, fontsize=int(lFontSize), style=str(lStyle)):
        label = QtGui.QLabel(text, self)
        font = QtGui.QFont()
        font.setPointSize(fontsize)
        font.setBold(True)
        font.setWeight(75)
        label.setFont(font)
        label.setStyleSheet(style)
        return label

    def create_text_edit(self):
        textEdit = QtGui.QTextEdit()
        return textEdit

    def create_line_edit(self):
        lineEdit = QtGui.QLineEdit()
        return lineEdit

    def dir_list(self):
        # Method which returns list of folders before static folder (in django structure). Optimized for Linux
        if os.name == 'nt':
            pathList = re.findall(r'static\\(.+).*$', self.PATH) # path is saved as a list with one element
            try:
                dirList = pathList[0].split('\\')
            except IndexError:  # Error when list is empty (for cases when the application isn't installed)
                QtGui.QMessageBox.warning(self, "InstallError",
                                          "Please, move the program inside your django project "
                                          "(..\static\..\images)to solve the Error!")
                raise
            return dirList
        else:
            pathList = re.findall(r'static/(.+).*$', self.PATH)
            try:
                dirList = pathList[0].split('/')
            except IndexError:
                QtGui.QMessageBox.warning(self, "InstallError",
                                          "Please, move the program inside your django project "
                                          "(..\static\..\images)to solve the Error!")
                raise
            return dirList

    def djangonize(self):
        # Download image and return its django-link (Overridable)
        url = str(self.linkText.toPlainText())
        if re.search(r'\.[a-z]{3}$', url):
            filename = str(self.nameLine.displayText())

            if len(filename) == 0:        # If the filename line is empty save the image with its basename
                newFilename = os.path.basename(url)
            else:                         # Else, save it with entered name
                newFilename = filename + os.path.basename(url)[-4:]

            dirList = self.dir_list()

            # If with dir_list() all is ok, download image to django directory
            # If statement don't used here, because any Exception in dir_list() stop execution of the method
            URLopener().retrieve(str(url), newFilename)

            # Return the link to user interface
            djangoView = "{% static '" + '/'.join(dirList) + '/' + newFilename + " '%}"
            self.djangoLine.setText(djangoView)

            # Log the result
            with open(self.database, "a") as f:
                historyNote = ','.join([newFilename, djangoView, str(self.NOW.year), str(self.NOW.month),
                                       str(self.NOW.day), str(self.NOW.hour), str(self.NOW.minute)])+'\n'
                f.write(historyNote)
        else:
            QtGui.QMessageBox.warning(self, "Link", "You enter a wrong link!")

    def open_next(self):
        # Overridable method for transitions
        return History()

    def quit_app(self):
        # Overridable method
        return QtCore.QCoreApplication.instance().quit


class History(DjangoImages):
    ''' Class for comfortable work with logs. Ih inherits methods only because design of this class is so different.
    Sort and filter djangonized images (RegEx supports). All info in table can be copied.

    '''
    def __init__(self):
        super(DjangoImages, self).__init__()            # Closed from parent constructor attributes
        self.proxyModel = SortFilterHistory(self)            # Technical class (PyQt template)
        self.proxyModel.setDynamicSortFilter(True)

        # Buttons
        self.openButton = self.create_button('Folder', self.open_folder, tooltip="Open folder with djangonized images")
        self.quitButton = self.create_button('Quit', self.quit_app(), tooltip="Close All Windows")
        self.emptyLabel = QtGui.QLabel()                # Filler for GridLayout with buttons

        self.filterPatternLineEdit =self.create_line_edit()          # Search line
        self.filterPatternLabel = QtGui.QLabel("Filter pattern:")
        self.filterPatternLabel.setBuddy(self.filterPatternLineEdit)

        self.filterSyntaxComboBox = QtGui.QComboBox()                            # Search modes
        self.filterSyntaxComboBox.addItem("Normal", QtCore.QRegExp.FixedString)  # 1st (Default)
        self.filterSyntaxComboBox.addItem("RegEx", QtCore.QRegExp.RegExp)  # 2nd (Switch with Normal to make it default)
        self.filterSyntaxComboBox.setToolTip("Search mode")

        self.fromDateEdit = QtGui.QDateEdit()
        self.fromDateEdit.setDate(QtCore.QDate(2016, 1, 1))
        self.fromDateEdit.setCalendarPopup(True)                   # True calendar
        self.fromLabel = QtGui.QLabel("From:")
        self.fromLabel.setBuddy(self.fromDateEdit)

        self.toDateEdit = QtGui.QDateEdit()
        self.toDateEdit.setDate(QtCore.QDate(2026, 1, 1))
        self.toDateEdit.setCalendarPopup(True)
        self.toLabel = QtGui.QLabel("To:")
        self.toLabel.setBuddy(self.toDateEdit)

        self.filterPatternLineEdit.textChanged.connect(self.text_filter_changed)
        self.filterSyntaxComboBox.currentIndexChanged.connect(self.text_filter_changed)
        self.fromDateEdit.dateChanged.connect(self.date_filter_changed)
        self.toDateEdit.dateChanged.connect(self.date_filter_changed)

    def __call__(self):
        self.proxyView = QtGui.QTreeView()                             # Table view
        self.proxyView.setRootIsDecorated(False)
        self.proxyView.setAlternatingRowColors(True)
        self.proxyView.setModel(self.proxyModel)                       # Setting of table for the view
        self.proxyView.setSortingEnabled(True)
        self.proxyView.sortByColumn(1, QtCore.Qt.AscendingOrder)
        self.proxyModel.setSourceModel(self.create_log_table())        # Setting of table for the window

        self.proxyView.setColumnWidth(0, 75)
        self.proxyView.setColumnWidth(1, 240)

        self.text_filter_changed()
        self.date_filter_changed()

        proxyLayout = QtGui.QGridLayout()
        proxyLayout.addWidget(self.proxyView, 0, 0, 1, 3)
        proxyLayout.addWidget(self.filterPatternLabel, 1, 0)
        proxyLayout.addWidget(self.filterPatternLineEdit, 1, 1)
        proxyLayout.addWidget(self.filterSyntaxComboBox, 1, 2)
        proxyLayout.addWidget(self.fromLabel, 3, 0)
        proxyLayout.addWidget(self.fromDateEdit, 3, 1, 1, 2)
        proxyLayout.addWidget(self.toLabel, 4, 0)
        proxyLayout.addWidget(self.toDateEdit, 4, 1, 1, 2)
        proxyGroupBox = QtGui.QGroupBox("Sort/Filter Links")
        proxyGroupBox.setLayout(proxyLayout)

        buttonsLayout = QtGui.QHBoxLayout()
        buttonsLayout.addWidget(self.openButton, 1)
        buttonsLayout.addWidget(self.emptyLabel, 3)
        buttonsLayout.addWidget(self.quitButton, 1)
        buttonsGroupBox = QtGui.QGroupBox("Control buttons")
        buttonsGroupBox.setLayout(buttonsLayout)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(proxyGroupBox)
        mainLayout.addWidget(buttonsGroupBox)

        self.setLayout(mainLayout)
        self.setWindowTitle("History of djangonized images")
        self.resize(*self.size)
        self.move(*self.position)
        self.show()

    def text_filter_changed(self):
        # Filtering by filter patterns (Normal, RegEx)
        syntax = QtCore.QRegExp.PatternSyntax(
            self.filterSyntaxComboBox.itemData(
                self.filterSyntaxComboBox.currentIndex()))

        regExp = QtCore.QRegExp(self.filterPatternLineEdit.text(), True, syntax)
        self.proxyModel.setFilterRegExp(regExp)

    def date_filter_changed(self):
        # Filtering by dates
        self.proxyModel.set_filter_minimum_date(self.fromDateEdit.date())
        self.proxyModel.set_filter_maximum_date(self.toDateEdit.date())

    def add_log(self,table, name, link, date):
        # Fill row of the table
        table.insertRow(0)
        table.setData(table.index(0, 0), name)
        table.setData(table.index(0, 1), link)
        table.setData(table.index(0, 2), date)

    def create_log_table(self):
        # Create table and fill it by log data
        table = QtGui.QStandardItemModel(0, 3, self)

        table.setHeaderData(0, QtCore.Qt.Horizontal, "Name")
        table.setHeaderData(1, QtCore.Qt.Horizontal, "Djangonized link")
        table.setHeaderData(2, QtCore.Qt.Horizontal, "Date")

        # Fill the table
        with open(self.database) as f:
            lines = f.readlines()
            for line in lines:
                    line = line.split(',')
                    self.add_log(table, line[0], line[1],           #name,link
                                 QtCore.QDateTime(QtCore.QDate(int(line[2]), int(line[3]), int(line[4])),  # Date
                                                               QtCore.QTime(int(line[5]), int(line[6]))))  # Time
        return table

    def open_folder(self):
        # Open folder with djangonized images
        return os.system(QtGui.QFileDialog().getOpenFileName(self,'Open Dj-folder', self.PATH))


class DjangoFiles(DjangoImages):
    ''' Class simplify work with website templates for django programmers.
    Djangonize links in CSS and HTML files, save copy of djangonized files in format [0-9]oldname, return name to user.

    '''
    def __init__(self):
        super(DjangoFiles, self).__init__()
        # Buttons (djangonizeButton, openButton and quitButton are inherited)
        self.djangonizeButton.setToolTip("Make a copy where pattern is replaced by django links, return name of copy")
        self.browseButton = self.create_button("Browse...", self.browse)
        self.openButton.setText('Open It!')
        self.openButton.setToolTip("Open djangonized file by default program")

        # Lines
        self.regexLine = self.create_line_edit()
        self.regexLine.setText("Choose CSS or HTML file!")
        self.djangonizeLine = self.create_line_edit()                    # Line for djangonized filename returning
        self.fileComboBox = self.create_combo_box(QtCore.QDir.currentPath())

    def __call__(self):
        fileLayout = QtGui.QHBoxLayout()
        fileLayout.addWidget(self.fileComboBox,4)
        fileLayout.addWidget(self.browseButton,1)
        fileGroupBox = QtGui.QGroupBox("Browse file:")
        fileGroupBox.setLayout(fileLayout)

        regexLayout = QtGui.QVBoxLayout()
        regexLayout.addWidget(self.regexLine)
        regexGroupBox = QtGui.QGroupBox("Pattern for replacement:")
        regexGroupBox.setLayout(regexLayout)

        buttonsLayout = QtGui.QGridLayout()
        buttonsLayout.addWidget(self.djangonizeButton, 0, 2, 1, 3)
        buttonsLayout.addWidget(self.djangonizeLine, 1, 2, 1, 3)
        buttonsLayout.addWidget(self.openButton, 2, 0)
        buttonsLayout.addWidget(self.quitButton, 2, 5)
        buttonsGroupBox = QtGui.QGroupBox("Djangonization and Control buttons:")
        buttonsGroupBox.setLayout(buttonsLayout)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(fileGroupBox)
        mainLayout.addWidget(regexGroupBox)
        mainLayout.addWidget(buttonsGroupBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Djangonize CSS or HTML file")
        self.resize(*self.size)
        self.move(*self.position)
        self.show()

    def create_combo_box(self, text=""):
        # Additional element constructor
        comboBox = QtGui.QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        return comboBox

    def browse(self):
        # Browse file and choose a default RegEx according to file extension
        openedFile = QtGui.QFileDialog.getOpenFileName(self, "Find CSS or HTML", QtCore.QDir.currentPath())

        if openedFile:
            if self.fileComboBox.findText(openedFile) == -1:
                self.fileComboBox.addItem(openedFile)

            self.fileComboBox.setCurrentIndex(self.fileComboBox.findText(openedFile))

        filePath = str(self.fileComboBox.currentText())

        if filePath[-3:] == "css":
            self.regexLine.setText(self.defaultCSS)
        elif filePath[-3:] == "tml":
            self.regexLine.setText(self.defaultHTML)
        else:
            self.regexLine.setText("Wrong file. Choose CSS or HTML!")

    def djangonize(self):
        # Method which make files more djangonized! (Overridden method for djangonizeButton)
        filePath = str(self.fileComboBox.currentText()) # Path to file from fileComboBox
        dirList = self.dir_list()         # DjangonizeImage inherited method which returns folders before static folder
        newFilename = str(randint(0, 9)) + os.path.basename(filePath) # Filename where changes will be saved

        if filePath[-3:] == "css":
            djPath = '../' + '/'.join(dirList) + '/'  # Path to images in django project
            nonDjPath = str(self.regexLine.displayText())  # Path to images in CSS for replacement

            if os.name == 'nt':
                with open(os.path.dirname(filePath) + '/' + newFilename, 'w') as f:    # open new
                    content = open(filePath).read()                                    # copy data from old
                    f.write('{% load staticfiles %}\n')                                # connect static files to CSS
                    f.write(re.sub(nonDjPath, djPath, content))                        # replace line and write in new
                    self.djangonizeLine.setText("New filename: " + newFilename)        # return name of new

            else:
                with open(os.path.dirname(filePath) + '\\' + newFilename, 'w') as f:
                    content = open(filePath).read()
                    f.write('{% load staticfiles %}\n')
                    f.write(re.sub(nonDjPath, djPath, content))
                    self.djangonizeLine.setText("New filename: " + newFilename)

        elif filePath[-3:] == "tml":

            djPath = "src=\"{% static '" + '/'.join(dirList) + '/' + "\g<2>" + "' %}\"" # Path to django-project images
            nonDjPath = str(self.regexLine.displayText())  # Path in CSS or HTML for replace

            if os.name == 'nt':
                with open(os.path.dirname(filePath) + '/' + newFilename, 'w') as f:   # Create a new file [0-9]oldname
                    content = open(filePath).read()                              # Open old file and read it content
                    f.write(re.sub(nonDjPath, djPath, content))                  # Replacement is here
                    self.djangonizeLine.setText("New filename: " + newFilename)     # Info for user

            else:
                with open(os.path.dirname(filePath) + '\\' + newFilename, 'w') as f:
                    content = open(filePath).read()
                    f.write(re.sub(nonDjPath, djPath, content))
                    self.djangonizeLine.setText("New filename: " + newFilename)
        else:
            self.djangonizeLine.setText("Wrong file. Choose CSS or HTML!")   # When not CSS or not HTML file is browsed

    def open_file(self):
        # This method open the folder with djangonized files in os explorer and allow choose file for opening
        # It should be opened as object not as function
        if re.match(r'New\sfilename', self.djangonizeLine.displayText()):
            os.system(QtGui.QFileDialog().getOpenFileName(self, 'Open Dj-file', self.fileComboBox.currentText()))
        else:
            QtGui.QMessageBox.warning(self,'OpenError', 'Djangonize file before opening')

    def open_next(self):
        # Overridden method for openButton
        return self.open_file


class MainMenu(DjangoFiles):
    """ Start window of the application
    Call the components of the application when buttons is clicking.

    """
    def __init__(self):
        super(MainMenu, self).__init__()
        # Buttons (djangonizeButton, openButton, browseButton and quitButton are inherited)
        self.djangonizeButton.setText('Djangonize image from Web')
        self.djangonizeButton.clicked.connect(self.djangonize())
        self.djangonizeButton.setToolTip(None)

        self.openButton.setText('History of djangonized images')
        self.openButton.setToolTip(None)

        self.browseButton.setText('Djangonize CSS or HTML file')
        self.browseButton.clicked.connect(self.browse())

        self.restartButton = self.create_button('R', self.restart,
                            tooltip="Temporary solution for issue with repainting of GroupBoxes")


        # Label
        self.mainLabel = self.create_label("Main menu", 16)

        # Location of components (Absolute). Here the problem with window resizing is solved.
        self.mainLabel.setGeometry(QtCore.QRect(self.size[0]*0.43, self.size[1]*0.03,  # Location (horizontal,vertical)
                                                self.size[0]*0.3, self.size[1]*0.15))  # Size of element (width, height)
        self.djangonizeButton.setGeometry(QtCore.QRect(self.size[0]*0.1, self.size[1]*0.20,
                                                           self.size[0]*0.48, self.size[1]*0.17))
        self.openButton.setGeometry(QtCore.QRect(self.size[0] * 0.1, self.size[1] * 0.4,
                                                 self.size[0] * 0.48, self.size[1] * 0.17))
        self.browseButton.setGeometry(QtCore.QRect(self.size[0]*0.1, self.size[1]*0.6,
                                                    self.size[0]*0.48, self.size[1]*0.17))
        self.quitButton.setGeometry(QtCore.QRect(self.size[0]*0.75, self.size[1]*0.85,
                                                 self.size[0]*0.2, self.size[1]*0.1))
        self.restartButton.setGeometry(QtCore.QRect(self.size[0]*0.01, self.size[1]*0.01,
                                                 self.size[0]*0.05, self.size[1]*0.05))

        self.setWindowTitle('DjangonizeIt! - Main menu')
        self.resize(*self.size)
        self.move(*self.position)

    # Overridden methods
    def djangonize(self):
        return DjangoImages()

    def browse(self):
        return DjangoFiles()

    def open_next(self):
        return History()

    def restart(self):
        # start new, sleep old
        return os.system(self.FILE)

class SortFilterHistory(QtGui.QSortFilterProxyModel):
    ''' Technical class for the History class. (is taken from pyQt templates)
    Example of the class is used for representing (filtering) of table content by date range.

    '''
    def __init__(self, parent=None):
        super(SortFilterHistory, self).__init__(parent)

        self.minDate = QtCore.QDate()
        self.maxDate = QtCore.QDate()

    def set_filter_minimum_date(self, date):
        self.minDate = date
        self.invalidateFilter()

    def filter_minimum_date(self):
        return self.minDate

    def set_filter_maximum_date(self, date):
        self.maxDate = date
        self.invalidateFilter()

    def filter_maximum_date(self):
        return self.maxDate

    def filter_accepts_row(self, sourceRow, sourceParent):
        index0 = self.sourceModel().index(sourceRow, 0, sourceParent)
        index1 = self.sourceModel().index(sourceRow, 1, sourceParent)
        index2 = self.sourceModel().index(sourceRow, 2, sourceParent)

        return ((self.filterRegExp().indexIn(self.sourceModel().data(index0)) >= 0
                 or self.filterRegExp().indexIn(self.sourceModel().data(index1)) >= 0)
                and self.date_in_range(self.sourceModel().data(index2)))

    def date_in_range(self, date):
        if isinstance(date, QtCore.QDateTime):
            date = date.date()

        return ((not self.minDate.isValid() or date >= self.minDate)
                and (not self.maxDate.isValid() or date <= self.maxDate))


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    menu = MainMenu()
    menu.show()
    sys.exit(app.exec_())