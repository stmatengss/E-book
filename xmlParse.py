try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

import sys

class XmlParse:
	'''parse xml'''
	
	#-------------basic----------------#
	def open(self, path):
		try:
			self.tree = ET.parse(path)
			self.root = self.tree.getroot()
		except Exception, e:
			print 'Error: Cannot parse file:'+path
	
	def write(self, path):
		self.tree.write(path)
		
	#-------------search---------------#
	def find_nodes(self, node, path):
		if node is None:
			return []
		
		return node.findall(path)
	
	def find_node_by_attr(self, node, path, match):
		nodes = self.find_nodes(node, path)
		
		selected = None
		for node in nodes:
			if node.get(match["attr"]) == str(match["val"]):
				selected = node
				break
		
		return selected
		
	#-------------change---------------#
	def create_node(self, tag, property, content):
		element = ET.Element(tag, property)
		element.text = content
		return element
	
	def append_node(self, node, element):
		node.append(element)

	def insert_node(self, node, index, element):
		node.insert(index, element)
	
	def change_node_text(self, node, text):
		node.text = text

	def remove_nodes(self, parent):
		if parent is not None:
			parent.clear()

	def remove_node(self, parent, node):
		if parent is not None:
			parent.remove(node)
		