# -*- coding: utf-8 -*-

import xml.dom.minidom
import codecs


def createElement(doc,name,content):
	elem = doc.createElement(name)
	elem.appendChild(doc.createTextNode(content))
	return elem




class ExportGestib:
	def __init__(self):
		self.doc = xml.dom.minidom.Document()
		self.root = self.doc.createElement("FET")
		self.root.setAttribute("version","5.11.0")
		self.doc.appendChild(self.root)
	
	
	def doActivities(self,activ_list):
		alist = self.doc.createElement("Activity_Tags_List")
		self.root.appendChild(alist)
		for a in activ_list:
			activity = self.doc.createElement("Activity_Tag")
			activity.appendChild(createElement(self.doc,"Name",a.getAttribute('curta')))
			alist.appendChild(activity)
			
	
	
	def doSubjects(self,subjects_list):
		slist = self.doc.createElement("Subjects_List")
		self.root.appendChild(slist)
		
		for s in subjects_list:
			subject = self.doc.createElement("Subject")
			sname = self.doc.createElement("Name")
			sname.appendChild(self.doc.createTextNode(s.getAttribute('curta')
				+' '+ '('+s.getAttribute('codi')+')'))
			subject.appendChild(sname)
			slist.appendChild(subject)
	
	
	def doTeachers(self,teachers_list):
		tlist = self.doc.createElement("Teachers_List")
		self.root.appendChild(tlist)
		for t in teachers_list:
			teacher = self.doc.createElement("Teacher")
			teacher.appendChild(createElement(self.doc,"Name",
				t.getAttribute("descripcio") + ' ' + '('+t.getAttribute("codi")+')'
			))
			tlist.appendChild(teacher)


	def doGroups(self,course_list):
		slist = self.doc.createElement("Students_List")
		self.root.appendChild(slist)
		year = self.doc.createElement("Year")
		year.appendChild(createElement(self.doc,"Name","any"))
		year.appendChild(createElement(self.doc,"Number_of_Students","0"))
		slist.appendChild(year)
		for c in course_list:
			course = self.doc.createElement("Group")
			course.appendChild(createElement(self.doc,"Number_of_Students","0"))
			course.appendChild(createElement(self.doc,"Name",c.getAttribute("descripcio")))
			year.appendChild(course)
			
			for s in c.getElementsByTagName('GRUP'):
				subgroup = self.doc.createElement("Subgroup")
				subgroup.appendChild(createElement(self.doc,"Name",c.getAttribute("descripcio") + 
					' ' + s.getAttribute("nom") + ' ('+s.getAttribute("codi")+')'))
				subgroup.appendChild(createElement(self.doc,"Number_of_Students","0"))
				course.appendChild(subgroup)


	def writeToFile(self,fname):
		f = codecs.open(fname, "w", "utf-8")
		self.doc.writexml(f)
		f.close()



