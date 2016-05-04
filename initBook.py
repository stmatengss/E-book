# -*- coding:utf-8 -*-
import xmlParse
import sys
import codecs

reload(sys)

blankHtml = """
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
    <link href="../static/css/index.css" rel="stylesheet" />
    
    <!-- lib js files -->
    <script type="text/javascript" src="../static/js/lib/jquery.min.js"></script>
    <script type="text/javascript" src="../static/js/lib/jquery.ui.min.js"></script>
    <script type="text/javascript" src="../static/js/lib/jquery.fileupload.js"></script>
    <script type="text/javascript" src="../static/js/lib/jquery.uploadify.js"></script>
    <script type="text/javascript" src="../static/js/lib/math.json2.js"></script>
    <script type="text/javascript" src="../static/js/lib/jquery.jstorage.js"></script>
    
    <script type="text/javascript" src="../static/js/common.tools.js"></script>
    <script type="text/javascript" src="../static/js/webSDK.js"></script>
    <script type="text/javascript" src="../static/js/index.js"></script>
</head>
<body>
    <div id="loading" tabindex="-1" unselectable="on" style="z-index: 99999999; display: none;">
        <div class="loading-mask" tabindex="-1" unselectable="on"></div>
        <div class="loading-state" style="">
            <div class="loading-text">正在生成中，请稍等</div>
        </div>
    </div>
    <span class="page-num">{pageNum}</span>
	<div class="print">
    	<img class="fa fa-arrow-circle-down" src="../static/img/down.png">
    </div>
	<div class="catalog">
    	<div class="header">Content</div>
        <ul>{chapters}</ul>
        <div class="jump-box">
            <input class="jump-control" type="text" />
            <span class="btn jump">跳转</span>
        </div>
    </div>
	<div class="container">
	<div class="catalog-content"></div>
		<div class="left">
            <div class="content-box">
            	<div class="input-panel input-left">
                    <div class="input-group">
                        <input class="form-control" placeholder="/发送弹幕" type="text" />
                        <input id="leftPicView" style="display:none" type="file" name="image" />
                        <img class="fa fa-image pic-select" src="../static/img/img.png" />
                        <!--span class="btn send">发送</span-->
						<img class="send" src="../static/img/send.png">
                    </div>
                    <div class="image-group">
                        <img id="leftImgView" src="" />
                        <img id="leftImgFakeView" src="" />
                        <div id="leftImgLoading" class="loading">正在加载中...</div>
                    </div>
                </div>
				<div class="label"></div>
            	<div class="content" data-max-seq="0" data-page="{idNum}">{content}</div>
            </div>
        </div>
    	<div class="right">
        	<div class="input-panel input-right">
                <div class="input-group">
                    <input class="form-control" placeholder="/发送弹幕" type="text" />
                    <!--<input id="picPreview" style="display:none" type="file" name="image" />
                    <i class="fa fa-image pic-select"></i>-->
                    <img class="send" src="../static/img/send.png">
                </div>
                <div class="image-group">
                    <img id="imagePreview" src="" />
                    <div id="imageLoading" class="loading">正在加载中...</div>
                </div>
            </div>
            <div class="comment-box">
			<!--div class="label"></div-->
        		<div class="comment">
                </div>
            </div>
            <div class="flip">
                <img class="fa fa-chevron-up up" src="../static/img/before.png"/>
                <img class="fa fa-chevron-down down" src="../static/img/after.png"/>
            </div>
        </div>
	</div>
	<div class="footer">
                	<div class="page">
                    	<span class="pre font-lg"><a href="{prePage}">&lt;</a></span>
                        <span class="cur font-ms">{curPage}</span>
                        <span class="fuck font-ms">/</span>
                        <span class="total font-ms">{totalPage}</span>
                        <span class="next font-lg"><a href="{nextPage}">&gt;</a></span>
                    </div>
    </div>
	<!--div style="background-color: #ffffff; width:10px; height:10px; position: absolute; bottom:0px; right:0px"></div-->
</body>

</html>
"""

chapterHtml = '''
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
    <link type="text/css" rel="stylesheet" href="../static/css/index.css">
    
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
    <span class="page-num">{pageNum}</span>
    <div class="print">
        <i class="fa fa-arrow-circle-down"></i>
    </div>
    <div class="container">
        <div class="left">
            <div class="content-box">
                <div class="content">
                    <div class="chapter">{content}</div>
                </div>
                <div class="footer">
                	<div class="page">
                    	<span class="pre font-lg"><a href="{prePage}" style="color:black;text-decoration:none;">&lt;</a></span>
                        <span class="cur font-ms">{curPage}</span>
                        <span class="font-ms">/</span>
                        <span class="total font-ms">{totalPage}</span>
                        <span class="next font-lg"><a href="{nextPage}" style="color:black;text-decoration:none;">&gt;</a></span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

sys.setdefaultencoding("utf-8")
f = codecs.open('db/txt-deal2', 'r', 'utf-8')
a = f.readlines()
f.close()

# page settings xml parse
setXmlPath = "data/settings.xml"
data = xmlParse.XmlParse()
data.open(setXmlPath)
data.remove_nodes(data.root)

# default value
# MAXLENGTH = 34
# MAXLINE = 32
MAXLENGTH = 34
MAXLINE = 34
# init page information
chapters = ''
pageCount = 0
chaptersNum = []


def initInfo():
    global chapters, pageCount
    cc = 0
    nn = 1

    for i in a:
        if i != '\n':
            length = len(i)
            if length > 2 and i[0] == '#' and i[1] == '#':
                if cc > 0:
                    nn += 1

                chapters += '''<li><a href="{href}">{text}</a></li>'''.format(href=str(nn), text=i[2:len(i)])
                chaptersNum.append(nn);
                cc = 0
                nn += 1
                continue
            else:
                tmp = length / MAXLENGTH + 2
                if cc+tmp > MAXLINE + 1:
                    cc = 0
                    nn += 1
                cc = cc + tmp



    pageCount = nn - 1


initInfo()

counter = 0
num = 1
s = ""


def genHtmlPage(htmlTemp, content):
    global s, counter, num
    global data, chapters, pageCount
    curPage = ""

    url = "templates/" + str(num) + ".html"
    f = codecs.open(url, 'w', 'utf-8')

    pageNum = 0;
    chapterIndex = 0;
    for indexI, chapterNum in enumerate(chaptersNum):
        if num < chapterNum:
            break;
        chapterIndex = indexI + 1

    if chapterIndex < 10:
        pageNum = '0' + str(chapterIndex)
    else:
        pageNum = str(chapterIndex)

    prePage = 1 if (num - 1) <= 0 else (num - 1)
    nextPage = pageCount if (num + 1) > pageCount else (num + 1)

    if num < 10:
        curPage = "00" + str(num)
    elif num < 100:
        curPage = "0" + str(num)
    else:
        curPage = str(num)

    f.write(htmlTemp.format(idNum=num, content=content, chapters=chapters, pageNum=pageNum, curPage=curPage,
                            prePage=str(prePage), nextPage=str(nextPage), totalPage=str(pageCount)))
    f.close()

    # add page info to settings.xml
    node = data.create_node("page", {"id": str(num), "change": str(0)}, "")
    data.append_node(data.root, node)

    s = ""
    counter = 0
    num = num + 1


for i in a:
    # i=a[j]
    if i != '\n':
        length = len(i)
        if length > 2 and i[0] == '#' and i[1] == '#':

            # counter is not zero
            if counter > 0:
                genHtmlPage(blankHtml, s)
            # output chapter page
            genHtmlPage(blankHtml, '<div style="font-family: courier; font-size: 12px">'+i[2:len(i)]+'</div>')
            continue

        else:
            tmp = length / MAXLENGTH + 2
            if counter +tmp >MAXLINE+1:
                genHtmlPage(blankHtml, s)
            counter = counter + length / MAXLENGTH + 2
            s = s + "<p><a>" + i + "</a></p>"
        # s=s+"""<p style="text-indent:2em"><a>"""+i+"</a></p>"

    # if counter >= MAXLINE:
    #     genHtmlPage(blankHtml, s)

data.write(setXmlPath)
