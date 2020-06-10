HTTP/1.1 200 OK
Date: Tue, 09 Jun 2020 14:49:35 GMT
Server: Apache
Last-Modified: Fri, 08 May 2020 09:24:49 GMT
ETag: "42e7-5a51f919b5a40"
Accept-Ranges: bytes
Content-Length: 17127
Keep-Alive: timeout=5, max=97
Connection: Keep-Alive
Content-Type: application/javascript

//NS-1383 网站新增热轧卷板品种  20140217 by zjj
//NS-1652  网站新增镍品种  20141209 by zjj
//NS-1653  网站新增锡品种  20141209 by zjj
//NS-2442 期权业务规则调整二期 20170929 wang.yiding

var datatxt;

$(document).ready(function(){
	var lastButtionId = "";
	var sid = new Date().Format("yyMMddHHmmss");
	var parambuttonid;		
	require.config({
		paths : {
			"jquery" : "/js/jquery",
			"business-data" : "/js/trade-data",
			"jquery.datepicker" : "/js/jquery.ui.datepicker"
		},
		shim : {
			'jquery.datepicker' : {
				deps : [ 'jquery' ]
			}
		}
	});
	require([ 'jquery', '/js/trade-data.js?' + sid,'jquery.datepicker' ],
		function($, bd) {
			var datatxt;
			$('#calendar').datepicker({
				altField: "#dateinput",
				altFormat: "yy-mm-dd",
				closeText : '关闭',
				prevText : '&#x3c;上月',
				nextText : '下月&#x3e;',
				currentText : '今天',
				monthNames : [ '一月', '二月',
						'三月', '四月', '五月',
						'六月', '七月', '八月',
						'九月', '十月', '十一月',
						'十二月' ],
				monthNamesShort : [ '一月',
						'二月', '三月', '四月',
						'五月', '六月', '七月',
						'八月', '九月', '十月',
						'十一月', '十二月' ],
				dayNames : [ '星期日', '星期一',
						'星期二', '星期三',
						'星期四', '星期五', '星期六' ],
				dayNamesShort : [ '周日',
						'周一', '周二', '周三',
						'周四', '周五', '周六' ],
				dayNamesMin : [ '日', '一',
						'二', '三', '四', '五',
						'六' ],
				weekHeader : '周',
				dateFormat : 'yymmdd',

				isRTL : false,
				showMonthAfterYear : true,
				yearSuffix : '年',
				inline : true,
				firstDay : 7,
				changeMonth : true,
				changeYear : true,
				showOtherMonths : true,
				onSelect : function(text,instance) {
					var cy = text.substring(0, 4);
					var cm = text.substring(4, 6);
					var cdd = text.substring(6, 8);
					
					if (lastButtionId == "") {
						lastButtionId = "kx";
					}
					tiaozhuan(lastButtionId,text);
				},
				beforeShowDay : function(date) {
					var dtstr = $.datepicker.formatDate("yymmdd",date);
					var year = dtstr.substr(0, 4);
					if ((!bd[year] || bd[year].indexOf(dtstr) != -1)) {
						return new Array(true,'no-data');
					} else {
						return new Array(true,'has-data');

					}
				}

			});
			
			var params = location.search;
			var paramss = params.substr(1,params.length-1);
			var paramsss = paramss.split("&");											
			var paramdate;
			
			
			if(paramsss[0] != null){
				var parambuttonids = paramsss[0].split("=");
				parambuttonid = parambuttonids[1];
				
			}
			if(parambuttonid==null||parambuttonid==""){
				parambuttonid="kx";
			}
			
			if(parambuttonid.indexOf("delaymarket_")>=0 && parambuttonid.indexOf("Q")==-1){
				tiaozhuan(parambuttonid,"");
				return;
			}
			
			if(paramsss[1] != null){
				var paramdates = paramsss[1].split("=");
					paramdate = paramdates[1];
			}
			
			if(paramdate==""||paramdate==null){
				paramdate=moment().format('YYYYMMDD');
				generatenull(parambuttonid,paramdate);
				switch (parambuttonid){
				case "kx":
					rollingGetjson("/data/dailydata/kx/kx",".dat",8,parambuttonid,paramdate,0);
					break;
				case "pm":
					rollingGetjson("/data/dailydata/kx/pm",".dat",8,parambuttonid,paramdate,0);
					break;
				case "week":
					rollingGetjson("/data/dailydata/",".dat",8,parambuttonid,paramdate,0);
					break;
				case "month":
					tiaozhuan(parambuttonid,paramdate);
					//rollingGetjson("/data/dailydata/","month.dat",6,parambuttonid,paramdate,0);
					break;
				case "monthprice":
					tiaozhuan(parambuttonid,paramdate);
					//rollingGetjson("/data/dailydata/","price.dat",6,parambuttonid,paramdate,0);
					break;
				case "exchangedelivery":
					rollingGetjson("/data/instrument/ExchangeDelivery",".dat",6,parambuttonid,paramdate,0);
					break;
				case "timeprice":
					rollingGetjson("/data/dailydata/ck/","defaultTimePrice.dat",8,parambuttonid,paramdate,0);
					break;
				case "markerprice":
					rollingGetjson("/data/dailydata/ck/","markerprice.dat",8,parambuttonid,paramdate,0);
					break;
				case "js":
					rollingGetjson("/data/dailydata/js/js",".dat",8,parambuttonid,paramdate,0);
					break;
				case "zs":
					rollingGetjson2("/data/dailydata/","zs.html",8,parambuttonid,paramdate,0);
					break;
				case "dailystock":	
					if(paramdate<"20140519"){
						rollingGetjson2("/data/dailydata/","dailystock.html",8,parambuttonid,paramdate,0);	
					}else{
						rollingGetjson("/data/dailydata/","dailystock.dat",8,parambuttonid,paramdate,0);
					}
					break;
				case "weeklystock":
					var now = moment(paramdate,"YYYYMMDD");
					now.isoWeekday(1);
					now.day(7);
					var dts = now.format("YYYYMMDD");
					if(paramdate<"20140519"){
						rollingGetjson2("/data/dailydata/","weeklystock.html",8,parambuttonid,dts,0,7);
					}else{
						rollingGetjson("/data/dailydata/","weeklystock.dat",8,parambuttonid,dts,13);
					}
					break;	
				case "yearstat":
					tiaozhuan(parambuttonid,paramdate);
					break;
					
				default:
					break;
				}
			}else{
				var dateP=/^\d{4}\d{2}\d{2}$/; 
				if(!dateP.test(paramdate)){
					paramdate=moment().format('YYYYMMDD');
				}
				
				$('#calendar').datepicker("setDate",paramdate);
				tiaozhuan(parambuttonid,paramdate);
				
			}
		});
	
	
	//延时行情
	$("ul.yansbb li").click(function(){
		var delayment = $(this).children().attr("id");
		var disphtmlname = "/statements/" + delayment + ".html";
		disphtml(disphtmlname);
	});
	//搜索按钮
	$("input#search").click(function(){
		var currdate = $('#calendar').datepicker("getDate");
		currdatestr = currdate.getFullYear().toString();
		if((currdate.getMonth()+1) < 10){
			currdatestr += "0" + (currdate.getMonth()+1).toString();
		}else{
			currdatestr += (currdate.getMonth()+1).toString();
		}
		if(currdate.getDate()<10){
			currdatestr +="0"+currdate.getDate().toString();
		}else{
			currdatestr += currdate.getDate().toString();
		}
		if(parambuttonid == null){
			alert("没有选中一个表类别");
		}else{
			if(parambuttonid == "weeklystock") {
				var now = moment(currdatestr,"YYYYMMDD");
				now.isoWeekday(1);
				now.day(7);
				var dts = now.format("YYYYMMDD");
				if(currdatestr<"20140519"){
					rollingGetjson2("/data/dailydata/","weeklystock.html",8,parambuttonid,dts,0,7);

				}else{
					rollingGetjson("/data/dailydata/","weeklystock.dat",8,parambuttonid,dts,13);
				}
			
			}else {
				tiaozhuan(parambuttonid,currdatestr);
			}
			
		}
		
	});
	//动态变化日期
	$("#calendar").change(function(){
		var currdate = $('#calendar').datepicker("getDate");
		currdatestr = currdate.getFullYear().toString();
		if((currdate.getMonth()+1) < 10){
			currdatestr += "0" + (currdate.getMonth()+1).toString();
		}else{
			currdatestr += (currdate.getMonth()+1).toString();
		}
		if(currdate.getDate()<10){
			currdatestr +="0"+currdate.getDate().toString();
		}else{
			currdatestr += currdate.getDate().toString();
		}
		
		var buttonid = $(this).attr("id");
		if(buttonid == "search"){
			return;
		}
		var year1 = currdatestr.substr(0,4);
		var month1 = currdatestr.substr(4,2);
		var date1 = currdatestr.substr(6,2);
		var paramdatetemp2 = year1 + "-" + month1 + "-" + date1;
		//$(":input#dateinput").val(paramdatetemp2);
	});
	//按钮点击事件（包括下载与表格选择）
	$("input.bttt").click(function(){
		var currdate = $('#calendar').datepicker("getDate");
		currdatestr = currdate.getFullYear().toString();
		if((currdate.getMonth()+1) < 10){
			currdatestr += "0" + (currdate.getMonth()+1).toString();
		}else{
			currdatestr += (currdate.getMonth()+1).toString();
		}
		if(currdate.getDate()<10){
			currdatestr +="0"+currdate.getDate().toString();
		}else{
			currdatestr += currdate.getDate().toString();
		}
		var buttonid = $(this).attr("id");
		if(buttonid == "search"){
			return;
		}
		parambuttonid = $(this).attr("id");
		
		if(parambuttonid == "weeklystock") {
				var now = moment(currdatestr,"YYYYMMDD");
				now.isoWeekday(1);
				now.day(7);
				var dts = now.format("YYYYMMDD");
				if(currdatestr<"20140519"){
					rollingGetjson2("/data/dailydata/","weeklystock.html",8,parambuttonid,dts,0,7);
				}else{
					rollingGetjson("/data/dailydata/","weeklystock.dat",8,parambuttonid,dts,13);
				}
				
		}else {
				tiaozhuan(parambuttonid,currdatestr);
		}
			
		//tiaozhuan(buttonid,currdatestr);
		
	});
	
	
		
	function rollingGetjson(prefix,end,len,parambuttonid,paramdate,maxtime) {
		if(maxtime <20) {
		 var datatxt = prefix + paramdate.substr(0,len) + end;			
			$.ajax({
			  url: datatxt,
			  success: function(json){
			  	if(datatxt.indexOf(".html")>=0||!jQuery.isEmptyObject(json) && (!jQuery.isEmptyObject(json.o_cursor) || !jQuery.isEmptyObject(json.o_curinstrument)||!jQuery.isEmptyObject(json.o_currefprice)||!jQuery.isEmptyObject(json.o_curMarkerPrice))) {
				  	tiaozhuan(parambuttonid,paramdate);
						var year1 = paramdate.substr(0,4);
						var month1 = paramdate.substr(4,2);
						var date1 = paramdate.substr(6,2); 
						var paramdatetemp = year1+""+month1+""+ date1;
						$('#calendar').datepicker("setDate",paramdatetemp);
						//$(":input#dateinput").val(year1+"-"+month1+"-"+date1);
				  }else {
				  	maxtime ++;
						var now = moment(paramdate,"YYYYMMDD");
						now.subtract('days',1);
						var nowstr = now.format("YYYYMMDD");
						
				  	rollingGetjson.call(this,prefix,end,len,parambuttonid,nowstr,maxtime);
				  }
				},
			  dataType: "json",
			  error:function(){
			  	maxtime ++;
						var now = moment(paramdate,"YYYYMMDD");
						now.subtract('days',1);
						var nowstr = now.format("YYYYMMDD");
				  	rollingGetjson.call(this,prefix,end,len,parambuttonid,nowstr,maxtime);
			  }
			});
		}else {
//			var now = moment(paramdate,"YYYYMMDD");
//			now.add('days',1);					
//			var nowstr = now.format("YYYYMMDD");
			var nowstr = moment().format("YYYYMMDD");
			generatenull(parambuttonid,nowstr);
			nodata();
			lastButtionId =parambuttonid;
			$('#calendar').datepicker("setDate",nowstr);
			//$(":input#dateinput").val(now.format("YYYY-MM-DD"));
		}
	}
	
	
	function rollingGetjson2(prefix,end,len,parambuttonid,paramdate,maxtime,n) {
		if(!n) {
			n = 20;
		}
		if(maxtime <n) {
		 var datatxt = prefix + paramdate.substr(0,len) + end;
			$.ajax({
			  url: datatxt,
			  success: function(json){
			  	if(datatxt.indexOf(".html")>=0||!jQuery.isEmptyObject(json) && (!jQuery.isEmptyObject(json.o_cursor) || !jQuery.isEmptyObject(json.o_curinstrument)||!jQuery.isEmptyObject(json.o_currefprice))) {
				  	tiaozhuan(parambuttonid,paramdate);
						var year1 = paramdate.substr(0,4);
						var month1 = paramdate.substr(4,2);
						var date1 = paramdate.substr(6,2);
						var paramdatetemp = year1+""+month1+""+ date1;
						$('#calendar').datepicker("setDate",paramdatetemp);
						//$(":input#dateinput").val(year1+"-"+month1+"-"+date1);
				  }else {
				  	maxtime ++;
						var now = moment(paramdate,"YYYYMMDD");
						now.subtract('days',1);
						var nowstr = now.format("YYYYMMDD");
				  	rollingGetjson2.call(this,prefix,end,len,parambuttonid,nowstr,maxtime,n);
				  }
				},
			  dataType: "html",
			  error:function(){
			  		maxtime ++;
						var now = moment(paramdate,"YYYYMMDD");
						now.subtract('days',1);
						var nowstr = now.format("YYYYMMDD");
						
				  	rollingGetjson2.call(this,prefix,end,len,parambuttonid,nowstr,maxtime,n);
			  }
			});
		}else {
//			var now = moment(paramdate,"YYYYMMDD");
//			now.add('days',1);
//			var nowstr = now.format("YYYYMMDD");
			var nowstr = moment().format("YYYYMMDD");					
			generatenull(parambuttonid,nowstr);
			nodata();
			lastButtionId =parambuttonid;
			$('#calendar').datepicker("setDate",nowstr);
		//	$(":input#dateinput").val(now.format("YYYY-MM-DD"));
		}
	}
	
	
	//记录尝试加载product_dat的次数
	var load_product_dat_times=0;
	
	//判断按钮ID，选择不一样的生成方式
	function tiaozhuan(buttonids,dates){		
		if(load_product_dat_times<3 && !product_data_json_flag){
			load_product_dat_times++;
			getProductNameFromDat_foot(function(){
				tiaozhuan(buttonids,dates);
			});
			return;
		}						
		if("downloadhistory,downloadnow".indexOf(buttonids)>-1){
			
		}else{
			generatenull(buttonids,dates);	
		}		
		switch (buttonids){
		case "kx":
			datatxt = "/data/dailydata/kx/kx" + dates + ".dat";
			dispkxdata(datatxt,dates);
			lastButtionId ="kx";
			break;
		case "pm":
			datatxt = "/data/dailydata/kx/pm" + dates + ".dat";
			disppmdata(datatxt);
			lastButtionId ="pm";
			break;
		case "week":
			datatxt = "/data/dailydata/" + dates + ".dat";
			dispweekdata(datatxt,dates);
			lastButtionId ="week";
			break;
		case "month":
			lastButtionId ="month";
			datatxt = "/data/dailydata/" + dates + "month.dat";
			$.ajax({
				type : "GET",
				url : datatxt,
				success : function(json) {
					dispmonthdata(datatxt,dates,dates);
				},
				error : function(msg) {
					datatxt = "/data/dailydata/" + dates.substr(0,6) + "month.dat";
					dispmonthdata(datatxt,dates.substr(0,6),dates);
					
				}
			});
			
			break;	
			
			
		case "monthprice":
			datatxt = "/data/dailydata/" + dates + "price.dat";
			lastButtionId ="monthprice";
			$.ajax({
				type : "GET",
				url : datatxt,
				success : function(json) {
					dispmonthpricedata(datatxt,dates);
				},
				error : function(msg) {
					datatxt = "/data/dailydata/" + dates.substr(0,6) + "price.dat";
					dispmonthpricedata(datatxt,dates.substr(0,6));
					
				}
			});
			
			break;
		case "dailystock":
			//liushangguo 20140505 update
			if(dates<"20140519"){
				datatxt = "/data/dailydata/" + dates + "dailystock.html";
				disphtml(datatxt);
			}else{
				datatxt = "/data/dailydata/" + dates + "dailystock.dat";
				dispdailydata(datatxt);			
			}
			lastButtionId ="dailystock";
			break;
		case "weeklystock":
			if(dates<"20140519"){
				datatxt = "/data/dailydata/" + dates + "weeklystock.html";
				disphtml(datatxt);
			}else{
				if(dates<"20181025"){
					datatxt = "/data/dailydata/" + dates + "weeklystock.dat";
					dispweeklystockdata(datatxt);
				}else{
					datatxt = "/data/dailydata/" + dates + "weeklystock.dat";
					dispweeklystockdata_new(datatxt);
				}
			}
			lastButtionId ="weeklystock";
			break;
		case "monthstat":
			datatxt = "/data/dailydata/" + dates.substr(0,6) + "monthstat.html";
			disphtml(datatxt);
			lastButtionId ="monthstat";
			break;
			
		case "yearstat":
			datatxt = "/data/dailydata/" + dates.substr(0,4) + "year.dat";
			dispyeardata(datatxt,dates.substr(0,4));
			lastButtionId ="yearstat";
			break;
			
		case "zs":
			datatxt = "/data/dailydata/" + dates + "zs.html";
			disphtml(datatxt);
			lastButtionId ="zs";
			break;
		case "exchangedelivery":
			datatxt = "/data/instrument/ExchangeDelivery" + dates.substr(0,6) + ".dat";
			dispexchangedelivery(datatxt);
			lastButtionId ="exchangedelivery";
			break;
		case "timeprice":
			datatxt = "/data/dailydata/ck/"+dates+"defaultTimePrice.dat" ;
			disptimeprice(datatxt);
			datatxt = "/data/dailydata/ck/"+dates+"mainTimePrice.dat" ;
			disptimeprice(datatxt);
			datatxt = "/data/dailydata/ck/"+dates+"dailyTimePrice.dat" ;
			disptimeprice(datatxt);
			lastButtionId ="timeprice";
			break;
		case "markerprice":
			datatxt = "/data/dailydata/ck/" + dates + "markerprice.dat";
			dispmarkerprice(datatxt);
			lastButtionId ="markerprice";
			break;
		case "js":
			datatxt = "/data/dailydata/js/js" + dates + ".dat";
			dispjsdata(datatxt);
			lastButtionId ="js";
			break;
		case "downloadhistory":
			var downloadyear = $("#yearselect").val();
			var typename = $("input[name='typename']:checked").val();
			downloadhistoryfile(downloadyear,typename);
			break;
		case "downloadnow":
			var downloadyear = $("#yearselect option:eq(0)").val();
			var typename = $("input[name='typename']:checked").val();
			downloadnowfile(downloadyear,typename);
			break;
		case (buttonids.match(/delaymarket_/) || {}).input:
			var disphtmlname = "/statements/"+buttonids+".html";
			disphtml(disphtmlname);
			lastButtionId=buttonids;
			break;
		default:
			break;
		}
	}
	
	
});



var tas_start_date=null;

function getCommonConfig(){	
	$.ajax({
		type:"get",
		url:"/data/config/config_common_config.dat?temp="+new Date().getTime(),
		dataType:"json",
		timeout:3000,
		success:function(json){
			if(json!=null){				
				tas_start_date = json.tas.txt.tas_start_date;
			}
		},
		error:function(request,status,error){
			
		}
		
	});
}
getCommonConfig();