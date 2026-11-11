
var in_word_div = 0;	// 判斷滑鼠是不是在文字的範圍中
var in_note_div = 0;	// 判斷滑鼠是不是在註解視窗的範圍中, 當不在這二個範圍中時, 註解視窗就消失

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

var aSubmenuData = [
{ id: "main", 
	itemdata: [
	{ text: "首　頁", url: "../../index.htm" },	{ text: "本站理念", url: "../../AgAs.htm" },	{ text: "阿含經南北傳對讀", url: "",
	submenu: { 		id: "agamanikaya", 		itemdata: [			{ text: "雜阿含經南北傳對讀", url: "../../SA/index.htm" },			{ text: "中阿含經南北傳對讀", url: "../../MA/index.htm" },			{ text: "長阿含經南北傳對讀", url: "../../DA/index.htm" },			{ text: "增壹阿含經南北傳對讀", url: "../../AA/index.htm" },			] 		}	},	{ text: "南傳四部", url: "",
	submenu: { 		id: "nikaya", 		itemdata: [			{ text: "相應部", url: "../../SN/index.htm" },			{ text: "中部", url: "../../MN/index.htm" },			{ text: "長部", url: "../../DN/index.htm" },			{ text: "增支部", url: "../../AN/index.htm" },			] 		}	},	{ text: "我的最愛/日常的省察", url: "../../anf.htm" },	{ text: "簡易巴利語經文解讀自學", url: "../../study/index.htm" },	{ text: "漢譯阿含經辭典", url: "../../ad/index.htm" },	{ text: "簡要巴漢辭典", url: "../../study/note.htm" },	{ text: "學佛的基本認識", url: "../../book/bb/bbi.htm"},	{ text: "印度佛教思想史要略", url: "../../book/buhis/buhisi.htm"},	{ text: "阿含經故事選", url: "../../book/as/asi.htm" },	{ text: "雜阿含經二十選", url: "../../book/nn20/nn20i.htm" },	{ text: "中阿含經十二選", url: "../../book/mn12/mn12i.htm" },	{ text: "阿含經隨身剪輯", url: "../../book/tb/tbi.htm" },	{ text: "下載與留言", url: "../../le/le.htm" },  ]
},
{ id: "book", 
	itemdata: [ 
	{ text: "目　次", url: "bbi.htm" },
	{ text: "序　仁俊 長老/自　序", url: "bb00.htm" },
	{ text: "第一章　佛法的特質", url: "bb01.htm" },
	{ text: "　第一節　佛陀之所以為佛陀", url: "bb01.htm" },
	{ text: "　第二節　緣起法下的三法印與空", url: "bb02.htm" },
	{ text: "　第三節　佛法是理性的宗教", url: "bb03.htm" },
	{ text: "第二章　生命之流", url: "bb04.htm" },
	{ text: "　第一節　生從何來死往何去", url: "bb04.htm" },
	{ text: "　第二節　無我下的輪迴", url: "bb05.htm" },
	{ text: "　第三節　業力的形成與展現", url: "bb06.htm" },
	{ text: "　第四節　人身難得", url: "bb07.htm" },
	{ text: "第三章　流傳人間的佛法", url: "bb08.htm" },
	{ text: "　第一節　佛陀的初轉法輪──四聖諦與八正道", url: "bb08.htm" },
	{ text: "　第二節　佛教經律論的成立", url: "bb09.htm" },
	{ text: "　第三節　佛教思想史概觀", url: "bb10.htm" },
	{ text: "第四章　認識自我", url: "bb11.htm" },
	{ text: "　第一節　人與人性的剖析", url: "bb11.htm" },
	{ text: "　第二節　我們的認識發展過程", url: "bb12.htm" },
	{ text: "第五章　生活中的佛法", url: "bb13.htm" },
	{ text: "　第一節　六根律儀", url: "bb13.htm" },
	{ text: "　第二節　對治與調伏", url: "bb14.htm" },
	{ text: "　第三節　專注與覺察", url: "bb15.htm" },
	{ text: "第六章　聖者之流", url: "bb16.htm" },
	{ text: "第七章　大乘菩薩行", url: "bb17.htm" },
	{ text: "　第一節　菩薩行與大乘佛教的開展", url: "bb17.htm" },
	{ text: "　第二節　偉大的菩薩行", url: "bb18.htm" },
	{ text: "第八章　歸依與受戒", url: "bb19.htm" },
	{ text: "雜　附(1)　佛陀十號的釐清", url: "bb20.htm" },
	{ text: "雜　附(2)　世尊譯詞的探討", url: "bb21.htm" },
	{ text: "雜　附(3)　依負面情緒實踐四諦", url: "bb22.htm" },
	{ text: "雜　附(4)　學習實踐如理作意", url: "bb23.htm" },
	{ text: "雜　附(5)　南北傳名色分析表", url: "bb24.htm" },
	{ text: "雜　附(6)　六識的依處", url: "bb25.htm" },
	{ text: "雜　附(7)　假想與如實", url: "bb26.htm" },
	{ text: "雜　附(8)　七清淨源流", url: "bb27.htm" },
	{ text: "雜　附(9)　消業", url: "bb28.htm" },
	{ text: "雜　附(10)　往生業", url: "bb29.htm" },
	{ text: "雜　附(11)　阿含中的修道次第", url: "bb30.htm" },
	{ text: "雜　附(12)　阿含中聞法時證初果的案例", url: "bb31.htm" },
	{ text: "轉　載　　入定要訣", url: "bb32.htm" },
 ]
},
];
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
		
		my_initial();
    });
}

function show_menu()
{
	document.writeln('<div style="margin: 0 auto; width: 100%;">');
	document.writeln('	<div style="align:center;">');
	document.writeln('		<!-- 選單開始 -->');
	document.writeln('		<div class="yui-skin-sam" style="margin: 0 auto; width:350px;">');
	document.writeln('            <div id="productsandservices" class="yuimenubar yuimenubarnav"> ');
	document.writeln('                <div class="bd" style="display:inline;"> ');
	document.writeln('                    <ul class="first-of-type"> ');
	document.writeln('                        <li class="yuimenubaritem first-of-type"> ');
	document.writeln('                            <a class="yuimenubaritemlabel" href="../../index.htm">首 頁</a> ');
	document.writeln('                        </li> ');
	document.writeln('                        <li class="yuimenubaritem"> ');
	document.writeln('                            <a class="yuimenubaritemlabel" href="bbi.htm">目 錄</a> ');
	document.writeln('                        </li>');

    var myurl=window.location.toString();       // 取得網址
    if (myurl.match(/bb(\d\d).htm/) != null) // 網址有三位數才需要下一則及上一則
    {
        var sutranum = RegExp.$1;           // 取出經號

        var next_sutra = parseInt(sutranum,10) + 1; // 下一則
        if(next_sutra > 32) {next_sutra = 0;}  // 超過32就回到 0 (序)
        next_sutra = "00" + next_sutra.toString();
        next_sutra = next_sutra.replace(/^.*(\d\d)/,"$1");

        var pre_sutra = parseInt(sutranum,10) - 1;  // 前一則
        if(pre_sutra < 0)  {pre_sutra = 32;}
        pre_sutra = "00" + pre_sutra.toString();
        pre_sutra = pre_sutra.replace(/^.*(\d\d)/,"$1");

        document.writeln('                        <li class="yuimenubaritem"> ');
        document.writeln('                            <a class="yuimenubaritemlabel" href="bb' + pre_sutra + '.htm">上一節</a> ');
        document.writeln('                        </li>');
        
        document.writeln('                        <li class="yuimenubaritem"> ');
        document.writeln('                            <a class="yuimenubaritemlabel" href="bb' + next_sutra + '.htm">下一節</a> ');
        document.writeln('                        </li>');
    }

	document.writeln('                    </ul> ');
	document.writeln('                </div> ');
	document.writeln('            </div> ');
	document.writeln('		</div>');
	document.writeln('		<!-- 選單結束 -->');
	document.writeln('	</div>');
	document.writeln('	<div style="align:left;">');
}

function show_foot()
{
	document.writeln('<hr>');
	document.writeln('		<div >莊春江工作站</div>');
	document.writeln('		<br>');
	document.writeln('	</div>');
	document.writeln('</div>');	
}

// 滑鼠移到註解時要秀出註解視窗

function my_initial()
{
	$("#notediv").mouseover(function(){ in_note_div = 1; });	// 記錄滑鼠移入註解視窗
    $("#notediv").mouseout(function(){ in_note_div = 0; });		// 記錄滑鼠移開註解視窗
	
	// 處理滑鼠移到主視窗的文字時, 要檢查此時是不是要取消註解視窗
	$("body").mouseover(function(){ check_note_div(); });
}

function note_over(num,num2)
{
    in_word_div = 1;                // 表示滑鼠進入 名相文字
    // 先指定滑鼠 onMouseOut 的行為, 讓視窗消失
    $(this).mouseout(function(){
        in_word_div = 0;
    });
    if(num2 == null) num2 = num;
    mynote = "#note" + num;
    mylink = "#link" + num2;
	$("#notediv").html($(mynote).html());
	$("#notediv").show();
	$("#notediv").css("top", $(mylink).position().top + 20);
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
		$("#notediv").css("top", $(mylink).position().top + 20);
	}
}

// 滑鼠移出註解數字就讓註解視窗消失

function note_out(num)
{
	// 不需要了, 在 check_note_div() 檢查
	//$("#notediv").hide();
}

function check_note_div()
{
	if (in_word_div == 0 && in_note_div == 0)
	{
		$("#notediv").hide();
	}
	else
	{
		$("#notediv").show();
	}
}

var in_word_div = 0;	// 判斷滑鼠是不是在文字的範圍中
function do_some_thing () 
{
	$(document).ready(function()
	{
	$('head').append('<meta http-equiv="expires" content="-1">');
	$('head').append('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">');
    	add_agama_link("#maindiv");
	});
}

// 經號連結
function add_agama_link(obj_div)
{
	var mycomp = $(obj_div).html();
	mycomp=mycomp.replace(/SA\.(\d+)/g, function(word,str1)
	{
		var mynum = "0000" + str1.toString();
		mynum = mynum.replace(/^.*(\d\d\d\d)/,"$1");
		mynum = '<a href="../../SA/SA' + mynum + '.htm" target="xxx">SA.' + str1.toString() + '</a>';
		//mynum = '<a href="../../SA/SA' + mynum + '.htm" target="xxx" style="color:#3366FF">SA.' + str1.toString() + '</a>';
  		return mynum;
  	}
	);

	mycomp=mycomp.replace(/MA\.(\d+)/g, function(word,str1)
	{
		var mynum = "000" + str1.toString();
		mynum = mynum.replace(/^.*(\d\d\d)/,"$1");
		mynum = '<a href="../../MA/MA' + mynum + '.htm" target="xxx">MA.' + str1.toString() + '</a>';
  		return mynum;
  	}
	);

	mycomp=mycomp.replace(/DA\.(\d+)/g, function(word,str1)
	{
		var mynum = "00" + str1.toString();
		mynum = mynum.replace(/^.*(\d\d)/,"$1");
		mynum = '<a href="../../DA/DA' + mynum + '.htm" target="xxx">DA.' + str1.toString() + '</a>';
  		return mynum;
  	}
	);

	mycomp=mycomp.replace(/AA\.(\d+\.\d+)/g, function(word,str1)
	 {
		mynum = '<a href="../../AA/dm.php?keyword=' +str1+'" target="xxx">AA.' + str1 + '</a>';
  		return mynum;
  	}
  	);

	mycomp=mycomp.replace(/SN\.(\d+\.\d+)/g, function(word,str1)
	 {
		mynum = '<a href="../../SN/sn.php?keyword=' +str1+'" target="xxx">SN.' + str1 + '</a>';
  		return mynum;
  	}
  	);

	mycomp=mycomp.replace(/MN\.(\d+)/g, function(word,str1)
	 {
		mynum = '<a href="../../MN/dm.php?keyword=' +str1+'" target="xxx">MN.' + str1 + '</a>';
  		return mynum;
  	}
  	);

	mycomp=mycomp.replace(/DN\.(\d+)/g, function(word,str1)
	 {
		mynum = '<a href="../../DN/dm.php?keyword=' +str1+'" target="xxx">DN.' + str1 + '</a>';
  		return mynum;
  	}
  	);

	mycomp=mycomp.replace(/AN\.(\d+\.\d+)/g, function(word,str1)
	 {
		mynum = '<a href="../../AN/an.php?keyword=' +str1+'" target="xxx">AN.' + str1 + '</a>';
  		return mynum;
  	}
  	);
  	$(obj_div).html(mycomp);

}
