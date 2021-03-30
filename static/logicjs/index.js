(function($){
var APP=function(){
	var self=this;
	
	/* ************************ */
	/* 			  Form			*/
	/* ************************ */
	self.Form=function(){
		/* ************************ */
		/* 		 Private - Form		*/
		/* ************************ */
		var Form=this;
		
		/* ************************ */
		/* 		 PUBLIC - Form		*/
		/* ************************ */
		Form.isEmail=function(email){   
			return email.match(/^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,})$/);
		};
		
		Form.isEmpty=function(variable){
			return (typeof variable==="undefined" || variable===null || variable.length===0 || (typeof variable.trim==="function" && variable.trim()==="") );
		};
		
		Form.haveWhitespaces=function(variable) {   
		    var espacio=[" ","\n","\t","\r"];
		    if(!Form.isEmpty(variable))
				for(var i=0; i<variable.length; i++)
					if(espacio.indexOf( variable.substring(i,i+1) ) != -1)
						return true;
		    return false;
		};
		Form.bindError=function(node){
			var $inputNode=self.Page.getNode(node);
			if($inputNode[0].type!=="submit"){
				if($inputNode[0].nodeName=="OPTION")
					$inputNode=$inputNode.parent();
				$inputNode.addClass("input_error");
				if($inputNode[0].type==="checkbox" || $inputNode[0].type==="radio" || $inputNode[0].type==="select-one" || $inputNode[0].type==="select-multiple")
					$inputNode.bind("change.inputError",function(){
						$inputNode.removeClass("input_error");
						$inputNode.unbind("change.inputError");
					});
				else if($inputNode[0].type!=="submit")
					$inputNode.bind("keyup.inputError",function(){
						$inputNode.removeClass("input_error");
						$inputNode.unbind("keyup.inputError");
					});
			}
		};
		Form.unbindError=function(node){
			var $inputNode=self.Page.getNode(node);
			if($inputNode[0].type!=="submit"){
				if($inputNode[0].nodeName=="OPTION")
					$inputNode=$inputNode.parent();
				$inputNode.removeClass("input_error");
				if($inputNode[0].type==="checkbox" || $inputNode[0].type==="radio" || $inputNode[0].type==="select-one" || $inputNode[0].type==="select-multiple")
					$inputNode.unbind("change.inputError");
				else if($inputNode[0].type!=="submit")
					$inputNode.unbind("keyup.inputError");
			}
		};
		//Dump all values into array, form can be an ID, html or jQuery node
		Form.getFields=function(form, validate){
			var $form=self.Page.getNode(form),
				focusMe=[];
			if(validate===undefined) validate=true;
			//console.log($form)
			if($form){
				var values={},
					valid=true;
				
				$form.find(":input").each(function(index,el){
					var $this=$(this);
					if(this.type==="radio"){
						if(this.checked)
							if($form.find("input[name="+this.name+"]").length>0)
								values[this.name]=$this.val();
							else
								values[this.id]=$this.val();
					}else if(this.type==="checkbox"){
						values[this.id]=this.checked;
					}else{
						if(this.type==="email" && !Form.isEmail(this.value) && this.required!==false ){
							valid=false;
							if(validate){
								Form.bindError(this);
								focusMe.push(this);
							}
						}else
							values[this.id]=$this.val();
					}
						
					if( $this.attr("required")!==undefined )
						if((this.type==="radio" || this.type==="checkbox") && !this.checked){
							if(validate){
								Form.bindError(this);
								focusMe.push(this);
							}
							valid=false;
							//alert("id: "+this.id+", name: "+this.name+", required:"+$this.attr("required"))
						}else{
							if(Form.isEmpty(this.value) || (this.type==="email" && !Form.isEmail(this.value)) || ($this.attr("placeholder")!==undefined && $this.attr("placeholder")===$this.val()) ){
								valid=false;
								if(validate){
									Form.bindError(this);
									focusMe.push(this);
								}
							}else
								if(validate)
									Form.unbindError(this);
						}
				});
				
				if(validate){
					if(valid)
						return values;
					else{
						$(focusMe[0]).focus();
						return null;
					}
				}else
					return values;
			}else
				return null;
		};
		
		/* ************************ */
		/* 	  CONSTRUCTOR - Form	*/
		/* ************************ */
		(function(){})();
	};
	
	/* ************************ */
	/* 		  	 Page  			*/
	/* ************************ */
	self.Page=function(){
		/* ************************ */
		/* 	  	 PRIVATE - Page		*/
		/* ************************ */
		var Page=this,
			_$img=null;
		
		/* ************************ */
		/* 	  	 PUBLIC - Page 		*/
		/* ************************ */
		//Show loading animation
		Page.loading=function(state,top,left,context){
			if(state===true && !_$img){
				_$img=$("<img src='"+base_url+"img/loading_big.gif' />").css({
					position:"absolute",
					zIndex:999,
					left:left||0,
					top:top||0
				});
				//console.log(context)
				if(!context)
					var context=self.Controller.getContext("index");
				//console.log(context)
				if(context.top!=window && context!=document)
					if(typeof context.append==="undefined")
						$(context).append(_$img);
					else
						context.append(_$img);
				else
					$("body").append(_$img);
			}else if(_$img){
				_$img.remove();
				_$img=null;
			}
		};
		//Block section
		Page.block=function(node){
			Page.getNode(node).css("opacity","0.4").css("pointer-events","none");
		};
		//Unblock section
		Page.unblock=function(node){
			Page.getNode(node).css("opacity","1").css("pointer-events","all");
		};
		//Get jQuery node
		Page.getNode=function(nodeThing,context){
			var $node=null,
				$context=context ? $(context) : $(self.Controller.getContext());
			if(typeof nodeThing!=="undefined"){
				if(typeof nodeThing==="string") //ID
					$node=$context.find("#"+nodeThing);
				else
					if(nodeThing.get===undefined) //html node
						$node=$(nodeThing);
					else //jQuery nodes
						$node=nodeThing;
			}
			return $node;
		};

		/* ************************ */
		/*   	CONSTRUCTOR - Page	*/
		/* ************************ */
		(function(){})();
	};
	
	/* ************************ */
	/* 		  Controller		*/
	/* ************************ */
	self.Controller=function(){
		/* ************************ */
		/* 	 PRIVATE - Controller	*/
		/* ************************ */
		var Controller=this,
			_stack={
				main	: null,
				after	: [],
				before	: []
			},
			_namespace={},
			_cache={
				controllers	: [],
				context	: [
					{
						page : "index",
						node : document
					}
				]
			};
		
		/* ************************ */
		/* 	 PUBLIC - Controller	*/
		/* ************************ */
		//Store Window context
		Controller.setContext=function(page,context){
			//console.log(arguments)
			var i=_cache.context.length,
				found=false;
			while(i--)
				if(page==_cache.context[i].page)
					found=i;
			if(found===false)
				_cache.context.push({
						page : page,
						node : context
					});
			else
				_cache.context[found].node=context;
		};
		Controller.getContext=function(page){
			var i=_cache.context.length,
				found=false;
			while(i--)
				if(page==_cache.context[i].page)
					found=i;
			
			return found!==false ? _cache.context[found].node : Controller.getContext("index") ;
		};
		//Store JS code after load
		Controller.after=function(controllerName){
			_stack.after.push( controllerName );
		};
		//Store JS code before load
		Controller.before=function(controllerName){
			_stack.before.push( controllerName );
		};
		//Store JS code before load
		Controller.main=function(controllerName){
			_stack.main = controllerName;
		};
		//Add extra stuff
		Controller.putExtra=function(object){
			$.extend(_namespace, object);
		};
		//Excecute all stored JS controllers code when loaded
		Controller.ready=function(mainFunction){
			
			for(var i=0; i<_stack.before.length; i++)
				for(var j=0; j<_cache.controllers.length; j++)
					if( _cache.controllers[j].name === _stack.before[i] )
						Controller.execute(_cache.controllers[j].name);
			
			if( _stack.main )
				Controller.execute( _stack.main );
			
			for(var i=0; i<_stack.after.length; i++)
				for(var j=0; j<_cache.controllers.length; j++)
					if( _cache.controllers[j].name === _stack.after[i] )
						Controller.execute(_cache.controllers[j].name);
			
			_stack.before=[];
			_stack.after=[];
			
		};
		//Load JS controller script
		Controller.load=function(name){
			name=name||actual_loc;
			
			if( Controller.exist(name)!==false ){
				
				Controller.main( name );
				Controller.ready();
				
			}else{
				
				$.cachedScript=function(url,options){
					options = $.extend(options||{},{
				    	dataType: "script",
				    	cache: self.settings.cache,
				    	url: url
				  	});
					return jQuery.ajax(options);
				};
				
				$.cachedScript(base_url+'logicjs/'+name+'.js').done(function(script){
					
					//Controller.execute( name );
					//Controller.main( name, _cache.controllers.length-1);
					
					if( _cache.main!==undefined )
						Controller.main( name );
					Controller.ready();
					
				});
				
			}
		};
		
		Controller.exist = function(controllerName){
			
			var found=false;
			
			for(var i=0;i<_cache.controllers.length;i++){
				if(controllerName==_cache.controllers[i].name)
					found=i;
			}
			
			return found;
			
		};
		
		Controller.execute = function(controllerName, args){
			
			var found=Controller.exist(controllerName);
			
			if( found!==false ){
				var args=[_namespace].concat( args || [] );
				
				_cache.controllers[ found ].start.apply( _cache.controllers[ found ], args );
			}//else
				//console.log("Controller not found: "+controllerName);
			
		};
		
		Controller.Model=function(controllerName, contextName, stackName, fnc){
			this.name		=  typeof contextName==="string" ? controllerName : "js-xp_"+_cache.controllers.lenght;
			this.context	= Controller.getContext( typeof contextName==="string" ? contextName : "index" );
			
			if( stackName==="after" || stackName==="before" || stackName==="main" )
				this.stack	= stackName;
			else
				this.stack	= "after";
			
			this.start		= typeof fnc==="function" ? fnc : function(){/*console.log("Malformed Controller");*/};
			this.APP		= self;
			this._			= _namespace;
			
			/* ****************************** */
			/* CONSTRUCTOR - Controller.Model */
			/* ****************************** */
			(function(){
				
				switch(stackName){
					case 'before':
						Controller.before( controllerName );
						break;
					case 'after':
						Controller.after( controllerName );
						break;
					case 'main':
						Controller.main( controllerName );
						break;
					case 'execute':
						Controller.execute( controllerName );
						break;
					//default:
						//console.log("Doing nothing")
				}
				
			})();
		};
		
		Controller.push = function(settings, fnc){
			
			var controller = new Controller.Model(settings.name, settings.context, settings.stack, fnc);
			
			_cache.controllers.push( controller );
			
		};
		
		/* ************************ */
		/* CONSTRUCTOR - Controller */
		/* ************************ */
		(function(){})();
	};
	
	
	/* ************************ */
	/* 	  PUBLIC - Start APP	*/
	/* ************************ */
	self.start=function(settings, onAPPStart){	
		self.settings=settings;
		//Window vars
		window.console = window.console!==null ? window.console : { log: function() {} };
		window.base_url = settings.base_url;
		window.ria_url = settings.ria_url;
		window.actual_loc = settings.actual_loc;
		window.isMobile = settings.isMobile;
		//Init Page Controller
		self.Page=new self.Page();
		//Init Form Controller
		self.Form=new self.Form();
		//APP callback
		$(document).ready(function(){
			//Init APP Controller
			self.Controller.setContext(settings.page||actual_loc, this);
			self.Controller.load(settings.page||actual_loc);
			onAPPStart();
		});
		//Destroy start
		self.start=function(page,context){
			if(typeof context==='object')
				self.Controller.setContext(page,context);
			self.Controller.load(page);
		};
	};
			
	
	/* ************************ */
	/* 		CONSTRUCTOR - APP	*/
	/* ************************ */
	(function(){
		
		//Init App Controller
		self.Controller=new self.Controller();
		
		function displaySize(){
			var wH = $(window).width();
			self.display = wH<701 ? "min" : wH<901 ? "med" : "max";
		}
        displaySize();
		$(window).resize(displaySize);
		
	})();
	
};

if(typeof window.APP==="undefined")
	window.APP=new APP();
	
})(jQuery);