// JavaScript Document
var HOST = window.location.host;
var MAXHEIGHT = 816;
var picStatus = true;

$(function(){
	//loading
    loadLabels();
	loadComments();
	var inputPanel = {
		left : {
			show : function(){
				$('.input-panel.input-left').show();
			},
			hide : function(){
				$('.input-panel.input-left').hide();
				/*Clean*/
				$('.input-panel.input-left .form-control').val('');
				$('.input-panel.input-left .form-control').removeAttr('disabled');
				$('#leftImgView').attr('src','');
				$('#leftImgLoading').hide();
				$('#leftImgView').hide();
			}
		},
		right : {
			show : function(){
				$('.input-panel.input-right').show();
			},
			hide : function(){
				$('.input-panel.input-right').hide();
				/*Clean*/
				$('.input-panel.input-right .form-control').val('');
				$('.input-panel.input-right .form-control').removeAttr('disabled');
				$('#rightImgView').attr('src','');
				$('#rightImgLoading').hide();
				$('#rightImgView').hide();
			}
		}
	};
	$('.content').on('click','p',function(e){
		if(!$(this).find('a').hasClass('selected')){
			$('.content p a').removeClass('selected');
			$(this).find('a').addClass('selected');
			var pos = $(this).position().top + $(this).height()+10;
			$('.input-panel.input-left').css("top",pos+"px");
			inputPanel.left.show();
		} else {
			$('.content p a').removeClass('selected');
			inputPanel.left.hide();
		}
	});
	$('.comment').on('click','.item',function(e){
		if(!$(this).hasClass('selected')){
			$('.comment .item').removeClass('selected');
			$(this).addClass('selected');
			var top = $(this).position().top + $(this).height() + 10;
			var left= $(this).position().left;
			$('.input-panel.input-right').css("top",top+"px");
			inputPanel.right.show();
		} else {
			$('.comment .item').removeClass('selected');
			inputPanel.right.hide();
		}
	});


	//TODO
	$('.input-panel.input-left .send').on('click', function(e){
		/*hide selected word*/
		var text = Trim($('.input-panel.input-left .form-control').val());
		if (text.length < 1 && picStatus) {
            alert (" 输入文字不能为空 ");
			picStatus = true;
            return ;
        }
		var $element = $('.content p a.selected');
		$element.removeClass('selected');
		//
		//if (picStatus == false)picStatus = true;
		/*show underline*/
		var seq = getItemSeq($element.parent('p'));
		if(seq.changed){
			var pos = $element.position().top+12;
			var span =
				String.parameterizeByName('<span style="left: 20px;position: absolute;top:${pos}px">${seq}</span>',
				{
					'pos' : pos,
					'seq' : seq.value_str
				});
			//$('.label').append(span);

			$element.after(" <sub>"+seq.value_str+"</sub>");
			//$element.append("<div class=\"sub-div\">"+seq.value_str+"</div>");
			$element.addClass('underline');
			//*
			$element.parent('p').attr('data-item-seq',seq.value);
			/*add page settings information*/
			insertLabel($element.parent('p').index(), seq.value_str, pos, 20);
		}

		/*add message to comment list*/
		addComment(seq.value_str);
		inputPanel.left.hide();

		loadComments(); //
	});

	$('.input-panel.input-left .pic-select').on('click',function(e){
		$('#leftPicView').click();
	});

	$('#leftPicView').change(function(e){
		if(typeof e.target.files[0] == 'undefined')
			return ;
		if(e.target.files[0].size > 512000){
			alert('图片不能大于500KB');
			return;
		}
		picStatus = false;
		//alert(picStatus);
		$('.input-panel.input-left .form-control').val('');
		$('.input-panel.input-left .form-control').attr('disabled','disabled');
		$('#leftImgLoading').show();
		$('#leftImgView').hide();
		var reader = new FileReader();
		reader.onload = function(data) {
			$('#leftImgView').attr('src',data.target.result);
			$('#leftImgFakeView').attr('src',data.target.result);
			$('#leftImgLoading').hide();
			$('#leftImgView').show();
		};
		reader.readAsDataURL(e.target.files[0]);
	});

	//comment
	$('.input-panel.input-right .send').on('click', function(e){
		if (Trim($('.input-panel.input-right .form-control').val()).length < 1 ) {
            alert (" 输入文字不能为空 ");
            return ;
        }
		var $element = $('.comment .item.selected');
		$element.removeClass('selected');
		$newElement = $element.clone(true);

		var num = $element.find('sup:first').text();

		$element.remove();

		var content = '<sup>'+num+'</sup>' + Trim($('.input-panel.input-right .form-control').val())+'//';
		$newElement.find('sup:first').before(content);
		$newElement.css("margin-bottom", "24px");
		$('.comment').prepend($newElement);
		// ##
		//set last element
		$('.comment .comment-item:last').css("margin-bottom", "0px");
		inputPanel.right.hide();
		judgeScroll();
		//TODO: update sub page
		updateComment($newElement.attr('data-lid'), encodeURIComponent($newElement.prop("outerHTML")));
	});


    $('.send').on('mouseenter',function(e){
    		$('.send').attr('src',"../static/img/send2.png");
    });
    $('.send').on('mouseleave',function(e){
        	$('.send').attr('src',"../static/img/send.png");
     });
	//mouse move event
	$('.container .catalog-content').on('mouseenter',function(e){
		$('.catalog').animate({left:"0px"});
	});
	$('.container').on('click', function(e){
		$('.catalog').animate({left:"-120px"});
	});

	$('.catalog').on('mouseleave',function(e){
		$('.catalog').animate({left:"-120px"});
	});

	//page jump
	$('.jump-box .jump').on('click',function(e){
		var pageNum = $('.jump-box input').val();
		var pageCount = $('.footer .page .total').text();
		if(pageNum > 0 && pageNum <= parseInt(pageCount))
			window.location.href = pageNum+'';
	});

	//flip event
	$('.flip img.up').on('click',function(e){
		var curMTop = $('.comment').css('margin-top').replace('px','');
		curMTop = parseInt(curMTop) + 100
		if(curMTop > 0)
			curMTop = 0;
		$('.comment').animate({
			marginTop: curMTop
		}, 500)
	});
	$('.flip img.down').on('click',function(e){
		var delta = Math.abs($('.comment-box').height() - $('.comment').height());
		var curMTop = $('.comment').css('margin-top').replace('px','');
		curMTop = parseInt(curMTop) - 100
		if(Math.abs(curMTop) > delta)
			curMTop = -delta;
		$('.comment').animate({
			marginTop: curMTop
		}, 500)
	});

	//left and right flip
	$(document).keydown(function(e){
		if(e.keyCode == 37){
			var href = $('.footer .pre a').attr("href");
			window.location.href = href;
		}else if (e.keyCode == 39){
			var href = $('.footer .next a').attr("href");
			window.location.href = href;
		}else if (e.keyCode == 9) {
         			$('.catalog').animate({left:"0px"});
       	}
	});

	//print all book
	$('.print').on('click',function(e){
		$element = $('#loading .loading-state .loading-text');
		var flag = false;
		var loading = {
			show : function(){
				$('#loading').show();
			},
			hide : function(){
				$('#loading').hide();
			}
		};
		function loadingState(){
			if(!flag){
				var loadingText = $element.text();
				loadingText.length < 11 && (loadingText = "\u6b63\u5728\u751f\u6210\u4e2d\uff0c\u8bf7\u7a0d\u7b49\u002e");
				loadingText += ".";
				loadingText.length > 14 && (loadingText = "\u6b63\u5728\u751f\u6210\u4e2d\uff0c\u8bf7\u7a0d\u7b49\u002e");
				$element.text(loadingText);
				setTimeout(loadingState, 1e3);
			}
			else
				$element.text("\u6b63\u5728\u751f\u6210\u4e2d\uff0c\u8bf7\u7a0d\u7b49");
		}

		loading.show();
		loadingState();

		var url = url_templates.print.get();
		request(url,"","get",function(data,status){
			loading.hide();
			window.location.href = data.url;
		});
	});
});

function updateCommentSub(start){
	$('.comment .comment-item').each(function(index, element){
		if(index >= start){
			var tHeight = $(element).position().top + $(element).height();
			var oldSub = $(element);
		}
	});


}

function loadLabels(){
	var url = url_templates.settings.get(getCurrentPage());
	request(url,"","get",function(data,status){
		if(status == "success"){
			var maxSeq = 0;
			for(var index = 0 ; index < data.length ; index++){

				$element = $('.content p:eq('+data[index].line+')');
				var pos = $element.find('a').position().top+12;
				var span =
					String.parameterizeByName('<span data-line="${line}" style="left: 20px;position: absolute;top:${pos}px">${seq}</span>',
					{
						'pos' : 0,//pos,
						'seq' : data[index].seq,
						'line' : data[index].line
					});
				//$('.label').append(span);
				$element.attr('data-item-seq',parseInt(data[index].seq));
				$element.find('a').addClass("underline");

				$element.append(" <sub>"+data[index].seq+"</sub>");

				if(maxSeq < parseInt(data[index].seq))
					maxSeq = parseInt(data[index].seq);

			}

			$('.content').attr('data-max-seq',maxSeq);

			arrangeTag();
		}
	});
}

function insertLabel(line, seq, top, left){
	var url = url_templates.settings.insert(getCurrentPage(), line, seq, top, left);
	request(url, "", "post", function(data, status){
		if(status == "success") {
		}
	});
}

function loadComments(){
	var url = url_templates.comments.get(getCurrentPage());
	request(url, "", "get", function(data, status){
		if(status == "success"){
			for(var index = 0 ; index < data.length ; index++) {
				var html = decodeURIComponent(data[index].content);
				var todo = $("<div style=\"float:left; width:408px;\"></div>");
				//console.log(html);
				//console.log(todo);
				//todo.wrap("<div style=\"float:left; width:370px;\"></div>");
				//todo.after(",.fuckfuckfuck");
				//console.log(todo);
				var $com = $(html);
				var sup = $(($com).find("sup")[0]).text();
				$(($com).find("sup")[0]).text("");
				// ##
				//$('.comment').append(html);
                $('.comment').append("<div style=\"float:left; width:28px; height: 14px; \"><sub style=\"font-size:14px;\">"+sup.toString()+"</sub></div>");
				$('.comment').append(todo.append($com));
				//$('.comment').height += $('.comment-item')
				//console.log(data[index]); //
				//var todo = $.parseHTML(html)[0];
				//console.log(todo);

				//todo.innerHTML = "01";
				// var span =
					// String.parameterizeByName('<span data-line="${data-line}" style="left: 10px;position: absolute;top:${pos}px">${seq}</span>',
					// {
						// 'pos' : 0,//pos,
						// 'seq' : data[index].lid,
						// 'data-line' : 0
					// });
				//$('.label').append(todo); //

			}
			arrangeTag(); //
			$('.comment .comment-item:last').css("margin-bottom", "0px");
			//judgeScroll();
		}
	});
}

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
	var labelTag = getElementsByClassNameDef('label')[0];
	var labels = labelTag.getElementsByTagName('span');
	var contentTag =  getElementsByClassNameDef('comment')[0];//
	var pTags = contentTag.getElementsByTagName('p');
	for(var index = 0 ; index < labels.length ; index++) {
		var line = labels[index].getAttribute('data-line');
		var contentP = pTags[line];
		labels[index].style.top = (contentP.offsetTop + 18) + 'px';
	}
}

function getItemSeq($element){
	var maxSeq = $('.content').attr('data-max-seq');
	var curSeq = $element.attr('data-item-seq');
	var flag = false;
	if(typeof curSeq == 'undefined' || curSeq == '') {
		flag = true;
		curSeq = parseInt(maxSeq)+1;
		$('.content').attr('data-max-seq', curSeq);
	}

	return {
		'changed' : flag,
		'value' : curSeq,
		'value_str' : parseInt(curSeq) < 10 ? '0'+curSeq : curSeq
	};
}

/*
	delLid: use to delete the review of comments
*/
function addComment(num){
    var text = Trim($('.input-panel.input-left .form-control').val());
	if (false) {
		alert (" 输入文字不能为空!! ");
		return ;
	}else{
		//alert();
	    var max = 0;
    	$('.comment .comment-item').each(function(index, element){
    		var lid = parseInt($(element).attr('data-lid'));
    		if( lid > max)
    			max = lid
    	});

    	//increase current lid
    	max += 1;
		var templates =
    		'<p class="comment-item item" data-lid="${lid}" style="text-indent:${dist}"><a><sup>${num}</sup>${text}</a></p>';

    	/*var images =
    		'<div class="comment-item" data-lid="${lid}"><div style="display:table;margin-left:${left}%">\
    			<span style="float:left">${num}</span><img width=300 src="${src}" />\
    		</div></div>';*/

    	var images =
    		'<div class="comment-item" data-lid="${lid}"><div style="display:table;margin-left:${left}px">\
    			<span style="float:left">${num}</span><div style="background: url(${src}) center center no-repeat;background-size: ${width}px ${height}px;width:${width}px;height:${height}px" class="img noise"></div>\
    		</div></div>';


    	var dist = Math.ceil(Math.random() * 6) * 48 + 'px';

    	if($('#leftImgView').attr('src') != ''){
    		spaceCount = 0;
    		var left = 48;
    		var imgObj = document.getElementById('leftImgFakeView');
    		var imgW = imgObj.width;
    		var imgH = imgObj.height;

    		var width = 308;
    		var height = parseInt(308 * imgH / imgW);

    		var options = {
    			'left': left,
    			'num' : num,
    			'lid' : max,
    			'src' : gray(imgObj),
    			'width' : width,
    			'height' : height
    		};
    		var html = String.parameterizeByName(images, options)
    	} else {
    		var options = {
    			'dist' : dist,
    			'num' : num,
    			'lid' : max,
    			'text' : text
    		};
    		var html = String.parameterizeByName(templates,options);
    	}

    	//recovery last item margin bottom
    	$('.comment .comment-item:last').css("margin-bottom", "24px");

    	//add to comments list
    	$('.comment').prepend(html);

    	//delete Current element's margin-bottom
    	$('.comment .comment-item:last').css("margin-bottom", "0px");
    	judgeScroll();

    	//calc sub page of all elements
    	var curHeight = $('.comment').height();
    	var subNum = parseInt(curHeight / MAXHEIGHT) + 1

    	//add to server
    	var form = {
    		"dist" : dist,
    		"lid" : max,
    		"content" : encodeURIComponent(html),
    		"sub" : subNum,
    		"subs" : JSON.stringify(calcCommentSub())
    	};

    	var url = url_templates.comments.insert(getCurrentPage());
    	$.post(url, form, function(data, status){
    		if(status == "success"){}
    	});
	}
		

}

function calcCommentSub(){
	var subs = [];
	$('.comment .comment-item').each(function(index, element){
		var outHeight = $(element).position().top + $(element).height();
		var subNum = parseInt(outHeight / MAXHEIGHT) + 1;
		subs.push({
			"lid" : $(element).attr("data-lid"),
			"sub" : subNum
		});
	});
	return subs;
}

function judgeScroll(){
	var flipPanel = {
		show : function(){
			$('.flip').show();
		},
		hide : function(){
			$('.flip').hide();
		}
	};
	var commentH    = $('.comment').height();
	console.log(commentH);
	var commentBoxH = $('.comment-box').height();
	console.log(commentBoxH);
	var delta = Math.abs(commentH - commentBoxH);
	// ##
//	if(commentH > commentBoxH) {
//		flipPanel.show();
//	} else {
//		flipPanel.hide();
//	}
    flip.show();
}

function updateComment(lid, content){
	var url = url_templates.comments.update(getCurrentPage());
	var form = {
		'lid' : lid,
		'content' : content,
		'subs' : JSON.stringify(calcCommentSub())
	};

	$.post(url, form, function(data, status){
		if(status == "success"){}
	});
}

function getCurrentPage(){
	return Trim($('.content').attr('data-page'));
}

function gray(imgObj) {
    var canvas = document.createElement('canvas');
    var canvasContext = canvas.getContext('2d');
     
    var imgW = imgObj.width;
    var imgH = imgObj.height;
    canvas.width = imgW;
    canvas.height = imgH;
     
    canvasContext.drawImage(imgObj, 0, 0);
    var imgPixels = canvasContext.getImageData(0, 0, imgW, imgH);
     
    for(var y = 0; y < imgPixels.height; y++){
        for(var x = 0; x < imgPixels.width; x++){
            var i = (y * 4) * imgPixels.width + x * 4;
            var avg = (imgPixels.data[i] + imgPixels.data[i + 1] + imgPixels.data[i + 2]) / 3;
            imgPixels.data[i] = avg; 
            imgPixels.data[i + 1] = avg; 
            imgPixels.data[i + 2] = avg;
        }
    }
    canvasContext.putImageData(imgPixels, 0, 0, 0, 0, imgPixels.width, imgPixels.height);
    return canvas.toDataURL();
}