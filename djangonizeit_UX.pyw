"""
    Info EN
                            'Djangonize It!' - A single-file application (Also, it is a single-window now!)
        The purpose of this application is to simplify work with images and templates for Django developers.
        For successful using, you should install the app into "images" folder inside the "static" folder of your
    django project (../static/../images/). This solution simultaneously supporting the recommended file
    structure of django projects and allows to avoid additional user and program activities related to path setting
    for image download. The installed PyQt4 is, also, needed.
        The application allows to perform the next operations:
        1. Download images from the Internet by link and return valid link for user's django project.
           All results of the operation are logging (in "db.txt" in a folder with the program). Also, the class for
           simplification of work with logs is realised (Also, you can log all existing images). It supports sorting
           by name/django link/date. Also, searching can be performed by normal and RegEx strings. The image is
           downloading to images folder as default, but user can choose any its subfolder as allocation for image.
        2. Search and replacement image links on django-links at frontend (HTML, CSS) files. Search is RegEx driven.
           The application have default regular expressions for CSS and HTML files, which can be changed by user (this
           is necessary for cases when the name of folder with images isn't "images").
           When you run the djangonization process for the file, it isn't replaced. The app creates a copy of the file
           at folder with original. Copy's name is forming as a "[0-9]old name", which allow simplifying it searching at
           folder (it was at the top or bottom). Also, created file can be opened from the program by os explorer.
        3. Add records for templates to views.py and connect their views to urls.py (inside the django app folder). If
           urls.py isn't exist inside the django app folder, the program will create it. After the operation performing,
           the django app is ready to be connected to urls.py of django-project thorough include() function. The app
           creates views and urls only for django templates (html files) except exception list(base.html and index.html)
           (editable).
        The application is created in object-oriented style.
    -----------------------------------------------------------------
    This is an UX (user experience) version of DjangonizeIt application.
    The inheritance structure is less complicated here.

     PyQT Parent |          QtGui.QWidget                  QtGui.QSortFilterProxyModel          QtGui.QDialog
     Parent      |    Welcome          DjangoImages             SortFilterHistory                   Main
     1st Child   |                DjangoFiles     History
     2nd Child   |              DjangoTemplates

        Class attributes from magic method __call__ is transferred to internal method _view. Most of class attributes
     from constructor are, also transferred to internal methods and just calling from their constructors. All buttons,
     from constructors, are moved to internal methods too.
        The user interface became more friendly.

"""

import os
import sys
import re
from urllib.request import URLopener
from datetime import datetime
from random import randint
from PyQt4 import QtGui, QtCore

class Welcome(QtGui.QWidget):
    """Class-greeting.
    The purpose of this class is to give a feeling that this app is user-friendly!

    """
    welcomeText = [
                   ["Hello, I'm UX version of DjangonizeIt! and I'm user-friendly!", "Move me into the 'images' folder "
                    "inside the 'static' folder\nof your django project (../static/../images/) and \n"
                    "I will perform a lot of routine work instead of you!"],
                   ["I'm able to:", "1. Download your images from web and return you django links for them.\n"
                                    "\tChoose tab 'Images' if you need this\n"
                                    "2. Remember information about every image which I downloaded for you!\n"
                                    "\tChoose tab 'Images History' if you need this info\n"
                                    "3. Replace non django links in your HTML and CSS files on django links.\n"
                                    "\tChoose tab 'Files' if you need this\n"
                                    "4. Update views and urls records for your django template files\n"
                                    "\tChoose tab 'Templates' if you need this\n"],
                   ["My hobby:", "Hide and seek"]
                  ]
    def __init__(self):
        super().__init__()
        self._view()

    def _view(self):
        "Contains information about positioning of elements at window"
        self._groupboxes()

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.helloGroupBox)
        mainLayout.addWidget(self.abilityGroupBox)
        mainLayout.addWidget(self.hobbyGroupBox)
        self.setLayout(mainLayout)

    def _groupboxes(self):
        "All GroupBoxes in one row"
        self.helloGroupBox, self.abilityGroupBox, self.hobbyGroupBox = map(self._welcome_box, self.welcomeText)

    def _welcome_box(self, text, fontsize=9, style="color: rgb(10, 15, 150)"):
        "Transform list to GroupBox"
        textLabel = QtGui.QLabel(text[1], self)
        font = QtGui.QFont()
        font.setPointSize(fontsize)
        textLayout = QtGui.QGridLayout()
        textLabel.setFont(font)
        textLayout.addWidget(textLabel, 0, 0)
        blockGroupBox = QtGui.QGroupBox(text[0])
        blockGroupBox.setFont(font)
        blockGroupBox.setLayout(textLayout)
        textLabel.setStyleSheet(style)
        blockGroupBox.setStyleSheet(style)
        return blockGroupBox


class DjangoImages(QtGui.QWidget):
    ''' Parent of functional classes of application (contains all elements constructors and default variables).
    Download images from the Web, return django-links, log the result.

    '''
    NOW = datetime.now()                # Constant for logs
    bFontSize = 10                      # Default font size for buttons
    bStyle = "color: rgb(0, 85, 200);"  # Default stylesheet for buttons
    lFontSize = 10                      # Default font size for labels
    lStyle = "color: rgb(0, 85, 200);"  # Default stylesheet for labels
    database = "db.txt"                 # Default name of database (for logs)
    defaultCSS = r'\.\..*/images/'      # Default pattern for re.sub function for CSS (DjangoFiles().djangonize())
    defaultHTML = r'src=\".*images/(.*\.[a-z]{3}).*?\"'  # Default pattern for re.sub function for HTML

    def __init__(self):
        super().__init__()
        self._view()          # is calling in all subclasses through constructor inheritance.

    def _view(self):
        "Contains information about positioning of elements at window"
        self._elements()

        self._linkgroupbox()
        self._namegroupbox()
        self._buttonsgroupbox()

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.linkGroupBox)
        mainLayout.addWidget(self.nameGroupBox)
        mainLayout.addWidget(self.buttonsGroupBox)
        self.setLayout(mainLayout)

    def _elements(self):
        # Buttons
        self.djangonizeButton = self.create_button("Djangonize It!", self.djangonize,
                                                   tooltip="Download image,return django link, log the result")
        self.quitButton = self.create_button('Quit', self.quit_app(), tooltip="Close All Windows")
        self.emptyLabel = self.create_label("\t     ")  # Filler for buttonsLayout

        # Lines
        self.linkText = self.create_text_edit(tooltip="Enter the image URL here. "
                                                      "Like: https://www.example.com/image.png")
        self.nameLine = self.create_line_edit(tooltip="Enter the new filename here. "
                                                      "Like: image for 'image.png'")
        self.djangoLine = self.create_line_edit(tooltip="A django link will arise here after djangonization")

        # Combobox
        self.folderBox = self.create_combo_box('Default')
        self.folderBox.setEditable(False)
        self.folderBox.setToolTip('Folders where the image may be allocated')
        self.add_folders()

    "GroupBoxes"
    def _linkgroupbox(self):
        linkLayout = QtGui.QGridLayout()
        linkLayout.addWidget(self.linkText, 0, 0)

        self.linkGroupBox = QtGui.QGroupBox("URL:")
        self.linkGroupBox.setLayout(linkLayout)
        return  self.linkGroupBox

    def _namegroupbox(self):
        nameLayout = QtGui.QHBoxLayout()
        nameLayout.addWidget(self.nameLine, 9)
        nameLayout.addWidget(self.folderBox, 2)

        self.nameGroupBox = QtGui.QGroupBox("Filename:")
        self.nameGroupBox.setLayout(nameLayout)
        return  self.nameGroupBox

    def _buttonsgroupbox(self):
        buttonsLayout = QtGui.QGridLayout()
        buttonsLayout.addWidget(self.djangonizeButton, 0, 3)
        buttonsLayout.addWidget(self.quitButton, 2, 5)
        buttonsLayout.addWidget(self.emptyLabel, 2, 0)
        buttonsLayout.addWidget(self.djangoLine, 1, 3)

        self.buttonsGroupBox = QtGui.QGroupBox("Djangonization and Control buttons:")
        self.buttonsGroupBox.setLayout(buttonsLayout)
        return  self.buttonsGroupBox

    "Element constructors"
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

    def create_text_edit(self, tooltip=None):
        textEdit = QtGui.QTextEdit()
        textEdit.setToolTip(tooltip)
        return textEdit

    def create_line_edit(self, tooltip=None):
        lineEdit = QtGui.QLineEdit()
        lineEdit.setToolTip(tooltip)
        return lineEdit

    def create_combo_box(self, text=""):
        # Element constructor for DjangoFiles
        comboBox = QtGui.QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        return comboBox

    def dir_list(self, path):
        "Method which returns list of folders before static folder (in django structure). Optimized for different os"
        if os.name == 'nt':
            pathList = re.findall(r'static\\(.+).*$', path) # path is saved as a list with one element
            try:
                dirList = pathList[0].split('\\')
            except IndexError:  # Error when list is empty (for cases when the application isn't installed)
                QtGui.QMessageBox.information(self, "InstallError",
                                          "Please, move the program inside your django project "
                                          "(..\static\..\images)to solve the Error!")
                raise
            return dirList
        else:
            pathList = re.findall(r'static/(.+).*$', path)
            try:
                dirList = pathList[0].split('/')
            except IndexError:
                QtGui.QMessageBox.information(self, "InstallError",
                                          "Please, move the program inside your django project "
                                          "(../static/../images)to solve the Error!")
                raise
            return dirList

    def djangonize(self):
        "Download image and return its django-link (Is overridden in DjangoFiles and DjangoTemplates)"
        url = str(self.linkText.toPlainText())       # Entered URL (by user)
        folder = self.folderBox.currentText()        # Folder where the image will be downloaded
        if re.search(r'\.[a-z]{3}$', url):           # Validate link by type of file
            filename = str(self.nameLine.displayText())

            if len(filename) == 0:        # If the filename line is empty save the image with its basename
                newFilename = os.path.basename(url)
            else:                         # Else, save it with entered name and original fileformat
                newFilename = filename + os.path.basename(url)[-4:]

            #Block to define allocation where the image will be downloaded
            if folder == 'Default':           # 'Default' - the same folder where the app file is placed
                allocation = newFilename
            else:
                allocation = '/'.join([folder, newFilename])

            dirList = self.dir_list(os.getcwd())

            # If with dir_list() all is ok, download image to django directory
            # If statement don't used here, because any Exception in dir_list() will stop an execution of the method
            URLopener().retrieve(str(url), allocation)

            djangoView = "{% static '" + '/'.join(dirList) + '/' + allocation + " '%}"   # Djangonized link
            self.djangoLine.setText(djangoView)              # Return the link to user interface

            # Log the result
            with open(self.database, "a") as f:
                historyNote = ','.join([newFilename, djangoView, str(self.NOW.year), str(self.NOW.month),
                                       str(self.NOW.day), str(self.NOW.hour), str(self.NOW.minute)])+'\n'
                f.write(historyNote)
        else:
            QtGui.QMessageBox.information(self, "Link is wrong or not exist", "The IMAGE link should be entered!")

    def add_folders(self):
        "Searching folders in folder with program and add them to combobox."
        directoryList = os.listdir()
        folders = list(filter(lambda x: x if os.path.isdir(x) else None, directoryList))
        list(map((lambda folder: self.folderBox.addItem(folder,folder)), folders))

    def quit_app(self):
        "Complete quit from app"
        return QtCore.QCoreApplication.instance().quit


class History(DjangoImages):
    ''' Class for comfortable work with logs.
    Sort and filter djangonized images (RegEx supports). All info in table can be copied.

    '''
    def __init__(self):
        super().__init__()

    def _view(self):
        "Contains information about positioning of elements at window"
        self._elements()

        self.text_filter_changed()
        self.date_filter_changed()

        self._proxygroupbox()
        self._buttonsgroupbox()

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.proxyGroupBox)
        mainLayout.addWidget(self.buttonsGroupBox)

        self.setLayout(mainLayout)

    def _elements(self):
        # Buttons
        self.openButton = self.create_button('Folder', self.open_folder, tooltip="Open folder with djangonized images")
        self.quitButton = self.create_button('Quit', self.quit_app(), tooltip="Close All Windows")
        self.refreshButton = QtGui.QPushButton('Refresh', self)
        self.refreshButton.clicked.connect(self.refresh_table)
        self.importButton = QtGui.QPushButton('Import All', self)
        self.importButton.clicked.connect(self.import_button)
        self.importButton.setToolTip('Add djangonized links of all files in image folder and its subfolders to database')

        self.emptyLabel = QtGui.QLabel()  # Filler for proxyLayout

        self._proxy()
        self._search_box()
        self._date_boxes()

    def _proxy(self):
        self.proxyModel = SortFilterHistory(self)       # Technical class (PyQt template)
        self.proxyModel.setDynamicSortFilter(True)

        self.proxyView = QtGui.QTreeView()  # Table view
        self.proxyView.setRootIsDecorated(False)
        self.proxyView.setAlternatingRowColors(True)
        self.proxyView.setModel(self.proxyModel)  # Setting of table for the view
        self.proxyView.setSortingEnabled(True)
        self.proxyView.sortByColumn(1, QtCore.Qt.AscendingOrder)
        self.proxyModel.setSourceModel(self.create_log_table())  # Setting of table for the window

        self.proxyView.setColumnWidth(0, 75)              # Width of the "Name" column
        self.proxyView.setColumnWidth(1, 235)             # Width of the "Djangonized link" column
        self.proxyView.setColumnWidth(2, 75)              # Width of the "Date" column

    "GroupBoxes"
    def _search_box(self):
        self.filterPatternLineEdit =self.create_line_edit()          # Search line
        self.filterPatternLabel = QtGui.QLabel("Filter pattern:")
        self.filterPatternLabel.setBuddy(self.filterPatternLineEdit)

        self.filterSyntaxComboBox = QtGui.QComboBox()                            # Search modes
        self.filterSyntaxComboBox.addItem("Normal", QtCore.QRegExp.FixedString)  # 1st (Default)
        self.filterSyntaxComboBox.addItem("RegEx", QtCore.QRegExp.RegExp)  # 2nd (Switch with Normal to make it default)
        self.filterSyntaxComboBox.setToolTip("Search mode")

    def _date_boxes(self):
        #Dates
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

    def _proxygroupbox(self):
        proxyLayout = QtGui.QGridLayout()
        proxyLayout.addWidget(self.proxyView, 0, 0, 1, 3)
        proxyLayout.addWidget(self.importButton, 1, 0)
        proxyLayout.addWidget(self.refreshButton, 1, 2)
        proxyLayout.addWidget(self.filterPatternLabel, 2, 0)
        proxyLayout.addWidget(self.filterPatternLineEdit, 2, 1)
        proxyLayout.addWidget(self.filterSyntaxComboBox, 2, 2)
        proxyLayout.addWidget(self.fromLabel, 3, 0)
        proxyLayout.addWidget(self.fromDateEdit, 3, 1, 1, 2)
        proxyLayout.addWidget(self.toLabel, 4, 0)
        proxyLayout.addWidget(self.toDateEdit, 4, 1, 1, 2)

        self.proxyGroupBox = QtGui.QGroupBox("Sort/Filter Links")
        self.proxyGroupBox.setLayout(proxyLayout)
        return  self.proxyGroupBox

    def _buttonsgroupbox(self):
        buttonsLayout = QtGui.QHBoxLayout()
        buttonsLayout.addWidget(self.openButton, 1)
        buttonsLayout.addWidget(self.emptyLabel, 3)
        buttonsLayout.addWidget(self.quitButton, 1)

        self.buttonsGroupBox = QtGui.QGroupBox("Control buttons")
        self.buttonsGroupBox.setLayout(buttonsLayout)
        return self.buttonsGroupBox

    def text_filter_changed(self):
        "Filtering by filter patterns (Normal, RegEx)"
        syntax = QtCore.QRegExp.PatternSyntax(
            self.filterSyntaxComboBox.itemData(
                self.filterSyntaxComboBox.currentIndex()))

        regExp = QtCore.QRegExp(self.filterPatternLineEdit.text(), True, syntax)
        self.proxyModel.setFilterRegExp(regExp)

    def date_filter_changed(self):
        "Filtering by dates"
        self.proxyModel.set_filter_minimum_date(self.fromDateEdit.date())
        self.proxyModel.set_filter_maximum_date(self.toDateEdit.date())

    def add_log(self,table, name, link, date):
        "Fill row of the table"
        table.insertRow(0)
        table.setData(table.index(0, 0), name)
        table.setData(table.index(0, 1), link)
        table.setData(table.index(0, 2), date)

    def create_log_table(self):
        "Create table and fill it by log data"
        table = QtGui.QStandardItemModel(0, 3, self)

        table.setHeaderData(0, QtCore.Qt.Horizontal, "Name")
        table.setHeaderData(1, QtCore.Qt.Horizontal, "Djangonized link")
        table.setHeaderData(2, QtCore.Qt.Horizontal, "Date")

        # Fill the table
        try:
            with open(self.database) as f:
                lines = f.readlines()
                for line in lines:
                        line = line.split(',')
                        self.add_log(table, line[0], line[1],           # Name,Link
                                     QtCore.QDateTime(QtCore.QDate(int(line[2]), int(line[3]), int(line[4])),  # Date
                                                                   QtCore.QTime(int(line[5]), int(line[6]))))  # Time'
        except FileNotFoundError:
            pass                        # This is right. We just need to avoid the Error if you haven't file for logs.
        return table

    def open_folder(self):
        "Open folder with djangonized images"
        return os.system(QtGui.QFileDialog().getOpenFileName(self,'Open Dj-folder', QtCore.QDir.currentPath()))

    def import_all(self, path):
        "Method to find all files (images) in the folder and it subfolders, and add their notes to database"
        elements = os.listdir(path)

        # Block for copykilling
        currentImages = []
        try:
            with open(self.database) as f:
                lines = f.readlines()
                for line in lines:
                    line = line.split(',')
                    currentImages.append(line[0])
        except FileNotFoundError:                      #Create the db file if it isn't exist
            f = open(self.database, 'w')
            f.close()

        # Block for adding the folder and subfolders elements
        for element in elements:
            if os.path.isdir(element):
                self.import_all(os.path.join(path, element))     # Recursive call for subfolder
            else:
                if element in currentImages:        # Copykiller
                    continue
                else:
                    dirList = self.dir_list(path)

                    djangoView = "{% static '" + '/'.join(dirList) + '/' + element + " '%}"  # Djangonized link

                    # Import element link to the database
                    with open(self.database, "a") as f:
                        historyNote = ','.join([element, djangoView, str(self.NOW.year), str(self.NOW.month),
                                                str(self.NOW.day), str(self.NOW.hour), str(self.NOW.minute)]) + '\n'
                        f.write(historyNote)

    def import_button(self):
        "Transform the import_all method in the form callable by PyQt button."
        return self.import_all(os.getcwd())

    def refresh_table(self):
        QtGui.QMessageBox.information(self, "Unready feature",
                                      "The feature isn't ready, restart the program to refresh!")


class DjangoFiles(DjangoImages):
    ''' Class simplify work with website templates for django programmers.
    Djangonize links in CSS and HTML files, save a copy of djangonized files in the format [0-9]oldname,
    return the name to a user.

    '''
    def __init__(self):
        super().__init__()

    def _view(self):
        "Contains information about positioning of elements at window"
        self._elements()
        self._filegroupbox()
        self._regexgroupbox()
        self._buttonsgroupbox()

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.fileGroupBox)
        mainLayout.addWidget(self.regexGroupBox)
        mainLayout.addWidget(self.buttonsGroupBox)
        self.setLayout(mainLayout)

    def _elements(self):
        # Buttons
        self.browseButton = self.create_button("Browse...", self.browse)
        self.djangonizeButton = self.create_button("Djangonize It!", self.djangonize,
                         tooltip="Make a copy of file where pattern is replaced by django links, return name of copy")
        self.djangonizeLine = self.create_line_edit(
                                        tooltip=" A name of changed file will arise here after djangonization")
        self.openButton = self.create_button("Open It!", self.open_file,
                                         tooltip="Open djangonized file by default program")
        self.quitButton = self.create_button('Quit', self.quit_app(), tooltip="Close All Windows")

        # Lines
        self.regexLine = self.create_line_edit()
        self.regexLine.setText("Choose a CSS or HTML file!")
        self.fileComboBox = self.create_combo_box(QtCore.QDir.currentPath())

    "GroupBoxes"
    def _filegroupbox(self):
        fileLayout = QtGui.QHBoxLayout()
        fileLayout.addWidget(self.fileComboBox, 4)
        fileLayout.addWidget(self.browseButton, 1)
        self.fileGroupBox = QtGui.QGroupBox("Browse file:")
        self.fileGroupBox.setLayout(fileLayout)
        return self.fileGroupBox

    def _regexgroupbox(self):
        regexLayout = QtGui.QVBoxLayout()
        regexLayout.addWidget(self.regexLine)
        self.regexGroupBox = QtGui.QGroupBox("Pattern for replacement:")
        self.regexGroupBox.setLayout(regexLayout)
        return self.regexGroupBox

    def _buttonsgroupbox(self):
        buttonsLayout = QtGui.QGridLayout()
        buttonsLayout.addWidget(self.djangonizeButton, 0, 2, 1, 3)
        buttonsLayout.addWidget(self.djangonizeLine, 1, 2, 1, 3)
        buttonsLayout.addWidget(self.openButton, 2, 0)
        buttonsLayout.addWidget(self.quitButton, 2, 5)
        self.buttonsGroupBox = QtGui.QGroupBox("Djangonization and Control buttons:")
        self.buttonsGroupBox.setLayout(buttonsLayout)
        return  self.buttonsGroupBox

    def browse(self):
        "Browse file and choose a default RegEx according to file extension"
        openedFile = QtGui.QFileDialog.getOpenFileName(self, "Find a CSS or HTML", self.fileComboBox.currentText())

        if openedFile:                            #add paths to the fileComboBox
            if self.fileComboBox.findText(openedFile) == -1:
                self.fileComboBox.addItem(openedFile)

            self.fileComboBox.setCurrentIndex(self.fileComboBox.findText(openedFile))

        filePath = self.fileComboBox.currentText()

        if filePath[-3:] == "css":
            self.regexLine.setText(self.defaultCSS)
        elif filePath[-3:] == "tml":
            self.regexLine.setText(self.defaultHTML)
        else:
            self.regexLine.setText("Wrong file. Choose a CSS or HTML!")

    def djangonize(self):
        "Method which make files more djangonized!"
        filePath = self.fileComboBox.currentText() # Path to file from fileComboBox
        dirList = self.dir_list()         # DjangonizeImage inherited method which returns folders before static folder
        newFilename = str(randint(0, 9)) + os.path.basename(filePath) # Filename where changes will be saved

        if filePath[-3:] == "css":
            djPath = '../' + '/'.join(dirList) + '/'  # Path to images in django project
            nonDjPath = str(self.regexLine.displayText())  # Path to images in CSS for replacement

            with open(os.path.join(os.path.dirname(filePath), newFilename), 'w') as f:    # open new
                content = open(filePath).read()                                    # copy data from old
                f.write('{% load staticfiles %}\n')                                # connect static files to CSS
                f.write(re.sub(nonDjPath, djPath, content))                        # replace line and write in new
                self.djangonizeLine.setText("New filename: {}".format(newFilename))        # return name of new

        elif filePath[-3:] == "tml":

            djPath = "src=\"{% static '" + '/'.join(dirList) + '/' + "\g<1>" + "' %}\"" # Path to django-project images
            nonDjPath = str(self.regexLine.displayText())  # Path in CSS or HTML for replace

            with open(os.path.join(os.path.dirname(filePath), newFilename), 'w') as f:   # Create a new file: [0-9]old name
                content = open(filePath).read()                              # Open old file and read it content
                f.write(re.sub(nonDjPath, djPath, content))                  # Replacement is here
                self.djangonizeLine.setText("New filename: {}".format(newFilename))     # Info for user

        else:
            self.djangonizeLine.setText("Wrong file. Choose CSS or HTML!")   # When not CSS or not HTML file is browsed

    def open_file(self):
        "This method open the folder with djangonized files in os explorer and allow choose file for opening."
        if re.match(r'New\sfilename', self.djangonizeLine.displayText()):
            if os.name == 'nt':
                os.system(QtGui.QFileDialog().getOpenFileName(self, 'Open Dj-file', '/'.join(
                                                            [os.path.dirname(self.fileComboBox.currentText()),
                                                             re.findall('\S+:\s(\d\S*)',
                                                                        self.djangonizeLine.displayText())[0]])))
            else:
                os.system(QtGui.QFileDialog().getOpenFileName(self, 'Open Dj-file', '\\'.join(
                                                            [os.path.dirname(self.fileComboBox.currentText()),
                                                             re.findall('\S+:\s(\d\S*)',
                                                                        self.djangonizeLine.displayText())[0]])))
        else:
            QtGui.QMessageBox.information(self,'OpenError', 'Djangonize file before opening')


class DjangoTemplates(DjangoFiles):
    ''' Class which connects user templates to views and urls in applications at django project.
    Compare templates in 'templates' folder with records in 'views.py' and 'urls.py' (create it if it isn't exist)
    and add records for templates which aren't connected to these files.

    '''
    exceptions = 'base.html, home.html, index.html'     #The program don't create views and urls for these templates

    def __init__(self):
        super().__init__()

    def _view(self):
        "Contains information about positioning of elements at window"
        self._elements()

        self._filegroupbox()                                    # Inherited
        self.fileGroupBox.setTitle("Browse templates folder:")

        self._regexgroupbox()                                   # Inherited
        self.regexGroupBox.setTitle("Except templates:")

        self._buttonsgroupbox()

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.fileGroupBox)
        mainLayout.addWidget(self.regexGroupBox)
        mainLayout.addWidget(self.buttonsGroupBox)
        self.setLayout(mainLayout)

    def _elements(self):
        # _filegroupbox (Is inherited from DjangoFiles)
        self.fileComboBox = self.create_combo_box(os.path.split(os.path.split(QtCore.QDir.currentPath())[0])[0])
        self.browseButton = self.create_button("Browse...", self.browse)

        # _regexgroupbox (Is inherited from DjangoFiles)
        self.regexLine = self.create_line_edit(tooltip="Views and urls records aren't be created for these files")
        self.regexLine.setText(self.exceptions)

        # _buttonsgroupbox
        self.djangonizeButton = self.create_button("DjangonizeIt!", self.djangonize, tooltip="Find templates in "
                                                   "choosen folder, analyse records in views and urls "
                                                    "if records for templates aren't found, create them")
        self.djangonizeText = self.create_text_edit()
        self.emptyLabel = QtGui.QLabel()
        self.quitButton = self.create_button("Quit", self.quit_app())

    def _buttonsgroupbox(self):
        buttonsLayout = QtGui.QGridLayout()
        buttonsLayout.addWidget(self.djangonizeButton, 0, 2, 1, 3)
        buttonsLayout.addWidget(self.djangonizeText, 1, 2, 1, 3)
        buttonsLayout.addWidget(self.emptyLabel, 2, 0)
        buttonsLayout.addWidget(self.quitButton, 2, 5)
        self.buttonsGroupBox = QtGui.QGroupBox("Djangonization and Control buttons:")
        self.buttonsGroupBox.setLayout(buttonsLayout)
        return self.buttonsGroupBox

    def browse(self):
        # Browse folder (Overrides method in DjangoFiles)
        openedDir = QtGui.QFileDialog.getExistingDirectory(self, "Find dir with templates",
                self.fileComboBox.currentText())

        if openedDir:
            if self.fileComboBox.findText(openedDir) == -1:
                self.fileComboBox.addItem(openedDir)

            self.fileComboBox.setCurrentIndex(self.fileComboBox.findText(openedDir))

    def find_templates(self):
        # Finds templates in choosen dir and return dict(name: dir/name)
        dirPath = self.fileComboBox.currentText()
        directory = os.path.split(dirPath)[1]
        exceptList = self.regexLine.displayText()

        directoryList = os.listdir(dirPath)
        templates = list(filter(lambda x: x.endswith('.html') if x not in exceptList else None, directoryList))
        self.djangonizeText.setText('I found {} template(s) for djangonization!'.format(len(templates)))
        tempDict = {template: '/'.join([directory, template]) for template in templates}
        return tempDict

    def find_views(self):
        # Finds file "views.py" of django application and return records with links on application templates
        dirPath = self.fileComboBox.currentText()
        limit = 0
        while ('views.py' not in os.listdir(dirPath)) and limit < 3:
            dirPath = os.path.split(dirPath)[0]           # level up!
            limit+=1
        else:
            assert(limit != 3)           # stop the program if while loop is stopped because the limit < 3 became False
            with open(os.path.join(dirPath,'views.py')) as viewsfile:
                viewsText = viewsfile.read()
                views = re.findall(r'[\'\"](\S+\/\S+\.html)[\'\"]', viewsText)
            return views, dirPath     # the urls.py will be searching in the same directory. Usually, we can have
                                      # situation in which urls.py don't exists at application folder and we should
                                      # create it. The dirPath of views.py will allow defining where the
                                      # urls.py should be created correctly.

    def create_find_urls(self):
        "Searching urls.py. If it isn't found, create it. Parse records with connected views, return them as list."
        dirPath = self.find_views()[1]
        if 'urls.py' not in os.listdir(dirPath):
            with open(os.path.join(dirPath, 'urls.py'), 'w') as urlsfile:
                urlsfile.write("from django.conf.urls import url\n\n"
                               "from . import views\n\n"
                               "urlpatterns = [\n"
                               "]")
            self.djangonizeText.setText('\n'.join([self.djangonizeText.toPlainText(),
                                                   'I created the urls.py in {}'.format(dirPath)]))
            urls = []
            return urls
        else:
            with open(os.path.join(dirPath, 'urls.py')) as urlsfile:
                urlsText = urlsfile.read()
                urls = re.findall(r'views\.(\S+),', urlsText)
                return urls

    def djangonize(self):
        "Add records for templates which aren't connected to views.py and urls.py (except exceptions)"
        tempDict = self.find_templates()
        views, dirPath = self.find_views()        # views = [ 'folder/name.html', ...]
        for key in tempDict:
            if tempDict[key] not in views:
                with open (os.path.join(dirPath, 'views.py'), 'a') as viewsfile:
                    viewsfile.write("\ndef {} (request):\n"
                                    "    return render(request, '{}')\n".format(key[:-5], tempDict[key]))
                self.djangonizeText.setText('\n'.join([self.djangonizeText.toPlainText(),
                                                       'I added the {} view to views.py'.format(key)]))

        urls = self.create_find_urls()            # urls = ['name', ...]

        for key in tempDict:
            if key[:-5] not in urls:
                with open(os.path.join(dirPath, 'urls.py')) as urlsfile:
                    urlsText = urlsfile.read()
                    urlsBuffer = urlsText[:]        # Allows to make changes in file without creation of second files
                with open(os.path.join(dirPath, 'urls.py'), 'w') as urlsfile:
                    urlsfile.write(re.sub(r']$', "    url(r'^{0}/', views.{0}, name='{0}'),\n]".format(key[:-5]),
                                          urlsBuffer))
                self.djangonizeText.setText('\n'.join([self.djangonizeText.toPlainText(),
                                                       'I added the {} url to urls.py'.format(key[:-5])]))

        self.djangonizeText.setText('\n'.join([self.djangonizeText.toPlainText(),
                                    "\nThe app is ready for connection to project's urls.py with include() function!"]))


class Main(QtGui.QWidget):
    """ Start window of the application
    Call the components of the application when buttons are clicking.

    """
    size = 450, 340                     # Default size of application windows (width, height)
    position = 450, 150                 # Default position of application windows (horizontal,vertical)

    def __init__(self):
        super().__init__()
        self._view()
        self.trayIcon.show()

    def _view(self):
        "Contains information about positioning of elements at window"
        self._main_tabs()

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.tabWidget)
        self.setLayout(mainLayout)

        # Tray icon block
        self._tray_icon_actions()
        self._tray_icon()
        self.trayIcon.activated.connect(self.double_click)

        self.setWindowTitle('DjangonizeIt! - A single-file application')
        self.resize(*self.size)
        self.move(*self.position)

    def _main_tabs(self):
        "List of Main tabs"
        self.tabWidget = QtGui.QTabWidget()
        self.tabWidget.addTab(Welcome(), "Welcome")
        self.tabWidget.addTab(DjangoImages(), "Images")
        self.tabWidget.addTab(History(), "Images History")
        self.tabWidget.addTab(DjangoFiles(), "Files")
        self.tabWidget.addTab(DjangoTemplates(), "Templates")
        return self.tabWidget

    def _tray_icon(self):
        "Create tray icon and link context menu actions to it"
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.minimizeAction)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)

    def _tray_icon_actions(self):
        "Context menu actions for tray icon"
        self.minimizeAction = QtGui.QAction("Minimize", self, triggered=self.hide)
        self.restoreAction = QtGui.QAction("Restore", self, triggered=self.show)
        self.quitAction = QtGui.QAction("Quit", self, triggered=QtGui.qApp.quit)

    def double_click(self, event):
        "Restore window by doubleclick"
        if event == QtGui.QSystemTrayIcon.DoubleClick:
            self.show()

    def closeEvent(self, event):
        "Intercepts close event (control panel), hide Main and show icon message"
        if self.trayIcon.isVisible():
            self.hide()                    #hide Main
            self.trayIcon.showMessage("Tray icon without icon", "Ha-ha, I'm here!")
            event.ignore()


class SortFilterHistory(QtGui.QSortFilterProxyModel):
    ''' Technical class for the History class. (pyQt template)
    An example of the class is used for representing (filtering) of table content by date range.

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
    view = Main()
    view.show()
    sys.exit(app.exec_())