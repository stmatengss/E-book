// JavaScript Document
$(function(){
	//print all book
	$('.container').on('click',function(e){
			location.href="1";				   
		});
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