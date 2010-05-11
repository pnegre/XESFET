# -*- coding: utf-8 -*-

import xml.dom.minidom
import codecs


def createElement(doc,name,content):
	elem = doc.createElement(name)
	elem.appendChild(doc.createTextNode(content))
	return elem


def exportGestib(teachers_list,subjects_list,course_list):
	doc = xml.dom.minidom.Document()
	root = doc.createElement("FET")
	root.setAttribute("version","5.11.0")
	doc.appendChild(root)
	Teachers_List = doc.createElement("Teachers_List")
	Students_List = doc.createElement("Students_List")
	Activity_Tags_List = doc.createElement("Activity_Tags_List")
	Subjects_List = doc.createElement("Subjects_List")
	root.appendChild(Teachers_List)
	root.appendChild(Students_List)
	root.appendChild(Activity_Tags_List)
	root.appendChild(Subjects_List)
	
	for t in teachers_list:
		teacher = doc.createElement("Teacher")
		tname = doc.createElement("Name")
		tname.appendChild(doc.createTextNode(t.getAttribute('nom') + ' ' +
			t.getAttribute('ap1') +' '+ t.getAttribute('ap2')))
		teacher.appendChild(tname)
		Teachers_List.appendChild(teacher)
	
	for s in subjects_list:
		subject = doc.createElement("Subject")
		sname = doc.createElement("Name")
		sname.appendChild(doc.createTextNode(s.getAttribute('descripcio')
			+' '+ s.getAttribute('codi')))
		subject.appendChild(sname)
		Subjects_List.appendChild(subject)
		
	#<Students_List>
	#<Year>
	#<Name>aa</Name>
	#<Number_of_Students>0</Number_of_Students>
			#<Group>
			#<Name>1erESO</Name>
			#<Number_of_Students>0</Number_of_Students>
					#<Subgroup>
					#<Name>A</Name>
					#<Number_of_Students>0</Number_of_Students>
					#</Subgroup>
					#<Subgroup>
					#<Name>B</Name>
					#<Number_of_Students>0</Number_of_Students>
					#</Subgroup>
			#</Group>
	#</Year>
	year = doc.createElement("Year")
	Students_List.appendChild(year)
	yname = doc.createElement("Name")
	yname.appendChild(doc.createTextNode("any"))
	year.appendChild(yname)
	nstud = doc.createElement("Number_of_Students")
	nstud.appendChild(doc.createTextNode("0"))
	year.appendChild(nstud)
	for c in course_list:
		course = doc.createElement("Group")
		nstud = doc.createElement("Number_of_Students")
		nstud.appendChild(doc.createTextNode("0"))
		course.appendChild(nstud)
		cname = doc.createElement("Name")
		cname.appendChild(doc.createTextNode(c.getAttribute("descripcio")))
		course.appendChild(cname)
		
		subgroups = c.getElementsByTagName('GRUP')
		for s in subgroups:
			subgroup = doc.createElement("Subgroup")
			nsub = createElement(doc,"Name",s.getAttribute("nom"))
			subgroup.appendChild(nsub)
			subgroup.appendChild(createElement(doc,"Number_of_Students","0"))
			course.appendChild(subgroup)
		
		year.appendChild(course)
	

	
	f = codecs.open("exportacioFET.fet", "w", "utf-8")
	doc.writexml(f)
	f.close()