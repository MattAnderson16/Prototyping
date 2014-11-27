import sys
import sqlite3
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tabs Test")
        
        self.tabs = QTabWidget()
        self.menu_bar = QMenuBar()
        self.tool_bar = QToolBar("Manage Databases")        

        self.file_menu = self.menu_bar.addMenu("File")
        self.open_database = self.file_menu.addAction("Open Database")

        self.tool_bar.addAction(self.open_database)
        self.addToolBar(self.tool_bar)

        self.setMenuWidget(self.menu_bar)

        self.open_database.triggered.connect(self.load_database)
        
        #Create tabs
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()

        #Create layouts
        self.create_button_layout()
        self.create_text_layout()
        self.create_text_box_layout()
        self.create_bar_layout()
        
        #Add tabs
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")
        self.tabs.addTab(self.tab3, "Tab 3")
        self.tabs.addTab(self.tab4, "Tab 4")
        
        self.setCentralWidget(self.tabs)

    def create_bar_layout(self):
        if not hasattr(self,"bar_layout"):
            self.bar_canvas = Canvas()
            self.bar_layout = QVBoxLayout()
            self.bar_layout.addWidget(self.bar_canvas)
            self.tab4.setLayout(self.bar_layout)

    def create_button_layout(self):
        if not hasattr(self,"button_layout"):
            self.button_layout = QVBoxLayout()
            self.button_label = QLabel("Push this pointless button!")
            self.button = QPushButton("pointless button")
            self.button_layout.addWidget(self.button_label)
            self.button_layout.addWidget(self.button)
            self.tab1.setLayout(self.button_layout)
            
    def create_text_layout(self):
        if not hasattr(self,"text_layout"):
            self.text_layout = QVBoxLayout()
            self.text = QLabel("Hello, I am a pointless label")
            self.text_layout.addWidget(self.text)
            self.tab2.setLayout(self.text_layout)
            
    def create_text_box_layout(self):
        if not hasattr(self,"text_box_layout"):
            self.text_box_layout = QVBoxLayout()
            self.text_box_label = QLabel("Enter your name into the pointless text box!")
            self.pointless_label = QLabel ("<< Pointless Text Box")
            self.text_box = QLineEdit()
            self.pointless_layout = QHBoxLayout()
            self.pointless_layout.addWidget(self.text_box)
            self.pointless_layout.addWidget(self.pointless_label)
            self.pointless_widget = QWidget()
            self.pointless_widget.setLayout(self.pointless_layout)
            self.text_box_layout.addWidget(self.text_box_label)
            self.text_box_layout.addWidget(self.pointless_widget)
            self.tab3.setLayout(self.text_box_layout)

    def load_database(self):
        path = QFileDialog.getOpenFileName(caption="Open Database")
        self.controller = Controller(path)
        self.graph_data()

    def graph_data(self):
        totals= self.controller.product_totals("2013-05-27")
        self.bar_canvas.show_bar_graph(totals,"2012-05-27")

class Canvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(1,1,1)
        super().__init__(self.fig)
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.fig.canvas.draw()

    def show_bar_graph(self,data,date):
        self.ax.clear()
        data_dict = dict(data)
        for i, key in enumerate(data_dict):
            self.ax.bar(i,data_dict[key])
        self.ax.set_xticks(np.arange(len(data_dict))+0.4)
        self.ax.set_xticklabels(list(data_dict.keys()))
        self.fig.autofmt_xdate()
        self.ax.set_title("Total Sales for {0}".format(date))
        self.ax.set_xlabel("Product")
        self.ax.set_ylabel("Amount (£)")
        self.fig.canvas.draw()

class Controller:
    def __init__(self,path):
        self.path = path

    def query(self,sql,parameters=None):
        with sqlite3.connect(self.path) as self.db:
            cursor = self.db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            if parameters != None:
                cursor.execute(sql,parameters)
            else:
                cursor.execute(sql)
            results = cursor.fetchall()
            return results

    def product_totals(self,date):
        sql = """SELECT product.name, sum(product.price) as total
                 FROM product, order_items, customer_order
                 WHERE order_items.order_id = customer_order.order_id and
                 order_items.product_id = product.product_id and
                 customer_order.date = ?
                 GROUP BY product.name"""
        return self.query(sql,[date])
    
    
if __name__ == "__main__":
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.raise_()
    application.exec_()
