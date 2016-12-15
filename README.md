# DjangonizeIt
A single-file program to simplify work with images for Django developers

The "djangonizeit.pyw" isn't actual, but it includes some Python features, which are absent in the UX version, like:
 1. Overriding of magic methods. Magic method __call__ is used here to call own windows of classes from
 other classes, when it is necessary. In the UX version, classes aren't calling. All of them (their examples) are
 started simultaneously with program as GUI elements (tabs) of Main window. Maybe the __call__ method will be used for
 calling History() from DjangoImages() in the future, when the functionality of program will arising and when the
 space for tabs will be needed.

 2. Inheritance of GUI elements. Classes in "djangonizeit.pyw" are inheriting complete buttons, labels, etc. from
 superclasses (and partly override them in some cases), which make the program more efficient, but more complicated.
 In the UX version, methods are inheriting only. For example method self._view() (from DjangoImages) is calling through
 its constructor and calling at all subclasses where the DjangoImages constructor is inheriting (but it is overriding
 in all cases).

 3. Absolute positioning (non-adaptive but fully customized). The main window of "djangonizeit.pyw" is painting
 through absolute positioning, other windows are painting through groupboxes. The UX version is painting through
 groupboxes only.

 4. "Restart". The "djangonizeit.pyw" can be pseudo-restarted from the main window ( The "Restart" button is connecting
 with two signals when the user click it: self.hide and os.system("djangonizeit.pyw")). In UX version this feature
 isn't demanding.

 5. UA Info. In "djangonizeit.pyw" this feature allows the Ukrainians to understand what is this program. Texts of the
 UX version are writing in Ukrainian English and it is easy to understand for both Ukrainians and Non-Ukrainians.