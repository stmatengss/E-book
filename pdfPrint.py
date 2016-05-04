from bs4 import BeautifulSoup
from pyPdf import PdfFileWriter, PdfFileReader
import pdfkit
import xmlParse
import urllib
import os
import os.path

chapters = [1,18, 40, 49, 65, 80, 95, 108, 130, 147, 162, 176, 192, 208, 225, 243, 260, 275, 291, 305]

counter = 0

class PDFPrint:
    def genSinglePDF(self, pageNum):
        global counter
        changeNum = 0
        status=0
        chapterFlag = 0
        isOdd = 0
        htmlFile = "templates/" + str(pageNum) + ".html"
        blank1 = "data/blank1.html"
        blank2 = "data/blank2.html"
        contents = []
        # first soup
        soup = BeautifulSoup(open(htmlFile), "html.parser")
        contents.append(soup)

        ps = soup.select(".content p")
        #ls = soup.select(".label")[0]
        cs = soup.select(".comment")[0]
        cotent = soup.select(".")

        chapterNum = soup.select_one(".page-num").string

        delList=[".fa-arrow-circle-down", ".catalog-content", ".fa-chevron-up", ".fa-chevron-down",".fuck", ".catalog"]

        fontLog = soup.select(".font-lg")

        # delete
        for i in delList:
            soup.select_one(i).decompose()

        for i in fontLog:
            i.decompose()

        # change states to add a blank page
        for i in chapters:
            if pageNum == i+1:
                counter = 0
            if pageNum ==i:
                chapterFlag = 1



        for no, i in enumerate(chapters):
            if pageNum < i:
                changeNum = no
                break


        print "changeNum==", changeNum

        # odd page delete
        if counter % 2 == 0 or chapterFlag == 1:
            isOdd = 1
            status = 1
            page = soup.select_one(".page-num")
            left = soup.select_one(".left")
            right = soup.select_one(".right")
            footer = soup.select_one(".footer")
            footer['class'] = 'footer2'
            page['style'] = 'left: 40px; '
            left['style'] = 'position:absolute; right: 48px; top:48px;'
            right['style'] = 'position:absolute; left: 256px; top:48px;'
            #left['class'] = 'right'
            #right['class'] = 'left'
            nowPage = str(int(soup.select_one(".cur").getText())-changeNum-1)
            nextPage = str(int(soup.select_one(".cur").getText())-changeNum)

            if len(nowPage) == 2:
                nowPage = "0"+nowPage
            if len(nowPage) == 1:
                nowPage  = "00"+nowPage
            if len(nextPage) == 2:
                nextPage = "0"+nextPage
            if len(nextPage) == 1:
                nextPage  = "00"+nextPage
            soup.select_one('.cur').string = nowPage
            soup.select_one('.total').string = nextPage
            #footer = soup.select_one(".footer")
            #footer['class'] = 'footer2'
        else:
            status = 2
            soup.select_one(".page-num").decompose()
            soup.select_one(".footer").decompose()

        if chapterFlag:
            blankSoup = blankSoup = BeautifulSoup(open(blank1), "html.parser")
            contents.append(blankSoup)

        # change to odd
        # remove script link
        soup.script.extract()
        soup.link.extract()

        settings = xmlParse.XmlParse()
        settings.open("data/settings.xml")

        comments = xmlParse.XmlParse()
        comments.open("data/comments.xml")

        # insert settings
        settingsPage = settings.find_node_by_attr(settings.root, "page", {"attr": "id", "val": pageNum})
        # judge whether changed
        if settingsPage.get("change") != "0":
          return None

        items = settings.find_nodes(settingsPage, "item")
        for item in items:
            commentNum = int(item.get("line"))
            p = ps[commentNum]
            p['data-item-seq'] = int(item.get('seq'))

            #underline
            underline = soup.new_tag("u")
            underline.string = p.getText()
            a = p.select_one('a')
            if a :
                a.replace_with(underline)

            commentNum = item.get('seq')
            if len(commentNum)==1:
                commentNum = '0'+ commentNum
            subTag = soup.new_tag("sub")
            subTag.string = commentNum
            p.append(subTag)
            # underline = soup.new_tag("u")
            # underline.string = p.getText()
            # p.string(underline)

            #a['class'] = 'underline'
            # insert label
            style = "left: " + item.get("left") + "px;position: absolute;"
            spanTag = soup.new_tag("span", style=style)
            spanTag['data-line'] = item.get('line')
            spanTag.string = item.get('seq')
            #ls.append(spanTag)

        # insert comments
        commentsPage = comments.find_node_by_attr(comments.root, "page", {"attr": "id", "val": pageNum})
        lines = comments.find_nodes(commentsPage, "line")

        subIns = 0
        status = 0
        for line in lines:
            comment = BeautifulSoup(urllib.unquote(line.text), "html.parser")
            #print  "Log2::",int(line.get("sub"))
            if int(line.get("sub")) != subIns:
                if subIns % 2 == 1:
                    #print  "Log::"
                    status+=1
                    if status%2==1:
                        if isOdd == 1:
                            blankSoup = BeautifulSoup(open(blank1), "html.parser")
                        else :
                            blankSoup = BeautifulSoup(open(blank2), "html.parser")
                        #blankSoup.select_one(".page-num").string = chapterNum
                    else :
                        if isOdd == 1:
                            blankSoup = BeautifulSoup(open(blank2), "html.parser")
                        else :
                            blankSoup = BeautifulSoup(open(blank1), "html.parser")

                    contents.append(blankSoup)

                subIns = subIns + 1
            print subIns,len(contents)
            if subIns == 1:
                soup.select_one(".comment").append(comment)
            elif subIns % 2 == 0:
                (contents[(subIns) / 2].select_one(".right .comment")).append(comment);
            elif subIns % 2 == 1:
                (contents[(subIns ) /2].select_one(".left .comment")).append(comment);

        #BLANK PAGE

        #status+=len(contents)
        if status % 2 ==1 and status>0:
            blankSoup = BeautifulSoup(open(blank1), "html.parser")
            contents.append(blankSoup)

        # counter+=len(contents)
        counter += 1
        # for i in chapters:
        #     if pageNum == i-1:
        #         blankSoup = BeautifulSoup(open(blank2), "html.parser")
        #         blankSoup.select_one(".page-num").string = chapterNum
        #         contents.append(blankSoup)
        # insert script code
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
		        var container = getElementsByClassNameDef('container')[0];
		        var body = getElementsByTagName('body')[0];
		        container.style.width = "1440px";
		        container.style.height = "1008px";
				//container.style.width = "1536px";
		        //container.style.height = "1224px";
		        body.style.width = "1440px";
		        body.style.height = "1008px";

		        var labelTag = getElementsByClassNameDef('label')[0];
		        var labels = labelTag.getElementsByTagName('span');
		        var contentTag =  getElementsByClassNameDef('content')[0];
		        var pTags = contentTag.getElementsByTagName('p');
		        for(var index = 0 ; index < labels.length ; index++) {
		            var line = labels[index].getAttribute('data-line');
		            var content = pTags[line]
		            var contentP = pTags[line].getElementsByTagName('a')[0];
		            var newNode = document.createElement("sub");
		            newNode.innerHTML = line;
		            content.appendChild(newNode);
		            labels[index].style.top = (contentP.offsetTop + 14) + 'px';
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

        # soup.body.append(script_tag)
#'page-width': '420',
#'page-height': '297',
        # content = soup.prettify()
        options = {
            #'page-size': 'A3',
            'page-width': '300mm',
            'page-height': '210mm',
            'dpi': '500',
            #'orientation':'Landscape',
            'encoding': 'UTF-8',
            'margin-top': '0.0in',
            'margin-right': '0.0in',
            'margin-bottom': '0.0in',
            'margin-left': '0.0in',
        }
        css = 'static/css/index.css'
        #record pagenum

        #orientation The orientation of the output document, must be either "Landscape" or "Portrait".
        pdfFileNames = []
        for i in range(0, len(contents)):
            contents[i].body.append(script_tag)
            pdfFile = "static/output/" + str(pageNum) + "." + str(i) + ".pdf"
            pdfkit.from_string(contents[i].prettify(), pdfFile, options=options, css=css)
            pdfFileNames.append(pdfFile)

        # make the blank page


        # Merge pdf
        output = PdfFileWriter()
        for fileName in pdfFileNames:
            output.addPage(PdfFileReader(file(fileName, "rb")).getPage(0))

        pdfFile = "static/output/" + str(pageNum) + ".pdf"
        outputStream = file(pdfFile, "wb")
        output.write(outputStream)
        outputStream.close()

        # remove useless pdf file
        for fileName in pdfFileNames:
            os.remove(fileName)

        # set changed to 1
        # settingsPage.set("change", "1")
        # settings.write("data/settings.xml")

    def genCoverPDF(self, path):
        htmlPath = 'templates/cover.html'
        soup = BeautifulSoup(open(htmlPath), "html.parser")
        # remove script link
        soup.script.extract()
        soup.link.extract()
        soup.select_one(".book-version")['style'] = 'position:absolute; left:676px; bottom: 668px;'
        soup.select_one(".website").string = "www.thedevotionfsuspectx.cn"

        #delete list
        delList = [ '.subject', '.book-info']
        for i in delList:
            soup.select_one(i).decompose()

        # insert script code
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
		        //var body = getElementsByTagName('body')[0];
		        container.style.width = "1536px";
		        container.style.height = "1024px";
				//container.style.width = "3304px";
		        //container.style.height = "2536px";
		        //body.style.width = "3304px";
		        //body.style.height = "2536px";
			}
		    //arrangeTag();
		'''
        script_tag = soup.new_tag('script', type="text/javascript")
        script_tag.string = jsScript

        soup.body.append(script_tag)

        options = {
            #'page-size': 'A3',
            'page-width': '300mm',
            'page-height': '210mm',
            'dpi': '500',
            #'orientation':'Landscape',
            'encoding': 'UTF-8',
            'margin-top': '0.0in',
            'margin-right': '0.0in',
            'margin-bottom': '0.0in',
            'margin-left': '0.0in',
        }
        css = 'static/css/cover.css'

        pdfkit.from_string(soup.prettify(), path, options=options, css=css)
        # pdfkit.from_string("", "static/output/blank.pdf", options=options, css=css)
        fileName = 'static/output/blank.pdf'
        coverAll = 'static/output/titlePage.pdf'
        output = PdfFileWriter()
        output.addPage(PdfFileReader(file(fileName, "rb")).getPage(0))
        output.addPage(PdfFileReader(file(path, "rb")).getPage(0))
        outputStream = file(coverAll, "wb")
        output.write(outputStream)
        outputStream.close()

    def genMultiPDF(self, dirPath):
        printPageRange = 305
        files = os.listdir(dirPath)
        fileNums = []
        for filename in files:
            names = filename.split('.')
            if len(names) == 2 and names[1] == 'html' and names[0] != 'cover' and names[0]!='down':
                fileNums.append(int(names[0]))

        fileNums.sort()

        # gen pdf file
        for num in fileNums:
            print num
            if num < printPageRange:
                self.genSinglePDF(num)

        # Merge chapter
        pdfFile = ""
        status = 1
        for num in fileNums:
            if num < printPageRange:
                status = 1
                for chapter,i in enumerate(chapters):
                    if num == i:
                        output = PdfFileWriter()
                        pdfFile = "static/output/" +"chapter"+str(chapter+1)+ ".pdf"
                        output.addPage(PdfFileReader(file("static/output/blank.pdf", "rb")).getPage(0))
                        output.addPage(PdfFileReader(file("static/output/blank.pdf", "rb")).getPage(0))
                        status = 0
                        break
                if status:
                    fileName = "static/output/" + str(num) + ".pdf"
                    pdfInput = PdfFileReader(file(fileName, "rb"))
                    for index in range(0, pdfInput.getNumPages()):
                        output.addPage(pdfInput.getPage(index))
                    for i in chapters:
                        if num == i-1:
                            outputStream = file(pdfFile, "wb")
                            output.write(outputStream)
                            outputStream.close()

        # Merge pdf
        output = PdfFileWriter()

        # gen cover
        coverPath = "static/output/cover.pdf"
        self.genCoverPDF(coverPath)
        output.addPage(PdfFileReader(file(coverPath, "rb")).getPage(0))
        for num in fileNums:
            if num < printPageRange:
                fileName = "static/output/" + str(num) + ".pdf"
                pdfInput = PdfFileReader(file(fileName, "rb"))
                for index in range(0, pdfInput.getNumPages()):
                    output.addPage(pdfInput.getPage(index))

        pdfFile = "static/output/all.pdf"
        outputStream = file(pdfFile, "wb")
        output.write(outputStream)
        outputStream.close()
