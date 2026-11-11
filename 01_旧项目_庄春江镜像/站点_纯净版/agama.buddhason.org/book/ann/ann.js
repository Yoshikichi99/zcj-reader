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

//這是很重要的工具, 很多程式都是靠這個在執行1.<script type="text/javascript" src="../../js/jquery.js"></script>2.<script type="text/javascript" src="ann.js"></script>
// 這是程式進入點, 這樣才會執行ann.js 裡面的 do_some_thing()<script type="text/javascript">do_some_thing();</script>
//把有資料的 div 加上了 id , 取名 maindiv , 這個可以自行取名, 但不可以重複, id 必須是唯一的.<div id="maindiv" style="text-align:justify;text-justify:inter-ideograph;"> ann.js 的這一行add_agama_link("#maindiv");意思就是把 id 為 maindiv 的區塊進行處理.target="xxx"xxx 隨便取名, 表示是某個視窗, 如果該視窗不存在, 就會開新的, 若存在, 就會重複在該視窗開啟經文, 就不會開一堆了.
//\d 是數字  . 是任意字 \. 才是代表半型句點  + 表示至少一個以上 (\d+ 表示至少一個數字)  所以如果 AA 一定是有二組數字在後面, 中間有句點, 可以用 /§AA\.(\d+\.\d+)/g 如果 AA 後面可能有一組數字或 n 組, 那就可以用 /§AA\.([\d\.]+)/g   [\d\.] 表示 數字或句點  但若為了安全, 最後一個只能是數字, 也可以用/§AA\.([\d\.]*\d)/g  * 是任意數量, 包括 0,  + 是至少一個
