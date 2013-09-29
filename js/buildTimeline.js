
$(document).ready(function(){
	console.log("dom is ready");

	
	$("#tagButton").click(function(){
		
		var tag =$('#tagInput').val();
		console.log("Tag entered = " + tag);
		getRelatedPhotos(tag, function(status){
			if (status){
				console.log("return succcess");
				
			}

		});	

	});




	
});

function getRelatedPhotos(tag, callback){
		console.log("Tag received  = " + tag);
		return callback(true);
}


