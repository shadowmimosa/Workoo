
var showType = 1;
var X2 = {} //my namespace:) 
X2.Eval = function (code) {
    if (!!(window.attachEvent && !window.opera)) {
        //ie 
        execScript(code);
    } else {
        //not ie 
        window.eval(code);
    }
}
function showMenuUl(t) {
    var urlStr = "";
    if (t == 1) {
        urlStr = '<li id="menu1" class="nav_selected2" onclick="SelectScore(1)" style=" cursor:pointer">' + Trans("总积分榜") + '</li>';
        urlStr += '<li id="menu2" class="nav_unselected2" onclick="SelectScore(2)"  style=" cursor:pointer">' + Trans("主场积分") + '</li>';
        urlStr += '<li id="menu3" class="nav_unselected2" onclick="SelectScore(3)"  style=" cursor:pointer">' + Trans("客场积分") + '</li>';
        urlStr += '<li id="menu4" class="nav_unselected2" onclick="SelectScore(4)" style=" cursor:pointer">' + Trans("半场总积分") + '</li>';
        urlStr += '<li id="menu5" class="nav_unselected2" onclick="SelectScore(5)" style=" cursor:pointer">' + Trans("半场主场积分") + '</li>';
        urlStr += '<li id="menu6" class="nav_unselected2" onclick="SelectScore(6)" style=" cursor:pointer">' + Trans("半场客场积分") + '</li>';
        urlStr += '<li class="dropDiv select" id="SelectLi"><select name="dropSelect" id="dropSelect" onchange="dropSelectChange(this)"></select></li>';
    }
    else if (t == 2) {
        urlStr = '<li id="menu1" class="nav_selected2" onclick="SelectLetgoal(1)" style=" cursor:pointer">' + Trans("总盘盘路") + '</li>';
        urlStr += '<li id="menu2" class="nav_unselected2" onclick="SelectLetgoal(2)"  style=" cursor:pointer">' + Trans("主场盘路") + '</li>';
        urlStr += '<li id="menu3" class="nav_unselected2" onclick="SelectLetgoal(3)"  style=" cursor:pointer">' + Trans("客场盘路") + '</li>';
        urlStr += '<li id="menu4" class="nav_unselected2" onclick="SelectLetgoal(4)" style=" cursor:pointer">' + Trans("半场盘路") + '</li>';
        urlStr += '<li id="menu5" class="nav_unselected2" onclick="SelectLetgoal(5)" style=" cursor:pointer">' + Trans("半场主队盘路") + '</li>';
        urlStr += '<li id="menu6" class="nav_unselected2" onclick="SelectLetgoal(6)" style="cursor:pointer">' + Trans("半场客队盘路") + '</li>';
    }
    else if (t == 3) {
        urlStr = '<li id="menu1" class="nav_selected2" onclick="SelectBigSmall(1)" style=" cursor:pointer">' + Trans("总盘盘路") + '</li>';
        urlStr += '<li id="menu2" class="nav_unselected2" onclick="SelectBigSmall(2)"  style=" cursor:pointer">' + Trans("主场盘路") + '</li>';
        urlStr += '<li id="menu3" class="nav_unselected2" onclick="SelectBigSmall(3)"  style=" cursor:pointer">' + Trans("客场盘路") + '</li>';
        urlStr += '<li id="menu4" class="nav_unselected2" onclick="SelectBigSmall(4)" style=" cursor:pointer">' + Trans("半场盘路") + '</li>';
        urlStr += '<li id="menu5" class="nav_unselected2" onclick="SelectBigSmall(5)" style=" cursor:pointer">' + Trans("半场主队盘路") + '</li>';
        urlStr += '<li id="menu6" class="nav_unselected2" onclick="SelectBigSmall(6)" style=" cursor:pointer">' + Trans("半场客队盘路") + '</li>';
    }
    else if (t == 7) {
        urlStr = '<li id="menu1" class="nav_selected2" onclick="ShowAllHalfData(1)" style="cursor:pointer">' + Trans("总榜") + '</li>';
        urlStr += '<li id="menu2" class="nav_unselected2" onclick="ShowAllHalfData(2)" style="cursor:pointer">' + Trans("主场成绩") + '</li>';
        urlStr += '<li id="menu3" class="nav_unselected2" onclick="ShowAllHalfData(3)" style="cursor:pointer">' + Trans("客场成绩") + '</li>';
    }
    else if (t == 10) {
        urlStr = '<li id="menu1" class="nav_selected2" onclick="ShowOnlyWinData(1)" style="cursor:pointer">' + Trans("总成绩") + '</li>';
        urlStr += '<li id="menu2" class="nav_unselected2" onclick="ShowOnlyWinData(2)" style="cursor:pointer">' + Trans("主场成绩") + '</li>';
        urlStr += '<li id="menu3" class="nav_unselected2" onclick="ShowOnlyWinData(3)" style="cursor:pointer">' + Trans("客场成绩") + '</li>';
    }
    document.getElementById("menuUl1").innerHTML = urlStr;
    document.getElementById("menuUl1").style.display = (urlStr == "" ? "none" : "");
    document.getElementById("nav_bottom").style.display = (urlStr == "" ? "none" : "");
}
var pathList = "matchResult,letGoal,bigSmall,normal,SinDou,moreBall,allHalf,timeDistri,boDanDistri,onlyWin,firGetLose".split(',');
var nameList = "s,l,bs,nor,sd,mb,ah,td,bd,ow,fgl".split(',');
function showHtml(t) {
    showType = t;
    if (t != 4) {
        document.getElementById("norMainTitle").style.display = "none";
        document.getElementById("norMainData").style.display = "none";
    }
    showMenuUl(t);
    getData(t);
    for (var i = 1; i < 12; i++)
        document.getElementById("li" + i).className = "";
    document.getElementById("li" + t).className = "nav_on";
    document.getElementById("Table4").style.display = (t == 1 ? "" : "none");
    if (t == 2 || t == 3) {
        var obj1 = document.getElementById("countTitle1");
        var obj2 = document.getElementById("countTitle2");
        obj1.style.display = "";
        obj2.style.display = "";
        obj1.innerHTML = (t == 2 ? Trans("全场让球盘路数据统计") : Trans("全场大小球盘路数据统计"));
        obj2.innerHTML = (t == 2 ? Trans("半场让球盘路数据统计") : Trans("半场大小球盘路数据统计"));
        document.getElementById("allTongJi1").style.display = "";
        document.getElementById("allTongJi2").style.display = "";
    }
    else {
        document.getElementById("countTitle1").style.display = "none";
        document.getElementById("countTitle2").style.display = "none";
        document.getElementById("allTongJi1").style.display = "none";
        document.getElementById("allTongJi2").style.display = "none";
    }
    var strShow = (t == 1 && typeof (totalScore) == "undefined" ? "none" : "");
    document.getElementById("tableId").style.display = strShow;
    //document.getElementById("menuUl1").style.display = strShow;
    //document.getElementById("navSelectBottom").style.display = strShow;
}
function getData(t) {
    if (t == 1) {
        scoreRoundSelect(1);
        showTotalScore();
    }
    else {
        var name = "/jsData/" + pathList[t - 1] + "/" + selectSeason + "/" + nameList[t - 1] + SclassID + (SubSclassID > 0 && t == 1 ? "_" + SubSclassID : "") + ".js";
        bomHelper.ajaxGet(name, function (data) {
            //try {
            //eval(data);
            X2.Eval(data);
            scoreRoundSelect(t);
            switch (t) {
                case 1: showTotalScore(); break;
                case 2:       
                    InitTeamArr();
                    showData(TotalPanLu, "0");
                    //全场盘路数据统计
                    allTongji(addUp, 1);
                    allTongji(addUpHalf, 2);
                    break;
                case 3:
                    InitTeamArr();
                    showBigSmallData(TotalBs, 0);
                    //全场盘路数据统计
                    allTongji_bigSmall(addUp, 1);
                    allTongji_bigSmall(addUpHalf, 2);
                    break;
                case 4: ShowNormal(); break;
                case 5: ShowSinDouData(); break;
                case 6: ShowMoreBallData(); break;
                case 7: ShowAllHalfData(1); break;
                case 8: ShowTimeDistriData(); break;
                case 9: ShowBoDanDistriData(); break;
                case 10: ShowOnlyWinData(1); break;
                case 11: ShowFirResultData(); break;
            }
            //} catch (e) {

            // }
        });
    }
}
//----------------------------------------------------------------------------------------------------------------让球榜
//选择不同的数据显示不同的数据
function SelectLetgoal(point) {
    //去除颜色
    for (var i = 1; i <= 6; i++) {
        var menu = document.getElementById("menu" + i);
        if (point == i) {
            if (menu.className)
                menu.className = "nav_selected2";
            else
                menu.setAttribute("class", "nav_selected2");
        } else {
            if (menu.className)
                menu.className = "nav_unselected2";
            else
                menu.setAttribute("class", "nav_unselected2");
        }
    }
    switch (point) {
        case 1: showData(TotalPanLu, "0"); break;
        case 2: showData(HomePanLu, "1"); break;
        case 3: showData(GuestPanLu, "2"); break;
        case 4: showData(TotalHalfPanLu, "3"); break;
        case 5: showData(HomeHalfPanLu, "4"); break;
        case 6: showData(GuestHalfPanLu, "5"); break;
    }
}
//数据显示
function showData(selectPanLu, kind) {
    var dataDiv = document.getElementById("tableId");
    
    //    var teamDrop = document.getElementById("dropSelect");
    //    var teamID = teamDrop.options[teamDrop.selectedIndex].value;
    var arrDiv = new Array();
    arrDiv.push("<table id='div_Table1' width='790' border='1' cellpadding='2' cellspacing='0' style='font-size:small'  bgcolor='#FFFFFF' class='tdlink'><tr align='center' bgcolor='#D1E2F5'><td width='35'><strong>" + Trans("排名") + "</strong></td><td  height='18'><strong>" + Trans("球队名称") + "</strong></td><td width='32' ><strong>" + Trans("赛") + "</strong></td><td width='35' ><strong>" + Trans("上盘") + "</strong></td><td width='35'  ><strong>" + Trans("平盘") + "</strong></td><td width='35' ><strong>" + Trans("下盘") + "</strong></td><td width='32'><strong>" + Trans("赢") + "</strong></td><td width='32' ><strong>" + Trans("走") + "</strong></td><td width='32'  ><strong>" + Trans("输") + "</strong></td><td width='32' align='center'  ><strong>" + Trans("净") + "</strong></td><td width='50' ><strong>" + Trans("胜") + "%</strong></td><td width='50'><strong>" + Trans("走") + "%</strong></td><td width='50'  ><strong>" + Trans("负") + "%</strong></td><td width='32'><strong>" + Trans("盘路") + "</strong></td></tr>");
    for (var i = 0; i < selectPanLu.length; i++) {
        var panLu = selectPanLu[i];
        //        if (teamID > 0 && teamID != panLu[1])
        //            continue;
        try {
            arrDiv.push("<tr align='center'  height='18'><td bgcolor='#e6edf7'>" + panLu[0] + "</td><td  bgcolor='#e6edf7' align='left'>" + showScoreTeam2(panLu[1]) + "</td><td  >" + panLu[2] + "</td><td>" + panLu[3] + "</td><td>" + panLu[4] + "</td><td >" + panLu[5] + "</td><td >" + panLu[6] + "</td><td>" + panLu[7] + "</td><td >" + panLu[8] + "</td><td bgcolor='#f5dbd1'>" + panLu[9] + "</td><td>" + panLu[10] + "%</td><td>" + panLu[11] + "%</td><td >" + panLu[12] + "%</td><td><a href='/" + LangManage.langName + "/Team/HandicapDetail.aspx?sclassid=" + arrLeague[0] + "&teamid=" + panLu[1] + "&matchseason=" + selectSeason + "&halfOrAll=" + kind + "' target='_blank'>" + Trans("详情") + "</a></td></tr>");
        } catch (e) {
            document.getElementById("rightLea").style.color = "red";
        }
    }
    arrDiv.push("</table>");
    dataDiv.innerHTML = arrDiv.join('');
}

function allTongji(tongjiData, num) {
    this.showTeam = function (arrTongjiTeam) {
        var tempHtml = "";
        for (var i = 1; i < arrTongjiTeam.length; i++) {
            try {
                tempHtml += ", " + teamHelper["T_" + arrTongjiTeam[i]][1 + lang];
            } catch (e) { }
        }
        if (tempHtml == "")
            return "";
        return tempHtml.substring(2);
    }

    var allTongjiDiv = document.getElementById("allTongJi" + num);
    var arrAll = new Array();
    arrAll.push("<table  id='DivData1' width='790' border='1' cellpadding='2' cellspacing='2'  bgcolor='#FFFFFF' class='tdlink'>");
    arrAll.push("<tr><td width='30%' bgcolor='#E6EDF7'>&nbsp;" + Trans("主场赢盘") + "</td><td width='50%' align='center' class='etime'>" + tongjiData[0] + "</td><td width='20%' align='center' class='etime'>" + tongjiData[1] + "</td></tr>"); //主场赢盘
    arrAll.push("<tr><td bgcolor='#DFEAF6'>&nbsp;" + Trans("和局走水") + "</td><td bgcolor='#F0F0F0' align='center' class='etime'>" + tongjiData[2] + "</td><td bgcolor='#F0F0F0' align='center' class='etime' >" + tongjiData[3] + "</td></tr>"); //和局走水
    arrAll.push("<tr><td bgcolor='#E6EDF7'>&nbsp;" + Trans("客场赢盘") + "</td><td align='center' class='etime'>" + tongjiData[4] + "</td><td align='center' class='etime'>" + tongjiData[5] + "</td></tr>"); //客场赢盘
    arrAll.push("<tr><td bgcolor='#DFEAF6' height='10'>&nbsp;" + Trans("最佳") + "<b><span class='STYLE7'>" + Trans("投注") + "</span></b>" + Trans("球队") + "</td><td bgcolor='#F0F0F0' align='center'>" + this.showTeam(tongjiData[6]) + "</td><td bgcolor='#F0F0F0' align='center' class='etime' >" + tongjiData[6][0] + "%</td></tr>"); //最佳投注球队
    arrAll.push("<tr><td bgcolor='#E6EDF7'>&nbsp;" + Trans("避免") + "<b><span class='STYLE8'>" + Trans("投注") + "</span></b>" + Trans("球队") + "</td><td align='center'>" + this.showTeam(tongjiData[7]) + "</td><td align='center' class='etime'>" + tongjiData[7][0] + "%</td></tr>"); //避免投注球队
    arrAll.push("<tr><td bgcolor='#DFEAF6'>&nbsp;" + Trans("主场") + "<strong class='STYLE7'>" + Trans("最佳") + "</strong>" + Trans("球队") + "</td><td bgcolor='#F0F0F0' align='center'>" + this.showTeam(tongjiData[8]) + "</td><td bgcolor='#F0F0F0' align='center' class='etime'>" + tongjiData[8][0] + "%</td></tr>"); //主场最佳球队
    arrAll.push("<tr><td bgcolor='#E6EDF7'>&nbsp;" + Trans("主场") + "<strong class='STYLE8'>" + Trans("避免") + "</strong>" + Trans("球队") + "</td><td align='center'>" + this.showTeam(tongjiData[9]) + "</td><td align='center' class='etime'>" + tongjiData[9][0] + "%</td></tr>"); //主场避免球队
    arrAll.push("<tr><td bgcolor='#DFEAF6'>&nbsp;" + Trans("客场") + "<strong class='STYLE7'>" + Trans("最佳") + "</strong>" + Trans("球队") + "</td><td bgcolor='#F0F0F0' align='center'>" + this.showTeam(tongjiData[10]) + "</td><td bgcolor='#F0F0F0' align='center' class='etime'>" + tongjiData[10][0] + "%</td></tr>"); //客场最佳球队
    arrAll.push("<tr><td bgcolor='#E6EDF7'>&nbsp;" + Trans("客场") + "<strong class='STYLE8'>" + Trans("避免") + "</strong>" + Trans("球队") + "</td><td align='center'>" + this.showTeam(tongjiData[11]) + "</td><td align='center' class='etime'>" + tongjiData[11][0] + "</td></tr>"); //客场避免球队
    arrAll.push("<tr><td bgcolor='#DFEAF6'>&nbsp;" + Trans("走水") + "<strong class='STYLE7'>" + Trans("最多") + "</strong>" + Trans("球队") + "</td><td bgcolor='#F0F0F0' align='center'>" + this.showTeam(tongjiData[12]) + "</td><td bgcolor='#F0F0F0' align='center' class='etime'>" + tongjiData[12][0] + "%</td></tr>"); //走水最多球队
    arrAll.push("<tr><td bgcolor='#E6EDF7'  height='10'>&nbsp;" + Trans("走水") + "<strong class='STYLE8'>" + Trans("最少") + "</strong>" + Trans("球队") + "</td><td align='center'>" + this.showTeam(tongjiData[13]) + "</td><td   align='center' class='etime'>" + tongjiData[13][0] + "%</td></tr>"); //走水最少球队
    arrAll.push("</table>");
    allTongjiDiv.innerHTML = arrAll.join('');

}
function showScoreTeam2(teamID) {
    var html = "";
    if (lang == 2) { //英文名
        html += teamHelper["T_" + teamID][1 + lang];
    } else {
        html += teamHelper["T_" + teamID][1 + lang] + "";
    }
    html = "<a href='/" + LangManage.langName + "/team/Summary/" + teamID + ".html' target='_blank'>" + html + "</a>";
    return html;
}
//-------------------------------------------------------------------------------------------------大小球
//选择不同的数据显示不同的数据
function SelectBigSmall(point) {
    //去除颜色
    for (var i = 1; i <= 6; i++) {
        var menu = document.getElementById("menu" + i);
        if (point == i) {
            if (menu.className)
                menu.className = "nav_selected2";
            else
                menu.setAttribute("class", "nav_selected2");
        } else {
            if (menu.className)
                menu.className = "nav_unselected2";
            else
                menu.setAttribute("class", "nav_unselected2");
        }
    }
    switch (point) {
        case 1: showBigSmallData(TotalBs, 0); break;
        case 2: showBigSmallData(HomeBs, 1); break;
        case 3: showBigSmallData(GuestBs, 2); break;
        case 4: showBigSmallData(TotalBsHalf, 3); break;
        case 5: showBigSmallData(HomeBsHalf, 4); break;
        case 6: showBigSmallData(GuestBsHalf, 5); break;
    }
}
//数据显示
function showBigSmallData(selectPanLu, kind) {
    var dataDiv = document.getElementById("tableId");
    //    var teamDrop = document.getElementById("dropSelect");
    //    var teamID = teamDrop.options[teamDrop.selectedIndex].value;
    var arrDiv = new Array();
    arrDiv.push("<table id='div_Table1' width='790' border='1' cellpadding='2' cellspacing='0' style='font-size:small'  bgcolor='#FFFFFF' class='tdlink'><tr align='center' bgcolor='#D1E2F5'><td width='30'><strong>" + Trans("排名") + "</strong></td><td  height='18'><strong>" + Trans("球队名称") + "</strong></td><td width='25' ><strong>" + Trans("赛") + "</strong></td><td width='50'><strong>" + Trans("大球") + "</strong></td><td width='25' ><strong>" + Trans("走") + "</strong></td><td width='50'  ><strong>" + Trans("小球") + "</strong></td><td width='50' align='center'  ><strong>" + Trans("大球") + "%</strong></td><td width='50' ><strong>" + Trans("走") + "%</strong></td><td width='50'><strong>" + Trans("小球") + "%</strong></td><td width='28'><strong>" + Trans("盘路") + "</strong></td></tr>");
    for (var i = 0; i < selectPanLu.length; i++) {
        var panLu = selectPanLu[i];
        //        if (teamID > 0 && teamID != panLu[1])
        //            continue;
        try {
            arrDiv.push("<tr align='center'  height='18'><td bgcolor='#e6edf7'>" + panLu[0] + "</td><td  bgcolor='#e6edf7' align='left'>" + showScoreTeam2(panLu[1]) + "</td><td  >" + panLu[2] + "</td><td>" + panLu[3] + "</td><td>" + panLu[4] + "</td><td >" + panLu[5] + "</td><td >" + panLu[6] + "%</td><td>" + panLu[7] + "%</td><td >" + panLu[8] + "%</td><td><a href='/" + LangManage.langName + "/Team/OuHandicap.aspx?sclassid=" + arrLeague[0] + "&teamid=" + panLu[1] + "&matchseason=" + selectSeason + "&halfOrAll=" + kind + "' target='_blank'>" + Trans("详情") + "</a></td></tr>");
        } catch (e) {
            document.getElementById("rightLea").style.color = "red";
        }
    }
    //BigSmallBallPuDatial.aspx?sclassid=36&teamid=22&matchseason=2011-2012&kind=3
    arrDiv.push("</table>");
    dataDiv.innerHTML = arrDiv.join('');
}


function allTongji_bigSmall(tongjiData, num) {
    this.showTeam = function (arrTongjiTeam) {
        var tempHtml = "";
        for (var i = 1; i < arrTongjiTeam.length; i++) {
            try {
                tempHtml += ", " + teamHelper["T_" + arrTongjiTeam[i]][1 + lang];
            } catch (e) { }
        }
        if (tempHtml == "")
            return "";
        return tempHtml.substring(2);
    }

    var allTongjiDiv = document.getElementById("allTongJi" + num);
    var arrAll = new Array();
    arrAll.push("<table  id='DivData1' width='790' border='1' cellpadding='2' cellspacing='2'  bgcolor='#FFFFFF' class='tdlink'>");
    arrAll.push("<tr><td width='30%' bgcolor='#E6EDF7'>&nbsp;" + Trans("大球") + "</td><td width='50%' align='center' class='etime'>" + tongjiData[0] + "</td><td width='20%' align='center' class='etime'>" + tongjiData[1] + "%</td></tr>"); //大球
    arrAll.push("<tr><td bgcolor='#DFEAF6'>&nbsp;" + Trans("走水") + "</td><td bgcolor='#F0F0F0' align='center' class='etime'>" + tongjiData[2] + "</td><td bgcolor='#F0F0F0' align='center' class='etime' >" + tongjiData[3] + "%</td></tr>"); //走水
    arrAll.push("<tr><td bgcolor='#E6EDF7'>&nbsp;" + Trans("小球") + "</td><td align='center' class='etime'>" + tongjiData[4] + "</td><td align='center' class='etime'>" + tongjiData[5] + "%</td></tr>"); //小球
    arrAll.push("<tr><td bgcolor='#DFEAF6' height='10'>&nbsp;" + Trans("大球") + "<b><span class='STYLE7'>" + Trans("最多") + "</span></b>" + Trans("球队") + "</td><td bgcolor='#F0F0F0' align='center'>" + this.showTeam(tongjiData[6]) + "</td><td bgcolor='#F0F0F0' align='center' class='etime' >" + tongjiData[6][0] + "%</td></tr>"); //最佳投注球队
    arrAll.push("<tr><td bgcolor='#E6EDF7'>&nbsp;" + Trans("小球") + "<b><span class='STYLE8'>" + Trans("最多") + "</span></b>" + Trans("球队") + "</td><td align='center'>" + this.showTeam(tongjiData[7]) + "</td><td align='center' class='etime'>" + tongjiData[7][0] + "%</td></tr>"); //避免投注球队
    arrAll.push("<tr><td bgcolor='#DFEAF6'>&nbsp;" + Trans("主场") + "<strong class='STYLE7'>" + Trans("大球") + "</strong>" + Trans("最多球队") + "</td><td bgcolor='#F0F0F0' align='center'>" + this.showTeam(tongjiData[8]) + "</td><td bgcolor='#F0F0F0' align='center' class='etime'>" + tongjiData[8][0] + "%</td></tr>"); //主场最佳球队
    arrAll.push("<tr><td bgcolor='#E6EDF7'>&nbsp;" + Trans("主场") + "<strong class='STYLE8'>" + Trans("小球") + "</strong>" + Trans("最多球队") + "</td><td align='center'>" + this.showTeam(tongjiData[9]) + "</td><td align='center' class='etime'>" + tongjiData[9][0] + "%</td></tr>"); //主场避免球队
    arrAll.push("<tr><td bgcolor='#DFEAF6'>&nbsp;" + Trans("客场") + "<strong class='STYLE7'>" + Trans("大球") + "</strong>" + Trans("最多球队") + "</td><td bgcolor='#F0F0F0' align='center'>" + this.showTeam(tongjiData[10]) + "</td><td bgcolor='#F0F0F0' align='center' class='etime'>" + tongjiData[10][0] + "%</td></tr>"); //客场最佳球队
    arrAll.push("<tr><td bgcolor='#E6EDF7'>&nbsp;" + Trans("客场") + "<strong class='STYLE8'>" + Trans("小球") + "</strong>" + Trans("最多球队") + "</td><td align='center'>" + this.showTeam(tongjiData[11]) + "</td><td align='center' class='etime'>" + tongjiData[11][0] + "%</td></tr>"); //客场避免球队
    arrAll.push("</table>");
    allTongjiDiv.innerHTML = arrAll.join('');

}
//------------------------------------------------------------------------最常见赛果
function ShowNormal() {
    var mainDiv = document.getElementById("tableId");
    var arrMainDiv = new Array();
    arrMainDiv.push("<table id='div_Table1' style='display: block' width='790' border='1' cellpadding='2' cellspacing='0'  bgcolor='#ffffff' class='tdlink'><tr bgcolor='#D1E2F5'><td width='125' align='center' ><span class='STYLE4'><strong>" + Trans("赛果") + "</strong></span></td><td width='220' height='18' align='center' ><span class='STYLE4'><strong>" + Trans("场数") + "/" + Trans("总赛场数") + "</strong></span></td><td width='250' align='center'  class='STYLE4'><strong>" + Trans("比率") + "</strong></td><td width='200' align='center' ><span class='STYLE4'><strong>" + Trans("详情") + "</strong></span></td></tr>");
    for (var i = 0; i < normal.length; i++) {
        var nor = normal[i];
        //arrMainDiv.push("<tr align='center' " + (i % 2 == 0 ? "bgcolor='#eff4fa'" : "") + "><td bgcolor='#eff4fa'>" + nor[0] + ":" + nor[1] + "</td><td>" + nor[2] + "/" + nor[3] + "</td><td>" + nor[4] + "%</td><td><a href='javascript:void(0)' onclick='ShowDetail(\"v" + nor[0] + "vs" + nor[1] + "\")'>" + Trans("详情") + "</a></td></tr>");
        arrMainDiv.push("<tr align='center' " + (i % 2 == 0 ? "bgcolor='#eff4fa'" : "") + "><td bgcolor='#eff4fa'>" + nor[0] + ":" + nor[1] + "</td><td>" + nor[2] + "/" + nor[3] + "</td><td>" + nor[4] + "%</td><td><a href='/" + (lang == 0 ? "cn" : "big") + "/LNormalDetail/" + selectSeason + "/" + SclassID + "\/v" + nor[0] + "vs" + nor[1] + ".html' target='_blank' > " + Trans("详情") + "</a ></td ></tr > ");
    }
    arrMainDiv.push("</table>");
    mainDiv.innerHTML = arrMainDiv.join('');
}

function ShowDetail(id) {
    var arrDetail = new Array();
    arrDetail.push("<table width='790' border='1' cellpadding='2' cellspacing='0' bgcolor='#ffffff' class='tdlink' id='Table1'><tr><td width='76' bgcolor='#d1e2f5'><div align='center'><strong>" + Trans("赛果") + "</strong></div></td><td width='110' bgcolor='#d1e2f5' height='24'><div align='center'><strong>" + Trans("赛事时间") + "</strong></div></td><td width='162' bgcolor='#d1e2f5'><div align='center'><strong>" + Trans("主队") + "</strong></div></td><td bgcolor='#d1e2f5' width='153'><div align='center'><strong>" + Trans("客队") + "</strong></div></td><td bgcolor='#d1e2f5'><div align='center'><strong>" + Trans("半场") + "</strong></div></td></tr>");
    for (var i = 0; i < jh[id].length; i++) {
        var de = jh[id][i];
        arrDetail.push("<tr align='center' " + (i % 2 == 0 ? "bgcolor='#eff4fa'" : "") + "><td bgcolor='#eff4fa'>" + de[3] + ":" + de[4] + "</td><td>" + de[2] + "</td><td><a href='/" + LangManage.langName + "/team/Summary/" + de[0] + ".html' target='_blank'>" + teamHelper["T_" + de[0]][1 + lang] + "</a></td><td><a href='/" + LangManage.langName + "/team/Summary/" + de[1] + ".html' target='_blank'>" + teamHelper["T_" + de[1]][1 + lang] + "</a></td><td>" + de[5] + ":" + de[6] + "</td></tr>");
    }
    arrDetail.push("</table>");
    var norMainData = document.getElementById("norMainData");
    var norTitl = document.getElementById("norMainTitle");
    norMainData.innerHTML = arrDetail.join('');
    norTitl.style.display = "block";
    norMainData.style.display = "block";
}
//-------------------------------------------------------------------------入球总数及单双统计
function ShowSinDouData() {
    var mainDiv = document.getElementById("tableId");
    var arrMainDiv = new Array();
    arrMainDiv.push("<table width='790' border='1' cellpadding='2' cellspacing='0'  bgcolor='#ffffff' class='tdlink' id='Table1'><tr bgcolor='#d1e2f5' align='center'   style='font-weight:bold;'><td width='194' height='24' rowspan='2'>" + Trans("球队名称") + "</td><td colspan='7' >" + Trans("入球总数") + "</td><td colspan='2' >" + Trans("单双") + "</td></tr><tr bgcolor='#d1e2f5' align='center'   style='font-weight:bold;'><td width='48' >0球</td><td width='48' >1球 </td><td width='44' >2球 </td><td >3球 </td><td >4球 </td><td width='46' >5球 </td><td width='75' >6球以上 </td><td width='43'  >" + Trans("单数") + "</td><td width='44' >" + Trans("双数") + "</td></tr>");
    for (var i = 0; i < arrDataInfo.length; i++) {
        var nor = arrDataInfo[i];
        arrMainDiv.push("<tr align='center' " + (i % 2 == 0 ? "bgcolor='#eff4fa'" : "") + ">  <td bgcolor='#EFF4FA' height='22' class='etime' align='left'>&nbsp;<a href='/" + LangManage.langName + "/team/Summary/" + nor[0] + ".html' target='_blank'>" + teamHelper["T_" + nor[0]][1 + lang] + "</a></td><td  class='etime'>" + nor[1] + "</td>  <td  class='etime'>" + nor[2] + "</td>  <td  class='etime'>" + nor[3] + "</td>  <td width='40'  class='etime'>" + nor[4] + "</td>  <td width='48'  class='etime'>" + nor[5] + "</td>  <td  class='etime'>" + nor[6] + "</td>  <td  class='etime'>" + nor[7] + "</td>  <td bgcolor='#F5DBD1' class='etime'>" + nor[8] + "</td>  <td bgcolor='#E7F7D7'  class='etime'>" + nor[9] + "</td></tr>");
    }
    arrMainDiv.push("</table>");
    mainDiv.innerHTML = arrMainDiv.join('');
}
//----------------------------------------------------------------------半全场胜负统计
function ShowAllHalfData(point) {
    var arrDataInfo = null;
    //去除颜色
    for (var i = 1; i <= 3; i++) {
        var menu = document.getElementById("menu" + i);
        if (point == i) {
            if (menu.className)
                menu.className = "nav_selected2";
            else
                menu.setAttribute("class", "nav_selected2");
        } else {
            if (menu.className)
                menu.className = "nav_unselected2";
            else
                menu.setAttribute("class", "nav_unselected2");
        }
    }
    switch (point) {
        case 1: arrDataInfo = allData; break;
        case 2: arrDataInfo = homeData; break;
        case 3: arrDataInfo = guestData; break;
    }
    var mainDiv = document.getElementById("tableId");
    var arrMainDiv = new Array();
    arrMainDiv.push("<table id='div_Table1' width='790' border='1' cellpadding='2' cellspacing='0'  bgcolor='#FFFFFF' class='tdlink'><tr bgcolor='#D1E2F5' align='center'  style='font-weight:bold;'><td width='127' height='24' rowspan='2'>" + Trans("球队名称") + "</td><td width='110' >" + Trans("半场") + "</td><td width='37' >" + Trans("胜") + "</td><td width='37' >" + Trans("胜") + "</td><td>" + Trans("胜") + "</td><td >" + Trans("平") + "</td><td width='37' >" + Trans("平") + "</td><td width='37' >" + Trans("平") + "</td><td width='37'>" + Trans("负") + "</td><td width='37' >" + Trans("负") + "</td><td width='37' >" + Trans("负") + "</td></tr><tr bgcolor='#D1E2F5' align='center' style='font-weight:bold;'><td >" + Trans("全场") + "</td><td width='37' >" + Trans("胜") + "</td><td width='37' >" + Trans("平") + "</td><td >" + Trans("负") + "</td><td >" + Trans("胜") + "</td><td width='37' >" + Trans("平") + "</td><td width='37' >" + Trans("负") + "</td><td width='37' >" + Trans("胜") + "</td><td >" + Trans("平") + "</td><td>" + Trans("负") + "</td></tr>");
    for (var i = 0; i < arrDataInfo.length; i++) {
        var nor = arrDataInfo[i];
        arrMainDiv.push("<tr align='center' " + (i % 2 == 0 ? "bgcolor='#eff4fa'" : "") + " >  <td colspan='2' bgcolor='#eff4fa' align='left'>&nbsp;<a href='/" + LangManage.langName + "/team/Summary/" + nor[0] + ".html' target='_blank'>" + teamHelper["T_" + nor[0]][1 + lang] + "</a></td>  <td bgcolor='#f5dbd1' class='etime'>" + nor[1] + "</td>  <td class='etime' >" + nor[2] + "</td>  <td width='37' class='etime' >" + nor[3] + "</td>  <td width='37' class='etime' >" + nor[4] + "</td>  <td bgcolor='#F7EDD5' class='etime'>" + nor[5] + "</td>  <td class='etime'>" + nor[6] + "</td>  <td class='etime'>" + nor[7] + "</td>  <td class='etime'>" + nor[8] + "</td>  <td bgcolor='#E7F7D7' class='etime'>" + nor[9] + "</td></tr>");
    }
    arrMainDiv.push("</table>");
    mainDiv.innerHTML = arrMainDiv.join('');
}
//---------------------------------------------------------------------------------------上下半场入球数较多
function ShowMoreBallData() {
    var mainDiv = document.getElementById("tableId");
    var arrMainDiv = new Array();
    arrMainDiv.push(" <table width='790' border='1' cellpadding='2' cellspacing='0'  bgcolor='#ffffff' class='tdlink' id='Table1'><tr align='center' bgcolor='#d1e2f5'   style='font-weight:bold;'><td width='115' height='24' rowspan='2'>" + Trans("球队名称") + "</td><td colspan='3'  height='24'>" + Trans("总") + "</td><td colspan='3'  height='24'>" + Trans("主") + "</td><td colspan='3'  height='24'>" + Trans("客") + "</td></tr><tr  align='center' bgcolor='#d1e2f5'   ><td width='52' align='center' >" + Trans("上半场入球数较多") + "</td><td width='65' > <span class='text'>" + Trans("上下半场入球数相同") + "</span></td><td width='52' ><span class='text'>" + Trans("下半场入球数较多") + "</span></td><td width='52' align='center' ><span class='text'>" + Trans("上半场入球数较多") + "</span></td><td width='65' ><span class='text'>" + Trans("上下半场入球数相同") + "</span></td><td width='52' ><span class='text'>" + Trans("下半场入球数较多") + "</span></td><td width='52' align='center' ><span class='text'>" + Trans("上半场入球数较多") + "</span></td><td width='65' ><span class='text'>" + Trans("上下半场入球数相同") + "</span></td><td width='52' ><span class='text'>" + Trans("下半场入球数较多") + "</span></td></tr>");
    for (var i = 0; i < dataArr.length; i++) {
        var nor = dataArr[i];
        arrMainDiv.push("<tr height='20' align='center' " + (i % 2 == 0 ? "bgcolor='#eff4fa'" : "") + ">  <td bgcolor='#EFF4FA'  align='left'  class='etime'>&nbsp;<a href='/" + LangManage.langName + "/team/Summary/" + nor[0] + ".html' target='_blank'>" + teamHelper["T_" + nor[0]][1 + lang] + "</a></td>  <td  class='etime'>" + nor[1] + "</td>  <td bgcolor='#f5dbd1'  class='etime'>" + nor[2] + "</td>  <td  class='etime'>" + nor[3] + "</td>  <td  class='etime'>" + nor[4] + "</td>  <td bgcolor='#F7EDD5'  class='etime'>" + nor[5] + "</td>  <td  class='etime'>" + nor[6] + "</td>  <td  class='etime'>" + nor[7] + "</td>  <td bgcolor='#E7F7D7'  class='etime'>" + nor[8] + "</td><td  class='etime'>" + nor[9] + "</td></tr>");
    }
    arrMainDiv.push("</table>");
    mainDiv.innerHTML = arrMainDiv.join('');
}
//------------------------------------------------------------------------------------入球时间分布表
function ShowTimeDistriData() {
    var mainDiv = document.getElementById("tableId");
    var arrMainDiv = new Array();
    arrMainDiv.push("<table width='790' border='1' cellpadding='2' cellspacing='0'   bgcolor='#ffffff' class='tdlink' id='Table1'><tr bgcolor='#d1e2f5' align='center' height='22' ><td width='135' height='24' rowspan='1' ><strong>" + Trans("球队名称") + "</strong></td><td width='20' >1<br/>-<br/>5</td><td  width='26' >6<br/>-<br/>10</td><td  width='24' >11<br/>-<br/>15</td><td  width='24' >16<br/>-<br/>20</td><td  width='24' >21<br/>-<br/>25</td><td  width='24' >26<br/>-<br/>30</td><td  width='24' >31<br/>-<br/>35</td><td  width='24' >36<br/>-<br/>40</td><td  width='26' >41<br/>-<br/>45</td><td  width='26' >46<br/>-<br/>50</td><td  width='26' >51<br/>-<br/>55</td><td  width='26' >56<br/>-<br/>60</td><td  width='26' >61<br/>-<br/>65</td><td  width='26' >66<br/>-<br/>70</td><td  width='26' >71<br/>-<br/>75</td><td  width='26' >76<br/>-<br/>80</td><td  width='26' >81<br/>-<br/>85</td><td  width='26' >86<br/>-<br/>90</td></tr>");
    for (var i = 0; i < arrData.length; i++) {
        var nor = arrData[i];
        arrMainDiv.push("<tr  " + (i % 2 == 0 ? "bgcolor='#eff4fa'" : "") + "  align='center'><td bgcolor='#eff4fa' align='left' >&nbsp;<a href='/" + LangManage.langName + "/team/Summary/" + nor[0] + ".html' target='_blank'>" + teamHelper["T_" + nor[0]][1 + lang] + "</a></td>  <td  class='etime'>" + nor[1] + "</td>  <td class='etime'>" + nor[2] + "</td>  <td class='etime'>" + nor[3] + "</td>  <td class='etime'>" + nor[4] + "</td>  <td class='etime'>" + nor[5] + "</td>  <td bgcolor='#f5dbd1' class='etime'>" + nor[6] + "</td>  <td class='etime'>" + nor[7] + "</td>  <td class='etime'>" + nor[8] + "</td>  <td class='etime'>" + nor[9] + "</td>  <td class='etime' >" + nor[10] + "</td>  <td class='etime'>" + nor[11] + "</td>  <td bgcolor='#F7EDD5' class='etime'>" + nor[12] + "</td>  <td  class='etime'>" + nor[13] + "</td>  <td  class='etime'>" + nor[14] + "</td>  <td  class='etime'>" + nor[15] + "</td>  <td  class='etime'>" + nor[16] + "</td>  <td  class='etime'>" + nor[17] + "</td>  <td bgcolor='#E7F7D7'  class='etime'>" + nor[18] + "</td></tr>");
    }
    arrMainDiv.push("</table>");
    mainDiv.innerHTML = arrMainDiv.join('');
}
//---------------------------------------------------------------------------------波胆分布
function ShowBoDanDistriData() {
    var mainDiv = document.getElementById("tableId");
    var arrMainDiv = new Array();
    arrMainDiv.push("<table width='790' border='1' cellpadding='2' cellspacing='0'  bgcolor='#ffffff' class='tdlink' id='Table1'><tr bgcolor='#d1e2f5'  align='center'><td width='135' height='24' rowspan='1' ><strong>" + Trans("球队名称") + "</strong></td><td  width='18' >1<br/>:<br/>0</td><td  width='18' >2<br/>:<br/>0</td><td  width='18' >2<br/>:<br/>1</td><td  width='18' >3<br/>:<br/>0</td><td  width='18' >3<br/>:<br/>1</td><td  width='18' >3<br/>:<br/>2</td><td  width='18' >4<br/>:<br/>0</td><td  width='18' >4<br/>:<br/>1</td><td  width='18' >4<br/>:<br/>2</td><td  width='18' >4<br/>:<br/>3</td><td  width='18' >0<br/>:<br/>0</td><td  width='18' >1<br/>:<br/>1</td><td  width='18' >2<br/>:<br/>2</td><td  width='18' >3<br/>:<br/>3</td><td  width='18' >4<br/>:<br/>4</td><td  width='18' >0<br/>:<br/>1</td><td  width='18' >0<br/>:<br/>2</td><td  width='18' >1<br/>:<br/>2</td><td  width='18' >0<br/>:<br/>3</td><td  width='18' >1<br/>:<br/>3</td><td  width='18' >2<br/>:<br/>3</td><td  width='18' >0<br/>:<br/>4</td><td  width='18' >1<br/>:<br/>4</td><td  width='18' >2<br/>:<br/>4</td><td  width='18' >3<br/>:<br/>4</td><td  width='26' >5球或以上</td></tr>");
    for (var i = 0; i < arrData.length; i++) {
        var nor = arrData[i];
        arrMainDiv.push("<tr height='20' " + (i % 2 == 0 ? "bgcolor='#eff4fa'" : "") + "  align='center'><td bgcolor='#EFF4FA'  align='left'>&nbsp;<a href='/" + LangManage.langName + "/team/Summary/" + nor[0] + ".html' target='_blank'>" + teamHelper["T_" + nor[0]][1 + lang] + "</a></td><td  class='etime'>" + nor[1] + "</td><td  class='etime' >" + nor[2] + "</td><td  class='etime' >" + nor[3] + "</td><td  class='etime' >" + nor[4] + "</td><td  class='etime' >" + nor[5] + "</td><td  class='etime' >" + nor[6] + "</td><td  class='etime' >" + nor[7] + "</td><td  class='etime' >" + nor[8] + "</td><td  class='etime' >" + nor[9] + "</td><td align='center' bgcolor='#f5dbd'1><span class='etime'>" + nor[10] + "</span></td><td  class='etime' >" + nor[11] + "</td><td  class='etime' >" + nor[12] + "</td><td  class='etime' >" + nor[13] + "</td><td  class='etime' >" + nor[14] + "</td><td bgcolor=#F7EDD5 class='etime' >" + nor[15] + "</td><td  class='etime' >" + nor[16] + "</td><td  class='etime' >" + nor[17] + "</td><td  class='etime' >" + nor[18] + "</td><td  class='etime' >" + nor[19] + "</td><td  class='etime' >" + nor[20] + "</td><td  class='etime' >" + nor[21] + "</td><td  class='etime' >" + nor[22] + "</td><td  class='etime' >" + nor[23] + "</td><td  class='etime' >" + nor[24] + "</td><td bgcolor=#E7F7D7 class='etime' >" + nor[25] + "</td><td  class='etime' >" + nor[26] + "</td></tr>")
    }
    arrMainDiv.push("</table>");
    mainDiv.innerHTML = arrMainDiv.join('');
}
//---------------------------------------------------------------净胜/净负球数总计
function ShowOnlyWinData(point) {
    var arrDataInfo = null;
    //去除颜色
    for (var i = 1; i <= 3; i++) {
        var menu = document.getElementById("menu" + i);
        if (point == i) {
            if (menu.className)
                menu.className = "nav_selected2";
            else
                menu.setAttribute("class", "nav_selected2");
        } else {
            if (menu.className)
                menu.className = "nav_unselected2";
            else
                menu.setAttribute("class", "nav_unselected2");
        }
    }
    switch (point) {
        case 1: arrDataInfo = arrData; break;
        case 2: arrDataInfo = arrData_H; break;
        case 3: arrDataInfo = arrData_G; break;
    }
    var mainDiv = document.getElementById("tableId");
    var arrMainDiv = new Array();
    arrMainDiv.push(" <table id='div_Table1' width='790' border='1' cellpadding='2' cellspacing='0'  bgcolor='#ffffff' class='tdlink'><tr bgcolor='#d1e2f5' align='center'><td width='135' height='24' rowspan='1' >" + Trans("球队名称") + "</td><td  width='95' >" + Trans("净胜") + "3球以上</td><td  width='80' >" + Trans("净胜") + "2球</td><td  width='80' >" + Trans("净胜") + "1球</td><td  width='65' >" + Trans("平手") + "</td><td  width='80' >" + Trans("净负") + "1球</td><td  width='80' >" + Trans("净负") + "2球</td><td  width='95' >" + Trans("净负") + "3球以上</td></tr>");
    for (var i = 0; i < arrDataInfo.length; i++) {
        var nor = arrDataInfo[i];
        arrMainDiv.push("<tr align='center' " + (i % 2 == 0 ? "bgcolor='#eff4fa'" : "") + " ><td bgcolor='#EFF4FA' align='left'>&nbsp;<a href='/" + LangManage.langName + "/team/Summary/" + nor[0] + ".html' target='_blank'>" + teamHelper["T_" + nor[0]][1 + lang] + "</a></td><td bgcolor='#F5DBD1' class='etime'>" + nor[1] + "</td><td class='etime' >" + nor[2] + "</td><td class='etime'>" + nor[3] + "</td class='etime'><td bgcolor='#F7EDD5' class='etime'>" + nor[4] + "</td><td class='etime'>" + nor[5] + "</td><td class='etime'>" + nor[6] + "</td><td bgcolor='#E7F7D7' class='etime'>" + nor[7] + "</td></tr>");
    }
    arrMainDiv.push("</table>");
    mainDiv.innerHTML = arrMainDiv.join('');
}
//--------------------------------------------------最先入球/失球赛果
function ShowFirResultData() {
    var mainDiv = document.getElementById("tableId");
    var arrMainDiv = new Array();
    arrMainDiv.push("<table width='790' border='1' cellpadding='2' cellspacing='0'  bgcolor='#ffffff' class='tdlink' id='Table1'><tr  align='center' bgcolor='#d1e2f5'   style='font-weight:bold;'><td width='135' height='24' rowspan='1' >" + Trans("球队名称") + "</td><td  width='95' >" + Trans("先入球") + "<br/>" + Trans("赛果胜") + "</td><td  width='95' >" + Trans("先入球") + "<br/>" + Trans("赛果和") + " </td><td  width='95' >" + Trans("先入球") + "<br/>" + Trans("赛果负") + " </td><td  width='95' >" + Trans("先失球") + "<br/>" + Trans("赛果胜") + " </td><td  width='95' >" + Trans("先失球") + "<br/>" + Trans("赛果和") + " </td><td  width='95' >" + Trans("先失球") + "<br/>" + Trans("赛果负") + " </td></tr>");
    for (var i = 0; i < arrResultData.length; i++) {
        var nor = arrResultData[i];
        arrMainDiv.push("<tr height='20' " + (i % 2 == 0 ? "bgcolor='#eff4fa'" : "") + " align='center'>  <td bgcolor='#EFF4FA' align='left'>&nbsp;<a href='/" + LangManage.langName + "/team/Summary/" + nor[0] + ".html' target='_blank'>" + teamHelper["T_" + nor[0]][1 + lang] + "</a></td>  <td  bgcolor='#F5DBD1' class='etime'>" + nor[1] + "</td>  <td class='etime'>" + nor[2] + "</td>  <td class='etime'>" + nor[3] + "</td>  <td bgcolor='#E7F7D7' class='etime'>" + nor[4] + "</td>  <td class='etime'>" + nor[5] + "</td>  <td class='etime'>" + nor[6] + "</td></tr>");
    }
    arrMainDiv.push("</table>");
    mainDiv.innerHTML = arrMainDiv.join('');
}
function InitTeamArr() {
    var url = window.location.href.toLowerCase();
    if (url.indexOf("subleague") != -1) {
        teamHelper = new Object();
        for (var i = 0; i < arrTeam.length; i++) {
            if (!contans("T_" + arrTeam[i][0]))
                teamHelper["T_" + arrTeam[i][0]] = arrTeam[i];
        }
    } else
        if (url.indexOf("lnormaldetail") != -1) {
            teamHelper = new Object();
            for (var i = 0; i < arrTeam.length; i++) {
                teamHelper["T_" + arrTeam[i][0]] = arrTeam[i];
            }
        }
}
