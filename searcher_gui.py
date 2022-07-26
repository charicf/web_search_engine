import sys
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QVBoxLayout, QGridLayout, QListWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot, Qt
from vector_space_IR_sys import *

class App(QMainWindow):

	def __init__(self, links, pages):
		super().__init__()
		self.title = 'Web search engine for UIC'
		self.left = 400
		self.top = 250
		self.width = 1000
		self.height = 600
		# Set the central widget and the general layout
		self.generalLayout = QVBoxLayout()
		self.centralWidget = QWidget(self)
		self.setCentralWidget(self.centralWidget)
		self.setContentsMargins(200,0,200,100);
		self.centralWidget.setLayout(self.generalLayout)

		self.links = links
		self.pages = pages
		self.click_number = 0

		self.initUI()
	
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
	
		horLayout = QHBoxLayout()
		horLayout.setContentsMargins(200,0,200,0);
		self.labelImage = QLabel(self)
		pixmap = QPixmap("uic.png").scaled(400,400,Qt.KeepAspectRatio)
		self.labelImage.setPixmap(pixmap)
		self.labelImage.move(0, 0)
		self.labelImage.setGeometry(70, 80, 100, 100)
		horLayout.addWidget(self.labelImage)
		self.generalLayout.addLayout(horLayout)

		# Create textbox
		self.textbox = QLineEdit()
		self.textbox.move(20, 20)
		self.textbox.resize(280,40)
		self.generalLayout.addWidget(self.textbox)
		
		# Create a button in the window
		buttonsLayout = QGridLayout()
		self.button_search = QPushButton('Search', self)
		self.button_search.move(20,80)
		self.button_search.setFixedSize(100, 40)
		buttonsLayout.addWidget(self.button_search, 0, 2)
		self.generalLayout.addLayout(buttonsLayout)
		
		# Scroll Area Properties.
		self.urls_list = QListWidget()
		#self.urls_list.setWidgetResizable(True)
		self.generalLayout.addWidget(self.urls_list)
		self.urls_list.hide()

		self.button = QPushButton('Show 10 more', self)
		self.button.move(20,80)
		self.button.setFixedSize(100, 40)
		self.generalLayout.addWidget(self.button)

		# connect button to function on_click
		self.button_search.clicked.connect(self.on_click_search)
		self.button.clicked.connect(self.on_click_more_pages)
		self.show()
	
	@pyqtSlot()
	def on_click_more_pages(self):

		self.click_number += 1
		self.urls_list.clear()
		for i, link in enumerate(self.sorted_links[:10*self.click_number]):
			self.urls_list.addItem(str(i) + '. ' + link)
		self.urls_list.show()

	@pyqtSlot()
	def on_click_search(self):

		#pdb.set_trace()
		
		self.click_number = 1
		self.urls_list.clear()
		query = self.textbox.text()
		sorted_pages = run_IR_system(self.pages, [query])
		self.sorted_links = self.sort_links(self.links, sorted_pages[0])

		if not self.sorted_links:
			self.urls_list.addItem('There are not results that match this query')
		else:
			for i, link in enumerate(self.sorted_links[:10*self.click_number]):
				self.urls_list.addItem(str(i) + '. ' + link)
		self.urls_list.show()


		#textboxValue = self.textbox.text()
		#QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
		#self.textbox.setText("")

	def sort_links(self, links, sorted_pages):

		sorted_links = []

		for page in sorted_pages:

			sorted_links.append(links[int(page[1:])])

		return sorted_links

