document.write('<script src="jquery-2.1.0.js" type="text/javascript" charset="utf-8"></script>');
!function(win){
    function X_picker(map){
        this.map = map || {};
        this.data = this.map.data || [""];
        this.is_move = false;
        this.win_row = 7; //模态窗口上可见行数
        this.row_h = 40;
        this.init_y = 0; //初始滚动值
        this.set_fn = function(){};
        this.changed_fn = function(){};
        this.touchstart_y = 0; //
        this.value = "";//当前选择项
        this.index = "";//当前选择索引
        this.init();
        this.set_opts(this.data);
        this.init_value();
        this.events();
    }
    X_picker.prototype = {
        init : function(){
            this.el = document.createElement('div');
            this.el.className = "xpicker-slider-wrap";
            var str = `
                <div class="xpicker-slider">
                </div>
                <div class="xpicker-mask">
                    <div class="xpicker-mask-top"></div>
                    <div class="xpicker-mask-mid"></div>
                    <div class="xpicker-mask-bottom"></div>
                </div>
            `;
            this.el.innerHTML = str;
            this.slider = this.el.querySelector(".xpicker-slider");
        }
        ,init_value: function(){
            this.get( Math.abs(this.init_y));
        }
        ,set_opts : function(list){
            this.data =  list ;
            var str = "";
            for(var i=0; i<list.length; i++){
                var item = list[i];
                str += "<div class='xpicker-slider-row'>" + item + "</div>";
            }
            this.slider.innerHTML = str;
            this.rows = this.slider.querySelectorAll('.xpicker-slider-row');
            this.slider_h = this.row_h * this.rows.length;
            this.max_scroll = this.slider_h-this.row_h; //最大滚动范围
            this.index_count = ~~(this.slider_h / this.row_h); //选项总数
            this.set(this.index);
            // debugger
        }
        ,changed : function(fn){
            this.changed_fn = fn;
        }
        ,set : function(index){ //设置定位到选项
            if(index >=this.index_count){
                return;
            }
            var pos = index;
            var y = -(Math.abs(pos * this.row_h));
            this.slider.style.transform = "translateY("+y+"px)";
            this.init_y = y; //初始滚动值;
            // debugger
            this.get(Math.abs(y));
            this.set_fn.call(this,this.value,this.index);
            
        }
        ,set_hook: function(fn){//set后钩子
            this.set_fn = fn;
        }
        ,locate : function(dis){//定位
            var rs = (Math.round(Math.abs(dis) / this.row_h)) * this.row_h;
            return -rs;
        }
        ,get : function(dis){//取滚动到指定位置的选项
            // if(dis < 0){
            //     return;
            // }
            var dis = Math.abs(dis);
            if(dis < this.slider_h){
                var index = ~~(dis / this.row_h);
            }else {
                var index =  ~~((dis - ((~~(dis / this.slider_h)) * this.slider_h)) / this.row_h);
            }
            this.value = this.rows[index].textContent;
            this.index = index;
            return {
                value : this.value
                ,index : this.index
            };
        }
        ,prevent_default(e){
            e.preventDefault();
        }
        ,events : function(){
            this.el.ontouchstart = this.touchstart.bind(this);
            this.el.ontouchmove = this.touchmove.bind(this);
            this.el.ontouchend = this.touchend.bind(this);
        }
        ,touchstart : function(e){
            // debugger
            document.addEventListener('touchmove',this.prevent_default,{passive:false});
            this.is_move = true;
            var y = e.changedTouches[0].pageY;
            this.touchstart_y = y;
            var patt = /-?\d+(?:\.\d+)?(?:e[+\-]?\d+)?/i;
            var match = patt.exec(this.slider.style.transform);
            if(match!=null){
                this.slider.removeAttribute('style');
                this.slider.style.transform = "translateY("+match[0]+"px)";
            }
            this.first_y = this.init_y;
            this.first_time = Date.now();
        }
        ,touchmove : function(e){
            if(!this.is_move)return;
            var y = e.changedTouches[0].pageY;
            this.init_y += y - this.touchstart_y;
            this.touchstart_y = y;
            this.slider.style.transform = "translateY("+this.init_y+"px)";
        }
        ,touchend : function(e){
            document.removeEventListener('touchmove',this.prevent_default);
            this.is_move = false;
            var duration = Date.now() - this.first_time
            var dist = this.init_y - this.first_y;
            this.init_y = this.compute_pos(dist, duration,this.init_y, this.slider);
            this.get(this.init_y);
            this.changed_fn.call(this,this.value,this.index);
        }
        ,compute_pos : function(dist, duration, cur_y, elem){
            var param = this.momentum(dist, duration);
            elem.style['transition'] = "transform "+ param.time + 'ms';
            var y = cur_y + param.dist;
            if(y > 0){
                y = 0;
            }else if(y < -this.max_scroll){
                y = -this.max_scroll;
            }
            var locate_y = this.locate(y);              
            elem.style.transform = 'translateY(' + locate_y + 'px)';
            return locate_y;
        }
        ,momentum : function(dist, time){
            var deceleration = 0.002;
            var speed = Math.abs(dist) / time;
            var new_dist = (speed * speed) / (2 * deceleration);
            var new_time = 0;
            new_dist = new_dist * (dist < 0 ? -1 : 1);
            new_time = speed / deceleration;
            if(new_time > 1000){
                new_time = 1000;
            }else if(new_time < 500){
                new_time = 500;
            }
            return { 
                'dist': new_dist, 
                'time': new_time 
            };
        }
    }
    var tid = null;
    function X_panel(map){
        this.map = map || {};
        this.rs = {};
        this.title = this.map.title || "";
        this.done_fn = function(){};
        this.cancel_fn = function(){};
        this.add_css();
        this.create_panel();
        this.bind_event();
    }
    X_panel.prototype = {
        add_css : function(){
            var css = `
            .xpicker-wrap{background:#fff; position: absolute; left: 0; bottom: 0; width: 100%;z-index: 11111; transition: opacity 0.5s;opacity:0; box-sizing: border-box;}
            .xpicker-wrap *{box-sizing: border-box;}
            .xpicker-head{display: flex; border-bottom: 1px solid #ededed;width: 100%;position: fixed;top: 0;background: #fff;}
            .xpicker-head-left,.xpicker-head-right{display: flex;width:20%; height:40px; justify-content:center; align-items: center; font-size: 12px; color:#00b7ee;}
            .xpicker-head-left:active,.xpicker-head-right:active{background:#fafafa;}
            .xpicker-head-mid{display: flex;width:60%; height:40px; justify-content:center; align-items: center; font-size: 12px; color:#666;}
            .xpicker-content{width: 100%; display: flex;position: fixed; top: 120px;}
            /*slider初始位置*/
            .xpicker-slider{position: absolute;  top: 120px; width: 100%;  }
            /*slider初始位置*/
            /*设置列宽度*/
            .xpicker-slider-wrap{flex:1;height:280px; overflow: hidden; position: relative;}
            /*设置列宽度*/
            .xpicker-slider-row{width: 100%; height: 40px; display: flex; justify-content: center; align-items: center; font-size: 12px; color:#666;}
            .xpicker-mask{width: 100%; height: 100%; position: absolute; top: 0; left: 0; z-index: 22222; pointer-events: none;}
            .xpicker-mask-top{height:120px;background: -webkit-gradient(linear,left top,left bottom,from(rgb(255,255,255)),color-stop(0.45,rgba(255,255,255,.85)),color-stop(0.75,rgba(255,255,255,.6)),to(rgba(255,255,255,.4)));}
            .xpicker-mask-mid{height: 40px; border-top: 1px solid #ededed; border-bottom: 1px solid #ededed;display:none}
            .xpicker-mask-bottom{height:120px; background: -webkit-gradient(linear,left top,left bottom,from(rgba(255,255,255,.4)),color-stop(0.25,rgba(255,255,255,.6)),color-stop(0.65,rgba(255,255,255,.85)),to(rgb(255,255,255)));}`;
            var el = document.createElement('style');
            el.innerHTML = css;
            el.id = 'xpanel-style';
            // debugger
            var head = document.querySelector('head');
            var is_exist = document.querySelector('#xpanel-style');
            if(!is_exist){
                head.appendChild(el);
            }
        }
        ,create_panel : function(){
            this.el = document.createElement('div');
            this.el.className = 'xpicker-wrap';
            this.el.innerHTML = `<div class="xpicker-head">
                <div class="xpicker-head-left xpicker-cancel">
                    取消
                </div>
                <div class="xpicker-head-mid">
                    选择生日
                </div>
                <div class="xpicker-head-right xpicker-ok">
                    确定
                </div>
            </div>
            <div class="xpicker-content">
                
            </div>`;
            var title = this.el.querySelector('.xpicker-head-mid');
            title.innerHTML = this.title;
        }
        ,bind_event : function(){
            var ok = this.el.querySelector('.xpicker-ok');
            var cancel = this.el.querySelector('.xpicker-cancel');
            ok.onclick = this.ok.bind(this);
            cancel.onclick = this.cancel.bind(this);
        }
        ,ok : function(e){
                $("#zhuanye").animate({
                    "transition-property": "transform",
                    "transition-duration": "0.35s",
                    "transition-delay": "0s",
                    "transition-timing-function": "linear",
                    "display":"block",
                    "top":"100vh"
                })
               setTimeout(function(){
                  $("#zhuanye").hide()
                  $(".xpicker-head").hide()
               },100)
            this.remove();
            if(typeof x_mask != 'undefined' )x_mask.remove();
            this.done_fn.call(this,e);
        }
        ,cancel :function(e){
			 $("#zhuanye").animate({
                    "transition-property": "transform",
                    "transition-duration": "0.35s",
                    "transition-delay": "0s",
                    "transition-timing-function": "linear",
                    "display":"block",
                    "top":"100vh"
                })
               setTimeout(function(){
                  $("#zhuanye").hide()
                  $(".xpicker-head").hide()
               },100)
            this.remove();
            if(typeof x_mask != 'undefined')x_mask.remove();
            this.cancel_fn.call(this,e);
        }
        ,done : function(fn){
            this.done_fn = fn;
             $(".xpicker-head").show()
        }
        ,canceled : function(fn){
            this.cancel_fn = fn;
             $(".xpicker-head").show()
        }
        ,remove : function(){
            this.el.style.opacity = 0;
            this.is_remove = true;
            var me = this;
            clearTimeout(tid);
            tid = setTimeout(function(){
                var els = document.querySelectorAll('.xpicker-wrap');
                for(var i=0; i<els.length;i++){
                    var el = els[i];
                    el.parentNode.removeChild(el);
                }
            },150)
        }
        ,show : function(){
            var me = this;
            this.remove();
            document.body.appendChild(this.el);
            clearTimeout(tid);
            tid = setTimeout(function(){
                me.el.style.opacity = 1;
                $(".xpicker-head").show()
            },15);
        }
        ,add : function(){
            var list = [].slice.call(arguments);
            var content = this.el.querySelector('.xpicker-content');
            content.innerHTML = "";
            list.forEach(function(el) {
                content.appendChild(el);
            });
        }
    }
    win.X_picker = X_picker;
    win.X_panel = X_panel;
}(this);