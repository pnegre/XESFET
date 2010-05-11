#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.dom.minidom import parse, parseString

import gestib

def main():
	dom = parse("gestib.xml")

	teachers = dom.getElementsByTagName('PROFESSOR')
	subjects = dom.getElementsByTagName('SUBMATERIES')[0].getElementsByTagName('SUBMATERIA')
	courses = dom.getElementsByTagName('CURS')
	
	gestib.exportGestib(teachers,subjects,courses)


main()