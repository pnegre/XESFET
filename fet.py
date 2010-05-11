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
		
		self.connect(self.ui.but_import_gestib,
			QtCore.SIGNAL("clicked()"), self.doImportGestib)
		
		self.connect(self.ui.but_export_fet,
			QtCore.SIGNAL("clicked()"), self.doExportFet)
	
	
	def doImportGestib(self):
		filename = QtGui.QFileDialog.getOpenFileName(self)
		dom = parse(str(filename))
		
		teachers = dom.getElementsByTagName('PLACA')
		courses = dom.getElementsByTagName('CURS')
		mats = dom.getElementsByTagName('MATERIA')
		acts = dom.getElementsByTagName('ACTIVITAT')
		
		g = ExportGestib()
		g.doTeachers(teachers)
		g.doGroups(courses)
		g.doSubjects(mats)
		g.doActivities(acts)
		
		self.importGestib = g
		self.ui.console.append('Fitxer ' + filename + ' carregat correctament')
	
	
	def doExportFet(self):
		filename = QtGui.QFileDialog.getOpenFileName(self)
		fn = str(filename)
		self.importGestib.writeToFile(fn)
		self.ui.console.append('Fitxer ' + fn + ' Exportat correctament')
		




if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	mainWin = MainWindow()
	mainWin.show()
	app.exec_()


