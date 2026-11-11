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
	{ text: "本站理念", url: "/AgAs.htm" },
	{ text: "南北傳雜阿含經對讀", url: "/SA/index.htm" },
	{ text: "南北傳中阿含經對讀", url: "/MA/index.htm" },
	{ text: "漢譯阿含經辭典", url: "/ad/index.htm" },
	{ text: "影音下載", url: "http://agama.buddhason.org/d.htm", 
	submenu: { 
		id: "download", 
		itemdata: [
			{ text: "專　題", url: "/d.htm" },
			{ text: "印順導師著作《正聞篇》", url: "/cxdl.htm" },
			{ text: "印順導師著《原始佛教聖典之集成》", url: "/esdl.htm" },
			{ text: "《阿含經故事選》mp3有聲書", url: "/asdl.htm" },
			{ text: "《南、北傳阿含經選讀》", url: "/ardl.htm" },
			{ text: "呂勝強老師課程影音", url: "/video/xs/xsdl.htm" },	
			] 
		}
	},
	{ text: "索書‧建議‧留言", url: "/le/le.htm" }, 
 ]
},
{ id: "book", 
  itemdata: [ 
	{ text: "學佛的基本認識", url: "/book/bb/bbi.htm",
	submenu: { 
		id: "bb", 
		itemdata: [
			{ text: "目　次", url: "/book/bb/bbi.htm" },
			{ text: "序", url: "/book/bb/bb01.htm" },
			{ text: "自　　序", url: "/book/bb/bb02.htm" },
			{ text: "第一章　佛法的特質", url: "/book/bb/bb11.htm" },
			{ text: "　第一節　佛陀之所以為佛陀", url: "/book/bb/bb11.htm" },
			{ text: "　第二節　緣起法下的三法印與空", url: "/book/bb/bb12.htm" },
			{ text: "　第三節　佛法是理性的宗教", url: "/book/bb/bb13.htm" },
			{ text: "第二章　生命之流", url: "/book/bb/bb21.htm" },
			{ text: "　第一節　生從何來死往何去", url: "/book/bb/bb21.htm" },
			{ text: "　第二節　無我下的輪迴", url: "/book/bb/bb22.htm" },
			{ text: "　第三節　業力的形成與展現", url: "/book/bb/bb23.htm" },
			{ text: "　第四節　人身難得", url: "/book/bb/bb24.htm" },
			{ text: "第三章　流傳人間的佛法", url: "/book/bb/bb31.htm" },
			{ text: "　第一節　佛陀的初轉法輪-- 四聖諦與八正道", url: "/book/bb/bb31.htm" },
			{ text: "　第二節　佛教經律論的成立", url: "/book/bb/bb32.htm" },
			{ text: "　第三節　佛教思想史概觀", url: "/book/bb/bb33.htm" },
			{ text: "第四章　認識自我", url: "/book/bb/bb41.htm" },
			{ text: "　第一節　人與人性的剖析", url: "/book/bb/bb41.htm" },
			{ text: "　第二節　我們的認識發展過程", url: "/book/bb/bb42.htm" },
			{ text: "第五章　生活中的佛法", url: "/book/bb/bb51.htm" },
			{ text: "　第一節　六根律儀", url: "/book/bb/bb51.htm" },
			{ text: "　第二節　對治與調伏", url: "/book/bb/bb52.htm" },
			{ text: "　第三節　專注與覺察", url: "/book/bb/bb53.htm" },
			{ text: "第六章　聖者之流", url: "/book/bb/bb61.htm" },
			{ text: "第七章　大乘菩薩行", url: "/book/bb/bb71.htm" },
			{ text: "　第一節　菩薩行與大乘佛教的開展", url: "/book/bb/bb71.htm" },
			{ text: "　第二節　偉大的菩薩行", url: "/book/bb/bb72.htm" },
			{ text: "第八章　歸依與受戒", url: "/book/bb/bb81.htm" },
			] 
		}
	},
	{ text: "印度佛教思想史要略", url: "/book/buhis/buhisi.htm",
	submenu: { 
		id: "buhis", 
		itemdata: [
			{ text: "目　次", url: "/book/buhis/buhisi.htm" },
			{ text: "印度佛教史地理圖略", url: "/book/buhis/indomap.htm" },
			{ text: "印度佛教記事略表", url: "/book/buhis/t0.htm" },
			{ text: "序‧呂勝強", url: "/book/buhis/buhis0a.htm" },
			{ text: "自序", url: "/book/buhis/buhis0b.htm" },
			{ text: "第一章　印度的宗教文明", url: "/book/buhis/buhis11.htm" },
			{ text: "　第一節　總　說", url: "/book/buhis/buhis11.htm" },
			{ text: "　第二節　婆羅門教的思想", url: "/book/buhis/buhis12.htm" },
			{ text: "　第三節　新興教派的思想", url: "/book/buhis/buhis13.htm" },
			{ text: "　第四節　印度教的思想/思考/引用資料", url: "/book/buhis/buhis14.htm" },
			{ text: "第二章　佛教的興起及其思想", url: "/book/buhis/buhis21.htm" },
			{ text: "　第一節　總　說", url: "/book/buhis/buhis21.htm" },
			{ text: "　第二節　阿含經的思想", url: "/book/buhis/buhis22.htm" },
			{ text: "　第三節　戒律的精神/思考/引用資料", url: "/book/buhis/buhis23.htm" },
			{ text: "第三章　佛教僧團的分化", url: "/book/buhis/buhis31.htm" },
			{ text: "　第一節　總　說", url: "/book/buhis/buhis31.htm" },
			{ text: "　第二節　僧團分化的原因", url: "/book/buhis/buhis32.htm" },
			{ text: "　第三節　部派思想大義/思考/引用資料", url: "/book/buhis/buhis33.htm" },
			{ text: "第四章　大乘佛教的興起及其思想", url: "/book/buhis/buhis41.htm" },
			{ text: "　第一節　總　說", url: "/book/buhis/buhis41.htm" },
			{ text: "　第二節　念佛與淨土思想", url: "/book/buhis/buhis42.htm" },
			{ text: "　第三節　中觀大乘及其思想", url: "/book/buhis/buhis43.htm" },
			{ text: "　第四節　瑜伽大乘及其思想", url: "/book/buhis/buhis44.htm" },
			{ text: "　第五節　如來藏思想/思考/引用資料", url: "/book/buhis/buhis45.htm" },
			{ text: "第五章　秘密大乘佛教的興起及其思想", url: "/book/buhis/buhis51.htm" },
			{ text: "　第一節　總　說", url: "/book/buhis/buhis51.htm" },
			{ text: "　第二節　秘密大乘佛教的思想/思考/引用資料", url: "/book/buhis/buhis52.htm" },
			{ text: "第六章　抉 擇/思考/引用資料", url: "/book/buhis/buhis6.htm" },
			] 
		}
	},
	{ text: "阿含經故事選", url: "/book/as/asi.htm",
	submenu: { 
		id: "as", 
		itemdata: [
			{ text: "目　次", url: "/book/as/as000.htm" },
			{ text: "序(呂勝強) / 自　序", url: "/book/as/as000.htm" },
			{ text: "第一篇　佛", url: "",
			submenu: { 
				id: "as01", 
				itemdata: [
					{ text: "001.怎樣才是真正的讚歎佛陀？", url: "/book/as/as001.htm" },
					{ text: "002.佛陀的修學歷程", url: "/book/as/as002.htm" },
					{ text: "003.佛陀的初轉法輪", url: "/book/as/as003.htm" },
					{ text: "004.拒絕利用神通傳教的佛陀", url: "/book/as/as004.htm" },
					{ text: "005.能成就無量福道的教誡教化", url: "/book/as/as005.htm" },
					{ text: "006.如何知道聖者", url: "/book/as/as006.htm" },
					{ text: "007.聖者的恬靜淡泊性格", url: "/book/as/as007.htm" },
					{ text: "008.佛陀如何面對謾罵", url: "/book/as/as008.htm" },
					{ text: "009.久離恐怖的佛陀", url: "/book/as/as009.htm" },
					{ text: "010.不聞雷聲的讚歎", url: "/book/as/as010.htm" },
					{ text: "011.對佛陀最誠敬的供養", url: "/book/as/as011.htm" },
					{ text: "012.佛滅後的「大師」", url: "/book/as/as012.htm" },
					{ text: "013.佛陀普渡眾生了嗎？", url: "/book/as/as013.htm" },
					] 
				}
			},
			{ text: "第二篇　法", url: "",
			submenu: { 
				id: "as02", 
				itemdata: [
					{ text: "014.緣起甚深", url: "/book/as/as014.htm" },
					{ text: "015.神射手的啟示──深徹的四聖諦", url: "/book/as/as015.htm" },
					{ text: "016.法最尊貴而不是血統──正法中沒有種族歧視", url: "/book/as/as016.htm" },
					{ text: "017.無關年資的非時通達", url: "/book/as/as017.htm" },
					{ text: "018.登頂之美", url: "/book/as/as018.htm" },
					{ text: "019.耕一種不一樣的田", url: "/book/as/as019.htm" },
					{ text: "020.善知識與精進不放逸", url: "/book/as/as020.htm" },
					{ text: "021.彌醯的獨修挫折", url: "/book/as/as021.htm" },
					{ text: "022.貧窮的財主摩訶男", url: "/book/as/as022.htm" },
					{ text: "023.金縷衣的布施", url: "/book/as/as023.htm" },
					{ text: "024.作福不嫌多，但用於解脫", url: "/book/as/as024.htm" },
					{ text: "025.人心不足", url: "/book/as/as025.htm" },
					{ text: "026.苦從哪裡來？", url: "/book/as/as026.htm" },
					{ text: "027.有愛就有痛苦", url: "/book/as/as027.htm" },
					{ text: "028.文荼王的喪妻之痛", url: "/book/as/as028.htm" },
					{ text: "029.就像接連中了兩支毒箭", url: "/book/as/as029.htm" },
					{ text: "030.佛陀受了風寒", url: "/book/as/as030.htm" },
					{ text: "031.身苦心不苦", url: "/book/as/as031.htm" },
					{ text: "032.在黑牛與白牛之間", url: "/book/as/as032.htm" },
					{ text: "033.大師就說調伏欲貪", url: "/book/as/as033.htm" },
					{ text: "034.以欲愛斷欲愛", url: "/book/as/as034.htm" },
					{ text: "035.法尚應捨，何況非法的感官欲樂──阿梨吒比丘的邪見", url: "/book/as/as035.htm" },
					{ text: "036.優填那王的讚歎──性慾的降服方法", url: "/book/as/as036.htm" },
					{ text: "037.同理心──自通之法", url: "/book/as/as037.htm" },
					{ text: "038.鹿住優婆夷的疑惑", url: "/book/as/as038.htm" },
					{ text: "039.佛法的修根", url: "/book/as/as039.htm" },
					{ text: "040.時時刻刻不染著", url: "/book/as/as040.htm" },
					{ text: "041.鷹與猴的死亡之路", url: "/book/as/as041.htm" },
					{ text: "042.在竹竿上特技表演的啟示", url: "/book/as/as042.htm" },
					{ text: "043.就像六隻不同類的動物", url: "/book/as/as043.htm" },
					{ text: "044.就像馴服一頭牛", url: "/book/as/as044.htm" },
					{ text: "045.安般念的教說因緣", url: "/book/as/as045.htm" },
					{ text: "046.都說止觀二法", url: "/book/as/as046.htm" },
					{ text: "047.就像郵遞馬車的次第接力", url: "/book/as/as047.htm" },
					{ text: "048.逐層突破的觀空法── 小空經的觀法", url: "/book/as/as048.htm" },
					{ text: "049.一舉突破的觀空法── 大空經的觀法", url: "/book/as/as049.htm" },
					{ text: "050.死亡的壓迫", url: "/book/as/as050.htm" },
					{ text: "051.勇猛銳利的隨死念", url: "/book/as/as051.htm" },
					{ text: "052.擔心來生嗎？", url: "/book/as/as052.htm" },
					{ text: "053.誰來享用祭品？", url: "/book/as/as053.htm" },
					{ text: "054.藝人塔羅布吒的悲泣", url: "/book/as/as054.htm" },
					{ text: "055.佛陀的無記回答", url: "/book/as/as055.htm" },
					{ text: "056.不能導向涅槃的無記──一個治療箭傷的譬喻", url: "/book/as/as056.htm" },
					{ text: "057.佛陀的沈默回應", url: "/book/as/as057.htm" },
					{ text: "058.眾多邪見的原因", url: "/book/as/as058.htm" },
					{ text: "059.有真我嗎？──薩遮迦的論辯挑戰（之一）", url: "/book/as/as059.htm" },
					{ text: "060.午睡是癡的表現嗎？──薩遮迦的論辯挑戰（之二）", url: "/book/as/as060.htm" },
					{ text: "061.焰摩迦的我見", url: "/book/as/as061.htm" },
					{ text: "062.誰受苦樂", url: "/book/as/as062.htm" },
					{ text: "063.同一個識在輪迴嗎？──嗏帝比丘的邪見", url: "/book/as/as063.htm" },
					{ text: "064.只能依附身心生存的識", url: "/book/as/as064.htm" },
					{ text: "065.遍尋不著瞿低迦的識", url: "/book/as/as065.htm" },
					{ text: "066.自以為是創造主的大梵天王", url: "/book/as/as066.htm" },
					{ text: "067.企圖找尋世界邊緣的赤馬仙", url: "/book/as/as067.htm" },
					{ text: "068.愚蠢的善宿", url: "/book/as/as068.htm" },
					{ text: "069.複雜的業報", url: "/book/as/as069.htm" },
					{ text: "070.[和＋心]破錯誤的惡業報應論", url: "/book/as/as070.htm" },
					{ text: "071.淳陀所喜歡的清淨修行法門──浮起來啊！石頭", url: "/book/as/as071.htm" },
					{ text: "072.意業為最重──優婆離外道居士的歸依", url: "/book/as/as072.htm" },
					{ text: "073.說與不說之間", url: "/book/as/as073.htm" },
					{ text: "074.興邦衛國的七不衰法", url: "/book/as/as074.htm" },
					{ text: "075.戰爭與勝負", url: "/book/as/as075.htm" },
					{ text: "076.念佛等六念法門的開示", url: "/book/as/as076.htm" },
					{ text: "077.在家居士的安樂八法", url: "/book/as/as077.htm" },
					] 
				}
			},
			{ text: "第三篇　僧伽", url: "",
			submenu: { 
				id: "as03", 
				itemdata: [
					{ text: "078.舍利弗的得解脫", url: "/book/as/as078.htm" },
					{ text: "079.舍利弗對昔日老友的關懷", url: "/book/as/as079.htm" },
					{ text: "080.無不散的筵席", url: "/book/as/as080.htm" },
					{ text: "081.舍利弗的「深信」", url: "/book/as/as081.htm" },
					{ text: "082.不要只是相信", url: "/book/as/as082.htm" },
					{ text: "083.質多羅居士的不必相信佛陀所說", url: "/book/as/as083.htm" },
					{ text: "084.二十億耳的精進", url: "/book/as/as084.htm" },
					{ text: "085.勇者富樓那", url: "/book/as/as085.htm" },
					{ text: "086.病比丘的看護", url: "/book/as/as086.htm" },
					{ text: "087.差摩比丘的病中證悟", url: "/book/as/as087.htm" },
					{ text: "088.銳利的阿支羅迦葉──朝聞道，朝入涅槃", url: "/book/as/as088.htm" },
					{ text: "089.須深盜法", url: "/book/as/as089.htm" },
					{ text: "090.見井水的準解脫者", url: "/book/as/as090.htm" },
					{ text: "091.面不改色的優波先那", url: "/book/as/as091.htm" },
					{ text: "092.縈髮目揵連的參訪", url: "/book/as/as092.htm" },
					{ text: "093.殺人魔鴦掘利摩羅的得解脫", url: "/book/as/as093.htm" },
					{ text: "094.朱利槃特的成就", url: "/book/as/as094.htm" },
					{ text: "095.佛陀對羅[目+侯]羅的教導", url: "/book/as/as095.htm" },
					{ text: "096.弗區沙提的奇遇", url: "/book/as/as096.htm" },
					{ text: "097.誰先見佛陀", url: "/book/as/as097.htm" },
					{ text: "098.闡陀的證入", url: "/book/as/as098.htm" },
					{ text: "099.善於說法的優陀夷", url: "/book/as/as099.htm" },
					{ text: "100.證初果的天帝釋", url: "/book/as/as100.htm" },
					{ text: "101.摩訶男捨身為眾的菩薩行典範", url: "/book/as/as101.htm" },
					{ text: "102.善於領導統御的手長者", url: "/book/as/as102.htm" },
					{ text: "103.師子將軍的歸依", url: "/book/as/as103.htm" },
					{ text: "104.瞻波城的布薩事件", url: "/book/as/as104.htm" },
					{ text: "105.拘睒彌地方僧團的紛爭──六和敬的教說", url: "/book/as/as105.htm" },
					{ text: "106.耆那教分裂的警惕──滅諍七法的教說", url: "/book/as/as106.htm" },
					] 
				}
			},
			] 
		}
	},
	{ text: "雜阿含經二十選", url: "/book/nn20/nn20i.htm",
	submenu: { 
		id: "nn20", 
		itemdata: [
			{ text: "目　次", url: "/book/nn20/nn20i.htm" },
			{ text: "序　/自　序/大綱表解", url: "/book/nn20/nn200.htm" },
			{ text: "第　一選　無明蓋，愛結繫　267(50)[44]", url: "/book/nn20/nn201.htm" },
			{ text: "第　二選　不如實知是無明　258(41)[35]", url: "/book/nn20/nn202.htm" },
			{ text: "第　三選　五蘊如實知--七處三觀經　42(154)[88]", url: "/book/nn20/nn203.htm" },
			{ text: "第　四選　六入處如實知--六分別六入處經　305(407)[283]", url: "/book/nn20/nn204.htm" },
			{ text: "第　五選　我見是無明　62(59)[53]", url: "/book/nn20/nn205.htm" },
			{ text: "第　六選　是我、異我、相在--焰摩迦所答經　104(172)[106]", url: "/book/nn20/nn206.htm" },
			{ text: "第　七選　欲令如是、不如是　33(145)[79]", url: "/book/nn20/nn207.htm" },
			{ text: "第　八選　欲愛是繫--黑牛與白牛　250(376)[252]", url: "/book/nn20/nn208.htm" },
			{ text: "第　九選　五蘊斷--攀緣四識住　39(151)[85]", url: "/book/nn20/nn209.htm" },
			{ text: "第十　選　六入處斷--四品法經　245(357)[247]", url: "/book/nn20/nn2010.htm" },
			{ text: "第十一選　先知法住，後知涅槃--須深盜法　347(489)[346]", url: "/book/nn20/nn2011.htm" },
			{ text: "第十二選　因緣觀--論因說因　53(165)[99]", url: "/book/nn20/nn2012.htm" },
			{ text: "第十三選　無常觀　265(48)[42]", url: "/book/nn20/nn2013.htm" },
			{ text: "第十四選　出入息念　803(1084)[815]", url: "/book/nn20/nn2014.htm" },
			{ text: "第十五選　沙門四果　797(1067)[809]", url: "/book/nn20/nn2015.htm" },
			{ text: "第十六選　閉根門，食知量--難陀品德　275(398)[274]", url: "/book/nn20/nn2016.htm" },
			{ text: "第十七選　忍辱不報復　311(413)[289]", url: "/book/nn20/nn2017.htm" },
			{ text: "第十八選　身苦，心不苦--不被第二毒箭　107(175)[109]", url: "/book/nn20/nn2018.htm" },
			{ text: "第十九選　隨時觀照--清淨乞食住　236(309)[238]", url: "/book/nn20/nn2019.htm" },
			{ text: "第二十選　自依、法依、莫異依　638(812)[652]", url: "/book/nn20/nn2020.htm" },
			] 
		}
	},
	{ text: "中阿含經十二選", url: "/book/mn12/mn12i.htm",
	submenu: { 
		id: "mn12", 
		itemdata: [
			{ text: "目　次", url: "/book/mn12/mn12i.htm" },
			{ text: "評　　介 (呂勝強)", url: "/book/mn12/mn120a.htm" },
			{ text: "自　　序/凡　　例", url: "/book/mn12/mn120b.htm" },
			{ text: "第　一選　佛陀的教學內容：《說處經》（八六）", url: "/book/mn12/mn1201.htm" },
			{ text: "第　二選　諸佛所說正要--四聖諦：《象跡喻經》（三○）", url: "/book/mn12/mn1202.htm" },
			{ text: "第　三選　佛法的不共理則--因緣：《嗏帝經》（二○一）", url: "/book/mn12/mn1203.htm" },
			{ text: "第　四選　佛法的價值觀（一）--正念當下：《阿難說經》（一六七）", url: "/book/mn12/mn1204.htm" },
			{ text: "第　五選　佛法的價值觀（二）--離欲：《苦陰經》（九九）", url: "/book/mn12/mn1205.htm" },
			{ text: "第　六選　佛法的價值觀（三）--無記：《箭喻經》（二二一）", url: "/book/mn12/mn1206.htm" },
			{ text: "第　七選　佛法的業報觀：《[和+心]破經》（一二）", url: "/book/mn12/mn1207.htm" },
			{ text: "第　八選　佛法的修道次第：《七車經》（九）", url: "/book/mn12/mn1208.htm" },
			{ text: "第　九選　佛法的修行方法（一）--四念處：《念處經》（九八）", url: "/book/mn12/mn1209.htm" },
			{ text: "第　十選　佛法的修行方法（二）：《小空經》（一九○）", url: "/book/mn12/mn1210.htm" },
			{ text: "第十一選　佛法的修行方法（三）：《大空經》（一九一）", url: "/book/mn12/mn1211.htm" },
			{ text: "第十二選　阿羅漢的人間關懷：《梵志陀然經》（二七）", url: "/book/mn12/mn1212.htm" },
			] 
		}
	},
	{ text: "阿含經隨身剪輯", url: "/book/tb/tbi.htm",
	submenu: { 
		id: "tb", 
		itemdata: [
			{ text: "目　次", url: "/book/tb/tbi.htm" },
			{ text: "阿含經隨身剪輯序(釋宏印)", url: "/book/tb/tb00a.htm" },
			{ text: "自　序", url: "/book/tb/tb00b.htm" },
			{ text: "前　言(呂勝強)", url: "/book/tb/tb00c.htm" },
			{ text: "凡　例", url: "/book/tb/tb00d.htm" },
			{ text: "　一、不放逸(選經1～7)", url: "/book/tb/tb01.htm" },
			{ text: "　二、守護(選經8～19)", url: "/book/tb/tb02.htm" },
			{ text: "　三、心(選經20～29)", url: "/book/tb/tb03.htm" },
			{ text: "　四、解脫的聖者(選經30～40)", url: "/book/tb/tb04.htm" },
			{ text: "　五、死(選經41～46)", url: "/book/tb/tb05.htm" },
			{ text: "　六、業報(選經47～52)", url: "/book/tb/tb06.htm" },
			{ text: "　七、欲愛(選經53～76)", url: "/book/tb/tb07.htm" },
			{ text: "　八、對治(選經77～87)", url: "/book/tb/tb08.htm" },
			{ text: "　九、止諍(選經88～93)", url: "/book/tb/tb09.htm" },
			{ text: "　十、次第(選經94～100)", url: "/book/tb/tb10.htm" },
			{ text: "十一、無常(選經101～109)", url: "/book/tb/tb11.htm" },
			{ text: "十二、因緣(選經110～124)", url: "/book/tb/tb12.htm" },
			{ text: "十三、四諦(選經125～127)", url: "/book/tb/tb13.htm" },
			{ text: "十四、味患離(選經128～131)", url: "/book/tb/tb14.htm" },
			{ text: "十五、四念處(選經132～137)", url: "/book/tb/tb15.htm" },
			{ text: "十六、念佛(選經138～142)", url: "/book/tb/tb16.htm" },
			{ text: "十七、其它(選經143～164)", url: "/book/tb/tb17.htm" },
			{ text: "一分鐘正思維", url: "/book/tb/tb18.htm" },
			{ text: "檢　索", url: "/book/tb/tb19.htm" },
			{ text: "經號索引", url: "/book/tb/tb20.htm" },
			] 
		}
	},
	{ text: "阿姜查與阿姜佛使的禪修世界", url: "/book/aps/apsi.htm",
	submenu: { 
		id: "aps", 
		itemdata: [
			{ text: "目　次", url: "/book/aps/apsi.htm" },
			{ text: "《阿姜 查的禪修世界》編輯說明", url: "/book/aps/aps0.htm" },
			{ text: "　　一、正見", url: "/book/aps/aps1.htm" },
			{ text: "　　二、調身（息）", url: "/book/aps/aps2.htm" },
			{ text: "　　三、調心", url: "/book/aps/aps3.htm" },
			{ text: "　　四、觀", url: "/book/aps/aps4.htm" },
			{ text: "　　五、境界與體驗", url: "/book/aps/aps5.htm" },
			{ text: "《阿姜 佛使的禪修世界》編輯說明", url: "/book/aps/aps10.htm" },
			{ text: "　　一、正見", url: "/book/aps/aps11.htm" },
			{ text: "　　二、不執著", url: "/book/aps/aps12.htm" },
			{ text: "　　三、無我、無我所", url: "/book/aps/aps13.htm" },
			{ text: "　　四、生活中的佛法", url: "/book/aps/aps14.htm" },
			{ text: "　　五、禪法", url: "/book/aps/aps15.htm" },
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
	document.writeln('<div style="margin: 0 auto; width: 80%;">');
	document.writeln('	<div style="align:center;">');
	document.writeln('		<!-- 選單開始 -->');
	document.writeln('		<div class="yui-skin-sam" style="margin: 0 auto; width:260px;">');
	document.writeln('            <div id="productsandservices" class="yuimenubar yuimenubarnav"> ');
	document.writeln('                <div class="bd" style="display:inline;"> ');
	document.writeln('                    <ul class="first-of-type"> ');
	document.writeln('                        <li class="yuimenubaritem first-of-type"> ');
	document.writeln('                            <a class="yuimenubaritemlabel" href="/">莊春江工作站　首 頁</a> ');
	document.writeln('                        </li> ');
	document.writeln('                        <li class="yuimenubaritem"> ');
	document.writeln('                            <a class="yuimenubaritemlabel" href="#">書　目</a> ');
	document.writeln('                        </li>');
	document.writeln('                    </ul> ');
	document.writeln('                </div> ');
	document.writeln('            </div> ');
	document.writeln('		</div>');
	document.writeln('		<!-- 選單結束 -->');
	document.writeln('	</div>');
	document.writeln('	<div style="align:left;">');
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

function show_foot2()
{
	document.writeln('<hr>');
	document.writeln('		<div >莊春江工作站 Copyright &copy; 2011</div>');
	document.writeln('		<br>');
	document.writeln('	</div>');
	document.writeln('</div>');	
}