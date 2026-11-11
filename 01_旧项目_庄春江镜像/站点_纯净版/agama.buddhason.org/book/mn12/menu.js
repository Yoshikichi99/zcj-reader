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
	{ text: "目　次", url: "mn12i.htm" },
	{ text: "評　　介　呂勝強/自　序/凡　例", url: "mn1200.htm" },
	{ text: "第　一選　佛陀的教學內容：《說處經》（八六）", url: "mn1201.htm" },
	{ text: "第　二選　諸佛所說正要--四聖諦：《象跡喻經》（三０）", url: "mn1202.htm" },
	{ text: "第　三選　佛法的不共理則--因緣：《嗏帝經》（二０一）", url: "mn1203.htm" },
	{ text: "第　四選　佛法的價值觀（一）--正念當下：《阿難說經》（一六七）", url: "mn1204.htm" },
	{ text: "第　五選　佛法的價值觀（二）--離欲：《苦陰經》（九九）", url: "mn1205.htm" },
	{ text: "第　六選　佛法的價值觀（三）--無記：《箭喻經》（二二一）", url: "mn1206.htm" },
	{ text: "第　七選　佛法的業報觀：《惒破經》（一二）", url: "mn1207.htm" },
	{ text: "第　八選　佛法的修道次第：《七車經》（九）", url: "mn1208.htm" },
	{ text: "第　九選　佛法的修行方法（一）--四念處：《念處經》（九八）", url: "mn1209.htm" },
	{ text: "第　十選　佛法的修行方法（二）：《小空經》（一九０）", url: "mn1210.htm" },
	{ text: "第十一選　佛法的修行方法（三）：《大空經》（一九一）", url: "mn1211.htm" },
	{ text: "第十二選　阿羅漢的人間關懷：《梵志陀然經》（二七）", url: "mn1212.htm" },
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
	document.writeln('		<div class="yui-skin-sam" style="margin: 0 auto; width:350px;">');
	document.writeln('            <div id="productsandservices" class="yuimenubar yuimenubarnav"> ');
	document.writeln('                <div class="bd" style="display:inline;"> ');
	document.writeln('                    <ul class="first-of-type"> ');
	document.writeln('                        <li class="yuimenubaritem first-of-type"> ');
	document.writeln('                            <a class="yuimenubaritemlabel" href="../../index.htm">首 頁</a> ');
	document.writeln('                        </li> ');
	document.writeln('                        <li class="yuimenubaritem"> ');
	document.writeln('                            <a class="yuimenubaritemlabel" href="mn12i.htm">目 錄</a> ');
	document.writeln('                        </li>');

    var myurl=window.location.toString();       // 取得網址
    if (myurl.match(/mn12(\d\d).htm/) != null) // 網址有三位數才需要下一則及上一則
    {
        var sutranum = RegExp.$1;           // 取出經號

        var next_sutra = parseInt(sutranum,10) + 1; // 下一則
        if(next_sutra > 12) {next_sutra = 0;}  // 超過106經就回到 0 (序)
        next_sutra = "00" + next_sutra.toString();
        next_sutra = next_sutra.replace(/^.*(\d\d)/,"$1");

        var pre_sutra = parseInt(sutranum,10) - 1;  // 前一則
        if(pre_sutra < 0)  {pre_sutra = 12;}
        pre_sutra = "00" + pre_sutra.toString();
        pre_sutra = pre_sutra.replace(/^.*(\d\d)/,"$1");

        document.writeln('                        <li class="yuimenubaritem"> ');
        document.writeln('                            <a class="yuimenubaritemlabel" href="mn12' + pre_sutra + '.htm">上一選</a> ');
        document.writeln('                        </li>');
        
        document.writeln('                        <li class="yuimenubaritem"> ');
        document.writeln('                            <a class="yuimenubaritemlabel" href="mn12' + next_sutra + '.htm">下一選</a> ');
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
