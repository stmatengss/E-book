// JavaScript Document
// Designed by Azy
//global variable
var invalid_letters = /[:"\<\>\\\/\?\*\|]/;
var valid_int = /^\d+$/;
var browser_exp = /(msie|webkit|gecko|presto|opera|safari|firefox|chrome|maxthon|android|ipad|iphone|webos|hpwos)[ \/os]*([\d_.]+)/ig;
var LANG = "&locale=zh_CN";

//trim routine
function LTrim(str){
    var i;
    for(i=0;i<str.length;i++)
    {
        if(str.charAt(i)!=" "&&str.charAt(i)!=" ")break;
    }
    str=str.substring(i,str.length);
    return str;
}

function RTrim(str){
    var i;
    for(i=str.length-1;i>=0;i--)
    {
        if(str.charAt(i)!=" "&&str.charAt(i)!=" ")break;
    }
    str=str.substring(0,i+1);
    return str;
}

function Trim(str){
    return LTrim(RTrim(str));
}

function isValid(value){
    if(value === null || typeof value === 'undefined')
        return false;
    else
        return true;
}

String.format = function(src){
    if (arguments.length === 0) 
        return null; 
		 
    var args = Array.prototype.slice.call(arguments, 1);
    for(var i = 0; i < args.length; ++i)
        args[i] = encodeURIComponent(args[i]);
    
    return src.replace(/\{(\d+)\}/g, function(m, i){
        return args[i];
    });
};

String.parameterize = function(src){
	if (arguments.length === 0) 
        return null;
		 
    var args = Array.prototype.slice.call(arguments, 1);    
    return src.replace(/\{(\d+)\}/g, function(m, i){
        return args[i];
    });
}

String.parameterizeByName = function(src,options){
	if(!isValid(options))
		return src;
	
	for(var d in options){
        src = src.replace(new RegExp('\\$\\{' + d + '\\}', 'g'), options[d]);
    }
	
	return src;
}

String.removeHTMLTag = function(str) {
	str = str.replace(/<\/?[^>]*>/g,''); //去除HTML tag
    str = str.replace(/[ | ]*\n/g,'\n'); //去除行尾空白
    str = str.replace(/\n[\s| | ]*\r/g,'\n'); //去除多余空行
    str=str.replace(/ /ig,'');//去掉 
	str=str.replace(/&nbsp;/g,'');
    return str;
}

String.checkFormat = function(str,type){
	var Regexs = {
		photo : (/^image\/jpg$|jpeg$|png$|gif$|bmp$/)
	};
	
	if(isValid(str) && Trim(str) != ''){
		var typeRegexs = Regexs[type];
		return typeRegexs.test(str);
	}
	
	return false;
}

function minVal(first,second){
	return first < second ? first : second;
}
Array.contains = function(array,obj) {
    var i = array.length;
    while (i--) {
        if (array[i] === obj) {
            return true;
        }
    }
    return false;
}
function maxVal(first,second){
	return first > second ? first : second;
}

function genSharePassword(){
    var codeBase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    var code = '';
    for(var index = 0 ; index < 4 ; index++){
        code += codeBase[Math.floor(Math.random()*26)];
    }
    return code;
}

function urlParamsParse(url){
	var params = {};
	var paramsStr = url.split('?')[1];
	if(typeof paramsStr !='undefined' && paramsStr != ''){
		var paramsArray = paramsStr.split('&');
		for(var index = 0 ; index < paramsArray.length ; index++){
			var valueArray = paramsArray[index].split('=');
			var name = valueArray[0];
			var value = valueArray[1];
			params[name] = value;
		}
	}
	return params;
}

function getBrowerInformation(){
	var userAgent = window.navigator.userAgent.toLowerCase(),
    browserInfo = {
        platform: window.navigator.platform
    };
    userAgent.replace(browser_exp,
    function(each, browserName, vesrion) {
        var name = browserName.toLowerCase();
        browserInfo[name] || (browserInfo[name] = version)
    }),
    browserInfo.opera && userAgent.replace(/opera.*version\/([\d.]+)/,
    function(each, version) {
        browserInfo.opera = version
    });
    if (browserInfo.msie) {
        browserInfo.ie = browserInfo.msie;
        var version = parseInt(browserInfo.msie, 10);
        browserInfo["ie" + version] = !0
    }
    return browserInfo; 
}

function getDocumentRect(){
	var docRect = new Object();
	docRect.width = $(window).width() || 0;
	docRect.height= $(window).height()|| 0;

    return docRect;
}

function randomChar(){
	return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
}

function createUUID(){
	 return randomChar() + randomChar() + '-' + randomChar() + '-' + 
	 		randomChar() + '-' + randomChar() + '-' + randomChar() + randomChar() + randomChar();
}

function getHash(hash){
	var hashStr = hash ? hash : location.hash;
    if($.client.browser == "Safari")
        hashStr = decodeURI(hashStr);
    //trim '#'
    var pos = 0;
    for(var index = 0 ; index < hashStr.length ; index++){
        if(hashStr.charAt(index) == '#')
            pos++;
        else
            break;
    }
	var urlStr = hashStr.slice(pos,hashStr.length);
	return urlStr;
}

function imgLoadError(element){
    $(element).removeAttr("onerror");
    $(element).attr("src",$(element).attr('data-original'));
    $(element).attr("onerror",'imgLoadError(this)');
}

function show_dialog(msg){
    alert(msg);
}

function GetStrLength(str) {
	///<summary>获得字符串实际长度，中文2，英文1</summary>
    ///<param name="str">要获得长度的字符串</param>
    var realLength = 0, len = str.length, charCode = -1;
    for (var i = 0; i < len; i++) {
    	charCode = str.charCodeAt(i);
        if (charCode >= 0 && charCode <= 128) realLength += 1;
        else realLength += 2;
    }
    return realLength;
};

function stringThumbnail(str,len){
    /*if(str.length > maxLength)
        return str.substr(0,maxLength-3)+'...';
    else
        return str;*/

	//如果给定字符串小于指定长度，则返回源字符串；
	if(GetStrLength(str) <= len){
		return str;
	} else {
		len -= 3;
	}
	
	var str_length = 0;
    var str_len = 0;
        str_cut = new String();
        str_len = str.length;
    for (var i = 0; i < str_len; i++) {
    	a = str.charAt(i);
            str_length++;
        if (escape(a).length > 4) {
        	//中文字符的长度经编码之后大于4  
        	str_length++;
        }
        str_cut = str_cut.concat(a);
        if (str_length >= len) {
        	str_cut = str_cut.concat("...");
            return str_cut;
        }
    }
}

function calcPageTotalCount(itemCount,pageSize){
    return parseInt(((parseInt(itemCount)-1) / pageSize)) + 1;
}

function formatFileSize(bytes){
    if (typeof bytes !== 'number')
        return '';

    if (bytes >= 1000000000)
        return (bytes / 1000000000).toFixed(2) + ' GB';

    if (bytes >= 1000000)
        return (bytes / 1000000).toFixed(2) + ' MB';
    
    return (bytes / 1000).toFixed(2) + ' KB';
}

function fileType(){
	var type = '*.gif; *.jpg; *.png ; *.bmp; *.jpeg; *.PNG; *JPEG; *.GIF; *.BMP; *.JPG';
	return type;
}

function request(url,data,method,callback){
    $.ajax({
        url: url,
        data: data,
        type: method,
        contentType: "application/json; charset=utf-8",
        success: callback,
        error: callback,
        dataType: "json"
    });
}

function requestSync(url,data,method,callback){
	$.ajax({
		url:url,
		data:data,
		type:method,
		async:false,
		contentType:"application/json; charset=utf-8",
		success: callback,
		error: callback,
		dataType:"json"
	});
}

function requestCommon(url,data,method,isAsync,callback){
	$.ajax({
		url:url,
		data:data,
		type:method,
		async:isAsync,
		contentType:"application/json; charset=utf-8",
		success: callback,
		error: callback,
		dataType:"json"
	}); 
}
