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
	{ text: "目　次", url: "nn20i.htm" },
	{ text: "序　/自　序/大綱表解", url: "nn2000.htm" },
	{ text: "第　一選　無明蓋，愛結繫　267(50)[44]", url: "nn2001.htm" },
	{ text: "第　二選　不如實知是無明　258(41)[35]", url: "nn2002.htm" },
	{ text: "第　三選　五蘊如實知--七處三觀經　42(154)[88]", url: "nn2003.htm" },
	{ text: "第　四選　六入處如實知--六分別六入處經　305(407)[283]", url: "nn2004.htm" },
	{ text: "第　五選　我見是無明　62(59)[53]", url: "nn2005.htm" },
	{ text: "第　六選　是我、異我、相在--焰摩迦所答經　104(172)[106]", url: "nn2006.htm" },
	{ text: "第　七選　欲令如是、不如是　33(145)[79]", url: "nn2007.htm" },
	{ text: "第　八選　欲愛是繫--黑牛與白牛　250(376)[252]", url: "nn2008.htm" },
	{ text: "第　九選　五蘊斷--攀緣四識住　39(151)[85]", url: "nn2009.htm" },
	{ text: "第十　選　六入處斷--四品法經　245(357)[247]", url: "nn2010.htm" },
	{ text: "第十一選　先知法住，後知涅槃--須深盜法　347(489)[346]", url: "nn2011.htm" },
	{ text: "第十二選　因緣觀--論因說因　53(165)[99]", url: "nn2012.htm" },
	{ text: "第十三選　無常觀　265(48)[42]", url: "nn2013.htm" },
	{ text: "第十四選　出入息念　803(1084)[815]", url: "nn2014.htm" },
	{ text: "第十五選　沙門四果　797(1067)[809]", url: "nn2015.htm" },
	{ text: "第十六選　閉根門，食知量--難陀品德　275(398)[274]", url: "nn2016.htm" },
	{ text: "第十七選　忍辱不報復　311(413)[289]", url: "nn2017.htm" },
	{ text: "第十八選　身苦，心不苦--不被第二毒箭　107(175)[109]", url: "nn2018.htm" },
	{ text: "第十九選　隨時觀照--清淨乞食住　236(309)[238]", url: "nn2019.htm" },
	{ text: "第二十選　自依、法依、莫異依　638(812)[652]", url: "nn2020.htm" },
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
	document.writeln('                            <a class="yuimenubaritemlabel" href="nn20i.htm">目 錄</a> ');
	document.writeln('                        </li>');

    var myurl=window.location.toString();       // 取得網址
    if (myurl.match(/nn20(\d\d).htm/) != null) // 網址有三位數才需要下一則及上一則
    {
        var sutranum = RegExp.$1;           // 取出經號

        var next_sutra = parseInt(sutranum,10) + 1; // 下一則
        if(next_sutra > 20) {next_sutra = 0;}  // 超過106經就回到 0 (序)
        next_sutra = "00" + next_sutra.toString();
        next_sutra = next_sutra.replace(/^.*(\d\d)/,"$1");

        var pre_sutra = parseInt(sutranum,10) - 1;  // 前一則
        if(pre_sutra < 0)  {pre_sutra = 20;}
        pre_sutra = "00" + pre_sutra.toString();
        pre_sutra = pre_sutra.replace(/^.*(\d\d)/,"$1");

        document.writeln('                        <li class="yuimenubaritem"> ');
        document.writeln('                            <a class="yuimenubaritemlabel" href="nn20' + pre_sutra + '.htm">上一選</a> ');
        document.writeln('                        </li>');
        
        document.writeln('                        <li class="yuimenubaritem"> ');
        document.writeln('                            <a class="yuimenubaritemlabel" href="nn20' + next_sutra + '.htm">下一選</a> ');
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

function show_foot2()
{
	document.writeln('<hr>');
	document.writeln('		<div >莊春江工作站</div>');
	document.writeln('		<br>');
	document.writeln('	</div>');
	document.writeln('</div>');	
}


function show_foot() {
    var licenseContent = 
        '<div style="text-align: center; font-size: 0.9em; margin-top: 20px; border-top: 1px solid #ccc; padding-top: 10px;">' +
            '<p style="font-size: 1.2em;">莊春江讀經站</p>' +
            '<p>本站內容由莊春江老師翻譯、整理與著述，現由家屬決議採創用 CC 授權開放分享。</p>' +
            '<p>除另有註明外，本站內容採用 ' +
                '<a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hant" target="_blank">' +
                    '創用 CC 姓名標示-非商業性-相同方式分享 4.0 國際</a> 授權條款釋出。' +
            '</p>' +
            '<a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hant" target="_blank">' +
                '<img alt="創用 CC 授權條款" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" />' +
            '</a>' +
        '</div>';

    // 嘗試尋找專門的容器，若無則直接輸出
    var container = document.getElementById('license-container');
    if (container) {
        container.innerHTML = licenseContent;
    } else {
        document.write(licenseContent);
    }
}
