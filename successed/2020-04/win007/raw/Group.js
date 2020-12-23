
function infoBaseInit() {
    var fragment = document.createDocumentFragment();
    var fragment2 = document.createElement("div");
    bomHelper.SetAttributeClass(fragment2, "gameList");
    fragment2.id = "allSclassList";
    for (var i = 0; i < arr.length; i++) {
        //创建div框架
        var div1 = document.createElement("div");
        var div_top = document.createElement("div");
        var div_bottom = document.createElement("div");
        var img = document.createElement("img");
        var span = document.createElement("span");
        //添加css
        if (bomHelper.ie != "" && parseFloat(bomHelper.ie) < 8) {
            div1.setAttribute("className", "divList");
            div_top.setAttribute("className", "div_inner_top");
            div_bottom.setAttribute("className", "div_inner_bottom");
            img.setAttribute("className", "div_inner_top_img");
            span.setAttribute("className", "div_inner_bottom_span");
        } else {
            div1.setAttribute("class", "divList");
            div_top.setAttribute("class", "div_inner_top");
            div_bottom.setAttribute("class", "div_inner_bottom");
            img.setAttribute("class", "div_inner_top_img");
            span.setAttribute("class", "div_inner_bottom_span");
        }
        //添加其他属性
        //img.setAttribute("width", "100");
        div1.id = arr[i][0];
        div1.setAttribute("infotype", arr[i][3]);
        img.id = arr[i][0] + "img";
        div_bottom.id = arr[i][0] + "bottomDiv";
        span.id = arr[i][0] + "bottomSpan";

        span.innerHTML = arr[i][1]; //国家名
        div_bottom.onmouseover = showSclass(arr[i][0]);
        div_bottom.onmouseout = hideSclass(arr[i][0]);
        img.src = "/Image/info/" + arr[i][2]; //图片路径

        div_top.appendChild(img);
        div_bottom.appendChild(span);
        div1.appendChild(div_top);
        div1.appendChild(div_bottom);
        fragment2.appendChild(div1);

        //添加联赛选择层
        if (arr[i][4] instanceof Array) {
            Layer1(fragment, arr[i][0], arr[i][4]);
        }
    }
    var info = document.getElementById("info");
    domHelper.formatChildNode(info);
    info.insertBefore(fragment2, info.lastChild);
    document.body.appendChild(fragment);
}
//层显示
function Layer1(fragment, objId, arrSclass) {
    var oDiv = document.createElement("div");
    if (bomHelper.ie != "" && parseFloat(bomHelper.ie) < 8)
        oDiv.setAttribute("className", "floatDiv");
    else
        oDiv.setAttribute("class", "floatDiv");
    oDiv.id = objId + "div";
    oDiv.onmouseout = hideSclass(objId);
    oDiv.onmouseover = showSclass(objId);
    var page = (arrSclass.length + 15) / 16; //16个作为一列，超出16个则分成两列
    for (var i = 1; i <= page; i++) {
        oDiv.appendChild(createSclassDiv(arrSclass, i));
    }
    fragment.appendChild(oDiv);
}

//显示联赛名(闭包)
function showSclass(sCountryID) {
    return function(event) {
        var abb = document.getElementById(sCountryID + "div");
        var ak001 = document.getElementById(sCountryID + "bottomDiv");

        var zbObj = domHelper.getPosition(ak001);
        abb.style.position = "absolute";
        if (abb.childNodes.length == 1) {
            var ul = abb.getElementsByTagName("ul")[0];
            var ulHeight = ul.childNodes.length * 20;          
            if (zbObj.top + ulHeight < document.body.scrollHeight) {//个数小于9个的位置设置 ul.childNodes.length <= 9
                //ul.style.borderTopColor = "#ffffff";
                abb.style.left = (zbObj.left + 4) + "px";
                abb.style.top = (zbObj.top + 27) + "px";
                abb.style.display = "block";
            } else {
                abb.style.left = (zbObj.left + 20) + "px";
                abb.style.top = (zbObj.top - 120) + "px";
                abb.style.display = "block";
            }
        } else {
            var divs_len = abb.childNodes.length * 85;
            var cha = zbObj.left + divs_len - document.body.clientWidth;
            if (cha > 0) {
                abb.style.left = (zbObj.left - cha) + "px";
            } else {
                abb.style.left = (zbObj.left + 20) + "px";
            }
            abb.style.top = (zbObj.top - 120) + "px";
            abb.style.display = "block";
        }

    }
}
//隐藏联赛名(闭包)
function hideSclass(sCountryID) {
    return function(event) {
        var abb = document.getElementById(sCountryID + "div");
        abb.style.display = "none";
    }
}

//显示赛季
function showSeason(obj, event, i) {
    if (obj.childNodes.length > 1) {

        var floatDiv = obj.parentNode.parentNode.parentNode;
        var left = parseInt(floatDiv.style.left);
        var ulHeight = obj.lastChild.childNodes.length * 17;
        if (event.offsetY + ulHeight > document.body.scrollHeight || obj.lastChild.childNodes.length < 3) {
            if (obj.lastChild.childNodes.length < 3)
                obj.lastChild.style.top = i % 16 * 20 - ulHeight + 10 + "px";
            else
                obj.lastChild.style.top = i % 16 * 20 - ulHeight + "px";
        }
        var changeZindex = false;
        if (floatDiv.childNodes.length > 1) {
            left = left + (floatDiv.childNodes.length - 1) * 85;
            changeZindex = true;
        }

        if (document.body.clientWidth - left < 130) {
            obj.lastChild.style.left = "-65px";
            if (changeZindex) {
                for (var i = 0; i < floatDiv.childNodes.length; i++)
                    floatDiv.childNodes[i].style.zIndex = 20 + i;
            }
        } else {
            obj.lastChild.style.left = "70px"
            if (changeZindex) {
                for (var i = 0; i < floatDiv.childNodes.length; i++)
                    floatDiv.childNodes[i].style.zIndex = 20 - i;
            }
        }

        obj.lastChild.style.display = "block";
        obj.style.backgroundColor = "#cccccc";
    }
}
//隐藏赛季
function hideSeason(obj) {
    if (obj.childNodes.length > 1) {
        obj.lastChild.style.display = "none";
        obj.style.backgroundColor = "#ffffff";

    }
}
//鼠标滑过改变颜色
function overColor(obj) {
    obj.style.backgroundColor = "#cccccc";
}
function outColor(obj) {
    obj.style.backgroundColor = "#ffffff";
}

//创建联赛分列的层
function createSclassDiv(arrSclass, pageNo) {

    var len = 16;
    var left = -pageNo * 2 + (pageNo - 1) * 90;
    var offset = (pageNo - 1) * len;
    var zIndex = 20 - pageNo; //层级
    var ulDiv = document.createElement("div");
    if (bomHelper.ie != "" && parseFloat(bomHelper.ie) < 8) {
        ulDiv.setAttribute("className", "ulDiv");
    } else {
        ulDiv.setAttribute("class", "ulDiv");
    }
    ulDiv.style.zIndex = zIndex;
    ulDiv.style.left = left + "px";
    var oDivInHtml = "<ul class=\"div_inner_bottom_span_ul\">";
    var arrMatch = null;
    var top = 0; //由于padding-top:3px
    for (var i = offset; i < (offset + len) && i < arrSclass.length; i++) {
        arrMatch = arrSclass[i].split(",");
        oDivInHtml += "<li onmouseover=\"showSeason(this,event," + i + ")\" onmouseout=\"hideSeason(this)\">&nbsp;<a  href=\"javascript:void(0)\">" + arrMatch[1] + "</a>";
        if (arrMatch.length > 4) {
            oDivInHtml += "&nbsp;&raquo;<ul class=\"inner_ul\" style=\"top:" + top + "px;\" >";
            if (arrMatch[2] == "1") {//联赛
                var tempMatch = "";
                var aspxName = "League";
                if (arrMatch[3] != "0")
                    aspxName = "SubLeague";
                for (var j = 4; j < arrMatch.length; j++) {
                    tempMatch = arrMatch[j];
                    oDivInHtml += "<li  onmouseover=\"overColor(this)\" onmouseout=\"outColor(this)\">&nbsp;<a href=\"/" + LangManage.langName + "/" + aspxName + "/" + tempMatch + "/" + arrMatch[0] + ".html\">" + arrMatch[j] + "</a></li>";
                }
            } else if (arrMatch[2] == "2") {//杯赛
                var tempMatch = "";
                for (var j = 4; j < arrMatch.length; j++) {
                    tempMatch = arrMatch[j];
                    oDivInHtml += "<li  onmouseover=\"overColor(this)\" onmouseout=\"outColor(this)\">&nbsp;<a href=\"/" + LangManage.langName + "/CupMatch/" + tempMatch + "/" + arrMatch[0] + ".html\">" + arrMatch[j] + "</a></li>";
                }
            }

            oDivInHtml += "</ul>";
        }
        oDivInHtml += "</li>";
        top += 17; //这里是根据div_inner_bottom_select_ul里面的line-height高度来设置的

    }
    oDivInHtml += "</ul>";
    ulDiv.innerHTML = oDivInHtml;
    return ulDiv;
}
//根据不同类型显示不同的赛事
function showSclasses(type, name) {
    var allSclassList = document.getElementById("allSclassList");
    if (type == "zq") {
        for (i = 0; i < 6; i++)
            document.getElementById("menu_" + i).className = "nav_unselected";
        document.getElementById("menu_" + name).className = "nav_selected";
        var arrCdList = allSclassList.childNodes;

        for (var i = 0; i < arrCdList.length; i++) {
            var infoType = arrCdList[i].getAttribute("infotype");
            if (infoType == undefined) continue;
            if (infoType != name && name != 0) {
                arrCdList[i].style.display = "none";
            } else {
                arrCdList[i].style.display = "block";
            }
        }
    }

}