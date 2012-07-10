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
	
	
	def log(self,string):
		self.ui.console.append(string)
	
	
	def deleteCourses(self):
		clist = self.ui.courseList.selectedItems()
		for c in clist:
			self.importGestib.deleteCourse(unicode(c.text()))
			self.ui.courseList.takeItem(self.ui.courseList.row(c))
			self.log("Eliminat curs " + c.text())
	
	
	def deleteProfs(self):
		plist = self.ui.profList.selectedItems()
		for p in plist:
			self.importGestib.deleteProf(unicode(p.text()))
			self.ui.profList.takeItem(self.ui.profList.row(p))
			self.log("Eliminat professor " + p.text())
	
	
	def updateButtons(self):
		if self.importGestib:
			self.ui.but_import_gestib.setEnabled(1)
			self.ui.but_export_fet.setEnabled(1)
			self.ui.but_delete_courses.setEnabled(1)
			self.ui.but_delete_profs.setEnabled(1)
		else:
			self.ui.but_import_gestib.setEnabled(1)
			self.ui.but_export_fet.setEnabled(0)
			self.ui.but_delete_courses.setEnabled(0)
			self.ui.but_delete_profs.setEnabled(0)
	
	
	def doImportGestib(self):
		self.importGestib = None
		filename = QtGui.QFileDialog.getOpenFileName(self,
			QtCore.QString("Fitxer gestib"), QtCore.QString(), "XML files (*.xml)")
		
		if filename == '': 
			self.updateButtons()
			return
		
		try:
			self.importGestib = ImportGestib(unicode(filename))
			self.log('Fitxer ' + filename + ' carregat correctament')
			self.updateButtons()
			
			groups = self.importGestib.getGroups()
			for g in groups:
				self.ui.courseList.addItem(g)
			
			profs = self.importGestib.getProfs()
			for p in profs:
				self.ui.profList.addItem(p)
		
		except:
			msgbox = QtGui.QMessageBox( self )
			msgbox.setText( "Error: %s" % sys.exc_info()[0] )
			msgbox.setModal( True )
			ret = msgbox.exec_()
	
	
	def doExportFet(self):
		filename = QtGui.QFileDialog.getSaveFileName(self,
			QtCore.QString("Fitxer FET"), QtCore.QString(), "XML FET (*.fet)")
		
		if filename == '':
			return
		
		try:
			fn = unicode(filename)
			self.importGestib.parse()
			self.importGestib.writeToFile(fn)
			self.log('Fitxer ' + fn + ' exportat correctament')
		except:
			msgbox = QtGui.QMessageBox( self )
			msgbox.setText( "Error: %s" % sys.exc_info()[0] )
			msgbox.setModal( True )
			ret = msgbox.exec_()
			




if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	mainWin = MainWindow()
	mainWin.show()
	app.exec_()


