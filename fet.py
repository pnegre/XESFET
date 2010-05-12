#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtCore, QtGui, uic
from xml.dom.minidom import parse, parseString
from gestib import ImportGestib



class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.ui = uic.loadUi("mainwindow.ui",self)
		
		self.connect(self.ui.but_import_gestib,
			QtCore.SIGNAL("clicked()"), self.doImportGestib)
		
		self.connect(self.ui.but_export_fet,
			QtCore.SIGNAL("clicked()"), self.doExportFet)
		
		self.importGestib = None
		self.updateButtons()
	
	
	def updateButtons(self):
		if self.importGestib:
			self.ui.but_import_gestib.setEnabled(1)
			self.ui.but_export_fet.setEnabled(1)
		else:
			self.ui.but_import_gestib.setEnabled(1)
			self.ui.but_export_fet.setEnabled(0)
	
	
	def doImportGestib(self):
		self.importGestib = None
		filename = QtGui.QFileDialog.getOpenFileName(self,
			QtCore.QString("Fitxer gestib"), QtCore.QString(), "XML files (*.xml)")
		
		if filename == '': 
			self.updateButtons()
			return
		
		try:
			dom = parse(str(filename))
			
			teachers = dom.getElementsByTagName('PLACA')
			courses = dom.getElementsByTagName('CURS')
			mats = dom.getElementsByTagName('MATERIA')
			acts = dom.getElementsByTagName('ACTIVITAT')
			
			g = ImportGestib()
			g.doTeachers(teachers)
			g.doGroups(courses)
			g.doSubjects(mats)
			g.doActivities(acts)
			
			self.importGestib = g
			self.ui.console.append('Fitxer ' + filename + ' carregat correctament')
			self.updateButtons()
		except:
			msgbox = QtGui.QMessageBox( self )
			msgbox.setText( "Error" )
			msgbox.setModal( True )
			ret = msgbox.exec_()
	
	
	def doExportFet(self):
		filename = QtGui.QFileDialog.getOpenFileName(self,
			QtCore.QString("Fitxer FET"), QtCore.QString(), "XML FET (*.fet)")
		
		if filename == '':
			return
		
		try:
			fn = str(filename)
			self.importGestib.writeToFile(fn)
			self.ui.console.append('Fitxer ' + fn + ' Exportat correctament')
		except:
			msgbox = QtGui.QMessageBox( self )
			msgbox.setText( "Error" )
			msgbox.setModal( True )
			ret = msgbox.exec_()
			




if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	mainWin = MainWindow()
	mainWin.show()
	app.exec_()


