from PySide.QtGui import *
from PySide.QtCore import *
import Edit,sys,os,re,time,syntax
import subprocess as sub

class msgBox(QMessageBox):
	def __init__(self):
		super(msgBox,self).__init__()
	def msg(self):
		self.setIcon(self.Warning)
		self.setText("<h4>Your Save File !</h4>")
		self.setStandardButtons(self.Cancel | self.Yes | self.No)
		self.setWindowTitle("Save File _ C")
		self.buttonClicked.connect(self.ret)
		self.exec_()
	def ret(self,but=None):
		if but != None:
			tBut = but.text()
				
		else:
			return tBut



class MainTab(QTabWidget):
	def __init__(self,parent=None):
		super(MainTab,self).__init__(parent=None)
		self.DFName = {}
		self.path_ap = re.search(r".*(?=/[A-Za-z0-9_].[A-Za-z0-9_])",sys.argv[0].replace("\\","/")).group()+"/"
		tab_bar = self.tabBar()
		self.setTabsClosable(True)
		self.setMovable(True)
		self.setTabShape(self.Triangular)
		self.tabCloseRequested.connect(self.rmTab)
		self.msg = msgBox()
		self.rmTab()
	def rmMBTab(self,but,intab):
		if type(but) == type(""):
			tBut = but
		else:
			tBut = but.text()
		if tBut == "&Yes":
			self.saveFile_c()
			if self.tabText(intab) in self.DFName :
				for i in self.DFName:
					if self.DFName[i][0] == self.DFName[self.tabText(intab)][0]:
						if i != self.tabText(intab):
							self.setTabText(self.DFName[i][1],self.DFName[i][0])
							self.DFName.update({self.DFName[i][0]:[i,self.DFName[i][1]]})
							self.DFName.pop(i)
				if self.DFName[self.tabText(intab)][1] == intab:
					self.DFName.pop(self.tabText(intab))
			self.removeTab(intab)
		elif tBut == "&No":
			if self.tabText(intab) in self.DFName :
				for i in self.DFName:
					if self.DFName[i][0] == self.DFName[self.tabText(intab)][0]:
						if i != self.tabText(intab):
							self.setTabText(self.DFName[i][1],self.DFName[i][0])
							self.DFName.update({self.DFName[i][0]:[i,self.DFName[i][1]]})
							self.DFName.pop(i)
				if self.DFName[self.tabText(intab)][1] == intab:
					self.DFName.pop(self.tabText(intab))
			self.removeTab(intab)
		else:
			pass

	def rmTab(self,inTab=0):
		self.indexTabs()
		if self.count() == 0:
			self.newTab()
		elif self.count() == 1:
			index = self.currentIndex()
			self.setCurrentIndex(inTab)
			doc = self.currentWidget().document()
			if doc.isModified():
				msg = QMessageBox()
				msg.setIcon(QMessageBox.Warning)
				msg.setText("<h4> Your Save File ! </h4>")
				msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes | QMessageBox.No)
				msg.setWindowTitle("Save File _ C")
				msg.buttonClicked.connect(lambda:self.rmMBTab(msg.clickedButton(),inTab))
				msg.exec_()
			else:
				if self.tabText(inTab) in self.DFName:
					if not os.path.exists(self.tabToolTip(inTab)):
						msg = QMessageBox()
						msg.setIcon(QMessageBox.Warning)
						msg.setText("<h4> Your Save File ! </h4>")
						msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes | QMessageBox.No)
						msg.setWindowTitle("Save File _ C")
						msg.buttonClicked.connect(lambda:self.rmMBTab(msg.clickedButton(),inTab))
						msg.exec_()
					else:
						self.rmMBTab("&No",inTab)
				else:
					self.rmMBTab("&No",inTab)
			self.newTab()
			self.setCurrentIndex(index)
		else:
			index = self.currentIndex()
			self.setCurrentIndex(inTab)
			doc = self.currentWidget().document()
			if doc.isModified():
				msg = QMessageBox()
				msg.setIcon(QMessageBox.Warning)
				msg.setText("<h4> Your Save File ! </h4>")
				msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes | QMessageBox.No)
				msg.setWindowTitle("Save File _ C")
				msg.buttonClicked.connect(lambda:self.rmMBTab(msg.clickedButton(),inTab))
				msg.exec_()
			else:
				if self.tabText(inTab) in self.DFName:
					if not os.path.exists(self.tabToolTip(inTab)):
						msg = QMessageBox()
						msg.setIcon(QMessageBox.Warning)
						msg.setText("<h4> Your Save File ! </h4>")
						msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes | QMessageBox.No)
						msg.setWindowTitle("Save File _ C")
						msg.buttonClicked.connect(lambda:self.rmMBTab(msg.clickedButton(),inTab))
						msg.exec_()
					else:
						self.rmMBTab("&No",inTab)
				else:
					self.rmMBTab("&No",inTab)
			self.setCurrentIndex(index)

	def newTab(self):
		self.addTab(Edit.Edit(False),"untitle")
	def openFile_c(self):
		self.indexTabs()
		fpath,ok = QFileDialog.getOpenFileName(self,'Open File C',"","(*.c)")
		if os.path.exists(fpath):
			index = self.currentIndex()+1
			fname = fpath.split("/")[-1]
			if not fname in self.DFName and not fpath in self.DFName:
				self.insertTab(index,Edit.Edit(True),fname)
				self.setTabToolTip(index,fpath)
				self.setCurrentIndex(index)
				wedit = self.currentWidget()
				fread = open(fpath,"r").read()
				wedit.setPlainText(fread)
				self.DFName.update({fname:[fpath,index]})
			elif fname in self.DFName and not fpath == self.DFName[fname][0] and not fpath in self.DFName:
				self.insertTab(index,Edit.Edit(True),fpath)
				self.setTabToolTip(index,fpath)
				self.setCurrentIndex(index)
				wedit = self.currentWidget()
				fread = open(fpath,"r").read()
				wedit.setPlainText(fread)
				self.DFName.update({fpath:[fname,index]})
				self.DFName[fname][0]
				self.DFName.update({self.DFName[fname][0]:[fname,self.DFName[fname][1]]})
				self.setCurrentIndex(self.DFName[fname][1])
				self.setTabText(self.currentIndex(),self.DFName[fname][0])
				self.setCurrentIndex(index)
				self.DFName.pop(fname)
			else:
				for i in range(self.count()):
					if fname == self.tabText(i):
						self.setCurrentIndex(i)
						break;
					elif fpath == self.tabText(i):
						self.setCurrentIndex(i)
						break;
	def indexTabs(self):
		if self.DFName != {}:
			for i in range(self.count()):
				if self.tabText(i) in self.DFName:
					for j in self.DFName:
						if j == self.tabText(i):
							self.DFName[j][1] = i
	def saveFile_c(self):
		wedit = self.currentWidget()
		doc = wedit.document()

		if doc.isModified():
			if os.path.exists(self.tabToolTip(self.currentIndex())):
				open(self.tabToolTip(self.currentIndex()),"w").write(wedit.toPlainText())
				doc.setModified(False)
			else:
				fSpath,ok = QFileDialog.getSaveFileName(self,"Save File","*.c")
				if fSpath:
					if self.tabText(self.currentIndex()) in self.DFName:
						self.DFName.pop(self.tabText(self.currentIndex()))
					fname = fSpath.split("/")[-1]
					open(fSpath,"w").write(wedit.toPlainText())
					if fSpath.endswith(".c"):
						self.highlighter = syntax.Highlighter(wedit.document())
						wedit.file_c2 = True
					self.DFName.update({fname:[fSpath,self.currentIndex()]})
					self.setTabText(self.currentIndex(),fname)
					self.setTabToolTip(self.currentIndex(),fSpath)
					doc.setModified(False)
		else:
			if os.path.exists(self.tabToolTip(self.currentIndex())):
				open(self.tabToolTip(self.currentIndex()),"w").write(wedit.toPlainText())
				doc.setModified(False)
			else:
				fSpath,ok = QFileDialog.getSaveFileName(self,"Save File","*.c")
				if fSpath:
					if self.tabText(self.currentIndex()) in self.DFName:
						self.DFName.pop(self.tabText(self.currentIndex()))
					fname = fSpath.split("/")[-1]
					open(fSpath,"w").write(wedit.toPlainText())
					if fSpath.endswith(".c"):
						self.highlighter = syntax.Highlighter(wedit.document())
						wedit.file_c2 = True
					self.DFName.update({fname:[fSpath,self.currentIndex()]})
					self.setTabText(self.currentIndex(),fname)
					self.setTabToolTip(self.currentIndex(),fSpath)
					doc.setModified(False)

	def saveFileAs(self):
		wedit = self.currentWidget()
		doc = wedit.document()
		fSpath,ok = QFileDialog.getSaveFileName(self,"Save File","*.c","*.c")
		if os.path.exists(fSpath):
			open(fSpath,"w").write(wedit.toPlainText())
	def run(self):
		Xpath = self.tabToolTip(self.currentIndex())
		co =  os.system('start %sbuil.py %s '%(self.path_ap,Xpath))
	def compile(self):
		Xpath = self.tabToolTip(self.currentIndex())
		path = re.search(".*(?=/+[A-Za-z0-9_]+\.c)",Xpath)
		Out_name = path.group()+"/"+Xpath.split("/")[-1].split(".")[0]
		os.popen("g++ -o %s %s"%(Out_name,Xpath))
	def open_file_c(self,Xpath):
		self.indexTabs();
		fpath = Xpath.replace("\\","/")
		if os.path.exists(fpath):
			index = self.currentIndex()+1
			fname = fpath.split("/")[-1]
			if not fname in self.DFName and not fpath in self.DFName:
				self.insertTab(index,Edit.Edit(True),fname)
				self.setTabToolTip(index,fpath)
				self.setCurrentIndex(index)
				wedit = self.currentWidget()
				fread = open(fpath,"r").read()
				wedit.setPlainText(fread)
				self.DFName.update({fname:[fpath,index]})
			elif fname in self.DFName and not fpath == self.DFName[fname][0] and not fpath in self.DFName:
				self.insertTab(index,Edit.Edit(True),fpath)
				self.setTabToolTip(index,fpath)
				self.setCurrentIndex(index)
				wedit = self.currentWidget()
				fread = open(fpath,"r").read()
				wedit.setPlainText(fread)
				self.DFName.update({fpath:[fname,index]})
				self.DFName[fname][0]
				self.DFName.update({self.DFName[fname][0]:[fname,self.DFName[fname][1]]})
				self.setCurrentIndex(self.DFName[fname][1])
				self.setTabText(self.currentIndex(),self.DFName[fname][0])
				self.setCurrentIndex(index)
				self.DFName.pop(fname)
			else:
				for i in range(self.count()):
					if fname == self.tabText(i):
						self.setCurrentIndex(i)
						break;
					elif fpath == self.tabText(i):
						self.setCurrentIndex(i)
						break;
	def open_otherFile(self,Xpath):
		self.indexTabs();
		fpath = Xpath.replace("\\","/")
		if os.path.exists(fpath):
			index = self.currentIndex()+1
			fname = fpath.split("/")[-1]
			if not fname in self.DFName and not fpath in self.DFName:
				self.insertTab(index,Edit.Edit(False),fname)
				self.setTabToolTip(index,fpath)
				self.setCurrentIndex(index)
				wedit = self.currentWidget()
				fread = open(fpath,"r").read()
				wedit.setPlainText(fread)
				self.DFName.update({fname:[fpath,index]})
			elif fname in self.DFName and not fpath == self.DFName[fname][0] and not fpath in self.DFName:
				self.insertTab(index,Edit.Edit(False),fpath)
				self.setTabToolTip(index,fpath)
				self.setCurrentIndex(index)
				wedit = self.currentWidget()
				fread = open(fpath,"r").read()
				wedit.setPlainText(fread)
				self.DFName.update({fpath:[fname,index]})
				self.DFName[fname][0]
				self.DFName.update({self.DFName[fname][0]:[fname,self.DFName[fname][1]]})
				self.setCurrentIndex(self.DFName[fname][1])
				self.setTabText(self.currentIndex(),self.DFName[fname][0])
				self.setCurrentIndex(index)
				self.DFName.pop(fname)
			else:
				for i in range(self.count()):
					if fname == self.tabText(i):
						self.setCurrentIndex(i)
						break;
					elif fpath == self.tabText(i):
						self.setCurrentIndex(i)
						break;