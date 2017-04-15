#########################
# SyntaxHighlighter  ####
####             ########

from PySide.QtGui import *
from PySide.QtCore import *

class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        keyword = QTextCharFormat()# color red
        self.keywords =["default","static","sizeof","continue",
                        "goto","extern","case","break","register","return",
                        "const","while","if","else","do","switch","for"]
        keyword.setForeground(QColor(249,38,89))
        keywordPatterns = self.keywords#open("keyword",'r').read().split("\n")

        operators = ['=','==', '!=', '<', '<=', '>', '>=','\+',
                    '-', '\*', '/', '//', '\%', '\*\*','\+=', '-=',
                    '\*=', '/=', '\%=','\^', '\|', '\&','\~','>>', '<<',]
        

        self.highlightingRules = [(QRegExp("\\b"+pattern+"\\b"), keyword)
                for pattern in keywordPatterns]
        [self.highlightingRules.append((QRegExp(r"%s"%o),keyword))for o in operators]


        keymain = QTextCharFormat()
        keymain.setForeground(QColor(166,198,40))
        self.highlightingRules.append((QRegExp("\\bmain\\b"),keymain))

        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(QColor(117,113,84))
        

        quotation = QTextCharFormat()
        quotation.setForeground(QColor(200,219,116))
        regu = r'(\br|u|ur|R|U|UR|Ur|uR|b|B|br|Br|bR|BR|rb|rB|Rb|RB)?'
        self.highlightingRules.append((QRegExp(regu+r'"[^"\\\n]*(\\.[^"\\\n]*)*"?'),
                quotation))
        self.highlightingRules.append((QRegExp(regu+r"'[^'\\\n]*(\\.[^'\\\n]*)*'?"),
                quotation))
        self.highlightingRules.append((QRegExp(regu+r"'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?"),
                quotation))
        self.highlightingRules.append((QRegExp(regu+r'"""[^"\\]*((\\.|"(?!""))[^"\\]*)*(""")?'),
                quotation))


        funct = QTextCharFormat()
        funct.setFontItalic(True)
        lis = ["scanf","printf","fopen","int","float","char","double","short","long","struct","enum","void","auto","typedef","union","unsigned","signed"]
        funct.setForeground(QColor(102,217,239))
        [self.highlightingRules.append((QRegExp("\\b%s\\b"%k),funct))for k in lis]


        number = QTextCharFormat()
        number.setFontItalic(True)
        number.setForeground(QColor(174,129,255))
        self.highlightingRules.append((QRegExp(r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b'),
               number))

        self.commentStartExpression = QRegExp("/\\*")
        self.commentEndExpression = QRegExp("\\*/")
        self.rs = []
                


    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        import re
        if text.startswith("#"):
            if len(text.rpartition("#")[0]) == 0:
                reg = re.search(r"(include|ifndef|define|endif)+(?![A-Za-z0-9_-|\-/\"!=@#$%^&*()_+~`<>?.,:\\;'\}\[\]])",text)
                if reg != None:
                    funInclude = QTextCharFormat()
                    funInclude.setForeground(QColor(249,38,89))
                    index = reg.span()[0]
                    while index >=0:
                        length = reg.span()[1]-1
                        self.setFormat(index,length,funInclude)
                        index = expression.indexIn(text,index + length)

        if text.startswith("#include"):
            reg = re.search(r"(?<=#include)[\s]<[^'\\]*(\\.[^'\\]*)*(?=[\>]).",text)
            if reg != None:
                quotation = QTextCharFormat()
                quotation.setForeground(QColor(200,219,116))
                index = reg.span()[1] - len(reg.group().strip())
                while index >=0:
                    length = reg.span()[1]-9
                    self.setFormat(index,length,quotation)
                    index = expression.indexIn(text,index + length)

        reg = re.search(r"//[^\n]*",text)
        if reg != None:
            index = reg.span()[0]
            while index >=0:
                length = reg.span()[1]
                self.setFormat(index,length,self.multiLineCommentFormat)
                index = expression.indexIn(text,index + length) 

        self.setCurrentBlockState(0)
        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength,
                    self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text,
                    startIndex + commentLength);