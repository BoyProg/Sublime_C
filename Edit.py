from PySide.QtGui import *
from PySide.QtCore import *
import syntax,os,re,sys
import numpy as np


class Edit(QPlainTextEdit):
	def __init__(self,file_c):
		super(Edit,self).__init__()
		self.file_c2 = file_c
	########### Setting Edit ###########################
		self.lis = []
		self.path_ap = re.search(r".*(?=/[A-Za-z0-9_].[A-Za-z0-9_])",sys.argv[0].replace("\\","/")).group()+"/"
		self.selectionChanged.connect(self.add_qu)
		font = QFont()
		font.setFamily("Consolas")
		font.setPointSize(11)
		self.setFont(font)
		self.setLineWrapMode(self.NoWrap)
		self.setTabStopWidth(40)
		# Completer Text #
		self.completer = QCompleter(self)
		if self.file_c2:
			li = open(self.path_ap+"key/keyword","r").read().split("\n")
			li.sort()
			self.completer.setModel(QStringListModel(li))
			self.highlighter = syntax.Highlighter(self.document())
			self.completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
			self.completer.setWrapAround(True)
		self.setCompleter(self.completer)
		self.cursorPositionChanged.connect(self.positionInBlock)
		###############################
		self.lineNumberArea = LineNumberArea(self)
		self.connect(self, SIGNAL('blockCountChanged(int)'), self.updateLineNumberAreaWidth)
		self.connect(self, SIGNAL('updateRequest(QRect,int)'), self.updateLineNumberArea)
		self.connect(self, SIGNAL('cursorPositionChanged()'), self.highlightCurrentLine)
		self.updateLineNumberAreaWidth(0)
        ##############################
	#########################################################
	def add_qu(self):
		a = self.createMimeDataFromSelection()
		if  a.text() == "" :
			self.lis.clear()
		else:
			tc = self.textCursor()
			self.lis.append(tc.position())
	# Get postion Cursor in Edit #
	def positionInBlock(self):

		tc1 = self.textCursor()
		return (tc1.position())
	def getText(self):
		return self.toPlainText()

	#Start Setting Tab Spase #
	def textUnderLine(self):
	    tc2 = self.textCursor()
	    tc2.select(tc2.LineUnderCursor)  
	    s = (tc2.selectedText())
	    return s

	def handle(self):
	    import re
	    a_0,a_1 = "",""
	    cursor = self.textCursor()
	    if str(self.textUnderLine()).startswith("\t"):
	        a = re.match("[?=\t]+(?!\t)",self.textUnderLine())
	        a_0 = a.group(0) 
	    
	    if str(self.textUnderLine()).endswith("{") :
	    	if self.getText()[self.positionInBlock()-1] == "{":
	    		a_1 = "\t"
	    self.a = str(a_0+a_1)
	    	
	# End ...................#

	# Split Word From Edit Text and return #
	def textUnderCursor(self):
		tc = self.textCursor()
		tc.select(tc.WordUnderCursor)  
		s = (tc.selectedText())
		reg = re.search(r"(?<=\<).*(?=\>)",self.textUnderLine())
		if reg != None:
			return reg.group()
		else:
			if not self.positionInBlock()-1 == -1:
				if s != ' ' :
					try:
						return s[:s.rindex(self.getText()[self.positionInBlock()-1])+1]
					except:
						return ' '
			else:
				return ' '
	# set Completer setting #
	def setCompleter(self, comp):
		self._c = comp
		comp.setWidget(self)
		comp.popup().setFont(QFont('Consolas',13))
		comp.popup().setStyleSheet("background-color:rgb(255,255,255);color:black")
		comp.setCompletionMode(QCompleter.PopupCompletion)
		comp.activated.connect(self.insertComplet)

    # Insert Complet Word # 
	def insertComplet(self, Textcomplet):
		self.handle()
		textc = self.textCursor()
		if Textcomplet in ["ifndef","define","endif","include"]:
			textc.movePosition(QTextCursor.StartOfWord)
			textc.insertText("#")
			textc.movePosition(QTextCursor.EndOfLine)
		reg = re.search(r"(?<=\<).*(?=\>)",self.textUnderLine())
		if reg != None:
			tc = self.textCursor()
			extra = len(Textcomplet) - len(self._c.completionPrefix())
			tc.movePosition(QTextCursor.Left)
			tc.movePosition(QTextCursor.EndOfWord)
			tc.insertText(Textcomplet[-extra:])
			self.setTextCursor(tc)
		else:
			tc = self.textCursor()
			tc.movePosition(tc.StartOfWord,tc.MoveAnchor)
			tc.select(tc.WordUnderCursor)
			tc.insertText(Textcomplet)
			self.setTextCursor(tc)

		
		if Textcomplet == "if":
			if str(self.textUnderLine()).startswith("\t"):
				textc.movePosition(QTextCursor.EndOfWord)
				textc.insertText("()\n"+self.a+"{\n"+self.a+"\t\n"+self.a+"}")
				textc.movePosition(QTextCursor.EndOfLine)
			else:
				textc.movePosition(QTextCursor.EndOfWord)
				textc.insertText("()\n{\n\t\n}")
				textc.movePosition(QTextCursor.EndOfLine)
		elif Textcomplet == "while":
			if str(self.textUnderLine()).startswith("\t"):
				textc.movePosition(QTextCursor.EndOfWord)
				textc.insertText("()\n"+self.a+"{\n"+self.a+"\t\n"+self.a+"}")
				textc.movePosition(QTextCursor.EndOfLine)
			else:
				textc.movePosition(QTextCursor.EndOfWord)
				textc.insertText("()\n{\n\t\n}")
				textc.movePosition(QTextCursor.EndOfLine)
		elif Textcomplet == "struct":
			if str(self.textUnderLine()).startswith("\t"):
				textc.movePosition(QTextCursor.EndOfWord)
				textc.insertText(" $\n"+self.a+"{\n"+self.a+"\t\n"+self.a+"};")
				textc.movePosition(QTextCursor.EndOfLine)
			else:
				textc.movePosition(QTextCursor.EndOfWord)
				textc.insertText(" $\n{\n\t\n};")
				textc.movePosition(QTextCursor.EndOfLine)
		elif Textcomplet == "switch":
			if str(self.textUnderLine()).startswith("\t"):
				textc.movePosition(QTextCursor.EndOfWord)
				textc.insertText(" ()\n"+self.a+"{\n"+self.a+"case $:\n"+self.a+"\t/*tstatement;*/\n"+self.a+"\tbreak;\n"+self.a+"\tdefault :\n"+self.a+"\t/*tstatement*/\n"+self.a+"}")
				textc.movePosition(QTextCursor.EndOfLine)
			else:
				textc.movePosition(QTextCursor.EndOfWord)#
				textc.insertText(" ()\n\tcase $:\n\t\t/*tstatement;*/\n\t\tbreak;\n\tdefault :\n\t\t/*tstatement*/;\n}")
				textc.movePosition(QTextCursor.EndOfLine)
		elif Textcomplet == "for":
			if str(self.textUnderLine()).startswith("\t"):
				textc.movePosition(QTextCursor.EndOfWord)
				textc.insertText(" (int i = 0; i < count; ++i)\n"+self.a+"{\n"+self.a+"\t\n"+self.a+"}")
				textc.movePosition(QTextCursor.EndOfLine)
			else:
				textc.movePosition(QTextCursor.EndOfWord)#
				textc.insertText(" (int i = 0; i < count; ++i)\n{\n\t\n}")
				textc.movePosition(QTextCursor.EndOfLine)
		elif Textcomplet == "do":
			if str(self.textUnderLine()).startswith("\t"):
				textc.movePosition(QTextCursor.EndOfWord)
				textc.insertText(" \n"+self.a+"{\n"+self.a+"\t\n"+self.a+"}while();")
				textc.movePosition(QTextCursor.EndOfLine)
			else:
				textc.movePosition(QTextCursor.EndOfWord)#
				textc.insertText("\n{\n\t\n}while();")
				textc.movePosition(QTextCursor.EndOfLine)
		elif Textcomplet == "main":
			if str(self.textUnderLine()).startswith("\t"):
				textc.movePosition(QTextCursor.StartOfLine)
				textc.insertText(self.a+"int ")
				textc.movePosition(QTextCursor.EndOfLine)
				textc.insertText("(int argc, char const *argv[])\n"+self.a+"{\n"+self.a+"\t\n"+self.a+"}")
				textc.movePosition(QTextCursor.EndOfLine)
			else:
				textc.movePosition(QTextCursor.StartOfLine)
				textc.insertText(self.a+"int ")
				textc.movePosition(QTextCursor.EndOfLine)
				textc.insertText("(int argc, char const *argv[])\n{\n\t\n}")
				textc.movePosition(QTextCursor.EndOfLine)

	# Get Key Press From KeyBored #
	def keyPressEvent(self, e):
		cursor = self.textCursor()
		if self._c is not None and self._c.popup().isVisible():
			if e.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab,Qt.Key_Backtab):
				e.ignore()
				return
		if self.file_c2:
			import re
			if not re.search(r"\#include+[\s]+(?=\<)",self.textUnderLine()) == None:
				self.completer.setModel(QStringListModel(open("key/keylib","r").read().split("\n")))
			else:
				self.completer.setModel(QStringListModel(open("key/keyword","r").read().split("\n")))

		isShortcut = ((e.modifiers() & Qt.ControlModifier) != 0 and e.key() == Qt.Key_E)
		if self._c is None or not isShortcut:
			if e.key() == Qt.Key_Return:
				self.handle()
				if str(self.textUnderLine()).endswith("{"):
					cursor.insertText("\n"+self.a)
				elif str(self.textUnderLine()).endswith("("):
					cursor.insertText("\n"+self.a)
				elif str(self.textUnderLine()).startswith("\t"):
					cursor.insertText("\n"+self.a)
				else:
					super().keyPressEvent(e)
			else:
				if e.text() == "'":
					if self.lis != []:
						if self.lis[0]-1 < self.lis[-1]+1 :
							cursor.setPosition(self.lis[0]-1);cursor.insertText("'")
							cursor.setPosition(self.lis[-1]+1);cursor.insertText("'")
						elif self.lis[0]-1 > self.lis[-1]+1 :
							cursor.setPosition(self.lis[0]+1);cursor.insertText("'")
							cursor.setPosition(self.lis[-1]);cursor.insertText("'")
					else:
						super().keyPressEvent(e)
					self.lis.clear()
				elif e.text() == '"':
						if self.lis != []:
							if self.lis[0]-1 < self.lis[-1]+1 :
								cursor.setPosition(self.lis[0]-1);cursor.insertText('"')
								cursor.setPosition(self.lis[-1]+1);cursor.insertText('"')
							elif self.lis[0]-1 > self.lis[-1]+1 :
								cursor.setPosition(self.lis[0]+1);cursor.insertText('"')
								cursor.setPosition(self.lis[-1]);cursor.insertText('"')
						else:
							super().keyPressEvent(e)
						self.lis.clear()
				elif e.text() == '(' or e.text() == ')':
						if self.lis != []:
							if self.lis[0]-1 < self.lis[-1]+1 :
								cursor.setPosition(self.lis[0]-1);cursor.insertText('(')
								cursor.setPosition(self.lis[-1]+1);cursor.insertText(')')
							elif self.lis[0]-1 > self.lis[-1]+1 :
								cursor.setPosition(self.lis[0]+1);cursor.insertText(')')
								cursor.setPosition(self.lis[-1]);cursor.insertText('(')
						else:
							super().keyPressEvent(e)
						self.lis.clear()
				else:
				   super().keyPressEvent(e)

		ctrlOrShift = e.modifiers() & (Qt.ControlModifier |Qt.ShiftModifier)
		if self._c is None or (ctrlOrShift and len(e.text()) == 0):
			return

		if e.text() == "{":	
			cursor.insertText("}")
		if e.text() == "[":
			cursor.insertText("]")

		eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="
		hasModifier = (e.modifiers() != Qt.NoModifier) and not ctrlOrShift
		completionPrefix = self.textUnderCursor()

		if not isShortcut and (hasModifier or len(e.text()) == 0 or len(completionPrefix) < 1 or e.text()[-1] in eow):
			self._c.popup().hide()
			return

		if completionPrefix != self._c.completionPrefix():
			self._c.setCompletionPrefix(completionPrefix)
			self._c.popup().setCurrentIndex(
			self._c.completionModel().index(0, 0))

		cr = self.cursorRect()
		cr.setWidth(self._c.popup().sizeHintForColumn(0) + self._c.popup().verticalScrollBar().sizeHint().width())
		self._c.complete(cr)



	##############################################

	def lineNumberAreaWidth(self):
	    """ This method has been slightly modified (use of log and uses actual
	    font rather than standart.) """
	    n_lines = self.blockCount()
	    digits = np.ceil(np.log10(n_lines)) + 1
	    return digits * QFontMetrics(self.font()).width('9') + 3


	def updateLineNumberAreaWidth(self, _):
		self.setViewportMargins(45,0, 0, 0)


	def updateLineNumberArea(self, rect, dy):
	    

	    if dy:
	    	self.lineNumberArea.scroll(0, dy)
	    else:

	        self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(),rect.height())

	    
	    if rect.contains(self.viewport().rect()):
	        self.updateLineNumberAreaWidth(0)


	def resizeEvent(self, event):
	    super().resizeEvent(event)

	    cr = self.contentsRect();
	    self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),40, cr.height()))

	def lineNumberAreaPaintEvent(self, event):
	    
	    painter = QPainter(self.lineNumberArea)
	    painter.setFont(QFont("Consolas",11))
	    painter.fillRect(event.rect(), QColor(39,40,34))#

	    block = self.firstVisibleBlock()
	    blockNumber = block.blockNumber()
	    top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
	    bottom = top + self.blockBoundingRect(block).height()

	    # Just to make sure I use the right font
	    height = QFontMetrics(self.font()).height()
	    while block.isValid() and (top <= event.rect().bottom()):
	        if block.isVisible() and (bottom >= event.rect().top()):
	            number = str(blockNumber + 1)
	            painter.setPen(QColor(143,144,138));
	            painter.drawText(1, top,30, height,
	                             Qt.AlignRight, number)

	        block = block.next()
	        top = bottom
	        bottom = top + self.blockBoundingRect(block).height()
	        blockNumber += 1


	def highlightCurrentLine(self):
	    extraSelections = []

	    if not self.isReadOnly():
	        selection = QTextEdit.ExtraSelection()

	        lineColor = QColor(Qt.black).lighter(160)

	        selection.format.setBackground(lineColor)
	        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
	        selection.cursor = self.textCursor()
	        selection.cursor.clearSelection()
	        extraSelections.append(selection)
	    self.setExtraSelections(extraSelections)

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor


    def sizeHint(self):
        return Qsize(self.editor.lineNumberAreaWidth(), 0)


    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)