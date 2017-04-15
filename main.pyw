from PySide.QtGui import *
from PySide.QtCore import *
import tab,os
class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow,self).__init__()
		self.setStyleSheet(open("style/app.css","r").read())
		self.resize(700,400)
		self.setWindowTitle("Sublime C")
		self.setAcceptDrops(True)
		self.tabs = tab.MainTab()
		self.setWindowIcon(QIcon("icon/icon_main.png"))
		self.setCentralWidget(self.tabs)
		self.menu()

	def menu(self):
		bar   = self.menuBar()
		File  = bar.addMenu("File")
		open_ = QAction("Open File..",self,triggered=self.tabs.openFile_c,shortcut="Ctrl+O")
		new_  = QAction("New File",self,triggered=self.tabs.newTab,shortcut="Ctrl+N")
		save_ = QAction("Save ",self,triggered=self.tabs.saveFile_c,shortcut="Ctrl+s")
		saveAs= QAction("SaveAs",self,triggered=self.tabs.saveFileAs,shortcut="Shift+Ctrl+S")
		tool  = bar.addMenu("Tool")
		run= QAction("Build",self,triggered=self.tabs.run,shortcut="Ctrl+B")
		complie= QAction("Complie",self,triggered=self.tabs.compile,shortcut="F5")




		File.addAction(new_)
		File.addAction(open_)
		File.addAction(save_)
		File.addAction(saveAs)
		tool.addAction(run)
		tool.addAction(complie)
		
	def side_bar_(self,a):
		if a.text().split(" ")[0] == "Hide":
			self.tree.setHidden(True)
			self.side_bar.setText("Show Side Bar")
		else:
			self.tree.setHidden(False)
			self.side_bar.setText("Hide Side Bar")



	def dragEnterEvent(self, e):
		if e.mimeData().hasUrls():
		 	e.accept()
		else:
			e.ignore()

	def dropEvent(self, e):
		path = e.mimeData().urls()[0].toString().split("///")[1]
		if os.path.isdir(path):
			self.tree.setHidden(False)
			self.side_bar.setText("Hide Side Bar")
			self.tree.open_drop(path)
		else:
			if path.endswith(".c"):
				self.tabs.open_file_c(path)
			else:
				self.tabs.open_otherFile(path)



def main():
	import sys
	app = QApplication([])
	

	win = MainWindow()
	if len(sys.argv) > 2:
		win.prt(sys.argv[2])
	if len(sys.argv) > 1:
		win.prt(sys.argv[1])
	win.show()
	app.exec_()
if __name__ == '__main__':
	main()
