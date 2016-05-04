from bs4 import BeautifulSoup
from pyPdf import PdfFileWriter, PdfFileReader

import pdfkit
import xmlParse
import urllib

pageNum = 1
htmlFile = "templates/"+str(pageNum) + ".html"
blank = "templates/blank.template.html"

contents = []
#first soup
soup = BeautifulSoup(open(htmlFile), "html.parser")
contents.append(soup)

ps = soup.select(".content p")
ls = soup.select(".label")[0]
cs = soup.select(".comment")[0]

#remove script link
soup.script.extract()
soup.link.extract()

settings = xmlParse.XmlParse()
settings.open("data/settings.xml")

comments = xmlParse.XmlParse()
comments.open("data/comments.xml")

#insert settings
settingsPage = settings.find_node_by_attr(settings.root, "page", {"attr":"id","val":pageNum})
items = settings.find_nodes(settingsPage, "item")
for item in items:
	p = ps[int(item.get("line"))]
	p['data-item-seq'] = int(item.get('seq'))
	a = p.select('a')[0] 
	a['class'] = 'underline'
	#insert label
	style = "left: "+item.get("left")+"px;position: absolute;"
	spanTag = soup.new_tag("span",style=style)
	spanTag['data-line'] = item.get('line')
	spanTag.string = item.get('seq')
	ls.append(spanTag)

#insert comments
commentsPage = comments.find_node_by_attr(comments.root, "page", {"attr":"id","val":pageNum})
lines = comments.find_nodes(commentsPage, "line")

subIns = 1
for line in lines:
	comment = BeautifulSoup(urllib.unquote(line.text), "html.parser")
	if int(line.get("sub")) != subIns:
		blankSoup = BeautifulSoup(open(blank), "html.parser")
		contents.append(blankSoup)
		subIns = subIns + 1
	
	(contents[subIns - 1].select(".comment")[0]).append(comment)


#cs.append(comment)


#insert script code
jsScript = '''
	//arrange label
	function getElementsByClassNameDef(className, element) {
		var children = (element || document).getElementsByTagName('*');
		var elements = new Array();
		         
		for (var i = 0; i < children.length; i++) {
			var child = children[i];
			var classNames = child.className.split(' ');
			for (var j = 0; j < classNames.length; j++) {
		    	if (classNames[j] == className) {
		    		elements.push(child);
		        	break;
		    	}
			}
		}
		         
		return elements;
	}

	function arrangeTag(){
		//arrange label
		var container = getElementsByClassNameDef('container')[0];
		container.style.width = "1536px";
		container.style.height = "1024px";
		var labelTag = getElementsByClassNameDef('label')[0];
		var labels = labelTag.getElementsByTagName('span');
		var contentTag =  getElementsByClassNameDef('content')[0];
		var pTags = contentTag.getElementsByTagName('p');
		for(var index = 0 ; index < labels.length ; index++) {
		    var line = labels[index].getAttribute('data-line');
		    var contentP = pTags[line].getElementsByTagName('a')[0];
		    labels[index].style.top = (contentP.offsetTop - 28) + 'px';
		}

		//arrange comment
		var commentBox = getElementsByClassNameDef('comment-box')[0];
		commentBox.style.overflow = 'hidden';
		var commentPanel = getElementsByClassNameDef('comment')[0];
		var comments = getElementsByClassNameDef('comment-item', commentPanel);
		var lastComment = comments[comments.length - 1];
		lastComment.style.marginBottom = '0px';
	}
	arrangeTag();
'''
script_tag = soup.new_tag('script', type="text/javascript")
script_tag.string = jsScript

options = {
	'page-width' : '420',
	'page-height' : '297',
	'dpi' : '300',
	'encoding' : 'UTF-8'
}
css = 'static/css/index.css'

pdfFileNames = []
for i in range(0, len(contents)):
	contents[i].body.append(script_tag)
	pdfFile = "static/output/"+str(pageNum)+"."+str(i)+".pdf"
	pdfkit.from_string(contents[i].prettify(), pdfFile, options=options, css=css)
	pdfFileNames.append(pdfFile)

#Merge pdf
output = PdfFileWriter()
for fileName in pdfFileNames:
	output.addPage(PdfFileReader(file(fileName, "rb")).getPage(0))

pdfFile = "static/output/"+str(pageNum)+".pdf"
outputStream = file(pdfFile, "wb")
output.write(outputStream)
outputStream.close()

'''
soup.body.append(script_tag)

content = soup.prettify()

		
options = {
	'page-width' : '420',
	'page-height' : '297',
	'dpi' : '300',
	'encoding' : 'UTF-8'
}

css = 'static/css/index.css'
pdfFile = "static/output/"+str(pageNum)+".pdf"
pdfkit.from_string(content, pdfFile, options=options, css=css)
'''
#pdfkit.from_file("1.html", "out.pdf", options=options)
