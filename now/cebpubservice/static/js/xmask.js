!function (win) {
    var tid = null;
    function X_mask() {
        this.remove_cb = function () { };
        this.init();
    }
    X_mask.prototype = {
        remove: function () {
            var me = this;
            var mask = document.querySelector('.x-mask');
            this.mask.style.opacity = 0;
            if (mask) {
                clearTimeout(tid);
                tid = setTimeout(function() {
                    mask.parentNode.removeChild(mask);
                    me.remove_cb.call(this);
                }, 150);
            }
        }
        , removed: function (fn) {
            this.remove_cb = fn;
        }
        , init: function () {
            this.mask = document.createElement('div');
            this.mask.className = "x-mask";
            // this.mask.style.cssText = "width:100%; position:fixed; left:0; top:0;z-index:9999; background:rgba(0,0,0,0.3); opacity:0; transition:opacity 0.5s";
            this.mask.style.cssText = "display:none;width:100%; position:fixed; left:0; top:0;z-index:9999; background:rgba(0,0,0,0.3); opacity:0; transition:opacity 0.5s";
            this.mask.style.height = window.innerHeight + 'px';
        }
        , add: function () {
            var me = this;
            this.remove();
            document.body.appendChild(this.mask);
            clearTimeout(tid);
            tid = setTimeout(function(){
                me.mask.style.opacity = 1;
            },15)
        }
    }
    win.x_mask = new X_mask();
}(this);