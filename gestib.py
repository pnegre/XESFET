# -*- coding: utf-8 -*-

import xml.dom.minidom
import codecs
import re


def createElement(doc,name,content):
	elem = doc.createElement(name)
	elem.appendChild(doc.createTextNode(content))
	return elem


def joinAttrs(element,at1,at2):
	return element.getAttribute(at1) + ' (' + element.getAttribute(at2) + ')'



class ImportGestib:
	def __init__(self,fname):
		self.dom = xml.dom.minidom.parse(fname)
		self.doc = xml.dom.minidom.Document()
		self.root = self.doc.createElement('FET')
		self.root.setAttribute('version','5.11.0')
		self.doc.appendChild(self.root)
		self.otherStuff()
	
	
	def getGroups(self):
		clist = self.dom.getElementsByTagName('CURSOS')[0]
		courses = clist.getElementsByTagName('CURS')
		result = []
		for c in courses:
			result.append(c.getAttribute('descripcio'))
		result.sort()
		return result
	
	
	def getProfs(self):
		plist = self.dom.getElementsByTagName('PLACES')[0]
		profs = plist.getElementsByTagName('PLACA')
		result = [ p.getAttribute('descripcio') for p in profs ]
		result.sort()
		return result
	
	
	def deleteProf(self,prof):
		plist = self.dom.getElementsByTagName('PLACES')[0]
		profs = plist.getElementsByTagName('PLACA')
		for p in profs:
			if p.getAttribute('descripcio') == prof:
				plist.removeChild(p)
	
	
	def deleteCourse(self,course):
		clist = self.dom.getElementsByTagName('CURSOS')[0]
		courses = clist.getElementsByTagName('CURS')
		mlist = self.dom.getElementsByTagName('MATERIES')[0]
		mats = mlist.getElementsByTagName('MATERIA')
		for c in courses:
			name = c.getAttribute('descripcio')
			cod = c.getAttribute('codi')
			if name == course:
				# Eliminem matèries del curs
				for m in mats:
					cod_mat_curs = m.getAttribute('curs')
					if cod == cod_mat_curs:
						mlist.removeChild(m)
				clist.removeChild(c)
	
	
	def parse(self):
		self.doTeachers()
		self.doGroups()
		self.doSubjects()
		self.doActivities()
	
	
	
	def doActivities(self):
		activ_list = self.dom.getElementsByTagName('ACTIVITAT')
		alist = self.doc.createElement('Activity_Tags_List')
		self.root.appendChild(alist)
		for a in activ_list:
			activity = self.doc.createElement('Activity_Tag')
			activity.appendChild(createElement(self.doc,'Name',
				joinAttrs(a,'curta','codi')))
			alist.appendChild(activity)
			
	
	
	def doSubjects(self):
		subjects_list = self.dom.getElementsByTagName('MATERIA')
		slist = self.doc.createElement('Subjects_List')
		self.root.appendChild(slist)
		
		courses_names = {}
		for c in self.dom.getElementsByTagName('CURS'):
			courses_names[c.getAttribute('codi')] = c.getAttribute('descripcio')
		
		for s in subjects_list:
			subject = self.doc.createElement('Subject')
			sname = self.doc.createElement('Name')
			sname.appendChild(self.doc.createTextNode(
				courses_names[s.getAttribute('curs')] + ' ' +
				joinAttrs(s,'descripcio','codi')))
			subject.appendChild(sname)
			slist.appendChild(subject)
	
	
	def doTeachers(self):
		teachers_list = self.dom.getElementsByTagName('PLACA')
		tlist = self.doc.createElement('Teachers_List')
		self.root.appendChild(tlist)
		for t in teachers_list:
			teacher = self.doc.createElement('Teacher')
			teacher.appendChild(createElement(self.doc,'Name',
				joinAttrs(t,'descripcio','codi')
			))
			tlist.appendChild(teacher)


	def doGroups(self):
		course_list = self.dom.getElementsByTagName('CURS')
		slist = self.doc.createElement('Students_List')
		self.root.appendChild(slist)
		year = self.doc.createElement('Year')
		year.appendChild(createElement(self.doc,'Name','any'))
		year.appendChild(createElement(self.doc,'Number_of_Students','0'))
		slist.appendChild(year)
		for c in course_list:
			course = self.doc.createElement('Group')
			course.appendChild(createElement(self.doc,'Number_of_Students','0'))
			course.appendChild(createElement(self.doc,'Name',joinAttrs(c,'descripcio','codi')))
			year.appendChild(course)
			
			for s in c.getElementsByTagName('GRUP'):
				subgroup = self.doc.createElement('Subgroup')
				subgroup.appendChild(createElement(self.doc,'Name',
					c.getAttribute('descripcio') + 
					' ' + joinAttrs(s,'nom','codi')))
				subgroup.appendChild(createElement(self.doc,'Number_of_Students','0'))
				course.appendChild(subgroup)


	def writeToFile(self,fname):
		f = codecs.open(fname, 'w', 'utf-8')
		self.doc.writexml(f)
		f.close()
	
	
	def otherStuff(self):
		#<Time_Constraints_List>
		#<ConstraintBasicCompulsoryTime>
				#<Weight_Percentage>100</Weight_Percentage>
		#</ConstraintBasicCompulsoryTime>
		#</Time_Constraints_List>

		#<Space_Constraints_List>
		#<ConstraintBasicCompulsorySpace>
				#<Weight_Percentage>100</Weight_Percentage>
		#</ConstraintBasicCompulsorySpace>
		#</Space_Constraints_List>
		
		Time_Constraints_List=self.doc.createElement('Time_Constraints_List')
		Space_Constraints_List=self.doc.createElement('Space_Constraints_List')
		self.root.appendChild(Time_Constraints_List)
		self.root.appendChild(Space_Constraints_List)
		
		compTime = self.doc.createElement('ConstraintBasicCompulsoryTime')
		Time_Constraints_List.appendChild(compTime)
		compTime.appendChild(createElement(self.doc,'Weight_Percentage','100'))
		
		compSpace = self.doc.createElement('ConstraintBasicCompulsorySpace')
		Space_Constraints_List.appendChild(compSpace)
		compSpace.appendChild(createElement(self.doc,'Weight_Percentage','100'))

