# -*- coding:utf-8 -*-
begin="""
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
            <!--<img src="../static/img/other/loading.gif">-->
            <div class="loading-text">正在生成中，请稍等</div>
        </div>
    </div>
	<div class="print">
    	<i class="fa fa-print book-print"></i>
    </div>
	<div class="catalog">
    	<div class="header">Content</div>
        <ul>
        	<li><a>Chapter 01</a></li>
            <li><a>Chapter 02</a></li>
            <li><a>Chapter 03</a></li>
            <li><a>Chapter 04</a></li>
            <li><a>Chapter 05</a></li>
            <li><a>Chapter 06</a></li>
    	</ul>
    </div>
	<div class="container">
		<div class="left">
            <div class="content-box">
            	<div class="input-panel input-left">
                    <div class="input-group">
                        <input class="form-control" placeholder="/发送弹幕" type="text" />
                        <input id="leftPicView" style="display:none" type="file" name="image" />
                        <i class="fa fa-image pic-select"></i>
                        <span class="btn send">发送</span>
                    </div>
                    <div class="image-group">
                        <img id="leftImgView" src="" />
                        <div id="leftImgLoading" class="loading">正在加载中...</div>
                    </div>
                </div>
            	<div class="label"></div>
            	<div class="content" data-max-seq="0" data-page=" """
        
end1="""
 </div>
                <div class="footer">
                	<div class="page">
                    	<span class="pre font-lg"><a href=" """
end2=""" " style="color:black;text-decoration:none;">&lt;</a></span>
                        <span class="cur font-ms">
"""
end3="""
</span>
                        <span class="font-ms">/</span>
                        <span class="total font-ms">255</span>
                        <span class="next font-lg"><a href=" """
end4=""" " style="color:black;text-decoration:none;">&gt;</a></span>
                    </div>
                </div>
            </div>
        </div>
    	<div class="right">
        	<div class="input-panel input-right">
                <div class="input-group">
                    <input class="form-control" placeholder="/发送弹幕" type="text" />
                    <!--<input id="picPreview" style="display:none" type="file" name="image" />
                    <i class="fa fa-image pic-select"></i>-->
                    <span class="btn send">发送</span>
                </div>
                <div class="image-group">
                    <img id="imagePreview" src="" />
                    <div id="imageLoading" class="loading">正在加载中...</div>
                </div>
            </div>
            <div class="comment-box">
        	   <div class="comment real">
            	
                </div>
            </div>
        </div>
        <div class="fake-right">
            <div class="comment-box">
                <div class="comment fake">
                </div>
            </div>
        </div>
	</div>
</body>
</html>
"""
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
f=codecs.open('db/txt','r','utf-8')
a=f.readlines()
f.close()
counter=0
num=0
s=""
for i in a:
    #i=a[j]
    if i!='\n':
        length=len(i)
        counter=counter+length/30+2
        s=s+"<p><a>"+i+"</a></p>"
    if counter>=25:
        url="templates/"+str(num)+".html"
        f=codecs.open(url,'w','utf-8')
        f.write(begin+str(num)+'\">'+s+end1+str(num-1)+end2+str(num)+end3+str(num+1)+end4)
        f.close()
        s=""
        counter=0
        num=num+1
        
        
        
