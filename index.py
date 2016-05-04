#-*- coding: UTF-8 -*- 
import web
import json
import xmlParse
import pdfPrint
from web.contrib.template import render_jinja
from bs4 import BeautifulSoup
import sys
import codecs

reload(sys)  
sys.setdefaultencoding('utf8') 

blank_temple="""
<!doctype html>
<html>
<head lang="en" slick-uniqueid="3">
    <meta charset="utf-8">
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
    <meta name="renderer" content="webkit">
    <meta name="Keywords" content="">
    <meta name="Description" content="">
    <title>EBook</title>
    <!-- css files -->
    <link type="text/css" rel="stylesheet" href="../static/css/font-awesome.min.css">
    <link type="text/css" rel="stylesheet" href="../static/css/font-awesome-ie7.min.css">
    <link type="text/css" rel="stylesheet" href="../static/css/cover.css">
    
    <!-- lib js files -->
    <script type="text/javascript" src="../static/js/lib/jquery.min.js"></script>
    <script type="text/javascript" src="../static/js/lib/jquery.ui.min.js"></script>
    <script type="text/javascript" src="../static/js/lib/jquery.fileupload.js"></script>
    <script type="text/javascript" src="../static/js/lib/jquery.uploadify.js"></script>
    <script type="text/javascript" src="../static/js/lib/math.json2.js"></script>
    <script type="text/javascript" src="../static/js/lib/jquery.jstorage.js"></script>
    
    <script type="text/javascript" src="../static/js/common.tools.js"></script>
    <script type="text/javascript" src="../static/js/webSDK.js"></script>
    <script type="text/javascript" src="../static/js/cover.js"></script>
    
</head>
<body>
    <div id="loading" tabindex="-1" unselectable="on" style="z-index: 99999999; display: none;">
        <div class="loading-mask" tabindex="-1" unselectable="on"></div>
        <div class="loading-state" style="">
            <div class="loading-text">正在生成中，请稍等</div>
        </div>
    </div>
    <!--div class="print">
        <i class="fa fa-arrow-circle-down"></i>
    </div-->
    <div class="container">
        <!--div class="subject"><strong>THE DEVOTION OF SUSPECT X</strong></div-->
        <!--div class="author"><strong>KEIGO HIGASHINO</strong></div-->
		<div class="subject" style="position:absolute; left:0px; top:0px;"><img src="../static/img/wtf.png" /></div>
        <div class="footer">
            <div class="book-info">
                <div class="item">嫌疑人X的献身</div>
                <div class="item">东野圭吾</div>
                <div class="item">THE DEVOTION OF SUSPECT X</div>
                <div class="item">KEIGO HIGASHINO</div>
            </div>
            <div class="book-version">
                <div class="item" id="reader">Version: 2016.No.{reader}</div>
                <div class="item" id="barrage">Barrage: {barrage}</div>
                <div class="item">Size: 1536&times;1040px</div>

            </div>
        </div>
    </div>
     <div class="item website" style="position:absolute; left: 845px; bottom: 24px; font-family: courier ;font-size:12px;"></div>
</body>

</html>
"""

render = render_jinja("templates", encoding="utf-8")

urls = (
	'/', 		       	'Index',
	'/(\d+)',	   		'Page',
	'/(\d+)/settings',	'PageSettings',
	'/(\d+)/comments',	'PageComments',
	'/(\d+)/updates', 	'PageUpdates',
	'/print',			'Print',
	'/download',    'Down'
)

def setChanged(id):
	path = "data/settings.xml"
	data = xmlParse.XmlParse()
	data.open(path)
	
	#if id[0]=='0':
	#	id = id[1:]
	#	if id[1] =='0':
	#		id = id[1:]
	
	page = data.find_node_by_attr(data.root, "page", {"attr":"id", "val": id})
	page.set("change", "0")
	data.write(path)
	
class Index:
	def GET(self):
		path = "data/comments.xml"
		#path2 = "data/settings.xml"
		data = xmlParse.XmlParse()
		data.open(path)
		
		#update reader and read reader & barrage
		reader = data.root.get('reader');
		print "Log Message(reader)::",reader
		data.root.set("reader", str(int(reader)+1))
		barrage = data.root.get('barrage');
		print "Log Message(barrage)::",barrage
		
		res=blank_temple.format(reader=reader, barrage=barrage);
		
		#fi=codecs.open('templates/cover.html','r','utf-8')
		#soup=BeautifulSoup(fi,"html.parser")
		#r=soup.find_all("div", id="reader")
		#print "Log::",r
		#r[0].string=reader
		#b=soup.find_all("div", id="barrage")
		#print "Log::",b
		#b[0].string=barrage
		#fi.close()
		
		fi=codecs.open('templates/cover.html','w','utf-8')
		fi.write(res)
		fi.close()
		
		data.write(path)
		return res;
		#return render.cover()

		
class Page:
	def GET(self, id):
		return getattr(render, id)()

class PageSettings:
	def GET(self, id):
		data = xmlParse.XmlParse()
		data.open("data/settings.xml")
		selected = data.find_node_by_attr(data.root, "page", {"attr":"id", "val": id})
		items = []
		
		nodes = data.find_nodes(selected, "item")
		for item in nodes:
			setting = {
				'line': item.get("line"),
				'seq' : item.get("seq"),
				'top' : item.get("top"),
				'left': item.get("left")
			}
			items.append(setting)
			
		return json.dumps(items)
	
	def POST(self, id):
		path = "data/settings.xml"
		data = xmlParse.XmlParse()
		data.open(path)
		params = web.input(line=0, seq='', top=0, left=0)
		
		#insert to settings.xml
		node   = data.create_node("item", {
			"line": params.line,
			"seq" : params.seq,
			"top" : params.top,
			"left": params.left},"")

		parent = data.find_node_by_attr(data.root, "page", {"attr":"id", "val": id})
		data.append_node(parent, node)
		data.write(path)
		
		settings = {
			'line' : node.get("line"),
			'seq'  : node.get("seq")
		}
		return json.dumps(settings)

class PageComments:
	def GET(self, id):
		path = "data/comments.xml"
		data = xmlParse.XmlParse()
		data.open(path)
		page  = data.find_node_by_attr(data.root, "page", {"attr":"id", "val": id})
		
		lines = data.find_nodes(page, "line")
		
		comments = []
		for line in lines:
			comment = {
				'lid' : line.get('id'),
				'sub' : line.get('sub'),
				'dist': line.get('dist'),
				'content' : line.text
			}
			comments.append(comment)
		return json.dumps(comments)
	
	def POST(self, id):
		form = web.input()
		
		path = "data/comments.xml"
		#path2 = "data/settings.xml"
		data = xmlParse.XmlParse()
		data.open(path)
		#data2 = xmlParse.XmlParse()
		#data2.open(path2)  #
		
		page = data.find_node_by_attr(data.root, "page", {"attr":"id", "val": id})
		
		#update barrage
		barrage = data.root.get('barrage');
		print "Log Message(barrage)::",barrage
		data.root.set("barrage", str(int(barrage)+1))
		
		#if not find create
		if page is None:
			page = data.create_node("page", { "id": str(id) }, "")
			data.append_node(data.root, page)

		node = data.create_node("line", {"id": form['lid'], "dist": form['dist'], "sub": form['sub']}, form['content'])
		data.insert_node(page, 0, node)

		#update sub value
		subs = json.loads(form['subs'])
		for sub in subs:
			item = data.find_node_by_attr(page, "line", {"attr":"id", "val":sub['lid']})
			if item is not None:
				item.set("sub", str(sub['sub']))

		data.write(path)
		#update settings change
		setChanged(id)

		settings = {
			'lid' : node.get('lid')
		}
		return json.dumps(settings)

class PageUpdates:
	def POST(self,id):

		form = web.input()
		
		path = "data/comments.xml"
		data = xmlParse.XmlParse()
		data.open(path)
		
		#update barrage
		barrage = data.root.get('barrage');
		print "Log Message::",barrage
		data.root.set("barrage", str(int(barrage)+1))
		
		page = data.find_node_by_attr(data.root, "page", {"attr":"id", "val": id})
		node = data.find_node_by_attr(page, "line", {"attr":"id", "val":form['lid']})
		
		data.change_node_text(node, form['content'])

		#move node to first
		newNode = data.create_node("line", {
			"id": node.get("id"),
			"dist": node.get('dist'),
			"sub": node.get('sub')},
			node.text)
		data.insert_node(page, 0, newNode)
		data.remove_node(page, node)

		#update sub value
		subs = json.loads(form['subs'])
		for sub in subs:
			item = data.find_node_by_attr(page, "line", {"attr":"id", "val":sub['lid']})
			if item is not None:
				item.set("sub", str(sub['sub']))
		
		data.write(path)

		#update settings change
		setChanged(id)
		
		settings = {
			'lid' : node.get('lid')
		}
		return json.dumps(settings)

class Print:
	def GET(self):
		pdf = pdfPrint.PDFPrint()
		pdf.genMultiPDF("templates")
		
		data = {
			'url' : "static/output/all.pdf"
		}
		# fi = codecs.open('templates/cover.html','r','utf-8')
		# res = fi.rea
		# fi.close()
		return json.dumps(data)

class Down:
	def GET(self):
		return render.down()

app = web.application(urls, globals())
application = app.wsgifunc()

if __name__ == "__main__":
  app.run()
