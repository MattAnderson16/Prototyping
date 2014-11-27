from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

##class main_window(QMainWindow):
##    def __init__(self):
##        super().__init__()
##        self.setWindowTitle("WebPage test")

WebView = QWebView()
WebView.load(QUrl("http://google.co.uk"))
WebView.Show()
