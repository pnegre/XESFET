#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtCore, QtGui, uic
from xml.dom.minidom import parse, parseString
from gestib import ExportGestib



class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.ui = uic.loadUi("mainwindow.ui",self)
		
		self.connect(self.ui.but_import,
			QtCore.SIGNAL("clicked()"), self.doStuff)
	
	
	def doStuff(self):
		filename = QtGui.QFileDialog.getOpenFileName(self)
		print filename
		dom = parse("gestib.xml")
		
		teachers = dom.getElementsByTagName('PLACA')
		courses = dom.getElementsByTagName('CURS')
		mats = dom.getElementsByTagName('MATERIA')
		acts = dom.getElementsByTagName('ACTIVITAT')
		
		g = ExportGestib(fname="exportacioFET.fet")
		g.doTeachers(teachers)
		g.doGroups(courses)
		g.doSubjects(mats)
		g.doActivities(acts)
		
		self.ui.console.setText('Fitxer ' + filename + ' carregat correctament')
		
		g.writeToFile()




def main():
	app = QtGui.QApplication(sys.argv)
	mainWin = MainWindow()
	mainWin.show()
	app.exec_()

main()