import xmlParse

path = "data/settings.xml"
data = xmlParse.XmlParse()
data.open(path)
		
#insert to settings.xml
node   = data.create_node("item", {"line": "0", "seq": "03"}, "")
print node.get("line"), node.get("seq")
parent = data.find_node_by_id(data.root, "page", 1)
print parent.get("id")
data.append_node(parent, node)
data.write(path)