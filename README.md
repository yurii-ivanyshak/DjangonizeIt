# DjangonizeIt
A single-file program to simplify work with static files for Django developers

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
    The UX (user experience) version of DjangonizeIt application is a main now.
    The inheritance structure is less complicated here.

     PyQT Parent |            QtGui.QWidget                                QtGui.QSortFilterProxyModel
     Parent      |    Welcome     Main      DjangoImages                        SortFilterHistory
     1st Child   |                    DjangoFiles     History
     2nd Child   |                  DjangoTemplates

        Class attributes from magic method __call__ is replaced by internal method _view. Most of class attributes
     from constructor are, also transferred to internal methods and just calling from their constructors. 
     All buttons from constructors, are moved to internal methods too.
        The user interface became more friendly.
 
 * .pyw extention allows to use file as exective at Windows. Change the extention to .py for using at Linux
 * UX version is strongly recommended
