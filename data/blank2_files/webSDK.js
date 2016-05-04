/*
	Web sdk: designed by aizhiyuan
*/

var servers = {
	settings : "",
	comments : "",
	print : ""
};

var url_templates = {
	settings : {
		get : function(id){
			var url = servers.settings + '/{0}/settings';
				url = String.format(url, id);
			return url;
		},
		insert : function(id, line, seq, top, left) {
			var url = servers.settings + '/{0}/settings?line={1}&seq={2}&top={3}&left={4}';
				url = String.format(url, id, line, seq, top, left);
			return url;
		}
	},
	comments : {
		get : function(id){
			var url = servers.settings + '/{0}/comments';
				url = String.format(url, id);
			return url;
		},
		insert : function(id){
			var url = servers.comments + '/{0}/comments';
				url = String.format(url, id);
			return url;
		},
		update : function(id){
			var url = servers.comments + '/{0}/updates';
				url = String.format(url, id);
			return url;
		}
	},
	print : {
		get : function(){
			var url = servers.print + '/print';
			return url;
		}
	}
};
