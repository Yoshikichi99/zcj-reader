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
	{ text: "首　頁", url: "../../index.htm" },
	{ text: "本站理念", url: "../../AgAs.htm" },
	{ text: "阿含經南北傳對讀", url: "",
	submenu: { 
		id: "agamanikaya", 
		itemdata: [
			{ text: "雜阿含經南北傳對讀", url: "../../SA/index.htm" },
			{ text: "中阿含經南北傳對讀", url: "../../MA/index.htm" },
			{ text: "長阿含經南北傳對讀", url: "../../DA/index.htm" },
			{ text: "增壹阿含經南北傳對讀", url: "../../AA/index.htm" },
			] 
		}
	},
	{ text: "南傳四部", url: "",
	submenu: { 
		id: "nikaya", 
		itemdata: [
			{ text: "相應部", url: "../../SN/index.htm" },
			{ text: "中部", url: "../../MN/index.htm" },
			{ text: "長部", url: "../../DN/index.htm" },
			{ text: "增支部", url: "../../AN/index.htm" },
			] 
		}
	},
	{ text: "我的最愛/日常的省察", url: "../../anf.htm" },
	{ text: "簡易巴利語經文解讀自學", url: "../../study/index.htm" },
	{ text: "漢譯阿含經辭典", url: "../../ad/index.htm" },
	{ text: "簡要巴漢辭典", url: "../../study/note.htm" },
	{ text: "學佛的基本認識", url: "../../book/bb/bbi.htm"},
	{ text: "印度佛教思想史要略", url: "../../book/buhis/buhisi.htm"},
	{ text: "阿含經故事選", url: "../../book/as/asi.htm" },
	{ text: "雜阿含經二十選", url: "../../book/nn20/nn20i.htm" },
	{ text: "中阿含經十二選", url: "../../book/mn12/mn12i.htm" },
	{ text: "阿含經隨身剪輯", url: "../../book/tb/tbi.htm" },
	{ text: "阿姜查與阿姜佛使的禪修世界", url: "../../book/aps/apsi.htm" },
	{ text: "下載與留言", url: "../../le/le.htm" }, 
 ]
},
{ id: "book", 
	itemdata: [ 
	{ text: "目　次", url: "tbi.htm" },
	{ text: "阿含經隨身剪輯序(釋宏印)", url: "tb00.htm" },
	{ text: "自　序", url: "tb01.htm" },
	{ text: "前　言(呂勝強)", url: "tb02.htm" },
	{ text: "凡　例", url: "tb03.htm" },
	{ text: "　一、不放逸(選經1～7)", url: "tb04.htm" },
	{ text: "　二、守護(選經8～19)", url: "tb05.htm" },
	{ text: "　三、心(選經20～29)", url: "tb06.htm" },
	{ text: "　四、解脫的聖者(選經30～40)", url: "tb07.htm" },
	{ text: "　五、死(選經41～46)", url: "tb08.htm" },
	{ text: "　六、業報(選經47～52)", url: "tb09.htm" },
	{ text: "　七、欲愛(選經53～76)", url: "tb10.htm" },
	{ text: "　八、對治(選經77～87)", url: "tb11.htm" },
	{ text: "　九、止諍(選經88～93)", url: "tb12.htm" },
	{ text: "　十、次第(選經94～100)", url: "tb13.htm" },
	{ text: "十一、無常(選經101～109)", url: "tb14.htm" },
	{ text: "十二、因緣(選經110～124)", url: "tb15.htm" },
	{ text: "十三、四諦(選經125～127)", url: "tb16.htm" },
	{ text: "十四、味患離(選經128～131)", url: "tb17.htm" },
	{ text: "十五、四念處(選經132～137)", url: "tb18.htm" },
	{ text: "十六、念佛(選經138～142)", url: "tb19.htm" },
	{ text: "十七、其它(選經143～164)", url: "tb20.htm" },
	{ text: "一分鐘正思維", url: "tb21.htm" },
	{ text: "檢　索", url: "tb22.htm" },
	{ text: "經號索引", url: "tb23.htm" },
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
    });
}

function show_menu()
{
	document.writeln('<div style="margin: 0 auto; width: 100%;">');
	document.writeln('	<div style="align:center;">');
	document.writeln('		<!-- 選單開始 -->');
	document.writeln('		<div class="yui-skin-sam" style="margin: 0 auto; width:450px;">');
	document.writeln('            <div id="productsandservices" class="yuimenubar yuimenubarnav"> ');
	document.writeln('                <div class="bd" style="display:inline;"> ');
	document.writeln('                    <ul class="first-of-type"> ');
	document.writeln('                        <li class="yuimenubaritem first-of-type"> ');
	document.writeln('                            <a class="yuimenubaritemlabel" href="../../index.htm">首 頁</a> ');
	document.writeln('                        </li> ');
	document.writeln('                        <li class="yuimenubaritem"> ');
	document.writeln('                            <a class="yuimenubaritemlabel" href="tbi.htm">目 錄</a> ');
	document.writeln('                        </li>');

    var myurl=window.location.toString();       // 取得網址
    if (myurl.match(/tb(\d\d).htm/) != null) // 網址有三位數才需要下一則及上一則
    {
        var sutranum = RegExp.$1;           // 取出經號

        var next_sutra = parseInt(sutranum,10) + 1; // 下一則
        if(next_sutra > 23) {next_sutra = 0;}  // 超過106經就回到 0 (序)
        next_sutra = "00" + next_sutra.toString();
        next_sutra = next_sutra.replace(/^.*(\d\d)/,"$1");

        var pre_sutra = parseInt(sutranum,10) - 1;  // 前一則
        if(pre_sutra < 0)  {pre_sutra = 23;}
        pre_sutra = "00" + pre_sutra.toString();
        pre_sutra = pre_sutra.replace(/^.*(\d\d)/,"$1");

        document.writeln('                        <li class="yuimenubaritem"> ');
        document.writeln('                            <a class="yuimenubaritemlabel" href="tb' + pre_sutra + '.htm">上一單元</a> ');
        document.writeln('                        </li>');
        
        document.writeln('                        <li class="yuimenubaritem"> ');
        document.writeln('                            <a class="yuimenubaritemlabel" href="tb' + next_sutra + '.htm">下一單元</a> ');
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
