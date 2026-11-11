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
	{ text: "目　次", url: "buhisi.htm" },
	{ text: "印度佛教史地理圖略", url: "indomap.htm" },
	{ text: "印度佛教記事略表", url: "t0.htm" },
	{ text: "序‧呂勝強/自序", url: "buhis00.htm" },
	{ text: "第一章　印度的宗教文明", url: "buhis01.htm" },
	{ text: "　第一節　總　說", url: "buhis02.htm" },
	{ text: "　第二節　婆羅門教的思想", url: "buhis02.htm" },
	{ text: "　第三節　新興教派的思想", url: "buhis03.htm" },
	{ text: "　第四節　印度教的思想/思考/引用資料", url: "buhis04.htm" },
	{ text: "第二章　佛教的興起及其思想", url: "buhis05.htm" },
	{ text: "　第一節　總　說", url: "buhis05.htm" },
	{ text: "　第二節　阿含經的思想", url: "buhis06.htm" },
	{ text: "　第三節　戒律的精神/思考/引用資料", url: "buhis07.htm" },
	{ text: "第三章　佛教僧團的分化", url: "buhis08.htm" },
	{ text: "　第一節　總　說", url: "buhis08.htm" },
	{ text: "　第二節　僧團分化的原因", url: "buhis09.htm" },
	{ text: "　第三節　部派思想大義/思考/引用資料", url: "buhis10.htm" },
	{ text: "第四章　大乘佛教的興起及其思想", url: "buhis11.htm" },
	{ text: "　第一節　總　說", url: "buhis11.htm" },
	{ text: "　第二節　念佛與淨土思想", url: "buhis12.htm" },
	{ text: "　第三節　中觀大乘及其思想", url: "buhis13.htm" },
	{ text: "　第四節　瑜伽大乘及其思想", url: "buhis14.htm" },
	{ text: "　第五節　如來藏思想/思考/引用資料", url: "buhis15.htm" },
	{ text: "第五章　秘密大乘佛教的興起及其思想", url: "buhis16.htm" },
	{ text: "　第一節　總　說", url: "buhis16.htm" },
	{ text: "　第二節　秘密大乘佛教的思想/思考/引用資料", url: "buhis17.htm" },
	{ text: "第六章　抉 擇/思考/引用資料", url: "buhis18.htm" },
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
	document.writeln('                            <a class="yuimenubaritemlabel" href="buhisi.htm">目 錄</a> ');
	document.writeln('                        </li>');

    var myurl=window.location.toString();       // 取得網址
    if (myurl.match(/buhis(\d\d).htm/) != null) // 網址有三位數才需要下一則及上一則
    {
        var sutranum = RegExp.$1;           // 取出經號

        var next_sutra = parseInt(sutranum,10) + 1; // 下一則
        if(next_sutra > 18) {next_sutra = 0;}  // 超過106經就回到 0 (序)
        next_sutra = "00" + next_sutra.toString();
        next_sutra = next_sutra.replace(/^.*(\d\d)/,"$1");

        var pre_sutra = parseInt(sutranum,10) - 1;  // 前一則
        if(pre_sutra < 0)  {pre_sutra = 18;}
        pre_sutra = "00" + pre_sutra.toString();
        pre_sutra = pre_sutra.replace(/^.*(\d\d)/,"$1");

        document.writeln('                        <li class="yuimenubaritem"> ');
        document.writeln('                            <a class="yuimenubaritemlabel" href="buhis' + pre_sutra + '.htm">上一節</a> ');
        document.writeln('                        </li>');
        
        document.writeln('                        <li class="yuimenubaritem"> ');
        document.writeln('                            <a class="yuimenubaritemlabel" href="buhis' + next_sutra + '.htm">下一節</a> ');
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
