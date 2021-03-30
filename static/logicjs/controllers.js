/* ------ MODULE ------
 * name: inicio
 * ------------------ */
APP.Controller.push({
	name	: "inicio",
	context	: "inicio",
	stack	: "main",
	start	: false
}, function(sharedObj){
	
	console.log("inicio")
	
	APP.Controller.execute("placeholders");
	
	APP.Controller.execute("parallax");
	
	APP.Controller.execute("stickyHeader");
	
	APP.Controller.execute("stickySections");
	
	//iCheck
	if($('input').length>0)
		$('input').iCheck({
			checkboxClass: 'icheckbox_square-yellow',
			radioClass: 'iradio_square-blue',
			increaseArea: '20%'
		});
	
	//Fancybox
	if($('.fancybox').length>0)
		$(".fancybox").fancybox({
			maxWidth	: 800,
			maxHeight	: 600,
			width		: '90%',
			height		: '90%',
			autoSize	: false,
			closeClick	: false,
			openEffect	: 'none',
			closeEffect	: 'none'
		});
	
});



/* ------ MODULE ------
 * name: parallax
 * ------------------ */
APP.Controller.push({
	name	: "parallax",
	context	: "inicio"
}, function(sharedObj){
	
	$("#top_home").easyBackground().easyParallax({
		offsetX		:"50%",	//Initial X position
		offsetY		: 0,	//Initial Y position
		speedFactor	: 0.8,	//Scroll speed
	});
	
	$("#cascos").easyParallax({
		offsetX		:"50%",	//Initial X position
		offsetY		: -150,	//Initial Y position
		speedFactor	: 0.2,	//Scroll speed
		maxHeight	: 1667	//Background image height
	});
	
	$("#bateria").easyParallax({
		offsetX		:"50%",	//Initial X position
		offsetY		: -400,	//Initial Y position
		speedFactor	: 0.2,	//Scroll speed
		maxHeight	: 1600	//Background image height
	});
	
});



/* ------ MODULE ------
 * name: placeholders
 * ------------------ */
APP.Controller.push({
	name	: "placeholders",
	context	: "inicio"
}, function(sharedObj){
	
	//PLACEHOLDERS
	if (!ModernizrCustom.input.placeholder) {
	    $("input").each(function(){
	      if($(this).val()=="" && $(this).attr("placeholder")!=""){
	        $(this).val($(this).attr("placeholder"));
	        $(this).focus(function(){
	          if($(this).val()==$(this).attr("placeholder")) $(this).val("");
	        });
	        $(this).blur(function(){
	          if($(this).val()=="") $(this).val($(this).attr("placeholder"));
	        });
	      }
	    });
	    $("textarea").each(function(){
	      if($(this).val()=="" && $(this).attr("placeholder")!=""){
	        $(this).val($(this).attr("placeholder"));
	        $(this).focus(function(){
	          if($(this).val()==$(this).attr("placeholder")) $(this).val("");
	        });
	        $(this).blur(function(){
	          if($(this).val()=="") $(this).val($(this).attr("placeholder"));
	        });
	      }
	    });
	}
	//END PLACEHOLDERS
	
});



/* ------ MODULE ------
 * name: stickyHeader
 * ------------------ */
APP.Controller.push({
	name	: "stickyHeader",
	context	: "inicio"
}, function(sharedObj){
	
	//Fixed header
	$('#menu').waypoint('sticky');
	
	
	//Scroll to sections (menu)
	$("#menu nav ul li a").click(function() {
		var id = $(this).attr("href");
		$('body').scrollTo(id, {
			duration : 350,
			offset : -90
		});
	});
	
	//Scroll to top (logo)
	$("#menu div.content h1 a").click(function() {
		$('body').scrollTo("#top_home", {
			duration : 350,
			offset : -90
		});
	});
	
	//Scroll to top (arrowUp)
	$("a.arrowup").click(function() {
		$('body').scrollTo("#top_home", {
			duration : 350,
			offset : -90
		});
	});
	
});



/* ------ MODULE ------
 * name: stickySections
 * ------------------ */
APP.Controller.push({
	name	: "stickySections",
	context	: "inicio"
}, function(sharedObj){
	
	$('#music, #queHacemos, #quienesSomos, #partners, #contacto').waypoint(function(direction) {
		$("#menu nav ul li a").removeClass("on");
		switch(this.id) {
			case 'music':
				if (direction == "down")
					$($("#menu nav ul li").get(0)).find("a").addClass("on");
				break;
			case 'queHacemos':
				if (direction == "down")
					$($("#menu nav ul li").get(1)).find("a").addClass("on");
				else if (direction == "up")
					$($("#menu nav ul li").get(0)).find("a").addClass("on");
				break;
			case 'quienesSomos':
				if (direction == "down")
					$($("#menu nav ul li").get(2)).find("a").addClass("on");
				else if (direction == "up")
					$($("#menu nav ul li").get(1)).find("a").addClass("on");
				break;
			case 'partners':
				if (direction == "down")
					$($("#menu nav ul li").get(3)).find("a").addClass("on");
				else if (direction == "up")
					$($("#menu nav ul li").get(2)).find("a").addClass("on");
				break;
			case 'contacto':
				if (direction == "down")
					$($("#menu nav ul li").get(4)).find("a").addClass("on");
				else if (direction == "up")
					$($("#menu nav ul li").get(3)).find("a").addClass("on");
				break;
		}

	}, {
		offset : 250
	});

});
