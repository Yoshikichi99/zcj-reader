function init_menu () 
{
        /*
             Initialize and render the MenuBar when its elements are ready 
             to be scripted.
        */
        YAHOO.util.Event.onContentReady("productsandservices", function () {
            /*
				Instantiate a MenuBar:  The first argument passed to the constructor
				is the id for the Menu element to be created, the second is an 
				object literal of configuration properties.
            */
            var oMenuBar = new YAHOO.widget.MenuBar("productsandservices", { 
                                                        autosubmenudisplay: true, 
                                                        hidedelay: 750, 
                                                        lazyload: true });
            /*
                 Define an array of object literals, each containing 
                 the data necessary to create a submenu.
            */

        /*
             Subscribe to the "beforerender" event, adding a submenu 
             to each of the items in the MenuBar instance.
        */
        oMenuBar.subscribe("beforeRender", function () {
			var nSubmenus = aSubmenuData.length,
				i;
            if (this.getRoot() == this) {
				for (i = 0; i < nSubmenus; i++) {
                	this.getItem(i).cfg.setProperty("submenu", aSubmenuData[i]);
				}
            }
        });
        /*
             Call the "render" method with no arguments since the 
             markup for this MenuBar instance is already exists in 
             the page.
        */
        oMenuBar.render();
    });
}

// 滑鼠移到註解時要秀出註解視窗

function note_over(num)
{
	mynote = "#note" + num;
	mylink = "#link" + num;
	
	$("#notediv").html($(mynote).html());
	$("#notediv").show();
	$("#notediv").css("top", $(mylink).position().top + 30);
	$("#notediv").css("left", $(mylink).position().left);
	if($(mylink).position().left + $("#notediv").width() > $(window).width())
	{
		$("#notediv").css("left", $(window).width() - $("#notediv").width() - 30);
	}
	if($("#notediv").position().top + $("#notediv").height() - $(window).scrollTop() + 10 > $(window).height())
	{
		$("#notediv").css("top", $(mylink).position().top - $("#notediv").height() - 20);
	}
	if($("#notediv").position().top < $(window).scrollTop())
	{
		$("#notediv").css("top", $(mylink).position().top + 30);
	}
}

// 滑鼠移出註解數字就讓註解視窗消失

function note_out(num)
{
	$("#notediv").hide();
}
