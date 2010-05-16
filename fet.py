#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtCore, QtGui, uic
from gestib import ImportGestib



class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.ui = uic.loadUi("mainwindow.ui",self)
		
		self.connect(self.ui.but_import_gestib,
			QtCore.SIGNAL("clicked()"), self.doImportGestib)
		
		self.connect(self.ui.but_export_fet,
			QtCore.SIGNAL("clicked()"), self.doExportFet)
		
		self.connect(self.ui.but_delete_courses,
			QtCore.SIGNAL("clicked()"), self.deleteCourses)
		
		self.connect(self.ui.but_delete_profs,
			QtCore.SIGNAL("clicked()"), self.deleteProfs)
		
		self.importGestib = None
		self.updateButtons()
	
	
	
	def deleteCourses(self):
		item = self.ui.courseList.currentItem()
		if item:
			self.importGestib.deleteCourse(unicode(item.text()))
			self.ui.courseList.takeItem(self.ui.courseList.currentRow())
	
	
	def deleteProfs(self):
		item = self.ui.profList.currentItem()
		if item:
			self.importGestib.deleteProf(unicode(item.text()))
			self.ui.profList.takeItem(self.ui.profList.currentRow())
	
	
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
			self.importGestib = ImportGestib()
			self.importGestib.parse(str(filename))
			self.ui.console.append('Fitxer ' + filename + ' carregat correctament')
			self.updateButtons()
			
			groups = self.importGestib.getGroups()
			for g in groups:
				self.ui.courseList.addItem(g)
			
			profs = self.importGestib.getProfs()
			for p in profs:
				self.ui.profList.addItem(p)
		
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
			self.ui.console.append('Fitxer ' + fn + ' exportat correctament')
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


