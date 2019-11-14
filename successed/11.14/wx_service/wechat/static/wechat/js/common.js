/**
 * Created by fox on 2016/12/7.
 */
function tipBoxShow(tips,status,times){
	if(status=='' || status==undefined || status==null){
		status = 'success';
	}
	var tipBox = $(".tipBox");
	tipBox.show();
	tipBox.find("i").removeClass("success");
	tipBox.find("i").removeClass("fail");
	tipBox.find("i").addClass(status);
	tipBox.find("span").html(tips);
	if(times==undefined || times==null || times==''){
		times = 1500;
	}

	$(function () {
		setTimeout(function () {
			tipBox.hide();
		}, times); // 设置2s后消失
	})
}

function jumpUrl(url,times) {
	if(times==undefined || times==null || times==''){
		times = 1500;
	}
	if(url==undefined || url==null || url==''){
		url ='';
	}
	$(function () {
		setTimeout(function () {
			window.location.href=url;
		}, times); // 设置2s后消失
	})
}