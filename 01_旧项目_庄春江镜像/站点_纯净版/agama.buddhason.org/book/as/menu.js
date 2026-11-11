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
	{ text: "目　次", url: "asi.htm" },
	{ text: "序(呂勝強) / 自　序", url: "as000.htm" },
	{ text: "第1選～第10選", url: "",
	submenu: { 
		id: "as01", 
		itemdata: [
			{ text: "001.怎樣才是真正的讚歎佛陀？", url: "as001.htm" },
			{ text: "002.佛陀的修學歷程", url: "as002.htm" },
			{ text: "003.佛陀的初轉法輪", url: "as003.htm" },
			{ text: "004.拒絕利用神通傳教的佛陀", url: "as004.htm" },
			{ text: "005.能成就無量福道的教誡教化", url: "as005.htm" },
			{ text: "006.如何知道聖者", url: "as006.htm" },
			{ text: "007.聖者的恬靜淡泊性格", url: "as007.htm" },
			{ text: "008.佛陀如何面對謾罵", url: "as008.htm" },
			{ text: "009.久離恐怖的佛陀", url: "as009.htm" },
			{ text: "010.不聞雷聲的讚歎", url: "as010.htm" },
			] 
		}
	},
	{ text: "第11選～第20選", url: "",
	submenu: { 
		id: "as02", 
		itemdata: [
			{ text: "011.對佛陀最誠敬的供養", url: "as011.htm" },
			{ text: "012.佛滅後的「大師」", url: "as012.htm" },
			{ text: "013.佛陀普渡眾生了嗎？", url: "as013.htm" },
			{ text: "014.緣起甚深", url: "as014.htm" },
			{ text: "015.神射手的啟示──深徹的四聖諦", url: "as015.htm" },
			{ text: "016.法最尊貴而不是血統──正法中沒有種族歧視", url: "as016.htm" },
			{ text: "017.無關年資的非時通達", url: "as017.htm" },
			{ text: "018.登頂之美", url: "as018.htm" },
			{ text: "019.耕一種不一樣的田", url: "as019.htm" },
			{ text: "020.善知識與精進不放逸", url: "as020.htm" },
			] 
		}
	},
	{ text: "第21選～第30選", url: "",
	submenu: { 
		id: "as03", 
		itemdata: [
			{ text: "021.彌醯的獨修挫折", url: "as021.htm" },
			{ text: "022.貧窮的財主摩訶男", url: "as022.htm" },
			{ text: "023.金縷衣的布施", url: "as023.htm" },
			{ text: "024.作福不嫌多，但用於解脫", url: "as024.htm" },
			{ text: "025.人心不足", url: "as025.htm" },
			{ text: "026.苦從哪裡來？", url: "as026.htm" },
			{ text: "027.有愛就有痛苦", url: "as027.htm" },
			{ text: "028.文荼王的喪妻之痛", url: "as028.htm" },
			{ text: "029.就像接連中了兩支毒箭", url: "as029.htm" },
			{ text: "030.佛陀受了風寒", url: "as030.htm" },
			] 
		}
	},
	{ text: "第31選～第40選", url: "",
	submenu: { 
		id: "as04", 
		itemdata: [
			{ text: "031.身苦心不苦", url: "as031.htm" },
			{ text: "032.在黑牛與白牛之間", url: "as032.htm" },
			{ text: "033.大師就說調伏欲貪", url: "as033.htm" },
			{ text: "034.以欲愛斷欲愛", url: "as034.htm" },
			{ text: "035.法尚應捨，何況非法的感官欲樂──阿梨吒比丘的邪見", url: "as035.htm" },
			{ text: "036.優填那王的讚歎──性慾的降服方法", url: "as036.htm" },
			{ text: "037.同理心──自通之法", url: "as037.htm" },
			{ text: "038.鹿住優婆夷的疑惑", url: "as038.htm" },
			{ text: "039.佛法的修根", url: "as039.htm" },
			{ text: "040.時時刻刻不染著", url: "as040.htm" },
			] 
		}
	},
	{ text: "第41選～第50選", url: "",
	submenu: { 
		id: "as05", 
		itemdata: [
			{ text: "041.鷹與猴的死亡之路", url: "as041.htm" },
			{ text: "042.在竹竿上特技表演的啟示", url: "as042.htm" },
			{ text: "043.就像六隻不同類的動物", url: "as043.htm" },
			{ text: "044.就像馴服一頭牛", url: "as044.htm" },
			{ text: "045.安般念的教說因緣", url: "as045.htm" },
			{ text: "046.都說止觀二法", url: "as046.htm" },
			{ text: "047.就像郵遞馬車的次第接力", url: "as047.htm" },
			{ text: "048.逐層突破的觀空法── 小空經的觀法", url: "as048.htm" },
			{ text: "049.一舉突破的觀空法── 大空經的觀法", url: "as049.htm" },
			{ text: "050.死亡的壓迫", url: "as050.htm" },
			] 
		}
	},
	{ text: "第51選～第60選", url: "",
	submenu: { 
		id: "as06", 
		itemdata: [
			{ text: "051.勇猛銳利的隨死念", url: "as051.htm" },
			{ text: "052.擔心來生嗎？", url: "as052.htm" },
			{ text: "053.誰來享用祭品？", url: "as053.htm" },
			{ text: "054.藝人塔羅布吒的悲泣", url: "as054.htm" },
			{ text: "055.佛陀的無記回答", url: "as055.htm" },
			{ text: "056.不能導向涅槃的無記──一個治療箭傷的譬喻", url: "as056.htm" },
			{ text: "057.佛陀的沈默回應", url: "as057.htm" },
			{ text: "058.眾多邪見的原因", url: "as058.htm" },
			{ text: "059.有真我嗎？──薩遮迦的論辯挑戰（之一）", url: "as059.htm" },
			{ text: "060.午睡是癡的表現嗎？──薩遮迦的論辯挑戰（之二）", url: "as060.htm" },
			] 
		}
	},
	{ text: "第61選～第70選", url: "",
	submenu: { 
		id: "as07", 
		itemdata: [
			{ text: "061.焰摩迦的我見", url: "as061.htm" },
			{ text: "062.誰受苦樂", url: "as062.htm" },
			{ text: "063.同一個識在輪迴嗎？──嗏帝比丘的邪見", url: "as063.htm" },
			{ text: "064.只能依附身心生存的識", url: "as064.htm" },
			{ text: "065.遍尋不著瞿低迦的識", url: "as065.htm" },
			{ text: "066.自以為是創造主的大梵天王", url: "as066.htm" },
			{ text: "067.企圖找尋世界邊緣的赤馬仙", url: "as067.htm" },
			{ text: "068.愚蠢的善宿", url: "as068.htm" },
			{ text: "069.複雜的業報", url: "as069.htm" },
			{ text: "070.惒破錯誤的惡業報應論", url: "as070.htm" },
			] 
		}
	},
	{ text: "第71選～第80選", url: "",
	submenu: { 
		id: "as08", 
		itemdata: [
			{ text: "071.淳陀所喜歡的清淨修行法門──浮起來啊！石頭", url: "as071.htm" },
			{ text: "072.意業為最重──優婆離外道居士的歸依", url: "as072.htm" },
			{ text: "073.說與不說之間", url: "as073.htm" },
			{ text: "074.興邦衛國的七不衰法", url: "as074.htm" },
			{ text: "075.戰爭與勝負", url: "as075.htm" },
			{ text: "076.念佛等六念法門的開示", url: "as076.htm" },
			{ text: "077.在家居士的安樂八法", url: "as077.htm" },
			{ text: "078.舍利弗的得解脫", url: "as078.htm" },
			{ text: "079.舍利弗對昔日老友的關懷", url: "as079.htm" },
			{ text: "080.無不散的筵席", url: "as080.htm" },
			] 
		}
	},
	{ text: "第81選～第90選", url: "",
	submenu: { 
		id: "as09", 
		itemdata: [
			{ text: "081.舍利弗的「深信」", url: "as081.htm" },
			{ text: "082.不要只是相信", url: "as082.htm" },
			{ text: "083.質多羅居士的不必相信佛陀所說", url: "as083.htm" },
			{ text: "084.二十億耳的精進", url: "as084.htm" },
			{ text: "085.勇者富樓那", url: "as085.htm" },
			{ text: "086.病比丘的看護", url: "as086.htm" },
			{ text: "087.差摩比丘的病中證悟", url: "as087.htm" },
			{ text: "088.銳利的阿支羅迦葉──朝聞道，朝入涅槃", url: "as088.htm" },
			{ text: "089.須深盜法", url: "as089.htm" },
			{ text: "090.見井水的準解脫者", url: "as090.htm" },
			] 
		}
	},
	{ text: "第91選～第106選", url: "",
	submenu: { 
		id: "as10", 
		itemdata: [
			{ text: "091.面不改色的優波先那", url: "as091.htm" },
			{ text: "092.縈髮目揵連的參訪", url: "as092.htm" },
			{ text: "093.殺人魔鴦掘利摩羅的得解脫", url: "as093.htm" },
			{ text: "094.朱利槃特的成就", url: "as094.htm" },
			{ text: "095.佛陀對羅睺羅的教導", url: "as095.htm" },
			{ text: "096.弗區沙提的奇遇", url: "as096.htm" },
			{ text: "097.誰先見佛陀", url: "as097.htm" },
			{ text: "098.闡陀的證入", url: "as098.htm" },
			{ text: "099.善於說法的優陀夷", url: "as099.htm" },
			{ text: "100.證初果的天帝釋", url: "as100.htm" },
			{ text: "101.摩訶男捨身為眾的菩薩行典範", url: "as101.htm" },
			{ text: "102.善於領導統御的手長者", url: "as102.htm" },
			{ text: "103.師子將軍的歸依", url: "as103.htm" },
			{ text: "104.瞻波城的布薩事件", url: "as104.htm" },
			{ text: "105.拘睒彌地方僧團的紛爭──六和敬的教說", url: "as105.htm" },
			{ text: "106.耆那教分裂的警惕──滅諍七法的教說", url: "as106.htm" },
			] 
		}
	},
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
	document.writeln('                            <a class="yuimenubaritemlabel" href="asi.htm">目 錄</a> ');
	document.writeln('                        </li>');

    var myurl=window.location.toString();       // 取得網址
    if (myurl.match(/as(\d\d\d).htm/) != null) // 網址有三位數才需要下一則及上一則
    {
        var sutranum = RegExp.$1;           // 取出經號

        var next_sutra = parseInt(sutranum,10) + 1; // 下一則
        if(next_sutra > 106) {next_sutra = 0;}  // 超過106經就回到 0 (序)
        next_sutra = "000" + next_sutra.toString();
        next_sutra = next_sutra.replace(/^.*(\d\d\d)/,"$1");

        var pre_sutra = parseInt(sutranum,10) - 1;  // 前一則
        if(pre_sutra < 0)  {pre_sutra = 106;}
        pre_sutra = "000" + pre_sutra.toString();
        pre_sutra = pre_sutra.replace(/^.*(\d\d\d)/,"$1");

        document.writeln('                        <li class="yuimenubaritem"> ');
        document.writeln('                            <a class="yuimenubaritemlabel" href="as' + pre_sutra + '.htm">上一選</a> ');
        document.writeln('                        </li>');
        
        document.writeln('                        <li class="yuimenubaritem"> ');
        document.writeln('                            <a class="yuimenubaritemlabel" href="as' + next_sutra + '.htm">下一選</a> ');
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
