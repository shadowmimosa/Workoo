
try {
    document.execCommand('BackgroundImageCache', false, true);
}
catch (e) { }
sfHover = function () {
    var sfEls = document.getElementById("web_nav").getElementsByTagName("LI");
    for (var i = 0; i < sfEls.length; i++) {
        sfEls[i].onmouseover = function () {
            this.className = (this.className ? this.className + " " : "") + "sfhover";
        }
        sfEls[i].onmouseout = function () {
            this.className = this.className.replace(/\s*?\bsfhover\b/, "");
        }
    }
    try {
        document.getElementById("ad_show1").innerHTML = showHead1();
        document.getElementById("ad_show2").innerHTML = showHead2();
    }
    catch (e) {
    }
    //document.getElementById("ad_show3").innerHTML = showHead3();
    //资料库
    infoBaseInit();
}
window.onload = sfHover;


document.write("<script src='http://img.titan007.com/footballInfo.aspx' type='text/javascript' defer='defer'></script>");

document.writeln("<div id='topnav' style='display:none'>");
//document.writeln("<iframe src='http://news.win007.com/users/head2.aspx' scrolling='no' frameborder='0' height='25' width='100%'></iframe>");
document.writeln("</div>");


document.writeln("<div id='tops'>");
document.writeln("    <div >");
document.writeln("   <h1 id='logo'>专业体育数据</h1>");
document.write('  <ul id="web_nav">');
document.write('    <li><span><a href="http://www.win007.com/" >' + Trans("首页") + '</a></span>');
document.write('    </li>');
//document.write('    <li><span><a href="' + (LangManage.lang == 1 ? "http://live.win007.com/indexall_big.aspx" :"http://live.win007.com/indexall.aspx")+'" target="_blank" >' + Trans("即时比分") + '</a></span>');
document.write('    <li><span><a href="' + (LangManage.lang == 1 ? "http://www.win0168.com/indexall_big.aspx" : "http://www.win0168.com/indexall.aspx") + '" target="_blank" >' + Trans("即时比分") + '</a></span>');
document.write('     <UL style="WIDTH: 160px">');
//document.write('    <LI><A href="http://live.win007.com/" target="_blank">' + Trans("足球") + '</A></LI>');
//document.write('    <LI><A href="http://lq3.win007.com/nba.htm" target="_blank">' + Trans("篮球") + '</A></LI>');
//document.write('    <LI><A href="' + (LangManage.lang == 1 ? "http://www.win0168.com/indexall_big.aspx" : "http://www.win0168.com/indexall.aspx") + '" target="_blank">' + Trans("足球") + '</A></LI>');
//document.write('    <LI><A href="' + (LangManage.lang == 1 ? "http://lq.win0168.com/nba_big.htm" : "http://lq.win0168.com/nba.htm") + '" target="_blank">' + Trans("篮球") + '</A></LI>');
document.write('    <LI><A href="' + (LangManage.lang == 1 ? "http://live.win007.com/indexall_big.aspx" : "http://live.win007.com/indexall.aspx") + '" target="_blank">' + Trans("足球") + '</A></LI>');
document.write('    <LI><A href="' + (LangManage.lang == 1 ? "http://lq3.win007.com/nba_big.htm" : "http://lq3.win007.com/nba.htm") + '" target="_blank">' + Trans("篮球") + '</A></LI>');
document.write('    <LI><A href="http://bf.win007.com/tennis.htm" target="_blank">' + Trans("网球") + '</A></LI>');
document.write('    <LI><A href="http://f1.win007.com/f1_bf.aspx" target="_blank">' + Trans("赛车") + '</A></LI>');
document.write('    <LI><A href="http://sports.win007.com/vollyball.aspx" target="_blank">' + Trans("排球") + '</A></LI> ');
document.write('    <LI><A href="http://sports.win007.com/baseball.aspx" target="_blank">' + Trans("棒球") + '</A></LI>');
document.write('    <LI><A href="http://sports.win007.com/pingpong.aspx" target="_blank">' + Trans("乒乓球") + '</A></LI>');
document.write('    <LI><A href="http://sports.win007.com/shuttlecock.aspx" target="_blank">' + Trans("羽毛球") + '</A></LI>');
document.write('    <LI><A href="http://sports.win007.com/snooker.htm" target="_blank">' + Trans("斯诺克") + '</A></LI>');
document.write('    <LI><A href="http://sports.win007.com/football.aspx" target="_blank">' + Trans("橄榄球") + '</A></LI>');
document.write('    <LI><A href="http://sports.win007.com/hockey.aspx" target="_blank">' + Trans("冰球") + '</A></LI>');
document.write('    <LI><A href="http://www.jdj007.com/?from=live_win007__home_navigation" target="_blank">' + Trans("电竞") + '</A></LI>');
document.write('    </UL>');
document.write('    </li>');
document.write('    <li><span><a href="' + (LangManage.lang == 1 ? "http://jc.win007.com/index_big.aspx" : "http://jc.win007.com/index.aspx") + '" target="_blank">' + Trans("竞彩") + '</a></span><ul style="WIDTH: 90px"><li><a style="width:90px;" href="http://jc.win007.com/index.aspx" target="_blank">' + Trans("竞足") + '</a></li><li><a style="width:90px;" href="http://jc.win007.com/nba/index.aspx" target="_blank">' + Trans("竞篮") +'</a></li></ul></li>');
document.write('    <li><span><a href="http://pl.zqsos.com/" target="_blank">' + Trans("指数") + '</a></span>');
document.write('    <UL style="WIDTH: 160px">');
document.write('    <LI><A href="http://pl.zqsos.com/" target="_blank">' + Trans("足球指数") + '</A></LI>');
document.write('    <LI><A href="http://nba.win007.com/odds/index.aspx" target="_blank">' + Trans("篮球指数") + '</A></LI>');
document.write('    <LI><A href="http://op1.win007.com/" target="_blank">' + Trans("足球百家") + '</A></LI>');
document.write('    <LI><A href="http://nba.win007.com/1x2/" target="_blank">' + Trans("篮球百家") + '</A></LI>');
document.write('    <LI><A href="/' + LangManage.langName + '/League/36.html" target="_blank">' + Trans("让球盘路") + '</A></LI>');
document.write('    <LI><A href="http://pl.zqsos.com/champion/index'+(LangManage.lang==1?"_big":"")+'.aspx" target="_blank">' + Trans("冠军指数") + '</A></LI>');
document.write('    <LI><a href="http://pl.zqsos.com/betfa/index.aspx" target="_blank">' + Trans("必发指数") + '</a></LI>');
document.write('    <LI><a href="http://www.jdj007.com/bet.html?from=bet_win007_home_navigation" target="_blank">' + Trans("电竞指数") + '</a></LI>');

document.write('    </UL>');
document.write('    </li>');
document.write('    <li><span><a href="/" target="_blank">' + Trans("资料库") + '</a></span>');
document.write('    <UL style="WIDTH: 160px">');
document.write('    <LI><A href="' + (LangManage.lang == 1 ? "/info/index_big.htm" : "/") + '" target="_blank">' + Trans("足球") + '</A></LI>');
document.write('    <LI><A href="http://nba.win007.com/' + (LangManage.lang == 1 ? "index_big.htm" : "") + '" target="_blank">' + Trans("篮球") + '</A></LI>');
document.write('    <LI><A href="http://f1.win007.com/Result.aspx" target="_blank">F1</A></LI>');
document.write('    <LI><A href="http://tennis1.win007.com" target="_blank">' + Trans("网球") + '</A></LI>');
document.write('    <LI><A href="http://sports.win007.com/SnookerDB.aspx" target="_blank">' + Trans("斯诺克") + '</A></LI>');
document.write('    <LI><A href="http://sports.win007.com/BB_Default.aspx?SclassID=1" target="_blank">' + Trans("棒球") + '</A></LI>');
document.write('    <LI><A href="http://sports.win007.com/Default.aspx?SclassID=187" target="_blank">' + Trans("冰球") + '</A></LI>');
document.write('    <LI><A href="http://sports.win007.com/FB_Default.aspx?SclassID=1" target="_blank">' + Trans("美式足球") + '</A></LI>');
document.write('    <LI><A href="/' + LangManage.langName + '/League/36.html" target="_blank">' + Trans("英超") + '</A></LI>');
document.write('    <LI><A href="/' + LangManage.langName + '/League/34.html" target="_blank">' + Trans("意甲") + '</A></LI>');
document.write('    <LI><A href="/' + LangManage.langName + '/League/8.html" target="_blank">' + Trans("德甲") + '</A></LI>');
document.write('    <LI><A href="/' + LangManage.langName + '/League/31.html" target="_blank">' + Trans("西甲") + '</A></LI>');
document.write('    <LI><A href="/' + LangManage.langName + '/League/11.html" target="_blank">' + Trans("法甲") + '</A></LI>');
document.write('    <LI><A href="/' + LangManage.langName + '/CupMatch/103.html" target="_blank">' + Trans("欧冠杯") + '</A></LI>');
document.write('    <LI><A href="/' + LangManage.langName + '/League/60.html" target="_blank">' + Trans("中超") + '</A></LI>');
document.write('    <LI><A href="/' + LangManage.langName + '/CupMatch/192.html" target="_blank">' + Trans("亚冠杯") + '</A></LI>');
document.write('    <LI><A href="http://nba.win007.com/League/index_' + LangManage.langName + '.aspx?SclassID=1" target="_blank">NBA</A></LI>');
document.write('    <LI><A href="http://nba.win007.com/' + LangManage.langName + '/cupmatch.aspx?SclassID=7" target="_blank">EURO</A></LI>');
document.write('    <LI><A href="http://nba.win007.com/League/index_' + LangManage.langName + '.aspx?SclassID=5" target="_blank">CBA</A></LI>');
document.write('    <LI><A href="/' + LangManage.langName + '/zh/yingchao.html" target="_blank">' + Trans("转会记录") + '</A></LI>');
document.write('    <LI><A href="/' + LangManage.langName + '/paiming.html" target="_blank">' + Trans("世界排名") + '</A></LI>');
document.write('    <LI><A href="/' + (LangManage.lang == 1 ? "big/" : "") + 'zhibo.html" target="_blank">' + Trans("电视直播表") + '</A></LI>');
document.write('    <LI><A href="http://www.jdj007.com/leagues.html?from=leagues_win007_home_navigation" target="_blank">' + Trans("电竞") + '</A></LI>');
document.write('    </UL>');
document.write('    </li>');
document.write('    <li><span><a href="http://hao.win007.com/" target="_blank">' + Trans("球探号") + '</a></span>');
document.write('    </li>');

document.write('   <li><span><a class="ddl" href="http://guess2.win007.com/" target="_blank">' + Trans("V猜球") + '<i>&nbsp;</i></a></span><ul style="WIDTH: 90px"><li><a style="width:90px;" href="http://guess2.win007.com/" target="_blank">' + Trans("足球") + '</a></li><li><a style="width:90px;" href="http://guess2.win007.com/basket/" target="_blank">' + Trans("篮球") + '</a></li></ul>');//<li><a style="width:90px;" href="http://guess2.win007.com/jingcai/" target="_blank">' + Trans("足球竞彩王") + '</a></li><li><a style="width:90px;" href="http://guess2.win007.com/bodan/" target="_blank">' + Trans("足球波胆王") + '</a></li>
document.write('    </li>');

document.write('    <li><span><a href="http://ba2.win007.com/" target="_blank">' + Trans("球吧") + '</a></span></li>');

document.write('    <li><span><a href="http://v.win007.com/" target="_blank">V' + Trans("推荐") + '</a></span></li>');


document.write('    <li><span><a href="http://gj.win007.com/" target="_blank">' + Trans("冠军杯") + '</a></span>');
document.write('    </li>');

document.write('    <li><span><a href="http://www.saiday.com/?sid=7" target="_blank">' + Trans("球票") + '</a></span>');
document.write('    </li>');
document.write('    <li><span><a href="http://www.jdj007.com/?from=win007__home_navigation" target="_blank">' + Trans("电竞比分") + '</a></span>');
document.write('    </li>');
document.write('    </ul>');
document.writeln("  <br style='clear:both'>");
document.writeln("    </div>");
document.writeln("</div>");


//广告
document.writeln("<div style='margin-bottom:0px;width:950px;overflow: hidden;' align='center' id='ad_show1'></div>");



//广告
document.writeln("<div style='margin-bottom:5px;width:950px;overflow: hidden;' align='center' id='ad_show3'></div>");

document.writeln("<div id='subMenu'>");
document.writeln('<a class="homeBtn" href="/info/index_' + LangManage.langName + '.htm"></a>');
document.writeln("  <div class='lang'> <span  onclick='changeLang(0)' " + (LangManage.lang == 0 ? "class='on'" : "") + " >简</span> <span   onclick='changeLang(1)' " + (LangManage.lang == 1 ? "class='on'" : "") + ">繁</span></div>");// <span  onclick='changeLang(2)'>EN</span> 
//document.writeln("  <div class='phoneDownload'><a href='http://www.win007.com/app/' target='_blank'>客户端下载<a/></div>");
document.writeln("  <a href='/" + LangManage.langName + "/League/36.html'>" + Trans("英超") + "</a> | <a href='/" + LangManage.langName + "/League/31.html'>" + Trans("西甲") + "</a> | <a href='/" + LangManage.langName + "/League/8.html'>" + Trans("德甲") + "</a>  | <a href='/" + LangManage.langName + "/League/34.html'>" + Trans("意甲") + "</a>| <a href='/" + LangManage.langName + "/League/11.html'>" + Trans("法甲") + "</a> | <a href='/" + LangManage.langName + "/League/60.html'>" + Trans("中超") + "</a> | <a href='/" + LangManage.langName + "/SubLeague/25.html'>" + Trans("日职联") + "</a> | <a href='/" + LangManage.langName + "/CupMatch/192.html'>" + Trans("亚冠杯") + "</a> | <a href='/" + LangManage.langName + "/CupMatch/103.html'>" + Trans("欧冠杯") + "</a> | <a href='/" + LangManage.langName + "/zh/yingchao.html' target='_blank'>" + Trans("足球转会") + "</a> | <a href='/" + LangManage.langName + "/paiming.html'>" + Trans("世界排名") + "</a> | <a href='/" + LangManage.langName + "/paiming.html?type=2'>" + Trans("俱乐部排名") + "</a>");
document.writeln("   <br style='clear:both;'>");
document.writeln("</div>");


//广告
document.writeln("<div style='margin-top: 3px;' align='center' id='ad_show2'></div>");

function changeLang(l) {

    if (l == 2) {
        window.location.href = "http://info.nowgoal.com/football/en/league_match/league_vs/2011-2012/36.htm";
        return "";
    }

    var url = document.URL;
    var rg = /lang=\d/;
    url = url.replace(rg, "");
    if (url.indexOf("cn") == -1) {
        var rgcn_big = /big/;
        url = url.replace(rgcn_big, "cn");
    }
    else {
        var rgcn_big = /cn/;
        url = url.replace(rgcn_big, "big");
    }
    var rg1 = /com\/zhibo/;
    if (l == 0)
        url = url.replace(rg1, "com/cn/zhibo");
    else if (l == 1)
        url = url.replace(rg1, "com/big/zhibo");
    var rg2 = /com\/team/;
    if (l == 0)
        url = url.replace(rg2, "com/cn/team");
    else if (l == 1)
        url = url.replace(rg2, "com/big/team");
    window.location.href = url; 
}
//那个radio按钮显示
function loadLang(l) {

}

function searchTeamOrPlayer() {
    var str2 = document.getElementsByName("textfield")[0].value;
    if (document.getElementById("Radio2").checked == true) {
        //str1=document.getElementById("Radio1").value;
        window.open("/" + LangManage.langName + "/aspx/Search_Team.aspx?str2=" + encodeURI(str2));
    }
    if (document.getElementById("Radio1").checked == true) {
        //str1=document.getElementById("Radio2").value;
        window.open("/" + LangManage.langName + "/aspx/Search_Player.aspx?str1=" + encodeURI(str2));
    }
}