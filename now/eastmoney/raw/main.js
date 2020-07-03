/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./jssrc/main.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./config/webconfig.js":
/*!*****************************!*\
  !*** ./config/webconfig.js ***!
  \*****************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = {
  test: {
    quotepath: function(){
      return 'http://61.129.249.233:18665/'
    },
    getpath: function(){
      return 'http://61.129.249.233:18665/'
    }
  },
  production: {
    quotepath: function(){
      var rnd = Math.floor(Math.random() * (99 - 1)) + 1
      return 'https://' + rnd + '.push2.eastmoney.com/'
    },
    getpath: function(){
      var rnd = Math.floor(Math.random() * (99 - 1)) + 1
      return 'https://push2.eastmoney.com/'
    }
  },
  getParam: function(name){
    var urlpara = location.search;
    var par = {};
    if (urlpara != "") {
      urlpara = urlpara.substring(1, urlpara.length);
      var para = urlpara.split("&");
      var parname;
      var parvalue;
      for (var i = 0; i < para.length; i++) {
        parname = para[i].substring(0, para[i].indexOf("="));
        parvalue = para[i].substring(para[i].indexOf("=") + 1, para[i].length);
        par[parname] = parvalue;
      }
    }
    if(typeof (par[name]) != "undefined"){
      return par[name];
    }
    else{
      return null;
    }
  },
  getWebPath: function (name) {
    if (this.getParam('env')) {
      return this[this.getParam('env')][name]()
    }
    return this.production[name]()
  }
}

/***/ }),

/***/ "./jssrc/main.js":
/*!***********************!*\
  !*** ./jssrc/main.js ***!
  \***********************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(/*! ../modules/polyfill */ "./modules/polyfill/index.js")

// $.ajaxSetup({
//   cache: false
// });

//全球时间
var qqsj = __webpack_require__(/*! ../modules/qqsj */ "./modules/qqsj/index.js")
qqsj()


var boxsize = __webpack_require__(/*! ../modules/boxsize */ "./modules/boxsize/index.js")
boxsize.init()


//登录注册
var user = __webpack_require__(/*! ../modules/user */ "./modules/user/index.js")
var thisuser = user.get()
if (thisuser) {
  $('#loginnick').text(thisuser.nick)
  $('#logoutlink').on('click', function(){
    user.logOut(function(){
      self.location.reload()
    })
  })
  $('#logind').show()
}
else{
  $('#nologind').show()
  $('#loginlink').attr('href', 'https://passport2.eastmoney.com/pub/login?backurl=' + encodeURIComponent(location.href))
  $('#reglink').attr('href', 'https://passport2.eastmoney.com/pub/reg?backurl=' + encodeURIComponent(location.href))  
}




if (window.suggest2017) {
  var newsuggest = new suggest2017({ //新建实例
    inputid: 'topnavsearch' //参数部分
  })  
}

//var popmenu = require('../modules/popmenu')

// var newpopmenu = new popmenu({
//   target: $('#popmenutest'),
//   items: [
//     $('<a href="javascript:;" target="_self">修改名称</a>'),
//     $('<a href="javascript:;" target="_self">删除组合</a>')
//   ]
// })

// var allstock_popmenu = new popmenu({
//   target: $('#allstock'),
//   items: [
//     $('<label><input type="checkbox"> 全部</label>'),
//     $('<a href="javascript:;" target="_self">删除组合</a>')
//   ]
// })


// var plsetting_popmenu = new popmenu({
//   target: $('#plsetting'),
//   items: [
//     $('<label><input type="checkbox"> 全部</label>'),
//     $('<a href="javascript:;" target="_self">删除组合</a>')
//   ]
// })

// var modalalert = require('../modules/modal/alert')
// modalalert('确定删除<i>该组</i>合？', function(){
//   console.info(222)
// })
// modal.confirm('确定删除该组合？', function(confirm_result){
//   console.info(confirm_result)
// })


var zshq = __webpack_require__(/*! ../modules/zshq */ "./modules/zshq/index.js")
zshq()
 

//快讯
var kuaixun = __webpack_require__(/*! ../modules/kuaixun */ "./modules/kuaixun/index.js")
kuaixun1 = new kuaixun({
    refreshbtn: $('#kx_refresh_t'),
    fontsizebtn: $('#kx_size_t'),
    autobtn: $('#kx_auto_t'),
    autosec: $('#kx_auto_sec_t'),
    kxlist: $('#kx_list_t'),
    kxloading: $('#kx_loading_t'),
    kxtype: '102',
    kxlink: 'http://kuaixun.eastmoney.com/' //http://js1.eastmoney.com/tg.aspx?ID=3493
});
kuaixun1.init();

//盘口异动
var pkyd = __webpack_require__(/*! ../modules/pkyd/web */ "./modules/pkyd/web.js")
pkyd.bind()


//自选股

var fingerprint = __webpack_require__(/*! ../modules/browser_fingerprint */ "./modules/browser_fingerprint/index.js")
fingerprint.get(function(fp){
  //console.info(fp)
  var zxg = __webpack_require__(/*! ../modules/zxg */ "./modules/zxg/index.js")
  var guba = __webpack_require__(/*! ../modules/guba/web */ "./modules/guba/web.js")
  var info = __webpack_require__(/*! ../modules/info/web */ "./modules/info/web.js") //信息流

  guba.init()
  zxg.init()    
})




//股吧

//


//主题投资
var zhuti = __webpack_require__(/*! ../modules/zhuti/web */ "./modules/zhuti/web.js")
zhuti.init()


// var fullscreen = require('../modules/fullscreen/web')
// fullscreen()



var zdtj = __webpack_require__(/*! ../modules/zdtj */ "./modules/zdtj/index.js")
zdtj.init()



var tixing = __webpack_require__(/*! ../modules/tixing */ "./modules/tixing/index.js")
$('#tixingtopbtn').click(function(){
  tixing.showList()
})

var addtixing = __webpack_require__(/*! ../modules/tixing/addtixing */ "./modules/tixing/addtixing.js")
addtixing.startTiXingTip()


/**
 * 绑定指标设置按钮
 */
var customitem = __webpack_require__(/*! ../modules/zxg/customitem */ "./modules/zxg/customitem.js")
customitem.bindBtn()

/**
 * 智能诊股
 */
var znzg = __webpack_require__(/*! ../modules/znzg */ "./modules/znzg/index.js")
znzg.init()

var batch_edit = __webpack_require__(/*! ../modules/zxg/batch_edit */ "./modules/zxg/batch_edit.js")
batch_edit.init()


var stock_filter = __webpack_require__(/*! ../modules/stock_filter */ "./modules/stock_filter/index.js")
stock_filter.init()

var guide = __webpack_require__(/*! ../modules/guide */ "./modules/guide/index.js")
guide.init()

var importcookie = __webpack_require__(/*! ../modules/importcookie */ "./modules/importcookie/index.js")
importcookie.bind($('#importcookiezxg'))

// var fltable = require('../modules/zxg/fltable')
// fltable.bind()

// window.refreshCSS = function () {
//   var sheets = [].slice.call(document.getElementsByTagName("link"));
//   var head = document.getElementsByTagName("head")[0];
//   for (var i = 0; i < sheets.length; ++i) {
//     var elem = sheets[i];
//     head.removeChild(elem);
//     var rel = elem.rel;
//     if (elem.href && typeof rel != "string" || rel.length == 0 || rel.toLowerCase() == "stylesheet") {
//       var url = elem.href.replace(/(&|\?)_cacheOverride=\d+/, '');
//       elem.href = url + (url.indexOf('?') >= 0 ? '&' : '?') + '_cacheOverride=' + (new Date().valueOf());
//     }
//     head.appendChild(elem);
//   }
// }

var user = __webpack_require__(/*! ../modules/user */ "./modules/user/index.js")
// if (user.get() == null) {
//   $('#gobackold').attr('href', 'http://quote.eastmoney.com/favor/default.html?from=zixuan')
// }

;(function(){
  if (window.localStorage) {



    // if (localStorage.getItem('showguide')) {
      
    // }
    // else{
    //   localStorage.setItem('showguide', '1')
    //   self.location = './guide'
    //   return false
    // }  

    if (localStorage.getItem('zktip')) {
      //$('#gubaswitchtip').show()
    }
    else{
      $('#gubaswitchtip').show()
      setTimeout(function(){
        $('#gubaswitchtip').hide()
      }, 30000);
      localStorage.setItem('zktip', '1')
    }

  }  
})()



/***/ }),

/***/ "./modules/bid/index.js":
/*!******************************!*\
  !*** ./modules/bid/index.js ***!
  \******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 浏览器id
 */

var cookie = __webpack_require__(/*! ../cookie */ "./modules/cookie/index.js")

module.exports = {
  get : function(){
      var zw = cookie.get('qgqp_b_id')
      if (zw == null) {
          return this.make()
      }
      else{
        return zw;
      }
      
  },
  make : function(){
      var newid = Math.floor(Math.random()*9+1).toString();
      for (var i = 0; i < 19; i++) {
          newid +=  Math.floor(Math.random()*9).toString();
          
      }
      cookie.set('qgqp_b_id', newid, 10000, '.eastmoney.com');
      return newid;
  },
  init: function(){
      if (this.get() == null || this.get() == '') {
          return this.make();
      }
      else{
          return this.get();
      }
  }
}

/***/ }),

/***/ "./modules/boxsize/index.js":
/*!**********************************!*\
  !*** ./modules/boxsize/index.js ***!
  \**********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 调整窗口大小
 */
var filltable = __webpack_require__(/*! ../zxg/filltable */ "./modules/zxg/filltable.js")
var debounce = __webpack_require__(/*! lodash/debounce */ "./node_modules/lodash/debounce.js")
var groups = __webpack_require__(/*! ../zxg/groups */ "./modules/zxg/groups.js")
var localstorage = __webpack_require__(/*! ../localstorage */ "./modules/localstorage/index.js")


var resize = {
  init: function(){
    resize.resize()
    resize.bind()
  },
  resize: function(){
    var height = $(window).height()
    if (height < 768) {
      height = 768
    }
    $('.main').height(height - 70)
    $('.mainl').height(height - 70)
    $('.mainr').height(height - 68)
    $('.zbb').height(height - 550) 
    resize.resizewtable()  
    filltable.resizeFill()
    groups.makeGroupHtml()
  },
  wtablefix: 311,
  resizewtable: function(){
    var height = $(window).height()
    if (height < 768) {
      height = 768
    }
    // console.info(111)
    $('.wl_table').height(height - ($('.gubanews').is(':visible')?$('.gubanews').height():-24) - resize.wtablefix + ($('#qqsj').is('.qqsj_short')?46:0))     
  },
  bind: function(){
    var _this = resize
    $(window).resize(debounce(function(){
      //console.info(111)
      _this.resize()
      
    }, 200))

    var wlth = $('.wlth')
    // $('.wl_table').scroll(function(){
    //   //console.info(111)
    //   //transform: translate(0,10px)
    //   //console.info($(this).scrollTop())
    //   wlth.css({
    //     transform: 'translate(0,' + $(this).scrollTop() + 'px)',
    //     '-ms-transform': 'translate(0,' + $(this).scrollTop() + 'px)'
    //   })
    // })


    $('#gubaswitch').add('#gubaswitch2').click(function(){ //底部开关
      if ($('.gubanews').is(':visible')) {
        //_this.wtablefix = 60 + $('.gubanews').height()
        $('.gubanews').hide()
        $('#gubaswitch').hide()
        $('#gubaswitch2').show()
        localstorage.set('bottom_switch', false)
      }
      else{
        $('.gubanews').show()
        $('#gubaswitch2').hide()
        $('#gubaswitch').show()
        localstorage.set('bottom_switch', true)
        //_this.wtablefix = 540
      }
      _this.resize()
    })

    $('#gubaswitchtip').click(function(){
      return false
    })

    $('#guideclose').click(function(){
      $('#gubaswitchtip').remove()
      return false
    })   

    $('#mainrzkt').add('#mainrzkt2').click(function(){ //右侧开关
      var m1440 = $('#m1440').is(':visible')

      if ($('.mainr').width() > 0) {
        $('.mainr').css({width:0})
        $('.mainrbody').hide()
        $('#mainrzkt').hide()
        $('#mainrzkt2').show()
        $('.mainl').css({'margin-right': 0})
        //_this.wtablefix = 540 - 249
        localstorage.set('right_switch', false)
      }
      else{
        
        $('.mainr').css({width:400})
        $('.mainrbody').show()
        $('#mainrzkt2').hide()
        $('#mainrzkt').show()
        if ( m1440 ) {
          $('.mainl').css({'margin-right': 400})
        }
        else{
          $('.mainl').css({'margin-right': 0})
        }
        localstorage.set('right_switch', true)
        //_this.wtablefix = 540
      }
      _this.resize()
    }) 

    //setTimeout(function(){
      if (localstorage.get('bottom_switch') == 'false') {
        $('#gubaswitch').click()
      }
      if (localstorage.get('right_switch') == 'false') {
        $('#mainrzkt').click()
      }      
    //}, 10);   

    //小于1920自动收起右侧
    if ( localstorage.get('right_switch') == null && $(window).width() < 1920) {
        $('.mainr').css({width:0})
        $('.mainrbody').hide()
        $('#mainrzkt').hide()
        $('#mainrzkt2').show()
        $('.mainl').css({'margin-right': 0})      
    }

  }
}

module.exports = resize



/***/ }),

/***/ "./modules/browser/index.js":
/*!**********************************!*\
  !*** ./modules/browser/index.js ***!
  \**********************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * 判断浏览器
 */

module.exports = {
  /**
   * 是否是IE6
   */
  isIE6: function(){
    return document.all && !window.XMLHttpRequest
  },
  isIE8: function(){
    return document.all && !document.addEventListener
  }
}

/***/ }),

/***/ "./modules/browser_fingerprint/fingerprint2.js":
/*!*****************************************************!*\
  !*** ./modules/browser_fingerprint/fingerprint2.js ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var __WEBPACK_AMD_DEFINE_FACTORY__, __WEBPACK_AMD_DEFINE_RESULT__;/*
* Fingerprintjs2 1.5.1 - Modern & flexible browser fingerprint library v2
* https://github.com/Valve/fingerprintjs2
* Copyright (c) 2015 Valentin Vasilyev (valentin.vasilyev@outlook.com)
* Licensed under the MIT (http://www.opensource.org/licenses/mit-license.php) license.
*
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
* AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
* IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
* ARE DISCLAIMED. IN NO EVENT SHALL VALENTIN VASILYEV BE LIABLE FOR ANY
* DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
* (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
* LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
* ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
* (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
* THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

(function (name, context, definition) {
  "use strict";
  if (true) { !(__WEBPACK_AMD_DEFINE_FACTORY__ = (definition),
				__WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ?
				(__WEBPACK_AMD_DEFINE_FACTORY__.call(exports, __webpack_require__, exports, module)) :
				__WEBPACK_AMD_DEFINE_FACTORY__),
				__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__)); }
  else {}
})("Fingerprint2", this, function() {
  "use strict";
  var Fingerprint2 = function(options) {

    if (!(this instanceof Fingerprint2)) {
      return new Fingerprint2(options);
    }

    var defaultOptions = {
      swfContainerId: "fingerprintjs2",
      swfPath: "flash/compiled/FontList.swf",
      detectScreenOrientation: true,
      sortPluginsFor: [/palemoon/i],
      userDefinedFonts: []
    };
    this.options = this.extend(options, defaultOptions);
    this.nativeForEach = Array.prototype.forEach;
    this.nativeMap = Array.prototype.map;
  };
  Fingerprint2.prototype = {
    extend: function(source, target) {
      if (source == null) { return target; }
      for (var k in source) {
        if(source[k] != null && target[k] !== source[k]) {
          target[k] = source[k];
        }
      }
      return target;
    },
    get: function(done){
      var keys = [];
      keys = this.userAgentKey(keys);
      keys = this.languageKey(keys);
      keys = this.colorDepthKey(keys);
      keys = this.pixelRatioKey(keys);
      keys = this.hardwareConcurrencyKey(keys);
      keys = this.screenResolutionKey(keys);
      keys = this.availableScreenResolutionKey(keys);
      keys = this.timezoneOffsetKey(keys);
      keys = this.sessionStorageKey(keys);
      keys = this.localStorageKey(keys);
      keys = this.indexedDbKey(keys);
      keys = this.addBehaviorKey(keys);
      keys = this.openDatabaseKey(keys);
      keys = this.cpuClassKey(keys);
      keys = this.platformKey(keys);
      keys = this.doNotTrackKey(keys);
      keys = this.pluginsKey(keys);
      keys = this.canvasKey(keys);
      keys = this.webglKey(keys);
      keys = this.adBlockKey(keys);
      keys = this.hasLiedLanguagesKey(keys);
      keys = this.hasLiedResolutionKey(keys);
      keys = this.hasLiedOsKey(keys);
      keys = this.hasLiedBrowserKey(keys);
      keys = this.touchSupportKey(keys);
      keys = this.customEntropyFunction(keys);
      var that = this;
      this.fontsKey(keys, function(newKeys){
        var values = [];
        that.each(newKeys, function(pair) {
          var value = pair.value;
          if (typeof pair.value.join !== "undefined") {
            value = pair.value.join(";");
          }
          values.push(value);
        });
        var murmur = that.x64hash128(values.join("~~~"), 31);
        return done(murmur, newKeys);
      });
    },
    customEntropyFunction: function (keys) {
      if (typeof this.options.customFunction === "function") {
        keys.push({key: "custom", value: this.options.customFunction()});
      }
      return keys;
    },
    userAgentKey: function(keys) {
      if(!this.options.excludeUserAgent) {
        keys.push({key: "user_agent", value: this.getUserAgent()});
      }
      return keys;
    },
    // for tests
    getUserAgent: function(){
      return navigator.userAgent;
    },
    languageKey: function(keys) {
      if(!this.options.excludeLanguage) {
        // IE 9,10 on Windows 10 does not have the `navigator.language` property any longer
        keys.push({ key: "language", value: navigator.language || navigator.userLanguage || navigator.browserLanguage || navigator.systemLanguage || "" });
      }
      return keys;
    },
    colorDepthKey: function(keys) {
      if(!this.options.excludeColorDepth) {
        keys.push({key: "color_depth", value: screen.colorDepth || -1});
      }
      return keys;
    },
    pixelRatioKey: function(keys) {
      if(!this.options.excludePixelRatio) {
        keys.push({key: "pixel_ratio", value: this.getPixelRatio()});
      }
      return keys;
    },
    getPixelRatio: function() {
      return window.devicePixelRatio || "";
    },
    screenResolutionKey: function(keys) {
      if(!this.options.excludeScreenResolution) {
        return this.getScreenResolution(keys);
      }
      return keys;
    },
    getScreenResolution: function(keys) {
      var resolution;
      if(this.options.detectScreenOrientation) {
        resolution = (screen.height > screen.width) ? [screen.height, screen.width] : [screen.width, screen.height];
      } else {
        resolution = [screen.width, screen.height];
      }
      if(typeof resolution !== "undefined") { // headless browsers
        keys.push({key: "resolution", value: resolution});
      }
      return keys;
    },
    availableScreenResolutionKey: function(keys) {
      if (!this.options.excludeAvailableScreenResolution) {
        return this.getAvailableScreenResolution(keys);
      }
      return keys;
    },
    getAvailableScreenResolution: function(keys) {
      var available;
      if(screen.availWidth && screen.availHeight) {
        if(this.options.detectScreenOrientation) {
          available = (screen.availHeight > screen.availWidth) ? [screen.availHeight, screen.availWidth] : [screen.availWidth, screen.availHeight];
        } else {
          available = [screen.availHeight, screen.availWidth];
        }
      }
      if(typeof available !== "undefined") { // headless browsers
        keys.push({key: "available_resolution", value: available});
      }
      return keys;
    },
    timezoneOffsetKey: function(keys) {
      if(!this.options.excludeTimezoneOffset) {
        keys.push({key: "timezone_offset", value: new Date().getTimezoneOffset()});
      }
      return keys;
    },
    sessionStorageKey: function(keys) {
      if(!this.options.excludeSessionStorage && this.hasSessionStorage()) {
        keys.push({key: "session_storage", value: 1});
      }
      return keys;
    },
    localStorageKey: function(keys) {
      if(!this.options.excludeSessionStorage && this.hasLocalStorage()) {
        keys.push({key: "local_storage", value: 1});
      }
      return keys;
    },
    indexedDbKey: function(keys) {
      if(!this.options.excludeIndexedDB && this.hasIndexedDB()) {
        keys.push({key: "indexed_db", value: 1});
      }
      return keys;
    },
    addBehaviorKey: function(keys) {
      //body might not be defined at this point or removed programmatically
      if(document.body && !this.options.excludeAddBehavior && document.body.addBehavior) {
        keys.push({key: "add_behavior", value: 1});
      }
      return keys;
    },
    openDatabaseKey: function(keys) {
      if(!this.options.excludeOpenDatabase && window.openDatabase) {
        keys.push({key: "open_database", value: 1});
      }
      return keys;
    },
    cpuClassKey: function(keys) {
      if(!this.options.excludeCpuClass) {
        keys.push({key: "cpu_class", value: this.getNavigatorCpuClass()});
      }
      return keys;
    },
    platformKey: function(keys) {
      if(!this.options.excludePlatform) {
        keys.push({key: "navigator_platform", value: this.getNavigatorPlatform()});
      }
      return keys;
    },
    doNotTrackKey: function(keys) {
      if(!this.options.excludeDoNotTrack) {
        keys.push({key: "do_not_track", value: this.getDoNotTrack()});
      }
      return keys;
    },
    canvasKey: function(keys) {
      if(!this.options.excludeCanvas && this.isCanvasSupported()) {
        keys.push({key: "canvas", value: this.getCanvasFp()});
      }
      return keys;
    },
    webglKey: function(keys) {
      if(this.options.excludeWebGL) {
        return keys;
      }
      if(!this.isWebGlSupported()) {
        return keys;
      }
      keys.push({key: "webgl", value: this.getWebglFp()});
      return keys;
    },
    adBlockKey: function(keys){
      if(!this.options.excludeAdBlock) {
        keys.push({key: "adblock", value: this.getAdBlock()});
      }
      return keys;
    },
    hasLiedLanguagesKey: function(keys){
      if(!this.options.excludeHasLiedLanguages){
        keys.push({key: "has_lied_languages", value: this.getHasLiedLanguages()});
      }
      return keys;
    },
    hasLiedResolutionKey: function(keys){
      if(!this.options.excludeHasLiedResolution){
        keys.push({key: "has_lied_resolution", value: this.getHasLiedResolution()});
      }
      return keys;
    },
    hasLiedOsKey: function(keys){
      if(!this.options.excludeHasLiedOs){
        keys.push({key: "has_lied_os", value: this.getHasLiedOs()});
      }
      return keys;
    },
    hasLiedBrowserKey: function(keys){
      if(!this.options.excludeHasLiedBrowser){
        keys.push({key: "has_lied_browser", value: this.getHasLiedBrowser()});
      }
      return keys;
    },
    fontsKey: function(keys, done) {
      if (this.options.excludeJsFonts) {
        return this.flashFontsKey(keys, done);
      }
      return this.jsFontsKey(keys, done);
    },
    // flash fonts (will increase fingerprinting time 20X to ~ 130-150ms)
    flashFontsKey: function(keys, done) {
      if(this.options.excludeFlashFonts) {
        return done(keys);
      }
      // we do flash if swfobject is loaded
      if(!this.hasSwfObjectLoaded()){
        return done(keys);
      }
      if(!this.hasMinFlashInstalled()){
        return done(keys);
      }
      if(typeof this.options.swfPath === "undefined"){
        return done(keys);
      }
      this.loadSwfAndDetectFonts(function(fonts){
        keys.push({key: "swf_fonts", value: fonts.join(";")});
        done(keys);
      });
    },
    // kudos to http://www.lalit.org/lab/javascript-css-font-detect/
    jsFontsKey: function(keys, done) {
      var that = this;
      // doing js fonts detection in a pseudo-async fashion
      return setTimeout(function(){

        // a font will be compared against all the three default fonts.
        // and if it doesn't match all 3 then that font is not available.
        var baseFonts = ["monospace", "sans-serif", "serif"];

        var fontList = [
                        "Andale Mono", "Arial", "Arial Black", "Arial Hebrew", "Arial MT", "Arial Narrow", "Arial Rounded MT Bold", "Arial Unicode MS",
                        "Bitstream Vera Sans Mono", "Book Antiqua", "Bookman Old Style",
                        "Calibri", "Cambria", "Cambria Math", "Century", "Century Gothic", "Century Schoolbook", "Comic Sans", "Comic Sans MS", "Consolas", "Courier", "Courier New",
                        "Garamond", "Geneva", "Georgia",
                        "Helvetica", "Helvetica Neue",
                        "Impact",
                        "Lucida Bright", "Lucida Calligraphy", "Lucida Console", "Lucida Fax", "LUCIDA GRANDE", "Lucida Handwriting", "Lucida Sans", "Lucida Sans Typewriter", "Lucida Sans Unicode",
                        "Microsoft Sans Serif", "Monaco", "Monotype Corsiva", "MS Gothic", "MS Outlook", "MS PGothic", "MS Reference Sans Serif", "MS Sans Serif", "MS Serif", "MYRIAD", "MYRIAD PRO",
                        "Palatino", "Palatino Linotype",
                        "Segoe Print", "Segoe Script", "Segoe UI", "Segoe UI Light", "Segoe UI Semibold", "Segoe UI Symbol",
                        "Tahoma", "Times", "Times New Roman", "Times New Roman PS", "Trebuchet MS",
                        "Verdana", "Wingdings", "Wingdings 2", "Wingdings 3"
                      ];
        var extendedFontList = [
                        "Abadi MT Condensed Light", "Academy Engraved LET", "ADOBE CASLON PRO", "Adobe Garamond", "ADOBE GARAMOND PRO", "Agency FB", "Aharoni", "Albertus Extra Bold", "Albertus Medium", "Algerian", "Amazone BT", "American Typewriter",
                        "American Typewriter Condensed", "AmerType Md BT", "Andalus", "Angsana New", "AngsanaUPC", "Antique Olive", "Aparajita", "Apple Chancery", "Apple Color Emoji", "Apple SD Gothic Neo", "Arabic Typesetting", "ARCHER",
                         "ARNO PRO", "Arrus BT", "Aurora Cn BT", "AvantGarde Bk BT", "AvantGarde Md BT", "AVENIR", "Ayuthaya", "Bandy", "Bangla Sangam MN", "Bank Gothic", "BankGothic Md BT", "Baskerville",
                        "Baskerville Old Face", "Batang", "BatangChe", "Bauer Bodoni", "Bauhaus 93", "Bazooka", "Bell MT", "Bembo", "Benguiat Bk BT", "Berlin Sans FB", "Berlin Sans FB Demi", "Bernard MT Condensed", "BernhardFashion BT", "BernhardMod BT", "Big Caslon", "BinnerD",
                        "Blackadder ITC", "BlairMdITC TT", "Bodoni 72", "Bodoni 72 Oldstyle", "Bodoni 72 Smallcaps", "Bodoni MT", "Bodoni MT Black", "Bodoni MT Condensed", "Bodoni MT Poster Compressed",
                        "Bookshelf Symbol 7", "Boulder", "Bradley Hand", "Bradley Hand ITC", "Bremen Bd BT", "Britannic Bold", "Broadway", "Browallia New", "BrowalliaUPC", "Brush Script MT", "Californian FB", "Calisto MT", "Calligrapher", "Candara",
                        "CaslonOpnface BT", "Castellar", "Centaur", "Cezanne", "CG Omega", "CG Times", "Chalkboard", "Chalkboard SE", "Chalkduster", "Charlesworth", "Charter Bd BT", "Charter BT", "Chaucer",
                        "ChelthmITC Bk BT", "Chiller", "Clarendon", "Clarendon Condensed", "CloisterBlack BT", "Cochin", "Colonna MT", "Constantia", "Cooper Black", "Copperplate", "Copperplate Gothic", "Copperplate Gothic Bold",
                        "Copperplate Gothic Light", "CopperplGoth Bd BT", "Corbel", "Cordia New", "CordiaUPC", "Cornerstone", "Coronet", "Cuckoo", "Curlz MT", "DaunPenh", "Dauphin", "David", "DB LCD Temp", "DELICIOUS", "Denmark",
                        "DFKai-SB", "Didot", "DilleniaUPC", "DIN", "DokChampa", "Dotum", "DotumChe", "Ebrima", "Edwardian Script ITC", "Elephant", "English 111 Vivace BT", "Engravers MT", "EngraversGothic BT", "Eras Bold ITC", "Eras Demi ITC", "Eras Light ITC", "Eras Medium ITC",
                        "EucrosiaUPC", "Euphemia", "Euphemia UCAS", "EUROSTILE", "Exotc350 Bd BT", "FangSong", "Felix Titling", "Fixedsys", "FONTIN", "Footlight MT Light", "Forte",
                        "FrankRuehl", "Fransiscan", "Freefrm721 Blk BT", "FreesiaUPC", "Freestyle Script", "French Script MT", "FrnkGothITC Bk BT", "Fruitger", "FRUTIGER",
                        "Futura", "Futura Bk BT", "Futura Lt BT", "Futura Md BT", "Futura ZBlk BT", "FuturaBlack BT", "Gabriola", "Galliard BT", "Gautami", "Geeza Pro", "Geometr231 BT", "Geometr231 Hv BT", "Geometr231 Lt BT", "GeoSlab 703 Lt BT",
                        "GeoSlab 703 XBd BT", "Gigi", "Gill Sans", "Gill Sans MT", "Gill Sans MT Condensed", "Gill Sans MT Ext Condensed Bold", "Gill Sans Ultra Bold", "Gill Sans Ultra Bold Condensed", "Gisha", "Gloucester MT Extra Condensed", "GOTHAM", "GOTHAM BOLD",
                        "Goudy Old Style", "Goudy Stout", "GoudyHandtooled BT", "GoudyOLSt BT", "Gujarati Sangam MN", "Gulim", "GulimChe", "Gungsuh", "GungsuhChe", "Gurmukhi MN", "Haettenschweiler", "Harlow Solid Italic", "Harrington", "Heather", "Heiti SC", "Heiti TC", "HELV",
                        "Herald", "High Tower Text", "Hiragino Kaku Gothic ProN", "Hiragino Mincho ProN", "Hoefler Text", "Humanst 521 Cn BT", "Humanst521 BT", "Humanst521 Lt BT", "Imprint MT Shadow", "Incised901 Bd BT", "Incised901 BT",
                        "Incised901 Lt BT", "INCONSOLATA", "Informal Roman", "Informal011 BT", "INTERSTATE", "IrisUPC", "Iskoola Pota", "JasmineUPC", "Jazz LET", "Jenson", "Jester", "Jokerman", "Juice ITC", "Kabel Bk BT", "Kabel Ult BT", "Kailasa", "KaiTi", "Kalinga", "Kannada Sangam MN",
                        "Kartika", "Kaufmann Bd BT", "Kaufmann BT", "Khmer UI", "KodchiangUPC", "Kokila", "Korinna BT", "Kristen ITC", "Krungthep", "Kunstler Script", "Lao UI", "Latha", "Leelawadee", "Letter Gothic", "Levenim MT", "LilyUPC", "Lithograph", "Lithograph Light", "Long Island",
                        "Lydian BT", "Magneto", "Maiandra GD", "Malayalam Sangam MN", "Malgun Gothic",
                        "Mangal", "Marigold", "Marion", "Marker Felt", "Market", "Marlett", "Matisse ITC", "Matura MT Script Capitals", "Meiryo", "Meiryo UI", "Microsoft Himalaya", "Microsoft JhengHei", "Microsoft New Tai Lue", "Microsoft PhagsPa", "Microsoft Tai Le",
                        "Microsoft Uighur", "Microsoft YaHei", "Microsoft Yi Baiti", "MingLiU", "MingLiU_HKSCS", "MingLiU_HKSCS-ExtB", "MingLiU-ExtB", "Minion", "Minion Pro", "Miriam", "Miriam Fixed", "Mistral", "Modern", "Modern No. 20", "Mona Lisa Solid ITC TT", "Mongolian Baiti",
                        "MONO", "MoolBoran", "Mrs Eaves", "MS LineDraw", "MS Mincho", "MS PMincho", "MS Reference Specialty", "MS UI Gothic", "MT Extra", "MUSEO", "MV Boli",
                        "Nadeem", "Narkisim", "NEVIS", "News Gothic", "News GothicMT", "NewsGoth BT", "Niagara Engraved", "Niagara Solid", "Noteworthy", "NSimSun", "Nyala", "OCR A Extended", "Old Century", "Old English Text MT", "Onyx", "Onyx BT", "OPTIMA", "Oriya Sangam MN",
                        "OSAKA", "OzHandicraft BT", "Palace Script MT", "Papyrus", "Parchment", "Party LET", "Pegasus", "Perpetua", "Perpetua Titling MT", "PetitaBold", "Pickwick", "Plantagenet Cherokee", "Playbill", "PMingLiU", "PMingLiU-ExtB",
                        "Poor Richard", "Poster", "PosterBodoni BT", "PRINCETOWN LET", "Pristina", "PTBarnum BT", "Pythagoras", "Raavi", "Rage Italic", "Ravie", "Ribbon131 Bd BT", "Rockwell", "Rockwell Condensed", "Rockwell Extra Bold", "Rod", "Roman", "Sakkal Majalla",
                        "Santa Fe LET", "Savoye LET", "Sceptre", "Script", "Script MT Bold", "SCRIPTINA", "Serifa", "Serifa BT", "Serifa Th BT", "ShelleyVolante BT", "Sherwood",
                        "Shonar Bangla", "Showcard Gothic", "Shruti", "Signboard", "SILKSCREEN", "SimHei", "Simplified Arabic", "Simplified Arabic Fixed", "SimSun", "SimSun-ExtB", "Sinhala Sangam MN", "Sketch Rockwell", "Skia", "Small Fonts", "Snap ITC", "Snell Roundhand", "Socket",
                        "Souvenir Lt BT", "Staccato222 BT", "Steamer", "Stencil", "Storybook", "Styllo", "Subway", "Swis721 BlkEx BT", "Swiss911 XCm BT", "Sylfaen", "Synchro LET", "System", "Tamil Sangam MN", "Technical", "Teletype", "Telugu Sangam MN", "Tempus Sans ITC",
                        "Terminal", "Thonburi", "Traditional Arabic", "Trajan", "TRAJAN PRO", "Tristan", "Tubular", "Tunga", "Tw Cen MT", "Tw Cen MT Condensed", "Tw Cen MT Condensed Extra Bold",
                        "TypoUpright BT", "Unicorn", "Univers", "Univers CE 55 Medium", "Univers Condensed", "Utsaah", "Vagabond", "Vani", "Vijaya", "Viner Hand ITC", "VisualUI", "Vivaldi", "Vladimir Script", "Vrinda", "Westminster", "WHITNEY", "Wide Latin",
                        "ZapfEllipt BT", "ZapfHumnst BT", "ZapfHumnst Dm BT", "Zapfino", "Zurich BlkEx BT", "Zurich Ex BT", "ZWAdobeF"];

        if(that.options.extendedJsFonts) {
            fontList = fontList.concat(extendedFontList);
        }

        fontList = fontList.concat(that.options.userDefinedFonts);

        //we use m or w because these two characters take up the maximum width.
        // And we use a LLi so that the same matching fonts can get separated
        var testString = "mmmmmmmmmmlli";

        //we test using 72px font size, we may use any size. I guess larger the better.
        var testSize = "72px";

        var h = document.getElementsByTagName("body")[0];

        // div to load spans for the base fonts
        var baseFontsDiv = document.createElement("div");

        // div to load spans for the fonts to detect
        var fontsDiv = document.createElement("div");

        var defaultWidth = {};
        var defaultHeight = {};

        // creates a span where the fonts will be loaded
        var createSpan = function() {
            var s = document.createElement("span");
            /*
             * We need this css as in some weird browser this
             * span elements shows up for a microSec which creates a
             * bad user experience
             */
            s.style.position = "absolute";
            s.style.left = "-9999px";
            s.style.fontSize = testSize;
            s.style.lineHeight = "normal";
            s.innerHTML = testString;
            return s;
        };

        // creates a span and load the font to detect and a base font for fallback
        var createSpanWithFonts = function(fontToDetect, baseFont) {
            var s = createSpan();
            s.style.fontFamily = "'" + fontToDetect + "'," + baseFont;
            return s;
        };

        // creates spans for the base fonts and adds them to baseFontsDiv
        var initializeBaseFontsSpans = function() {
            var spans = [];
            for (var index = 0, length = baseFonts.length; index < length; index++) {
                var s = createSpan();
                s.style.fontFamily = baseFonts[index];
                baseFontsDiv.appendChild(s);
                spans.push(s);
            }
            return spans;
        };

        // creates spans for the fonts to detect and adds them to fontsDiv
        var initializeFontsSpans = function() {
            var spans = {};
            for(var i = 0, l = fontList.length; i < l; i++) {
                var fontSpans = [];
                for(var j = 0, numDefaultFonts = baseFonts.length; j < numDefaultFonts; j++) {
                    var s = createSpanWithFonts(fontList[i], baseFonts[j]);
                    fontsDiv.appendChild(s);
                    fontSpans.push(s);
                }
                spans[fontList[i]] = fontSpans; // Stores {fontName : [spans for that font]}
            }
            return spans;
        };

        // checks if a font is available
        var isFontAvailable = function(fontSpans) {
            var detected = false;
            for(var i = 0; i < baseFonts.length; i++) {
                detected = (fontSpans[i].offsetWidth !== defaultWidth[baseFonts[i]] || fontSpans[i].offsetHeight !== defaultHeight[baseFonts[i]]);
                if(detected) {
                    return detected;
                }
            }
            return detected;
        };

        // create spans for base fonts
        var baseFontsSpans = initializeBaseFontsSpans();

        // add the spans to the DOM
        h.appendChild(baseFontsDiv);

        // get the default width for the three base fonts
        for (var index = 0, length = baseFonts.length; index < length; index++) {
            defaultWidth[baseFonts[index]] = baseFontsSpans[index].offsetWidth; // width for the default font
            defaultHeight[baseFonts[index]] = baseFontsSpans[index].offsetHeight; // height for the default font
        }

        // create spans for fonts to detect
        var fontsSpans = initializeFontsSpans();

        // add all the spans to the DOM
        h.appendChild(fontsDiv);

        // check available fonts
        var available = [];
        for(var i = 0, l = fontList.length; i < l; i++) {
            if(isFontAvailable(fontsSpans[fontList[i]])) {
                available.push(fontList[i]);
            }
        }

        // remove spans from DOM
        h.removeChild(fontsDiv);
        h.removeChild(baseFontsDiv);

        keys.push({key: "js_fonts", value: available});
        done(keys);
      }, 1);
    },
    pluginsKey: function(keys) {
      if(!this.options.excludePlugins){
        if(this.isIE()){
          if(!this.options.excludeIEPlugins) {
            keys.push({key: "ie_plugins", value: this.getIEPlugins()});
          }
        } else {
          keys.push({key: "regular_plugins", value: this.getRegularPlugins()});
        }
      }
      return keys;
    },
    getRegularPlugins: function () {
      var plugins = [];
      for(var i = 0, l = navigator.plugins.length; i < l; i++) {
        plugins.push(navigator.plugins[i]);
      }
      // sorting plugins only for those user agents, that we know randomize the plugins
      // every time we try to enumerate them
      if(this.pluginsShouldBeSorted()) {
        plugins = plugins.sort(function(a, b) {
          if(a.name > b.name){ return 1; }
          if(a.name < b.name){ return -1; }
          return 0;
        });
      }
      return this.map(plugins, function (p) {
        var mimeTypes = this.map(p, function(mt){
          return [mt.type, mt.suffixes].join("~");
        }).join(",");
        return [p.name, p.description, mimeTypes].join("::");
      }, this);
    },
    getIEPlugins: function () {
      var result = [];
      if((Object.getOwnPropertyDescriptor && Object.getOwnPropertyDescriptor(window, "ActiveXObject")) || ("ActiveXObject" in window)) {
        var names = [
          "AcroPDF.PDF", // Adobe PDF reader 7+
          "Adodb.Stream",
          "AgControl.AgControl", // Silverlight
          "DevalVRXCtrl.DevalVRXCtrl.1",
          "MacromediaFlashPaper.MacromediaFlashPaper",
          "Msxml2.DOMDocument",
          "Msxml2.XMLHTTP",
          "PDF.PdfCtrl", // Adobe PDF reader 6 and earlier, brrr
          "QuickTime.QuickTime", // QuickTime
          "QuickTimeCheckObject.QuickTimeCheck.1",
          "RealPlayer",
          "RealPlayer.RealPlayer(tm) ActiveX Control (32-bit)",
          "RealVideo.RealVideo(tm) ActiveX Control (32-bit)",
          "Scripting.Dictionary",
          "SWCtl.SWCtl", // ShockWave player
          "Shell.UIHelper",
          "ShockwaveFlash.ShockwaveFlash", //flash plugin
          "Skype.Detection",
          "TDCCtl.TDCCtl",
          "WMPlayer.OCX", // Windows media player
          "rmocx.RealPlayer G2 Control",
          "rmocx.RealPlayer G2 Control.1"
        ];
        // starting to detect plugins in IE
        result = this.map(names, function(name) {
          try {
            new ActiveXObject(name); // eslint-disable-no-new
            return name;
          } catch(e) {
            return null;
          }
        });
      }
      if(navigator.plugins) {
        result = result.concat(this.getRegularPlugins());
      }
      return result;
    },
    pluginsShouldBeSorted: function () {
      var should = false;
      for(var i = 0, l = this.options.sortPluginsFor.length; i < l; i++) {
        var re = this.options.sortPluginsFor[i];
        if(navigator.userAgent.match(re)) {
          should = true;
          break;
        }
      }
      return should;
    },
    touchSupportKey: function (keys) {
      if(!this.options.excludeTouchSupport){
        keys.push({key: "touch_support", value: this.getTouchSupport()});
      }
      return keys;
    },
    hardwareConcurrencyKey: function(keys){
      if(!this.options.excludeHardwareConcurrency){
        keys.push({key: "hardware_concurrency", value: this.getHardwareConcurrency()});
      }
      return keys;
    },
    hasSessionStorage: function () {
      try {
        return !!window.sessionStorage;
      } catch(e) {
        return true; // SecurityError when referencing it means it exists
      }
    },
    // https://bugzilla.mozilla.org/show_bug.cgi?id=781447
    hasLocalStorage: function () {
      try {
        return !!window.localStorage;
      } catch(e) {
        return true; // SecurityError when referencing it means it exists
      }
    },
    hasIndexedDB: function (){
      try {
        return !!window.indexedDB;
      } catch(e) {
        return true; // SecurityError when referencing it means it exists
      }
    },
    getHardwareConcurrency: function(){
      if(navigator.hardwareConcurrency){
        return navigator.hardwareConcurrency;
      }
      return "unknown";
    },
    getNavigatorCpuClass: function () {
      if(navigator.cpuClass){
        return navigator.cpuClass;
      } else {
        return "unknown";
      }
    },
    getNavigatorPlatform: function () {
      if(navigator.platform) {
        return navigator.platform;
      } else {
        return "unknown";
      }
    },
    getDoNotTrack: function () {
      if(navigator.doNotTrack) {
        return navigator.doNotTrack;
      } else if (navigator.msDoNotTrack) {
        return navigator.msDoNotTrack;
      } else if (window.doNotTrack) {
        return window.doNotTrack;
      } else {
        return "unknown";
      }
    },
    // This is a crude and primitive touch screen detection.
    // It's not possible to currently reliably detect the  availability of a touch screen
    // with a JS, without actually subscribing to a touch event.
    // http://www.stucox.com/blog/you-cant-detect-a-touchscreen/
    // https://github.com/Modernizr/Modernizr/issues/548
    // method returns an array of 3 values:
    // maxTouchPoints, the success or failure of creating a TouchEvent,
    // and the availability of the 'ontouchstart' property
    getTouchSupport: function () {
      var maxTouchPoints = 0;
      var touchEvent = false;
      if(typeof navigator.maxTouchPoints !== "undefined") {
        maxTouchPoints = navigator.maxTouchPoints;
      } else if (typeof navigator.msMaxTouchPoints !== "undefined") {
        maxTouchPoints = navigator.msMaxTouchPoints;
      }
      try {
        document.createEvent("TouchEvent");
        touchEvent = true;
      } catch(_) { /* squelch */ }
      var touchStart = "ontouchstart" in window;
      return [maxTouchPoints, touchEvent, touchStart];
    },
    // https://www.browserleaks.com/canvas#how-does-it-work
    getCanvasFp: function() {
      var result = [];
      // Very simple now, need to make it more complex (geo shapes etc)
      var canvas = document.createElement("canvas");
      canvas.width = 2000;
      canvas.height = 200;
      canvas.style.display = "inline";
      var ctx = canvas.getContext("2d");
      // detect browser support of canvas winding
      // http://blogs.adobe.com/webplatform/2013/01/30/winding-rules-in-canvas/
      // https://github.com/Modernizr/Modernizr/blob/master/feature-detects/canvas/winding.js
      ctx.rect(0, 0, 10, 10);
      ctx.rect(2, 2, 6, 6);
      result.push("canvas winding:" + ((ctx.isPointInPath(5, 5, "evenodd") === false) ? "yes" : "no"));

      ctx.textBaseline = "alphabetic";
      ctx.fillStyle = "#f60";
      ctx.fillRect(125, 1, 62, 20);
      ctx.fillStyle = "#069";
      // https://github.com/Valve/fingerprintjs2/issues/66
      if(this.options.dontUseFakeFontInCanvas) {
        ctx.font = "11pt Arial";
      } else {
        ctx.font = "11pt no-real-font-123";
      }
      ctx.fillText("Cwm fjordbank glyphs vext quiz, \ud83d\ude03", 2, 15);
      ctx.fillStyle = "rgba(102, 204, 0, 0.2)";
      ctx.font = "18pt Arial";
      ctx.fillText("Cwm fjordbank glyphs vext quiz, \ud83d\ude03", 4, 45);

      // canvas blending
      // http://blogs.adobe.com/webplatform/2013/01/28/blending-features-in-canvas/
      // http://jsfiddle.net/NDYV8/16/
      ctx.globalCompositeOperation = "multiply";
      ctx.fillStyle = "rgb(255,0,255)";
      ctx.beginPath();
      ctx.arc(50, 50, 50, 0, Math.PI * 2, true);
      ctx.closePath();
      ctx.fill();
      ctx.fillStyle = "rgb(0,255,255)";
      ctx.beginPath();
      ctx.arc(100, 50, 50, 0, Math.PI * 2, true);
      ctx.closePath();
      ctx.fill();
      ctx.fillStyle = "rgb(255,255,0)";
      ctx.beginPath();
      ctx.arc(75, 100, 50, 0, Math.PI * 2, true);
      ctx.closePath();
      ctx.fill();
      ctx.fillStyle = "rgb(255,0,255)";
      // canvas winding
      // http://blogs.adobe.com/webplatform/2013/01/30/winding-rules-in-canvas/
      // http://jsfiddle.net/NDYV8/19/
      ctx.arc(75, 75, 75, 0, Math.PI * 2, true);
      ctx.arc(75, 75, 25, 0, Math.PI * 2, true);
      ctx.fill("evenodd");

      result.push("canvas fp:" + canvas.toDataURL());
      return result.join("~");
    },

    getWebglFp: function() {
      var gl;
      var fa2s = function(fa) {
        gl.clearColor(0.0, 0.0, 0.0, 1.0);
        gl.enable(gl.DEPTH_TEST);
        gl.depthFunc(gl.LEQUAL);
        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
        return "[" + fa[0] + ", " + fa[1] + "]";
      };
      var maxAnisotropy = function(gl) {
        var anisotropy, ext = gl.getExtension("EXT_texture_filter_anisotropic") || gl.getExtension("WEBKIT_EXT_texture_filter_anisotropic") || gl.getExtension("MOZ_EXT_texture_filter_anisotropic");
        return ext ? (anisotropy = gl.getParameter(ext.MAX_TEXTURE_MAX_ANISOTROPY_EXT), 0 === anisotropy && (anisotropy = 2), anisotropy) : null;
      };
      gl = this.getWebglCanvas();
      if(!gl) { return null; }
      // WebGL fingerprinting is a combination of techniques, found in MaxMind antifraud script & Augur fingerprinting.
      // First it draws a gradient object with shaders and convers the image to the Base64 string.
      // Then it enumerates all WebGL extensions & capabilities and appends them to the Base64 string, resulting in a huge WebGL string, potentially very unique on each device
      // Since iOS supports webgl starting from version 8.1 and 8.1 runs on several graphics chips, the results may be different across ios devices, but we need to verify it.
      var result = [];
      var vShaderTemplate = "attribute vec2 attrVertex;varying vec2 varyinTexCoordinate;uniform vec2 uniformOffset;void main(){varyinTexCoordinate=attrVertex+uniformOffset;gl_Position=vec4(attrVertex,0,1);}";
      var fShaderTemplate = "precision mediump float;varying vec2 varyinTexCoordinate;void main() {gl_FragColor=vec4(varyinTexCoordinate,0,1);}";
      var vertexPosBuffer = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, vertexPosBuffer);
      var vertices = new Float32Array([-.2, -.9, 0, .4, -.26, 0, 0, .732134444, 0]);
      gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);
      vertexPosBuffer.itemSize = 3;
      vertexPosBuffer.numItems = 3;
      var program = gl.createProgram(), vshader = gl.createShader(gl.VERTEX_SHADER);
      gl.shaderSource(vshader, vShaderTemplate);
      gl.compileShader(vshader);
      var fshader = gl.createShader(gl.FRAGMENT_SHADER);
      gl.shaderSource(fshader, fShaderTemplate);
      gl.compileShader(fshader);
      gl.attachShader(program, vshader);
      gl.attachShader(program, fshader);
      gl.linkProgram(program);
      gl.useProgram(program);
      program.vertexPosAttrib = gl.getAttribLocation(program, "attrVertex");
      program.offsetUniform = gl.getUniformLocation(program, "uniformOffset");
      gl.enableVertexAttribArray(program.vertexPosArray);
      gl.vertexAttribPointer(program.vertexPosAttrib, vertexPosBuffer.itemSize, gl.FLOAT, !1, 0, 0);
      gl.uniform2f(program.offsetUniform, 1, 1);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, vertexPosBuffer.numItems);
      if (gl.canvas != null) { result.push(gl.canvas.toDataURL()); }
      result.push("extensions:" + gl.getSupportedExtensions().join(";"));
      result.push("webgl aliased line width range:" + fa2s(gl.getParameter(gl.ALIASED_LINE_WIDTH_RANGE)));
      result.push("webgl aliased point size range:" + fa2s(gl.getParameter(gl.ALIASED_POINT_SIZE_RANGE)));
      result.push("webgl alpha bits:" + gl.getParameter(gl.ALPHA_BITS));
      result.push("webgl antialiasing:" + (gl.getContextAttributes().antialias ? "yes" : "no"));
      result.push("webgl blue bits:" + gl.getParameter(gl.BLUE_BITS));
      result.push("webgl depth bits:" + gl.getParameter(gl.DEPTH_BITS));
      result.push("webgl green bits:" + gl.getParameter(gl.GREEN_BITS));
      result.push("webgl max anisotropy:" + maxAnisotropy(gl));
      result.push("webgl max combined texture image units:" + gl.getParameter(gl.MAX_COMBINED_TEXTURE_IMAGE_UNITS));
      result.push("webgl max cube map texture size:" + gl.getParameter(gl.MAX_CUBE_MAP_TEXTURE_SIZE));
      result.push("webgl max fragment uniform vectors:" + gl.getParameter(gl.MAX_FRAGMENT_UNIFORM_VECTORS));
      result.push("webgl max render buffer size:" + gl.getParameter(gl.MAX_RENDERBUFFER_SIZE));
      result.push("webgl max texture image units:" + gl.getParameter(gl.MAX_TEXTURE_IMAGE_UNITS));
      result.push("webgl max texture size:" + gl.getParameter(gl.MAX_TEXTURE_SIZE));
      result.push("webgl max varying vectors:" + gl.getParameter(gl.MAX_VARYING_VECTORS));
      result.push("webgl max vertex attribs:" + gl.getParameter(gl.MAX_VERTEX_ATTRIBS));
      result.push("webgl max vertex texture image units:" + gl.getParameter(gl.MAX_VERTEX_TEXTURE_IMAGE_UNITS));
      result.push("webgl max vertex uniform vectors:" + gl.getParameter(gl.MAX_VERTEX_UNIFORM_VECTORS));
      result.push("webgl max viewport dims:" + fa2s(gl.getParameter(gl.MAX_VIEWPORT_DIMS)));
      result.push("webgl red bits:" + gl.getParameter(gl.RED_BITS));
      result.push("webgl renderer:" + gl.getParameter(gl.RENDERER));
      result.push("webgl shading language version:" + gl.getParameter(gl.SHADING_LANGUAGE_VERSION));
      result.push("webgl stencil bits:" + gl.getParameter(gl.STENCIL_BITS));
      result.push("webgl vendor:" + gl.getParameter(gl.VENDOR));
      result.push("webgl version:" + gl.getParameter(gl.VERSION));

      try {
        // Add the unmasked vendor and unmasked renderer if the debug_renderer_info extension is available
        var extensionDebugRendererInfo = gl.getExtension("WEBGL_debug_renderer_info");
        if (extensionDebugRendererInfo) {
          result.push("webgl unmasked vendor:" + gl.getParameter(extensionDebugRendererInfo.UNMASKED_VENDOR_WEBGL));
          result.push("webgl unmasked renderer:" + gl.getParameter(extensionDebugRendererInfo.UNMASKED_RENDERER_WEBGL));
        }
      } catch(e) { /* squelch */ }

      if (!gl.getShaderPrecisionFormat) {
        return result.join("~");
      }

      result.push("webgl vertex shader high float precision:" + gl.getShaderPrecisionFormat(gl.VERTEX_SHADER, gl.HIGH_FLOAT ).precision);
      result.push("webgl vertex shader high float precision rangeMin:" + gl.getShaderPrecisionFormat(gl.VERTEX_SHADER, gl.HIGH_FLOAT ).rangeMin);
      result.push("webgl vertex shader high float precision rangeMax:" + gl.getShaderPrecisionFormat(gl.VERTEX_SHADER, gl.HIGH_FLOAT ).rangeMax);
      result.push("webgl vertex shader medium float precision:" + gl.getShaderPrecisionFormat(gl.VERTEX_SHADER, gl.MEDIUM_FLOAT ).precision);
      result.push("webgl vertex shader medium float precision rangeMin:" + gl.getShaderPrecisionFormat(gl.VERTEX_SHADER, gl.MEDIUM_FLOAT ).rangeMin);
      result.push("webgl vertex shader medium float precision rangeMax:" + gl.getShaderPrecisionFormat(gl.VERTEX_SHADER, gl.MEDIUM_FLOAT ).rangeMax);
      result.push("webgl vertex shader low float precision:" + gl.getShaderPrecisionFormat(gl.VERTEX_SHADER, gl.LOW_FLOAT ).precision);
      result.push("webgl vertex shader low float precision rangeMin:" + gl.getShaderPrecisionFormat(gl.VERTEX_SHADER, gl.LOW_FLOAT ).rangeMin);
      result.push("webgl vertex shader low float precision rangeMax:" + gl.getShaderPrecisionFormat(gl.VERTEX_SHADER, gl.LOW_FLOAT ).rangeMax);
      result.push("webgl fragment shader high float precision:" + gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.HIGH_FLOAT ).precision);
      result.push("webgl fragment shader high float precision rangeMin:" + gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.HIGH_FLOAT ).rangeMin);
      result.push("webgl fragment shader high float precision rangeMax:" + gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.HIGH_FLOAT ).rangeMax);
      result.push("webgl fragment shader medium float precision:" + gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.MEDIUM_FLOAT ).precision);
      result.push("webgl fragment shader medium float precision rangeMin:" + gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.MEDIUM_FLOAT ).rangeMin);
      result.push("webgl fragment shader medium float precision rangeMax:" + gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.MEDIUM_FLOAT ).rangeMax);
      result.push("webgl fragment shader low float precision:" + gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.LOW_FLOAT ).precision);
      result.push("webgl fragment shader low float precision rangeMin:" + gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.LOW_FLOAT ).rangeMin);
      result.push("webgl fragment shader low float precision rangeMax:" + gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.LOW_FLOAT ).rangeMax);
      result.push("webgl vertex shader high int precision:" + gl.getShaderPrecisionFormat(gl.VERTEX_SHADER, gl.HIGH_INT ).precision);
      result.push("webgl vertex shader high int precision rangeMin:" + gl.getShaderPrecisionFormat(gl.VERTEX_SHADER, gl.HIGH_INT ).rangeMin);
      result.push("webgl vertex shader high int precision rangeMax:" + gl.getShaderPrecisionFormat(gl.VERTEX_SHADER, gl.HIGH_INT ).rangeMax);
      result.push("webgl vertex shader medium int precision:" + gl.getShaderPrecisionFormat(gl.VERTEX_SHADER, gl.MEDIUM_INT ).precision);
      result.push("webgl vertex shader medium int precision rangeMin:" + gl.getShaderPrecisionFormat(gl.VERTEX_SHADER, gl.MEDIUM_INT ).rangeMin);
      result.push("webgl vertex shader medium int precision rangeMax:" + gl.getShaderPrecisionFormat(gl.VERTEX_SHADER, gl.MEDIUM_INT ).rangeMax);
      result.push("webgl vertex shader low int precision:" + gl.getShaderPrecisionFormat(gl.VERTEX_SHADER, gl.LOW_INT ).precision);
      result.push("webgl vertex shader low int precision rangeMin:" + gl.getShaderPrecisionFormat(gl.VERTEX_SHADER, gl.LOW_INT ).rangeMin);
      result.push("webgl vertex shader low int precision rangeMax:" + gl.getShaderPrecisionFormat(gl.VERTEX_SHADER, gl.LOW_INT ).rangeMax);
      result.push("webgl fragment shader high int precision:" + gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.HIGH_INT ).precision);
      result.push("webgl fragment shader high int precision rangeMin:" + gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.HIGH_INT ).rangeMin);
      result.push("webgl fragment shader high int precision rangeMax:" + gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.HIGH_INT ).rangeMax);
      result.push("webgl fragment shader medium int precision:" + gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.MEDIUM_INT ).precision);
      result.push("webgl fragment shader medium int precision rangeMin:" + gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.MEDIUM_INT ).rangeMin);
      result.push("webgl fragment shader medium int precision rangeMax:" + gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.MEDIUM_INT ).rangeMax);
      result.push("webgl fragment shader low int precision:" + gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.LOW_INT ).precision);
      result.push("webgl fragment shader low int precision rangeMin:" + gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.LOW_INT ).rangeMin);
      result.push("webgl fragment shader low int precision rangeMax:" + gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.LOW_INT ).rangeMax);
      return result.join("~");
    },
    getAdBlock: function(){
      var ads = document.createElement("div");
      ads.innerHTML = "&nbsp;";
      ads.className = "adsbox";
      var result = false;
      try {
        // body may not exist, that's why we need try/catch
        document.body.appendChild(ads);
        result = document.getElementsByClassName("adsbox")[0].offsetHeight === 0;
        document.body.removeChild(ads);
      } catch (e) {
        result = false;
      }
      return result;
    },
    getHasLiedLanguages: function(){
      //We check if navigator.language is equal to the first language of navigator.languages
      if(typeof navigator.languages !== "undefined"){
        try {
          var firstLanguages = navigator.languages[0].substr(0, 2);
          if(firstLanguages !== navigator.language.substr(0, 2)){
            return true;
          }
        } catch(err) {
          return true;
        }
      }
      return false;
    },
    getHasLiedResolution: function(){
      if(screen.width < screen.availWidth){
        return true;
      }
      if(screen.height < screen.availHeight){
        return true;
      }
      return false;
    },
    getHasLiedOs: function(){
      var userAgent = navigator.userAgent.toLowerCase();
      var oscpu = navigator.oscpu;
      var platform = navigator.platform.toLowerCase();
      var os;
      //We extract the OS from the user agent (respect the order of the if else if statement)
      if(userAgent.indexOf("windows phone") >= 0){
        os = "Windows Phone";
      } else if(userAgent.indexOf("win") >= 0){
        os = "Windows";
      } else if(userAgent.indexOf("android") >= 0){
        os = "Android";
      } else if(userAgent.indexOf("linux") >= 0){
        os = "Linux";
      } else if(userAgent.indexOf("iphone") >= 0 || userAgent.indexOf("ipad") >= 0 ){
        os = "iOS";
      } else if(userAgent.indexOf("mac") >= 0){
        os = "Mac";
      } else{
        os = "Other";
      }
      // We detect if the person uses a mobile device
      var mobileDevice;
      if (("ontouchstart" in window) ||
           (navigator.maxTouchPoints > 0) ||
           (navigator.msMaxTouchPoints > 0)) {
            mobileDevice = true;
      } else{
        mobileDevice = false;
      }

      if(mobileDevice && os !== "Windows Phone" && os !== "Android" && os !== "iOS" && os !== "Other"){
        return true;
      }

      // We compare oscpu with the OS extracted from the UA
      if(typeof oscpu !== "undefined"){
        oscpu = oscpu.toLowerCase();
        if(oscpu.indexOf("win") >= 0 && os !== "Windows" && os !== "Windows Phone"){
          return true;
        } else if(oscpu.indexOf("linux") >= 0 && os !== "Linux" && os !== "Android"){
          return true;
        } else if(oscpu.indexOf("mac") >= 0 && os !== "Mac" && os !== "iOS"){
          return true;
        } else if(oscpu.indexOf("win") === 0 && oscpu.indexOf("linux") === 0 && oscpu.indexOf("mac") >= 0 && os !== "other"){
          return true;
        }
      }

      //We compare platform with the OS extracted from the UA
      if(platform.indexOf("win") >= 0 && os !== "Windows" && os !== "Windows Phone"){
        return true;
      } else if((platform.indexOf("linux") >= 0 || platform.indexOf("android") >= 0 || platform.indexOf("pike") >= 0) && os !== "Linux" && os !== "Android"){
        return true;
      } else if((platform.indexOf("mac") >= 0 || platform.indexOf("ipad") >= 0 || platform.indexOf("ipod") >= 0 || platform.indexOf("iphone") >= 0) && os !== "Mac" && os !== "iOS"){
        return true;
      } else if(platform.indexOf("win") === 0 && platform.indexOf("linux") === 0 && platform.indexOf("mac") >= 0 && os !== "other"){
        return true;
      }

      if(typeof navigator.plugins === "undefined" && os !== "Windows" && os !== "Windows Phone"){
        //We are are in the case where the person uses ie, therefore we can infer that it's windows
        return true;
      }

      return false;
    },
    getHasLiedBrowser: function () {
      var userAgent = navigator.userAgent.toLowerCase();
      var productSub = navigator.productSub;

      //we extract the browser from the user agent (respect the order of the tests)
      var browser;
      if(userAgent.indexOf("firefox") >= 0){
        browser = "Firefox";
      } else if(userAgent.indexOf("opera") >= 0 || userAgent.indexOf("opr") >= 0){
        browser = "Opera";
      } else if(userAgent.indexOf("chrome") >= 0){
        browser = "Chrome";
      } else if(userAgent.indexOf("safari") >= 0){
        browser = "Safari";
      } else if(userAgent.indexOf("trident") >= 0){
        browser = "Internet Explorer";
      } else{
        browser = "Other";
      }

      if((browser === "Chrome" || browser === "Safari" || browser === "Opera") && productSub !== "20030107"){
        return true;
      }

      var tempRes = eval.toString().length;
      if(tempRes === 37 && browser !== "Safari" && browser !== "Firefox" && browser !== "Other"){
        return true;
      } else if(tempRes === 39 && browser !== "Internet Explorer" && browser !== "Other"){
        return true;
      } else if(tempRes === 33 && browser !== "Chrome" && browser !== "Opera" && browser !== "Other"){
        return true;
      }

      //We create an error to see how it is handled
      var errFirefox;
      try {
        throw "a";
      } catch(err){
        try{
          err.toSource();
          errFirefox = true;
        } catch(errOfErr){
          errFirefox = false;
        }
      }
      if(errFirefox && browser !== "Firefox" && browser !== "Other"){
        return true;
      }
      return false;
    },
    isCanvasSupported: function () {
      var elem = document.createElement("canvas");
      return !!(elem.getContext && elem.getContext("2d"));
    },
    isWebGlSupported: function() {
      // code taken from Modernizr
      if (!this.isCanvasSupported()) {
        return false;
      }

      var canvas = document.createElement("canvas"),
          glContext;

      try {
        glContext = canvas.getContext && (canvas.getContext("webgl") || canvas.getContext("experimental-webgl"));
      } catch(e) {
        glContext = false;
      }

      return !!window.WebGLRenderingContext && !!glContext;
    },
    isIE: function () {
      if(navigator.appName === "Microsoft Internet Explorer") {
        return true;
      } else if(navigator.appName === "Netscape" && /Trident/.test(navigator.userAgent)) { // IE 11
        return true;
      }
      return false;
    },
    hasSwfObjectLoaded: function(){
      return typeof window.swfobject !== "undefined";
    },
    hasMinFlashInstalled: function () {
      return swfobject.hasFlashPlayerVersion("9.0.0");
    },
    addFlashDivNode: function() {
      var node = document.createElement("div");
      node.setAttribute("id", this.options.swfContainerId);
      document.body.appendChild(node);
    },
    loadSwfAndDetectFonts: function(done) {
      var hiddenCallback = "___fp_swf_loaded";
      window[hiddenCallback] = function(fonts) {
        done(fonts);
      };
      var id = this.options.swfContainerId;
      this.addFlashDivNode();
      var flashvars = { onReady: hiddenCallback};
      var flashparams = { allowScriptAccess: "always", menu: "false" };
      swfobject.embedSWF(this.options.swfPath, id, "1", "1", "9.0.0", false, flashvars, flashparams, {});
    },
    getWebglCanvas: function() {
      var canvas = document.createElement("canvas");
      var gl = null;
      try {
        gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl");
      } catch(e) { /* squelch */ }
      if (!gl) { gl = null; }
      return gl;
    },
    each: function (obj, iterator, context) {
      if (obj === null) {
        return;
      }
      if (this.nativeForEach && obj.forEach === this.nativeForEach) {
        obj.forEach(iterator, context);
      } else if (obj.length === +obj.length) {
        for (var i = 0, l = obj.length; i < l; i++) {
          if (iterator.call(context, obj[i], i, obj) === {}) { return; }
        }
      } else {
        for (var key in obj) {
          if (obj.hasOwnProperty(key)) {
            if (iterator.call(context, obj[key], key, obj) === {}) { return; }
          }
        }
      }
    },

    map: function(obj, iterator, context) {
      var results = [];
      // Not using strict equality so that this acts as a
      // shortcut to checking for `null` and `undefined`.
      if (obj == null) { return results; }
      if (this.nativeMap && obj.map === this.nativeMap) { return obj.map(iterator, context); }
      this.each(obj, function(value, index, list) {
        results[results.length] = iterator.call(context, value, index, list);
      });
      return results;
    },

    /// MurmurHash3 related functions

    //
    // Given two 64bit ints (as an array of two 32bit ints) returns the two
    // added together as a 64bit int (as an array of two 32bit ints).
    //
    x64Add: function(m, n) {
      m = [m[0] >>> 16, m[0] & 0xffff, m[1] >>> 16, m[1] & 0xffff];
      n = [n[0] >>> 16, n[0] & 0xffff, n[1] >>> 16, n[1] & 0xffff];
      var o = [0, 0, 0, 0];
      o[3] += m[3] + n[3];
      o[2] += o[3] >>> 16;
      o[3] &= 0xffff;
      o[2] += m[2] + n[2];
      o[1] += o[2] >>> 16;
      o[2] &= 0xffff;
      o[1] += m[1] + n[1];
      o[0] += o[1] >>> 16;
      o[1] &= 0xffff;
      o[0] += m[0] + n[0];
      o[0] &= 0xffff;
      return [(o[0] << 16) | o[1], (o[2] << 16) | o[3]];
    },

    //
    // Given two 64bit ints (as an array of two 32bit ints) returns the two
    // multiplied together as a 64bit int (as an array of two 32bit ints).
    //
    x64Multiply: function(m, n) {
      m = [m[0] >>> 16, m[0] & 0xffff, m[1] >>> 16, m[1] & 0xffff];
      n = [n[0] >>> 16, n[0] & 0xffff, n[1] >>> 16, n[1] & 0xffff];
      var o = [0, 0, 0, 0];
      o[3] += m[3] * n[3];
      o[2] += o[3] >>> 16;
      o[3] &= 0xffff;
      o[2] += m[2] * n[3];
      o[1] += o[2] >>> 16;
      o[2] &= 0xffff;
      o[2] += m[3] * n[2];
      o[1] += o[2] >>> 16;
      o[2] &= 0xffff;
      o[1] += m[1] * n[3];
      o[0] += o[1] >>> 16;
      o[1] &= 0xffff;
      o[1] += m[2] * n[2];
      o[0] += o[1] >>> 16;
      o[1] &= 0xffff;
      o[1] += m[3] * n[1];
      o[0] += o[1] >>> 16;
      o[1] &= 0xffff;
      o[0] += (m[0] * n[3]) + (m[1] * n[2]) + (m[2] * n[1]) + (m[3] * n[0]);
      o[0] &= 0xffff;
      return [(o[0] << 16) | o[1], (o[2] << 16) | o[3]];
    },
    //
    // Given a 64bit int (as an array of two 32bit ints) and an int
    // representing a number of bit positions, returns the 64bit int (as an
    // array of two 32bit ints) rotated left by that number of positions.
    //
    x64Rotl: function(m, n) {
      n %= 64;
      if (n === 32) {
        return [m[1], m[0]];
      }
      else if (n < 32) {
        return [(m[0] << n) | (m[1] >>> (32 - n)), (m[1] << n) | (m[0] >>> (32 - n))];
      }
      else {
        n -= 32;
        return [(m[1] << n) | (m[0] >>> (32 - n)), (m[0] << n) | (m[1] >>> (32 - n))];
      }
    },
    //
    // Given a 64bit int (as an array of two 32bit ints) and an int
    // representing a number of bit positions, returns the 64bit int (as an
    // array of two 32bit ints) shifted left by that number of positions.
    //
    x64LeftShift: function(m, n) {
      n %= 64;
      if (n === 0) {
        return m;
      }
      else if (n < 32) {
        return [(m[0] << n) | (m[1] >>> (32 - n)), m[1] << n];
      }
      else {
        return [m[1] << (n - 32), 0];
      }
    },
    //
    // Given two 64bit ints (as an array of two 32bit ints) returns the two
    // xored together as a 64bit int (as an array of two 32bit ints).
    //
    x64Xor: function(m, n) {
      return [m[0] ^ n[0], m[1] ^ n[1]];
    },
    //
    // Given a block, returns murmurHash3's final x64 mix of that block.
    // (`[0, h[0] >>> 1]` is a 33 bit unsigned right shift. This is the
    // only place where we need to right shift 64bit ints.)
    //
    x64Fmix: function(h) {
      h = this.x64Xor(h, [0, h[0] >>> 1]);
      h = this.x64Multiply(h, [0xff51afd7, 0xed558ccd]);
      h = this.x64Xor(h, [0, h[0] >>> 1]);
      h = this.x64Multiply(h, [0xc4ceb9fe, 0x1a85ec53]);
      h = this.x64Xor(h, [0, h[0] >>> 1]);
      return h;
    },

    //
    // Given a string and an optional seed as an int, returns a 128 bit
    // hash using the x64 flavor of MurmurHash3, as an unsigned hex.
    //
    x64hash128: function (key, seed) {
      key = key || "";
      seed = seed || 0;
      var remainder = key.length % 16;
      var bytes = key.length - remainder;
      var h1 = [0, seed];
      var h2 = [0, seed];
      var k1 = [0, 0];
      var k2 = [0, 0];
      var c1 = [0x87c37b91, 0x114253d5];
      var c2 = [0x4cf5ad43, 0x2745937f];
      for (var i = 0; i < bytes; i = i + 16) {
        k1 = [((key.charCodeAt(i + 4) & 0xff)) | ((key.charCodeAt(i + 5) & 0xff) << 8) | ((key.charCodeAt(i + 6) & 0xff) << 16) | ((key.charCodeAt(i + 7) & 0xff) << 24), ((key.charCodeAt(i) & 0xff)) | ((key.charCodeAt(i + 1) & 0xff) << 8) | ((key.charCodeAt(i + 2) & 0xff) << 16) | ((key.charCodeAt(i + 3) & 0xff) << 24)];
        k2 = [((key.charCodeAt(i + 12) & 0xff)) | ((key.charCodeAt(i + 13) & 0xff) << 8) | ((key.charCodeAt(i + 14) & 0xff) << 16) | ((key.charCodeAt(i + 15) & 0xff) << 24), ((key.charCodeAt(i + 8) & 0xff)) | ((key.charCodeAt(i + 9) & 0xff) << 8) | ((key.charCodeAt(i + 10) & 0xff) << 16) | ((key.charCodeAt(i + 11) & 0xff) << 24)];
        k1 = this.x64Multiply(k1, c1);
        k1 = this.x64Rotl(k1, 31);
        k1 = this.x64Multiply(k1, c2);
        h1 = this.x64Xor(h1, k1);
        h1 = this.x64Rotl(h1, 27);
        h1 = this.x64Add(h1, h2);
        h1 = this.x64Add(this.x64Multiply(h1, [0, 5]), [0, 0x52dce729]);
        k2 = this.x64Multiply(k2, c2);
        k2 = this.x64Rotl(k2, 33);
        k2 = this.x64Multiply(k2, c1);
        h2 = this.x64Xor(h2, k2);
        h2 = this.x64Rotl(h2, 31);
        h2 = this.x64Add(h2, h1);
        h2 = this.x64Add(this.x64Multiply(h2, [0, 5]), [0, 0x38495ab5]);
      }
      k1 = [0, 0];
      k2 = [0, 0];
      switch(remainder) {
        case 15:
          k2 = this.x64Xor(k2, this.x64LeftShift([0, key.charCodeAt(i + 14)], 48));
        case 14:
          k2 = this.x64Xor(k2, this.x64LeftShift([0, key.charCodeAt(i + 13)], 40));
        case 13:
          k2 = this.x64Xor(k2, this.x64LeftShift([0, key.charCodeAt(i + 12)], 32));
        case 12:
          k2 = this.x64Xor(k2, this.x64LeftShift([0, key.charCodeAt(i + 11)], 24));
        case 11:
          k2 = this.x64Xor(k2, this.x64LeftShift([0, key.charCodeAt(i + 10)], 16));
        case 10:
          k2 = this.x64Xor(k2, this.x64LeftShift([0, key.charCodeAt(i + 9)], 8));
        case 9:
          k2 = this.x64Xor(k2, [0, key.charCodeAt(i + 8)]);
          k2 = this.x64Multiply(k2, c2);
          k2 = this.x64Rotl(k2, 33);
          k2 = this.x64Multiply(k2, c1);
          h2 = this.x64Xor(h2, k2);
        case 8:
          k1 = this.x64Xor(k1, this.x64LeftShift([0, key.charCodeAt(i + 7)], 56));
        case 7:
          k1 = this.x64Xor(k1, this.x64LeftShift([0, key.charCodeAt(i + 6)], 48));
        case 6:
          k1 = this.x64Xor(k1, this.x64LeftShift([0, key.charCodeAt(i + 5)], 40));
        case 5:
          k1 = this.x64Xor(k1, this.x64LeftShift([0, key.charCodeAt(i + 4)], 32));
        case 4:
          k1 = this.x64Xor(k1, this.x64LeftShift([0, key.charCodeAt(i + 3)], 24));
        case 3:
          k1 = this.x64Xor(k1, this.x64LeftShift([0, key.charCodeAt(i + 2)], 16));
        case 2:
          k1 = this.x64Xor(k1, this.x64LeftShift([0, key.charCodeAt(i + 1)], 8));
        case 1:
          k1 = this.x64Xor(k1, [0, key.charCodeAt(i)]);
          k1 = this.x64Multiply(k1, c1);
          k1 = this.x64Rotl(k1, 31);
          k1 = this.x64Multiply(k1, c2);
          h1 = this.x64Xor(h1, k1);
      }
      h1 = this.x64Xor(h1, [0, key.length]);
      h2 = this.x64Xor(h2, [0, key.length]);
      h1 = this.x64Add(h1, h2);
      h2 = this.x64Add(h2, h1);
      h1 = this.x64Fmix(h1);
      h2 = this.x64Fmix(h2);
      h1 = this.x64Add(h1, h2);
      h2 = this.x64Add(h2, h1);
      return ("00000000" + (h1[0] >>> 0).toString(16)).slice(-8) + ("00000000" + (h1[1] >>> 0).toString(16)).slice(-8) + ("00000000" + (h2[0] >>> 0).toString(16)).slice(-8) + ("00000000" + (h2[1] >>> 0).toString(16)).slice(-8);
    }
  };
  Fingerprint2.VERSION = "1.5.1";
  return Fingerprint2;
});


/***/ }),

/***/ "./modules/browser_fingerprint/index.js":
/*!**********************************************!*\
  !*** ./modules/browser_fingerprint/index.js ***!
  \**********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 浏览器指纹
 */

var fingerprint = __webpack_require__(/*! ./fingerprint2 */ "./modules/browser_fingerprint/fingerprint2.js");
var bid = __webpack_require__(/*! ../bid */ "./modules/bid/index.js");
var save = __webpack_require__(/*! ./save */ "./modules/browser_fingerprint/save.js");

/**
 * 是否支持canvas
 * 
 * @returns 
 */
function isSupportCanvas(){
  var elem = document.createElement('canvas');
  return !!(elem.getContext && elem.getContext('2d'));
}

module.exports = {
  get: function(callback){
    if (isSupportCanvas()) {
      new fingerprint({
        dontUseFakeFontInCanvas: true,
         swfContainerId : true,
         swfPath : true,
        // userDefinedFonts : true,
         excludeUserAgent : true,
        // excludeLanguage : true,
        // excludeColorDepth : true,
        excludeScreenResolution : true,
        excludeAvailableScreenResolution: true,
        // excludeTimezoneOffset : true,
        // excludeSessionStorage : true,
        // excludeIndexedDB : true,
        // excludeAddBehavior : true,
        // excludeOpenDatabase : true,
        // excludeCpuClass : true,
        // excludePlatform : true,
        // excludeDoNotTrack : true,
        // excludeCanvas : true,
        // excludeWebGL : true,
         excludeAdBlock : true,
        // excludeHasLiedLanguages : true,
        // excludeHasLiedResolution : true,
        // excludeHasLiedOs : true,
        // excludeHasLiedBrowser : true,
        // excludeJsFonts : true,
         excludeFlashFonts : true,
         excludePlugins : true,
         excludeIEPlugins : true
        // excludeTouchSupport : true,
        // excludePixelRatio : true,
        // excludeHardwareConcurrency : true,
      }).get(function(result, components){
        save(result);
        callback(result, components);
        return;
      });
    }
    else{
      callback(bid.init());
      return;
    }
  }
}

/***/ }),

/***/ "./modules/browser_fingerprint/save.js":
/*!*********************************************!*\
  !*** ./modules/browser_fingerprint/save.js ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 保存浏览器指纹
 */

var cookie = __webpack_require__(/*! ../cookie */ "./modules/cookie/index.js");

module.exports = function(fingerprint){
  if (fingerprint) {
    cookie.set('qgqp_b_id', fingerprint, 10000, '.eastmoney.com');
  }
}

/***/ }),

/***/ "./modules/cookie/index.js":
/*!*********************************!*\
  !*** ./modules/cookie/index.js ***!
  \*********************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * cookie
 */

var cookie = {
	get: function (name) {
		var xarr = document.cookie.match(new RegExp("(^| )" + name + "=([^;]*)(;|$)"));
		if (xarr != null)
			return decodeURIComponent(xarr[2]);
		return null;
	},
	set: function(key,value,expiredays,domain){
		var cookiestr = key + "=" + escape(value)

		if (expiredays != undefined) {
			var exdate = new Date();
			exdate.setDate(exdate.getDate() + expiredays);	
			cookiestr += ";expires=" + exdate.toGMTString()
		}
		if (domain != undefined) {
			cookiestr += ";domain=" + domain
		}
		cookiestr += ';path=/'
		document.cookie = cookiestr

	},
	del: function (key, domain) {
		var exdate = new Date((new Date).getTime() - 1);
		if (domain) {
			document.cookie = key + '=;path=/;expires=' + exdate.toGMTString() + ';domain=' + domain;
		}
		else{
			document.cookie = key + '=;path=/;expires=' + exdate.toGMTString();
		}
		
	}
};

module.exports = cookie;

/***/ }),

/***/ "./modules/datacache/index.js":
/*!************************************!*\
  !*** ./modules/datacache/index.js ***!
  \************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * 数据缓存
 */

module.exports = {
  /**
   * 当前组合id
   */
  thisgroupid: null,

  //thisgroupname: null,
  /**
   * 组合信息
   */
  groupdata: null,

  /**
   * 更改组合
   */
  changeGroup: null,
  /**
   * 当前自选股
   */
  stocks: null,
  /**
   * 当前显示类型
   */
  thisshowtype: null,
  /**
   * 更改显示类型
   */
  changeShowType: null,
  /**
   * 股票类型
   */
  stocktype: null,
  /**
   * 笔记数据
   */
  notedata: null,
  /**
   * 盈利预测数据
   */
  ylycdata: null,
  /**
   * 盈利预测基准年
   */
  ylyc_year: null,
  /**
   * 排序类型
   */
  pxtype: null,

  /**
   * 排序规则 正序 倒序
   */
  pxorder: null,
  /**
   * 禁止排序
   */
  forbid_sort: false,
  /**
   * 默认组合id
   */
  firstgroupid: null,
  /**
   * 置顶组合id
   */
  topgroupid: null,
  /**
   * 置顶的自选股列表
   */
  top_stocks: null,
  /**
   * 当前是否是默认分组
   */
  is_defaultgroup: null,
  /**
   * 刷新时间
   */
  refreshtime: 2000,
  /**
   * 是否是海外用户
   */
  ishaiwai: false
}

/***/ }),

/***/ "./modules/datadiff/index.js":
/*!***********************************!*\
  !*** ./modules/datadiff/index.js ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * 全量数据差异
 * 
 */

module.exports = function(d1, d2){
  var diff = []
  Object.keys(d2).forEach(function(v){
    var d2item = d2[v]
    var d1item = d1[v]
    var diffitem = {
      index: v,
      code: d1item.f13 + '.' + d1item.f12,
      change: false,
      fullchange: false,
      changedata: {}
    }
    if (d2item.f12 != d1item.f12 || d2item.f13 != d1item.f13) {
      diffitem.change = true
      diffitem.fullchange = true
      diffitem.changedata = d2item
      diff.push(diffitem)
      return false
    }
    Object.keys(d2item).forEach(function(iv){
      if(d2item[iv] != d1item[iv]){
        diffitem.changedata[iv] = d2item[iv]
        diffitem.change = true
      }
    })
    diff.push(diffitem)
  })
  return diff
}

/***/ }),

/***/ "./modules/datetime/index.js":
/*!***********************************!*\
  !*** ./modules/datetime/index.js ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 时间相关
 */

var dateformat = __webpack_require__(/*! dateformat */ "./node_modules/dateformat/lib/dateformat.js")

var datetime = {
  dcdatestr: 'yyyy-MM-dd hh:mm:ss', //东财时间格式
  /**
   * 东财格式时间转换成时间
   * @param {*} datestr 
   */
  strToDate: function(datestr){
    //console.info(datestr)
    datestr = datestr.replace(/-/ig, '/')
    datestr = datestr.replace(/T/ig, ' ')
    //console.info(datestr)
    return new Date(datestr.substring(0, 19))
  },
  /**
   * 如果是今天就显示时间，不是则显示日期
   * @param {*} datestr 
   */
  strToDayOrTime: function(datestr){
    //console.info(datestr)
    var time = datetime.strToDate(datestr)
    //console.info(time)
    var thistime = new Date()
    if (time.getFullYear() == thistime.getFullYear() && time.getMonth() == thistime.getMonth() && time.getDate() == thistime.getDate()) {
      return dateformat(time, 'HH:MM')
    }
    else{
      return dateformat(time, 'mm-dd')
    }
  }
}

module.exports = datetime

/***/ }),

/***/ "./modules/dom/index.js":
/*!******************************!*\
  !*** ./modules/dom/index.js ***!
  \******************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * dom相关方法
 */

module.exports = {
  /**
   * 光标移动到输入框最后面
   * @param {*} obj 
   */
  cursorMoveEnd: function (obj) {
    obj.focus();
    var len = obj.value.length;
    if (document.selection) {
      var sel = obj.createTextRange();
      sel.moveStart('character', len);
      sel.collapse();
      sel.select();
    } else if (typeof obj.selectionStart == 'number' && typeof obj.selectionEnd == 'number') {
      obj.selectionStart = obj.selectionEnd = len;
    }
  }
}

/***/ }),

/***/ "./modules/global_event/index.js":
/*!***************************************!*\
  !*** ./modules/global_event/index.js ***!
  \***************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * 全局事件
 */

module.exports = {
  eventpool: {},
  /**
   * 注册新事件
   * @param {*} event_name 
   * @param {*} callback 
   */
  regEvent: function(event_name, callback){
    if (!this.eventpool.event_name) {
      this.eventpool.event_name = []
    }

    this.eventpool.event_name.push(callback)

  },
  /**
   * 删除事件
   * @param {*} event_name 
   * @param {*} callback 
   */
  delEvent: function(event_name, callback){
    try{
      this.eventpool.event_name = this.eventpool.event_name.filter(function(v){
        return v != callback
      })
    }
    catch(error){
    }
  },
  /**
   * 触发事件
   * @param {*} event_name 
   */
  trigger: function(event_name, data){
    try{
      this.eventpool.event_name.forEach(function(v){
        v(data)
      })
    }
    catch(error){
    }
  }
}

/***/ }),

/***/ "./modules/guba/web.js":
/*!*****************************!*\
  !*** ./modules/guba/web.js ***!
  \*****************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {


var codes = ''

// var isbind = false

var global_event = __webpack_require__(/*! ../global_event */ "./modules/global_event/index.js")
var datetime = __webpack_require__(/*! ../datetime */ "./modules/datetime/index.js")
var debounce = __webpack_require__(/*! lodash/debounce */ "./node_modules/lodash/debounce.js")
var gubanews = $('#gubanews')
var localstorage = __webpack_require__(/*! ../localstorage */ "./modules/localstorage/index.js")

var guba;

guba = {
  thistype: 'normal',
  thisindex: 1,
  allowload: true,
  init: function(stocks){
    this.bind()
    global_event.regEvent('stockchange', function(stocks){
      guba.changeStocks(stocks)
      guba.get(1)
    })
  },
  changeStocks: function(stocks){
    codes = this.dealstocks(stocks)
  },
  getLocalData: function(){
    var _this = this
    if (localstorage.get('gubatype')) {
      if (localstorage.get('gubatype') == 'time') {
        _this.thistype = 'normal'
        // _this.thisindex = 1
        // _this.get(1)
      }
      else if(localstorage.get('gubatype') == 'hot'){
        _this.thistype = 'hot'
        // _this.thisindex = 1
        // _this.get(1)
      }      
    }
  },
  data: null,
  /**
   * 去重
   * @param {*} list 
   */
  removeSame: function(list){
    var temp = {}
    list.forEach(function(v){
      temp[v.id] = v
    })
    return Object.keys(temp).reverse().map(function(v){
      return temp[v]
    })
  },

  removeSame2: function(list1, list2){
    var temp1 = {}
    list1.forEach(function(v){
      temp1[v.id] = v
    })
    var temp2 = {}
    list2.forEach(function(v){
      if(temp1[v.id] == undefined){
        temp2[v.id] = v
      }
    })
    return Object.keys(temp2).map(function(v){
      return temp2[v]
    })
  },
  dealstocks: function(stocks){
    var codes = []
    stocks.forEach(function(v){
      if (v.indexOf('0.') == 0 || v.indexOf('1.') == 0) {
        codes.push(v.substring(2))
      }
      else if (v.indexOf('105.') == 0 || v.indexOf('106.') == 0 || v.indexOf('107.') == 0) {
        codes.push('us' + v.substring(4))
      }
      else if (v.indexOf('116.') == 0) {
        codes.push('hk' + v.substring(4))
      }

    })
    return codes.join(',').toLocaleLowerCase()
  },
  bind: function(){
    isbind = true
    var _this = this
    $('#chooseguba').on('click', 'a', function(){
      var type = $(this).data('type')
      localstorage.set('gubatype', type)
      if (type == 'time') {
        _this.thistype = 'normal'
        _this.thisindex = 1
        _this.get(1)
      }
      else if(type == 'hot'){
        _this.thistype = 'hot'
        _this.thisindex = 1
        _this.get(1)
      }
    })

    $('#refreshguba').click(function(){
      $('#refreshguba .refreshgubat').text('加载中...')
      _this.get(1).then(function(){
        $('#refreshguba .refreshgubat').text('刷新')
      })
      return false
    })
    setInterval(function(){
      // if (_this.thistype == 'hot') {
      //   _this.getHot(1)
      // }
      // else if(_this.thistype == 'normal'){
      //   _this.getNormal(1)
      // }

      _this.get(1)
    }, 60 * 1000);
    gubanews.on('scroll', debounce(function(){
      if ( (gubanews.scrollTop() + gubanews.height()) >= gubanews.get(0).scrollHeight ) {
       
        //more.click(function(){
          _this.loadMore()
        //})
      }
    }, 100))
  },
  loadMore: function(){
    if (!this.allowload) {
      return false
    }
    this.allowload = false

    if(this.thisindex == 1){
      this.thisindex = 3
    }
    else{
      this.thisindex ++
    }
    
    // console.info(this.thisindex)
    if (this.thisindex > 5) {

      return false
    }
     //var more = $('<li class="gubamoreli">加载中...</li>')
     
       // gubanews.append(more)
    // if (this.thistype == 'hot') {
      
    // }
    this.get(this.thisindex)
  },
  // makeHTML: function (data){
  //   var html = []
  //   if (data.length == 0) {
  //     $('#gubanews').html('<div class="infonod">暂无相关内容</div>')
  //     return false
  //   }
  //   data.forEach(function(v){
  //     var icon = ''
  //     if (v.market == 106) {
  //       icon = '<span class="hkstock">HK</span>'
  //     }
  //     else if (v.market == 103 || v.market == 104 || v.market == 105){
  //       icon = '<span class="usstock">US</span>'
  //     }
  //     html.push('<li><a href="http://guba.eastmoney.com/list,' + v.code + '.html">[' + v.name + ']</a> ' + icon + ' <a href="http://guba.eastmoney.com/news,' + v.code + ',' + v.id + '.html">' + v.title + '</a><span class="time">' +  datetime.strToDayOrTime(v.time) + '</span></li>')
  //   })
    
  //   $('#gubanews').html(html.join(''))
  // },
  makeHTML: function (data){
    if (data.length == 0) {
      return '<div class="infonod">暂无相关内容</div>' //<div class="infonod">暂无相关内容1</div>
    }

    var html = []
    data.forEach(function(v){
      var icon = ''
      if (v.market == 106) {
        icon = '<span class="hkstock">HK</span>'
      }
      else if (v.market == 103 || v.market == 104 || v.market == 105){
        icon = '<span class="usstock">US</span>'
      }
      else if (v.market == 155 || v.market == 156) {//英股
        icon == '<span class="ukstock">UK</span>'
      }
      html.push('<li>[<a href="http://guba.eastmoney.com/list,' + v.code + '.html">' + v.name + '</a>] ' + icon + ' <a href="http://guba.eastmoney.com/news,' + v.code + ',' + v.id + '.html" title="' + v.title + '">' + v.title + '</a><span class="time">' +  datetime.strToDayOrTime(v.time) + '</span></li>')
    })
    
    return html.join('')
  },  
  get: function(pageindex){
    this.getLocalData()
    this.thisindex = pageindex
    var _this = this
    if (codes == '') {
      gubanews.html('<div class="infonod">暂无相关内容</div>')
      $('#chooseguba a').removeClass('on')
      $('#chooseguba a:last').addClass('on')
      return false
    }
    $('.infonod', gubanews).remove()
    gubanews.append('<li class="gubamoreli">加载中...</li>')

    var pagesize = 10
    var pageindex_true = pageindex
    if (pageindex_true == 1) {
      pagesize = 20
    }
    else{
      //pageindex_true ++
      pagesize = 10
    }

    var url = './api/guba/hotarticle'
    if (this.thistype == 'normal') {
      url = './api/guba/article'
    }

    return $.ajax({
      url: url,
      type: 'GET',
      dataType: 'json',
      data: {
        codes: codes,
        pageindex: pageindex_true,
        pagesize: pagesize
      }
    })
    .done(function(json) {   
      if (json.re) {
        //console.info(_this.thisindex)
        json.result = _this.removeSame(json.result)
        if (_this.thisindex == 1) {
          gubanews.html(_this.makeHTML(json.result))
          _this.data = json.result
          this.data = json.result
        }
        else{
          json.result = _this.removeSame2(_this.data, json.result)
          _this.data = _this.data.concat(json.result)
          gubanews.append(_this.makeHTML(json.result))

        }
        if (pageindex == 1) {
          gubanews.scrollTop(0)
        }
        $('.chooseguba').removeClass('on')
        if(_this.thistype == 'hot'){
          $('.chooseguba:last').addClass('on')
        }
        else{
          $('.chooseguba:first').addClass('on')
        }
        
      }
    })
    .fail(function(error) {
      
    }) 
    .always(function(){
      $('.gubamoreli', gubanews).remove()
      _this.allowload = true
    })

  },
  getHot: function (pageindex){
    this.thistype = 'hot'
    this.thisindex = pageindex
    var _this = this

    if (codes == '') {
      _this.makeHTML([])
      $('#chooseguba a').removeClass('on')
      $('#chooseguba a:last').addClass('on')
      return false
    }

    var pagesize = 10
    if (pageindex == 1) {
      pagesize = 20
    }
    else{
      pageindex ++
      pagesize = 10
    }
    $.ajax({
      url: './api/guba/hotarticle',
      type: 'GET',
      dataType: 'json',
      data: {
        codes: codes,
        pageindex: pageindex,
        pagesize: pagesize
      }
    })
    .done(function(json) {   
      if (json.re) {
        _this.makeHTML(json.result)
        $('#chooseguba a').removeClass('on')
        $('#chooseguba a:last').addClass('on')
      }
    })
    .fail(function(error) {
      
    })    
  },
  getNormal: function (pageindex) {
    this.thistype = 'normal'
    this.thisindex = pageindex
    var _this = this

    if (codes == '') {
      _this.makeHTML([])
      $('#chooseguba a').removeClass('on')
      $('#chooseguba a:first').addClass('on')
      return false
    }

    var pagesize = 10
    if (pageindex == 1) {
      pagesize = 20
    }
    else{
      pageindex ++
      pagesize = 10
    }
    $.ajax({
      url: './api/guba/article',
      type: 'GET',
      dataType: 'json',
      data: {
        codes: codes,
        pageindex: pageindex,
        pagesize: pagesize
      }
    })
    .done(function(json) {   
      if (json.re) {
        _this.makeHTML(json.result)
        $('#chooseguba a').removeClass('on')
        $('#chooseguba a:first').addClass('on')
      }
    })
    .fail(function(error) {
      
    })    
  }
  // ,
  // changeCode: function(codes){
  //   codes = codes
  //   console.info(111)
  //   this.get(1)
  // }

}



// module.exports = function(stocks){
//   //guba.init(stocks)
//   //return guba
// }

module.exports = guba

/***/ }),

/***/ "./modules/guide/guide.html":
/*!**********************************!*\
  !*** ./modules/guide/guide.html ***!
  \**********************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"mguide\">\r\n  <div class=\"mguideclose\"><img src=\"./images/guide2/close.png\" alt=\"\"></div>\r\n  <div class=\"mguidep\" id=\"mguidep1\"><img src=\"./images/guide2/p1.png\" alt=\"\"></div>\r\n  <div class=\"mguidep\" id=\"mguidep2\"><img src=\"./images/guide2/p2.png\" alt=\"\"></div>\r\n  <div class=\"mguidep\" id=\"mguidep3\"><img src=\"./images/guide2/p3.png\" alt=\"\"></div>\r\n  <div class=\"mguidep\" id=\"mguidep4\"><img src=\"./images/guide2/p4.png\" alt=\"\"></div>\r\n  <div class=\"mguidep\" id=\"mguidep5\"><img src=\"./images/guide2/p5.png\" alt=\"\"></div>\r\n</div>"

/***/ }),

/***/ "./modules/guide/index.js":
/*!********************************!*\
  !*** ./modules/guide/index.js ***!
  \********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 用户引导
 */

var guide_html = __webpack_require__(/*! ./guide.html */ "./modules/guide/guide.html")

module.exports = {
  init: function(){
    if (window.localStorage && (new Date().getTime()) < 1556668800000) {
      //this.show()
      //return false
      if (localStorage.getItem('showguide2')) {
        
      }
      else{
        localStorage.setItem('showguide2', '1')
        this.show()
        return false
      }  
    }  
  },
  show: function(){
    var _this = this
    var html = this.html = $(guide_html)
    var p1 = $('#mguidep1 img', html)
    $('body').append(html)
    p1.on('load', function(){
      _this.cdStart()
    })

    $('.mguideclose', html).click(function(){
      _this.html.remove()
      try{
        clearInterval(_this.cd)
      }
      catch(error){
      }
      return false
    })
  },
  thisindex: 0,
  cdStart: function(){
    var _this = this
    this.cd = setInterval(function(){
      _this.thisindex++
      if (_this.thisindex == 5) {
        _this.html.remove()
        clearInterval(_this.cd)
        return false
      }
      $('.mguidep', _this.html).hide()
      $('.mguidep', _this.html).eq(_this.thisindex).show()
    }, 5000);
  }
}

/***/ }),

/***/ "./modules/hegui/index.js":
/*!********************************!*\
  !*** ./modules/hegui/index.js ***!
  \********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 港股合规问题
 */
var cookie = __webpack_require__(/*! ../cookie */ "./modules/cookie/index.js")
var modal_alert = __webpack_require__(/*! ../modal/alert */ "./modules/modal/alert.js")
var datacache = __webpack_require__(/*! ../datacache */ "./modules/datacache/index.js")
var user = __webpack_require__(/*! ../user */ "./modules/user/index.js")

//是否登录用户
var islogin = user.get() != null ? true : false

module.exports = {
  /**
   * 判断是否是海外用户
   * cookie保存最新结果，1天
   */
  isOutside: function(){
    return new Promise(function(resolve, reject){
      var isoutside_cookie = cookie.get('isoutside')
      if ( isoutside_cookie != null) {
        if (isoutside_cookie == '1') {
          datacache.ishaiwai = true
          resolve(true)
        }
        else{
          datacache.ishaiwai = false
          resolve(false)
        }
      }
      else{
        $.ajax({
          url: '//push2.eastmoney.com/api/qt/stock/get?cb=?',
          type: 'GET',
          dataType: 'jsonp'
        })
        .then(function(json) {   
          // console.info(json)
          if (json.lt && json.lt == 2) {
            cookie.set('isoutside', '1', 1)
            datacache.ishaiwai = true
            resolve(true)
          }
          else{
            cookie.set('isoutside', '0', 1)
            datacache.ishaiwai = false
            resolve(false)
          }
        })        
      }
    })
  },
  /**
   * 外海合规弹窗
   */
  outsiderAlert: function(){
    if (cookie.get('outsideralert') == null) {
      cookie.set('outsideralert', '1')
      modal_alert('<div style="width:400px">应港交所要求，港股Level2行情仅对大陆地区登录用户限时开放，大陆地区以外用户只可免费访问港股的BMP行情，您的港股自选股行情已做延时15分钟处理。给您带来的不便敬请谅解。</div>')
    }
  },
  /**
   * 处理港股代码 替换成延迟行情代码
   */
  dealHKStock: function(stocks){
    if (stocks instanceof Array) {
      return stocks.map(function(v){
        return v.replace('116.', '128.')
      })
    }
    if (typeof stocks == "string") {
      return stocks.replace(/116\./g, '128.')
    }
    return stocks
  },
  /**
   * 是否需要港股延迟数据
   */
  isHKDelay: function(){
    if (datacache.ishaiwai) {
      return 1
    }
    if (!islogin) {
      return 2
    }
    return 0
  }
}

/***/ }),

/***/ "./modules/importcookie/index.js":
/*!***************************************!*\
  !*** ./modules/importcookie/index.js ***!
  \***************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 导入cookie中的自选股
 */
var cookie = __webpack_require__(/*! ../cookie */ "./modules/cookie/index.js")
var modal_alert = __webpack_require__(/*! ../modal/alert */ "./modules/modal/alert.js")
var modal_confirm = __webpack_require__(/*! ../modal/confirm */ "./modules/modal/confirm.js")
var datacache = __webpack_require__(/*! ../datacache */ "./modules/datacache/index.js")

module.exports = {
  getzxg: function(){
    var zxg = cookie.get('emhq_stock')
    if (zxg != null && zxg != '') {
      return decodeURIComponent(zxg).split(',')
    }
    else{
      return []
    }
  },
  /**
   * 分析即将导入的自选股
   */
  fxzxg: function(zxglist, groupname){
    var nowzxglist = datacache.stocks
    var importzxglist = this.dealstocks(zxglist)
    var nowob = {}
    nowzxglist.forEach(function(v){
      nowob[v] = 1
    })
    var newlength = 0
    importzxglist.forEach(function(v){
      if (nowob[v] == undefined) {
        newlength++
      }
    })

    if (newlength == 0) {
      return {
        re: false,
        message: '您暂无新的自选股可导入'
      }
    }

    if (nowzxglist.length > 500) {
      return {
        re: false,
        message: '您的[' + groupname + ']分组中自选股数量已达到500条上限'
      }
    }        

    if (nowzxglist.length + newlength > 500) {
      return {
        re: false,
        message: '您的[' + groupname + ']分组中自选股数量即将超过500条上限'
      }
    }    

    return {
      re: true,
      newlength: newlength
    }
  },
  importzxg: function(){
    var _this = this
    var zxg = this.getzxg()

    if (zxg.length == 0) {
      modal_alert('导入失败！', '您暂无新的自选股可导入')
      return false
    }

    var nowgroup = $('#zxggrouplist li.on')
    var groupid = nowgroup.data('groupid')
    var groupname = nowgroup.data('groupname')

    var fxresult = this.fxzxg(zxg, groupname)
    
    if (!fxresult.re) {
      modal_alert('导入失败！', fxresult.message)
      return false
    }

    modal_confirm('', '是否将您本地的' + fxresult.newlength + '支自选股<br>导入[' + groupname + ']分组中', function(){
      _this.pladdzxg(zxg, groupname)
    })

  },
  drzxg: function(){
    var zxg = this.getzxg()

  },
  /**
   * 批量添加自选股
   */
  pladdzxg: function(stocks, groupname){
    stocks = this.dealstocks(stocks)
    $.ajax({
      url: './api/zxg/addlotstock',
      type: 'POST',
      dataType: 'json',
      data: {
        groupid: datacache.thisgroupid,
        stockcode:  stocks.join(',')
      }
    })
    .done(function(json) {   
      if (json.re) {
        modal_alert('导入成功！', '您已成功将' + stocks.length + '条自选股导入[' + groupname + ']分组中', function(){
          datacache.changeGroup(datacache.thisgroupid)
        })
      }
      else{
        modalalert(json.message)
      }
      //console.info(json)
    })
    .fail(function(error) {
      
    })
  },
  dealstocks: function(stocks){
    var back = []
    stocks.forEach(function(v){
      var first = v.substring(0,1)
      if ( first == '6') {
        back.push('1.' + v)
      }
      else if(first == '3' || first == '0')(
        back.push('0.' + v)
      )
    })
    return back
  },
  bind: function(btn){
    var _this = this
    btn.on('click', function(){
      _this.importzxg()
      return false
    })
  }
}

/***/ }),

/***/ "./modules/info/web.js":
/*!*****************************!*\
  !*** ./modules/info/web.js ***!
  \*****************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 信息流
 */

var global_event = __webpack_require__(/*! ../global_event */ "./modules/global_event/index.js")
var boxsize = __webpack_require__(/*! ../boxsize */ "./modules/boxsize/index.js")
var sessionstorage = __webpack_require__(/*! ../sessionstorage */ "./modules/sessionstorage/index.js")
var localstorage = __webpack_require__(/*! ../localstorage */ "./modules/localstorage/index.js")

var info_web = {
  codes: null,
  isbind: false,
  thisindex : 0,
  init: function(codes){
    this.codes = codes.join(',')

    //this.getMix()
    $('#newstypetab li').removeClass('on')
    $('#newstypetab li:first').addClass('on')
    if (sessionstorage.get('newstype')) {
      if(sessionstorage.get('newstype') !=  5){ //如果不是问答
        this.changeType(parseInt(sessionstorage.get('newstype')))
      }
      else{
        this.changeType(0)
      }
    }
    else{
      this.changeType(0)
    }
    
    if(!this.isbind){
      this.bind()
    }
  },
  bind: function(){
    var _this = this
    this.isbind = true
    $('#newstypetab').on('click', 'li', function(){
      
      
      var index = $(this).index()
      _this.changeType(index)
      sessionstorage.save('newstype', index)
    })

    $('#newsnumsc').on('click', 'a', function(){
      var level = $(this).data('level')
      localstorage.set('newsheight', level)
      _this.changeHeight(level)
      return false
    })

    if(localstorage.get('newsheight')){
      _this.changeHeight(localstorage.get('newsheight'))
    }

    setInterval(function(){
      _this.changeType(_this.thisindex)
    }, 30 * 1000);
  },
  changeType: function(index){
    this.thisindex = index
    $('#newstypetab li').removeClass('on')
    $('#newstypetab li').eq(index).addClass('on')
    switch (index) {
      case 0:
        this.getMix()
        break;
      case 1:
        this.getInfo(0)
        break;
      case 2:
        this.getInfo(1)
        break;        
      case 3:
        this.getInfo(2)
        break;
      case 4:
        this.getInfo(4)
        break;        
      case 5:
        this.getInfo(3)
        break;   
      default:
        break;
    }
    
  },
  getMix: function(){
    var _this = this
    $('#newsinfoc ul').css({
      display: 'none'
    })  
    if(this.codes == ''){
      // $('#newsinfoc ul').css({
      //   display: 'none'
      // }) 
      $('#mixnewsd').html(_this.fillHTML([], true)).show()       
      return false
    }

    $.ajax({
      url: './api/info/mix',
      type: 'GET',
      dataType: 'json',
      data: {
        codes: _this.codes
      }
    })
    .done(function(json) {   
      //return false
      if (json.re) {
      
        $('#mixnewsd').html(_this.fillHTML(json.result.data, true)).show()
      }

    })
    .fail(function(error) {
      
    })
  },
  getInfo: function(type){
    var _this = this

    var content = null
    var zd = ''
    $('#newsinfoc ul').css({
      display: 'none'
    })
    switch (type) {
      case 0:
        content = $('#newsd')
        zd = 'news'
        break;
      case 1:
        content = $('#ggd')
        zd = 'bulletin'
        break;
      case 2:
        content = $('#ybd')
        zd = 'report'
        break;
      case 3:
        content = $('#wdd')
        zd = 'qa'
        break;            
      case 4:
        content = $('#cfhd')
        zd = 'cfh'
        break;           
      default:
        break;
    }

    if(this.codes == ''){
      // $('#newsinfoc ul').css({
      //   display: 'none'
      // }) 
      content.html(_this.fillHTML([], false)).show()       
      return false
    }

    content.show()

    $.ajax({
      url: './api/info/one',
      type: 'GET',
      dataType: 'json',
      data: {
        codes: _this.codes,
        type: type
      }
    })
    .done(function(json) {   

      if (json.re) {

        



        content.html(_this.fillHTML(json.result[zd].data, false))

      }
    })
    .fail(function(error) {
      
    })
  },  
  fillHTML: function(data, showtype){
    //console.info(data)
    if (data.length == 0) {
      return '<div class="infonod">暂无相关内容</div>'
    }

    var html = []
    data.forEach(function(v){
      var type = ''
      var link = ''

      if (v.stockInfo) {
        v.stock = {
          code: v.stockInfo.split('|')[0],
          name: v.stockInfo.split('|')[1]
        }
        v.stock.jmk = v.stock.code.split('.')[0]
        v.stock.jcode = v.stock.code.split('.')[1]
        v.stock.gubamk = ''
        if (v.stock.jmk == '116') {
          v.stock.gubamk = 'hk'
        }
        else if (v.stock.jmk == '105' || v.stock.jmk == '106' || v.stock.jmk == '107') {
          v.stock.gubamk = 'us'
        }
      }      

      switch (v.type) {
        case 'qa':
          type = '问答'
          link = v.stock?'http://ask.eastmoney.com/list.html?code=' + v.stock.jcode:''
          break;
        case 'news':
          type = '资讯'
          link = v.stock?'http://guba.eastmoney.com/interface/GetList.aspx?code=' + v.stock.code:'' //v.stock?'http://guba.eastmoney.com/list,' + v.stock.gubamk + v.stock.jcode + ',1,f.html':''
          break;   
        case 'report':
          type = '研报'
          link = v.stock?'http://data.eastmoney.com/report/' + v.stock.jcode + '.html':''
          break;
        case 'bulletin':
          type = '公告'
          link = v.stock?'http://data.eastmoney.com/notices/stock/' + v.stock.jcode + '.html':''
          break;
        case 'cfh':
          type = '财富号'          
          break;              
        default:
          break;
      }

      html.push('<li>')

      if (showtype) {
        html.push('[')
        if (link) html.push('<a href="' + link + '" target="_blank">')
        html.push(type)
        if (v.stock) {
          html.push('·' + v.stock.name)
        }
        if (link) html.push('</a>')
        html.push('] ')
      }
      else{
        if (v.stock) {
          html.push('[')
          if (link) html.push('<a href="' + link + '" target="_blank">')
          html.push(v.stock.name)
          if (link) html.push('</a>')
          html.push('] ')
        }        
      }
      if (v.type == 'qa') {
        html.push('<span class="qamoney">￥ ' + v.money + '元</span>')
      }      
      html.push('<a href="' + v.url + '" title="' + v.title + '">' + v.title + '</a><span class="time">' + (v.date?v.date.substring(5,10):'') + '</span></li>')
    })
    return html.join('')
  },
  changeHeight: function(level){
    $('#newsnumsc a').removeClass('on')
    $('#newsnumsc a[data-level=' + level + ']').addClass('on')
    var list = $('#newsinfoc .newslist').add('#gubanews')
    if (level == 0) {
      list.height(136)
    }
    else if(level == 1){
      list.height(272)
    }
    else if(level == 2){
      list.height(408)
    }    
    boxsize.resize()
  }
}

global_event.regEvent('stockchange', function(stocks){

  info_web.init(stocks)
})

module.exports = info_web

/***/ }),

/***/ "./modules/info_mines/index.js":
/*!*************************************!*\
  !*** ./modules/info_mines/index.js ***!
  \*************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 信息地雷
 */

var datacache = __webpack_require__(/*! ../datacache */ "./modules/datacache/index.js")
var popmenu = __webpack_require__(/*! ../popmenu */ "./modules/popmenu/index.js")

var infomines = {
  getData: function(codes){
    return $.ajax({
      url: './api/info/infomines',
      type: 'GET',
      dataType: 'json',
      data: {
        codes: codes.join(',')
      }
    })
    .then(function(json) {   
      if (json.re) {
        return json.result
      }
    })
  },
  fillHTML: function(data){
    var _this = this
    //console.info(data)
    Object.keys(data).forEach(function(v){
      if ($('#tablethd4 [data-code="' + v + '"] .td_f14 em .list_mine').length) {
        return false
      }
      var mine = $('<span class="list_mine"><span class="icon icon_mine' + (data[v].data.length > 1?'s':'') + '"></span></span>')
      $('#tablethd4 [data-code="' + v + '"] .td_f14 em').append(mine)
      var newpop = new popmenu({
        target: mine,
        offsetx: -12,
        arrow_dir: 1,
        content: _this.newsHTML(data[v].data)
      })
    })
  },
  newsHTML: function(data){
    var type = ''
    var html = ['<div class="mines_list"><ul>']
    data.forEach(function(v){
      if (!v) {
        return
      }
      switch (v.bztype) {
        case 'news':
          type = '新闻'
          break;
        case 'report':
          type = '研报'
          break;
        case 'notice':
          type = '公告'
          break;
        case 'bulletin':
          type = '公告'
          break;          
        default:
          type = ''
          break;
      }

      if (type) {
        type = ' [' + type + '] '
      }
      else{
        type = ' '
      }

      html.push('<li><a href="' + v.url + '">' + v.date.substring(0, 10) + type + v.title + '</a></li>')
    })
    html.push('</ul></div>')
    return $(html.join(''))
  },
  show: function(){
    var _this = this
    if (datacache.stocks.length == 0) {
      return false
    }
    this.getData(datacache.stocks).then(function(v){
      if (v) {
        _this.fillHTML(v)
        datacache.resizeFill()
      }
      
    })
  }
}





module.exports = infomines

/***/ }),

/***/ "./modules/jsutils/index.js":
/*!**********************************!*\
  !*** ./modules/jsutils/index.js ***!
  \**********************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * 功能库
 */

module.exports = {
  /**
   * 数组排重
   */
  arrayFilterSame: function(array){
    var obj = {}
    array.forEach(function(v){
      obj[v] = null
    })
    return Object.keys(obj)
  }
}

/***/ }),

/***/ "./modules/kuaixun/index.js":
/*!**********************************!*\
  !*** ./modules/kuaixun/index.js ***!
  \**********************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * 快讯
 */


var kuaixun = (function () {

    function kuaixun(options) {
        var defaultoptions = {
            refreshbtn : null, //刷新按钮
            fontsizebtn : null, //字号按钮
            autobtn : null, //自刷按钮
            autosec : null, //自刷时间
            kxlist : null, //内容容器
            kxloading : null, //loading
            refreshtime : 60, //刷新时间
            kxtype: '102', //快讯类型
            kxlink: 'http://kuaixun.eastmoney.com/' //快讯链接
        }
        this.options = $.extend(defaultoptions, options);
        this.cdci = null; //自动刷新
        this.isautocd = true; //是否自动刷新
        this.iskxshow = true; //快讯是否在展示中
        this.fontsize = 14; //当前字号
    }

    /**
     * 初始化
     * @return {[type]} [description]
     */
    kuaixun.prototype.init = function () {
        this.options.autosec.text(this.options.refreshtime);
        this.bind();
        this.refresh();
        this.refreshcd();
    };

    /**
     * 绑定事件
     * @return {[type]} [description]
     */
    kuaixun.prototype.bind = function (){
        var _this = this;
        //刷新按钮
        this.options.refreshbtn.on('click', function(){
            _this.refresh();
            return false;
        });
        //自动刷新按钮
        $('#kx_auto_tc').on('change',function () {
            var thisbtn = $(this);
            //console.info(thisbtn)
            if (thisbtn.is(':checked')) {//开启
                //thisbtn.addClass('kx_autoing');
                _this.isautocd = true;
                _this.refreshcd();

            } else {  //暂停
                //thisbtn.removeClass('kx_autoing');
                _this.isautocd = false;
                clearInterval(_this.cdci);
                _this.options.autosec.text(_this.options.refreshtime);            

            }
        });
        
        if( this.options.fontsizebtn ){
            this.options.fontsizebtn.on('click', function () { //调整字号
                var thisbtn = $(this);
                if (_this.fontsize == 14) {
                    _this.fontsize = 16;
                    //thisbtn.text('小字-');
                    thisbtn.addClass('icon_fontsize').removeClass('icon_fontsize2')
                } else {
                    _this.fontsize = 14;
                    //thisbtn.text('大字+');
                    thisbtn.addClass('icon_fontsize2').removeClass('icon_fontsize')
                }
                _this.options.kxlist.css('font-size', _this.fontsize + 'px');
            }); 
        }
    }

    /**
     * 刷新倒计时
     * @return {[type]} [description]
     */
    kuaixun.prototype.refreshcd = function (){
        var _this = this;
        clearInterval(this.cdci);
        this.cdci = null;
        this.options.autosec.text(this.options.refreshtime);
        if (this.isautocd && this.iskxshow) {
            this.cdci = setInterval(function () {
                var oldTime = _this.options.autosec.text();
                if (oldTime == 1) {
                    _this.refresh();
                } else {
                    _this.options.autosec.text(oldTime - 1);
                }
            }, 1000);
        }
    }
    
    /**
     * 停止倒计时
     */
    kuaixun.prototype.stopRefresh = function(){
        clearInterval(this.cdci);
        this.options.autosec.text(this.options.refreshtime);
    };

    /**
     * 刷新内容
     * @return {[type]} [description]
     */
    kuaixun.prototype.refresh = function (){
        var _this = this;
        this.options.kxloading.show();
        $('#kx_list_t #kx_loading_t').remove()
        $('#kx_list_t').prepend('<div id="kx_loading_t">加载中...</div>')

        setTimeout(function(){
            $.ajax({
                url: 'https://newsinfo.eastmoney.com/kuaixun/v2/api/list',
                type: 'GET',
                dataType: 'jsonp',
                jsonpCallback: 'ajaxResult_' + _this.options.kxtype,
                scriptCharset : 'utf-8',
                cache: false,
                data: {
                    column: _this.options.kxtype,
                    limit: 20,
                    p: 1,
                    callback: 'kxall_ajaxResult' + _this.options.kxtype
                }
            })
            .done(function(data) {   
                data = data.news;         
                var _kxhtml = [];
                //_kxhtml.push('<ul>');
                for (var i = 0; i < data.length; i++) {

                    var aurl = data[i].url_w
                    if (data[i].url_unique && data[i].url_unique.indexOf('http') >= 0) {
                        aurl = data[i].url_unique
                    }

                    _kxhtml.push('<div class="zbbi">');
                    _kxhtml.push('<div class="time">' + data[i].showtime.substring(11,16) + '</div>');
                    //_kxhtml.push('<span class="kx_itime_end">|</span>');
                    var _kx_digest = data[i].digest;
                    if(_kx_digest=='')_kx_digest=data[i].title;
                    if (data[i].newstype == "1") {
                        if (data[i].topic != null) {
                            _kx_digest = '<a href="' + data[i].topic.As_URL + '">' + _kx_digest + '</a><span class="bd_i_zt">专题</span>';
                        }else{
                        _kx_digest = '<a href="' + aurl + '">' + _kx_digest + '[点击查看全文]</a>';
                    }
                        
                    }
                    var _kx_style = "";
                    switch (data[i].titlestyle) {
                        case "1":
                        _kx_style = " bold";
                        break;
                        case "2":
                        _kx_style = " red";
                        break;
                        case "3":
                        _kx_style = " bold red";
                        break;
                    }
                    _kxhtml.push('<div class="zbtext' + _kx_style + '">' + _kx_digest + '</div>');
                    _kxhtml.push('</div>');
                }
                _kxhtml.push('<div class="kx_more_e"><a href="' + _this.options.kxlink + '" target="_blank">查看更多</a></div>');
                _this.options.kxlist.html(_kxhtml.join(''));
                
                _this.options.kxloading.hide();   
            })
            .fail(function() {
                
                var kx_error = $('<div class="kx_error">抱歉，数据没有正常显示<br></div>')
                var handrefreshbtn = $('<a href="javascript:;" target="_self" class="handrefreshbtn">请点此手动刷新</a>');
                kx_error.append(handrefreshbtn);
                _this.options.kxlist.html(kx_error);
                handrefreshbtn.on('click', function(){
                    _this.refresh();
                });
                return false;
            })
            .always(function() {
                _this.refreshcd();
                $('#kx_loading_t').remove()
            });             
        }, 200);
          
    }

    return kuaixun;
})();

module.exports = kuaixun;


/***/ }),

/***/ "./modules/localstorage/index.js":
/*!***************************************!*\
  !*** ./modules/localstorage/index.js ***!
  \***************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * 本地存储
 */

module.exports = {
  get: function(name){
    if (window.localStorage) {
      return localStorage.getItem(name)
    }
    return null
  },
  set: function(name, value){
    if (window.localStorage) {
      localStorage.setItem(name, value)
    }
    
  },
  del: function(name){
    if (window.localStorage) {
      localStorage.removeItem(name)
    }
    
  }
}

/***/ }),

/***/ "./modules/modal/alert.js":
/*!********************************!*\
  !*** ./modules/modal/alert.js ***!
  \********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {


var modal = __webpack_require__(/*! ./index.js */ "./modules/modal/index.js")

module.exports = function(text, bodytext, callback){
  if(typeof bodytext == "function" && callback == undefined){
    callback = bodytext
    bodytext = undefined
  }
  var html = $('<div><div class="modalalert"></div><div class="modalbtnd"><a href="javascript:;" target="_self" class="modalbtn_default">确定</a></div></div>')
  if (text) {
     $('.modalalert', html).append(text)
  }
  if (bodytext) {
    $('.modalalert', html).append('<div class="modalalertb">' + bodytext + '</div>')
  }



  var newmodal = new modal({
    content: html,
    onClose: function(){
      // if (callback) {
      //   callback()
      // }
    }
  })



  newmodal.show()
  

  $('.modalbtn_default', html).click(function(){
    if (callback) {
      callback()
    }
    newmodal.close()
  })
}

/***/ }),

/***/ "./modules/modal/confirm.js":
/*!**********************************!*\
  !*** ./modules/modal/confirm.js ***!
  \**********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var modal = __webpack_require__(/*! ./index.js */ "./modules/modal/index.js")

module.exports = function(text, bodytext, yescallback, nocallback){
  if (typeof bodytext == 'function' && yescallback == undefined) { //两个参数
    yescallback = bodytext
    nocallback = undefined
    bodytext = undefined
  }
  else if(typeof bodytext == 'function' && nocallback == undefined){ //三个参数
    nocallback = yescallback
    yescallback = bodytext
    bodytext = undefined
  }

  var html = $('<div><div class="modalalert"></div><div class="modalbtnd"><a href="javascript:;" target="_self" class="modalbtn_default">确 定</a> &nbsp; <a href="javascript:;" target="_self"  class="modalbtn_cancel">取 消</a></div></div>')
  if (text) {
    $('.modalalert', html).append(text)
  }
  if (bodytext) {
    $('.modalalert', html).append('<div class="modalalertb">' + bodytext + '</div>')
  }  
  var newmodal = new modal({
    content: html,
    onClose: function(){

    }
  })

  newmodal.show()
  

  $('.modalbtn_default', html).click(function(){
    if ( yescallback ) {
      yescallback()
    }
    newmodal.close()
  })

  $('.modalbtn_cancel', html).click(function(){
    if (nocallback) {
      nocallback()
    }
    newmodal.close()
  })  
}

/***/ }),

/***/ "./modules/modal/index.js":
/*!********************************!*\
  !*** ./modules/modal/index.js ***!
  \********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * modal
 */
var modal_html = __webpack_require__(/*! ./modal.html */ "./modules/modal/modal.html")
var dot = __webpack_require__(/*! dot */ "./node_modules/dot/doT.js")
var browser = __webpack_require__(/*! ../browser */ "./modules/browser/index.js")

function modal(options) {
  var default_options = {
    content: '',
    showclose: true,
    showtitle: true,
    title: null,
    onClose: null
  }
  this.options = $.extend(default_options, options)

}

modal.prototype.show = function (callback) {
  var _this = this
  this.html = $(dot.template(modal_html)({
    showclose: this.options.showclose,
    showtitle: this.options.showtitle
  }))

  $('.modaldiv', this.html).append(this.options.content)

  if (this.options.showtitle && this.options.title) {
    $('.modaltitle', this.html).html(this.options.title)
  }

  $('.modal_close', this.html).click(function(){
    _this.close()
  })

  this.html.css({
    top: $(window).scrollTop()
  })

  if (browser.isIE6()) {
    $('.modal_shadow', this.html).css({
      height: $(window).height()
    })
  }

  $('body').append(this.html)

  $('html').css({
    overflow:'hidden'
  })  
  
  this.html.fadeIn(150, function(){
    
    if (callback) {
      callback()
    }
  })
  setTimeout(function(){
    _this.resize()
  }, 10);
};

modal.prototype.close = function(){
  var _this = this
  this.html.fadeOut(150, function(){
    _this.html.remove()
    if (_this.options.onClose) {
      _this.options.onClose()
    }    
  })
  $('html').css({
    overflow:'scroll'
  })

}

modal.prototype.resize = function(){
  var modalbody = $('.modalbody', this.html)

  var top = 0
  var whei = $(window).height()

  if (whei > modalbody.outerHeight()) {
    top = (whei - modalbody.outerHeight())/2 + 100
  }
  modalbody.css({
    //'margin-top': -(modalbody.outerHeight() / 2),
    top: top,
    'margin-left': -(modalbody.outerWidth() / 2)
  })
}

module.exports = modal;


/***/ }),

/***/ "./modules/modal/modal.html":
/*!**********************************!*\
  !*** ./modules/modal/modal.html ***!
  \**********************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"modal\">\r\n  <div class=\"modal_shadow\"></div>\r\n  <div class=\"modalbody\">\r\n    {{? it.showclose }}\r\n    <div class=\"modal_close\"><span class=\"icon icon_mclose\"></span></div>\r\n    {{?}}\r\n    {{? it.showtitle }}\r\n    <div class=\"modaltitle\">提示</div>\r\n    {{?}}\r\n    <div class=\"modaldiv\">\r\n      <!-- <div class=\"modalbtnd\">\r\n        <a href=\"\" class=\"modalbtn_default\">确定</a>\r\n        <a href=\"\" class=\"modalbtn_cancel\">确定</a>        \r\n      </div> -->\r\n\r\n    </div>\r\n  </div>\r\n</div>"

/***/ }),

/***/ "./modules/pager/index.js":
/*!********************************!*\
  !*** ./modules/pager/index.js ***!
  \********************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * 分页
 */

module.exports = function(pageindex, pagesize, sum, urlstr){

  var maxpage = Math.ceil(sum / pagesize)
  
  var fylist = []
  fylist.push({
    text: '第一页',
    num: 1,
    active: false
  })
  if (pageindex > 1) {
    fylist.push({
      text: '上一页',
      num: pageindex - 1,
      active: false
    })        
  }

  if (pageindex <= 4) {
    for (var i = 1; i <= maxpage && i < 6; i++) {
      fylist.push({
        text: i,
        num: i,
        active: pageindex == i
      })          
    }
  }
  else if (pageindex > maxpage - 2) {
    for (var i = maxpage - 4; i <= maxpage; i++) {
      fylist.push({
        text: i,
        num: i,
        active: pageindex == i
      })          
    }
  }      
  else{
    for (var i = pageindex - 2; i <= maxpage && i <= pageindex + 2; i++) {
      fylist.push({
        text: i,
        num: i,
        active: pageindex == i
      })          
    }
  }

  
  // for (var i = 0; i * 20 < json.result.count; i++) {
  //   fylist.push({
  //     text: i + 1,
  //     num: i + 1,
  //     active: pageindex == i + 1
  //   })
  // }

  if (pageindex < maxpage) {
    fylist.push({
      text: '下一页',
      num: pageindex + 1,
      active: false
    })        
  }

  fylist.push({
    text: '最后页',
    num: maxpage,
    active: false
  })

  var html = []
  var link

  fylist.forEach(function(v){
      link = urlstr.replace('{page}', v.num)
      html.push('<a ')
      if (v.active) {
        html.push('class="on" ')
      }
      html.push('href="' + link + '" data-page="' + v.num + '" target="_self">' + v.text + '</a>')
  })

  if (maxpage >= 2) {
    return html.join('')
  }
  else{
    return ''
  }
  
}

/***/ }),

/***/ "./modules/pkyd/web.js":
/*!*****************************!*\
  !*** ./modules/pkyd/web.js ***!
  \*****************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 盘口异动
 */

var ts = __webpack_require__(/*! ../quote_ts/ts */ "./modules/quote_ts/ts.js")
var global_event = __webpack_require__(/*! ../global_event */ "./modules/global_event/index.js")
var webconfig = __webpack_require__(/*! ../../config/webconfig */ "./config/webconfig.js")

var pkyd = {
  maxlength: 9,
  datacache: null,
  isstock: false,
  stocks: null,
  init: function(){
    this.link()
    this.bind()
  },
  config: {
    201: {
      name: "封涨停板"
    },
    301: {
      name: "封跌停板"
    },
    202: {
      name: "打开涨停板"
    },
    302: {
      name: "打开跌停板"
    },
    1: {
      name: "有大买盘"
    },
    101: {
      name: "有大卖盘"
    },
    2: {
      name: "大笔买入"
    },
    102: {
      name: "大笔卖出"
    },
    402: {
      name: "火箭发射"
    },
    403: {
      name: "快速反弹"
    },
    502: {
      name: "高台跳水"
    },
    503: {
      name: "快速下跌"
    },
    404: {
      name: "竞价上涨"
    },
    504: {
      name: "竞价下跌"
    },
    203: {
      name: "高开5日线"
    },
    303: {
      name: "低开5日线"
    },
    401: {
      name: "向上缺口"
    },
    501: {
      name: "向下缺口"
    },
    204: {
      name: "60日新高"
    },
    304: {
      name: "60日新低"
    },
    405: {
      name: "60日大幅上涨"
    },
    505: {
      name: "60日大幅下跌"
    }
  },
  thison: false,
  bind: function(){
    var _this = this
    var pkydmore = $('#pkydmore')

    pkydmore.on('mouseenter', function(){
      _this.thison = true
    })

    pkydmore.on('mouseleave', function(){
      _this.thison = false
    })    

    $('#pkydzk').click(function(){
      if (pkydmore.is(':visible')) {
        $('#pkydmore').fadeOut(150)
        $('#pkydzk .icon:first').show()
        $('#pkydzk .icon:last').hide()
      }
      else{
        $('#pkydmore').fadeIn(150)
        $('#pkydzk .icon:first').hide()
        $('#pkydzk .icon:last').show()
      }
      
    })

    $('#pykdcheck').click(function(){
      if (_this.isstock) {
        $('#pykdcheck .icon:first').show()
        $('#pykdcheck .icon:last').hide()        
        _this.isstock = false
      }
      else{
        $('#pykdcheck .icon:first').hide()
        $('#pykdcheck .icon:last').show()
        _this.isstock = true
      }
       _this.link()
    })
  },
  /**
   * 首次填充
   */
  firstFill: function(data){
    //console.info(data)
    if (data.length == 0) {
      $('#pkyd_first').html('')
      $('#pkydmore ul').html('')
      return false
    }
    var _this = this
    var firstitem = data[data.length - 1]
    $('#pkyd_first').html(this.itemFill(firstitem.split(',')))

    var html = []
    for (var i = data.length - 9; i < data.length - 1; i++) {
      if (i < 0) {
        i = 0
      }
      html.push('<li>' + _this.itemFill(data[i].split(',')) + '</li>')
    }

    if(!this.thison){
      $('#pkydmore ul').html(html.join(''))
    } 
    //$('#pkydmore ul').html(html.join(''))
  },
  itemFill: function(item){
    var market = ''
    if (item[2] == '0') {
      market = 'sz'
    }
    else if(item[2] == '1'){
      market = 'sh'
    }
    var msg = ''
    if (this.config[item[4]]) {
      msg = this.config[item[4]].name
    }
    var color = ''
    if (item[6] == "1") {
      color = 'stockup'
    }
    else if(item[6] == "2"){
      color = 'stockdown'
    }
    return item[0] + ' <a href="http://quote.eastmoney.com/changes/stocks/' + market + item[1] + '.html">' + item[3] + '</a> <span class="' + color + '">' + msg + ' ' + item[5] + '</span>'
  },
  setStocks: function(stocks){
    this.stocks = stocks.join(',')
  },
  link: function(){
    var _this = this
    if (this.qts) {
      this.qts.close()
    }
    this.getTS(function(data){
      if (data.data == null) {
        return false
      }
      if (data.full == 1 && data.rt == 15 && data.data.pkyd ) {
        _this.datacache = data.data.pkyd
        _this.firstFill(_this.datacache)
      }
      else if(data.data.pkyd.length > 0){
        _this.datacache.push(data.data.pkyd[0])
        _this.firstFill(_this.datacache)
      }
      
    })
  },
  getTS: function(callback){
    var tsurl =  webconfig.getWebPath('quotepath') + 'api/qt/pkyd/sse?lmt=9&fields=f1,f2,f3,f4,f5,f6,f7&ut=6d2ffaa6a585d612eda28417681d58fb'
    if (this.isstock) {
      tsurl += '&secids=' + this.stocks
    }
    this.qts = new ts({
      subUrl: tsurl, //
      callback: function(data){
        if (data.rc == 0 && data.data != null) {
          callback(data)
        }
      }
    });
  }
}

global_event.regEvent('stockchange', function(stocks){
  // console.info(stocks)
  pkyd.setStocks(stocks)
  pkyd.link()
})

module.exports = pkyd

/***/ }),

/***/ "./modules/polyfill/array.js":
/*!***********************************!*\
  !*** ./modules/polyfill/array.js ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports) {

// https://tc39.github.io/ecma262/#sec-array.prototype.find
if (!Array.prototype.find) {
  Object.defineProperty(Array.prototype, 'find', {
    value: function(predicate) {
     // 1. Let O be ? ToObject(this value).
      if (this == null) {
        throw new TypeError('"this" is null or not defined');
      }

      var o = Object(this);

      // 2. Let len be ? ToLength(? Get(O, "length")).
      var len = o.length >>> 0;

      // 3. If IsCallable(predicate) is false, throw a TypeError exception.
      if (typeof predicate !== 'function') {
        throw new TypeError('predicate must be a function');
      }

      // 4. If thisArg was supplied, let T be thisArg; else let T be undefined.
      var thisArg = arguments[1];

      // 5. Let k be 0.
      var k = 0;

      // 6. Repeat, while k < len
      while (k < len) {
        // a. Let Pk be ! ToString(k).
        // b. Let kValue be ? Get(O, Pk).
        // c. Let testResult be ToBoolean(? Call(predicate, T, « kValue, k, O »)).
        // d. If testResult is true, return kValue.
        var kValue = o[k];
        if (predicate.call(thisArg, kValue, k, o)) {
          return kValue;
        }
        // e. Increase k by 1.
        k++;
      }

      // 7. Return undefined.
      return undefined;
    }
  });
}

/***/ }),

/***/ "./modules/polyfill/index.js":
/*!***********************************!*\
  !*** ./modules/polyfill/index.js ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(/*! ./promise */ "./modules/polyfill/promise.js")
__webpack_require__(/*! ./array */ "./modules/polyfill/array.js")

/***/ }),

/***/ "./modules/polyfill/promise.js":
/*!*************************************!*\
  !*** ./modules/polyfill/promise.js ***!
  \*************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(process, global) {/*!
 * @overview es6-promise - a tiny implementation of Promises/A+.
 * @copyright Copyright (c) 2014 Yehuda Katz, Tom Dale, Stefan Penner and contributors (Conversion to ES6 API by Jake Archibald)
 * @license   Licensed under MIT license
 *            See https://raw.githubusercontent.com/stefanpenner/es6-promise/master/LICENSE
 * @version   v4.2.5+7f2b526d
 */

(function (global, factory) {
	 true ? module.exports = factory() :
	undefined;
}(this, (function () { 'use strict';

function objectOrFunction(x) {
  var type = typeof x;
  return x !== null && (type === 'object' || type === 'function');
}

function isFunction(x) {
  return typeof x === 'function';
}



var _isArray = void 0;
if (Array.isArray) {
  _isArray = Array.isArray;
} else {
  _isArray = function (x) {
    return Object.prototype.toString.call(x) === '[object Array]';
  };
}

var isArray = _isArray;

var len = 0;
var vertxNext = void 0;
var customSchedulerFn = void 0;

var asap = function asap(callback, arg) {
  queue[len] = callback;
  queue[len + 1] = arg;
  len += 2;
  if (len === 2) {
    // If len is 2, that means that we need to schedule an async flush.
    // If additional callbacks are queued before the queue is flushed, they
    // will be processed by this flush that we are scheduling.
    if (customSchedulerFn) {
      customSchedulerFn(flush);
    } else {
      scheduleFlush();
    }
  }
};

function setScheduler(scheduleFn) {
  customSchedulerFn = scheduleFn;
}

function setAsap(asapFn) {
  asap = asapFn;
}

var browserWindow = typeof window !== 'undefined' ? window : undefined;
var browserGlobal = browserWindow || {};
var BrowserMutationObserver = browserGlobal.MutationObserver || browserGlobal.WebKitMutationObserver;
var isNode = typeof self === 'undefined' && typeof process !== 'undefined' && {}.toString.call(process) === '[object process]';

// test for web worker but not in IE10
var isWorker = typeof Uint8ClampedArray !== 'undefined' && typeof importScripts !== 'undefined' && typeof MessageChannel !== 'undefined';

// node
function useNextTick() {
  // node version 0.10.x displays a deprecation warning when nextTick is used recursively
  // see https://github.com/cujojs/when/issues/410 for details
  return function () {
    return process.nextTick(flush);
  };
}

// vertx
function useVertxTimer() {
  if (typeof vertxNext !== 'undefined') {
    return function () {
      vertxNext(flush);
    };
  }

  return useSetTimeout();
}

function useMutationObserver() {
  var iterations = 0;
  var observer = new BrowserMutationObserver(flush);
  var node = document.createTextNode('');
  observer.observe(node, { characterData: true });

  return function () {
    node.data = iterations = ++iterations % 2;
  };
}

// web worker
function useMessageChannel() {
  var channel = new MessageChannel();
  channel.port1.onmessage = flush;
  return function () {
    return channel.port2.postMessage(0);
  };
}

function useSetTimeout() {
  // Store setTimeout reference so es6-promise will be unaffected by
  // other code modifying setTimeout (like sinon.useFakeTimers())
  var globalSetTimeout = setTimeout;
  return function () {
    return globalSetTimeout(flush, 1);
  };
}

var queue = new Array(1000);
function flush() {
  for (var i = 0; i < len; i += 2) {
    var callback = queue[i];
    var arg = queue[i + 1];

    callback(arg);

    queue[i] = undefined;
    queue[i + 1] = undefined;
  }

  len = 0;
}

function attemptVertx() {
  try {
    var vertx = Function('return this')().require('vertx');
    vertxNext = vertx.runOnLoop || vertx.runOnContext;
    return useVertxTimer();
  } catch (e) {
    return useSetTimeout();
  }
}

var scheduleFlush = void 0;
// Decide what async method to use to triggering processing of queued callbacks:
if (isNode) {
  scheduleFlush = useNextTick();
} else if (BrowserMutationObserver) {
  scheduleFlush = useMutationObserver();
} else if (isWorker) {
  scheduleFlush = useMessageChannel();
} else if (browserWindow === undefined && "function" === 'function') {
  scheduleFlush = attemptVertx();
} else {
  scheduleFlush = useSetTimeout();
}

function then(onFulfillment, onRejection) {
  var parent = this;

  var child = new this.constructor(noop);

  if (child[PROMISE_ID] === undefined) {
    makePromise(child);
  }

  var _state = parent._state;


  if (_state) {
    var callback = arguments[_state - 1];
    asap(function () {
      return invokeCallback(_state, child, callback, parent._result);
    });
  } else {
    subscribe(parent, child, onFulfillment, onRejection);
  }

  return child;
}

/**
  `Promise.resolve` returns a promise that will become resolved with the
  passed `value`. It is shorthand for the following:

  ```javascript
  let promise = new Promise(function(resolve, reject){
    resolve(1);
  });

  promise.then(function(value){
    // value === 1
  });
  ```

  Instead of writing the above, your code now simply becomes the following:

  ```javascript
  let promise = Promise.resolve(1);

  promise.then(function(value){
    // value === 1
  });
  ```

  @method resolve
  @static
  @param {Any} value value that the returned promise will be resolved with
  Useful for tooling.
  @return {Promise} a promise that will become fulfilled with the given
  `value`
*/
function resolve$1(object) {
  /*jshint validthis:true */
  var Constructor = this;

  if (object && typeof object === 'object' && object.constructor === Constructor) {
    return object;
  }

  var promise = new Constructor(noop);
  resolve(promise, object);
  return promise;
}

var PROMISE_ID = Math.random().toString(36).substring(2);

function noop() {}

var PENDING = void 0;
var FULFILLED = 1;
var REJECTED = 2;

var TRY_CATCH_ERROR = { error: null };

function selfFulfillment() {
  return new TypeError("You cannot resolve a promise with itself");
}

function cannotReturnOwn() {
  return new TypeError('A promises callback cannot return that same promise.');
}

function getThen(promise) {
  try {
    return promise.then;
  } catch (error) {
    TRY_CATCH_ERROR.error = error;
    return TRY_CATCH_ERROR;
  }
}

function tryThen(then$$1, value, fulfillmentHandler, rejectionHandler) {
  try {
    then$$1.call(value, fulfillmentHandler, rejectionHandler);
  } catch (e) {
    return e;
  }
}

function handleForeignThenable(promise, thenable, then$$1) {
  asap(function (promise) {
    var sealed = false;
    var error = tryThen(then$$1, thenable, function (value) {
      if (sealed) {
        return;
      }
      sealed = true;
      if (thenable !== value) {
        resolve(promise, value);
      } else {
        fulfill(promise, value);
      }
    }, function (reason) {
      if (sealed) {
        return;
      }
      sealed = true;

      reject(promise, reason);
    }, 'Settle: ' + (promise._label || ' unknown promise'));

    if (!sealed && error) {
      sealed = true;
      reject(promise, error);
    }
  }, promise);
}

function handleOwnThenable(promise, thenable) {
  if (thenable._state === FULFILLED) {
    fulfill(promise, thenable._result);
  } else if (thenable._state === REJECTED) {
    reject(promise, thenable._result);
  } else {
    subscribe(thenable, undefined, function (value) {
      return resolve(promise, value);
    }, function (reason) {
      return reject(promise, reason);
    });
  }
}

function handleMaybeThenable(promise, maybeThenable, then$$1) {
  if (maybeThenable.constructor === promise.constructor && then$$1 === then && maybeThenable.constructor.resolve === resolve$1) {
    handleOwnThenable(promise, maybeThenable);
  } else {
    if (then$$1 === TRY_CATCH_ERROR) {
      reject(promise, TRY_CATCH_ERROR.error);
      TRY_CATCH_ERROR.error = null;
    } else if (then$$1 === undefined) {
      fulfill(promise, maybeThenable);
    } else if (isFunction(then$$1)) {
      handleForeignThenable(promise, maybeThenable, then$$1);
    } else {
      fulfill(promise, maybeThenable);
    }
  }
}

function resolve(promise, value) {
  if (promise === value) {
    reject(promise, selfFulfillment());
  } else if (objectOrFunction(value)) {
    handleMaybeThenable(promise, value, getThen(value));
  } else {
    fulfill(promise, value);
  }
}

function publishRejection(promise) {
  if (promise._onerror) {
    promise._onerror(promise._result);
  }

  publish(promise);
}

function fulfill(promise, value) {
  if (promise._state !== PENDING) {
    return;
  }

  promise._result = value;
  promise._state = FULFILLED;

  if (promise._subscribers.length !== 0) {
    asap(publish, promise);
  }
}

function reject(promise, reason) {
  if (promise._state !== PENDING) {
    return;
  }
  promise._state = REJECTED;
  promise._result = reason;

  asap(publishRejection, promise);
}

function subscribe(parent, child, onFulfillment, onRejection) {
  var _subscribers = parent._subscribers;
  var length = _subscribers.length;


  parent._onerror = null;

  _subscribers[length] = child;
  _subscribers[length + FULFILLED] = onFulfillment;
  _subscribers[length + REJECTED] = onRejection;

  if (length === 0 && parent._state) {
    asap(publish, parent);
  }
}

function publish(promise) {
  var subscribers = promise._subscribers;
  var settled = promise._state;

  if (subscribers.length === 0) {
    return;
  }

  var child = void 0,
      callback = void 0,
      detail = promise._result;

  for (var i = 0; i < subscribers.length; i += 3) {
    child = subscribers[i];
    callback = subscribers[i + settled];

    if (child) {
      invokeCallback(settled, child, callback, detail);
    } else {
      callback(detail);
    }
  }

  promise._subscribers.length = 0;
}

function tryCatch(callback, detail) {
  try {
    return callback(detail);
  } catch (e) {
    TRY_CATCH_ERROR.error = e;
    return TRY_CATCH_ERROR;
  }
}

function invokeCallback(settled, promise, callback, detail) {
  var hasCallback = isFunction(callback),
      value = void 0,
      error = void 0,
      succeeded = void 0,
      failed = void 0;

  if (hasCallback) {
    value = tryCatch(callback, detail);

    if (value === TRY_CATCH_ERROR) {
      failed = true;
      error = value.error;
      value.error = null;
    } else {
      succeeded = true;
    }

    if (promise === value) {
      reject(promise, cannotReturnOwn());
      return;
    }
  } else {
    value = detail;
    succeeded = true;
  }

  if (promise._state !== PENDING) {
    // noop
  } else if (hasCallback && succeeded) {
    resolve(promise, value);
  } else if (failed) {
    reject(promise, error);
  } else if (settled === FULFILLED) {
    fulfill(promise, value);
  } else if (settled === REJECTED) {
    reject(promise, value);
  }
}

function initializePromise(promise, resolver) {
  try {
    resolver(function resolvePromise(value) {
      resolve(promise, value);
    }, function rejectPromise(reason) {
      reject(promise, reason);
    });
  } catch (e) {
    reject(promise, e);
  }
}

var id = 0;
function nextId() {
  return id++;
}

function makePromise(promise) {
  promise[PROMISE_ID] = id++;
  promise._state = undefined;
  promise._result = undefined;
  promise._subscribers = [];
}

function validationError() {
  return new Error('Array Methods must be provided an Array');
}

var Enumerator = function () {
  function Enumerator(Constructor, input) {
    this._instanceConstructor = Constructor;
    this.promise = new Constructor(noop);

    if (!this.promise[PROMISE_ID]) {
      makePromise(this.promise);
    }

    if (isArray(input)) {
      this.length = input.length;
      this._remaining = input.length;

      this._result = new Array(this.length);

      if (this.length === 0) {
        fulfill(this.promise, this._result);
      } else {
        this.length = this.length || 0;
        this._enumerate(input);
        if (this._remaining === 0) {
          fulfill(this.promise, this._result);
        }
      }
    } else {
      reject(this.promise, validationError());
    }
  }

  Enumerator.prototype._enumerate = function _enumerate(input) {
    for (var i = 0; this._state === PENDING && i < input.length; i++) {
      this._eachEntry(input[i], i);
    }
  };

  Enumerator.prototype._eachEntry = function _eachEntry(entry, i) {
    var c = this._instanceConstructor;
    var resolve$$1 = c.resolve;


    if (resolve$$1 === resolve$1) {
      var _then = getThen(entry);

      if (_then === then && entry._state !== PENDING) {
        this._settledAt(entry._state, i, entry._result);
      } else if (typeof _then !== 'function') {
        this._remaining--;
        this._result[i] = entry;
      } else if (c === Promise$2) {
        var promise = new c(noop);
        handleMaybeThenable(promise, entry, _then);
        this._willSettleAt(promise, i);
      } else {
        this._willSettleAt(new c(function (resolve$$1) {
          return resolve$$1(entry);
        }), i);
      }
    } else {
      this._willSettleAt(resolve$$1(entry), i);
    }
  };

  Enumerator.prototype._settledAt = function _settledAt(state, i, value) {
    var promise = this.promise;


    if (promise._state === PENDING) {
      this._remaining--;

      if (state === REJECTED) {
        reject(promise, value);
      } else {
        this._result[i] = value;
      }
    }

    if (this._remaining === 0) {
      fulfill(promise, this._result);
    }
  };

  Enumerator.prototype._willSettleAt = function _willSettleAt(promise, i) {
    var enumerator = this;

    subscribe(promise, undefined, function (value) {
      return enumerator._settledAt(FULFILLED, i, value);
    }, function (reason) {
      return enumerator._settledAt(REJECTED, i, reason);
    });
  };

  return Enumerator;
}();

/**
  `Promise.all` accepts an array of promises, and returns a new promise which
  is fulfilled with an array of fulfillment values for the passed promises, or
  rejected with the reason of the first passed promise to be rejected. It casts all
  elements of the passed iterable to promises as it runs this algorithm.

  Example:

  ```javascript
  let promise1 = resolve(1);
  let promise2 = resolve(2);
  let promise3 = resolve(3);
  let promises = [ promise1, promise2, promise3 ];

  Promise.all(promises).then(function(array){
    // The array here would be [ 1, 2, 3 ];
  });
  ```

  If any of the `promises` given to `all` are rejected, the first promise
  that is rejected will be given as an argument to the returned promises's
  rejection handler. For example:

  Example:

  ```javascript
  let promise1 = resolve(1);
  let promise2 = reject(new Error("2"));
  let promise3 = reject(new Error("3"));
  let promises = [ promise1, promise2, promise3 ];

  Promise.all(promises).then(function(array){
    // Code here never runs because there are rejected promises!
  }, function(error) {
    // error.message === "2"
  });
  ```

  @method all
  @static
  @param {Array} entries array of promises
  @param {String} label optional string for labeling the promise.
  Useful for tooling.
  @return {Promise} promise that is fulfilled when all `promises` have been
  fulfilled, or rejected if any of them become rejected.
  @static
*/
function all(entries) {
  return new Enumerator(this, entries).promise;
}

/**
  `Promise.race` returns a new promise which is settled in the same way as the
  first passed promise to settle.

  Example:

  ```javascript
  let promise1 = new Promise(function(resolve, reject){
    setTimeout(function(){
      resolve('promise 1');
    }, 200);
  });

  let promise2 = new Promise(function(resolve, reject){
    setTimeout(function(){
      resolve('promise 2');
    }, 100);
  });

  Promise.race([promise1, promise2]).then(function(result){
    // result === 'promise 2' because it was resolved before promise1
    // was resolved.
  });
  ```

  `Promise.race` is deterministic in that only the state of the first
  settled promise matters. For example, even if other promises given to the
  `promises` array argument are resolved, but the first settled promise has
  become rejected before the other promises became fulfilled, the returned
  promise will become rejected:

  ```javascript
  let promise1 = new Promise(function(resolve, reject){
    setTimeout(function(){
      resolve('promise 1');
    }, 200);
  });

  let promise2 = new Promise(function(resolve, reject){
    setTimeout(function(){
      reject(new Error('promise 2'));
    }, 100);
  });

  Promise.race([promise1, promise2]).then(function(result){
    // Code here never runs
  }, function(reason){
    // reason.message === 'promise 2' because promise 2 became rejected before
    // promise 1 became fulfilled
  });
  ```

  An example real-world use case is implementing timeouts:

  ```javascript
  Promise.race([ajax('foo.json'), timeout(5000)])
  ```

  @method race
  @static
  @param {Array} promises array of promises to observe
  Useful for tooling.
  @return {Promise} a promise which settles in the same way as the first passed
  promise to settle.
*/
function race(entries) {
  /*jshint validthis:true */
  var Constructor = this;

  if (!isArray(entries)) {
    return new Constructor(function (_, reject) {
      return reject(new TypeError('You must pass an array to race.'));
    });
  } else {
    return new Constructor(function (resolve, reject) {
      var length = entries.length;
      for (var i = 0; i < length; i++) {
        Constructor.resolve(entries[i]).then(resolve, reject);
      }
    });
  }
}

/**
  `Promise.reject` returns a promise rejected with the passed `reason`.
  It is shorthand for the following:

  ```javascript
  let promise = new Promise(function(resolve, reject){
    reject(new Error('WHOOPS'));
  });

  promise.then(function(value){
    // Code here doesn't run because the promise is rejected!
  }, function(reason){
    // reason.message === 'WHOOPS'
  });
  ```

  Instead of writing the above, your code now simply becomes the following:

  ```javascript
  let promise = Promise.reject(new Error('WHOOPS'));

  promise.then(function(value){
    // Code here doesn't run because the promise is rejected!
  }, function(reason){
    // reason.message === 'WHOOPS'
  });
  ```

  @method reject
  @static
  @param {Any} reason value that the returned promise will be rejected with.
  Useful for tooling.
  @return {Promise} a promise rejected with the given `reason`.
*/
function reject$1(reason) {
  /*jshint validthis:true */
  var Constructor = this;
  var promise = new Constructor(noop);
  reject(promise, reason);
  return promise;
}

function needsResolver() {
  throw new TypeError('You must pass a resolver function as the first argument to the promise constructor');
}

function needsNew() {
  throw new TypeError("Failed to construct 'Promise': Please use the 'new' operator, this object constructor cannot be called as a function.");
}

/**
  Promise objects represent the eventual result of an asynchronous operation. The
  primary way of interacting with a promise is through its `then` method, which
  registers callbacks to receive either a promise's eventual value or the reason
  why the promise cannot be fulfilled.

  Terminology
  -----------

  - `promise` is an object or function with a `then` method whose behavior conforms to this specification.
  - `thenable` is an object or function that defines a `then` method.
  - `value` is any legal JavaScript value (including undefined, a thenable, or a promise).
  - `exception` is a value that is thrown using the throw statement.
  - `reason` is a value that indicates why a promise was rejected.
  - `settled` the final resting state of a promise, fulfilled or rejected.

  A promise can be in one of three states: pending, fulfilled, or rejected.

  Promises that are fulfilled have a fulfillment value and are in the fulfilled
  state.  Promises that are rejected have a rejection reason and are in the
  rejected state.  A fulfillment value is never a thenable.

  Promises can also be said to *resolve* a value.  If this value is also a
  promise, then the original promise's settled state will match the value's
  settled state.  So a promise that *resolves* a promise that rejects will
  itself reject, and a promise that *resolves* a promise that fulfills will
  itself fulfill.


  Basic Usage:
  ------------

  ```js
  let promise = new Promise(function(resolve, reject) {
    // on success
    resolve(value);

    // on failure
    reject(reason);
  });

  promise.then(function(value) {
    // on fulfillment
  }, function(reason) {
    // on rejection
  });
  ```

  Advanced Usage:
  ---------------

  Promises shine when abstracting away asynchronous interactions such as
  `XMLHttpRequest`s.

  ```js
  function getJSON(url) {
    return new Promise(function(resolve, reject){
      let xhr = new XMLHttpRequest();

      xhr.open('GET', url);
      xhr.onreadystatechange = handler;
      xhr.responseType = 'json';
      xhr.setRequestHeader('Accept', 'application/json');
      xhr.send();

      function handler() {
        if (this.readyState === this.DONE) {
          if (this.status === 200) {
            resolve(this.response);
          } else {
            reject(new Error('getJSON: `' + url + '` failed with status: [' + this.status + ']'));
          }
        }
      };
    });
  }

  getJSON('/posts.json').then(function(json) {
    // on fulfillment
  }, function(reason) {
    // on rejection
  });
  ```

  Unlike callbacks, promises are great composable primitives.

  ```js
  Promise.all([
    getJSON('/posts'),
    getJSON('/comments')
  ]).then(function(values){
    values[0] // => postsJSON
    values[1] // => commentsJSON

    return values;
  });
  ```

  @class Promise
  @param {Function} resolver
  Useful for tooling.
  @constructor
*/

var Promise$2 = function () {
  function Promise(resolver) {
    this[PROMISE_ID] = nextId();
    this._result = this._state = undefined;
    this._subscribers = [];

    if (noop !== resolver) {
      typeof resolver !== 'function' && needsResolver();
      this instanceof Promise ? initializePromise(this, resolver) : needsNew();
    }
  }

  /**
  The primary way of interacting with a promise is through its `then` method,
  which registers callbacks to receive either a promise's eventual value or the
  reason why the promise cannot be fulfilled.
   ```js
  findUser().then(function(user){
    // user is available
  }, function(reason){
    // user is unavailable, and you are given the reason why
  });
  ```
   Chaining
  --------
   The return value of `then` is itself a promise.  This second, 'downstream'
  promise is resolved with the return value of the first promise's fulfillment
  or rejection handler, or rejected if the handler throws an exception.
   ```js
  findUser().then(function (user) {
    return user.name;
  }, function (reason) {
    return 'default name';
  }).then(function (userName) {
    // If `findUser` fulfilled, `userName` will be the user's name, otherwise it
    // will be `'default name'`
  });
   findUser().then(function (user) {
    throw new Error('Found user, but still unhappy');
  }, function (reason) {
    throw new Error('`findUser` rejected and we're unhappy');
  }).then(function (value) {
    // never reached
  }, function (reason) {
    // if `findUser` fulfilled, `reason` will be 'Found user, but still unhappy'.
    // If `findUser` rejected, `reason` will be '`findUser` rejected and we're unhappy'.
  });
  ```
  If the downstream promise does not specify a rejection handler, rejection reasons will be propagated further downstream.
   ```js
  findUser().then(function (user) {
    throw new PedagogicalException('Upstream error');
  }).then(function (value) {
    // never reached
  }).then(function (value) {
    // never reached
  }, function (reason) {
    // The `PedgagocialException` is propagated all the way down to here
  });
  ```
   Assimilation
  ------------
   Sometimes the value you want to propagate to a downstream promise can only be
  retrieved asynchronously. This can be achieved by returning a promise in the
  fulfillment or rejection handler. The downstream promise will then be pending
  until the returned promise is settled. This is called *assimilation*.
   ```js
  findUser().then(function (user) {
    return findCommentsByAuthor(user);
  }).then(function (comments) {
    // The user's comments are now available
  });
  ```
   If the assimliated promise rejects, then the downstream promise will also reject.
   ```js
  findUser().then(function (user) {
    return findCommentsByAuthor(user);
  }).then(function (comments) {
    // If `findCommentsByAuthor` fulfills, we'll have the value here
  }, function (reason) {
    // If `findCommentsByAuthor` rejects, we'll have the reason here
  });
  ```
   Simple Example
  --------------
   Synchronous Example
   ```javascript
  let result;
   try {
    result = findResult();
    // success
  } catch(reason) {
    // failure
  }
  ```
   Errback Example
   ```js
  findResult(function(result, err){
    if (err) {
      // failure
    } else {
      // success
    }
  });
  ```
   Promise Example;
   ```javascript
  findResult().then(function(result){
    // success
  }, function(reason){
    // failure
  });
  ```
   Advanced Example
  --------------
   Synchronous Example
   ```javascript
  let author, books;
   try {
    author = findAuthor();
    books  = findBooksByAuthor(author);
    // success
  } catch(reason) {
    // failure
  }
  ```
   Errback Example
   ```js
   function foundBooks(books) {
   }
   function failure(reason) {
   }
   findAuthor(function(author, err){
    if (err) {
      failure(err);
      // failure
    } else {
      try {
        findBoooksByAuthor(author, function(books, err) {
          if (err) {
            failure(err);
          } else {
            try {
              foundBooks(books);
            } catch(reason) {
              failure(reason);
            }
          }
        });
      } catch(error) {
        failure(err);
      }
      // success
    }
  });
  ```
   Promise Example;
   ```javascript
  findAuthor().
    then(findBooksByAuthor).
    then(function(books){
      // found books
  }).catch(function(reason){
    // something went wrong
  });
  ```
   @method then
  @param {Function} onFulfilled
  @param {Function} onRejected
  Useful for tooling.
  @return {Promise}
  */

  /**
  `catch` is simply sugar for `then(undefined, onRejection)` which makes it the same
  as the catch block of a try/catch statement.
  ```js
  function findAuthor(){
  throw new Error('couldn't find that author');
  }
  // synchronous
  try {
  findAuthor();
  } catch(reason) {
  // something went wrong
  }
  // async with promises
  findAuthor().catch(function(reason){
  // something went wrong
  });
  ```
  @method catch
  @param {Function} onRejection
  Useful for tooling.
  @return {Promise}
  */


  Promise.prototype.catch = function _catch(onRejection) {
    return this.then(null, onRejection);
  };

  /**
    `finally` will be invoked regardless of the promise's fate just as native
    try/catch/finally behaves
  
    Synchronous example:
  
    ```js
    findAuthor() {
      if (Math.random() > 0.5) {
        throw new Error();
      }
      return new Author();
    }
  
    try {
      return findAuthor(); // succeed or fail
    } catch(error) {
      return findOtherAuther();
    } finally {
      // always runs
      // doesn't affect the return value
    }
    ```
  
    Asynchronous example:
  
    ```js
    findAuthor().catch(function(reason){
      return findOtherAuther();
    }).finally(function(){
      // author was either found, or not
    });
    ```
  
    @method finally
    @param {Function} callback
    @return {Promise}
  */


  Promise.prototype.finally = function _finally(callback) {
    var promise = this;
    var constructor = promise.constructor;

    if (isFunction(callback)) {
      return promise.then(function (value) {
        return constructor.resolve(callback()).then(function () {
          return value;
        });
      }, function (reason) {
        return constructor.resolve(callback()).then(function () {
          throw reason;
        });
      });
    }

    return promise.then(callback, callback);
  };

  return Promise;
}();

Promise$2.prototype.then = then;
Promise$2.all = all;
Promise$2.race = race;
Promise$2.resolve = resolve$1;
Promise$2.reject = reject$1;
Promise$2._setScheduler = setScheduler;
Promise$2._setAsap = setAsap;
Promise$2._asap = asap;

/*global self*/
function polyfill() {
  var local = void 0;

  if (typeof global !== 'undefined') {
    local = global;
  } else if (typeof self !== 'undefined') {
    local = self;
  } else {
    try {
      local = Function('return this')();
    } catch (e) {
      throw new Error('polyfill failed because global object is unavailable in this environment');
    }
  }

  var P = local.Promise;

  if (P) {
    var promiseToString = null;
    try {
      promiseToString = Object.prototype.toString.call(P.resolve());
    } catch (e) {
      // silently ignored
    }

    if (promiseToString === '[object Promise]' && !P.cast) {
      return;
    }
  }

  local.Promise = Promise$2;
}

// Strange compat..
Promise$2.polyfill = polyfill;
Promise$2.Promise = Promise$2;

Promise$2.polyfill();

return Promise$2;

})));



//# sourceMappingURL=es6-promise.auto.map
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! ./../../node_modules/process/browser.js */ "./node_modules/process/browser.js"), __webpack_require__(/*! ./../../node_modules/webpack/buildin/global.js */ "./node_modules/webpack/buildin/global.js")))

/***/ }),

/***/ "./modules/popmenu/index.js":
/*!**********************************!*\
  !*** ./modules/popmenu/index.js ***!
  \**********************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * 悬浮菜单
 */

//arrow_dir



function popmenu(options) {
  var default_options = {
    target: '',
    method: 'mouseenter',
    delay: 300,
    outdelay: 500,
    items: null,
    content: null,
    offsetx: 0,
    arrow_dir: 2,
    onMoveIn: null,
    onHover: function(){
      
    },
    onOut: function(){
      
    }
  }
  this.options = $.extend(default_options, options)

  var _this = this

  this.html = $('<div class="popmenu"><div class="arrow arrow' + this.options.arrow_dir + '"></div><div class="popmenubody"></div></div>')

  if (this.options.content != null) {
    $('.popmenubody', this.html).append(this.options.content)
  }
  else if (this.options.items != null) {
    $('.popmenubody', this.html).append('<ul class="popmenulist"></ul>')
    this.options.items.forEach(function(v){
      var li = $('<li>')
      li.html(v)
      $('ul', _this.html).append(li)
    })
  }

  

  //$('body').append(this.html)
  
  this.mouseentercd = null
  this.mouseleavecd = null

  this.options.target.on('mouseenter', function(){
    //console.info(111)
    try{
      clearTimeout(_this.mouseleavecd)
    }
    catch(error){
    }
    
    _this.mouseentercd = setTimeout(function(){
      _this.show()
      _this.options.onHover()
    }, _this.options.delay);
  })

  this.options.target.on('mouseleave', function(){
    //console.info(222)
    try{
      clearTimeout(_this.mouseentercd)
    }
    catch(error){
    }
    
    _this.mouseleavecd = setTimeout(function(){
      _this.close()
      _this.options.onOut()
    }, _this.options.outdelay);
  })

  this.html.on('mouseenter', function(){
    clearTimeout(_this.mouseleavecd)
  })

  this.html.on('mouseleave', function(){
    clearTimeout(_this.mouseentercd)
    _this.mouseleavecd = setTimeout(function(){
      _this.close()      
    }, _this.options.outdelay);
  })  
}



popmenu.prototype.show = function(){
  $('body').append(this.html)
  if (this.html.is(":visible")) {
    return false
  }
  //console.info(this.options.target)
  //console.info(this.options.target.length)
  var offset = this.options.target.offset()
  //console.info(offset)
  if (offset.left == 0 && offset.top == 0) {
    return false
  }
  //console.info(offset)
  var hei = this.options.target.height()

  if (this.options.onMoveIn) {
    this.options.onMoveIn()
  }
  

  this.html.css({
    top: offset.top + hei + 15,
    left: offset.left + this.options.offsetx
  }).fadeIn(100)
}

popmenu.prototype.close = function () {
  this.html.fadeOut(100, function(){
    //_this.html.remove()
  })
};


module.exports = popmenu




/***/ }),

/***/ "./modules/qqsj/index.js":
/*!*******************************!*\
  !*** ./modules/qqsj/index.js ***!
  \*******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 全球时间
 */
var dateformat = __webpack_require__(/*! dateformat */ "./node_modules/dateformat/lib/dateformat.js")
var boxsize = __webpack_require__(/*! ../boxsize */ "./modules/boxsize/index.js")
var localstorage = __webpack_require__(/*! ../localstorage */ "./modules/localstorage/index.js")

dateformat.i18n = {
    dayNames: [
        '日', '一', '二', '三', '四', '五', '六',
        '星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'
    ],
    monthNames: [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
        'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
    ],
    timeNames: [
        'a', 'p', 'am', 'pm', 'A', 'P', 'AM', 'PM'
    ]
};

function setTime(time){
  $('#time_bj').text(moment(time).format('MM-DD HH:mm:ss'))
  $('#time_ld').text(moment(time).tz('Europe/London').format('MM-DD HH:mm:ss'))
  $('#time_ny').text(moment(time).tz('America/New_York').format('MM-DD HH:mm:ss'))
}


module.exports = function(){
  $.ajax({
    url: '//cmsjs.eastmoney.com/TimeZone/Default.aspx?type=utctime&ids=41,2,78,53&jn=emutc',
    type: 'GET',
    dataType: 'script'
  })
  .done(function() {   
    if (window.emutc) {
      setTime(emutc.UTCTIME)
      setInterval(function(){
        emutc.UTCTIME = emutc.UTCTIME + 1000
        setTime(emutc.UTCTIME)
      }, 1000);
    }
  })
  .fail(function(error) {
    
  }) 

  setInterval(function(){
    $('#localtime').text(dateformat(new Date(), 'yyyy年m月d日 dddd HH:MM:ss'))
  }, 1000);

  //展开缩起
  $('#qqsj_zk').click(function(){
    if ($('#qqsj').is('.qqsj_short')) {
      $('#qqsj_zk span:first').show()
      $('#qqsj_zk span:last').hide()
      $('#qqsj').removeClass('qqsj_short')
      localstorage.set('qqsj_zk', 'open')
    }
    else{
      $('#qqsj_zk span:first').hide()
      $('#qqsj_zk span:last').show()
      $('#qqsj').addClass('qqsj_short')
      localstorage.set('qqsj_zk', 'close')
    }
    boxsize.resize()
  })
  
  if (localstorage.get('qqsj_zk') == 'close') {
    // console.info(222)
      $('#qqsj_zk span:first').hide()
      $('#qqsj_zk span:last').show()
      $('#qqsj').addClass('qqsj_short')    
  }

  
}

/***/ }),

/***/ "./modules/quote/index.js":
/*!********************************!*\
  !*** ./modules/quote/index.js ***!
  \********************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * 行情相关
 */

module.exports = {
  /**
   * 获取股票基本信息
   */
  getStockBaseInfo: function(code, fields){
    var fields_str = 'f1,f2,f3,f4,f12,f14'
    if (fields) {
      fields_str = fields
    }

    return $.ajax({
      url: '//push2.eastmoney.com/api/qt/ulist.np/get?cb=?&fields=' + fields_str,
      type: 'GET',
      dataType: 'json',
      data: {
        ut: '6d2ffaa6a585d612eda28417681d58fb',
        secids: code
      }
    })
    .then(function(json) {   
      if (json.rc == 0) {
        if (json.data.diff.length == 1) {
          return json.data.diff[0]
        } 
        else{
          return json.data.diff
        }
      }
    })
  },
  /**
   * 获取股票市场和分类
   * @param {*} code 
   */
  getStockTypeInfo: function(code){
    var fields_str = 'f12,f13,f14,f29'

    return $.ajax({
      url: '//push2.eastmoney.com/api/qt/ulist.np/get?cb=?&fields=' + fields_str + '&secids=' + code,
      type: 'GET',
      dataType: 'json',
      data: {
        ut: '6d2ffaa6a585d612eda28417681d58fb'
      }
    })
    .then(function(json) {   
      if (json.rc == 0) {
        if (json.data.diff.length == 1) {
          return json.data.diff[0]
        } 
        else{
          return json.data.diff
        }
      }
    })
  }
}

/***/ }),

/***/ "./modules/quote_ts/ie_sse_polyfill.js":
/*!*********************************************!*\
  !*** ./modules/quote_ts/ie_sse_polyfill.js ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/*
   * EventSource polyfill version 0.9.7
   * Supported by sc AmvTek srl
   * :email: devel@amvtek.com
 */
;(function (global) {

    if (global.EventSource && !global._eventSourceImportPrefix){
        return;
    }

    var evsImportName = (global._eventSourceImportPrefix||'')+"EventSource";

    var EventSource = function (url, options) {

        if (!url || typeof url != 'string') {
            throw new SyntaxError('Not enough arguments');
        }

        this.URL = url;
        this.setOptions(options);
        var evs = this;
        setTimeout(function(){evs.poll()}, 0);
    };

    EventSource.prototype = {

        CONNECTING: 0,

        OPEN: 1,

        CLOSED: 2,

        defaultOptions: {

            loggingEnabled: false,

            loggingPrefix: "eventsource",

            interval: 500, // milliseconds

            bufferSizeLimit: 256*1024, // bytes

            silentTimeout: 300000, // milliseconds

            getArgs:{
                'evs_buffer_size_limit': 256*1024
            },

            xhrHeaders:{
                'Accept': 'text/event-stream',
                'Cache-Control': 'no-cache',
                'X-Requested-With': 'XMLHttpRequest'
            }
        },

        setOptions: function(options){

            var defaults = this.defaultOptions;
            var option;

            // set all default options...
            for (option in defaults){

                if ( defaults.hasOwnProperty(option) ){
                    this[option] = defaults[option];
                }
            }

            // override with what is in options
            for (option in options){

                if (option in defaults && options.hasOwnProperty(option)){
                    this[option] = options[option];
                }
            }

            // if getArgs option is enabled
            // ensure evs_buffer_size_limit corresponds to bufferSizeLimit
            if (this.getArgs && this.bufferSizeLimit) {

                this.getArgs['evs_buffer_size_limit'] = this.bufferSizeLimit;
            }

            // if console is not available, force loggingEnabled to false
            if (typeof console === "undefined" || typeof console.log === "undefined") {

                this.loggingEnabled = false;
            }
        },

        log: function(message) {

            if (this.loggingEnabled) {

                console.log("[" + this.loggingPrefix +"]:" + message)
            }
        },

        poll: function() {

            try {

                if (this.readyState == this.CLOSED) {
                    return;
                }

                this.cleanup();
                this.readyState = this.CONNECTING;
                this.cursor = 0;
                this.cache = '';
                this._xhr = new this.XHR(this);
                this.resetNoActivityTimer();

            }
            catch (e) {

                // in an attempt to silence the errors
                this.log('There were errors inside the pool try-catch');
                this.dispatchEvent('error', { type: 'error', data: e.message });
            }
        },

        pollAgain: function (interval) {

            // schedule poll to be called after interval milliseconds
            var evs = this;
            evs.readyState = evs.CONNECTING;
            evs.dispatchEvent('error', {
                type: 'error',
                data: "Reconnecting "
            });
            this._pollTimer = setTimeout(function(){evs.poll()}, interval||0);
        },


        cleanup: function() {

            this.log('evs cleaning up')

            if (this._pollTimer){
                clearInterval(this._pollTimer);
                this._pollTimer = null;
            }

            if (this._noActivityTimer){
                clearInterval(this._noActivityTimer);
                this._noActivityTimer = null;
            }

            if (this._xhr){
                this._xhr.abort();
                this._xhr = null;
            }
        },

        resetNoActivityTimer: function(){

            if (this.silentTimeout){

                if (this._noActivityTimer){
                    clearInterval(this._noActivityTimer);
                }
                var evs = this;
                this._noActivityTimer = setTimeout(
                        function(){ evs.log('Timeout! silentTImeout:'+evs.silentTimeout); evs.pollAgain(); },
                        this.silentTimeout
                        );
            }
        },

        close: function () {

            this.readyState = this.CLOSED;
            this.log('Closing connection. readyState: '+this.readyState);
            this.cleanup();
        },

        _onxhrdata: function() {

            var request = this._xhr;

            if (request.isReady() && !request.hasError() ) {
                // reset the timer, as we have activity
                this.resetNoActivityTimer();

                // move this EventSource to OPEN state...
                if (this.readyState == this.CONNECTING) {
                    this.readyState = this.OPEN;
                    this.dispatchEvent('open', { type: 'open' });
                }

                var buffer = request.getBuffer();

                if (buffer.length > this.bufferSizeLimit) {
                    this.log('buffer.length > this.bufferSizeLimit');
                    this.pollAgain();
                }

                if (this.cursor == 0 && buffer.length > 0){

                    // skip byte order mark \uFEFF character if it starts the stream
                    if (buffer.substring(0,1) == '\uFEFF'){
                        this.cursor = 1;
                    }
                }

                var lastMessageIndex = this.lastMessageIndex(buffer);
                if (lastMessageIndex[0] >= this.cursor){

                    var newcursor = lastMessageIndex[1];
                    var toparse = buffer.substring(this.cursor, newcursor);
                    this.parseStream(toparse);
                    this.cursor = newcursor;
                }

                // if request is finished, reopen the connection
                if (request.isDone()) {
                    this.log('request.isDone(). reopening the connection');
                    this.pollAgain(this.interval);
                }
            }
            else if (this.readyState !== this.CLOSED) {

                this.log('this.readyState !== this.CLOSED');
                this.pollAgain(this.interval);

                //MV: Unsure why an error was previously dispatched
            }
        },

        parseStream: function(chunk) {

            // normalize line separators (\r\n,\r,\n) to \n
            // remove white spaces that may precede \n
            chunk = this.cache + this.normalizeToLF(chunk);

            var events = chunk.split('\n\n');

            var i, j, eventType, datas, line, retry;

            for (i=0; i < (events.length - 1); i++) {

                eventType = 'message';
                datas = [];
                parts = events[i].split('\n');

                for (j=0; j < parts.length; j++) {

                    line = this.trimWhiteSpace(parts[j]);

                    if (line.indexOf('event') == 0) {

                        eventType = line.replace(/event:?\s*/, '');
                    }
                    else if (line.indexOf('retry') == 0) {

                        retry = parseInt(line.replace(/retry:?\s*/, ''));
                        if(!isNaN(retry)) {
                            this.interval = retry;
                        }
                    }
                    else if (line.indexOf('data') == 0) {

                        datas.push(line.replace(/data:?\s*/, ''));
                    }
                    else if (line.indexOf('id:') == 0) {

                        this.lastEventId = line.replace(/id:?\s*/, '');
                    }
                    else if (line.indexOf('id') == 0) { // this resets the id

                        this.lastEventId = null;
                    }
                }

                if (datas.length) {
                    // dispatch a new event
                    var event = new MessageEvent(eventType, datas.join('\n'), window.location.origin, this.lastEventId);
                    this.dispatchEvent(eventType, event);
                }
            }

            this.cache = events[events.length - 1];
        },

        dispatchEvent: function (type, event) {
            var handlers = this['_' + type + 'Handlers'];

            if (handlers) {

                for (var i = 0; i < handlers.length; i++) {
                    handlers[i].call(this, event);
                }
            }

            if (this['on' + type]) {
                this['on' + type].call(this, event);
            }

        },

        addEventListener: function (type, handler) {
            if (!this['_' + type + 'Handlers']) {
                this['_' + type + 'Handlers'] = [];
            }

            this['_' + type + 'Handlers'].push(handler);
        },

        removeEventListener: function (type, handler) {
            var handlers = this['_' + type + 'Handlers'];
            if (!handlers) {
                return;
            }
            for (var i = handlers.length - 1; i >= 0; --i) {
                if (handlers[i] === handler) {
                    handlers.splice(i, 1);
                    break;
                }
            }
        },

        _pollTimer: null,

        _noactivityTimer: null,

        _xhr: null,

        lastEventId: null,

        cache: '',

        cursor: 0,

        onerror: null,

        onmessage: null,

        onopen: null,

        readyState: 0,

        // ===================================================================
        // helpers functions
        // those are attached to prototype to ease reuse and testing...

        urlWithParams: function (baseURL, params) {

            var encodedArgs = [];

            if (params){

                var key, urlarg;
                var urlize = encodeURIComponent;

                for (key in params){
                    if (params.hasOwnProperty(key)) {
                        urlarg = urlize(key)+'='+urlize(params[key]);
                        encodedArgs.push(urlarg);
                    }
                }
            }

            if (encodedArgs.length > 0){

                if (baseURL.indexOf('?') == -1)
                    return baseURL + '?' + encodedArgs.join('&');
                return baseURL + '&' + encodedArgs.join('&');
            }
            return baseURL;
        },

        lastMessageIndex: function(text) {

            var ln2 =text.lastIndexOf('\n\n');
            var lr2 = text.lastIndexOf('\r\r');
            var lrln2 = text.lastIndexOf('\r\n\r\n');

            if (lrln2 > Math.max(ln2, lr2)) {
                return [lrln2, lrln2+4];
            }
            return [Math.max(ln2, lr2), Math.max(ln2, lr2) + 2]
        },

        trimWhiteSpace: function(str) {
            // to remove whitespaces left and right of string

            var reTrim = /^(\s|\u00A0)+|(\s|\u00A0)+$/g;
            return str.replace(reTrim, '');
        },

        normalizeToLF: function(str) {

            // replace \r and \r\n with \n
            return str.replace(/\r\n|\r/g, '\n');
        }

    };

    if (!isOldIE()){

        EventSource.isPolyfill = "XHR";

        // EventSource will send request using XMLHttpRequest
        EventSource.prototype.XHR = function(evs) {

            request = new XMLHttpRequest();
            this._request = request;
            evs._xhr = this;

            // set handlers
            request.onreadystatechange = function(){
                if (request.readyState > 1 && evs.readyState != evs.CLOSED) {
                    if (request.status == 200 || (request.status>=300 && request.status<400)){
                        evs._onxhrdata();
                    }
                    else {
                        request._failed = true;
                        evs.readyState = evs.CLOSED;
                        evs.dispatchEvent('error', {
                            type: 'error',
                            data: "The server responded with "+request.status
                        });
                        evs.close();
                    }
                }
            };

            request.onprogress = function () {
            };

            var fullurl = evs.urlWithParams(evs.URL, evs.getArgs)
            var posturl = fullurl.substring(0, fullurl.indexOf('?'))
            var search = fullurl.substring(fullurl.indexOf('?') + 1)

            request.open('POST', posturl, true);

            var headers = evs.xhrHeaders; // maybe null
            for (var header in headers) {
                if (headers.hasOwnProperty(header)){
                    request.setRequestHeader(header, headers[header]);
                }
            }
            if (evs.lastEventId) {
                request.setRequestHeader('Last-Event-Id', evs.lastEventId);
            }
            request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            //console.info(111)
            request.send(encodeURI(search));
            //console.info(222)
        };

        EventSource.prototype.XHR.prototype = {

            useXDomainRequest: false,

            _request: null,

            _failed: false, // true if we have had errors...

            isReady: function() {


                return this._request.readyState >= 2;
            },

            isDone: function() {

                return (this._request.readyState == 4);
            },

            hasError: function() {

                return (this._failed || (this._request.status >= 400));
            },

            getBuffer: function() {

                var rv = '';
                try {
                    rv = this._request.responseText || '';
                }
                catch (e){}
                return rv;
            },

            abort: function() {

                if ( this._request ) {
                    this._request.abort();
                }
            }
        };
    }
    else {

	EventSource.isPolyfill = "IE_8-9";

        // patch EventSource defaultOptions
        var defaults = EventSource.prototype.defaultOptions;
        defaults.xhrHeaders = null; // no headers will be sent
        defaults.getArgs['evs_preamble'] = 2048 + 8;

        // EventSource will send request using Internet Explorer XDomainRequest
        EventSource.prototype.XHR = function(evs) {

            request = new XDomainRequest();
            this._request = request;

            // set handlers
            request.onprogress = function(){
                request._ready = true;
                evs._onxhrdata();
            };

            request.onload = function(){
                this._loaded = true;
                evs._onxhrdata();
            };

            request.onerror = function(){
                this._failed = true;
                evs.readyState = evs.CLOSED;
                evs.dispatchEvent('error', {
                    type: 'error',
                    data: "XDomainRequest error"
                });
            };

            request.ontimeout = function(){
                this._failed = true;
                evs.readyState = evs.CLOSED;
                evs.dispatchEvent('error', {
                    type: 'error',
                    data: "XDomainRequest timed out"
                });
            };

            // XDomainRequest does not allow setting custom headers
            // If EventSource has enabled the use of GET arguments
            // we add parameters to URL so that server can adapt the stream...
            var reqGetArgs = {};
            if (evs.getArgs) {

                // copy evs.getArgs in reqGetArgs
                var defaultArgs = evs.getArgs;
                    for (var key in defaultArgs) {
                        if (defaultArgs.hasOwnProperty(key)){
                            reqGetArgs[key] = defaultArgs[key];
                        }
                    }
                if (evs.lastEventId){
                    reqGetArgs['evs_last_event_id'] = evs.lastEventId;
                }
            }
            // send the request


            // var fullurl = evs.urlWithParams(evs.URL, evs.getArgs)
            // var posturl = fullurl.substring(0, fullurl.indexOf('?')).replace('https://','http://')
            // var search = fullurl.substring(fullurl.indexOf('?') + 1)

            // console.info(111)
            // console.info(posturl)
            // console.info(search)

            // request.open('POST', posturl);
            // request.send(search);

            // console.info(222)
            // console.info(evs.urlWithParams(evs.URL,reqGetArgs).replace('https://','http://'))

            request.open('GET', evs.urlWithParams(evs.URL,reqGetArgs).replace('https://','http://'));
            request.send();
        };

        EventSource.prototype.XHR.prototype = {

            useXDomainRequest: true,

            _request: null,

            _ready: false, // true when progress events are dispatched

            _loaded: false, // true when request has been loaded

            _failed: false, // true if when request is in error

            isReady: function() {

                return this._request._ready;
            },

            isDone: function() {

                return this._request._loaded;
            },

            hasError: function() {

                return this._request._failed;
            },

            getBuffer: function() {

                var rv = '';
                try {
                    rv = this._request.responseText || '';
                }
                catch (e){}
                return rv;
            },

            abort: function() {

                if ( this._request){
                    this._request.abort();
                }
            }
        };
    }

    function MessageEvent(type, data, origin, lastEventId) {

        this.bubbles = false;
        this.cancelBubble = false;
        this.cancelable = false;
        this.data = data || null;
        this.origin = origin || '';
        this.lastEventId = lastEventId || '';
        this.type = type || 'message';
    }

    function isOldIE () {

        //return true if we are in IE8 or IE9
        return (window.XDomainRequest && (window.XMLHttpRequest && new XMLHttpRequest().responseType === undefined)) ? true : false;
    }

    global[evsImportName] = EventSource;
})(window);

/***/ }),

/***/ "./modules/quote_ts/index.js":
/*!***********************************!*\
  !*** ./modules/quote_ts/index.js ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 行情推送
 */
var ts = __webpack_require__(/*! ./ts.js */ "./modules/quote_ts/ts.js")
var datacache = __webpack_require__(/*! ../datacache */ "./modules/datacache/index.js")
var webconfig = __webpack_require__(/*! ../../config/webconfig */ "./config/webconfig.js")
var modalalert = __webpack_require__(/*! ../modal/alert */ "./modules/modal/alert.js")
var hegui = __webpack_require__(/*! ../hegui */ "./modules/hegui/index.js")
var ykyl = __webpack_require__(/*! ../zxg/ykyl */ "./modules/zxg/ykyl.js")

var qts = null

module.exports = {
  bindCodes : function(stocklist, fields, callback, failcallback){
    if (hegui.isHKDelay()) {
      stocklist = hegui.dealHKStock(stocklist)
    }
    
    var count = stocklist.length
    if (stocklist instanceof Array) {
      stocklist = stocklist.join(',')
    }

    if (qts != null) {
      qts.close()
    }

    var pxstr = ''
    var postr = '&po=1'
    if (datacache.pxorder && datacache.pxtype.substring(0,1) == 'f') { //行情接口排序
      pxstr = '&fid=' + datacache.pxtype
      if (datacache.pxorder == 'asc') {
        postr = '&po=0'
      }

    }

    // console.info(222)
    var refeshtime = datacache.refreshtime
    qts = new ts({
      subUrl: webconfig.getWebPath('quotepath') + 'api/qt/ulist/sse?invt=3&pi=0&pz=' + count + '&mpi=' + refeshtime + '&secids=' + stocklist + '&ut=6d2ffaa6a585d612eda28417681d58fb&fields=' + fields.join(',') + postr + pxstr, //
      callback: function(data){
        //console.info(data)
        if (data.rc == 0) {
          // if (data.rc == 0 && data.lt == 2 && window.sessionStorage && sessionStorage.getItem('hkalert') == null) { //
          //   modalalert('应港交所要求，海外IP用户（中国大陆内地<br>以外地区）只可免费访问港股的BMP行情，<br>该行情需用户手动刷新获取实时数据，给您<br>带来的不便敬请谅解。')
          //   sessionStorage.setItem('hkalert', '1')
          // }

          if (data.data != null) {
            if (hegui.isHKDelay() && data.data.diff) {
              Object.keys(data.data.diff).forEach(function(v){
                if (data.data.diff[v].f13 == 128) {
                  data.data.diff[v].f13 = 116
                }
              })
            }
            // console.info(data)
            callback(data)
          }
          //console.info(data)
          // if (data.rc == 0 && data.data.mv) {
          //   console.info(data)
          // }
          
        }
        else{
          //console.info(11111)
          if (failcallback) {
            failcallback()
          }
        }
      }
    });
  },
  /**
   * get获取全量数据
   * @param {*} stocklist 
   * @param {*} fields 
   * @param {*} callback 
   * @param {*} failcallback 
   */
  bindCodesGet: function(stocklist, fields, callback, failcallback){
    //console.info('get请求')
    var count = stocklist.length
    if (stocklist instanceof Array) {
      stocklist = stocklist.join(',')
    }

    var pxstr = ''
    var postr = '&po=1'
    if (datacache.pxorder) {
      pxstr = '&fid=' + datacache.pxtype
      if (datacache.pxorder == 'asc') {
        postr = '&po=0'
      }

    }

    $.ajax({
      url: webconfig.getWebPath('getpath') + 'api/qt/ulist/get?cb=?&invt=3&pi=0&pz=' + count + '&mpi=2000&secids=' + stocklist + '&ut=6d2ffaa6a585d612eda28417681d58fb&fields=' + fields.join(',') + postr + pxstr,
      type: 'GET',
      dataType: 'json',
      data: {
        
      }
    })
    .done(function(json) {   
      //console.info(json)
      callback(json)
    })
    .fail(function(error) {
      if (failcallback) {
        failcallback()
      }
    })


    // qts = new ts({
    //   subUrl: , //
    //   callback: function(data){
    //     console.info(data)
    //     if (data.rc == 0) {
    //       if (data.data != null) {
    //         callback(data)
    //       }
    //       //console.info(data)
    //       // if (data.rc == 0 && data.data.mv) {
    //       //   console.info(data)
    //       // }
          
    //     }
    //     else{
    //       //console.info(11111)
    //       if (failcallback) {
    //         failcallback()
    //       }
    //     }
    //   }
    // });
  },
  close: function(){
    try{
      qts.close()
    }
    catch(error){
      //console.error(error)
    }
  },
  bindCodesLite : function(stocklist, fields, callback, failcallback){
    if (hegui.isHKDelay()) {
      stocklist = hegui.dealHKStock(stocklist)
    }

    var count = stocklist.length
    if (stocklist instanceof Array) {
      stocklist = stocklist.join(',')
    }


    var pxstr = ''
    var postr = '&po=1'
    if (datacache.pxorder && ykyl.allowpx.indexOf(datacache.pxtype) < 0 && ykyl.allquotepx.indexOf(datacache.pxtype) < 0) {
      pxstr = '&fid=' + datacache.pxtype
      if (datacache.pxorder == 'asc') {
        postr = '&po=0'
      }

    }
    // console.info(222)
    $.ajax({
      url: webconfig.getWebPath('getpath') + 'api/qt/ulist/get?cb=?&invt=3&pi=0&pz=' + count + '&mpi=2000&secids=' + stocklist + '&ut=6d2ffaa6a585d612eda28417681d58fb&fields=' + fields.join(',') + postr + pxstr,
      type: 'GET',
      dataType: 'json',
      data: {
        
      }
    })
    .done(function(data) {   
        if (data.rc == 0) {
          if (data.data != null) {
            if (hegui.isHKDelay() && data.data.diff) {
              Object.keys(data.data.diff).forEach(function(v){
                if (data.data.diff[v].f13 == 128) {
                  data.data.diff[v].f13 = 116
                }
              })
            }
            callback(data)
          }
          //console.info(data)
          // if (data.rc == 0 && data.data.mv) {
          //   console.info(data)
          // }
          
        }
        else{
          //console.info(11111)
          if (failcallback) {
            failcallback()
          }
        }
    })
    .fail(function(error) {
      
    })

    // qts = new ts({
    //   subUrl: webconfig.getWebPath('quotepath') + 'api/qt/ulist/sse?invt=3&pi=0&pz=' + count + '&mpi=2000&secids=' + stocklist + '&ut=6d2ffaa6a585d612eda28417681d58fb&fields=' + fields.join(',') + postr + pxstr, //
    //   callback: function(data){
    //     //console.info(data)
    //     if (data.rc == 0) {
    //       if (data.data != null) {
    //         callback(data)
    //       }
    //       //console.info(data)
    //       // if (data.rc == 0 && data.data.mv) {
    //       //   console.info(data)
    //       // }
          
    //     }
    //     else{
    //       //console.info(11111)
    //       if (failcallback) {
    //         failcallback()
    //       }
    //     }
    //   }
    // });
  }
  
}

/***/ }),

/***/ "./modules/quote_ts/ts.js":
/*!********************************!*\
  !*** ./modules/quote_ts/ts.js ***!
  \********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(/*! ./ie_sse_polyfill */ "./modules/quote_ts/ie_sse_polyfill.js")

function ts(options) {
  var _this = this
  var default_options = {}
  this.options = $.extend(default_options, options)
  if (typeof (EventSource) !== "undefined") {
    this.eventsource = new EventSource(this.options.subUrl)
    this.eventsource.onmessage = function(e){
      _this.options.callback(JSON.parse(e.data))
    }
  }

}

ts.prototype.close = function(){
  if (typeof (EventSource) !== "undefined") {
    this.eventsource.close()
  }  
}


module.exports = ts

/***/ }),

/***/ "./modules/radar_chart/index.js":
/*!**************************************!*\
  !*** ./modules/radar_chart/index.js ***!
  \**************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * 雷达图
 */

module.exports = function (ele, data) {
  //console.log(data)

  var width = 232;
  var height = 176;
  // var width = 480;
  // var height = 420;
  //console.log(width);



  var mColorPolygon = '#B8B8B8'; //多边形颜色
  var mCount = 5;
  var mCenter = width / 2;
  var mcenterY = height / 2;
  var mRadius = mCenter - 50; //去除文本的位置,根据横坐标作为正五边形的边长
  var mangle = Math.PI * 2 / mCount;

  var redcolor = 'rgba(236, 101, 28, 1)';
  var redcolor2 = 'rgba(86, 156, 249, 1)';

  var areacolor = 'rgba(236, 101, 28, 0.3)';
  var areacolor2 = 'rgba(163, 204, 255, 0.3)';

  var arr1 = data[0].value;
  var arr2 = data[1].value;

  var fotterColor = 'rgba(234, 85, 4, 1)';
  var fotterColor2 = 'rgba(86, 156, 249, 1)';

  var font = "12px sans-serif";
  var fontsize = 12;
  var fontcolor = '#666666';


  var footer_height = height * 0.92;

  var fontwidth = 59; //6个字或者以上 宽度肯定大于60，需要换行
  var everywidth = 40; //如果需要換行，則每一行的宽度

  // var pointradius = width / 45;

  var specialangle = 54 * Math.PI / 180;


  //初始化
  (function init() {
    var dongcai_leida = document.createElement('canvas');
    ele.appendChild(dongcai_leida);

    dongcai_leida.height = height;
    dongcai_leida.width = width;

    var ctx = dongcai_leida.getContext("2d");
    //ctx.rotate(30*Math.PI/180);
    //console.log(ctx);

    myBgkcolor(ctx);
    mdrawPolygon(ctx);
    mdrawLines(ctx);
    mdrawText(ctx);

    //画2018年数据
    mdrawArea(ctx, redcolor, areacolor, arr1);
    mdrawArcPoint(ctx, redcolor, arr1);

    //画2017年数据
    mdrawArea(ctx, redcolor2, areacolor2, arr2);
    mdrawArcPoint(ctx, redcolor2, arr2);

    mdrawFooter(ctx, fotterColor, font);


  })();


  //设置背景颜色
  function myBgkcolor(ctx) {
    ctx.save();
    ctx.fillStyle = 'white';

    var danwei = mRadius / mCount;

    //填充最外面背景颜色
    for (var i = 4; i < mCount; i++) {
      var mmdanwei = danwei * (1 + i);

      ctx.beginPath();
      //6条边
      for (var j = 0; j < mCount; j++) {

        var mmangle = mangle * j + specialangle;
        //console.log(mmangle);

        var x = mCenter + mmdanwei * Math.cos(mmangle);
        var y = mcenterY + mmdanwei * Math.sin(mmangle);

        ctx.lineTo(x, y);

      }
      //6条边结束

      ctx.closePath();
      ctx.fill();

    }


    ctx.restore();
  }


  //6个圈
  function mdrawPolygon(ctx) {

    ctx.save();
    ctx.strokeStyle = mColorPolygon;

    var danwei = mRadius / mCount;

    //填充最外面背景颜色


    //6个圈
    for (var i = 0; i < mCount; i++) {
      var mmdanwei = danwei * (1 + i);

      ctx.beginPath();
      //6条边
      for (var j = 0; j < mCount; j++) {

        var mmangle = mangle * j + specialangle;
        //console.log(mmangle);

        var x = mCenter + mmdanwei * Math.cos(mmangle);
        var y = mcenterY + mmdanwei * Math.sin(mmangle);

        // console.log(x);
        // console.log('-------------');
        // console.log(y);

        ctx.lineTo(x, y);

      }
      //6条边结束

      ctx.closePath();

      ctx.stroke();



    }

    ctx.restore();

  }


  //6条线
  function mdrawLines(ctx) {

    ctx.save();

    ctx.strokeStyle = mColorPolygon;

    ctx.beginPath();
    //画6条线

    for (var i = 0; i < mCount; i++) {

      var mmangle = mangle * i + specialangle;
      ctx.moveTo(mCenter, mcenterY);
      var x = mCenter + mRadius * Math.cos(mmangle);
      var y = mcenterY + mRadius * Math.sin(mmangle);
      ctx.lineTo(x, y);

    }

    ctx.closePath();
    ctx.stroke();

    ctx.restore();

  }


  //边上的字
  function mdrawText(ctx) {

    ctx.save();
    ctx.fillStyle = '#666666';
    ctx.font = "12px sans-serif";
    var fontsize = 12;

    //填充文字
    for (var i = 0; i < mCount; i++) {

      var mmangle = mangle * i + specialangle;

      var x = mCenter + mRadius * Math.cos(mmangle);
      var y = mcenterY + mRadius * Math.sin(mmangle);

      //console.log(ctx.measureText(data[0].item[i].width));


      //当字都少于6个字的时候
      if (ctx.measureText(data[0].item[i]).width <= fontwidth) {

        if (mmangle >= 0 && mmangle < Math.PI / 2) {
          ctx.fillText(data[0].item[i], x + 5, y);
        }

        if (mmangle >= Math.PI / 2 && mmangle < Math.PI) {
          ctx.fillText(data[0].item[i], x - ctx.measureText(data[0].item[i]).width - 3, y);

          // drawText(ctx, data[0].item[i], x - ctx.measureText(data[0].item[i]).width + 55, y - 30, 40);

        }


        if (mmangle >= Math.PI && mmangle < Math.PI * 5 / 4) {
          ctx.fillText(data[0].item[i], x - ctx.measureText(data[0].item[i]).width - 2, y + 5);
        }


        if (mmangle >= Math.PI * 5 / 4 && mmangle <= Math.PI * 3 / 2) {
          ctx.fillText(data[0].item[i], x - ctx.measureText(data[0].item[i]).width / 2, y - 2);
        }

        if (mmangle >= Math.PI * 7 / 4 && mmangle <= Math.PI * 2) {
          ctx.fillText(data[0].item[i], x + 2, y + 5);
        }


      } else {

        if (mmangle >= 0 && mmangle < Math.PI / 2) {
          // ctx.fillText(data[0].item[i], x + 5, y);
          drawText(ctx, data[0].item[i], x + 10, y - 30, everywidth, 'left');
        }

        if (mmangle >= Math.PI / 2 && mmangle < Math.PI) {
          //ctx.fillText(data[0].item[i], x - ctx.measureText(data[0].item[i]).width - 3, y);

          drawText(ctx, data[0].item[i], x - ctx.measureText(data[0].item[i]).width + 60, y - 30, everywidth, 'right');

        }


        if (mmangle >= Math.PI && mmangle < Math.PI * 5 / 4) {
          //ctx.fillText(data[0].item[i], x - ctx.measureText(data[0].item[i]).width - 2, y + 5);
          drawText(ctx, data[0].item[i], x - 2, y - 14, everywidth, 'right');
        }


        if (mmangle >= Math.PI * 5 / 4 && mmangle <= Math.PI * 3 / 2) {
          ctx.fillText(data[0].item[i], x - ctx.measureText(data[0].item[i]).width / 2, y - 2, 'right');
        }

        if (mmangle >= Math.PI * 7 / 4 && mmangle <= Math.PI * 2) {
          // ctx.fillText(data[0].item[i], x + 2, y + 5);
          drawText(ctx, data[0].item[i], x + 5, y - 10, everywidth, 'left');
        }

      }




    }

    ctx.restore();

  }



  //底部标记
  function mdrawFooter(ctx) {

    ctx.save();
    ctx.fillStyle = fontcolor;
    ctx.font = font;
    var fontsize = fontsize;

    //red圆点
    ctx.beginPath();
    ctx.arc(width / 2 - width / 48 - ctx.measureText(data[0].name).width - ctx.measureText(data[0].name).width / 10, footer_height, 5, 0, Math.PI * 2);
    ctx.fillStyle = fotterColor;
    ctx.fill();

    ctx.closePath();


    ///字
    ctx.fillStyle = fontcolor;
    ctx.font = font;
    var fontsize = fontsize;
    ctx.fillText(data[0].name, width / 2 - width / 48 - ctx.measureText(data[0].name).width, footer_height + 4);


    //blue圆点
    ctx.beginPath();
    ctx.arc(width / 2 + width / 48 * 2, footer_height, 5, 0, Math.PI * 2);
    ctx.fillStyle = fotterColor2;
    ctx.fill();

    ctx.closePath();


    ///字
    ctx.fillStyle = fontcolor;
    ctx.font = font;
    var fontsize = fontsize;
    ctx.fillText(data[1].name, width / 2 + width / 48 * 2 + ctx.measureText(data[1].name).width / 10, footer_height + 4);





    ctx.restore();



  }



  //当一行字超过一定宽度的时候，将字换行
  function drawText(ctx, t, x, y, w, di) {

    ctx.save();

    ctx.textAlign = di;

    var chr = t.split("");
    var temp = "";
    var row = [];

    for (var a = 0; a < chr.length; a++) {
      if (ctx.measureText(temp).width < w) {
        // console.log('if')
        //  console.log(w)
        // console.log(ctx.measureText(temp).width)
        ;
      } else {
        //console.log('else')
        row.push(temp);
        temp = "";
      }
      temp += chr[a];
    }

    row.push(temp);

    for (var b = 0; b < row.length; b++) {
      ctx.fillText(row[b], x, y + (b + 1) * 15);
    }



    ctx.restore();
  }



  //填充区域
  function mdrawArea(ctx, color, areacolor, arr) {

    ctx.save();

    ctx.beginPath();
    for (var i = 0; i < mCount; i++) {

      var mmangle = mangle * i + specialangle;

      var x = mCenter + mRadius * Math.cos(mmangle) * arr[i];

      var y = mcenterY + mRadius * Math.sin(mmangle) * arr[i];

      // console.log(x);
      // console.log('-------------');
      // console.log(y);

      ctx.lineTo(x, y);

    }

    ctx.closePath();

    ctx.fillStyle = areacolor;
    ctx.fill();

    ctx.strokeStyle = color;
    ctx.stroke();

    ctx.restore();
  }



  //画小圆点
  function mdrawArcPoint(ctx, color, arr) {
    ctx.save();

    for (var i = 0; i < mCount; i++) {

      var mmangle = mangle * i + specialangle;

      var x = mCenter + mRadius * Math.cos(mmangle) * arr[i];

      var y = mcenterY + mRadius * Math.sin(mmangle) * arr[i];

      ctx.beginPath();
      ctx.arc(x, y, 3, 0, Math.PI * 2);
      ctx.fillStyle = 'white';
      ctx.fill();


      ctx.strokeStyle = color;
      ctx.stroke();
      ctx.closePath();

    }

    ctx.restore();

  }


}

/***/ }),

/***/ "./modules/sessionstorage/index.js":
/*!*****************************************!*\
  !*** ./modules/sessionstorage/index.js ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * sessionStorage
 */

module.exports = {
  save: function(key, value){
    if (window.sessionStorage) {
      sessionStorage.setItem(key, value)
    }
  },
  get: function(key){
    if (window.sessionStorage) {
      return sessionStorage.getItem(key)
    }
    return null
  }
}

/***/ }),

/***/ "./modules/stock_filter/filter.html":
/*!******************************************!*\
  !*** ./modules/stock_filter/filter.html ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<ul class=\"stock_filter\" id=\"stock_filter\">\r\n  {{~it.typelist :value:index}}\r\n  <li>\r\n    <label><input type=\"radio\" value=\"{{=value.type}}\"> {{=value.name}}</label>\r\n  </li>\r\n  {{~}}\r\n</ul>"

/***/ }),

/***/ "./modules/stock_filter/index.js":
/*!***************************************!*\
  !*** ./modules/stock_filter/index.js ***!
  \***************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 类型筛选
 */
var filter_html = __webpack_require__(/*! ./filter.html */ "./modules/stock_filter/filter.html")
var dot = __webpack_require__(/*! dot */ "./node_modules/dot/doT.js")
var popmenu = __webpack_require__(/*! ../popmenu */ "./modules/popmenu/index.js")
var datacache = __webpack_require__(/*! ../datacache */ "./modules/datacache/index.js")

module.exports = {
  init: function(){
    this.bind()
  },
  typelist: [{
      name: '全部',
      type: 'all'
    },
    {
      name: '沪深 ',
      type: 'hs'
    },
    {
      name: '港股',
      type: 'hk'
    },
    {
      name: '美股',
      type: 'us'
    },
    {
      name: '英股',
      type: 'uk'
    },    
    {
      name: '期货',
      type: 'qh'
    },
    {
      name: '基金',
      type: 'fund'
    },
    {
      name: '外汇',
      type: 'wh'
    },
    {
      name: '债券',
      type: 'zq'
    },
    {
      name: '期权',
      type: 'qq'
    }  
  ],
  getTypeName: function(type){
    if(!type){
      return this.typelist[0]
    }
    return this.typelist.find(function(item){
      return item.type == type
    })
  },
  bind: function(){
    var allstock = $('#allstock') 

    $('#wl_mainbody').on('click', '#clickall', function(){

      var batchselect = $('.batchselect') 
      if (batchselect.prop('checked')) {
        batchselect.prop('checked', false)
        $('#tablethd7 .allstock input').prop('checked', false)
        $('#clickall').prop('checked', false)
      }
      else{
        batchselect.prop('checked', true)
        $('#tablethd7 .allstock input').prop('checked', true)
        $('#clickall').prop('checked', true)
      }
      //return false
    })

    $('#wl_mainbody').on('click', '.batchselect', function(){

      var batchselect = $('.batchselect') 

      var allselect = true

      batchselect.each(function(i, v){
        if ($(v).prop('checked') == false) {
          allselect = false
        }
      })


      if (allselect) {
        $('#clickall').prop('checked', true)
      }
      else{
        $('#clickall').prop('checked', false)
      }
      //return false
    })    

    var filterhtml = $(dot.template(filter_html)({
      typelist: this.typelist
    }))
    $('input:radio:first', filterhtml).prop('checked', true)
    var newpop = new popmenu({
      target: allstock,
      //offsetx: -35,
      content: filterhtml
    })

    $('input', filterhtml).on('change', function(){
      var thisinput = $(this)
      $('input', filterhtml).prop('checked', false)
      thisinput.prop('checked', true)
      var stocktype = $(this).val()
      datacache.stocktype = stocktype
      if (stocktype == 'all') {
        datacache.stocktype = null
      }
      datacache.changeGroup(datacache.thisgroupid)
      return false
    })
  },
  filterCode: function(codelist, quote_type, codetype){
    //console.info(codelist)
    //console.info(quote_type)
    //console.info(codetype)
    return codelist.filter(function(v, i){
      


      // if (v.split('.')[0] != quote_type[i]) {
        
      // }

      var quote_item = quote_type.find(function(v2){
        return v2.f12 == v.split('.')[1]
      })

      if (quote_item == undefined) {
        return false
      }

      var market = quote_item.f13
      var type = quote_item.f29
      if (codetype == 'all') {
        return true
      }
      else if(codetype == 'hs'){
        return (market == 0 || market == 1) && type == 1
      }
      else if(codetype == 'hk'){
        return market == 116 && type == 1
      }
      else if(codetype == 'us'){
        return (market == 105 || market == 106 || market == 107) && ( type == 1 || type == 512 )
      }
      else if(codetype == 'uk'){
        return (market == 155 || market == 156 )
      }
      else if(codetype == 'qh'){
        return type == 16
      }  
      else if(codetype == 'fund'){
        return type == 8
      }  
      else if(codetype == 'wh'){
        return type == 128
      }        
      else if(codetype == 'zq'){
        return type == 4
      }           
      else if(codetype == 'qq'){
        return type == 32
      }   
      
            
    })
  }
}

/***/ }),

/***/ "./modules/tabs/index.js":
/*!*******************************!*\
  !*** ./modules/tabs/index.js ***!
  \*******************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * tabs切换
 */


var tabs = (function () {

	function tabs(options) {
		var defaultoptions = {
            tabsobj: null, //tab
			parent: null, //父级元素 用于on绑定
			child: null, //子级元素 用于on绑定
            type: 'display', //切换类型 display: 控制contents数组元素的显示和隐藏 switch: 通过switchCallback控制contents元素的内容
            contents: [], //内容obj数组
            cdtime: 150, //鼠标悬停时间 毫秒
            switchCallback: function (index, content){ //切换内容回调函数 index当前tab的序号 content 当前的contents
            	
            }
        }
        this.options = $.extend(defaultoptions, options);
        this.cd = null; //悬停计时
	}

	/**
	 * 初始化
	 * @return {[type]} [description]
	 */
	tabs.prototype.init = function () {	
		this.bind();
	};

	/**
	 * 绑定事件
	 * @return {[type]} [description]
	 */
	tabs.prototype.bind = function (){
		var _this = this;
		
		if (this.options.parent != null && this.options.child != null) {
			this.options.parent.on("mouseover", this.options.child, function(){
				_this.showContent($(this));
			});
			this.options.parent.on("mouseout", this.options.child, function(){
				clearTimeout(_this.cd);
			});	
			
			return false;
		}

		this.options.tabsobj.on("mouseover",function (){
			_this.showContent($(this));
		});
		this.options.tabsobj.on("mouseout", function (){
			clearTimeout(_this.cd);
		});

	};

	/**
	 * 显示内容
	 * @param  {[type]} thisobj [description]
	 * @return {[type]}         [description]
	 */
	tabs.prototype.showContent = function (thisobj){
		var _this = this;
		var index = thisobj.index();
		this.cd = setTimeout(function (){
			
			if (_this.options.parent != null && _this.options.child != null) {
				$(_this.options.child, _this.options.parent).removeClass('on');
			}
			else{
				_this.options.tabsobj.removeClass('on');
			}
			
			thisobj.addClass('on');

			if ( _this.options.type == 'display' ) {
				_this.options.contents.hide();
				_this.options.contents.eq(index).show();	
			}
			
			_this.options.switchCallback(index, _this.options.contents);
		}, this.options.cdtime);
	};

	return tabs;
})();

module.exports = tabs;


/***/ }),

/***/ "./modules/text/index.js":
/*!*******************************!*\
  !*** ./modules/text/index.js ***!
  \*******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 文本处理
 */

var datacache = __webpack_require__(/*! ../datacache */ "./modules/datacache/index.js")

var text = {
  className: function(num){
    if (num > 0) {
      return 'stockup'
    }
    else if(num < 0){
      return 'stockdown'
    }
    return ''
  },
  textColor: function(text, num){
    if (num == null || num == undefined || isNaN(num)) {
      return text
    }
    if (num > 0) {
      return '<span class="stockup">' + text + '</span>'
    }
    else if (num < 0) {
      return '<span class="stockdown">' + text + '</span>'
    }    
    else{
      return text
    }
  },
  textNumColor: function(num, fixed){
    var text = ''
    if (num == null || num == undefined || isNaN(num)) {
      return text
    }
    else{
      num = num / 1
      if (fixed) {
        text = num.toFixed(fixed)
      }
      else{
        text = num.toString()
      }
    }

    if (num > 0) {
      return '<span class="stockup">' + text + '</span>'
    }
    else if (num < 0) {
      return '<span class="stockdown">' + text + '</span>'
    }    
    else{
      return text
    }
  },
  textNumColorPlus: function(num, fixed){
    var text = ''
    if (num == null || num == undefined || isNaN(num)) {
      return text
    }
    else{
      num = num / 1
      if (fixed) {
        text = num.toFixed(fixed)
      }
      else{
        text = num.toString()
      }
    }

    if (num > 0) {
      return '<span class="stockup">+' + text + '</span>'
    }
    else if (num < 0) {
      return '<span class="stockdown">' + text + '</span>'
    }    
    else{
      return text
    }
  },
  formatNum: function(num){
    if(num == 0) {
      return num
    }
    if(num == undefined || num == '' || isNaN(num)){
      return '';
    }

    var hz = '';
    if(num >= 100000000||num <= -100000000){
      num = num / 100000000;
      hz = '亿';
    }
    else if(num >= 10000||num <= -10000){
      num = num / 10000;
      hz = '万';
    }
    else{
      return num;
    }

    var num2 = num.toFixed(2);

    // if(parseInt(num) >= 1000){ //整数部分超过4位
    //   num2 = num.toFixed(1);
    // }

    return num2.toString() + hz;
  },
  /**
   * 是否是沪深股票
   * @param {*} f13 
   * @param {*} f19 
   */
  isHSStock: function(f13, f19){
    return (f13 == 1 && f19 == 2) || ((f13 == 0) && (f19 == 6 || f19 == 13 || f19 == 80))
  },
  /**
   * 通过代码判断是否是沪深A股
   * @param {*} code 
   */
  isHSStockByCode: function(code){
    var codearray = code.split('.')
    if (codearray.length < 2) {
      return false
    }
    var market = codearray[0]
    var codestr = codearray[1]
    if(market == 1 && codestr[0] == '6'){ //上证A股
      return true
    } 
    if(market == 0 && (codestr[0] == '0' && codestr[1] == '0' && codestr[2] == '2')){//中小板
      return true  
    } 
    if( market == 0 && (codestr[0] == '0' && codestr[1] == '0') ){ //深证A股
      return true
    } 
    if( market == 0 && (codestr[0] == '3' && codestr[1] == '0') ){ //创业板
      return true
    } 
    
    return false
  },
  /**
   * 通过代码获取行情链接
   * @param {*} code 
   */
  getLinkByCode: function(code){
    if (datacache.islite == true) {
      return 'http://quote.eastmoney.com/unify/r/' + code
    }
    if (text.isHSStockByCode(code)) {
      var codearray = code.split('.')
      var market = codearray[0]
      var codestr = codearray[1]
      var marketstr = 'sz'
      if (market == '1') {
        marketstr = 'sh'
      }
      return 'http://quote.eastmoney.com/concept/' + marketstr + codestr + '.html?from=zixuan'
    }
    return 'http://quote.eastmoney.com/unify/r/' + code
  },
  
    /**
   * 字符串截取 
   * 
   * @param {string} txt 输入文本
   * @param {int} n 截取多少个字 一个汉字算2个
   * @param {boolean} needtip 是否需要全文提示
   * @returns 
   */
  txtLeft: function (txt, n, needtip) {
    if( txt == null || txt == "" ){
      return "";
    }
    var thislength = 0;
    for (var i = 0; i < txt.length; i++) {
      if (txt.charCodeAt(i) > 255) {
        thislength += 2;
      }
      else {
        thislength++;
      }
      if (thislength > n + 3) {
        if(needtip){
          return '<span title="' + txt + '">' + txt.substring(0, i) + "...</span>";
        }
        else{
          return txt.substring(0, i) + "...";
        }
        break;
      }
    }
    return txt;
  },
    /**
   * 字符串截取  英文单独算 不把两个英文当一个中文
   * 
   * @param {string} txt 输入文本
   * @param {int} n 截取多少个字 一个汉字算2个
   * @param {boolean} needtip 是否需要全文提示
   * @returns 
   */
  txtLeftPure: function (txt, n, needtip) {
    if( txt == null || txt == "" ){
      return "";
    }
    var thislength = txt.length;
    var tip = needtip ? '...' : ''
    if (thislength > n) {
      return txt.substring(0, n) + tip
    }
    return txt
  }  

}

module.exports = text

/***/ }),

/***/ "./modules/tixing/addtixing.html":
/*!***************************************!*\
  !*** ./modules/tixing/addtixing.html ***!
  \***************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"stockalarmset\">\r\n  <form action=\"\" target=\"_self\">\r\n  <div class=\"sastitle\"><b>{{=it.name}}</b> {{=it.code}} &nbsp; 当前股价：<span class=\"{{? it.quotedata.f4 > 0 }}stockup{{?? it.quotedata.f4 < 0}}stockdown{{?}}\">{{=it.price}}</span></div>\r\n  <div class=\"sasaset\">\r\n    <div class=\"item\"><input type=\"checkbox\" {{? it.isinfo }}checked{{?}} id=\"sasi1\"><label for=\"sasi1\"> 当有最新公司公告、数据、研究报告时提醒</label></div>\r\n  </div>\r\n  <div class=\"sasalarm\">\r\n    <div class=\"sasalarmtitle\"> 股价预警</div>\r\n    <div class=\"sasaqr\"><img src=\"./images/tixingqr.png\" alt=\"\"></div>\r\n    <div class=\"item\">\r\n      <input type=\"checkbox\" {{? it.tixingdata.priceup }}checked{{?}} id=\"sasi4\">\r\n      <label for=\"sasi4\">股价突破</label>\r\n      <input type=\"text\" id=\"sasinum1\"\r\n        class=\"inty\" value=\"{{? it.tixingdata.priceup }}{{=it.tixingdata.priceup}}{{?}}\" > 元 <div id=\"sasinum1error\" class=\"stockup saserrtip\"></div></div>\r\n    <div class=\"item\">\r\n      <input type=\"checkbox\" {{? it.tixingdata.pricedown }}checked{{?}} id=\"sasi5\">\r\n      <label for=\"sasi5\"> 股价跌破</label>\r\n      <input type=\"text\" id=\"sasinum2\"\r\n        class=\"inty\" value=\"{{? it.tixingdata.pricedown }}{{=it.tixingdata.pricedown}}{{?}}\"> 元 <div id=\"sasinum2error\" class=\"stockup saserrtip\"></div></div>\r\n    <div class=\"item\">\r\n      <input type=\"checkbox\" id=\"sasi6\" {{? it.tixingdata.pricezf }}checked{{?}}>\r\n      <label for=\"sasi6\"> 日涨跌幅达到</label>\r\n      <input type=\"text\" id=\"sasinum3\"\r\n        class=\"inty\" value=\"{{? it.tixingdata.pricezf }}{{=it.tixingdata.pricezf}}{{?}}\"> ％ <div id=\"sasinum3error\" class=\"stockup saserrtip\"></div></div>\r\n  </div>\r\n  <div class=\"sasbtns\">\r\n    <a href=\"javascript:;\" target=\"_self\" id=\"sasclear\">清空</a>\r\n    <div class=\"modalbtnd\">\r\n      <button type=\"submit\" class=\"modalbtn_default modalbtn_default_button\">保 存</button> &nbsp; <a href=\"javascript:;\" target=\"_self\" class=\"modalbtn_cancel\">取\r\n        消</a>\r\n    </div>\r\n  </div>\r\n  </form>\r\n</div>"

/***/ }),

/***/ "./modules/tixing/addtixing.js":
/*!*************************************!*\
  !*** ./modules/tixing/addtixing.js ***!
  \*************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 加提醒
 */
var addtixing_html = __webpack_require__(/*! ./addtixing.html */ "./modules/tixing/addtixing.html")
var dot = __webpack_require__(/*! dot */ "./node_modules/dot/doT.js")
var user = __webpack_require__(/*! ../user */ "./modules/user/index.js")
var modalalert = __webpack_require__(/*! ../modal/alert */ "./modules/modal/alert.js")
var modal = __webpack_require__(/*! ../modal */ "./modules/modal/index.js")
var quote = __webpack_require__(/*! ../quote */ "./modules/quote/index.js")

module.exports = {
  //判断是否支持提醒功能
  hasTiXing: function(m, t){
    //沪深AB股 
    if ((m==0&&t==6) || (m==0&&t==13) || (m==0&&t==80) || (m==1&&t==2) || (m==0&&t==7) || (m==1&&t==3)){
      return true
    }
    //沪深板块
    if(m==90) return true    
    //沪深指数
    if((m==1&&t==1) || (m==0&&t==5)){
      return true
    }
    //沪深债券
    if((m==1&&t==4) || (m==0&&t==8)){
      return true
    }
    //场内基金
    if((m==1&&t==9) || (m==0&&t==10)){
      return true
    }
    //新三板   
    if(m==0&&t==81){
      return true
    }
    //港股(股票)
    if((m==116)&&(t==3||t==4)){
      return true
    }
    //美股(股票)
    if((m==105||m==106||m==107)&&(t==1||t==2||t==3)){
      return true
    }
    return false
  },
  /**
   * 转换码表至提醒的码表
   * @param {*} code 
   */
  toTiXingCode: function(code){
    return code.toString().replace('.', ',')
  },
  /**
   * 获取提醒数据
   * @param {*} code 
   */
  getTiXing: function(code){
    var _this = this
    var uid = user.get().id
    return $.ajax({
      url: '//userinfo.eastmoney.com/api/ZxgMsg/UserCfgGet?callback=?',
      type: 'GET',
      dataType: 'json',
      data: {
        a: uid,
        b: _this.toTiXingCode(code)
      }
    })
    .then(function(json) {   
      return json
    })
  },
  /**
   * 加提醒
   * @param {*} code 
   * @param {*} name 
   */
  add: function(code, name, onChangeOK){
    var _this = this
    if (user.get() == null) {
      modalalert('提醒功能要登录用户才能使用！')
      return false
    }    

    var _this = this

    Promise.all([
      this.getTiXing(code),
      quote.getStockBaseInfo(code)
    ])
    .then(function(backdata){
      var tixingdata = backdata[0]
      var quotedata = backdata[1]
      var nowprice = quotedata.f2 / (Math.pow(10, quotedata.f1))

      var html = $(dot.template(addtixing_html)({
        quotedata: quotedata,
        name: quotedata.f14,
        price: nowprice,
        code: quotedata.f12,
        tixingdata: tixingdata,
        isinfo: tixingdata.isdatainfo == "1" && tixingdata.isnoticeinfo == "1" && tixingdata.isreportinfo == "1"
      }))
      var newmodal = new modal({
        content: html,
        title: '提醒设置'
      })

      newmodal.show() 

      _this.bindSubmitForm($('form', html), code, newmodal, nowprice, onChangeOK)

      $('.modalbtn_cancel', html).click(function(){
        newmodal.close()
      })
    })
  },
  /**
   * 绑定提醒表单
   * @param {*} form 
   * @param {*} code 
   * @param {*} newmodal 
   */
  bindSubmitForm: function(form, code, newmodal, nowprice, onChangeOK){
    var _this = this

    var sasi1 = $('#sasi1', form)
    var sasi4 = $('#sasi4', form)
    var sasi5 = $('#sasi5', form)
    var sasi6 = $('#sasi6', form)
    var sasinum1 = $('#sasinum1', form)
    var sasinum2 = $('#sasinum2', form)
    var sasinum3 = $('#sasinum3', form)

    var sasinum1error = $('#sasinum1error')
    var sasinum2error = $('#sasinum2error')
    var sasinum3error = $('#sasinum3error')

    var sasinum1Type = true //记录股价突破异常
    var sasinum2Type = true //记录股价跌破异常
    var sasinum3Type = true //记录日涨跌幅异常



    sasi4.change(function () {
      if (!$(this).prop('checked')) {
        sasinum1.val('')
        sasinum1error.text('')
        sasinum1Type = true
      } else {
        sasinum1error.text("所填价格不能为空")
        sasinum1Type = false
      }
    })
    sasi5.change(function () {
      if (!$(this).prop('checked')) {
        sasinum2.val('')
        sasinum2error.text('')
        sasinum2Type = true
      } else {
        sasinum2error.text("所填价格不能为空")
        sasinum2Type = false
      }
    })

    sasi6.change(function () {
      if (!$(this).prop('checked')) {
        sasinum3.val('')
        sasinum3error.text('')
      } else {
        sasinum3error.text("所填日涨跌幅不能为空")
        sasinum3Type = false;
      }
    })

    sasinum1.bind('input propertychange', function () {
      var closed = nowprice //当前股价
      if (sasinum1.val() == "") {
        sasi4.prop('checked', false)
        sasinum1error.text('')
        sasinum1Type = true
        return
      } else {
        sasi4.prop('checked', true)
        sasinum1Type = true;
        sasinum1error.text('')
        // return;
      }
      if (isNaN(sasinum1.val())) {
        sasinum1error.text("必须输入数字")
        sasinum1.val("")
        sasi4.prop('checked', false)
        return
      }

      if (sasinum1.val() - closed < 0) {
        sasinum1error.text("所填价格不可小于现价")
        sasinum1Type = false
        return
      }

      if (sasinum1.val() - closed >= 0) {
        sasinum1error.text("此价格较现价的涨幅为" + (sasinum1.val() / closed * 100 - 100).toFixed(2) + "%")
        sasi4.prop('checked', true)
        sasinum1Type = true
        return
      }
    });


    sasinum2.bind('input propertychange', function () {
      var closed = nowprice
      if (sasinum2.val() == "") {
        sasi5.prop('checked', false)
        sasinum2error.text('')
        sasinum2Type = true
        return
      } else {
        sasi5.prop('checked', true)
        sasinum2Type = true
        sasinum2error.text('')
        // return;
      }
      if (isNaN(sasinum2.val())) {
        sasinum2error.text("必须输入数字")
        sasinum2.val("")
        sasi5.prop('checked', false)
        sasinum2Type = false
        return
      }
      if (sasinum2.val() - closed >= 0) {
        sasinum2error.text("所填价格不可大于现价")
        sasinum2Type = false
        return
      }
      if (sasinum2.val() - closed <= 0) {
        sasinum2error.text("此价格较现价的跌幅为" + ((sasinum2.val() - closed) / closed * 100).toFixed(2) + "%")
        sasi5.prop('checked', true)
        sasinum2Type = true
        return
      }
    });

    $('#sasinum3').bind('input propertychange', function () {
      if (sasinum3.val() == "") {
        sasi6.prop('checked', false)
        sasinum3error.text('')
        return
      } else {
        sasi6.prop('checked', true)
        sasinum3Type = true;
        sasinum3error.text('')
        // return;
      }
      if (isNaN(sasinum3.val())) {
        sasinum3error.text("必须输入数字")
        sasinum3.val('')
        sasi6.prop('checked', false)
        return
      }
    })

    //清空
    $('#sasclear', form).click(function(){
      sasi1.add(sasi4).add(sasi5).add(sasi6).prop({
        checked: false
      })
      sasinum1.add(sasinum2).add(sasinum3).val('')
      sasinum1error.add(sasinum2error).add(sasinum3error).text('')
      sasinum2Type = true
      sasinum1Type = true
      sasinum3Type = true
    })

    //提交
    var issubmit = false
    form.submit(function(){
      // console.info(sasinum2Type)
      // console.info(sasinum1Type)
      // console.info(sasinum3Type)
      if(sasinum2Type && sasinum1Type && sasinum3Type){

      }
      else{
        return false
      }


      var sasi1_val = sasi1.is(':checked')
      var sasinum1_val = sasinum1.val()
      var sasinum2_val = sasinum2.val()
      var sasinum3_val = sasinum3.val()

      if (issubmit) {
        return false
      }
      issubmit = true

      $.ajax({
        url: '//userinfo.eastmoney.com/api/ZxgMsg/UserCfgSet?callback=?',
        type: 'GET',
        dataType: 'jsonp',
        data: {
          a: user.get().id,
          b: _this.toTiXingCode(code),
          c: sasi1_val ? 1 : 2,
          d: sasi1_val ? 1 : 2,
          e: sasi1_val ? 1 : 2,
          f: sasinum1_val,
          g: sasinum2_val,
          h: sasinum3_val,
          i: '',
          j: '',
          k: ''
        }
      })
      .done(function(json) {   
        //if (json.re) {
          modalalert('修改成功', function(){
            if (onChangeOK) {
              onChangeOK()
            }
          })
        //}
        //else{
        //  modalalert(json.message)
        //}
      })
      .fail(function(error) {
        modalalert(error.statusText)
      })
      .always(function(){
        newmodal.close()
        issubmit = false
      }) 
      return false
    })
  },
  /**
   * 获取提醒消息
   * @param {*} code 
   */
  getTiXingMsg: function(){


    return $.ajax({
      url: '//userinfo.eastmoney.com/api/ZxgMsg/GetFlag?callback=?',
      type: 'GET',
      dataType: 'jsonp',
      data: {
        uid: user.get().id
      }
    })
    .then(function(json) {   
      return json.Data
    })
  },
  /**
   * 显示提醒小红点
   */
  showTiXingTip: function(){
    $('#tixingtopbtn').addClass('tixingon')
  },
  /**
   * 移除提醒小红点
   */
  removeTiXingTip: function(){
    $('#tixingtopbtn').removeClass('tixingon')
  },
  /**
   * 获取提醒tip
   */
  getTiXingTip: function(){
    if (user.get() == null) {
      return false
    }
    this.getTiXingMsg().then(function(v){
      if (v.price_alert || v.notice || v.report) {
        this.showTiXingTip()
      }
      else{
        this.removeTiXingTip()
      }
    }.bind(this))
  },
  tixingtip: null,
  /**
   * 开始定时获取提醒
   */
  startTiXingTip: function(){
    this.getTiXingTip()
    this.tixingtip = setInterval(function(){
      this.getTiXingTip()
    }.bind(this), 30 * 1000);
  },
  /**
   * 停止定时获取提醒
   */
  stopTiXingTip: function(){
    try{
      clearInterval(this.tixingtip)
    }
    catch(error){
    }
  },
  /**
   * 清除所有提醒
   */
  clearAllTip: function(){
    var _this = this
    $.ajax({
      url: '//userinfo.eastmoney.com/api/ZxgMsg/Clear?callback=?',
      type: 'GET',
      dataType: 'json',
      data: {
        uid: user.get().id,
        type: 'all'
      }
    })
    .done(function(json) {   
      _this.removeTiXingTip()
    })
    .fail(function(error) {
      
    })
  }
}

/***/ }),

/***/ "./modules/tixing/index.js":
/*!*********************************!*\
  !*** ./modules/tixing/index.js ***!
  \*********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 提醒列表
 */

var user = __webpack_require__(/*! ../user */ "./modules/user/index.js")
var modal = __webpack_require__(/*! ../modal */ "./modules/modal/index.js")
var modalalert = __webpack_require__(/*! ../modal/alert */ "./modules/modal/alert.js")
var tixing_html = __webpack_require__(/*! ./tixing.html */ "./modules/tixing/tixing.html")
var table_html = __webpack_require__(/*! ./tixing_table.html */ "./modules/tixing/tixing_table.html")
var dot = __webpack_require__(/*! dot */ "./node_modules/dot/doT.js")
var pager = __webpack_require__(/*! ../pager */ "./modules/pager/index.js")
var addtixing = __webpack_require__(/*! ./addtixing */ "./modules/tixing/addtixing.js")
var text = __webpack_require__(/*! ../text */ "./modules/text/index.js")

module.exports = {
  showList: function(type){
    if (!type) {
      type = 'price_alert'
    }
    var _this = this
    var thisuser = user.get()
    if (thisuser == null) {
      modalalert('只有登录用户才能设置提醒')
      return false
    }

    this.showType(type, 1)


  },
  showType: function(type, pageindex){
    var _this = this
    this.getData(type, pageindex)
    .done(function(json) {   

      //清除所有提醒
      addtixing.clearAllTip()

      var tabindex = 0
      var typename = ''
      switch (type) {
        case 'price_alert':
          tabindex = 0
          typename = '股价提醒'
          break;
        case 'notice':
          tabindex = 1
          typename = '公告提醒'
          break;      
        case 'report':
          tabindex = 2
          typename = '研报提醒'
          break;
      }

      var html = $(dot.template(tixing_html)({}))
      var table_html = _this.fillTable(json.msgs, pageindex, typename)

      $('.txtabled', html).html(table_html)

      var pager_html = $(pager(pageindex, 10, 10 * json.pageCount, 'javascript:;'))
      $('#tixingpager', html).html(pager_html)




      if ($('#tixingc').length <= 0) {
        var newmodal = _this.modal = new modal({
          content: html,
          showtitle: false
        })
 
        newmodal.show()        
      }
      else{
        $('#tixingc').replaceWith(html);
        try{
          _this.modal.resize()
        }
        catch(error){
        }
      }


      $('#tixingpager', html).on('click', 'a', function(){
        var gotopage = $(this).data('page')
        _this.showType(type, gotopage)
        return false
      })

      $('#changetype', html).on('click', 'li', function(){
        var type = $(this).data('type')
        _this.showType(type, 1)

      })

      $('#changetype li').removeClass('on')
      $('#changetype li').eq(tabindex).addClass('on')
    })
    .fail(function(error) {
      
    })    
  },
  getData: function(type, pageindex){
    return $.ajax({
      url: '//userinfo.eastmoney.com/api/ZxgMsg/Lst?type=' + type + '&key=' + user.get().id + '&p=' + pageindex + '&ps=10&callback=?',
      type: 'GET',
      dataType: 'jsonp',
      data: {
        
      }
    })
  },
  fillTable: function(data, pageindex, typename){
    if (!data || data.length <= 0) {
      return false
    }

    function dealStockName(stockName) {
      if (stockName.indexOf('(') > 0) {
        return stockName.substring(0, stockName.indexOf('('))
      }
      else{
        return stockName
      }
    }

    data.forEach(function(v, i){
      v.index = i + 10 * (pageindex - 1)
      v.code = v.value.stockCode.substring(v.value.stockCode.indexOf(',') + 1)
      v.market = v.value.stockCode.substring(0, 1)
      v.stocklink = text.getLinkByCode(v.value.stockCode.replace(',','.'))
      if (v.type == 'notice' || v.type == 'report') {
        v.link = 'http://guba.eastmoney.com/news,' + v.code + ',' + v.value.stockbarid + '.html'
      }
      else{
        v.link = ''
      }
      v.stockname = dealStockName(v.value.stockName)
    })

    return $(dot.template(table_html)({
      list: data,
      dealStockName: dealStockName,
      typename: typename
    }))

  }
}

/***/ }),

/***/ "./modules/tixing/tixing.html":
/*!************************************!*\
  !*** ./modules/tixing/tixing.html ***!
  \************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div id=\"tixingc\">\r\n  <div class=\"tixing\" id=\"tixing\">\r\n    <div class=\"tab2 tixingtab\">\r\n      <ul id=\"changetype\">\r\n        <li class=\"on\" data-type=\"price_alert\"><a href=\"javascript:;\" target=\"_self\">股价提醒</a></li>\r\n        <li data-type=\"notice\"><a href=\"javascript:;\" target=\"_self\">公告提醒</a></li>\r\n        <li data-type=\"report\"><a href=\"javascript:;\" target=\"_self\">研报提醒</a></li>\r\n      </ul>\r\n    </div>\r\n    <div class=\"txtabled\"></div>\r\n  </div>\r\n  <div class=\"pager\" id=\"tixingpager\"></div>\r\n</div>"

/***/ }),

/***/ "./modules/tixing/tixing_table.html":
/*!******************************************!*\
  !*** ./modules/tixing/tixing_table.html ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<table class=\"txtable\">\r\n  <tr>\r\n    <th>序号</th>\r\n    <th>日期</th>\r\n    <th>类型</th>\r\n    <th>内容</th>\r\n  </tr>\r\n  {{~it.list :value:index}}\r\n  <tr>\r\n    <td>{{= value.index + 1}}</td>\r\n    <td>{{=value.value.showtime.substring(5, 16)}}</td>\r\n    <td>{{=it.typename}}</td>\r\n    <td class=\"txtd\">【<a href=\"{{=value.stocklink}}\">{{=value.stockname}}</a>】\r\n    {{? value.link }}\r\n      <a href=\"{{=value.link}}\">{{=value.value.content}}</a>\r\n    {{??}}\r\n      {{=value.value.content}}\r\n    {{?}}\r\n    </td>\r\n  </tr>\r\n  {{~}}\r\n</table> "

/***/ }),

/***/ "./modules/trend_kline/index.js":
/*!**************************************!*\
  !*** ./modules/trend_kline/index.js ***!
  \**************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

(function webpackUniversalModuleDefinition(root, factory) {
	if(true)
		module.exports = factory();
	else {}
})(window, function() {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./index.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./index.js":
/*!******************!*\
  !*** ./index.js ***!
  \******************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 趋势研判K线图
 */

var candle = __webpack_require__(/*! ./modules/candle */ "./modules/candle.js")
var axis = __webpack_require__(/*! ./modules/axis */ "./modules/axis.js")
var average = __webpack_require__(/*! ./modules/average */ "./modules/average.js")
var imgbase64 = __webpack_require__(/*! ./modules/img */ "./modules/img.js")
var text = __webpack_require__(/*! ./modules/text */ "./modules/text.js")
var dealarray = __webpack_require__(/*! ./modules/dealarray */ "./modules/dealarray.js")
var int = __webpack_require__(/*! ./modules/int */ "./modules/int.js")
var canvas = __webpack_require__(/*! ./modules/canvas */ "./modules/canvas.js")

function qskline(options) {

  this.options = options;
  var ele = this.options.ele
  ele.innerHTML = ''

  var width = this.options.width
  var height = this.options.height
  var data = this.options.data
  var statdata = dealarray.deal(data)

  this.statdata = statdata
  //console.info(statdata)

  //console.info(max)
  //console.info(min) 

  var axis_canvas = canvas.new(ele, width, height)
  var axis_ctx = axis_canvas.getContext('2d')
  axis_ctx.translate(0,18)

  var watermark_canvas = canvas.new(ele, width, height)
  var watermark_ctx = watermark_canvas.getContext('2d')

  var k_canvas = canvas.new(ele, width, height)
  var k_ctx = k_canvas.getContext('2d'); 
   

  //文字层
  text(watermark_ctx, width, height, data, statdata)

  //水印
  var img = new Image();
  img.src = imgbase64.logo
  img.onload = function(){
    watermark_ctx.drawImage(img,width - 108,0 + 26, 100, 26)
  }
  
  //坐标层
  axis(axis_ctx, width, height)

  //K线
  k_ctx.translate(0,18) 
  candle(k_ctx, data, width, height, statdata)

  //均线
  average(k_ctx, data, width, height, statdata)
 

}

qskline.prototype.getPrice = function(){
  //console.info(this.statdata)
  return {
    yl:{
      price: this.statdata.yl.num,
      date: this.options.data[this.statdata.yl.index].d
    },
    zc: {
      price: this.statdata.zc.num,
      data: this.options.data[this.statdata.zc.index].d
    }
  }
}

// qskline.prototype.methodName = function () {
//   return "Hello, " + this.par;
// };

module.exports = qskline


/***/ }),

/***/ "./modules/average.js":
/*!****************************!*\
  !*** ./modules/average.js ***!
  \****************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 均线
 */

var int = __webpack_require__(/*! ./int */ "./modules/int.js")

module.exports = function(ctx, data, width, height, statdata){
  var min = statdata.num_min
  var max = statdata.num_max
  var mheight = height - (18 * 2)
  var dpp = (max - min) / mheight

  ctx.strokeStyle = '#5a85ff'
  ctx.beginPath()

  var xs = width / data.length
  
  data.forEach(function(v, i){
    var y = int.int(mheight - ((v.d5 - min) / dpp))
    if (i == 0) {
      ctx.moveTo(xs / 2, y)
    }
    else if(i == data.length - 1){
      ctx.lineTo(int.int(xs * i + xs / 2), y)
      ctx.stroke()   
    }
    else{
      ctx.lineTo(int.int(xs * i + xs / 2), y)
    }

  })

  ctx.strokeStyle = '#ff10ff'
  ctx.beginPath()
  data.forEach(function(v, i){
    var y = int.int(mheight - ((v.d20 - min) / dpp))
    if (i == 0) {
      ctx.moveTo(xs / 2, y)
    }
    else if(i == data.length - 1){
      ctx.lineTo(int.int(xs * i + xs / 2), y)
      ctx.stroke()   
    }
    else{
      ctx.lineTo(int.int(xs * i + xs / 2), y)
    }

  })

  ctx.strokeStyle = '#018101'
  ctx.beginPath()
  data.forEach(function(v, i){
    var y = int.int(mheight - ((v.d60 - min) / dpp))
    if (i == 0) {
      ctx.moveTo(xs / 2, y)
    }
    else if(i == data.length - 1){
      ctx.lineTo(int.int(xs * i + xs / 2), y)
      ctx.stroke()   
    }
    else{
      ctx.lineTo(int.int(xs * i + xs / 2), y)
    }

  })  
}

/***/ }),

/***/ "./modules/axis.js":
/*!*************************!*\
  !*** ./modules/axis.js ***!
  \*************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 坐标轴
 */

var int = __webpack_require__(/*! ./int */ "./modules/int.js")

module.exports = function(ctx, width, height){
    ctx.fillStyle = '#fff'
  ctx.fillRect(0, 0, width, height - (18 * 2));


  var mheight = height - (18 * 2)

  for (var i = 0; i < 5; i++) {
    ctx.beginPath()

    ctx.moveTo(0, int.int(mheight*i/4))

    if (i>0 && i< 4) {
      ctx.strokeStyle = '#dcdcdc'
      ctx.setLineDash([4, 4]);
    }
    else{
      ctx.strokeStyle = '#dcdcdc'
      ctx.setLineDash([0,0]);
    }
    ctx.lineWidth = 1


    ctx.lineTo(width, int.int(mheight*i/4))
    ctx.stroke()    
    
  }



  for (var i = 0; i < 5; i++) {
    
    ctx.beginPath()

    var x = int.int(width*i/4)

    ctx.moveTo(x, 0)

    if (i>0 && i< 4) {
      ctx.strokeStyle = '#dcdcdc'
      ctx.setLineDash([4, 4]);
    }
    else{
      ctx.strokeStyle = '#dcdcdc'
      ctx.setLineDash([0,0]);
    }
    ctx.lineWidth = 1


    ctx.lineTo(x, mheight)
    ctx.stroke()    
    
  }

  
  // ctx.moveTo(0, 300)
  // ctx.lineTo(500, 300)
  // ctx.stroke()




  
}

/***/ }),

/***/ "./modules/candle.js":
/*!***************************!*\
  !*** ./modules/candle.js ***!
  \***************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 蜡烛
 */
var int = __webpack_require__(/*! ./int */ "./modules/int.js")
var imgbase64 = __webpack_require__(/*! ./img */ "./modules/img.js")

function candleOne(ctx, data, dpp){
  //ctx.save()
  var color = '#ff0000'

  if (data.c < data.o) {
    color = '#008000'
  } else if (data.c == data.o) {
    color = '#666'
  }

  ctx.fillStyle = color;
  ctx.strokeStyle = color;

  ctx.beginPath();
  ctx.moveTo(data.x, data.y);
  ctx.lineTo(data.x, data.y + (data.h - data.l) / dpp);
  ctx.stroke();

  ctx.lineWidth = 1

  var boxh = (data.c - data.o) / dpp
  if (boxh == 0) {
    boxh = 1
  }
  //console.info(boxh)

  if (color == '#008000') {
    

    ctx.fillRect(data.x - data.w / 2 , data.y + (data.h - data.c) / dpp , data.w, boxh);
  } else {
    ctx.fillRect(data.x - (data.w / 2), data.y + (data.h - data.c) / dpp, data.w, boxh);

    //ctx.fillStyle = '#fff'
    //ctx.fillRect(data.x - (data.w / 2) + 0.5, data.y + (data.h - data.c) / dpp + 0.5, data.w - 1, (data.c - data.o) / dpp - 1);
  }



  //ctx.restore()  
}

module.exports = function (ctx, data, width, height, statdata) {
  var xs = width / data.length
  var barw = xs * 0.75
  var mheight = height - (18 * 2)
  var max = statdata.num_max
  var min = statdata.num_min
  var dpp = (max - min) / mheight
  var zc = statdata.zc
  var yl = statdata.yl


  
  data.forEach(function(v, i){
    candleOne(ctx, {
      x: int.int(xs / 2 + i * xs),
      y: int.int(mheight - (v.h - min) / dpp),
      w: barw,
      c: v.c,
      o: v.o,
      h: v.h,
      l: v.l,
    }, dpp)  
    if (i == zc.index) {
      var ylimg = new Image();
      ylimg.src = imgbase64.zc
      ylimg.onload = function(){
        var x = int.int(xs / 2 + i * xs)
        var y = int.int(mheight - (v.h - min) / dpp) + (v.h - v.l) / dpp
        ctx.drawImage(ylimg,  x - 5, y, 9 ,12)
        ctx.beginPath();
        ctx.moveTo(x, y + 1);
        ctx.lineTo(x - 50, y + 1);
        ctx.strokeStyle = '#f87101'
        ctx.setLineDash([3, 2])
        ctx.stroke();
        ctx.font="12px Arial";
        ctx.fillStyle = '#f87101'
        ctx.fillText(zc.num, x - 50 , y - 3);

      }
    }
    if (i == yl.index) {
      var ylimg = new Image();
      ylimg.src = imgbase64.yl
      ylimg.onload = function(){
        var x = int.int(xs / 2 + i * xs)
        var y = int.int(mheight - (v.h - min) / dpp)
        ctx.drawImage(ylimg, x - 5, y - 12, 9 ,12)
        ctx.beginPath();
        ctx.moveTo(x, y + 1);
        ctx.lineTo(x - 50, y + 1);
        ctx.strokeStyle = '#31a0ff'
        ctx.setLineDash([3, 2])
        ctx.stroke();
        ctx.font="12px Arial";
        ctx.fillStyle = '#31a0ff'
        ctx.fillText(yl.num, x - 50 , y - 3);

      }
    }
    
  })

}

/***/ }),

/***/ "./modules/canvas.js":
/*!***************************!*\
  !*** ./modules/canvas.js ***!
  \***************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * canvas相关
 */

module.exports = {
  new: function(element, width, height){
    var new_canvas = document.createElement('canvas');
    new_canvas.width = width
    new_canvas.height = height
    element.appendChild(new_canvas)
    return new_canvas
  }
}

/***/ }),

/***/ "./modules/dealarray.js":
/*!******************************!*\
  !*** ./modules/dealarray.js ***!
  \******************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * 处理数组
 */

module.exports = {
  deal: function(array){
    var max = array[0].h
    var min = array[0].l
    var zcmin = array[array.length - 1].l
    var zcindex = array.length - 1
    var ylmax = array[array.length - 1].h
    var ylindex = array.length - 1
    var num_max = array[0].h
    var num_min = array[0].l
    array.forEach(function(v, i){
      //最大值
      var maxi = Math.max(v.h, v.d5, v.d20, v.d60 )
      if (maxi >= num_max) {
        num_max = maxi
      }
      //最小值
      var mini = Math.min(v.l, v.d5, v.d20, v.d60 )
      if (mini <= num_min) {
        num_min = mini
      }      


      if (v.h >= max) {
        max = v.h
      }
      if (min >= v.l) {
        min = v.l
      }
      if (i > array.length - 20 && zcmin >= v.l) {
        zcmin = v.l
        zcindex = i
      }
      if (i > array.length - 22 && v.h >= ylmax ) {
        ylmax = v.h  
        ylindex = i       
      }
    })
  
    return {
      max: max,
      min: min,
      num_max: num_max,
      num_min: num_min,
      zc: {
        num: zcmin,
        index: zcindex
      },
      yl: {
        num: ylmax,
        index: ylindex
      }
    }
    
    // return max
    // return min
    // return {
    //   num: min,
    //   index: index
    // }
  }
  // getMax: function(array){
  //   var max = array[0].High
  //   array.forEach(function(v){
  //     if (v.High >= max) {
  //       max = v.High
  //     }
  //   })
  //   return max
  // },
  // getMin: function(array){
  //   var min = array[0].Low
  //   array.forEach(function(v){
  //     if (min >= v.Low) {
  //       min = v.Low
  //     }
  //   })
  //   return min
  // },
  // getZC: function(array){
  //   var min = array[array.length - 1].Low
  //   var index = array.length - 1
  //   array.forEach(function(v, i){
  //     if (i > array.length - 19 && min >= v.Low) {
  //       min = v.Low
  //       index = i
  //     }
  //   })
  //   return {
  //     num: min,
  //     index: index
  //   }
  // },
  // getYL: function(array){
  //   var max = array[array.length - 1].High
  //   var index = array.length - 1
  //   array.forEach(function(v, i){
  //     if (i > array.length - 21 && v.High >= max ) {
  //       max = v.High  
  //       index = i       
  //     }
  //   })
  //   return {
  //     num: max,
  //     index: index
  //   }
  // },
  
  // date: function(date){
  //   return date.substring(0, date.indexOf(' '))
  // }
}

/***/ }),

/***/ "./modules/img.js":
/*!************************!*\
  !*** ./modules/img.js ***!
  \************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * 水印
 */

module.exports = {
  logo: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUgAAABSCAYAAAA2Lk16AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyFpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNS1jMDE0IDc5LjE1MTQ4MSwgMjAxMy8wMy8xMy0xMjowOToxNSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIChXaW5kb3dzKSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDpEREJGMDUzQkZCQzUxMUU1OEY5M0QwOTQzOUVCOTg4QSIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDpEREJGMDUzQ0ZCQzUxMUU1OEY5M0QwOTQzOUVCOTg4QSI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOkREQkYwNTM5RkJDNTExRTU4RjkzRDA5NDM5RUI5ODhBIiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOkREQkYwNTNBRkJDNTExRTU4RjkzRDA5NDM5RUI5ODhBIi8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+TKYRegAAHUBJREFUeNrsXQlzGzey7uElniIlWZct2bItOxu/3fe26v3/n7Cvaispx4kTW5Zk66RO6iBFDh+RbWQgCOcMZkha6KqpxBQ5gwEaX3/daDSC4XAIXrx48eLloRSCIJi2Ns+OrqvRNfDD58WLlySiI4i5KXynudFVZf5d9sPsxYuXNGTaADI/uuZH1wzz2RP8zIsXL14eNUAuYZvzzGed0bUxuhp+OL148fJYAbI4upYZJknldnSRQOqr0VViPi/44fXixctjAcjnDDCykdUeA4jPmc9JrLLph9iLFy9xZVpY1uLoajH/ZlewQ+b/m/i9s9F1PLp+HF210fVtAt+pYRAWuBldp1OqW4TV1zXf6TIG7nuXmsZgH0B2mRlLmrl/jXPIA+QUtJGk9axzn6kU6RkOLmGZO6PrLfxnUWeLY57jDhe80vQ/aesvU+6dvNV8Zy9l40U8jmXB5/3RdYgGqo5grhPymyu84gLkquLvxxkCJOmTkuLvbQ+Q0wGQNQQSXoFvOabCSplhkZej6wKiVe7PExQu0PX9ITJIL8kAUgRKPdSbtRj3JIuCn0bXne/e2LKp8C5ORtc2/CeVj8zbiqEBi+fmRHngQ/RoyPieDYfDcNIBsongKIqTsgBZkrjk1ALuIwudR6XeHfN7LXDhApBM4D0/j1J1/5fQre0pwHUeHubZ1lEvf/XdmMi7yCv+thzTeLkQgh39EXB+HoHkxaQCpKqDupwrMiNxy4sIiJfIxCp43xt0IcYhJUG4QCRb4HcKpR3i+A11QyUEQP+GusODJGE41xm3u6pxjYm3FAqMQYFjYTpGltM8h5eBQ30tI4kgTO4I57vr0BiNj69ISCL57PUIJN9PGkCS9myAOpjdEbjhImlhB9OYyhrj3l5xLDQr2VBYTipHBhPXSzLpG/ZxyOkOr3dZA+QSgodMfkJGPINMqAnxdprN4WUjQ5xTV9hnnZjvWMM5sJ1yX5J2no+udxKDQYzEyiQBJNkR88zA7T8XWHOQsMgjJq6xxrw4AaoPDtmuibUl3zFJZg8MWWZcuQQfgA85xiIL44QgjzXmJ/TdSFjgBfNOLtkd++55gd5W8HqSAOQIwO9k1Fe3COSyeVmfBICsISDUDBX7nEN5GUCyL33HuNn0mYsMgCaRBYELltRQpC1+hTKSNxID9wsyxEDhhm5Yuo4qWWOAez+mh0P0+iXq+iHOlbQWk8j7vFa8F10HuIhhwLPMNumrQjHjBEgymE+R6ZnKKWf9WyBPdicWrsgoyAUHZKvoCoQJ3+MTqBPua3A/gV0mOwncEhu504Q4XIG9ySYEU1atk2sYT8x2weG9WJe2HRMgSUxtD6+0QYa07wDZqkxmpsBAKuOxhTE0poWxlHqM3x8K3AmdlaOA0IH7OXFFbMe+A0VRgcQrQ0Z3OAHKUkdWkCXAuAAZkwWXNOQPi+82Nd7BF4bNxE3vOnWgzzaiA+E45IMYzbcSI7jLzHsTT2uH6ctNgdHWGtWsALLMTIZizHtcwP2g+AzotxKyrpNI6WiqR1rWdt3AivYh/YC0DbvUud+zBuywo3FdsnSTJiVUUTLQ76S7ik4YvUtTyHOuUrp3D6IsFN4T+4pzdd7Q85jH38h2MZ2Ok0FWkC2Sq+rgft8E4KYTNpDcRYuW41jkHKNYLqVlYeUmJen4yoAV/bcBQH4DvxI/TllK+f7XKQIkkXPB3Mkh0F1ZhGWaCJAtxXNaWQFkHhs+i5fL+ANvsUqG4BMIGBLfricpAGRRE5thGciJYFADR6wlDTFZvfXneIxX0t6i2mNAKyuAJFK3fG4FMa6hYO2pAWQZmWEdr0pKnTWAh7tfVg07aShwxXiAbGA/uHTT1g36diBxrV9qQOhfY5x4gWG/h/C4JAB16CjrghxZ5WfqFljjsswLnLuBxfMuJUAow6ZrE8/NBCBzCIYVBER6ZVUqbZt7kSqYp8KEAoCUucPHjtrbBLMk212Yvv28+Zj9/r0LmR/vFH//v+/wnWs4F3sKkIu7GYPojyg/sa7QQTKffhR8/kyCVecmDSkILCFlhFUExXEu1Z9wLihp33OL3/cNXb9ZRwCZM2xfxyEge4Acv6gWYO4chhwIWeCTqOcZ9jrHPYs8+xT/Pgvuktsps/uKTCyNXWkXAoAMQLye0cF23AjYYlnhxlsBJAHFDZic3CXywl+4z5bALKHc1rWpO2rzU9CvVg4F7/W9AeRj20deysi9FhmeRZCHty5xzJ5DihVxEGw+Ox73C2R/ps+nvzEJ9d2Zuv8Fxm19A5NTYZy8wB+cQlQsOoxKV8DwRFJEJU+izDNgtnoYd5eEZ5CTK0WNLo+zXesIILcxmSwtdjGvmD8krLQKbitlXaMHaBIGZAFy2RB8jYQ+fG2CwJFYoY8cWNGEaxsr2BNYNNUEryYEyBWD9t1Btom8rqVgMamG+P0qPKwmo2PYdA/07ZSw0awYpK0Q9/J3U3dSI4SNvtTMnzTc7HmDeX7DtDE0wLJzG4WvwOScCNjHAeWTul+AfVWSG0tLn+R87QDMjp79OuXsyjTFh/THBvZJUteOHjtxBONLCE/CIMcJkB1H4Ahj8nouDebVOad7l6DfQGLFIFsTomRE+X8TANsKxDv3+koAYsWYLMAEOHRWizChE5huMQFIYgDIti5aDsyEBeYhWhTkhVaIIa7TFkxmoY1JZZDTLiZAdiYA1aYGF4y9EgKQ9QnoiFtkjnzMkKzKPYt5z46AIarYTJLFqRDEeVs8CNB40J2GjUJKrsxtQgabN/wOeb+fY4DDLIZS8pL7vkIj2pmwiTypAFnD+e2ivypjaH8PMWFGQTouLUHVqrpQAca/ak0a/EmA6g1NzEPn5l1ZDnCSpPkQ2aGu8MIiXknkxwS/TVrUIW+o1J8S6MI3kO8lpufIfIDJEZ33ME6A7CKbb6NnFmeRJgdRYReVXKeID4sK93ooCMn0FEbLSv8LCV3LpEImw57E8m1C/PhVR8CUagaKkES+ICg3UaHitl0H5EkO8ho4AAOTUEkSOQd1sYUa3C9jN24pagz1ONtJnk2qRD1P+TnnkN4ZSucKgDxVgOCCRP+t2HQB0s2PUlnVLQma10FcmshGziT3TRMgyWQ4guRFeP+pAaL3Y5xwJix74KAfdTIzQQA5o2FwaUtbQXK6qI8diCrkuJrvIUSnAKa5gCNbmR4q2KAMIC9sWfQ4CuaSHSS7kolEBvG1A7A6E1j5KniZBoAsGk7OSZFxA+SBwXduYHqPEB4qAFIGdjKDUY6j8LrFBVdCrMy2AvUJ4r9w0JYOPIz7zIKXrAAyqeSnrE/GDZDfu1QlekcAswHiNCbZKnYFLDeEFNDip6n4A4xPHEoQnwAiWaledvQ80ZGuc2McYN3CDDEYtocU6VKfSH+fjgkg+xk8Y5KSx7MGyBqo4+lt7J8Kfi+rDSA91GXXY6NK2WkJADKv6R+rugu0zFcaABli/GNfMWkImpOValepRuQ5J4J3nDVsb1oAqVp4iROz7IA6/WkxJYDMGY5B2i72JNWbLGcMkHRbn8rgPgN9snRa7jBx+b86vGdL87dtTh/mDO5nBZBdSLaLRNRJxwiMKipLXOp1xy7VngDoFgzd9jR2aVQ14DiMCWQdUOeHNcD9Sm+QUT9mzSCDhL9VZYGMY/fJM2zTgcLolzVAsq8xQnUQ774L0LsJwc2q9oxm/hSQLbIr07pNJQ009KGpMrrK0xogMB5oJiYZnOfgfnvjncQyLFq037XoBusyAaAQV+qpxgC53PdtepZQUiZuApCuGGRO8V5ET3W5fSUFwA5hPDmQRI9/0fRRywAgdfNhU8FSlw1A1kRMQmMtBiBNTslUxS6FX046iMRKkhjaT6AuAptD1+AdpLP3W8Qem2CeCO9amQPQJ463E9xft23R9fnaRYsJmjZAugqHqEI7q4YMR6VP4wgF7GX0XBXA5B15pXOW35lzeN97LnYcN/oMGZvJ1p0mmJ3wF1duJOxxxeIergFyXjPZB5BsX3EX5GXm6eRtgLvDs7IyNDqAdBkrXtJ4OibHCqvGZxwSTshzkobO6AkGOilBdJiXKfC1TN3sgmWc5ApZz6mha1hAdzrtVeRdgdVsgN3ij2uA1Ln2Jw6Uua1h44sOAdJ0L27SuKcOIIcO30e3kEEM7BaI42mXGg/hsaf4JE3Xs/GAFlDvTItp5/E3RybKqBvIK2Q6p5aDTlD6BaSfO3ciYbFPY4QKXEnNYLCOHDyHjMmaoo/nkPl1HQGKiWeRNoO0ceFphSgR+3li+M6EoXyT/P15iobiMUteMj59/Fsg8Nb6ChKxIDF+xybKGML9zd1EyTsIimcxFX4ZJ27aQjplRwLOtqlDLgFSl9PZATc7G0Ic5BWNG7mT8DmBYX92EzK8wDGDDCUMOm/BUFYloZAZjYs9rqrxbwz6SOf+/mAIYmnJCohTyg5BfORzXjIHKD7k4WG6UMlgnv6ljBeoTBcQ7X1MQo3XMlKGXYHlCGI8v+swdqNLoaAD7Up0AEnGYz8ho6kYToikFV2yWqBZAvME6ipOrjMBa1Gx3HMYj5gspunc35KDeyTRtXlJSGMfx60m8GgCgSHdwrEg/30LD2OaT3XeFVXILw4HJytwPAXxKvAK2C8GuSzVpHPte+C26GsXJ6MsnkazB7YTPMM0hpy07qAJCLtYJbfdtcWzyJyGge4IgDyrHS3vDbw+AvivFX//yaCfidu6kUL7q4L5cgjRTjzSrl9xTOYlBuESwyIdRmdIibxFHLcKA6rlpBbbRhYgm720PQmoz4DdyjWVK0ftqhmAyQG4T8M4AvWCwxNUsLhun2lF96SsySQ1JClArkh0lIaWGgYsckXCsgYIju2YzM5LtBBMPMMbic4O0HvcxX4tc6GNO8n4UqDNI1bkkdDUswLIrKqTy46Y3IhpqV0B5LoBsKsCw7mYBuYcWXBV4Q6RBYXfYty7Zehy0SIhLYi/J9ckqT9JbK8M8tSeIzRef5e4j5RFtiDKkaT1Hq/xnU9AvligW7Qbghc6vjYLmHcxwkcDxmvMZckgs7CSuxJXbjkmQA8dudgmZ3bvYBsvJRNiLsEkIvdWBdcbCEC2q+erht/bZxT2HxAt8pmAJTEKZIucyZ75uG48AT1ZtShaUKWPBmxRwyL/BQ/z6OZx/GhpsQEH/DXNuLra6jopp5NOg5RAnZ3RL0zZC52AuP5dnDOz2QmXNPBv8vxdnFzPMP5DV7Lp8bQqdsMyUNV77GhY7BrYraAvglmy7injXl/hu76AKL3ilnF9hhxozaDRMJnYslVp03epK8CdAtRXbLeoPc8gKvPP6wwZ2zfMM9hzinTvdu2QQS6A22IRccMh46jZWUSX+dzAMOdAX16x5xog08z9Ikr0RfKitmdms3KRsF2kD1UV0O8QMOjWwG9ouebBvk6lLhRwiBP9KYgXqnI4iT+APpA/Y2h0iCJucZ8d4wTZgCgQ7mLrmckeYdXEkbG3I45NnoI4d44asQMJIPyOxq9hyeRcnna5AlE8dagw6CqpawCupjHmAxhPgd47HDtadJvGMLvYppDRbZPQ0blrgCSNSaPMUheVTzRoLxJOviQAWcTByCMwDfC/9ND7Djws807TD+7AfjW1bTjZTiGquFJGRcgjmOcQ0P8AeYpDHr+T17iFhwj4oaQd18haXejEBcQrvhGA/KRECuY86O7hBMpLWOSFBADIfT7iOy8Ztk+2TTaudCzCIjLZdBAGG1fVdzI2ZJX7JURHBsfFnCPXuUzzEP8kQmkcAF9YFJxfAv3CiO7e/x5jyKCO7TdxY9sCppaWm7IpaVMPWewlmG83pe9JVtLnIF6M7BDE20lNwHEDxKvwAwTcfQXLWgfxqjbph180719DoGpqwOyTpee1AupMjQ/Yz1XIvjr7LeqpztN5C/Itsq70nKZiLYP9wYTEsH8aDodd1wBJGvIPx+D4m8RaN9BdTPIOx+AuBzQpULbwnWY4xb5BF/AYslnprDIKFeJFVwpDB0pLz2qmzynBw8XCEJW0g+8dZ6tkgJNjlgHEAQfyJu9TxnuU0XjkmUm0azgnGnD/6IAeRJsyHqO8Avmi1alhv9pIDcewynhUOQFjvMLnn43A8S8lci1/A/NN43HBcQafkzRE8BGSxyDTEBrYHzyiSZPD9w7Bp7x4yUaIsRth4TBUKaVrcRFwvkO3+kbyUpsOwHEwwRZ8+MjAkbLGgQdHLxnKQAWOaQHkaUIlv8E4yq2EWb0CNyui534yevHiJWuAJOwv7l7jS2SOshSUVXB3hGvbD78XL16yBkgicWodEtf8o8K1JHHNFUftu4PHGyD34sWLoaS1k+YSXWRTV5jk0ulOQVsHd4tKJ969jmVMaQFeeuTGje8WLx4g47NIXY4irdWmc8mb4GZl3LvX8YUsjLG5ayTcQWLF175rvHgXOx4IqVaISI7bezCLV847bJerat6PSUTHaZqc2ujFi2eQCnZIknz5LVchutQHFvdyeUzskR92Z3qS913jxQNkMjBiAZKwRVJxxvacG1dl1Ejy+WlGfRtAtEuE7tHuJ7hXEaK91Oye7zhtogcfDfAeaeZckvauMEbujDGO9GyYGr4fLXJAvI9bzkASL4Luq6W7YU4M+4DuhqlCtBuG/K4L0X75UOPB0GLQJKTwFdtK+nAO713Cf9PjeE9Bv1MngOj0TbpTh5Y+u8G2yYpOBDi3Gvj/bRDnIJN2PcP/3mLfJz0vpwrR7qAijnEf7tcfMH13unuMvjtbX/Na83uqVznUq31GrxawX1V6VQ+CYAH7PsBn/1mwdzgc3tGHpC10O+BXiF+Y9n8dtWUf0i0FVcAJ30Ll4fuXbjE7NugLMrCkRFcTgUE0ViEq5CnIj5HN433mFPfp431OOAOyhuCQl4RjaNmvISr0Z8FkJvfgi3J8RiCRJfwP8TtE6V8oXHny7C8g35xQxefrPBDy/oeoH3z7m/CweMMx6tEmyGPjZKz/UEzyRZBXJmflDj0uvqDFC3h47AMp6MJXded3tpH7/Qzxto3OItjqagcMsH9k3toSvruO+FzhfUQZJ8/gYVbLFwTC15J700IxRMefg/zYDNI32yOQbGcBkDlIvof372B/zoyoc34G9+dfsyzjuYXbSSb1toS9kUn5CuxixLc4QbocQGxaMvALvA95j/+x7IMPAuB/Bw8rqnRAfxAYLTv2xGBcRYtFLbAvg3cJD6tGiQC+j/1cMwA3ERi9BPu4+gkaDSr/FPTfGYIylRoCpMk46WQR1MfciuQLB+x0o0fL8j7bArD9UQDUHWSDBY1enYBZ9foPWVQfdlH2yMV+6dOUwfGlZUxuHsErEBiUl2C/gFaG+5WUcgpwHCrGZRYVeGDpwsvOxBb1Sd2gr0yPZg0EADaDfWFLABrwsAZmIPEUTLIqigL2uywBxxDZ3zGIFxHnOcZ0K2l/wBlamTG1kVoMcCTC1+BciQGOgM+uGoxL3SBsmDcExz/HaloqirctXkrlXqchpMNl6Ux7EG1pnBO4BHV4WIC1KACPO/wOPaqBTuScQJELyHBmJeDIlg4r4wTmj0HtM8ysiYCzLHGBaE5pB+xjorSYqa7A7A3eu6GYGPxEzEnau4VAThl/IGBKB4bGlMasVAWB6wz7oSdMilgNv71W5EKv4r0GyBZrAl2sQXQshSi00AH7mPMzxfvvQZTzvMT1A411D0F+djVgCIEeprUG4qNHniK7N5EutkmnVzr9q08LQNLyVHFXs2UFTl3IgsRq7ePAU7lWMIpDJvbVhehwqD5Eh0kNOMBognjbJR1oWWxrBi96DMJXvP88KneHifn08PlVCUDeQvwzvqkrTwH/reR7bEk6Wb3RIscsZGf7bDEgdIzvtShgJi2D9yJ9854Zlw0Qx0qLHDvPS7ybW4EheyIY2xYShrYEuBo4hnkJy7XNAS4o5t3vTGjjEvv0KaMr3xi9nlUYrT3GUGxJ+ol+pgN30o6P+FxinH5QkK4tUtYsCALZMbjFaTqTZhfjKXHipgcptmtWYV0bAqYgmkBlDsD/YCwvq6hFBLeGgbGQsbkmXgNUTrbuYpZVoNn6lrQ2Y07CeFnll7nZrAEQgVBfAEKXID+gSyfn3Hi2QZ8XWlWMyTsDF5J6CW0cX9F56LMIOHXBPUKwz+KoKlj9tSDMQg1uyOlTVQFofBuvBPOKvEsF9Ie2sXpF2XJeo1cdlXWYFrnGl7I9puAK0q35KFs8Wre8x40kFliDKA3BRs5Avd0zj8+YZRSzjVa/n8F4dgUAVpIwNXbymDAeU4PRU8QOddI3MH6m9y2C+UJayIFyUwCgeYnhPovhXhcNx0/VN6r72IyLSWXwO8G45DXPkOr7tB0R+S2Gq/wt5TYlTZYOOUtcRjaxiS5WJSZrJlb0VzCvrJRDNvUOkmcMjFOGFrqeNwAhlxImfK8O5w2dCwAvUHgYbQUDL0n6KEwAVib3yVvg0iANPaHVw6edQdJOJmd4/GgI7mmzR2qxRNbxxICJ0WB7j1GMNwrl66GBoC6I7hzwPrrrBGTnIUruDTSMYR3MA+KTJl3FhOZTzmYU/Zxl2/ZiGnLqMvOxSjapnn0n0VwgYYE1xIIhuqg7cD8mLpIyiGOCdOFxAPeT0nuK+/BSyXhcvhuABOxwkg/2egLYI43FVCXuzKmi3yvIHAecW12SAClfYd0kzYTuoaa7PyhbmMHfL0uUsQHTK3QXSkXAkpYhWhDIK8I1aRlVWQx1Dts1FOjJIoZaCFBtC4xuWwCQcxKDDQJ3fIPro0WIVqcBdacvwAp6rvQWAjUxrKtwP6ZL3P+f8L1In4oWlVqoj13m3xUJEcm8hkJhSicBAZ8vOEDjZI8A8jOUV3FC9DlruYzfp1ub3jPfUcVpbjiWV9e4LET5f2DY4hFE8UW6gk0s8luDGJLMPaohW6E7ccIJ0Y9DiW48RfDv4eQtSFheWnpzA+JsjDKGVGjKzAzqyALjKVVRD3a433awzbqwiMi9liWrt+B++UHCKlckwN7E54vi5DRlrY9AeyUw7Dn0CM/xu7LczbHUUJhWgKSDRgZElsC6m1E7zlFJ6wI34b8QzPuoGA2BAjUZ5VW5Ia9xcpUg2hesGtMmp7CL+LtTVFZVNZ4zAWiIVpnZ5HQ+7cVF3A3g4ZniprrRBHFSckPjsn42fE6oaKdKiGEXHTjHLpjJJFCA31MNWbiN2ec0BNCQeC05hUvMh5m28N3zAqM+r2n/fsy2J6r7Om2LNCKrsi2Z4J0M2/FJooB0b/aKZGKGXDsvFTEfMtnXkYEWQJ7GU2SYbSgY7wW8z5pEsa8FoQkam9K581UJaxK9d9fge13uHUJJ/9xIxuTQYoKQ8fsNHm7Bk7l115q2svflv/cr2G/16yhCRrrcxrbi86HB98l7fQS7A/mol8f3hW0N0TZEeY2q/qftvDUYv57AkIvm720A34esMPGNITKZ24zbkEPwWgR9ygaNyXwVDOAMssWK4reHeL0TWGN2n20N+8UkpngHUVJ6KGEvGwpLL2OQJWT5dewjmpx+LnjvFxAtIt2gO8kDSRUBvspMlG0FkJWwzXXs0wJElYx6+PszQXvY915HA0UN0zGIK+A3sb/LeP8OgoRssa6ObmoNovxNtsoSXZQzMfhvJeNM9OXfIF8BbqDelvGZbY0xpO4/rUBEC5nQ/en0bGldexvMu9MKU/Q0T1rJ6ERBGIqoL6xefRN4PyX8Xg379hb16s/2/XX+dRBUUE8rjP5tfy8AyYLkscByZSk0oZWWgipAdKQpjf9dG7ieNYjKgAWMArJxzRIqWRE/u5BY1gKjiDQuFDKM7AbMA+BlVO4SE6+kcbsQvGQtOcYIiQDyFNm0F5H1GKodjMJ39K60VNXJuPscQSrpUQRXBm5YD8x2CfUVDMlWbsfAzr2IGdQm6Hf9+ALRCaTwnb3PgR9SL49EZg3A8Rz86Z2J6bkXL16mT7oGHshn302eQXrx8hiFLgCRBRZ2lxAJ7ZAwE1u0wUtM+X8BBgA+EoPr8o5ceQAAAABJRU5ErkJggg==',
  zc: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAkAAAAMCAYAAACwXJejAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAABZ0RVh0Q3JlYXRpb24gVGltZQAxMi8xOS8xOBJAKZ4AAAAcdEVYdFNvZnR3YXJlAEFkb2JlIEZpcmV3b3JrcyBDUzbovLKMAAAAnklEQVQYlY3QsQ3CMBAF0G8XrBBRUqZALAB7MELqSExBRxkpDV3SZQekpDRiAJd0KVPYsT+dkQGL/Pbe3elOmMuBXt+QitzsIZPVEEKQ/MsWTPpEZqK9HgkzMYnmroRXLeau/D3Jq4aurwAArq/gVcMIcdS0bRF127YAR82A3FBDZnm8IsvhhhoA3i/g80Fz3gW0Ot0h1lvxfV0ii9ALEms//widFg0AAAAASUVORK5CYII=',
  yl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAkAAAAMCAYAAACwXJejAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAABZ0RVh0Q3JlYXRpb24gVGltZQAxMi8xOS8xOBJAKZ4AAAAcdEVYdFNvZnR3YXJlAEFkb2JlIEZpcmV3b3JrcyBDUzbovLKMAAAAoklEQVQYlWP8//8/AwMDA8Od9wz/wzYxwMEqPwYGFUEGRgYGBgYmBiIAUYoY////zzD1HMP/Uy8YGC6/RkjoijIwmEkwMGQbMTAyMTAwMASoMTDc/4iq+/5HiDjcOmkeBsYaS1RFNZYQcRQ3uSkwMAZBdQapQfhwHf///4fj77///y878P//99///yOLM8LCieIgYEnazvD/wivcCgzEiDQJAOdmPiuqgpQNAAAAAElFTkSuQmCC'
}

/***/ }),

/***/ "./modules/int.js":
/*!************************!*\
  !*** ./modules/int.js ***!
  \************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * 取整
 */

module.exports = {
  int: function(num){
    var i = Math.floor(num)
    if (i == 0) {
      return Math.floor(num) + 0.5
    }
    return Math.floor(num) - 0.5
  }
}

/***/ }),

/***/ "./modules/text.js":
/*!*************************!*\
  !*** ./modules/text.js ***!
  \*************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * 文字层
 */

module.exports = function(ctx, width, height, data, statdata){
  var lastdata = data[data.length - 1]

  var t1 = lastdata.d5
  var t2 = lastdata.d20
  var t3 = lastdata.d60
  var d1 = data[0].d
  var d2 = data[Math.floor(data.length / 2)].d
  var d3 = lastdata.d
  var max = statdata.num_max.toFixed(2)
  var min = statdata.num_min.toFixed(2)

  ctx.font="12px Arial";

  ctx.textBaseline="top";
  var txt1 = 'MA5: ' + t1.toFixed(2)
  ctx.fillStyle = '#5a85ff'
  ctx.fillText(txt1 ,0 ,0);

  var txt2 = 'MA20: ' + t2.toFixed(2)
  ctx.fillStyle = '#ff10ff'
  ctx.fillText(txt2 ,ctx.measureText(txt1).width + 12 ,0);

  ctx.fillStyle = '#018101'
  ctx.fillText('MA60: ' + t3.toFixed(2) ,ctx.measureText(txt1).width + ctx.measureText(txt2).width + 24 ,0);
  
  ctx.fillStyle = '#000'
  ctx.textBaseline="bottom";
  ctx.fillText(d1 ,0 ,height);
  ctx.fillText(d2 ,width/2 ,height);
  ctx.textAlign="end";
  ctx.fillText(d3 ,width ,height);

  ctx.textAlign="start";
  ctx.textBaseline="top";
  ctx.fillText(max ,5 , 22);

  ctx.textAlign="start";
  ctx.textBaseline="bottom";
  ctx.fillText(min ,5 , height - 20);  
}

/***/ })

/******/ });
});
//# sourceMappingURL=index.js.map

/***/ }),

/***/ "./modules/user/getuid.js":
/*!********************************!*\
  !*** ./modules/user/getuid.js ***!
  \********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 登录用户获取uid,未登录用户获取指纹
 */

var user = __webpack_require__(/*! ./index */ "./modules/user/index.js")
var fingerprint = __webpack_require__(/*! ../browser_fingerprint */ "./modules/browser_fingerprint/index.js")

module.exports = {
  get: function(){
    return new Promise(function(resolve, reject){
      if (user.get() != null) {
        resolve(user.get().id)
        return
      }
      
      fingerprint.get(function(zw){
        resolve(zw)
      })
    })
  }
}

/***/ }),

/***/ "./modules/user/index.js":
/*!*******************************!*\
  !*** ./modules/user/index.js ***!
  \*******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 用户信息
 */

var cookie = __webpack_require__(/*! ../cookie/ */ "./modules/cookie/index.js");

/**
 * 用户
 */
var user = {
    /**
     * 获取用户信息
     */
    get: function(){
        if (cookie.get('ut') && cookie.get('ct') && cookie.get('uidal')) {
            
            //获取加v信息
            var jiav = {vtype:null, state: null, name: ''};
            if (cookie.get('vtpst') && cookie.get('vtpst') != '|') {
                var jiavarr = cookie.get('vtpst').split('|');
                if( jiavarr.length > 1 ){
                    //console.info(typeof jiavarr[0]);
                    if (jiavarr[1] == "0" || jiavarr[1] == "3") {
                        switch (jiavarr[0]) {
                            case "301":
                                jiav.vtype = 1;
                                jiav.name = '理财师';
                                break;
                            case "302":
                                jiav.vtype = 2;
                                jiav.name = '非理财师';
                                break;
                            case "303":
                                jiav.vtype = 3;
                                jiav.name = '企业';
                                break;
                            default:
                                break;
                        }
                    }

                    switch (jiavarr[1]) {
                        case "0":
                            jiav.state = 0; //审核通过
                            break;                        
                        case "1":
                            jiav.state = 11; //审核未通过
                            break;
                        case "2":
                            jiav.state = 12; //审核中
                            break;
                        case "3":
                            jiav.state = 13; //加v用户修改审核
                            break;
                        case "8":
                            jiav.state = 18; //加v用户修改审核
                            break;
                        case "9":
                            jiav.state = 19; //加v用户修改审核
                            break;
                        default:
                            break;
                    }
                    
                    //console.info(jiav);

                }
            }
            
            return {
              id: cookie.get('uidal').substring(0,16),
              nick: cookie.get('uidal').substring(16),
              jiav: jiav
            };
        }
        return null; 
    },
    /**
     * 退出登录
     * @param  {function} 退出之后回调
     */
    logOut: function (callback) {
        var date = new Date();
        document.cookie = "pi=;path=/;domain=eastmoney.com;expires=" + date.toGMTString();
        document.cookie = "ct=;path=/;domain=eastmoney.com;expires=" + date.toGMTString();
        document.cookie = "ut=;path=/;domain=eastmoney.com;expires=" + date.toGMTString();
        document.cookie = "uidal=;path=/;domain=eastmoney.com;expires=" + date.toGMTString();
        if (callback) {
            callback();
        }
    },
    isLogin: function (){
        if( this.get() ){
            return true;
        }
        else{
            return false;
        }
    }
};

module.exports = user;





/***/ }),

/***/ "./modules/utils/index.js":
/*!********************************!*\
  !*** ./modules/utils/index.js ***!
  \********************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * 
 */

module.exports = {
  /**
   * 数组插队
   * @param {*} array 数组
   * @param {*} fromindex 从什么位置
   * @param {*} toindex 插入到什么位置
   */
  arrayJump: function(array, fromindex, toindex){
    if (fromindex > toindex) {
      var a1 = array.slice(0,toindex)
      var a2 = array[fromindex]
      var a3 = array.slice(toindex, fromindex)
      var a4 = array.slice(fromindex + 1)
      return a1.concat(a2).concat(a3).concat(a4)    
    }
    else if (fromindex < toindex) {
      var a1 = array.slice(0,fromindex)
      var a2 = array.slice(fromindex + 1, toindex + 1)
      var a3 = array[fromindex]
      var a4 = array.slice(toindex + 1)
      return a1.concat(a2).concat(a3).concat(a4)    
    }
    return array
  },
  /**
   * 获取url变量
   * 
   * @param {any} name 变量名
   */
  getParam: function(name){
    var urlpara = location.search;
    var par = {};
    if (urlpara != "") {
      urlpara = urlpara.substring(1, urlpara.length);
      var para = urlpara.split("&");
      var parname;
      var parvalue;
      for (var i = 0; i < para.length; i++) {
        parname = para[i].substring(0, para[i].indexOf("="));
        parvalue = para[i].substring(para[i].indexOf("=") + 1, para[i].length);
        par[parname] = parvalue;
      }
    }
    if(typeof (par[name]) != "undefined"){
      return par[name];
    }
    else{
      return null;
    }
  },
  /**
   * object排序
   * @param {*} obj 
   */
  objectSort: function(obj, callback){
    var templist = Object.keys(obj)
    templist.sort(function(v1, v2){
      return callback(obj[v1], obj[v2])
    })
    var backobj = {}
    templist.forEach(function(v){
      backobj[v] = obj[v]
    })
    return backobj
  }
}

/***/ }),

/***/ "./modules/ylyc/web.js":
/*!*****************************!*\
  !*** ./modules/ylyc/web.js ***!
  \*****************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 盈利预测
 */

var datacache = __webpack_require__(/*! ../datacache */ "./modules/datacache/index.js")

module.exports = {
  getData: function(codes){
    return $.ajax({
      url: './api/ylyc',
      type: 'GET',
      dataType: 'json',
      data: {
        codes: codes
      }
    })
    .then(function(json){
      datacache.ylyc_year = parseInt(json.result.BASICYEAR)
      return json.result.Data.map(function(v){
        return v.split('|')
      })
    })
  }
}

/***/ }),

/***/ "./modules/zdtj/index.js":
/*!*******************************!*\
  !*** ./modules/zdtj/index.js ***!
  \*******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 涨跌统计
 */
var webconfig = __webpack_require__(/*! ../../config/webconfig */ "./config/webconfig.js")

module.exports = {
  init: function(){
    var _this = this
    this.getData()
    setInterval(function(){
      _this.getData()
    }, 30 * 1000);
  },
  getData: function(){
    var _this = this
    $.ajax({
      url: webconfig.getWebPath('getpath') + 'api/qt/ulist.np/get?secids=1.000001,0.399001&fields=f104,f105,f106&ut=6d2ffaa6a585d612eda28417681d58fb&cb=?',
      type: 'GET',
      dataType: 'jsonp',
      data: {
        
      }
    })
    .done(function(json) {   
      if (json.rc == 0) {
        $('#zdtj_z').text(json.data.diff[0].f104 + json.data.diff[1].f104)
        $('#zdtj_d').text(json.data.diff[0].f105 + json.data.diff[1].f105)
        $('#zdtj_p').text(json.data.diff[0].f106 + json.data.diff[1].f106)
      }
    })
    .fail(function(error) {
      
    })

    $.ajax({
      url: webconfig.getWebPath('getpath') + 'api/qt/kamt/get?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54&ut=6d2ffaa6a585d612eda28417681d58fb&cb=?',
      type: 'GET',
      dataType: 'json',
      data: {
        
      }
    })
    .done(function(json) {   
      if (json.rc == 0) {
        var num1 = json.data.hk2sh.dayNetAmtIn
        var num2 = json.data.hk2sz.dayNetAmtIn
        $('#zdtj_hgt').text(_this.dealNum(num1).text).removeClass('stockup stockdown').addClass(_this.dealNum(num1).classname)
        $('#zdtj_sgt').text(_this.dealNum(num2).text).removeClass('stockup stockdown').addClass(_this.dealNum(num2).classname)
      }
    })
    .fail(function(error) {
      
    })
  },
  dealNum: function(num){
    var classname = ''

    if (num > 0) {
      classname = 'stockup'
    }
    else if (num < 0){
      classname = 'stockdown'
    }

    var qz = ''
    if (num < 0) {
      qz = '-'
      num = Math.abs(num)
    }
    var fx = '万'
    
    if (num >= 10000) {
      num = num / 10000
      fx = '亿'
    }


    return {
      text: qz + num.toFixed(2) + fx,
      classname: classname
    }
  }
}

/***/ }),

/***/ "./modules/zhuti/chance.html":
/*!***********************************!*\
  !*** ./modules/zhuti/chance.html ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"bkblock\">\r\n  <div class=\"bkt\"><a href=\"http://quote.eastmoney.com/zhuti/{{? it.IsImportant == '0' }}subject{{??}}topic{{?}}/{{=it.Code}}\" class=\"glink\">{{=it.Name}}</a></div>\r\n  <div class=\"bkintro\">{{=it.Reason}}</div>\r\n  <div class=\"bkstock\">\r\n    <ul>\r\n      {{~it.StockList :value:index}}\r\n        {{? index <= 1 }}\r\n        <li><a href=\"http://quote.eastmoney.com/concept/{{=value.MarketName + value.Code}}.html?from=zixuan\">{{=value.Name}}</a> <span class=\"time {{=value.classname}}\">{{=value.Chg}}%</span></li>\r\n        {{?}}\r\n      {{~}}\r\n    </ul>\r\n  </div>\r\n</div>"

/***/ }),

/***/ "./modules/zhuti/fxb.html":
/*!********************************!*\
  !*** ./modules/zhuti/fxb.html ***!
  \********************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<table class=\"fxbtable\">\r\n  <tr>\r\n    <th>名称</th>\r\n    <th>最新价</th>\r\n    <th>涨幅</th>\r\n    <th>入选原因</th>\r\n  </tr>\r\n  {{~it.data :value:index}}\r\n  <tr>\r\n    <td><a href=\"http://quote.eastmoney.com/concept/{{=value[5]}}{{=value[0]}}.html?from=zixuan\">{{=value[1]}}<br>{{=value[0]}}</a></td>\r\n    <td>{{=it.textColor(value[6],value[7])}}</td>\r\n    <td>{{=it.textColor(value[7] + '%',value[7])}}</td>\r\n    <td class=\"fxbyy\"><div title=\"{{=value[4]}}\">{{=value[4]}}</div></td>\r\n  </tr>\r\n  {{~}}\r\n</table>"

/***/ }),

/***/ "./modules/zhuti/web.js":
/*!******************************!*\
  !*** ./modules/zhuti/web.js ***!
  \******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 主题投资
 */

var chancehtml = __webpack_require__(/*! ./chance.html */ "./modules/zhuti/chance.html")
var fxbhtml = __webpack_require__(/*! ./fxb.html */ "./modules/zhuti/fxb.html")
var dot = __webpack_require__(/*! dot */ "./node_modules/dot/doT.js")
var text = __webpack_require__(/*! ../text */ "./modules/text/index.js")
var tabs = __webpack_require__(/*! ../tabs */ "./modules/tabs/index.js")

module.exports = {
  init: function(){
    var _this = this
    this.getData().done(function(data){
      _this.fillHtml(data.result[0])
    })
    // $('#scfgbtab').on('click', 'li', function(){
    //   var index = $(this).index()
    //   $('#scfgbtab li').removeClass('on')
    //   $(this).addClass('on')
    //   if (index == 0) {
    //     $('#scfgbt1').show()
    //     $('#scfgbt2').hide()
    //   }
    //   else{
    //     if ($('#scfgbt2').html() == '') {
    //       _this.getFXB()
    //     }
    //     $('#scfgbt2').show()
    //     $('#scfgbt1').hide()
    //   }

    // })

    _this.getFXB()
    setInterval(function(){
      _this.getFXB()
    }, 30 * 1000);
    var sxfgtab = new tabs({
      tabsobj: $('#scfgbtab li'),
      type: 'display',
      contents: $('.scfgbtd')
    });
    sxfgtab.init();

    
  },
  getData: function(){
    return $.ajax({
      url: './api/zhuti/fg',
      type: 'GET',
      dataType: 'json',
      data: {
        
      }
    })
  },
  zttabs: null,
  fillHtml: function(data){
    var _this = this
    //建议仓位
    $('#ztfg').text(data.TopText.PositionInd)
    //指针
    var angle = (data.TopText.PositionInd / 100) * Math.PI - Math.PI/2

    var x = 95 + 56 * Math.cos(Math.PI/2 - angle)
    var y = 68 - 56 * Math.sin(Math.PI/2 - angle)

    $('#jycwarrow').css({
      'display': 'block',
      'transform': 'translate(' + x + 'px,' + y + 'px) rotate(' + angle + 'rad) ',
      '-ms-transform': 'translate(' + x + 'px,' + y + 'px) rotate(' + angle + 'rad) '
    })

    $('#jycwzss').text(data.TopText.Title)
    $('#jycwzss2').text(data.TopText.Content)

    //市场风格 scfgtab
    $('#scfgblocks').html('')

    var scfghtml = []
    data.MarketStyle.forEach(function(v, i){
      scfghtml.push('<li')
      if (i == 0) {
        scfghtml.push(' class="on"')
      }
      scfghtml.push('><a href="http://quote.eastmoney.com/zhuti/">' + v.Category + '</a></li>')
      _this.fillBlock(v.ThemeList, i)
    })
    $('#scfgtab').html(scfghtml.join(''))

    // $('#scfgtab').off()
    // $('#scfgtab').on('click', 'li', function(){
    //   var index = $(this).index()
    //   $('#scfgtab li').removeClass('on')
    //   $(this).addClass('on')
    //   $('#scfgblocks ul').hide()
    //   $('#scfgblocks ul').eq(index).show()
    // })

    this.zttabs = new tabs({
      tabsobj: $('#scfgtab li'),
      type: 'display',
      contents: $('#scfgblocks ul') 
    });
    this.zttabs.init();

    //短线机会 中长线机会

    function dealChangeData(v){
      v.StockList.forEach(function(v2){
        v2.classname = text.className(v2.Chg)
        v2.MarketName = ''
        if (v2.Market == '01') {
          v2.MarketName = 'sh'
        }
        else if(v2.Market == '02'){
          v2.MarketName = 'sz'
        }
      })
    }

    // dealChangeData(data.Recommend[0].ThemeList[0])
    // dealChangeData(data.Recommend[1].ThemeList[0])

    // $('#dxjh').html(_this.fillChance(data.Recommend[0].ThemeList[0]))
    // $('#zcxjh').html(_this.fillChance(data.Recommend[1].ThemeList[0]))
  },

  /**
   * 填充市场风格颜色块
   * @param {*} data 
   */
  fillBlock: function(data, index){

    if(data.length > 5){
      data = data.slice(0, 5)
    }
    var _this = this
    var html = []
    html.push('<ul>')
    data.forEach(function(v, i){
      var fg = ' '
      var blockclass = _this.blockClass(data.length, i)
      if (blockclass == 'mblock') {
        fg = '<br>'
      }
      if (v.Chg == '') {
        v.Chg = '0.00'
      }
      html.push('<li class="' + blockclass + ' ' + _this.blockColorClass(v.HotRate) + '"><a href="' + _this.ztlink(v.Code, v.IsImportant) + '">' + v.Name + fg + v.Chg + '%</a></li>')
    })
    html.push('</ul>')
    html = $(html.join(''))
    if (index > 0) {
      html.hide()
    }
    $('#scfgblocks').append(html)
  },
  ztlink: function(code, isimportant){
    if( isimportant == '1'){
      return 'http://quote.eastmoney.com/zhuti/topic/' + code
    }
    return 'http://quote.eastmoney.com/zhuti/subject/' + code
  },
  blockClass: function(count, index){
    if (count == 5) {
      if (index == 0) {
        return 'mblock'
      }
      else{
        return 'sblock'
      }
    }
    else if(count == 4){
      if (index <= 1) {
        return 'mblock'
      }
      else{
        return 'sblock'
      }
    }
    else if(count == 3){
      return 'mblock'
    }

    return 'lblock'


  },
  blockColorClass: function(rate){
    if (rate >= 10) {
      return 'r5'
    }
    if (rate >= 7) {
      return 'r4'
    }
    if (rate >= 3) {
      return 'r3'
    }
    if (rate >= 1) {
      return 'r2'
    }
    if (rate > 0) {
      return 'r1'
    }    
    if (rate == 0) {
      return 'r0'
    }
    if (rate >= -1) {
      return 'g1'
    }
    if (rate >= -3) {
      return 'g2'
    }
    if (rate >= -7) {
      return 'g3'
    }
    if (rate >= -10) {
      return 'g4'
    }
    return 'g5'
  },
  /**
   * 填充机会
   * @param {*} data 
   */
  fillChance: function(data){
    //console.info(data)
    data.StockList.forEach(function(v){
      if (v.Chg == '') {
        v.Chg = '0.00'
      }
    })
    return dot.template(chancehtml)(data)
  },
  getFXB: function(){
    var _this = this
    $.ajax({
      url: './api/zhuti/fxb',
      type: 'GET',
      dataType: 'json',
      data: {
        
      }
    })
    .done(function(json) {   
      if (json.re) {
        _this.fillFXB(json.result[0].Data)
      }
    })
    .fail(function(error) {
      
    })
  },
  fillFXB: function(data){
    data = data.map(function(v){
      var back = v.split('|')
      if (back[6] == '') {
        back[6] = '0.00'
      }      
      if (back[7] == '') {
        back[7] = '0.00'
      }
      if (back[5] == '01') {
        back[5] = 'sh'
      }
      else if(back[5] == '02'){
        back[5] = 'sz'
      }
      return back
    })
    //console.info(data)
    $('#scfgbt2').html(dot.template(fxbhtml)({
      data: data,
      textColor: text.textColor
    }))
  }
}

/***/ }),

/***/ "./modules/znzg/index.js":
/*!*******************************!*\
  !*** ./modules/znzg/index.js ***!
  \*******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 智能诊股
 */

var znzg_html = __webpack_require__(/*! ./znzg.html */ "./modules/znzg/znzg.html")
var znzg_none_html = __webpack_require__(/*! ./znzg_none.html */ "./modules/znzg/znzg_none.html")
var dot = __webpack_require__(/*! dot */ "./node_modules/dot/doT.js")
var text = __webpack_require__(/*! ../text */ "./modules/text/index.js")
var trend_kline = __webpack_require__(/*! ../trend_kline */ "./modules/trend_kline/index.js")
var radar_chart = __webpack_require__(/*! ../radar_chart */ "./modules/radar_chart/index.js")
var tabs = __webpack_require__(/*! ../tabs */ "./modules/tabs/index.js")
var datetime = __webpack_require__(/*! ../datetime */ "./modules/datetime/index.js")
var modalalert = __webpack_require__(/*! ../modal/alert */ "./modules/modal/alert.js")
var datacache = __webpack_require__(/*! ../datacache */ "./modules/datacache/index.js")

module.exports = {
  init: function () {
    this.bind()
  },
  bind: function () {
    var _this = this
    $('#wl_mainbody').on('click', '#wltable tr, #tablethd4 tr', function (e) {

      if (datacache.pxorder) {
        return true
      }
      // console.info(e.target.nodeName)
      if (e.target.nodeName == 'A' || e.target.nodeName == 'I' || e.target.nodeName == 'INPUT') {
        return true
      }
      var thistr = $(this)
      //console.info(thistr)
      var trindex = $(this).index()

      var ishsstock = thistr.data('ishsstock')
      var code = thistr.data('code').toString()
      if (ishsstock != '1') {
        return true
      }
      // if (code == '0.300059') {
      //   modalalert('医者不能自医，换只股票试试')
      //   return true
      // }

      var iszk = thistr.is('.zk')
      // $('.wltable tr.zk').removeClass('zk')
      // $('#tablethd4 tr.zk').removeClass('zk')
      // //$('#tablethd4 .znzgd').html('').hide()
      // $('#znzgd').html('').hide()
      _this.close()
      if (!iszk) {

        var hscode = code.substring(code.indexOf('.') + 1)
        var market = code.substring(0, code.indexOf('.'))
        var ywzcode = hscode + '1'
        if (market == 0) {
          ywzcode = hscode + '2'
        }

        //东财特殊处理
        if (code == '0.300059') {
          _this.show(null, trindex, code, hscode, ywzcode, true)
          return true
        }

        $.ajax({
            url: './api/znzg?code=' + hscode,
            type: 'GET',
            dataType: 'json',
            data: {

            }
          })
          .then(function (json) {
            _this.show(json, trindex, code, hscode, ywzcode)
          })
          .fail(function (error) {

          })


      }

    })

    $('#wl_mainbody').on('click', '.znzgd', function (e) {
      if (e.target.nodeName == 'A') {
        return true
      }
      return false
    })


  },
  show: function (json, trindex, code, hscode, ywzcode, isdc) {
    var bm60 = false
    var _this = this
    if (isdc) {
      json = {re: true}
    }
    if (json.re == false && json.message == '目前智能诊股只支持上市满六十交易日的沪深A股') {
      json = {re: true}
      isdc = true
      bm60 = true
    }
    if (json.re) {
      $('#wltable tr').eq(trindex).addClass('zk')
      $('#tablethd4 tr').eq(trindex).addClass('zk')
      $('#tablethd6 tr').eq(trindex).addClass('zk')
      $('#tablethdd6').css({
        'z-index': 6
      })
      var top = $('#tablethd4 tr').eq(trindex).offset().top - (122 + $('#zshq').outerHeight())
      var vscroll = $('#tablethdd5').get(0).offsetWidth - $('#tablethdd5').get(0).clientWidth //竖向滚动条宽度
      //$('#tablethd4 .znzgd').eq(trindex).show()
      $('#znzgd').data('index', trindex).css({
        top: top,
        width: $('#wl_mainbody').get(0).clientWidth - vscroll
      })

      if ($('#ykylcount').length) {
        $('#ykylcount').css({top: $('#tablethd4').height() + 36})
      } 

      //return false
      var html

      if (isdc) {
        html = $(dot.template(znzg_none_html)({
          bm60: bm60,
          hqlink: text.getLinkByCode(code)
        }))
      }
      else{
        json.result.ApiResults.yqgz.All = json.result.ApiResults.yqgz.All.slice(0, 5)

        html = $(dot.template(znzg_html)({
          data: json.result.ApiResults,
          textNumColor: text.textNumColor,
          textNumColorPlus: text.textNumColorPlus,
          textColor: text.textColor,
          formatNum: text.formatNum,
          hscode: hscode,
          hqlink: text.getLinkByCode(code),
          strToDayOrTime: datetime.strToDayOrTime
        }))
      }

      //$('#tablethd4 .znzgd').eq(trindex).show().html(html)
      $('#znzgd').show().html(html)
      var fp = _this.fdshow() //屏幕种类
      var img_height = 200
      if (fp == 'middle') {
        img_height = 170
      }
      //k线图
      var option = {
        container: "#znzgkchart",
        code: code,
        newquote: true,
        width: 340,
        height: img_height,
        bigImg: {
          stauts: "show"
        },
        color: {
          background: '#f7f7f7'
        },
        show: {
          title: true
        },
        onMove: function (msg) {
          //console.log(msg);
        },
        onComplete: function () {
          //console.log("onComplete")
        }
      }

      //console.info(111)
      //setTimeout(function(){
      var kmini = new emcharts3.kmini(option);
      //console.info(222)
      // kmini.start(1);
      kmini.draw();
      //}, 1000);


      //分时图
      var fsoption = {
        container: "#znzgfschart",
        code: code,
        token: "fa5fd1943c7b386f172d6893dbfba10b",
        width: 340,
        height: img_height,
        color: {
          background: '#f7f7f7'
        },
        //"color.background": ,
        bigImg: {
          stauts: "show"
        },
        timeline: [
          // {
          //     time: "11:30/13:00",
          //     position: 0.5
          // }
        ],
        onMove: function (msg) {
          //console.log(msg);
        },
        // show: {
        //     title: false
        // },
        onComplete: function () {
          //console.log("onComplete")
        },
        onError: function (err) {
          //console.log(err);
        }
      }


      var mm = new emcharts3.timemini(fsoption);
      mm.start();
      mm.draw();

      if (isdc) {
        return false
      }

      //趋势研判图
      var newqskline = new trend_kline({
        ele: document.getElementById('trend_klinediv'),
        width: 352,
        height: 173,
        data: json.result.ApiResults.zj.Trend[1].map(function (v) {
          return {
            d: v.TDate.substring(0, v.TDate.indexOf(' ')),
            c: parseFloat(v.Close),
            o: parseFloat(v.Open),
            h: parseFloat(v.High),
            l: parseFloat(v.Low),
            d5: parseFloat(v.Price5),
            d20: parseFloat(v.Price20),
            d60: parseFloat(v.Price60),
          }
        })
      })

      var zcyl = newqskline.getPrice()
      $('#zcprice', html).text(zcyl.zc.price)
      $('#ylprice', html).text(zcyl.yl.price)

      //雷达图
      var radardata = [{
          name: json.result.ApiResults.zj.Value[2][0].ReportText,
          color: '#EA5504',
          item: ['成长能力', '运营偿债能力', '现金流', '估值水平', '盈利能力'],
          value: [json.result.ApiResults.zj.Value[2][0].GrowUpScorePercent, json.result.ApiResults.zj.Value[2][0].OperationScorePercent, json.result.ApiResults.zj.Value[2][0].CashFlowScorePercent, json.result.ApiResults.zj.Value[2][0].ValuationScorePercent, json.result.ApiResults.zj.Value[2][0].ProfitabilityScorePercent]
        },
        {
          name: json.result.ApiResults.zj.Value[2][1].ReportText,
          color: '#EA5504',
          item: ['成长能力', '运营偿债能力', '现金流', '估值水平', '盈利能力'],
          value: [json.result.ApiResults.zj.Value[2][1].GrowUpScorePercent, json.result.ApiResults.zj.Value[2][1].OperationScorePercent, json.result.ApiResults.zj.Value[2][1].CashFlowScorePercent, json.result.ApiResults.zj.Value[2][1].ValuationScorePercent, json.result.ApiResults.zj.Value[2][1].ProfitabilityScorePercent]
        }
      ]
      radar_chart($('#jzpgchart').get(0), radardata)

      // $('.tab6', html).on('click', 'li', function(){
      //   var index = $(this).index()
      //   $('.tab6 li', html).removeClass('on')
      //   $(this).addClass('on')
      //   $('.zgb>div', html).hide()
      //   $('.zgb>div', html).eq(index).show()
      //   return false
      // })
      var zgzbtabs = new tabs({
        tabsobj: $('.tab6 li', html),
        type: 'display',
        contents: $('.zgb>div', html)
      });
      zgzbtabs.init();


    } else {
      modalalert(json.message)
    }
  },
  close: function () {
    $('.wltable tr.zk').removeClass('zk')
    $('#tablethd4 tr.zk').removeClass('zk')
    $('#tablethd6 tr').removeClass('zk')
    $('#znzgd').html('').hide()
    $('#tablethdd6').css({
      'z-index': 8
    })
    if ($('#ykylcount').length) {
        $('#ykylcount').css({top: $('#tablethd4').height() + 36})
      }
  },
  /**
   * 根据屏幕宽度分段显示
   */
  fdshow: function () {
    var w = $(window).width()
    if (w >= 1440) {
      return 'big'
    }
    if (w > 1024) {
      $('.znzgtab2').show()
      $('#znzgkcharta').hide()
      $('.fskxd').css({
        float: 'left',
        width: 340
      })
      $('.znzgs2tab li').on('click', function () {
        var index = $(this).index()
        if (index == 0) {
          $('#znzgfscharta').css({
            display: 'block'
          })
          $('#znzgkcharta').css({
            display: 'none'
          })
        } else if (index == 1) {
          $('#znzgfscharta').css({
            display: 'none'
          })
          $('#znzgkcharta').css({
            display: 'block'
          })
        }
        $('.znzgs2tab li').removeClass('on')
        $(this).addClass('on')
      })

      return 'middle'
    }

    //small
    $('.znzgsmalltab li').on('click', function () {
      var index = $(this).index()
      if (index == 0) {
        $('.fskxd').css({
          display: 'block'
        })
        $('.znzg_rc').css({
          display: 'none'
        })
      } else if (index == 1) {
        $('.fskxd').css({
          display: 'none'
        })
        $('.znzg_rc').css({
          display: 'block'
        })
      }
      $('.znzgsmalltab li').removeClass('on')
      $(this).addClass('on')
    })

    $('.znzg').css({
      width: 'auto'
    })
    $('.znzgsmalltab').css({
      display: 'block'
    })
    $('.fskxd').css({
      display: 'block'
    })
    $('.znzg_rc').css({
      display: 'none'
    })
    return 'small'
  }
}

/***/ }),

/***/ "./modules/znzg/znzg.html":
/*!********************************!*\
  !*** ./modules/znzg/znzg.html ***!
  \********************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"znzg\">\r\n\r\n  <div class=\"znzgtab znzgsmalltab\">\r\n    <ul>\r\n      <li class=\"on\"><a href=\"javascript:;\" target=\"_self\">分时K线</a></li>\r\n      <li><a href=\"javascript:;\" target=\"_self\">智能诊股</a></li>\r\n    </ul>\r\n  </div>\r\n\r\n\r\n\r\n  <div class=\"fskxd\">\r\n    <div class=\"znzgtab2\">\r\n      <ul class=\"znzgs2tab\">\r\n        <li class=\"on\"><a href=\"javascript:;\" target=\"_self\">分时</a></li>\r\n        <li><a href=\"javascript:;\" target=\"_self\">K线</a></li>\r\n      </ul>      \r\n    </div>\r\n    <a href=\"{{=it.hqlink}}\" id=\"znzgfscharta\"><div class=\"fschart\" id=\"znzgfschart\"></div></a>\r\n    <a href=\"{{=it.hqlink}}\" id=\"znzgkcharta\"><div class=\"kchart\" id=\"znzgkchart\"></div></a>    \r\n  </div>\r\n\r\n  <div class=\"znzg_rc\">\r\n    <div class=\"zhpf\">\r\n      <div class=\"pin\"><span class=\"icon icon_pin\"></span></div>\r\n      <div class=\"zhpfd1\">综合评分 <span>{{=Math.round(it.data.zj.Overall[0].TotalScore)}}</span></div>\r\n      <div class=\"zhpfd2\">今日表现 &nbsp;&nbsp;&nbsp; {{=it.textNumColorPlus(it.data.zj.Overall[0].TotalScoreCHG, 2)}} </div>\r\n      <div class=\"zhpfd3\">打败了 <span class=\"c_or\">{{=(it.data.zj.Overall[0].LeadPre / 1).toFixed(2)}}%</span> 的股票</div>\r\n      <div class=\"zhpfd4\">次日上涨概率 &nbsp;&nbsp;&nbsp;  <span class=\"stockup\">{{=(it.data.zj.Overall[0].RisePro / 1).toFixed(2)}}%</span></div>\r\n      <div class=\"zhpfd5\">{{=it.data.zj.Overall[0].Comment}}</div>\r\n      <div class=\"zhpfd6\" title=\"本功能中的内容均仅供参考，建议投资者根据自身投资风格进行筛选，并合理控制风险。\">免责声明 <span class=\"icon icon_question\"></span> &nbsp;&nbsp; <a href=\"http://data.eastmoney.com/stockcomment/stock/{{=it.hscode}}.html#zhpj\">详情</a></div>\r\n    </div>\r\n    <div class=\"zg\">\r\n      <div class=\"tab6\">\r\n        <ul>\r\n          <li class=\"on\"><a href=\"http://data.eastmoney.com/stockcomment/stock/{{=it.hscode}}.html#yqjk\">舆情关注</a></li>\r\n          <li><a href=\"http://data.eastmoney.com/stockcomment/stock/{{=it.hscode}}.html#scrd\">市场热度</a></li>\r\n          <li><a href=\"http://data.eastmoney.com/stockcomment/stock/{{=it.hscode}}.html#qsyp\">趋势研判</a></li>\r\n          <li><a href=\"http://data.eastmoney.com/stockcomment/stock/{{=it.hscode}}.html#zjdx\">资金动向</a></li>\r\n          <li><a href=\"http://data.eastmoney.com/stockcomment/stock/{{=it.hscode}}.html#jzpg\">价值评估</a></li>\r\n        </ul>\r\n      </div>\r\n      <div class=\"zgb\">\r\n        <div class=\"zgb1\">\r\n          <ul class=\"newslist\">\r\n            {{~it.data.yqgz.All :value:index}}\r\n            <li><a href=\"{{=value.Url}}\" title=\"{{=value.Title}}\">{{=value.Title}}</a><span class=\"time\">\r\n              {{=it.strToDayOrTime(value.DateTime)}}\r\n            </span></li>\r\n            {{~}}\r\n          </ul>\r\n          <div class=\"newsmore\"><a href=\"http://data.eastmoney.com/stockcomment/stock/{{=it.hscode}}.html#yqjk\">点击查看更多</a></div>\r\n        </div>\r\n        <div class=\"zgb2\">\r\n          <div class=\"scrdd\">\r\n            <div class=\"t\">关注指数</div>\r\n            <div class=\"num\">\r\n              {{? it.data.zj.Market[0].FocusScore >= 60 }}\r\n                <span class=\"stockup\">{{=it.data.zj.Market[0].FocusScore}}</span>\r\n              {{??}}\r\n                <span class=\"stockdown\">{{=it.data.zj.Market[0].FocusScore}}</span>\r\n              {{?}}\r\n            </div>\r\n            <div class=\"intro\">今日用户关注指数为 {{=it.data.zj.Market[0].FocusScore}} 市场排名 {{=it.data.zj.Market[0].Ranking}}/{{=it.data.zj.Market[0].StockCount}}</div>\r\n          </div>\r\n          <div class=\"scrdd\">\r\n            <div class=\"t\">参与意愿</div>\r\n            <div class=\"num\">{{=it.textColor(((it.data.zj.Market[0].Day5HandWishChg / 1) * 100).toFixed(2) + '%', it.data.zj.Market[0].Day5HandWishChg)}}</div>\r\n            <div class=\"intro\">{{=it.data.zj.Market[0].scrd1}} {{=it.data.zj.Market[0].scrd2}}</div>\r\n          </div>\r\n          <div class=\"scrdd\">\r\n            <div class=\"t\">市场成本</div>\r\n            <div class=\"num\">{{=(it.data.zj.Market[0].AvgPrice / 1).toFixed(2)}}</div>\r\n            <div class=\"intro\">今日市场成本为{{=(it.data.zj.Market[0].AvgBuyPrice/1).toFixed(2)}}元，{{=it.data.zj.Market[0].scrd3}}</div>\r\n          </div>\r\n        </div>\r\n        <div class=\"zgb3\">\r\n          <div class=\"zcinfo\">\r\n            <span class=\"icon icon_zc\"></span> 支撑位：<span id=\"zcprice\"></span>元<br>\r\n            <span class=\"icon icon_yl\"></span> 压力位：<span id=\"ylprice\"></span>元<br>\r\n            更新时间： {{=it.data.zj.Trend[0][0].UpdateTime.substring(0, it.data.zj.Trend[0][0].UpdateTime.indexOf(' '))}}\r\n            <div class=\"zcinfot\">{{=it.data.zj.Trend[0][0].qsyp1}}，{{=it.data.zj.Trend[0][0].qsyp2}}</div>\r\n          </div>\r\n          <div class=\"zcchart\" id=\"trend_klinediv\">\r\n            <img src=\"./images/zcyl.png\" alt=\"\">\r\n          </div>\r\n        </div>\r\n        <div class=\"zgb4\">\r\n          <div class=\"zjdx\">\r\n            {{=it.data.zj.Capital[0].zjdx1}}<br>\r\n            今日资金净流入{{=it.textColor(it.formatNum(it.data.zj.Capital[0].MajorNetFlow) + '元', it.data.zj.Capital[0].MajorNetFlow)}}，占流通盘比{{=(it.data.zj.Capital[0].MNFOccuMktVal*100).toFixed(2)}}%<br>\r\n            五日资金净流入{{=it.textColor(it.formatNum(it.data.zj.Capital[0].Day5MajorNetFlow) + '元', it.data.zj.Capital[0].Day5MajorNetFlow)}}，占流通盘比{{=(it.data.zj.Capital[0].Day5MNFOccuMktVal*100).toFixed(2)}}%<br>\r\n            所属{{=it.data.zj.Capital[0].IndustryName}}行业，五日行业资金流入共{{=it.textColor(it.formatNum(it.data.zj.Capital[0].IndustryDay5MajorNet) + '元', it.data.zj.Capital[0].IndustryDay5MajorNet)}}\r\n          </div>\r\n          {{? it.data.zj.Capital[0].ActiveInterval == '' }}\r\n          <div class=\"zjdxinfo\">今日无明显成交活跃时间段，全天统计如下：</div>\r\n          <div class=\"zjdxtj\">\r\n            <table>\r\n              <tr>\r\n                <td>涨跌幅<br>{{=it.textColor(it.data.zj.Capital[0].RChange + '%', it.data.zj.Capital[0].RChange)}}</td>\r\n                <td>成交活跃价格<br>{{=it.textColor(it.data.zj.Capital[0].ActivePrice, it.data.zj.Capital[0].RChange)}}</td>\r\n                <td>成交活跃手数<br><span>{{=it.data.zj.Capital[0].ActiveCount}}</span></td>\r\n              </tr>\r\n            </table>\r\n          </div>\r\n          {{??}}\r\n          <div class=\"zjdxinfo\">今日成交活跃时间为 <span class=\"c_or\">{{=it.data.zj.Capital[0].ActiveInterval}}</span>，区间统计如下：</div>\r\n          <div class=\"zjdxtj\">\r\n            <table>\r\n              <tr>\r\n                <td>区间涨跌幅<br>{{=it.textColor(parseFloat(it.data.zj.Capital[0].IntervalRChange).toFixed(2) + '%', it.data.zj.Capital[0].IntervalRChange)}}</td>\r\n                <td>成交量占当日比<br>{{=it.textColor(it.data.zj.Capital[0].IntervalVolOccupyDayVol + '%', it.data.zj.Capital[0].IntervalVolOccupyDayVol)}}</td>\r\n                <td>主买量占区间比<br><span>{{=it.textColor(it.data.zj.Capital[0].IntervalBuyVolOccupySectVol + '%', it.data.zj.Capital[0].IntervalBuyVolOccupySectVol)}}</span></td>\r\n              </tr>\r\n            </table>\r\n          </div>\r\n          {{?}}\r\n        </div>\r\n        <div class=\"zgb5\">\r\n          <div class=\"jzpg\">\r\n            <div class=\"t\">\r\n              {{=it.data.zj.Value[0][0].SecName}}属于{{=it.data.zj.Value[0][0].IndustryName}}行业<br>排名<span class=\"stockup\">{{=it.data.zj.Value[0][0].ValueRanking}}</span>/{{=it.data.zj.Value[0][0].Total}}\r\n            </div>\r\n            <div class=\"jzpginfo\">{{=it.data.zj.Value[0][0].Comment}}</div>\r\n          </div>\r\n          <div class=\"jzpgchart\" id=\"jzpgchart\"></div>\r\n        </div>\r\n      </div>\r\n    </div>\r\n  </div>\r\n\r\n</div>"

/***/ }),

/***/ "./modules/znzg/znzg_none.html":
/*!*************************************!*\
  !*** ./modules/znzg/znzg_none.html ***!
  \*************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"znzg\">\r\n\r\n  <div class=\"znzgtab znzgsmalltab\">\r\n    <ul>\r\n      <li class=\"on\"><a href=\"javascript:;\" target=\"_self\">分时K线</a></li>\r\n      <li><a href=\"javascript:;\" target=\"_self\">智能诊股</a></li>\r\n    </ul>\r\n  </div>\r\n\r\n\r\n\r\n  <div class=\"fskxd\">\r\n    <div class=\"znzgtab2\">\r\n      <ul class=\"znzgs2tab\">\r\n        <li class=\"on\"><a href=\"javascript:;\" target=\"_self\">分时</a></li>\r\n        <li><a href=\"javascript:;\" target=\"_self\">K线</a></li>\r\n      </ul>      \r\n    </div>\r\n    <a href=\"{{=it.hqlink}}\" id=\"znzgfscharta\"><div class=\"fschart\" id=\"znzgfschart\"></div></a>\r\n    <a href=\"{{=it.hqlink}}\" id=\"znzgkcharta\"><div class=\"kchart\" id=\"znzgkchart\"></div></a>    \r\n  </div>\r\n\r\n  <div class=\"znzg_rc\">\r\n    <div class=\"dcznzg\">\r\n      <div><span class=\"icon icon_znzgtip\"></span></div>\r\n      {{? it.bm60}}\r\n        目前智能诊股只支持上市满六十交易日的沪深A股\r\n      {{??}}\r\n      <div>医者不能自医，换只股票试试</div>\r\n      {{?}}\r\n    </div>\r\n  </div>\r\n\r\n</div>"

/***/ }),

/***/ "./modules/zshq/index.js":
/*!*******************************!*\
  !*** ./modules/zshq/index.js ***!
  \*******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 指数行情
 */
var webconfig = __webpack_require__(/*! ../../config/webconfig */ "./config/webconfig.js")

function gethq(){
  return $.ajax({
    url: webconfig.getWebPath('getpath') + 'api/qt/ulist.np/get?secids=1.000001,0.399001,0.399006,0.399005,8.040120,104.CN00Y,100.HSI,100.DJIA,100.FTSE,100.N225,100.NDX,100.GDAXI,102.CL00Y,101.GC00Y,100.UDI,133.USDCNH,120.USDCNYC,142.scm&fields=f1,f2,f3,f4,f12,f13,f14,f107,f152&ut=6d2ffaa6a585d612eda28417681d58fb&cb=?',
    type: 'GET',
    dataType: 'jsonp'
  })
  .done(function(json) {   
    if (json.rc == 0 && json.data.total == 18) {
      var html = []
      html.push(makeHTML(json.data.diff.slice(0, 6)))
      html.push(makeHTML(json.data.diff.slice(6, 12)))
      html.push(makeHTML(json.data.diff.slice(12, 18)))
      $('#zshq').html(html.join(''))
    }
  })
  .fail(function(error) {
    
  })  
}

function makeHTML(array){
  var html = ['<ul>']
  array.forEach(function(v){

    var classname = 'icon_close'
    if(v.f107 == 1 || v.f107 == 2 ||v.f107 == 4){
      classname = 'icon_open'
    }

    var updown = 'draw'
    if($.isNumeric(v.f4)){
      if(v.f4 > 0){
        updown = 'up'
      }
      if(v.f4 < 0){
        updown = 'down'
      }
    }

    html.push('<li><a href="http://quote.eastmoney.com/unify/r/' + v.f13 + '.' + v.f12 + '"><span class="icon ' + classname + ' "></span> ' + v.f14 + '&nbsp;&nbsp;<span class="stock' + updown + '">' + (v.f2 / Math.pow(10, v.f1)).toFixed(v.f1) + '</span>&nbsp;&nbsp;<span class="stock' + updown + '">' + (v.f4 / Math.pow(10, v.f1)).toFixed(v.f1) + '</span>&nbsp;&nbsp;<span class="stock' + updown + '">' + (v.f3 / 100).toFixed(v.f152) + '%</span></a></li>')
  })
  html.push('</ul>')
  return html.join('')
}


module.exports = function(){
  setInterval(function(){
    gethq()
  }, 30 * 1000);
  gethq()
}

/***/ }),

/***/ "./modules/zxg/batch_edit.js":
/*!***********************************!*\
  !*** ./modules/zxg/batch_edit.js ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 批量修改
 */
var popmenu = __webpack_require__(/*! ../popmenu */ "./modules/popmenu/index.js")
var batch_edit_stock_html = __webpack_require__(/*! ./batch_edit_stock.html */ "./modules/zxg/batch_edit_stock.html")
var dot = __webpack_require__(/*! dot */ "./node_modules/dot/doT.js")
var datacache = __webpack_require__(/*! ../datacache */ "./modules/datacache/index.js")
var modalalert = __webpack_require__(/*! ../modal/alert */ "./modules/modal/alert.js")
var modalcomfirm = __webpack_require__(/*! ../modal/confirm */ "./modules/modal/confirm.js")
var data = __webpack_require__(/*! ./data */ "./modules/zxg/data.js")

module.exports = {
  init: function(){
    var _this = this
    //plsetting

    var html = $(dot.template(batch_edit_stock_html)({

    }))
  
    var newpop = new popmenu({
      target: $('#plsetting'),
      //offsetx: -25,
      content: html,
      onMoveIn: function(){
        var groupdata = datacache.groupdata.groups.filter(function(v){
          if (v.id == datacache.groupdata.horder || v.id == datacache.thisgroupid) {
            return false
          }
          return true
        })
        $('.popmenud2list', html).html(groupdata.map(function(v){
          return '<li><a href="javascript:;" class="movegroup" target="_self" data-groupid="' + v.id + '">' + v.name + '</a></li>'
        }).join(''))
      },
      onHover: function(){
        var w = html.offset().left + html.width() + 120
        //console.info(w)
        if (w > $('body').width()) {
          $('.editgroupname', html).html('<span class="icon icon_larrow"></span> 修改分组')
          $('.popmenud2list', html).css({right: '100%', left: 'auto'}).addClass('popmenud2listsd2')
          //console.info(111)
        }
        else{
          $('.editgroupname', html).html('修改分组 &nbsp;<span class="icon icon_rarrow"></span>')
          $('.popmenud2list', html).css({right: 'auto', left: '100%'}).removeClass('popmenud2listsd2')
        }
      }
    })

    html.on('click', '.deletestock', function(){
      _this.deleteStock()
    })

    html.on('click', '.movegroup', function(){
      var togroupid = $(this).data('groupid')
      _this.moveGroup(togroupid)
    })    
  },
  getCodes: function(){
    var codes = []
    $('#wl_mainbody .batchselect').each(function(i, v){
      if ($(v).is(':checked')) {
        codes.push($(v).val())
      }
    })
    return codes
  },
  deleteStock: function(){
    var codes = this.getCodes()
    if (codes.length == 0) {
      modalalert('请至少选择一只股票！')
      return false
    }

    modalcomfirm('确定要删除这些自选股吗？', function(){
      data.batchDelete(codes.join(','), datacache.thisgroupid)
      .then(function(json){
        if (json.re) {
          if (datacache.is_defaultgroup) { //处理置顶股票
            _.pullAll(datacache.top_stocks, codes)
          } 
          //modalalert('删除成功！', function(){
            datacache.changeGroup()
          //})
        }
      })      
    })
  },
  moveGroup: function(togroupid){
    var codes = this.getCodes()
    if (codes.length == 0) {
      modalalert('请至少选择一只股票！')
      return false
    }



    data.moveGroup(codes.join(','), datacache.thisgroupid, togroupid)
    .then(function(json){
      if (json.re) {
        
        if (datacache.is_defaultgroup) { //处理置顶股票
          _.pullAll(datacache.top_stocks, codes)
        }        
        modalalert('移动成功！', function(){
          datacache.changeGroup(togroupid)
        })
      }
      else{
        modalalert(json.message)
      }
    })      
  }
}

/***/ }),

/***/ "./modules/zxg/batch_edit_stock.html":
/*!*******************************************!*\
  !*** ./modules/zxg/batch_edit_stock.html ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div>\r\n<ul class=\"popmenulist\">\r\n  <li><a href=\"javascript:;\" class=\"deletestock\" target=\"_self\">删除</a></li>\r\n  <li><a href=\"javascript:;\" class=\"editgroupname\" target=\"_self\">修改分组 &nbsp;<span class=\"icon icon_rarrow\"></span></a>\r\n    <ul class=\"popmenud2list\"></ul>\r\n  </li>\r\n</ul>\r\n\r\n</div>\r\n"

/***/ }),

/***/ "./modules/zxg/customitem.js":
/*!***********************************!*\
  !*** ./modules/zxg/customitem.js ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 指标设置
 */

var zbsetting_html = __webpack_require__(/*! ./zbsetting.html */ "./modules/zxg/zbsetting.html")
var dot = __webpack_require__(/*! dot */ "./node_modules/dot/doT.js")
var modal = __webpack_require__(/*! ../modal */ "./modules/modal/index.js")
var itemconfig = __webpack_require__(/*! ./itemconfig */ "./modules/zxg/itemconfig.js")
var getuid = __webpack_require__(/*! ../user/getuid */ "./modules/user/getuid.js")
var modalalert = __webpack_require__(/*! ../modal/alert */ "./modules/modal/alert.js")
var datacache = __webpack_require__(/*! ../datacache */ "./modules/datacache/index.js")

module.exports = {
  bindBtn: function(){
    var _this = this
    $('#zbsetting').click(function(){
      _this.showSetting()
    })
        
    setTimeout(function(){
      if (self.location.hash == '#showzb') {
        _this.showSetting()
        self.location.hash = ''
      }
    }, 1000);
  },
  showSetting: function(){
    var _this = this


    var html = $(dot.template(zbsetting_html)({
      default_zb: itemconfig.type_config.default_zx.show_fields.map(function(v){
        return {
          //disabled: v == 'f12' || v == 'f14' || v == 'z1',
          name: itemconfig.item_config[v].name,
          itemname: v
        }
      })
    }))

    $('#zbssel1', html).html(this.allFill())
    //$('#zbssel2', html).html(this.defaultFill())
    this.getFill().then(function(optionhtml){
      $('#zbssel2', html).html(optionhtml)
      _this.setDisabled()  
    })

    var newmodal = this.modal = new modal({
      content: html,
      title: '指标设置'
    })

    newmodal.show()
     

    this.bind(html)

    $('#setting_cancel', html).click(function(){
      newmodal.close()
    })

    $('#setting_submit', html).click(function(){
      _this.submit(html)
    })

      

  },
  bind: function(html){
    var _this = this
    var zbssel1 = $('#zbssel1', html)
    var zbssel2 = $('#zbssel2', html)

    zbssel1.focus(function(){
      $('#additem', html).addClass('modalbtn_default').removeClass('modalbtn_disabled')
    })

    zbssel2.focus(function(){
      $('#delitem', html).add('#moveup', html).add('#movedown', html).addClass('modalbtn_default').removeClass('modalbtn_disabled')
    }) 

    //添加按钮
    $('#additem', html).click(function(){
      var selitem = $('option:selected', zbssel1)
      if (selitem.length) {
        selitem.each(function(i, v){

          var hasitem = false //检测是否已经有此项
          $('option', zbssel2).each(function(i2, v2){
            if ($(v2).val() == $(v).val()) {
              hasitem = true
              return false
            }
          })
          if (!hasitem) {
            zbssel2.append('<option value=' + $(v).val() + '>' + $(v).text() + '</option>')
            _this.setDisabled()
            $('#zbssel1').get(0).options.selectedIndex = -1
          }

        })
      }
    })
    
    //双击添加
    $('option', zbssel1).dblclick(function(){
      var thisoption = $(this)
      var hasitem = false //检测是否已经有此项
      $('option', zbssel2).each(function(i2, v2){
        if ($(v2).val() == thisoption.val()) {
          hasitem = true
          return false
        }
      })
      if (!hasitem) {
        zbssel2.append('<option value=' + thisoption.val() + '>' + thisoption.text() + '</option>')    
        _this.setDisabled()      
        $('#zbssel1').get(0).options.selectedIndex = -1  
      }      
    })

    //删除按钮
    $('#delitem', html).click(function(){
      var selitem = $('option:selected', zbssel2)
      if (selitem.length) {
        selitem.remove()
        $('#delitem', html).add('#moveup', html).add('#movedown', html).addClass('modalbtn_disabled').removeClass('modalbtn_default')
        _this.setDisabled()
      }
    })    

    //上移
    $('#moveup', html).click(function(){
      var selitem = $('option:selected', zbssel2)
      if (selitem.length) {
        var previtem = selitem.eq(0).prev()
      if (previtem.attr('disabled')) {
        return false
      }
        previtem.before(selitem)
      }
    })     

    //下移
    $('#movedown', html).click(function(){
      var selitem = $('option:selected', zbssel2)
      if (selitem.length) {
        var previtem = selitem.last().next()
        previtem.after(selitem)
      }
    })

    //重置
    $('#resetbtn', html).click(function(){
      zbssel2.html(_this.defaultFill())
      $('#delitem', html).add('#moveup', html).add('#movedown', html).addClass('modalbtn_disabled').removeClass('modalbtn_default')
      _this.setDisabled()
      return false
    })

    //清空
    $('#clearbtn', html).click(function(){
      zbssel2.html(_this.clearFill())
      $('#delitem', html).add('#moveup', html).add('#movedown', html).addClass('modalbtn_disabled').removeClass('modalbtn_default')
      _this.setDisabled()
      return false
    })

    //



  },
  //已有指标变成不可选择
  setDisabled: function(){
    var zbssel1 = $('#zbssel1')
    var zbssel2 = $('#zbssel2')
    $('option', zbssel1).not('.dloption').prop('disabled', false)
    $('option', zbssel2).each(function(i, v){
      $('option[value="' + $(v).val() + '"]', zbssel1).prop('disabled', true)
    })
  },
  /**
   * 所有选项
   */
  allFill: function(){
    var html = []
    itemconfig.type_config.all_zx.show_fields.forEach(function(v){
      html.push('<option ')
      if (!/[a-z]/.test(v.substring(0, 1))) {
        html.push('class="dloption" disabled')
        html.push(' >' + v + '</option>') 
      }
      else{
        html.push(' value="' + v + '">' + itemconfig.item_config[v].name + '</option>')        
      }
    })
    return html.join('')    
  },
  /**
   * 重置
   */
  defaultFill: function(){
    var html = []
    itemconfig.type_config.default_zx.show_fields.forEach(function(v){
      html.push('<option ')
      // if (v == 'f12' || v == 'f14' || v == 'z1') {
      //   html.push('disabled')
      // }
      html.push(' value="' + v + '">' + itemconfig.item_config[v].name + '</option>')
    })
    return html.join('')
  },
  getFill: function(){
    return this.getSetting('zx').then(function(data){
      var html = []
      data.forEach(function(v){
        html.push('<option ')
        // if (v == 'f12' || v == 'f14' || v == 'z1') {
        //   html.push('disabled')
        // }
        html.push(' value="' + v + '">' + itemconfig.item_config[v].name + '</option>')
      })
      return html.join('')
    })
  },
  /**
   * 清空
   */
  clearFill: function(){
    var html = []
    // html.push('<option disabled value="f12">代码</option>')
    // html.push('<option disabled value="f14">名称</option>')
    // html.push('<option disabled value="z1">股吧</option>')
    return html.join('')    
  },
  submit: function(html){
    //var zbssel1 = $('#zbssel1', html)
    var zbssel2 = $('#zbssel2', html)
    var submit_data = []
    $('option', zbssel2).each(function(i, v){
      submit_data.push({
        itemname: $(v).text(),
        name: $(v).val()
      })
    })
    // console.info(submit_data)
    this.save(submit_data)
    return false
  },
  /**
   * 是否和默认设置一样
   */
  isDefault: function(data){
    if (data.length != itemconfig.type_config.default_zx.show_fields.length) {
      return false
    }
    var isdefault = true
    data.forEach(function(v, i){
      if(data[i].name != itemconfig.type_config.default_zx.show_fields[i]){
        isdefault = false
      }
    })
    return isdefault
  },
  save: function(data){
    var _this = this

    if (!window.localStorage) {
      modalalert('您的浏览器不支持本地保存！您的设置不会被保存')
      return false
    }

    var groupid = datacache.thisgroupid

    getuid.get().then(function(uid){
      var key = uid + '_' + groupid
      var zxgdata = localStorage.getItem('zxg')
      if (zxgdata != null) {
        zxgdata = JSON.parse(zxgdata)
      }
      else{
        zxgdata = {}
      }

      if (zxgdata.customitem == undefined) {
        zxgdata.customitem = {}
      }

      if (_this.isDefault(data)) {
        try{
          delete zxgdata.customitem[key]
        }
        catch(error){
        }
        
      }
      else{
        zxgdata.customitem[key] = data.map(function(v){
          return v.name
        })

         
      }

      localStorage.setItem('zxg', JSON.stringify(zxgdata))       

      _this.modal.close()
      modalalert('保存成功！', function(){
        datacache.changeShowType('zx', 0)
      })
      //localStorage.setItem('zxg', )
    })
  },
  /**
   * 获取我的自选字段设置
   * @param {*} type 
   */
  getSetting: function(type){
    var _this = this
    var groupid = datacache.thisgroupid
    var default_data = itemconfig.type_config.default_zx.show_fields

    if (type != 'zx') {
      return Promise.resolve(itemconfig.type_config[type].show_fields)
    }

    if (!window.localStorage) {
      return Promise.resolve(default_data)
    }

    return getuid.get().then(function(uid){
      var key = uid + '_' + groupid
      var zxgdata = localStorage.getItem('zxg')
      if (zxgdata == null) {
        return default_data
      }
      zxgdata = JSON.parse(zxgdata)
      if (zxgdata.customitem == undefined || zxgdata.customitem[key] == undefined) {
        return default_data
      }
      return _.difference(zxgdata.customitem[key], itemconfig.type_config.required.show_fields)
    })
  }

}

/***/ }),

/***/ "./modules/zxg/data.js":
/*!*****************************!*\
  !*** ./modules/zxg/data.js ***!
  \*****************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * 自选股数据层
 */

module.exports = {
  /**
   * 移动分组
   * @param {*} code 
   * @param {*} fromgroupid 
   * @param {*} togroupid 
   */
  moveGroup: function(code, fromgroupid, togroupid){
    return $.ajax({
      url: './api/zxg/movegroup',
      type: 'POST',
      dataType: 'json',
      data: {
        code: code,
        fromgroupid: fromgroupid,
        togroupid: togroupid
      }
    })
  },
  batchDelete: function(codes, groupid){
    return $.ajax({
        url: './api/zxg/batchdeletestock',
        type: 'POST',
        dataType: 'json',
        data: {
          codes: codes,
          groupid: groupid
        }
      })
  }
}

/***/ }),

/***/ "./modules/zxg/dgtl.html":
/*!*******************************!*\
  !*** ./modules/zxg/dgtl.html ***!
  \*******************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"dgtldiv sscroll\">\r\n  <ul id=\"dgtllist\">\r\n    {{~it.stocklist :value:index}}\r\n    <li><a href=\"{{=it.text.getLinkByCode(value.code)}}\"><img src=\"//webquotepic.eastmoney.com/GetPic.aspx?nid={{=value.code}}&imagetype={{=value.imgmoban}}&rnd={{=it.rnd}}\" alt=\"\"></a></li>\r\n    {{~}}\r\n  </ul>\r\n  <div class=\"pager\" id=\"dgtlpager\">\r\n    {{=it.pagerhtml}}\r\n  </div>\r\n</div>"

/***/ }),

/***/ "./modules/zxg/dgtl.js":
/*!*****************************!*\
  !*** ./modules/zxg/dgtl.js ***!
  \*****************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 多股同列
 */

var dot = __webpack_require__(/*! dot */ "./node_modules/dot/doT.js")
var dgtl_html = __webpack_require__(/*! ./dgtl.html */ "./modules/zxg/dgtl.html")
var pager = __webpack_require__(/*! ../pager */ "./modules/pager/index.js")
var text = __webpack_require__(/*! ../text */ "./modules/text/index.js")
var datacache = __webpack_require__(/*! ../datacache */ "./modules/datacache/index.js")
var hegui = __webpack_require__(/*! ../hegui */ "./modules/hegui/index.js")


var dgtl = {
  zscd: null,
  show: function(stockcodes){
    dgtl.showPage(stockcodes, 1)
    try{
      clearInterval(dgtl.zscd)
    }
    catch(error){
    }
    dgtl.zscd = setInterval(function() {
      if (datacache.thisshowtype != 'dgtl') {
        try{
          clearInterval(dgtl.zscd)
        }
        catch(error){
        }        
        return false
      }
      dgtl.showPage(stockcodes, dgtl.thispage)
    }, 30 * 1000);
  },
  thispage: 1,
  showPage: function(stockcodes, pageindex){
    var _this = dgtl
    _this.thispage = pageindex
    var showdata = stockcodes.slice(12 * (pageindex - 1), 12 * pageindex)
    var isHKDelay = hegui.isHKDelay()
    var showstocklist = showdata.map(function(v){
      var imgmoban = 'ZXGINDEX'
      if (v.indexOf('116.') == 0 && isHKDelay > 0) {
        imgmoban = 'ZXGINDEX_D'
      }
      return {
        imgmoban: imgmoban,
        code: v
      }
    })
    // console.info(showdata)
    var html = $(dot.template(dgtl_html)({
      stocklist: showstocklist,
      text: text,
      pagerhtml: dgtl.pager(stockcodes.length, pageindex),
      rnd: Math.floor(Math.random()*99999+1)
    }))
    $('#wl_mainbody').html(html)
    $('img', html).one('error', function(){
      setTimeout(function(){
        //console.info(222)
        $(this).attr('src', $(this).attr('src'))
      }.bind(dgtl), 500);
    })

    $('#dgtlpager a').click(function(){
      var page = $(this).data('page')
      _this.showPage(stockcodes, page)
      return false
    })
  },
  pager: function(max, pageindex){
    var pagerhtml = ''
    pagerhtml = pager(pageindex, 12, max, 'javascript:;')
    return pagerhtml
  },
  /**
   * 使用行情接口过滤股票列表，去掉一些没有行情的过期代码
   * @param {*} codelist 
   */
  filterCodeList: function(codelist){
    return $.ajax({
      url: 'https://push2.eastmoney.com/api/qt/ulist.np/get?fields=f12,f13&ut=6d2ffaa6a585d612eda28417681d58fb&cb=?',
      type: 'GET',
      dataType: 'jsonp',
      data: {
        secids: codelist.join(',')
      }
    })
    .then(function(json) { 
      var back = []
      json.data.diff.forEach(function(v){
        back.push(v.f13.toString() + '.' + v.f12.toString())
      })
      return back
    })
  }
}

module.exports = dgtl

/***/ }),

/***/ "./modules/zxg/dragdrop.js":
/*!*********************************!*\
  !*** ./modules/zxg/dragdrop.js ***!
  \*********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 拖动排序
 */

var datacache = __webpack_require__(/*! ../datacache */ "./modules/datacache/index.js")
var debounce = __webpack_require__(/*! lodash/debounce */ "./node_modules/lodash/debounce.js")
var znzg = __webpack_require__(/*! ../znzg */ "./modules/znzg/index.js")

module.exports = {
  init: function(){
    if (datacache.pxorder) {
      return false
    }
    var _this = this
    var c = {};
    //var ml = $('#tablethd4').width()
    var fromindex = 0
    var toindex = 0

    $("#wltable tr").draggable({
      //helper: "clone",
      helper: function(){
        //console.info(111)
        znzg.close()
        //return '<div>aa</div>'
        //console.info(this)
        
        //return '<div>aaa</div>'
        //console.info($(this).index())
        //console.info(_this.getHelper($(this).index()))
        return _this.getHelper($(this).index())
      },
      axis: "y",
      containment: 'parent',   //'parent'$('#tablethdd5') $('#drapcontain')
      cursor: "move",
      opacity: 0.7,
      //"grid": [ 0, 39 ],
      //zIndex: 10,
      //appendTo: $('#drapcontain'),
      start: function(event, ui) {
        //console.info(111)
        var index = $(this).index()
        fromindex = index
        //$(this).hide()
        $('#tablethdd5').scrollLeft(0)
        $('#tablethdd5').css({'z-index':10})

        //$('#tablethd4 tr:eq(' + index + ')').hide()
        //$('#wltable tr:eq(' + index + ')').hide()

        //ml = $('#tablethd4').width()

        //console.info(this)
        //console.info($(this).index())
          //c.tr = this;
          //c.helper = ui.helper;
      }
    });


    $("#wltable tr").droppable({
      cursor: "move",
      //greedy: true,
      // classes: {
      //       "ui-droppable-hover": "dropon"
      //     },
        drop: function(event, ui) {
          //console.info(222)
          var index = $(this).index()
          //console.info(222)


          toindex = index

          _this.moveStock(fromindex, toindex)
            // var inventor = ui.draggable.text();
            // $(this).find("input").val(inventor);

            // $(c.tr).remove();
            // $(c.helper).remove();
        },
        deactivate: debounce(function(){
          //console.info(333)
          $('#tablethdd5').css({'z-index':5})
          //console.info(index)
          //console.info(ui)
          $('#tablethd4 tr').removeClass('dropon')
          $('#wltable tr').removeClass('dropon')          
        }, 200),
        over: function(event, ui){
          //console.info(111)
          var index = $(this).index()

          //console.info(index)
          $('#tablethd4 tr').removeClass('dropon')
          $('#tablethd4 tr:eq(' + index + ')').addClass('dropon')

          $('#wltable tr').removeClass('dropon')
          $('#wltable tr:eq(' + index + ')').addClass('dropon')
          
        }
    });


    $("#tablethdd4 tr").draggable({
      //helper: "clone",
      helper: function(){
        //console.info(111)
        znzg.close()
        //return '<div>aa</div>'
        //console.info(this)
        
        //return '<div>aaa</div>'
        //console.info($(this).index())
        //console.info(_this.getHelper($(this).index()))
        return _this.getHelper($(this).index(), true)
      },
      axis: "y",
      containment: 'parent',   //'parent'$('#tablethdd5') $('#drapcontain')
      cursor: "move",
      opacity: 0.7,
      //"grid": [ 0, 39 ],
      //zIndex: 10,
      //appendTo: $('#drapcontain'),
      start: function(event, ui) {
        //console.info(111)
        var index = $(this).index()
        fromindex = index
        //$(this).hide()
        $('#tablethdd5').scrollLeft(0)
        $('#tablethdd5').css({'z-index':10})

        //$('#tablethd4 tr:eq(' + index + ')').hide()
        //$('#wltable tr:eq(' + index + ')').hide()

        //ml = $('#tablethd4').width()

        //console.info(this)
        //console.info($(this).index())
          //c.tr = this;
          //c.helper = ui.helper;
      }
    });


    $("#tablethdd4 tr").droppable({
      cursor: "move",
      //greedy: true,
      // classes: {
      //       "ui-droppable-hover": "dropon"
      //     },
        drop: function(event, ui) {
          //console.info(222)
          var index = $(this).index()
          //console.info(222)


          toindex = index

          _this.moveStock(fromindex, toindex)
            // var inventor = ui.draggable.text();
            // $(this).find("input").val(inventor);

            // $(c.tr).remove();
            // $(c.helper).remove();
        },
        deactivate: debounce(function(){
          //console.info(333)
          $('#tablethdd5').css({'z-index':5})
          //console.info(index)
          //console.info(ui)
          $('#tablethd4 tr').removeClass('dropon')
          $('#wltable tr').removeClass('dropon')          
        }, 200),
        over: function(event, ui){
          //console.info(111)
          var index = $(this).index()

          //console.info(index)
          $('#tablethd4 tr').removeClass('dropon')
          $('#tablethd4 tr:eq(' + index + ')').addClass('dropon')

          $('#wltable tr').removeClass('dropon')
          $('#wltable tr:eq(' + index + ')').addClass('dropon')
          
        }
    });



  },
  getHelper: function(index, isleft){
    var ml = $('#tablethd4').width()
    if (isleft) {
      ml = 0
    }
    var t4trd = $('#tablethd4 tr:eq(' + index + ') td')
    var t5trd =  $('#wltable tr:eq(' + index + ') td')
    var helpertable = $('<table style="margin-left:-' + ml + 'px;" class="tablethd tabledrag"><tr></tr></table>')

    var trs = t4trd
    if (!isleft) {
      trs = t4trd.add(t5trd)
    }
    trs.each(function(i, v){
      var td
      if (i == 0) {
        td = $('<td style="width:' + v.clientWidth + 'px"><em></em></td>')
      }
      else{
        td = $('<td style="width:' + v.clientWidth + 'px"><em>' + $(v).text() + '</em></td>')
      }


      $('tr', helpertable).append(td)

    })
    //helpertable.css({'margin-left': -helpertable})
    return helpertable
    //tablethd
  },
  moveStock: function(fromindex, toindex){



    //console.info(fromindex)
    //console.info(toindex)
    //return 
    var code = $('#tablethd4>tr:eq(' + fromindex + ')').data('code').toString()

    var pretr = $('#tablethd4>tr:eq(' + (toindex - 1) + ')')
    var nexttr = $('#tablethd4>tr:eq(' + toindex + ')')
    //console.info(pretr.data('code'))
    //console.info(pretr.data('code'))
    var precode = pretr.data('code').toString()
    var nextcode = nexttr.data('code').toString()

    // console.info(code)
    //  console.info(precode)
    //  console.info(nextcode)

    precode = precode || ''
    nextcode = nextcode || ''

    if (toindex == 0) {
      precode = ''
    }

    //console.info('drop')



  //  if (datacache.is_defaultgroup) {
      var nextistop = nexttr.is('.topcode')
      var codes = []
      var topcodes = []
      $('#tablethd4>tr').each(function(i, v){
        var thiscode = $(this).data('code').toString()
        if (i == fromindex) {
          return true
        }
        if (i == toindex) {
          if (nextistop) {
            topcodes.push(code)
          }
          else{
            codes.push(code)
          }
        }
        if ($(this).is('.topcode')) {
          topcodes.push(thiscode)
        }
        else{
          codes.push(thiscode)
        }
      })

      //console.info(topcodes)
      //console.info(codes)

      //return false

      var senddata = {
          codes: codes.reverse().join(','),
          groupid: datacache.thisgroupid,
        }

      if (datacache.is_defaultgroup) {
        senddata.topgroupid = datacache.topgroupid
        senddata.topcodes = topcodes.reverse().join(',')
        if (senddata.topcodes) {
          senddata.codes = senddata.codes + ',' + senddata.topcodes
        }
        
        // console.info(senddata.codes)
      }
      // console.info(senddata)
      //return false

      $.ajax({
        url: './api/zxg/batchedit',
        type: 'POST',
        dataType: 'json',
        data: senddata
      })
      .done(function(json) {   
        if (json.re) {
          //console.info(111)
          if (datacache.is_defaultgroup) {
            datacache.top_stocks = senddata.topcodes.split(',').reverse()
          }
          
          datacache.changeGroup()
          
          //移动的视觉效果
          var thistr1 = $('#tablethd4 tr:eq(' + fromindex + ')')
          var thistr2 = $('#wltable tr:eq(' + fromindex + ')')

          $('#tablethd4 tr:eq(' + toindex + ')').before(thistr1)
          $('#wltable tr:eq(' + toindex + ')').before(thistr2)
        }
      })
      .fail(function(error) {
        
      })    
//    }
    // else{
    //   $.ajax({
    //     url: './api/zxg/move',
    //     type: 'POST',
    //     dataType: 'json',
    //     data: {
    //       code: code,
    //       groupid: datacache.thisgroupid,
    //       upcode: precode,
    //       downcode: nextcode
    //     }
    //   })
    //   .done(function(json) {   
    //     if (json.re) {
    //       //console.info(111)
    //       datacache.changeGroup()
    //     }
    //   })
    //   .fail(function(error) {
        
    //   })      
    // }

  }
}

/***/ }),

/***/ "./modules/zxg/edit_group.js":
/*!***********************************!*\
  !*** ./modules/zxg/edit_group.js ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 修改组合
 */

var popmenu = __webpack_require__(/*! ../popmenu */ "./modules/popmenu/index.js")
var modal = __webpack_require__(/*! ../modal */ "./modules/modal/index.js")
var modalalert = __webpack_require__(/*! ../modal/alert */ "./modules/modal/alert.js")
var modalconfirm = __webpack_require__(/*! ../modal/confirm */ "./modules/modal/confirm.js")
var dom = __webpack_require__(/*! ../dom */ "./modules/dom/index.js")
var datacache = __webpack_require__(/*! ../datacache */ "./modules/datacache/index.js")
var data = __webpack_require__(/*! ./data */ "./modules/zxg/data.js")


module.exports = {
  bind: function(){
    // var _this = this
    // // var group_lis = $('#zxggrouplist li')
    // // var _this = this
    // // group_lis.each(function(i, v){
    // //   if (i == 0) {
    // //     return
    // //   }
    // //   var thisli = $(v)
    // //   if (!thisli.data('groupid')) {
    // //     return
    // //   }
    // //   var newpop = new popmenu({
    // //     target: thisli,
    // //     items: ['<a href="javascript:;" class="editgroupname" target="_self">修改名称</a>', '<a href="javascript:;" class="deletegroup" target="_self">删除组合</a>']
    // //   })
    // //   $('.editgroupname', newpop.html).click(function(){
    // //     _this.editGroupName($(v).data('groupid'), $(v).data('groupname'), thisli)
    // //   })
    // //   $('.deletegroup', newpop.html).click(function(){
    // //     _this.deleteGroup($(v).data('groupid'), $(v).data('groupname'), thisli)
    // //   })
    // // })
    // $('#zxggrouplist').on('click', '.groupeditli li', function(){
    //   var groupname = $(this).data('groupname')
    //   var groupid = $(this).data('groupid')
    //   var thispli = $(this).parents('li')
    //   if ($(this).is('.modygroupli')) {
    //     _this.editGroupName(groupid, groupname, thispli)
    //   }
    //   else if($(this).is('.deletegroupli')){
    //     _this.deleteGroup(groupid, groupname, thispli)
    //   }
    //})
  }

}

/***/ }),

/***/ "./modules/zxg/edit_stock.html":
/*!*************************************!*\
  !*** ./modules/zxg/edit_stock.html ***!
  \*************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div>\r\n  <ul class=\"popmenulist\">\r\n    <li><a href=\"javascript:;\" class=\"deletestock\" target=\"_self\">删除</a></li>\r\n    {{? it.isdefaultgroup }}\r\n    <li class=\"settopli\"><a href=\"javascript:;\" class=\"settop\" target=\"_self\">置顶</a></li>\r\n    <li class=\"canceltopli\"><a href=\"javascript:;\" class=\"canceltop\" target=\"_self\">取消置顶</a></li>\r\n    {{?}}\r\n    <li><a href=\"javascript:;\" class=\"editgroupname\" target=\"_self\">修改分组 &nbsp;<span class=\"icon icon_rarrow\"></span></a>\r\n      <ul class=\"popmenud2list\">\r\n        {{~it.groupdata :value:index}}\r\n        <li><a href=\"javascript:;\" class=\"movegroup\" target=\"_self\" data-groupid=\"{{=value.id}}\">{{=value.name}}</a></li>\r\n        {{~}}\r\n      </ul>\r\n    </li>\r\n    <li><a href=\"javascript:;\" class=\"editnote\" target=\"_self\">交易笔记</a></li>\r\n    <li class=\"addtixingli\"><a href=\"javascript:;\" class=\"addtixing\" target=\"_self\">加提醒</a></li>\r\n  </ul>\r\n</div>"

/***/ }),

/***/ "./modules/zxg/edit_stock.js":
/*!***********************************!*\
  !*** ./modules/zxg/edit_stock.js ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 修改自选股
 */

var popmenu = __webpack_require__(/*! ../popmenu */ "./modules/popmenu/index.js")
var modal = __webpack_require__(/*! ../modal */ "./modules/modal/index.js")
var edit_stock_html = __webpack_require__(/*! ./edit_stock.html */ "./modules/zxg/edit_stock.html")
var modalconfirm = __webpack_require__(/*! ../modal/confirm */ "./modules/modal/confirm.js")
var modalalert = __webpack_require__(/*! ../modal/alert */ "./modules/modal/alert.js")
var dot = __webpack_require__(/*! dot */ "./node_modules/dot/doT.js")
var datacache = __webpack_require__(/*! ../datacache */ "./modules/datacache/index.js")
var note_html = __webpack_require__(/*! ./note.html */ "./modules/zxg/note.html")
var quote = __webpack_require__(/*! ../quote */ "./modules/quote/index.js")
var note = __webpack_require__(/*! ./note */ "./modules/zxg/note.js")
var addtixing = __webpack_require__(/*! ../tixing/addtixing */ "./modules/tixing/addtixing.js")
var edit_group = __webpack_require__(/*! ./edit_group */ "./modules/zxg/edit_group.js")
var groups = __webpack_require__(/*! ./groups */ "./modules/zxg/groups.js")
var text = __webpack_require__(/*! ../text */ "./modules/text/index.js")

module.exports = { 
  bindOption : function(){
    var _this = this

    var groupdata = datacache.groupdata.groups.filter(function(v){
      if (v.id == datacache.groupdata.horder || v.id == datacache.thisgroupid) {
        return false
      }
      return true
    })

    var html = dot.template(edit_stock_html)({
      groupdata: groupdata,
      isdefaultgroup: datacache.is_defaultgroup
    })

    $('#tablethd6 .stockoptiontd').each(function(i, v){
      //console.info(html)
      var pophtml = $(html)
      //console.info(html)
      var thistd = $(v)
      var code = thistd.data('code').toString()
      var name = thistd.data('name')      

      //判断是否支持加提醒
      var m = thistd.data('m')
      var t = thistd.data('t')
      if (!addtixing.hasTiXing(m, t)) {
        $('.addtixingli', pophtml).remove()
      }

      var istop = (datacache.top_stocks.indexOf(code) >= 0)

      if (istop) {
        $('.settopli', pophtml).hide()
      }
      else{
        $('.canceltopli', pophtml).hide()
      }

      var newpop = new popmenu({
        target: $('em', thistd),
        offsetx: -45,
        content: pophtml,
        onHover: function(){
          var w = pophtml.offset().left + pophtml.width() + 120
          //console.info(w)
          if (w > $('body').width()) {
            $('.editgroupname', pophtml).html('<span class="icon icon_larrow"></span> 修改分组')
            $('.popmenud2list', pophtml).css({right: '100%', left: 'auto'}).addClass('popmenud2listsd2')
            //console.info(111)
          }
          else{
            $('.editgroupname', pophtml).html('修改分组 &nbsp;<span class="icon icon_rarrow"></span>')
            $('.popmenud2list', pophtml).css({right: 'auto', left: '100%'}).removeClass('popmenud2listsd2')
          }
        }
      })

      $('.deletestock', newpop.html).click(function(){
        _this.deleteStock(code, name)
        return false
      })
      $('.editnote', newpop.html).click(function(){
        _this.editnote(code, name)
        return false
      })
      $('.addtixing', newpop.html).click(function(){
        addtixing.add(code, name)
        return false
      })
      $('.settop', newpop.html).click(function(){
        _this.setTop(code)
        return false
      })   
      $('.canceltop', newpop.html).click(function(){
        _this.cancelTop(code)
        return false
      })           
      $('.movegroup', newpop.html).click(function(){
        var togroupid = $(this).data('groupid')
        groups.moveGroup(code, datacache.thisgroupid, togroupid)
        return false
      })      
    })
  },
  /**
   * 删除自选股
   * @param {*} code 
   */
  deleteStock: function(code, name){
    code = code.toString()
    var issubmit = false
    modalconfirm('确定要删除 [' + name + '] 自选股吗？', function(){
      if (issubmit) {
        return false
      }
      issubmit = true

      $.ajax({
        url: './api/zxg/deletestock',
        type: 'POST',
        dataType: 'json',
        data: {
          code: code,
          groupid: datacache.thisgroupid
        }
      })
      .done(function(json) {   
        if (json.re) {
          //modalalert('删除成功')
          _.pull(datacache.top_stocks, code)
          datacache.changeGroup()
        }
        else{
          modalalert(json.message)
        }
      })
      .fail(function(error) {
        modalalert(error.statusText)
      })
      .always(function(){
        issubmit = false
      }) 
    })
  },
  /**
   * 交易笔记
   * @param {*} code 
   * @param {*} name 
   */
  editnote: function(code, name){
    code = code.toString()
    var _this = this
    var groupid = datacache.thisgroupid
    var oldcode = code.substring(code.indexOf('.') + 1)

    Promise.all([
      note.getNoteData(groupid, code),
      quote.getStockBaseInfo(code)
    ])
    .then(function(backdata){
      var notedata = backdata[0][0]
      var quotedata = backdata[1]
      var nowprice = quotedata.f2 / (Math.pow(10, quotedata.f1))

      var inputdate = notedata.date.split('|')[0]
      var thatprice = notedata.date.split('|')[1]
      inputdate = inputdate.substring(0, 4) + '-' + inputdate.substring(4, 6) + '-' + inputdate.substring(6)

      var data = notedata.note.split('|')
      if (!notedata.note) {
        data = [
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          '',
          ''
        ]
      }      

      var html = $(dot.template(note_html)({
        name: name,
        code: oldcode,
        inputdate: inputdate,
        thatprice: thatprice,
        nowprice: text.textColor(nowprice, quotedata.f4),
        data: data
      }))
      var newmodal = new modal({
        content: html,
        title: '交易管理'
      })

      newmodal.show() 

      _this.bindNoteForm($('#noteform', html), groupid, code, newmodal)

      $('.modalbtn_cancel', html).click(function(){
        newmodal.close()
      })
    })
  },
  bindNoteForm: function(thisform, groupid, code, newmodal){

    var issubmit = false

    thisform.submit(function(){
      
      var c = $.trim($('.c',thisform).val())
      var p = $.trim($('.p',thisform).val())
      var m = $.trim($('.m',thisform).val())
      var z = $.trim($('.z',thisform).val())
      var y = $.trim($('.y',thisform).val())
      var x = $.trim($('.x',thisform).val())
      var h = $.trim($('.h',thisform).val())
      var r = $.trim($('.r',thisform).val())
      var b = $.trim($('.b',thisform).val())

      if (issubmit) {
        return false
      }
      issubmit = true

      $.ajax({
        url: './api/zxg/editnote',
        type: 'POST',
        dataType: 'json',
        data: {
          code: code,
          groupid: groupid,
          c: c,
          p: p,
          m: m,
          z: z,
          y: y,
          x: x,
          h: h,
          r: r,
          b: b
        }
      })
      .done(function(json) {   
        if (json.re) {
          modalalert('修改成功', function(){
            newmodal.close()
          })
          if (datacache.thisshowtype == 'ykyl') {
            datacache.changeShowType()
          }
        }
        else{
          modalalert(json.message)
        }
      })
      .fail(function(error) {
        modalalert(error.statusText)
      })
      .always(function(){
        issubmit = false
      }) 

      return false
    })
  },
  setTop: function(code){
    $.ajax({
      url: './api/zxg/settop',
      type: 'POST',
      dataType: 'json',
      data: {
        code: code,
        topgroupid: datacache.topgroupid
      }
    })
    .done(function(json) {   
      console.info(json)
      if (json.re) {
        modalalert('置顶成功！', function(){
          datacache.top_stocks.unshift(code)
          datacache.changeGroup()          
        })
      }
      else{
        
        modalalert(json.message)
      }
    })
    .fail(function(error) {
      
    })
  },
  cancelTop: function(code){
    $.ajax({
      url: './api/zxg/canceltop',
      type: 'POST',
      dataType: 'json',
      data: {
        code: code,
        topgroupid: datacache.topgroupid
      }
    })
    .done(function(json) {   
      console.info(json)
      if (json.re) {
        modalalert('取消置顶成功！', function(){
          datacache.top_stocks = datacache.top_stocks.filter(function(v){
            return v != code
          })
          datacache.changeGroup()          
        })

      }
      else{
        
        modalalert(json.message)
      }
    })
    .fail(function(error) {
      
    })
  }
  
}

/***/ }),

/***/ "./modules/zxg/filltable.js":
/*!**********************************!*\
  !*** ./modules/zxg/filltable.js ***!
  \**********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 填充表格
 */

var text = __webpack_require__(/*! ../text */ "./modules/text/index.js")
var quote_ts = __webpack_require__(/*! ../quote_ts */ "./modules/quote_ts/index.js")
var edit_stock = __webpack_require__(/*! ./edit_stock */ "./modules/zxg/edit_stock.js")
var datacache = __webpack_require__(/*! ../datacache */ "./modules/datacache/index.js")
var info_mines = __webpack_require__(/*! ../info_mines */ "./modules/info_mines/index.js")
var itemconfig = __webpack_require__(/*! ./itemconfig */ "./modules/zxg/itemconfig.js")
var customitem = __webpack_require__(/*! ./customitem */ "./modules/zxg/customitem.js")
var jsutils = __webpack_require__(/*! ../jsutils */ "./modules/jsutils/index.js")
var stock_filter = __webpack_require__(/*! ../stock_filter */ "./modules/stock_filter/index.js")
//var fltable = require('./fltable')
var throttle = __webpack_require__(/*! lodash/throttle */ "./node_modules/lodash/throttle.js")
var drapdrop = __webpack_require__(/*! ./dragdrop */ "./modules/zxg/dragdrop.js")
var datadiff = __webpack_require__(/*! ../datadiff */ "./modules/datadiff/index.js")
var isIE9 = document.all && !window.atob; //是否是小于等于IE9
var ykyl = __webpack_require__(/*! ./ykyl */ "./modules/zxg/ykyl.js")

var dataconfig = {
  fulldata: null,
  sourcedata: null,
  /**
   * 处理全量数据
   * @param {*} dataobj 
   */
  dealFullData: function (dataobj) {
    return Object.keys(dataobj).map(function (v, i) {
      dataobj[v].index = parseInt(v)
      return dataobj[v]
    })
  },
  /**
   * 全量数据 根据推送行情和数据配置成生表格
   * @param {*} tsdata 
   */
  makeDefaultTableHtml: function (tsdata, type) {
    // console.info('全量 ')
    // console.info(this.firstFullData)
    // console.info(tsdata)

    this.fulldata = this.dealFullData(tsdata)

    if (this.firstFullData) {
      this.sourcedata = tsdata
      
      var _this = this

      //console.info(this.fulldata)

      customitem.getSetting(type).then(function (show_fields) {
        _this.fillHTMl(tsdata, show_fields)
      })      
    }
    else{
      this.reFillHTML(tsdata)
    }

  },
  /**
   * 第二次全量填充
   */
  reFillHTML: function(tsdata){
    // console.info('第二次')
    if($('#tablethdd5').length <= 0){
      return false
    }

    if (datacache.thisshowtype == 'ykyl') {
      this.countYKYL()
    }

    var diff = datadiff(this.sourcedata, tsdata)


    // console.info(diff)
    diff.forEach(function(v){
      if (!v.change) {
        return false
      }
  
      //单元变化
      var tr = $("#wltable tr[data-code='" + v.code + "']")
      
      //行变化
      if(v.fullchange){
        $('#znzgd').html('').hide() //关闭智能诊股

        var ishs = text.isHSStock(tsdata[v.index].f13, tsdata[v.index].f19)
        
        var tr4 = $("#tablethd4 tr[data-code='" + v.code + "']")
        var tr6 = $("#tablethdd6 tr[data-code='" + v.code + "']")
        tr4.data('ishsstock', ishs)
        tr.data('ishsstock', ishs)
        tr6.data('ishsstock', ishs)
        tr4.data('code', v.code)
        tr.data('code', v.code)
        tr6.data('code', v.code)

        if (ishs) {
          tr4.addClass('ishs')
          tr.addClass('ishs')
          tr6.addClass('ishs')
        }
        else{
          tr4.removeClass('ishs')
          tr.removeClass('ishs')
          tr6.removeClass('ishs')          
        }


        $('.batchselect', tr4).val(v.code)
        $('.td_f12 em', tr4).html(itemconfig.item_config.f12.html(tsdata[v.index]))
        $('.td_f14 em', tr4).html(itemconfig.item_config.f14.html(tsdata[v.index]))
        var stockoptiontd = $('.stockoptiontd', tr6)
        stockoptiontd.data('code', v.code).data('m', tsdata[v.index].f13).data('t', tsdata[v.index].f19).data('name', tsdata[v.index].f14)
      }        

      Object.keys(v.changedata).forEach(function(vi){
        var onedata = itemconfig.item_config[vi]
        var dataitem = v.changedata[vi]
        var td = $('.td_' + vi, tr)
        if (td.length <= 0) {
          return false
        }
        td.data('odata', dataitem)
        $('em', td).html(onedata.html(tsdata[v.index], v.index))
        // console.info(v.index)
        // console.info(vi)
        // console.info(dataitem)
        // console.info(onedata.html(tsdata[v.index], v.index))
      })

    })
  },
  fillHTMl: function (tsdata, show_fields) {

    var ykyld = ykyl.dealQuotePXData(tsdata)
    tsdata = ykyld.data
    datacache.now_ykyl_stock = ykyld.nowlist

    var required_fields = itemconfig.type_config.required.show_fields

    var _this = this
    //var html = []
    var table7d = $('<div class="tablethdd" id="tablethdd7"><table class="tablethd" id="tablethd7"></table></div>')
    var table7 = $('table', table7d)

    var table8d = $('<div class="tablethdd" id="tablethdd8"><table class="tablethd" id="tablethd8"></table></div>')
    var table8 = $('table', table8d)

    var table4d = $('<div class="tablethdd" id="tablethdd4"><table class="tablethd" id="tablethd4"></table><div class="ykylpatch"></div></div>')
    var table4 = $('table', table4d)

    var table5d = $('<div class="tablethdd sscroll" id="tablethdd5"><table class="wltable" id="wltable"></table><div class="ykylpatch"></div></div>')
    var table5 = $('table', table5d)

    var table6d = $('<div class="tablethdd" id="tablethdd6"><table class="tablethd" id="tablethd6"></table><div class="ykylpatch"></div></div>')
    var table6 = $('table', table6d)

    var table9d = $('<div id="tablethdd9"></div>')

    var html7 = []
    var html8 = []
    var html4 = []
    var html5 = []
    var html6 = []

    //html.push('<tr class="wlth">')

    //table7

    var alltypestr = '全部'
    if (datacache.stocktype) {
      alltypestr = stock_filter.typelist.find(function (v) {
        return v.type == datacache.stocktype
      }).name
    }

    html7.push('<tr><th class="allstock"><em><input id="clickall" type="checkbox"> ' + alltypestr + ' <span class="icon icon_darrow3"></span></em></th>')

    //表头 必选
    required_fields.forEach(function(v, i){
      var item = itemconfig.item_config[v]
      html7.push('<th')
      if (item.sort && !datacache.forbid_sort) {
        html7.push(' class="pxth" data-px="' + v + '" title="点击排序"')
      }
      html7.push('><em')
      
      if (item.align) {
        html7.push(' class="tda_' + item.align + '"')
      }
      
      html7.push('>' + (typeof item.name == 'function' ? item.name() : item.name))

      if (datacache.pxtype == v && datacache.pxorder) {
        if (datacache.pxorder == 'desc') {
          html7.push('<span class="icon icon_px2"></span')
        } else if (datacache.pxorder == 'asc') {
          html7.push('<span class="icon icon_px1"></span')
        }
      }

      html7.push('</em></th>')
    })
    html7.push('</tr>')

    //表头
    html8.push('<tr>')
    show_fields.forEach(function (v, i) {
      var item = itemconfig.item_config[v]

      html8.push('<th')
      if (item.sort && !datacache.forbid_sort) {
        html8.push(' class="pxth" data-px="' + v + '" title="点击排序"')
      }
      html8.push('><em')
      
      if (item.align) {
        html8.push(' class="tda_' + item.align + '"')
      }
      
      html8.push('>' + (typeof item.name == 'function' ? item.name() : item.name))

      if (datacache.pxtype == v && datacache.pxorder) {
        if (datacache.pxorder == 'desc') {
          html8.push('<span class="icon icon_px2"></span')
        } else if (datacache.pxorder == 'asc') {
          html8.push('<span class="icon icon_px1"></span')
        }
      }

      html8.push('</em></th>')
    })

    if (datacache.thisshowtype == 'zx') {
      html8.push('<th><em id="thitemsetting"><span class="icon icon_option"></span> 增加指标&nbsp;&nbsp;</em></th>')
    }

    html8.push('<th class="bcth"><em></em></th></tr>')

    // if (datacache.thisshowtype == 'ykyl') {
    //   var zcg = 0 //总持股
    //   var zgb = 0 //总股本
    //   var zsz = 0 //总市值
    //   var zmgyk = 0 //总每股盈亏
    //   var zxj = 0 //总现价
    //   var zfdyk = 0 //总浮动盈亏
    // }

    //html.push('<th></th>')

    //html.push('</tr>')   
    if(datacache.pxorder){
      $('#wl_mainbody').addClass('closeznzg')
    }
    else{
      $('#wl_mainbody').removeClass('closeznzg')
    }


    Object.keys(tsdata).forEach(function (v, i) {
      var item = tsdata[v]
      var line = parseInt(v.substring(4))
      var code = item.f13 + '.' + item.f12
      var istop = false

      if (datacache.is_defaultgroup) {
        if (datacache.top_stocks.indexOf(code) >= 0) {
          istop = true
        }
      }
      var trclass = ''
      if (istop) {
        trclass += 'topcode'
      }

      var tophtml = ''
      if (istop) {
        tophtml = '<span class="icon icon_settop"></span> '
      }

      var ishs = text.isHSStock(item.f13, item.f19)
      if (ishs) {
        trclass += ' ishs'
      }



      //if (i < 3) {
      html4.push('<tr id="hqtablecode_h' + i + '" data-code="' + code + '" data-ishsstock="' + (ishs ? 1 : 0) + '" class="' + trclass + '"><td class="tdselect"><em class="tda_left"><div class="znzgd"></div>' + tophtml + '<label><input type="checkbox" class="batchselect" value="' + code + '"> <i>' + (i + 1) + '</i></label></em></td>')
      //}
      //else{
      html5.push('<tr id="hqtable_h' + i + '" data-code="' + code + '" data-ishsstock="' + (text.isHSStock(item.f13, item.f19) ? 1 : 0) + '" class="' + trclass + '">')

      html6.push('<tr id="hqtableoption_h' + i + '" data-code="' + code + '" data-ishsstock="' + (text.isHSStock(item.f13, item.f19) ? 1 : 0) + '">')      
      //}

      //必选字段
      required_fields.forEach(function (v, i2) {
        var onedata = itemconfig.item_config[v]
        html4.push('<td class="td_' + v)
        //sort
        if (datacache.pxorder && datacache.pxtype && datacache.pxtype == v) {
          html4.push(' pxtd')
        }
        html4.push('" data-odata="' + item[v] + '"><em')
        if (onedata.align) {
          html4.push(' class="tda_' + onedata.align + '"')
        }
        html4.push('>' + onedata.html(item, i) + '</em></td>')        
      })

      //表行
      show_fields.forEach(function (v, i2) {
        var onedata = itemconfig.item_config[v]
        var extradata = {}

        //盈亏一览数据
        if (datacache.thisshowtype == 'ykyl') {
          var sid = item.f13.toString() + '.' + item.f12
          var thisnote = datacache.notedata.find(function(v){
            return v.sid == sid
          })
          extradata.notedata = thisnote
        }

        html5.push('<td class="td_' + v)
        //sort
        if (datacache.pxorder && datacache.pxtype && datacache.pxtype == v) {
          html5.push(' pxtd')
        }
        html5.push('" data-odata="' + item[v] + '"><em')
        if (onedata.align) {
          html5.push(' class="tda_' + onedata.align + '"')
        }
        html5.push('>' + onedata.html(item, i, false, extradata) + '</em></td>')
      })

      if (datacache.thisshowtype == 'zx') {
        html5.push('<td><em></em></td>')
      }

      html6.push('<td class="stockoptiontd" data-code="' + code + '" data-m="' + item.f13 + '"  data-t="' + item.f19 + '" data-name="' + item.f14 + '"><em><span class="icon icon_stockmore"></span></em></td>')

      html5.push('<td class="bcth"><em></em></td></tr>')
      html6.push('</tr>')
      html4.push('</tr>')
    })

    //return html.join('')
    //$('#wl_mainbody').html(html.join(''))
    table7.append(html7.join(''))
    table8.append(html8.join(''))
    table4.append(html4.join(''))
    table5.append(html5.join(''))
    table6.append(html6.join(''))



    //console.info(111)
    $('#wl_mainbody').html('')
    //console.info(222)
    $('#wl_mainbody').html('<div id="znzgd" class="sscroll"></div>').append(table7d).append(table8d).append(table4d).append(table5d).append(table6d).append(table9d)


    if (datacache.thisshowtype == 'ykyl') {
      // if (zfdyk < 10000) {
      //   zfdyk = parseFloat(zfdyk.toFixed(2))
      // }
      // $('#wl_mainbody').append('<div id="ykylcount">&nbsp; 当前页总计： 总持股 ' + zcg + ' &nbsp;&nbsp; 总股本 ' + text.formatNum(zgb) + ' &nbsp;&nbsp; 总市值 ' + text.formatNum(zsz.toFixed(2)) + ' &nbsp;&nbsp; 总每股盈亏 ' + zmgyk.toFixed(2) + ' &nbsp;&nbsp; 总盈亏率 ' + ((zsz - zgb)/zgb * 100).toFixed(0) + '% &nbsp;&nbsp; 总浮动盈亏 ' + text.formatNum(zfdyk) + '</div>')
      $('#wl_mainbody').append('<div id="ykylcount"></div>')
      _this.countYKYL()
      $('.ykylpatch').css({height:30})
    }

    this.bindFill()
    this.resizeFill()
    drapdrop.init()
    //return false
    //fltable.init()

    //tablethd
    // $('#wl_mainbody .wlth').appendTo($('#tablethd'))
    // //setTimeout(function(){
    //   $('#tablethd').width($('#wltable').width())
    //   $('#wltable tr:first td').each(function(i, v){
    //     console.info($(v).width())
    //     $('#tablethd tr:first th').eq(i).width($(v).width())
    //   })    

    // //}, 0);


    //return false
    $('#allstock').show()
    info_mines.show()
    edit_stock.bindOption()
  },
  bindFill: function(){

    $('#tablethdd5').on('scroll', throttle(function () {
      var scrollTop = $(this).scrollTop()
      var scrollLeft = $(this).scrollLeft()
      //console.info(scrollTop)

      $('#tablethdd4').scrollTop(scrollTop)
      $('#tablethdd6').scrollTop(scrollTop)
      $('#tablethdd8').scrollLeft(scrollLeft)


      if ($('#znzgd').is(':visible')) {
        var vscroll = $('#tablethdd5').get(0).offsetWidth - $('#tablethdd5').get(0).clientWidth //竖向滚动条宽度
        var top = $('#tablethd4 tr').eq($('#znzgd').data('index')).offset().top - (122 + $('#zshq').outerHeight())
        $('#znzgd').css({top: top, width: $('#wl_mainbody').get(0).clientWidth - vscroll})
      }

      if ($('#ykylcount').length) {
        var top = $('#tablethd4').height() + 36 - scrollTop
        $('#ykylcount').css({top: top})
      }      

    }, 1000 / 120))

    $('#wltable tr').hover(
      function () {
        var index = $(this).index()
        $(this).addClass("hover")
        $('#tablethd4 tr:eq(' + index + ')').addClass("hover")
        $('#tablethd6 tr:eq(' + index + ')').addClass("hover")
      },
      function () {
        var index = $(this).index()
        $(this).removeClass("hover")
        $('#tablethd4 tr:eq(' + index + ')').removeClass("hover")
        $('#tablethd6 tr:eq(' + index + ')').removeClass("hover")
      }
    )
  },
  resizeFill: function(){
    //console.info('resizetable')
    if ($('#tablethdd5').length <= 0) {
      return false
    }

    var tablethd4em = $('#tablethd4 tr:first em')
    $('#tablethd7 em').each(function(i, v){
      if (i > 0) {
        if (tablethd4em.eq(i).width() > 0) {
          $(v).width(tablethd4em.eq(i).width())
        }
        else{
          tablethd4em.eq(i).width($(v).width())
        }
      }
    })       

    var mleft = $('#tablethdd4').width()
    var mhei = $('#wl_mainbody').height()
    var mwid = $('#wl_mainbody').width()

    //console.info(mleft)

    $('#tablethdd8').css({left: mleft, width: mwid - mleft})
    //$('#tablethdd8 table').css({width: $('#wltable').width()})

    $('#tablethdd5').css({left: 0, height: mhei - 36, width: mwid, 'padding-left': mleft })
    $('#tablethdd7').css({width:mleft})
    


    dataconfig.resizeZWTable()


    var tablethd4em = $('#tablethd4 tr:first em')
    $('#tablethd7 em').each(function(i, v){
      if (i > 0 && tablethd4em.eq(i).width() > 0) {
        $(v).width(tablethd4em.eq(i).width())
      }
    })    

    var vscroll = $('#tablethdd5').get(0).offsetWidth - $('#tablethdd5').get(0).clientWidth //竖向滚动条宽度
    var hscroll = $('#tablethdd5').get(0).offsetHeight - $('#tablethdd5').get(0).clientHeight //横向滚动条宽度    

    $('#tablethdd6').css({height: $('#tablethdd5').get(0).clientHeight})  
    $('#tablethdd4').css({height: $('#tablethdd5').get(0).clientHeight})

    $('#tablethdd6').css({right: vscroll})

    if (vscroll) {
      $('#tablethdd9').css({width: 36 + vscroll})
    }

    //是否有空间展示右边的选项
    $('#tablethd8 em:last').width(0)
    $('#wltable tr:first em:last').width(0)    
    var canshowoption = $('#tablethdd5').width() - ($('#wltable').width())
    //console.info(222)
    //console.info(canshowoption)
    //console.info(canshowoption)
    // //console.info(canshowoption)

    if (canshowoption > 0) {
      $('#tablethd8 em:last').width(canshowoption)
      $('#wltable tr:first em:last').width(canshowoption - 36)
      //
      //$('#tablethd8').append('<th ><em style="width:' + (canshowoption - 16) + 'px;"><em></th>')
      //$('#wltable tr').append('<td><em style="width:' + (canshowoption - 16) + 'px;"><em></td>')
    }
    else{
      $('#tablethd8 em:last').width(36)
      $('#wltable tr:first em:last').width(36)
      // $('#tablethd8').append('<th><em style="width:' + (20 + vscroll) + 'px;"><em></th>')
      // $('#wltable tr').each(function(i, v){
      //   $(v).append('<td><em style="width:20px;"><em></td>')
      // })
    }

      if ($('#znzgd').is(':visible')) {
        var vscroll = $('#tablethdd5').get(0).offsetWidth - $('#tablethdd5').get(0).clientWidth //竖向滚动条宽度
        var top = $('#tablethd4 tr').eq($('#znzgd').data('index')).offset().top - (122 + $('#zshq').outerHeight())
        $('#znzgd').css({top: top, width: $('#wl_mainbody').get(0).clientWidth - vscroll})
      }

      if ($('#ykylcount').length) {
        var top = $('#tablethd4').height() + 36
        //console.info(top)
        $('#ykylcount').css({top: top})
      } 
  },
  resizeZWTable: function(){
    var tablethd5em = $('#wltable tr:first em')
    $('#tablethd8 em').each(function(i, v){
      if($(v).parent().is('.bcth')){
        return false
      }
      if ($(v).width() > tablethd5em.eq(i).width()) {
        tablethd5em.eq(i).width($(v).width())
      }
      else{
        $(v).width(tablethd5em.eq(i).width())
      }
    })
  },
  dealChangeMove: function (tsmv) {
    var _this = this
    //console.info(this.fulldata)
    //console.info(tsmv)
    Object.keys(tsmv).forEach(function (v, i) {
      _this.fulldata[parseInt(v)].index = parseInt(tsmv[v])
    })
    //console.info(this.fulldata)
    this.fulldata.sort(function (v1, v2) {
      return v1.index - v2.index
    })
    //console.info(this.fulldata)
  },
  /**
   * 处理主表格行变换
   * @param {*} tsmv 
   */
  dealTableChange: function (tsmv) {
    //console.info(tsmv)
    var trs = []

    $('#wltable tr').each(function (i, v) {
      $(v).data('index', i)
      trs.push($(v))
    })

    Object.keys(tsmv).forEach(function (v, i) {
      var index = parseInt(v)
      trs[index].data('index', tsmv[v])
    })

    trs.sort(function (v1, v2) {
      return v1.data('index') - v2.data('index')
    })

    trs.forEach(function (v, i) {
      v.attr('id', 'hqtable_h' + i)
      //$('.tdselect em', v).text(i + 1)
      $('#wltable').append(v)
    })
  },
  /**
   * 处理代码表格行变换
   * @param {*} tsmv 
   */
  dealCodeTableChange: function (tsmv) {
    //console.info(tsmv)
    var trs = []

    $('#tablethd4 tr').each(function (i, v) {
      $(v).data('index', i)
      trs.push($(v))
    })

    Object.keys(tsmv).forEach(function (v, i) {
      var index = parseInt(v)
      trs[index].data('index', tsmv[v])
    })

    trs.sort(function (v1, v2) {
      return v1.data('index') - v2.data('index')
    })

    trs.forEach(function (v, i) {
      v.attr('id', 'hqtablecode_h' + i)
      $('.tdselect i', v).text(i + 1)
      $('#tablethd4').append(v)
    })
  },
  
  /**
   * 扩展全量数据
   * @param {*} tsdata 
   */
  extendTSData: function (tsdata) {
    var _this = this
    Object.keys(tsdata).forEach(function (v) {
      var index = parseInt(v)
      $.extend(_this.fulldata[index], tsdata[v])
    })
  },
  /**
   * 增量数据 部分数据推送更改单元格
   * @param {*} tsdata 
   */
  diffChangeTabel: function (tsdata, tsmv) {
    // console.info(tsdata)
    //return false
    // if (type == undefined) {
    //   type = 'zx'
    // }

    if (tsmv) { //处理调换逻辑
      //console.info(tsmv)
      this.dealChangeMove(tsmv)
      this.dealTableChange(tsmv)
      this.dealCodeTableChange(tsmv)      
    }

    this.extendTSData(tsdata)

    //this.fulldata = $.extend(true, this.fulldata, tsdata)
    var _this = this

    if (datacache.thisshowtype == 'ykyl') {
      this.countYKYL()
    }


    if (datacache.pxorder != '' && ykyl.allquotepx.indexOf(datacache.pxtype) >= 0) {
      var newnowlist = ykyl.dealQuotePXData(this.fulldata).nowlist
      var ykyl_resort = JSON.stringify(datacache.now_ykyl_stock) != JSON.stringify(newnowlist)
      if (ykyl_resort) {
        this.linkTS(newnowlist, 'ykyl')
      }
      return false
    }


    Object.keys(tsdata).forEach(function (v, i) {
      var data = tsdata[v]
      var code = data.f13.toString() + '.' + data.f12.toString()
      // console.info(data)
      //var tr = $('#wltable #hqtable_h' + v)
      var tr = $("#wltable tr[data-code='" + code + "']")
      var index = tr.index()
      //console.info(index)



      Object.keys(data).forEach(function (v2) {
        if (v2 == 'f12' || v2 == 'f13') {
          return false
        }
        var td = $('.td_' + v2, tr)
        var odata = td.data('odata')
        var ndata = _this.fulldata[v][v2]
        var htmlfun = itemconfig.item_config[v2].html
        td.html('<em>' + htmlfun(_this.fulldata[v]) + '</em>').data('odata', ndata)

        var ycolor = 'transparent' //td.css('background-color')
        if (td.is('.pxtd')) {
          ycolor = '#f2f2f2'
        }

        var color = ''
        if (ndata > odata) {
          color = '#ffe7e7'
        } else if (odata > ndata) {
          color = '#caffe2'
        }

        //盈亏一览的最新价变化
        if (datacache.thisshowtype == 'ykyl' && v2 == 'f2') {
          var sid = _this.fulldata[v].f13.toString() + '.' + _this.fulldata[v].f12
          console.info(sid)
          var thisnote = datacache.notedata.find(function(v){
            return v.sid == sid
          })
          console.info(thisnote)
          $('.td_c4', tr).html('<em>' + itemconfig.item_config['c4'].html(_this.fulldata[v], index, false, {notedata: thisnote}) + '</em>')
          $('.td_c5', tr).html('<em>' + itemconfig.item_config['c5'].html(_this.fulldata[v], index, false, {notedata: thisnote}) + '</em>')
          $('.td_c6', tr).html('<em>' + itemconfig.item_config['c6'].html(_this.fulldata[v], index, false, {notedata: thisnote}) + '</em>')
          $('.td_c7', tr).html('<em>' + itemconfig.item_config['c7'].html(_this.fulldata[v], index, false, {notedata: thisnote}) + '</em>')          
        }
        if (isIE9) {
          if (color) {
            td.css({
              'background-color': color
            })
            setTimeout(function () {
              td.css({
                'background-color': ycolor //'transparent'
              })
            }, 750);            
          }
        }
        else{
          if (color) {
            td.css({
              'background-color': color
            })
            setTimeout(function () {
              td.css({
                'background-color': ycolor //'transparent'
              })
            }, 500);
          }          
        }



      })
    })
    dataconfig.resizeZWTable()
  },
  /**
   * 计算盈亏一览总数据
   */
  countYKYL: function(){
    var _this = this
    //_this.fulldata
      var zcg = 0 //总持股
      var zgb = 0 //总股本
      var zsz = 0 //总市值
      var zmgyk = 0 //总每股盈亏
      var zxj = 0 //总现价
      var zfdyk = 0 //总浮动盈亏

      Object.keys(this.fulldata).forEach(function (v, i) {
        var item = _this.fulldata[v]
        var noteitem = datacache.notedata.find(function(noteitem){
          return noteitem.sid == (item.f13 + '.' + item.f12)
        }).note
        zcg += noteitem[0]
        zgb += parseFloat(noteitem[1]*noteitem[0])+ parseFloat(noteitem[3])+parseFloat(noteitem[1]*noteitem[0])*(parseFloat(noteitem[2])+parseFloat(noteitem[4]))/1000
        zsz += noteitem[0] * (item.f2 / (Math.pow(10, item.f1)))
        if (noteitem[1] > 0 && noteitem[0] > 0) {
          zmgyk += (item.f2 / (Math.pow(10, item.f1))) - noteitem[1]
          zxj += item.f2 / (Math.pow(10, item.f1))
          zfdyk = zsz - zgb
        }

        
      })


      //console.info(zgb)
      if (zfdyk < 10000) {
        zfdyk = parseFloat(zfdyk.toFixed(2))
      }
      // console.info(zfdyk)
      // console.info(zfdyk < 0)
      var zykl = (zgb==0)?'0.00':((zsz - zgb)/zgb * 100).toFixed(2)
      $('#ykylcount').html('&nbsp; 当前页总计： 总持股 ' + zcg + ' &nbsp;&nbsp; 总成本 ' + text.formatNum(zgb.toFixed(2)) + ' &nbsp;&nbsp; 总市值 ' + text.formatNum(zsz.toFixed(2)) + ' &nbsp;&nbsp; 总每股盈亏 ' + text.textColor(zmgyk.toFixed(2),zmgyk) + ' &nbsp;&nbsp; 总盈亏率 ' + text.textColor(zykl + '%', zykl) + ' &nbsp;&nbsp; 总浮动盈亏 ' + text.textColor(text.formatNum(zfdyk.toFixed(2)), zfdyk))
      //return '<div id="ykylcount"> + '</div>'
  },

  firstFullData: true,
  linkTS: function (stocklist, type) {
    try{
      clearInterval(this.tsErrorCD)
    }
    catch(error){
    }

    var _this = this
    this.firstFullData = true
    customitem.getSetting(type).then(function (show_fields) {
      var all_fields = itemconfig.type_config.required.show_fields.concat(show_fields)
      var ts_fields = []
      

      all_fields.forEach(function (v) {
        ts_fields = ts_fields.concat(itemconfig.item_config[v].needfields)
      })
      ts_fields = jsutils.arrayFilterSame(ts_fields)

      _this.tsErrorCD = setTimeout(function(){ //推送超时倒计时
        _this.tsErrorDeal(stocklist, ts_fields, type)
      }, 4000);
      // console.info(111)
      quote_ts.bindCodes(stocklist, ts_fields, function (data) {
        try{
          clearTimeout(_this.tsErrorCD)
        }
        catch(error){
        }
        //console.info(JSON.stringify(data))
        if (data.full == 1) {
          // console.info(data.data.diff)
          _this.makeDefaultTableHtml(data.data.diff, type)
          _this.firstFullData = false
        }
        if (data.full == 0 && data.data.diff) {
          //console.info(data.data.diff)
          _this.diffChangeTabel(data.data.diff, data.data.mv)
        }
      }, function(){
        $('#wl_mainbody').html('')
      })
    }, function(){
      $('#wl_mainbody').html('')
    })

  },
  tsErrorCD: null, //推送错误倒计时
  /**
   * 推送超时处理
   */
  tsErrorDeal: function(stocklist, ts_fields, type){
    var _this = this
    quote_ts.close()

    try{
      clearInterval(this.tsErrorCD)
    }
    catch(error){
    }
    // customitem.getSetting(type).then(function (show_fields) {


    // }, function(){
    //   $('#wl_mainbody').html('')
    // })
      quote_ts.bindCodesGet(stocklist, ts_fields, function(data){
        if (data.rc == 0 && data.data) {
          _this.makeDefaultTableHtml(data.data.diff, type)
          _this.firstFullData = false        
        }
      }) 
    

    this.tsErrorCD = setInterval(function(){
      quote_ts.bindCodesGet(stocklist, ts_fields, function(data){
        if (data.rc == 0 && data.data) {
          _this.makeDefaultTableHtml(data.data.diff, type)
          _this.firstFullData = false        
        }
      })      
    }, 60 * 1000)


  }
}

datacache.resizeFill = dataconfig.resizeFill
window.resizeFill = dataconfig.resizeFill

module.exports = dataconfig

/***/ }),

/***/ "./modules/zxg/groups.js":
/*!*******************************!*\
  !*** ./modules/zxg/groups.js ***!
  \*******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 分组
 */

var datacache = __webpack_require__(/*! ../datacache */ "./modules/datacache/index.js")
var clone = __webpack_require__(/*! lodash/clone */ "./node_modules/lodash/clone.js")
var util = __webpack_require__(/*! ../utils */ "./modules/utils/index.js")
//var edit_group = require('./edit_group')
//var popmenu = require('../popmenu')
var modal = __webpack_require__(/*! ../modal */ "./modules/modal/index.js")
var modalalert = __webpack_require__(/*! ../modal/alert */ "./modules/modal/alert.js")
var modalconfirm = __webpack_require__(/*! ../modal/confirm */ "./modules/modal/confirm.js")
var dom = __webpack_require__(/*! ../dom */ "./modules/dom/index.js")
var data = __webpack_require__(/*! ./data */ "./modules/zxg/data.js")


var bind_debounce = null

var groups = {
  bind: function(){
    var _this = this
    $('#moregroupul').on('click', 'li', function(){
      var groupid = $(this).data('groupid')
      datacache.changeGroup(groupid)
      //console.info(groupid)
    })
    $('#zxggrouplist').on('click', '.groupeditli li', function(){
      var groupname = $(this).data('groupname')
      var groupid = $(this).data('groupid')
      var thispli = $(this).parents('li')
      if ($(this).is('.modygroupli')) {
        _this.editGroupName(groupid, groupname, thispli)
      }
      else if($(this).is('.deletegroupli')){
        _this.deleteGroup(groupid, groupname, thispli)
      }
    })
  },
  reloadGroupHtml: function(){
    
  },
  /**
   * 生成组合html
   */
  makeGroupHtml: function(groupid, onhide_index){
    if (!datacache.groupdata) {
      return false
    }
    if (groupid) {
      datacache.thisgroupid = groupid
    }

    // if (groupid == undefined && datacache.thisgroupid == null) {
      
    // }

    //console.info(datacache.thisgroupid)

    var glist = clone(datacache.groupdata.groups)
    //console.info(glist)

    if (onhide_index) {
      glist = util.arrayJump(glist, onhide_index, 1)
      //console.info(glist)
      //return false
    }

    var html = []
    glist.forEach(function (v, i) {
      if (v.id == datacache.groupdata.horder) {
        return
      }
      html.push('<li data-groupid="' + v.id + '" data-groupname="' + v.name + '" class="populd lia noshow')
      if (datacache.thisgroupid == null && i == 0) {
        html.push(' on')
      }
      else if (v.id == datacache.thisgroupid) {
        html.push(' on')
      }
      // else{
      //   html.push(' noshow')
      // }
      html.push('"><a href="javascript:;" target="_self">' + v.name + '</a>')
      html.push('<ul class="popul groupeditli w100"><div class="tooltip__arrow"></div><div class="poplis"><li data-groupid="' + v.id + '" data-groupname="' + v.name + '" class="modygroupli lia"><a href="javascript:;" target="_self">修改名称</a></li><li data-groupid="' + v.id + '" data-groupname="' + v.name + '" class="lia deletegroupli"><a href="javascript:;" target="_self">删除组合</a></li></div></ul>')
      html.push('</li>')
    })

    html = $(html.join(''))
    $('#zxggrouplist').html(html)



    this.resizeGroup()
    // console.info(resize)
    // if (resize == 'resize_again') {
    //   console.info(111)
    // }
    // bind_debounce = debounce(function(){
    //   console.info(222)
    //   $('#zxggrouplist li.on').removeClass('noshow')
    // }, 100)
    try{
      clearTimeout(bind_debounce)
    }
    catch(error){
    }
    bind_debounce = setTimeout(function(){
      var onli = $('#zxggrouplist li.on')
      var index = onli.index()
      if (index == 0) {
        return false
      }
      onli.one('mouseover', function(){
        $(this).removeClass('noshow')
      })
      //onli.removeClass('noshow')
    }, 200);
  },
  /**
   * 重新组织组合样式
   */
  resizeGroup: function(){
    var w = $('.wl_t').width() - 335
    var ulliw = []
    var sumw = 0
    var moreshow = false
    var morewidth = $('.moregroup').outerWidth()
    var moniwidth = 130 //$('.monigroup').outerWidth()
    var onhide_index = null
    //console.info(morewidth)
    $('.moregroup').hide()
    $('.moregroup .poplis').html('')

    $('#zxggrouplist>li[data-groupid]').each(function(i, v){
      var liw = $(v).outerWidth()
      sumw += liw
      var show = true
      if (sumw + morewidth + moniwidth > w) {
        show = false
      }
      ulliw.push({
        ele: $(this),
        index: i,
        width: liw,
        show: show
      })

      if (!show) {
        if ($(this).is('.on') && !show) {
          onhide_index = i
        }
        //$('.moregroup .poplis').append($(this))
        moreshow = true
      }
    })

    if (!moreshow) {
      return 'no_resize'
    }

    ulliw.forEach(function(v, i){
      if (!v.show) {
        $('.popul', v.ele).remove()
        $('.moregroup .poplis').append(v.ele)
      }
    })

    if (moreshow) {
      $('.moregroup').css({display:'inline-block'})
    }

    if (onhide_index) {
      this.makeGroupHtml(datacache.thisgroupid, onhide_index)
      return 'resize_again'
    }

    return 'resize_done'

    //console.info(w)
    //console.info(ulliw)
    
  },
  editGroupName: function(groupid, groupname, thisli){
    var _this = this
    var html = $('<div><form target="_self"><input type="text" value="' + groupname + '" class="modalinput" id="newgroupname"><div class="modalbtnd"><button type="submit" class="modalbtn_default">确 定</button> &nbsp; <a href="javascript:;" target="_self" class="modalbtn_cancel">取 消</a></div></form></div>')
    var newmodal = new modal({
      content: html,
      title: '请输入组合名<small>（最多6个汉字或12个字符）</small>'
    })

    newmodal.show(function(){
      dom.cursorMoveEnd($('#newgroupname', html).get(0))
    })

    $('.modalbtn_cancel', html).click(function(){
      newmodal.close()
    })

    var issubmit = false
    $('form', html).submit(function(){
      if (issubmit) {
        return false
      }
      var newgroupname = $.trim($('#newgroupname', html).val())
      issubmit = true
      $.ajax({
        url: './api/zxg/editgroupname',
        type: 'POST',
        dataType: 'json',
        data: {
          groupid: groupid,
          groupname: newgroupname
        }
      })
      .done(function(json) {   
        if (json.re) {
          modalalert('修改成功')
          _this.reloadGroupInfo()
          thisli.text(newgroupname)
        }
        else{
          modalalert(json.message)
        }
      })
      .fail(function(error) {
        modalalert(error.statusText)
      })
      .always(function(){
        issubmit = false
        newmodal.close()
      })

      return false
    })
  },
  deleteGroup: function(groupid, groupname, thisli){
    var _this = this
    var issubmit = false
    modalconfirm('确定要删除 [' + groupname + '] 分组吗？', function(){
      if (issubmit) {
        return false
      }
      issubmit = true
      $.ajax({
        url: './api/zxg/deletegroup',
        type: 'POST',
        dataType: 'json',
        data: {
          groupid: groupid
        }
      })
      .done(function(json) {   
        if (json.re) {
          //modalalert('删除成功')
          _this.reloadGroupInfo()
          datacache.thisgroupid = datacache.firstgroupid
          datacache.changeGroup()
          //$('#zxggrouplist li:first').click()
          //thisli.remove()
        }
        else{
          modalalert(json.message)
        }
      })
      .fail(function(error) {
        modalalert(error.statusText)
      })
      .always(function(){
        issubmit = false
      }) 
    })
  },
  /**
   * 新增组合
   */
  addGroup: function(){
    var _this = this
    var html = $('<div><form target="_self"><input type="text" class="modalinput" id="newgroupname"><div class="modalbtnd"><button type="submit" class="modalbtn_default">确 定</button> &nbsp; <a href="javascript:;" target="_self" class="modalbtn_cancel">取 消</a></div></form></div>')
    var newmodal = new modal({
      content: html,
      title: '请输入组合名<small>（最多6个汉字或12个字符）</small>'
    })

    newmodal.show(function(){
      $('#newgroupname', html).focus()
    })

    $('.modalbtn_cancel', html).click(function(){
      newmodal.close()
    })

    var issubmit = false
    $('form', html).submit(function(){
      if (issubmit) {
        return false
      }
      var newgroupname = $.trim($('#newgroupname', html).val())

      if (newgroupname == '') {
        modalalert('组合名称不能为空！')
        return false
      }

      issubmit = true
      $.ajax({
        url: './api/zxg/addgroup',
        type: 'POST',
        dataType: 'json',
        data: {
          groupname: newgroupname
        }
      })
      .done(function(json) {   
        if (json.re) {
          modalalert('新建组合成功')
          _this.reloadGroupInfo()
          //$('#zxggrouplist .newgroupli').before('<li data-groupid="' + json.result.gid + '" data-groupname="' + newgroupname + '">' + newgroupname + '</li>')
        }
        else{
          modalalert(json.message)
        }
      })
      .fail(function(error) {
        modalalert(error.statusText)
      })
      .always(function(){
        issubmit = false
        newmodal.close()
      })

      return false
    })
  },
  /**
   * 重载组合信息
   */
  reloadGroupInfo: function(){
    var _this = this
    return $.ajax({
      cache: false,
      url: './api/zxg/group',
      type: 'GET',
      dataType: 'json',
      data: {
        
      }
    }).then(function(json){
      datacache.groupdata = json.result
      _this.makeGroupHtml()
    })
  },
  moveGroup: function(code, fromgroupid, togroupid){
    return data.moveGroup(code, fromgroupid, togroupid)
    .then(function(json) {
      if(json.re){
        if (datacache.is_defaultgroup) { //处理置顶股票
          _.pull(datacache.top_stocks, code)
        }
        modalalert('移动成功！')
        //datacache.changeGroup()
        datacache.changeGroup(togroupid)
      }
      else{
        modalalert(json.message)
      }
    })
  }
}

module.exports = groups

/***/ }),

/***/ "./modules/zxg/index.js":
/*!******************************!*\
  !*** ./modules/zxg/index.js ***!
  \******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 自选股
 */


var filltable = __webpack_require__(/*! ./filltable */ "./modules/zxg/filltable.js")
var dgtl = __webpack_require__(/*! ./dgtl */ "./modules/zxg/dgtl.js")
var quote_ts = __webpack_require__(/*! ../quote_ts */ "./modules/quote_ts/index.js")
var edit_group = __webpack_require__(/*! ./edit_group */ "./modules/zxg/edit_group.js")
var datacache = __webpack_require__(/*! ../datacache */ "./modules/datacache/index.js")
var modalalert = __webpack_require__(/*! ../modal/alert */ "./modules/modal/alert.js")
var note = __webpack_require__(/*! ./note */ "./modules/zxg/note.js")
var global_event = __webpack_require__(/*! ../global_event */ "./modules/global_event/index.js")
var stock_filter = __webpack_require__(/*! ../stock_filter */ "./modules/stock_filter/index.js")
var quote = __webpack_require__(/*! ../quote */ "./modules/quote/index.js")
var ylyc = __webpack_require__(/*! ../ylyc/web */ "./modules/ylyc/web.js")
var datacache = __webpack_require__(/*! ../datacache */ "./modules/datacache/index.js")
var customitem = __webpack_require__(/*! ./customitem */ "./modules/zxg/customitem.js")
var sessionstorage = __webpack_require__(/*! ../sessionstorage */ "./modules/sessionstorage/index.js")
var localstorage = __webpack_require__(/*! ../localstorage */ "./modules/localstorage/index.js")
var hegui = __webpack_require__(/*! ../hegui */ "./modules/hegui/index.js")
var ykyl = __webpack_require__(/*! ./ykyl */ "./modules/zxg/ykyl.js")

var groups = __webpack_require__(/*! ./groups */ "./modules/zxg/groups.js")
groups.bind()

/**
 * 获取自选股回调
 */

var this_groupid = ''
var this_datatype = 'zx' //当前的显示类型
var this_stocklist = ''

/**
 * 获取组合
 */
function getGroup(){
  $.ajax({
    url: './api/zxg/group',
    type: 'GET',
    dataType: 'json',
    cache: false,
    data: {
      
    }
  })
  .done(function(json) {   
    if (json.re) {
      datacache.groupdata = json.result
      //console.info(datacache.groupdata)
      datacache.topgroupid = json.result.horder
      datacache.firstgroupid = json.result.groups[0].id
      datacache.top_stocks = json.result.topstocks
      // console.info(datacache.top_stocks)

      if (sessionstorage.get('groupid') && datacache.groupdata.groups.some(function(v){
        return v.id == sessionstorage.get('groupid')
      })) {
        changeGroup(sessionstorage.get('groupid'))
        if (sessionstorage.get('groupid') == json.result.groups[0].id) {
          datacache.is_defaultgroup = true
        }
      }
      else{
        getDefault(json.result.groups[0].id)
        datacache.is_defaultgroup = true       
      }


      //groups.makeGroupHtml()

      // var html = []
      // json.result.groups.forEach(function(v, i){
      //   if (v.id == json.result.horder) {
      //     return
      //   }
      //   html.push('<li data-groupid="' + v.id + '" data-groupname="' + v.name + '" class="lia')
      //   if (i == 0) {
      //     html.push(' on')
      //   }
      //   html.push('"><a href="javascript:;" target="_self">' + v.name + '</a></li>')
      // })

     // html.push('<li class="monigroup lia"><a href="http://group.eastmoney.com/MyCombin.html">模拟组合</a></li>')
      //html.push('<li class="newgroupli"><span class="newgroupbtn"><em>+</em> 新建组合</span></li>')
     // html.push('<li class="moregroup">更多组合 <span class="icon icon_darrow3"></span></li>')

      // html = $(html.join(''))
      // $('#zxggrouplist').html(html)
      

      //edit_group.bind() //绑定组合操作
    }
  })
  .fail(function(error) {
    
  })
}

datacache.getGroup = getGroup


// var default_zxg = null

/**
 * 获取默认组合自选股
 */
function getDefault(groupid){
  changeGroup(groupid)
  // $.ajax({
  //   url: './api/zxg/default',
  //   type: 'GET',
  //   dataType: 'json',
  //   data: {
      
  //   }
  // })
  // .done(function(json) {   
  //   if (json.re) {
  //     default_zxg = json.result
  //     bindTS(default_zxg)
  //     onGetStocks(default_zxg)
  //   }
  // })
  // .fail(function(error) {
    
  // })
}

function changeGroup(groupid){
  datacache.pxorder = ''
  if (groupid  == undefined) {
    groupid = datacache.thisgroupid
  }
  else{
    //var grounpindex = $('#zxggrouplist [data-groupid=' + groupid + ']').index()
    //$('#zxggrouplist li').removeClass('on')
    //$('#zxggrouplist li').eq(grounpindex).addClass('on')
    groups.makeGroupHtml(groupid)
  }

  this_groupid = groupid
  datacache.is_defaultgroup = datacache.firstgroupid == groupid
  sessionstorage.save('groupid', groupid)

  return $.ajax({
    url: './api/zxg/getstockbygroupid/' + groupid,
    type: 'GET',
    dataType: 'json',
    cache: false,
    data: {
      rnd: Math.floor(Math.random()*10000000+1)
    }
  })
  .then(function(json) { 
    //alert(json.result.length)
    if (json.re) {
      //('#allstock').hide()
      this_stocklist = json.result
      // console.info(this_stocklist)
      // console.info(datacache.top_stocks)
      this_stocklist = margeTopStock(this_stocklist, datacache.top_stocks)
      
      // console.info(this_stocklist)
      if (datacache.stocktype) {
        return quote.getStockTypeInfo(this_stocklist.join(','))
      }
    }
  }).then(function(quote_type){
    if (datacache.stocktype) {
      this_stocklist = stock_filter.filterCode(this_stocklist, quote_type, datacache.stocktype)
      
    }

    bindTS(this_stocklist)
    global_event.trigger('stockchange', this_stocklist)
    datacache.stocks = this_stocklist
    //datacache.stocktype = null
  })
}

datacache.changeGroup = changeGroup


/**
 * 合并自选股和置顶股票
 * @param {*} stocklist 
 * @param {*} topstocklist 
 */
function margeTopStock(stocklist, topstocklist){
  // console.info(stocklist)
  // console.info(topstocklist)
  // stocklist = ['1.600000','0.300059','0.300051','1.600017']
  // topstocklist = ['1.600017','0.300059']
  if (!datacache.is_defaultgroup || topstocklist.length == 0) {
    return stocklist
  }

  var toptemplist = []

  stocklist.forEach(function(v){
    if (topstocklist.indexOf(v) >= 0) {
      toptemplist.push(v)
    }
  })

  // console.info(111)
  // console.info(toptemplist)

  var list = toptemplist.concat(stocklist)
  var listobj = []
  list.forEach(function(v){
    listobj[v] = null
  })

  // console.info(Object.keys(listobj))
  return Object.keys(listobj)
}

/**
 * 绑定行情推送
 * @param {*} stocklist 
 */
function bindTS(){
  // if (this_stocklist.length == 0) {
  //   $('#allstock').hide()
  //   $('#wl_mainbody').html('<div class="nostockd">您暂无自选股</div>');
  //   return false
  // }
  changeShowType()
}

// /**
//  * 首次全量推送填充表格
//  * @param {*} hqdata 
//  */
// function stockListHtml(hqdata){
  
// }

// /**
//  * 推送数据改变表格
//  * @param {*} hqts 
//  */
// function tsHtml(hqts){
//   filltable.diffChangeTabel(hqts)
// }

function bind(){
  //切换自选股组合
  $('#zxggrouplist').on('click', 'a', function(){
    var thisli = $(this)
    var groupid = $(this).parent('li').data('groupid')
    if (!groupid) {
      // if (thisli.is('.newgroupli')) {
      //   edit_group.addGroup()
      // }
      return true
    }
    datacache.stocktype = null
    changeGroup(groupid).then(function(){
      // $('#zxggrouplist li').removeClass('on')
      // thisli.addClass('on')
    })
  })

  $('.newgroupbtn').click(function(){
    groups.addGroup()
    return false
  })

  //添加自选股
  addStock()

  //切换数据类型
  $('#wltypelist').on('click', 'li', function(){
    var type = $(this).data('type')
    var index = $(this).index()
    changeShowType(type, index)
    datacache.pxorder = ''
  })

  //切换字体大小
  $('#stocklistfzbtn').click(function(){
    localstorage.set('fontsize', 'big')
    $('#wl_mainbody').addClass('wl_table_big')

    $('#stocklistfzbtn').hide()
    $('#stocklistfzbtn2').css({
      display: 'inline-block'
    })
    setTimeout(function(){
      datacache.resizeFill()
    }, 1000);
    
  })
  $('#stocklistfzbtn2').click(function(){
    localstorage.set('fontsize', 'small')
    $('#wl_mainbody').removeClass('wl_table_big')
    $('#stocklistfzbtn2').hide()
    $('#stocklistfzbtn').css({
      display: 'inline-block'
    })
    setTimeout(function(){
      datacache.resizeFill()
    }, 1000);
  })


  if (localstorage.get('fontsize') == 'big') {
    $('#wl_mainbody').addClass('wl_table_big')
    $('#stocklistfzbtn').hide()
    $('#stocklistfzbtn2').css({
      display: 'inline-block'
    })
    // setTimeout(function(){
    //   datacache.resizeFill()
    // }, 1000);    
  }


  //排序
  $('#wl_mainbody').on('click', ' .pxth', function(){
    var pxtype = $(this).data('px')
    var pxorder = datacache.pxorder //$(this).data('pxorder')
    if (pxorder == undefined || pxorder == '') {
      pxorder = 'desc'
    }
    else if(pxorder == 'desc'){
      pxorder = 'asc'
    }
    else if(pxorder = 'asc'){
      pxorder = ''
    }
    if (pxtype && datacache.pxtype && pxtype != datacache.pxtype) {
      pxorder = 'desc'
    }

    switch (pxorder) {
      case 'desc':
        $('#pxtext').text('降序排序中（非默认状态下不可拖动，不可展开智能诊股）')
        break;
      case 'asc':
        $('#pxtext').text('升序排序中（非默认状态下不可拖动，不可展开智能诊股）')
        break;
      default:
        $('#pxtext').text('默认排序中，点击表头可更改排序状态（拖动每行可以自定义排序）')
        break;
    }

    datacache.pxtype = pxtype
    datacache.pxorder = pxorder
    datacache.changeShowType()
  })

  //增加指标
  $('body').on('click', '#thitemsetting', function(){
    customitem.showSetting()
  })

  //切换刷新频率
  $('#refreshtime').on('click', 'a', function(){
    $('#refreshtime a').removeClass('on')
    $(this).addClass('on')
    var index = $(this).index()
    console.info(index)
    switch (index) {
      case 0:
        datacache.refreshtime = 2000
        break;
      case 1:
        datacache.refreshtime = 5000
        break;
      case 2:
        datacache.refreshtime = 10000
        break;   
      default:
        datacache.refreshtime = 2000
        break;
    }

    datacache.changeShowType()

    return false
  })
  
}

/**
 * 切换显示类型
 * @param {*} type 
 */
function changeShowType(type, liindex){
  if (type == undefined && sessionstorage.get('showtype')) {
    type = sessionstorage.get('showtype')
  }

  $('#pxtext').show()
  $('#pxtext_dgtl').hide()
  // console.info(type)
  // console.info(liindex)
  //datacache.pxorder = ''
  if (type) {
    this_datatype = type
  }
  if (type == undefined) {
    this_datatype = datacache.thisshowtype ? datacache.thisshowtype : 'zx'
  }
  // if (type == undefined && datacache.thisshowtype != null) {
  //   type = datacache.thisshowtype
  // }
  // else{
  //   this_datatype = datacache.thisshowtype
  // }

  //console.info(this_datatype)
  if (liindex != undefined) {
    $('#wltypelist li').removeClass('on')
    $('#wltypelist li').eq(liindex).addClass('on')    
  }
  else{
    $('#wltypelist li').removeClass('on')
    var liindex = 0
    switch (type) {
      case 'zx':
        liindex = 0
        break;
      case 'zjl':
        liindex = 1
        break;
      case 'ddejc':
        liindex = 2
        break;
      case 'ylyc':
        liindex = 3
        break;
      case 'cwsj':
        liindex = 4
        break;
      case 'dgtl':
        liindex = 5
        break;
      case 'ykyl':
        liindex = 6
        break;
        
      default:
        liindex = 0
        break;
    }
    $('#wltypelist li').eq(liindex).addClass('on')
  }
  datacache.thisshowtype = this_datatype
  sessionstorage.save('showtype', this_datatype)
  datacache.forbid_sort = false

  if (this_stocklist.length == 0) {

    //$('#allstock').hide()
    $('#wl_mainbody').html('<table class="tablethd" id="tablethd7"><th class="allstock"><em>' + stock_filter.getTypeName(datacache.stocktype).name + ' <span class="icon icon_darrow3"></span></em></th><th data-px="f12"><em class="tda_left" style="width: 84px;">代码</em></th><th><em class="tda_left" style="width: 136px;">名称</em></th></table><div class="nostockd">您暂无自选股</div>');
    return false
  }

  if (this_datatype == 'dgtl') {
    dgtl.filterCodeList(this_stocklist).then(function(filter_stocklist){
      datacache.forbid_sort = true
      quote_ts.close()
      dgtl.show(filter_stocklist)
      $('#allstock').hide()
      $('#pxtext').hide()
      if (hegui.isHKDelay() == 1) {
        $('#pxtext_dgtl').text('应港交所要求，中国大陆以外地区用户港股行情图需做延时处理，给您带来的不便敬请谅解。').show()
      }
      else if (hegui.isHKDelay() == 2) {
        $('#pxtext_dgtl').html('未登录用户仅可查看港股延时行情图，给您带来的不便敬请谅解。<a href="https://passport2.eastmoney.com/pub/login?backurl=' + encodeURIComponent(self.location.href) + '" target="_self">登录</a>').show()
      }      
    })
    
    return false
  }

  if (this_datatype == 'ykyl') { //盈亏一览
    // datacache.forbid_sort = true
    note.getNoteData(this_groupid, this_stocklist)
    .then(function(notedata){
      datacache.notedata = note.dealNoteData(notedata)
      console.info(datacache.notedata)
      //处理盈亏一览排序 非行情部分
      var sort_this_stocklist = ykyl.dealPXStocks(this_stocklist)
      filltable.linkTS(sort_this_stocklist, this_datatype)
    })
    
    return false
  }

  if (this_datatype == 'ylyc') {
    datacache.forbid_sort = true
    ylyc.getData(this_stocklist.join(','))
    .then(function(notedata){
      datacache.ylycdata = notedata
      filltable.linkTS(this_stocklist, this_datatype)
    })
    return false
  }
  
  filltable.linkTS(this_stocklist, this_datatype)
}

datacache.changeShowType = changeShowType

/**
 * 添加自选股
 */
function addStock(){
  if (window.suggest2017) {
    var addstocksuggest = new suggest2017({
      zindex: 50,
      inputid: 'addfavstockinput',
      showblank: false,
      modules: ['stock'],
      showstocklink: false,
      stockcount: 10,
      width: 300,
      offset: {
        left: -40,
        top: 8
      },
      onSubmit: function(stockinfo){
        formAddFavStock(stockinfo)
        return false
      },
      onConfirmStock: function(stockinfo){
        formAddFavStock(stockinfo)
        return false

      }
    })  
  }

}

function formAddFavStock(stockinfo){
  if (stockinfo.stock) {
    stockinfo = stockinfo.stock
  }
  else{
    return false
  }
  stockinfo.Code = stockinfo.Code.replace('.', '_')

  $.ajax({
    url: './api/zxg/addstock',
    type: 'POST',
    dataType: 'json',
    data: {
      groupid: this_groupid,
      stockcode:  stockinfo.MktNum +  '.' + stockinfo.Code
    }
  })
  .done(function(json) {   
    if (json.re) {
      changeGroup(this_groupid)
    }
    else{
      if (json.message == '股票代码不符合规范') {
        json.message = '暂不支持添加该品种'
      }
      modalalert(json.message)
    }
    //console.info(json)
  })
  .fail(function(error) {
    
  })
}

// module.exports = function(callback){

//   onGetStocks = callback
// }

module.exports = {
  init: function(){
    bind()
    hegui.isOutside().then(function(isoutsider){
      getGroup()
      if (isoutsider) {
        hegui.outsiderAlert()
      }
    })
    
    //onGetStocks = callback
  },
  // onGetStocks: function(callback){
  //   onGetStocks = callback
  // },
  changeGroup: function(groupid){
    changeGroup(groupid)
  },
  changeShowType: changeShowType
}

/***/ }),

/***/ "./modules/zxg/itemconfig.js":
/*!***********************************!*\
  !*** ./modules/zxg/itemconfig.js ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 配置数据
 */
var text = __webpack_require__(/*! ../text */ "./modules/text/index.js")
var datacache = __webpack_require__(/*! ../datacache */ "./modules/datacache/index.js")
var hegui = __webpack_require__(/*! ../hegui */ "./modules/hegui/index.js")

var nonedata = '<span class="ndatas">—</span>'

module.exports = {
  item_config: {
    f12: {
      name: '代码',
      needfields: ['f12', 'f13', 'f19'],
      sort: true,
      align: 'left',
      html: function(item, index, isshort){
        var back = '<a href="' + text.getLinkByCode(item.f13 + '.' + item.f12) + '">' + item.f12

        //if (isshort == true) {
          if (item.f13 == 105 || item.f13 == 106 || item.f13 == 107) {//美股
            back += ' <span class="usstock">US</span> '
          }
          else if (item.f13 == 116) {//港股
            back += ' <span class="hkstock">HK</span> '
          }
          else if (item.f13 == 155 || item.f13 == 156) {//英股
            back += ' <span class="ukstock">UK</span> '
          } 
        //}

        back += '</a>'
        return back
        
      }
    },
    f14: {
      name: '名称',
      needfields: ['f14', 'f13', 'f12'],
      align: 'left',
      html: function(item, index, isshort){
        var back = ''
        // if (isshort == true) {
            
        // }
        // else{
        //   if (item.f13 == 105 || item.f13 == 106 || item.f13 == 107) {//美股
        //     back += '<span class="usstock">US</span> '
        //   }
        //   if (item.f13 == 116 && hegui.isHKDelay() == 0) {//港股
        //     back += '<span class="hkstock">HK</span> '
        //   }
        //   if (item.f13 == 116 && hegui.isHKDelay() == 1) {//港股
        //     back += '<span class="hkdelay" title="中国大陆以外地区用户仅可查看港股延时行情，给您带来的不便敬请谅解"></span> '
        //   }
        //   if (item.f13 == 116 && hegui.isHKDelay() == 2) {//港股
        //     back += '<span class="hkdelay" title="未登录用户仅可查看港股延时行情，您可通过登录的方式获取港股实时行情报价，给您带来的不便敬请谅解"></span> '
        //   }          
        //   if (item.f13 == 155 || item.f13 == 156) {//英股
        //     back += '<span class="ukstock">UK</span> '
        //     //back += text.txtLeft(item.f14,10,false)
        //   }          
        // }

        if (isshort == true) {
          back += '<a href="' + text.getLinkByCode(item.f13 + '.' + item.f12) + '" title="' + item.f14 + '">' + text.txtLeftPure(item.f14,6,true) + '</a>'
        }
        else{
          back += '<a href="' + text.getLinkByCode(item.f13 + '.' + item.f12) + '" title="' + item.f14 + '">' + text.txtLeft(item.f14,10,false) + '</a>'
        }


        // if (isshort == true) {
            if (item.f13 == 116 && hegui.isHKDelay() == 1) {//港股
              back += '<span class="hkdelay_lite" title="中国大陆以外地区用户仅可查看港股延时行情，给您带来的不便敬请谅解"></span> '
            }
            if (item.f13 == 116 && hegui.isHKDelay() == 2) {//港股
              back += '<span class="hkdelay_lite" title="未登录用户仅可查看港股延时行情，您可通过登录的方式获取港股实时行情报价，给您带来的不便敬请谅解"></span> '
            }             
        // }
            
        
        return back
      }
    },
    z1: {
      name: '股吧',
      needfields: ['f12', 'f13', 'f19', 'f139', 'f148'],
      sort: false,
      align: 'center',
      html: function(item){ 
        var m = item.f13
        var t = item.f19
        var k = item.f139
        // console.info(m)
        // console.info(t)

        var hasguba = false

         if ((m==0||m==1) && (item.f148&2)){//表示已退市

         }  
         else{
          //科创板
          if( m==1 && t==23 ) hasguba = true
          //沪深AB股
          if((m==0&&t==6) || (m==0&&t==13) || (m==0&&t==80) || (m==1&&t==2) || (m==0&&t==7) || (m==1&&t==3)) hasguba = true
          //港股：主板、创业板、基金
          if( (m==116&&t==1) || (m==116&&t==3) || (m==116&&t==4)) hasguba = true
          //美股：股票 优先股 存托凭证 基金
          if((m==105||m==106||m==107) && (t==1||t==2||t==3||t==4)) hasguba = true
          //英股：全市场
          if(m==155||m==156) hasguba = true


          //国内期货：上期所、大商所、郑商所、上期能源 
          if((m==113||m==114||m==115||m==142)) hasguba = true
          // //沪深基金
          //  if((m==1&&t==9) || (m==0&&t==10)) hasguba = true

            //沪深指数+全球指数
            if ((m==1&&t==1) || (m==0&&t==5) || (m==100))  hasguba = true
          //板块
          if(m == 90) hasguba = true

          //可转债
          if(k == 11) hasguba = true  

          if ( m==0 && t==81 ) hasguba = true  //新三板

    
         }


        if(hasguba){
          return '<a href="http://guba.eastmoney.com/interface/GetList.aspx?code=' + item.f13 + '.' + item.f12 + '">股吧</a>'
        }
        else{
          return ''
        }
      }
    },    
    f2: {
      name: '最新价',
      sort: true,
      needfields: ['f2', 'f4', 'f1', 'f125', 'f18', 'f1'],
      html: function(item){
        if(item.f125  == 2 && item.f18 != null){
          return (item.f18 / (Math.pow(10, item.f1))).toFixed(item.f1)
        }        
        if (item.f2 == null) {
          return nonedata
        }
        // console.info((item.f2 / (Math.pow(10, item.f1))).toFixed(item.f1))
        return text.textColor((item.f2 / (Math.pow(10, item.f1))).toFixed(item.f1), item.f4)
      }
    },
    f3: {
      name: '涨跌幅',
      needfields: ['f3', 'f4', 'f125', 'f152'],
      sort: true,
      html: function(item){
        if(item.f125  == 2){
          return '停牌'
        }
        if (item.f3 == null) {
          return nonedata
        }
        return text.textColor(((item.f3 / Math.pow(10, item.f152)).toFixed(item.f152) + '%'), item.f4)
      }
    },   
    f4: {
      name: '涨跌额',
      needfields: ['f1', 'f4'],
      sort: true,
      html: function(item){
        if (item.f4 == null) {
          return nonedata
        }
        return text.textColor((item.f4 / (Math.pow(10, item.f1))).toFixed(item.f1), item.f4)
      }
    },  
    f5: {
      name: '总手',
      sort: true,
      needfields: ['f5'],
      html: function(item){
        if (item.f5 == null) {
          return nonedata
        }
        return text.formatNum(item.f5)
      }
    },      
    f30: {
      name: '现手',
      sort: true,
      needfields: ['f30'],
      html: function(item){
        if (item.f30 == null) {
          return nonedata
        }
        return text.textColor(text.formatNum(Math.abs(item.f30)), item.f30)
      }
    },        
    f31: {
      name: '买入价',
      sort: true,
      needfields: ['f1', 'f31', 'f18'],
      html: function(item){
        if (item.f31 == null) {
          return nonedata
        }
        return text.textColor((item.f31 / (Math.pow(10, item.f1))).toFixed(item.f1), item.f31 - item.f18)
      }
    },      
    f32: {
      name: '卖出价',
      sort: true,
      needfields: ['f1', 'f32', 'f18'],
      html: function(item){
        if (item.f32 == null) {
          return nonedata
        }
        return text.textColor((item.f32 / (Math.pow(10, item.f1))).toFixed(item.f1), item.f32 - item.f18)
      }
    },   
    f18: {
      name: '昨收',
      sort: true,
      needfields: ['f1', 'f18'],
      html: function(item){
        if (item.f18 == null) {
          return nonedata
        }
        return (item.f18 / (Math.pow(10, item.f1))).toFixed(item.f1)
      }
    },    
    f6: {
      name: '成交额',
      sort: true,
      needfields: ['f6'],
      html: function(item){
        if (item.f6 == null) {
          return nonedata
        }
        return text.formatNum(item.f6)
      }
    },     
    f8: {
      name: '换手率',
      sort: true,
      needfields: ['f8', 'f152'],
      html: function(item){
        if (item.f8 == null) {
          return nonedata
        }
        return (item.f8 / Math.pow(10, item.f152)).toFixed(item.f152) + '%'
      }
    }, 
    f7: {
      name: '振幅',
      sort: true,
      needfields: ['f7', 'f152'],
      html: function(item){
        if (item.f7 == null) {
          return nonedata
        }
        return (item.f7 / Math.pow(10, item.f152)).toFixed(item.f152) + '%'
      }
    }, 
    f10: {
      name: '量比',
      sort: true,
      needfields: ['f10', 'f152'],
      html: function(item){
        if (item.f10 == null) {
          return nonedata
        }
        return (item.f10 / Math.pow(10, item.f152)).toFixed(item.f152)
      }
    },
    f15: {
      name: '最高价',
      sort: true,
      needfields: ['f1', 'f18', 'f15'],
      html: function(item){
        if (item.f15 == null) {
          return nonedata
        }
        return text.textColor((item.f15 / (Math.pow(10, item.f1))).toFixed(item.f1), item.f15 - item.f18)
      }
    },
    f16: {
      name: '最低价',
      sort: true,
      needfields: ['f1', 'f18', 'f16'],
      html: function(item){
        if (item.f16 == null) {
          return nonedata
        }
        return text.textColor((item.f16 / (Math.pow(10, item.f1))).toFixed(item.f1), item.f16 - item.f18)
      }
    },
    f17: {
      name: '开盘价',
      sort: true,
      needfields: ['f1', 'f17', 'f18'],
      html: function(item){
        if (item.f17 == null) {
          return nonedata
        }
        return text.textColor((item.f17 / (Math.pow(10, item.f1))).toFixed(item.f1), item.f17 - item.f18)
      }
    },
    
    f22: {
      name: '涨速',
      sort: true,
      needfields: ['f22', 'f152'],
      html: function(item){
        if (item.f22 == null) {
          return nonedata
        }
        return text.textColor((item.f22 / Math.pow(10, item.f152)).toFixed(item.f152) + '%', item.f22)
      }
    },   
    f9: {
      name: '市盈率',
      sort: true,
      needfields: ['f9', 'f152'],
      html: function(item){
        if (item.f9 == null) {
          return nonedata
        }
        return (item.f9 / Math.pow(10, item.f152)).toFixed(item.f152)
      }
    },        
    f62: {
      name: '主力净流入',
      sort: true,
      needfields: ['f62'],
      html: function(item){
        if (item.f62 == null) {
          return nonedata
        }
        return text.textColor(text.formatNum(item.f62), item.f62)
      }
    },
    f63: {
      name: '集合竞价',
      sort: true,
      needfields: ['f63'],
      html: function(item){
        if (item.f63 == null) {
          return nonedata
        }
        return Math.round(item.f63 / 10000)
      }
    },
    f64: {
      name: '超大单流入',
      sort: true,
      needfields: ['f64'],
      html: function(item){
        if (item.f64 == null) {
          return nonedata
        }
        return text.textColor(text.formatNum(item.f64), item.f64)
      }
    },
    f65: {
      name: '超大单流出',
      sort: true,
      needfields: ['f65'],
      html: function(item){
        if (item.f65 == null) {
          return nonedata
        }
        var value = item.f65
        return text.textColor(text.formatNum(value), -1)
      }
    },  
    f66: {
      name: '超大单净额',
      sort: true,
      needfields: ['f66'],
      html: function(item){
        if (item.f66 == null) {
          return nonedata
        }
        return text.textColor(text.formatNum(item.f66), item.f66)
      }
    },     
    f69: {
      name: '超大单净占比',
      sort: true,
      needfields: ['f69', 'f152'],
      html: function(item){
        if (item.f69 == null) {
          return nonedata
        }
        return text.textColor((item.f69 / Math.pow(10, item.f152)).toFixed(item.f152) + '%', item.f69)
      }
    },
    f70: {
      name: '大单流入',
      sort: true,
      needfields: ['f70'],
      html: function(item){
        if (item.f70 == null) {
          return nonedata
        }
        return text.textColor(text.formatNum(item.f70), item.f70)
      }
    },
    f71: {
      name: '大单流出',
      sort: true,
      needfields: ['f71'],
      html: function(item){
        if (item.f71 == null) {
          return nonedata
        }
        var value = item.f71
        // if (item.f71 > 0) {
        //   value = item.f71
        // }
        return text.textColor(text.formatNum(value), -1)
      }
    },  
    f72: {
      name: '大单净额',
      sort: true,
      needfields: ['f72'],
      html: function(item){
        if (item.f72 == null) {
          return nonedata
        }
        return text.textColor(text.formatNum(item.f72), item.f72)
      }
    },     
    f75: {
      name: '大单净占比',
      sort: true,
      needfields: ['f75', 'f152'],
      html: function(item){
        if (item.f75 == null) {
          return nonedata
        }
        return text.textColor((item.f75 / Math.pow(10, item.f152)).toFixed(item.f152) + '%', item.f75)
      }
    },
    f76: {
      name: '中单流入',
      sort: true,
      needfields: ['f76'],
      html: function(item){
        if (item.f76 == null) {
          return nonedata
        }
        return text.textColor(text.formatNum(item.f76), item.f76)
      }
    },
    f77: {
      name: '中单流出',
      sort: true,
      needfields: ['f77'],
      html: function(item){
        if (item.f77 == null) {
          return nonedata
        }
        var value = item.f77
        // if (item.f77 > 0) {
        //   value = item.f77
        // }
        return text.textColor(text.formatNum(value), -1)
      }
    },  
    f78: {
      name: '中单净额',
      sort: true,
      needfields: ['f78'],
      html: function(item){
        if (item.f78 == null) {
          return nonedata
        }
        return text.textColor(text.formatNum(item.f78), item.f78)
      }
    },     
    f81: {
      name: '中单净占比',
      sort: true,
      needfields: ['f81', 'f152'],
      html: function(item){
        if (item.f81 == null) {
          return nonedata
        }
        return text.textColor((item.f81 / Math.pow(10, item.f152)).toFixed(item.f152) + '%', item.f81)
      }
    },    
    f82: {
      name: '小单流入',
      sort: true,
      needfields: ['f82'],
      html: function(item){
        if (item.f82 == null) {
          return nonedata
        }
        return text.textColor(text.formatNum(item.f82), item.f82)
      }
    },
    f83: {
      name: '小单流出',
      sort: true,
      needfields: ['f83'],
      html: function(item){
        if (item.f83 == null) {
          return nonedata
        }
        var value = item.f83
        // if (item.f83 > 0) {
        //   value = item.f83
        // }
        return text.textColor(text.formatNum(value), -1)
      }
    },  
    f84: {
      name: '小单净额',
      sort: true,
      needfields: ['f84'],
      html: function(item){
        if (item.f84 == null) {
          return nonedata
        }
        return text.textColor(text.formatNum(item.f84), item.f84)
      }
    },     
    f87: {
      name: '小单净占比',
      sort: true,
      needfields: ['f87', 'f152'],
      html: function(item){
        if (item.f87 == null) {
          return nonedata
        }
        return text.textColor((item.f87 / Math.pow(10, item.f152)).toFixed(item.f152) + '%', item.f87)
      }
    }, 
    f88: {
      name: '当日DDX',
      sort: true,
      needfields: ['f88', 'f153'],
      html: function(item){
        if (item.f88 == null) {
          return nonedata
        }
        return text.textColor((item.f88 / Math.pow(10, item.f153)).toFixed(item.f153), item.f88)
      }
    }, 
    f89: {
      name: '当日DDY',
      sort: true,
      needfields: ['f89', 'f153'],
      html: function(item){
        if (item.f89 == null) {
          return nonedata
        }
        return text.textColor((item.f89 / Math.pow(10, item.f153)).toFixed(item.f153), item.f89)
      }
    },   
    f90: {
      name: '当日DDZ',
      sort: true,
      needfields: ['f90', 'f152'],
      html: function(item){
        if (item.f90 == null) {
          return nonedata
        }
        return text.textColor((item.f90 / Math.pow(10, item.f152)).toFixed(item.f152), item.f90)
      }
    }, 
    f91: {
      name: '5日DDX',
      sort: true,
      needfields: ['f91', 'f153'],
      html: function(item){
        if (item.f91 == null) {
          return nonedata
        }
        return text.textColor((item.f91 / Math.pow(10, item.f153)).toFixed(item.f153), item.f91)
      }
    }, 
    f92: {
      name: '5日DDY',
      sort: true,
      needfields: ['f92', 'f153'],
      html: function(item){
        if (item.f92 == null) {
          return nonedata
        }
        return text.textColor((item.f92 / Math.pow(10, item.f153)).toFixed(item.f153), item.f92)
      }
    },   
    // f93: {
    //   name: '5日DDZ',
    //   needfields: ['f93'],
    //   html: function(item){
    //     return text.textColor((item.f93 / 100).toFixed(2), item.f93)
    //   }
    // },
    f94: {
      name: '10日DDX',
      sort: true,
      needfields: ['f94', 'f153'],
      html: function(item){
        if (item.f94 == null) {
          return nonedata
        }
        return text.textColor((item.f94 / Math.pow(10, item.f153)).toFixed(item.f153), item.f94)
      }
    }, 
    f95: {
      name: '10日DDY',
      sort: true,
      needfields: ['f95', 'f153'],
      html: function(item){
        if (item.f95 == null) {
          return nonedata
        }
        return text.textColor((item.f95 / Math.pow(10, item.f153)).toFixed(item.f153), item.f95)
      }
    },   
    // f96: {
    //   name: '10日DDZ',
    //   needfields: ['f96'],
    //   html: function(item){
    //     return text.textColor((item.f96 / 100).toFixed(2), item.f96)
    //   }
    // }, 
    f97: {
      name: 'DDX飘红天数(连续)',
      sort: true,
      needfields: ['f97'],
      html: function(item){
        if (item.f97 == null) {
          return nonedata
        }
        return text.textColor(item.f97, item.f97)
      }
    }, 
    f98: {
      name: 'DDX飘红天数(5日)',
      sort: true,
      needfields: ['f98'],
      html: function(item){
        if (item.f98 == null) {
          return nonedata
        }
        return text.textColor(item.f98, item.f98)
      }
    },   
    f99: {
      name: 'DDX飘红天数(10日)',
      sort: true,
      needfields: ['f99'],
      html: function(item){
        if (item.f99 == null) {
          return nonedata
        }
        return text.textColor(item.f99, item.f99)
      }
    },
    f38: {
      name: '总股本',
      sort: true,
      needfields: ['f38'],
      html: function(item){
        if (item.f38 == null) {
          return nonedata
        }
        return text.formatNum(item.f38)
      }
    },    
    f39: {
      name: '流通股',
      sort: true,
      needfields: ['f39'],
      html: function(item){
        if (item.f39 == null) {
          return nonedata
        }
        return text.formatNum(item.f39)
      }
    },
    f36: {
      name: '人均持股数',
      sort: true,
      needfields: ['f36'],
      html: function(item){
        if (item.f36 == null) {
          return nonedata
        }
        return text.formatNum(Math.floor(item.f36))
      }
    },
    f112: {
      name: '每股收益',
      sort: true,
      needfields: ['f112'],
      html: function(item){
        if (item.f112 == null) {
          return nonedata
        }
        return item.f112.toFixed(2)
      }
    },
    f221: {
      name: '更新日期',
      sort: true,
      needfields: ['f221'],
      html: function(item){
        if (item.f221 == null || item.f221 == 0 || item.f221 == 10101) {
          return nonedata
        }
        var back = ''
        try{
          back = item.f221.toString()
          back = back.substring(0,4) + '-' + back.substring(4,6) + '-' + back.substring(6,8)
        }
        catch(error){

        }
        if (back == '') {
          return nonedata
        }
        return back
      }
    },    
    f113: {
      name: '每股净资产',
      sort: true,
      needfields: ['f113'],
      html: function(item){
        if (item.f113 == null) {
          return nonedata
        }
        return item.f113.toFixed(2)
      }
    },    
    f37: {
      name: '净资产收益率(加权)',
      sort: true,
      needfields: ['f37'],
      html: function(item){
        if (item.f37 == null) {
          return nonedata
        }
        return item.f37.toFixed(2)
      }
    },
    f40: {
      name: '营业收入',
      sort: true,
      needfields: ['f40'],
      html: function(item){
        if (item.f40 == null) {
          return nonedata
        }
        return text.formatNum(item.f40)
      }
    },
    f41: {
      name: '营业收入同比',
      sort: true,
      needfields: ['f41'],
      html: function(item){
        if (item.f41 == null) {
          return nonedata
        }
        return item.f41.toFixed(2)
      }
    },
    f42: {
      name: '营业利润',
      sort: true,
      needfields: ['f42'],
      html: function(item){
        if (item.f42 == null) {
          return nonedata
        }
        return text.formatNum(item.f42)
      }
    }, 
    f43: {
      name: '投资收益',
      sort: true,
      needfields: ['f43'],
      html: function(item){
        if (item.f43 == null) {
          return nonedata
        }
        return text.formatNum(item.f43)
      }
    }, 
    f44: {
      name: '利润总额',
      sort: true,
      needfields: ['f44'],
      html: function(item){
        if (item.f44 == null) {
          return nonedata
        }
        return text.formatNum(item.f44)
      }
    },   
    f45: {
      name: '净利润',
      sort: true,
      needfields: ['f45'],
      html: function(item){
        if (item.f45 == null) {
          return nonedata
        }
        return text.formatNum(item.f45)
      }
    },      
    f46: {
      name: '净利润同比',
      sort: true,
      needfields: ['f46'],
      html: function(item){
        if (item.f46 == null) {
          return nonedata
        }
        return item.f46.toFixed(2)
      }
    },  
    f47: {
      name: '未分配利润',
      sort: true,
      needfields: ['f47'],
      html: function(item){
        if (item.f47== null) {
          return nonedata
        }
        return text.formatNum(item.f47)
      }
    },  
    f48: {
      name: '每股未分配利润',
      sort: true,
      needfields: ['f48'],
      html: function(item){
        if (item.f48 == null) {
          return nonedata
        }
        return item.f48.toFixed(2)
      }
    }, 
    f49: {
      name: '毛利率',
      sort: true,
      needfields: ['f49'],
      html: function(item){
        if (item.f49 == null) {
          return nonedata
        }
        return item.f49.toFixed(2)
      }
    },    
    f50: {
      name: '总资产',
      sort: true,
      needfields: ['f50'],
      html: function(item){
        if (item.f50 == null) {
          return nonedata
        }
        return text.formatNum(item.f50)
      }
    }, 
    f51: {
      name: '流动资产',
      sort: true,
      needfields: ['f51'],
      html: function(item){
        if (item.f51 == null) {
          return nonedata
        }
        return text.formatNum(item.f51)
      }
    }, 
    f52: {
      name: '固定资产',
      sort: true,
      needfields: ['f52'],
      html: function(item){
        if (item.f52 == null) {
          return nonedata
        }
        return text.formatNum(item.f52)
      }
    },     
    f53: {
      name: '无形资产',
      sort: true,
      needfields: ['f53'],
      html: function(item){
        if (item.f53 == null) {
          return nonedata
        }
        return text.formatNum(item.f53)
      }
    },                       
    f54: {
      name: '总负债',
      sort: true,
      needfields: ['f54'],
      html: function(item){
        if (item.f54 == null) {
          return nonedata
        }
        return text.formatNum(item.f54)
      }
    }, 
    f55: {
      name: '流动负债',
      sort: true,
      needfields: ['f55'],
      html: function(item){
        if (item.f55 == null) {
          return nonedata
        }
        return text.formatNum(item.f55)
      }
    },     
    f56: {
      name: '长期负债',
      sort: true,
      needfields: ['f56'],
      html: function(item){
        if (item.f56 == null) {
          return nonedata
        }
        return text.formatNum(item.f56)
      }
    },     
    f57: {
      name: '资产负债比率',
      sort: true,
      needfields: ['f57'],
      html: function(item){
        if (item.f57 == null) {
          return nonedata
        }
        return item.f57.toFixed(2)
      }
    }, 
    f58: {
      name: '股东权益',
      sort: true,
      needfields: ['f58'],
      html: function(item){
        if (item.f58 == null) {
          return nonedata
        }
        return text.formatNum(item.f58)
      }
    }, 
    f59: {
      name: '股东权益比',
      sort: true,
      needfields: ['f59'],
      html: function(item){
        if (item.f59 == null) {
          return nonedata
        }
        return item.f59.toFixed(2)
      }
    },     
    f60: {
      name: '公积金',
      sort: true,
      needfields: ['f60'],
      html: function(item){
        if (item.f60 == null) {
          return nonedata
        }
        return text.formatNum(item.f60)
      }
    }, 
    f61: {
      name: '每股公积金',
      sort: true,
      needfields: ['f61'],
      html: function(item){
        if (item.f61 == null) {
          return nonedata
        }
        return item.f61.toFixed(2)
      }
    },
    f26: {
      name: '上市日期',
      sort: true,
      needfields: ['f26'],
      html: function(item){
        if (item.f26 == null) {
          return nonedata
        }
        item.f26 = item.f26.toString()
        if (item.f26.length <6) {
          return '-'
        }
        return item.f26.substring(0,4) + '-' + item.f26.substring(4,6) + '-' + item.f26.substring(6)
      }
    },
    

    c1: {
      name: '买入均价',
      sort: true,
      needfields: [],
      sortnum: function(hqdata, notedata){
        return notedata[1]
      },
      html: function(item, i, isshort, extradata){
        // // console.info(item)
        // var sid = item.f13.toString() + '.' + item.f12
        // console.info(sid)
        // var thisnote = datacache.notedata.find(function(v){
        //   return v.sid == sid
        // })
        // console.info(thisnote)
        return extradata.notedata.note[1]
      }
    },
    c2: {
      name: '持有量(股)',
      sort: true,
      needfields: [],
      sortnum: function(hqdata, notedata){
        return notedata[0]
      },
      html: function(item, i, isshort, extradata){
        // return datacache.notedata[i].note[0]
        return extradata.notedata.note[0]
      }
    },
    c3: {
      name: '买入成本',
      sort: true,
      needfields: [],
      sortnum: function(hqdata, notedata){
        var node = notedata
        var back = parseFloat(node[1]*node[0])+ parseFloat(node[3])+parseFloat(node[1]*node[0])*(parseFloat(node[2])+parseFloat(node[4]))/1000
        return back
      },
      html: function(item, i, isshort, extradata){
        var node = extradata.notedata.note
        var back = parseFloat(node[1]*node[0])+ parseFloat(node[3])+parseFloat(node[1]*node[0])*(parseFloat(node[2])+parseFloat(node[4]))/1000
        return text.formatNum(back.toFixed(2))
      }
    },
    c4: {
      name: '当前市值',
      sort: true,
      needfields: [],
      sortnum: function(hqdata, notedata){
        var node = notedata
        var back = node[0] * (hqdata.f2 / (Math.pow(10, hqdata.f1)))
        return back
      },
      html: function(item, i, isshort, extradata){
        var node = extradata.notedata.note
        var back = node[0] * (item.f2 / (Math.pow(10, item.f1)))
        return text.formatNum(back.toFixed(2))
      }
    },
    c5: {
      name: '每股盈亏',
      sort: true,
      needfields: [],
      sortnum: function(hqdata, notedata){
        var note = notedata
        if (note[0] > 0 && note[1] > 0) {
          var back = (hqdata.f2 / (Math.pow(10, hqdata.f1))) - note[1]
          return back
        }
        return 0
      },
      html: function(item, i, isshort, extradata){
        var note = extradata.notedata.note
        if (note[0] > 0 && note[1] > 0) {
          var back = (item.f2 / (Math.pow(10, item.f1))) - note[1]
          return text.textColor(back.toFixed(2), back)
        }
        return '0.00'
      }
    },
    c6: {
      name: '盈亏率',
      sort: true,
      needfields: [],
      sortnum: function(hqdata, notedata){
        var note = notedata
        if (note[1] == 0 || note[0] == 0 ) {
          return 0
        }
        var sz = note[0] * (hqdata.f2 / (Math.pow(10, hqdata.f1)))
        var cb = parseFloat(note[1]*note[0])+ parseFloat(note[3])+parseFloat(note[1]*note[0])*(parseFloat(note[2])+parseFloat(note[4]))/1000

        var back = (sz/cb - 1) * 100
        return back
      },
      html: function(item, i, isshort, extradata){
        var note = extradata.notedata.note
        if (note[1] == 0 || note[0] == 0 ) {
          return '0'
        }
        var sz = note[0] * (item.f2 / (Math.pow(10, item.f1)))
        var cb = parseFloat(note[1]*note[0])+ parseFloat(note[3])+parseFloat(note[1]*note[0])*(parseFloat(note[2])+parseFloat(note[4]))/1000

        var back = (sz/cb - 1) * 100
        return text.textColor(back.toFixed(2) + '%', back)
      }
    },
    c7: {
      name: '浮动盈亏',
      sort: true,
      needfields: [],
      sortnum: function(hqdata, notedata){
        var note = notedata
        if (note[1] == 0) {
          return 0
        }
        //var back = ((item.f2 / (Math.pow(10, item.f1))) - note[1]) * note[0]
        //console.info(back)
        var dqsz = note[0] * (hqdata.f2 / (Math.pow(10, hqdata.f1)))
        var mrcb = parseFloat(note[1]*note[0])+ parseFloat(note[3])+parseFloat(note[1]*note[0])*(parseFloat(note[2])+parseFloat(note[4]))/1000
        var back = dqsz - mrcb
        return back
      },
      html: function(item, i, isshort, extradata){
        var note = extradata.notedata.note
        if (note[1] == 0) {
          return '0.00'
        }
        //var back = ((item.f2 / (Math.pow(10, item.f1))) - note[1]) * note[0]
        //console.info(back)
        var dqsz = note[0] * (item.f2 / (Math.pow(10, item.f1)))
        var mrcb = parseFloat(note[1]*note[0])+ parseFloat(note[3])+parseFloat(note[1]*note[0])*(parseFloat(note[2])+parseFloat(note[4]))/1000
        var back = dqsz - mrcb
        return text.textColor(text.formatNum(back.toFixed(2)), back)
      }
    },

    f100: {
      name: '所属行业板块',
      needfields: ['f100'],
      align: 'txt',
      html: function(item){
        if (item.f100 == null) {
          return nonedata
        }
        return item.f100
      }
    },
    f102: {
      name: '所属地区板块',
      needfields: ['f102'],
      align: 'txt',
      html: function(item){
        if (item.f102 == null) {
          return nonedata
        }
        return item.f102
      }
    },
    f103: {
      name: '所属概念板块',
      needfields: ['f103'],
      align: 'txt',
      html: function(item){
        if (item.f103 == null) {
          return nonedata
        }
        if (item.f103) {
          return '<span title="' + item.f103 + '">' + item.f103.split(',')[0] + '</span>'
        }
        return item.f103
      }
    },    

    //盈利预测字段
    y1: {
      name: '研报数',
      needfields: [],
      html: function(item, i){
        return datacache.ylycdata[i][27]
      }
    },

    y2: {
      name: '评级统计(六个月)买入',
      shortname: '买入评级',
      needfields: [],
      html: function(item, i){
        return datacache.ylycdata[i][28]
      }
    },
    y3: {
      name: '评级统计(六个月)增持',
      shortname: '增持评级',
      needfields: [],
      html: function(item, i){
        return datacache.ylycdata[i][29]
      }
    },
    y4: {
      name: '评级统计(六个月)中性',
      shortname: '中性评级',
      needfields: [],
      html: function(item, i){
        return datacache.ylycdata[i][30]
      }
    },
    y5: {
      name: '评级统计(六个月)减持',
      shortname: '减持评级',
      needfields: [],
      html: function(item, i){
        return datacache.ylycdata[i][31]
      }
    },
    y6: {
      name: '评级统计(六个月)卖出',
      shortname: '卖出评级',
      needfields: [],
      html: function(item, i){
        return datacache.ylycdata[i][32]
      }
    },
    y7: {
      name: function(){
        return datacache.ylyc_year + '实际收益'
      },
      needfields: [],
      html: function(item, i){
        return parseFloat(datacache.ylycdata[i][8]).toFixed(3)
      }
    },
    y8: {
      name:  function(){
        return datacache.ylyc_year + 1 + '预测收益'
      },
      needfields: [],
      html: function(item, i){
        return parseFloat(datacache.ylycdata[i][9]).toFixed(3)
      }
    },
    y9: {
      name:  function(){
        return datacache.ylyc_year + 1 + '预测市盈率'
      },
      needfields: [],
      html: function(item, i){
        return parseFloat(datacache.ylycdata[i][17]).toFixed(3)
      }
    },

    y10: {
      name:  function(){
        return datacache.ylyc_year + 2 + '预测收益'
      },
      needfields: [],
      html: function(item, i){
        return parseFloat(datacache.ylycdata[i][10]).toFixed(3)
      }
    },
    y11: {
      name:  function(){
        return datacache.ylyc_year + 2 + '预测市盈率'
      },
      needfields: [],
      html: function(item, i){
        return parseFloat(datacache.ylycdata[i][18]).toFixed(3)
      }
    },    

    y12: {
      name:  function(){
        return datacache.ylyc_year + 3 + '预测收益'
      },
      needfields: [],
      html: function(item, i){
        return parseFloat(datacache.ylycdata[i][11]).toFixed(3)
      }
    },
    y13: {
      name:  function(){
        return datacache.ylyc_year + 3 + '预测市盈率'
      },
      needfields: [],
      html: function(item, i){
        return parseFloat(datacache.ylycdata[i][19]).toFixed(3)
      }
    },
    lite1: {
      name:  function(){
        return '<a href="javascript:;" class="litemovelr" target="_self"><span class="icon_left"></span></a>'
      },
      needfields: [],
      html: function(item, i){
        return ''
      }
    },
    lite2: {
      name:  function(){
        return '<a href="javascript:;" class="litemovelr" target="_self"><span class="icon_right"></span></a>'
      },
      needfields: [],
      html: function(item, i){
        return ''
      }
    }
    
    
    
    
    //,       
    // s1: {
    //   name:  function(){
    //     return '增加指标'
    //   },
    //   needfields: [],
    //   html: function(item, i){
    //     return '增加指标'
    //   }      
    // }
    

  },
  type_config: {
    all_zx: { //所有字段
      show_fields: [
        '————基础类————',
        'f100',
        'f102',
        'f103',
        '————行情类————',
        'f2', 'f3', 'f4', 'f5', 'f30', 'f31', 'f32', 'f18', 'f6', 'f8', 'f7', 'f10', 'f22', 'f9', 'f15', 'f16', 'f17',
        '———资金流向类———',
        'f62', 'f63', 'f64', 'f65', 'f66', 'f69', 'f70', 'f71', 'f72', 'f75', 'f76', 'f77', 'f78', 'f81', 'f82', 'f83', 'f84', 'f87',
        '———DDE决策类———',
        'f88', 'f89', 'f90', 'f91', 'f92', 'f94', 'f95', 'f97', 'f98', 'f99',
        '———财务数据类———',
        'f38', 'f39', 'f36', 'f112', 'f113', 'f37', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f26'
      ]
    },
    required: { //必选字段
      show_fields:['f12', 'f14', 'z1']
    },
    default_zx: { //默认字段
      show_fields: ['f2', 'f3', 'f4', 'f5', 'f30', 'f31', 'f32', 'f18', 'f6', 'f8', 'f7', 'f10', 'f22', 'f9', 'f112', 'f100']
    },
    default_zx_lite: { //默认字段 lite
      show_fields: ['lite1', 'f2', 'f3', 'f4', 'f5', 'f30', 'f31', 'f32', 'f18', 'f8', 'f6', 'f9', 'lite2']
    },
    // zx: { //当前自选字段
    //   show_fields: ['f12', 'f14', 'f2', 'f3', 'f4', 'f5', 'f30', 'f31', 'f32', 'f18', 'f6', 'f8', 'f7', 'f10', 'f22', 'f9']
    // },
    zjl: {
      show_fields: ['f2', 'f3', 'f62', 'f63', 'f64', 'f65', 'f66', 'f69', 'f70', 'f71', 'f72', 'f75', 'f76', 'f77', 'f78', 'f81', 'f82', 'f83', 'f84', 'f87']
    },
    zjl_lite: {
      show_fields: ['lite1', 'f2', 'f3', 'f62', 'f63', 'f69', 'f75', 'f81', 'f87', 'lite2']
    },    
    ddejc: {
      show_fields: ['f2', 'f3', 'f88', 'f89', 'f90', 'f91', 'f92', 'f94', 'f95', 'f97', 'f98', 'f99']
    },
    ddejc_lite: {
      show_fields: ['lite1', 'f2', 'f3', 'f97', 'f88', 'f89', 'f90', 'f91', 'f92', 'f94', 'f95', 'lite2']
    },    
    cwsj:{
      show_fields: ['f2', 'f3', 'f221', 'f38', 'f39', 'f36', 'f112', 'f113', 'f37', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f26']   
    },
    cwsj_lite:{
      show_fields: ['lite1', 'f2', 'f3', 'f221', 'f38', 'f39', 'f36', 'f112', 'f113', 'f40', 'f42', 'f50', 'lite2']   
    },    
    ykyl: {
      show_fields: ['f2', 'f3', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7']
    },
    ykyl_lite: {
      show_fields: ['lite1', 'f2', 'f3', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'lite2']
    },    
    ylyc: {
      show_fields: ['f2', 'f3', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 'y8', 'y9', 'y10', 'y11', 'y12', 'y13']
    },
    ylyc_lite: {
      show_fields: ['lite1','f2', 'f3', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 'y8', 'lite2']
    }
  }
}

/***/ }),

/***/ "./modules/zxg/note.html":
/*!*******************************!*\
  !*** ./modules/zxg/note.html ***!
  \*******************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"stocknote\">\r\n  <form target=\"_self\" id=\"noteform\">\r\n  <div class=\"exchangestock\">\r\n    <div class=\"leftexchange\"><span id=\"note_stockname\">{{=it.name}}</span> &nbsp; <span id=\"note_code\">{{=it.code}}</span> &nbsp; <span>当前</span> <span\r\n        id=\"note_nowprice\">{{=it.nowprice}}</span></div>\r\n    <div class=\"rightexchange\"><span>我在</span> <span>{{=it.inputdate}}</span> &nbsp; <span>当日价</span> <span\r\n       >{{=it.thatprice}}</span> <span>添加该股</span></div>\r\n  </div>\r\n  <table class=\"extable\">\r\n    <thead>\r\n      <tr>\r\n        <td>数量</td>\r\n        <td>买入价</td>\r\n        <td>目标价</td>\r\n        <td>止损价</td>\r\n        <td>佣金‰</td>\r\n        <td>手续费（元）</td>\r\n        <td>印花税‰</td>\r\n        <td>交易（买入）日期</td>\r\n      </tr>\r\n    </thead>\r\n    <tbody>\r\n      <tr>\r\n        <td><input type=\"text\" class=\"c\" maxlength=\"6\" value=\"{{= it.data[0]}}\"></td>\r\n        <td><input type=\"text\" class=\"p\" maxlength=\"6\" value=\"{{= it.data[1]}}\"></td>\r\n        <td><input type=\"text\" class=\"m\" maxlength=\"6\" value=\"{{= it.data[5]}}\"></td>\r\n        <td><input type=\"text\" class=\"z\" maxlength=\"6\" value=\"{{= it.data[6]}}\"></td>\r\n        <td><input type=\"text\" class=\"y\" maxlength=\"6\" value=\"{{= it.data[2]}}\"></td>\r\n        <td><input type=\"text\" class=\"x\" maxlength=\"5\" value=\"{{= it.data[3]}}\"></td>\r\n        <td><input type=\"text\" class=\"h\" maxlength=\"6\" value=\"{{= it.data[4]}}\"></td>\r\n        <td><input type=\"text\" class=\"r input2\" maxlength=\"10\" value=\"{{= it.data[7]}}\"></td>\r\n      </tr>\r\n    </tbody>\r\n  </table>\r\n  <div class=\"exchangenote\">\r\n    <div class=\"exchangenotel\">投资笔记:</div>\r\n    <div class=\"exchangenoter\">您还可以输入<span>200</span>个字</span></div>\r\n  </div>\r\n  <textarea maxlength=\"200\" class=\"b\" id=\"note_note\">{{= it.data[8]}}</textarea>\r\n  <div class=\"modalbtnd\">\r\n    <button type=\"submit\" class=\"modalbtn_default\">保 存</button> &nbsp; <a href=\"javascript:;\"\r\n        target=\"_self\" class=\"modalbtn_cancel\">取 消</a>\r\n  </div>\r\n  </form>\r\n</div>"

/***/ }),

/***/ "./modules/zxg/note.js":
/*!*****************************!*\
  !*** ./modules/zxg/note.js ***!
  \*****************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * 笔记
 */

module.exports = {
  /**
   * 获取笔记信息
   * @param {*} groupid 
   * @param {*} code 
   */
  getNoteData: function(groupid, code){
    if (code instanceof Array) {
      code = code.join(',')
    }
    return $.ajax({
      url: './api/zxg/stocknote',
      type: 'GET',
      dataType: 'json',
      cache: false,
      data: {
        groupid: groupid,
        code: code
      }
    })
    .then(function(json){
      if (json.re) {
        //if (json.result.notes.length == 1) {
        //  return json.result.notes[0]
        //}
        //else{
          return json.result.notes
        //}
      }
    })
  },
  dealNoteData: function(data){
    return data.map(function(v){
      var back = {}
      if (v.note) {
        //console.info(v.note)
        back.note = v.note.split('|').map(function(v2, i){
          if (i > 7) {
            return v2
          }
          if (v2 == '') {
            return 0
          }
          return parseFloat(v2)
        })
        //console.info(back.note)
      }
      else{
        back.note = [
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          '',
          ''
        ]
      }
      back.sid = v.sid
      back.date = v.date.split('|')
      return back
    })
  }
}

/***/ }),

/***/ "./modules/zxg/ykyl.js":
/*!*****************************!*\
  !*** ./modules/zxg/ykyl.js ***!
  \*****************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 盈亏一览
 */
var datacache = __webpack_require__(/*! ../datacache */ "./modules/datacache/index.js")
var itemconfig = __webpack_require__(/*! ./itemconfig */ "./modules/zxg/itemconfig.js")
var utils = __webpack_require__(/*! ../utils */ "./modules/utils/index.js")


var allowpx = ['c1', 'c2', 'c3'] 
var allquotepx = ['c4', 'c5', 'c6', 'c7']

/**
 * 处理盈亏一览非行情排序
 * @param {*} stocks 
 */
function dealPXStocks(stocks){
  if (datacache.pxorder != '' && allowpx.indexOf(datacache.pxtype) >= 0) {
    console.info(111)
    var stocks_extra = stocks.map(function(v){
      var thisnotedata = datacache.notedata.find(function(v2){
        return v2.sid == v
      })
      if(thisnotedata == undefined){
        thisnotedata = {
          note: [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            '',
            ''
          ]
        }
      }
      return {
        sid: v,
        num: itemconfig.item_config[datacache.pxtype].sortnum(null, thisnotedata.note)
      }
    })
    stocks_extra.sort(function(v1, v2){
      if (datacache.pxorder == 'asc') {
        return v1.num - v2.num
      }
      else{
        return v2.num - v1.num
      }
    })

    return stocks_extra.map(function(v){
      return v.sid
    })
  }
  return stocks
}

/**
 * 处理盈亏一览行情部分排序
 * @param {*} tsdata 
 */
function dealQuotePXData(tsdata){
  var tempobj = {}
  Object.keys(tsdata).forEach(function(key){
    tempobj['line' + key] = tsdata[key]
  })

  if (datacache.pxorder != '' && allquotepx.indexOf(datacache.pxtype) >= 0) {
    tempobj = utils.objectSort(tempobj, function(v1, v2){
        var v1notedata = datacache.notedata.find(function(v){
          return v.sid == v1.f13.toString() + '.' + v1.f12.toString()
        })
        var v2notedata = datacache.notedata.find(function(v){
          return v.sid == v2.f13.toString() + '.' + v2.f12.toString()
        })    
        if (datacache.pxorder == 'asc') {
          return itemconfig.item_config[datacache.pxtype].sortnum(v1, v1notedata.note) - itemconfig.item_config[datacache.pxtype].sortnum(v2, v2notedata.note)
        }
        else{
          return itemconfig.item_config[datacache.pxtype].sortnum(v2, v2notedata.note) - itemconfig.item_config[datacache.pxtype].sortnum(v1, v1notedata.note)
        }       
    })
    var now_ykyl_stock = Object.keys(tempobj).map(function(v){
      return tempobj[v].f13.toString() + '.' + tempobj[v].f12
    })

    return {
      data: tempobj,
      nowlist: now_ykyl_stock
    }
  }

  return {
    data: tempobj,
    nowlist: null
  }
}

module.exports = {
  dealPXStocks: dealPXStocks,
  dealQuotePXData: dealQuotePXData,
  allquotepx: allquotepx,
  allowpx: allowpx
}

/***/ }),

/***/ "./modules/zxg/zbsetting.html":
/*!************************************!*\
  !*** ./modules/zxg/zbsetting.html ***!
  \************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div id=\"zbsetting\">\r\n  <div class=\"zbsl\">\r\n    <div class=\"zbst\">备选数据</div>\r\n    <select class=\"zbsselect sscroll\" multiple id=\"zbssel1\"></select>\r\n  </div>\r\n  <div class=\"zbsm\">\r\n    <a href=\"javascript:;\" id=\"additem\" target=\"_self\" class=\"modalbtn_disabled smodalbtn\">添 加</a><br>\r\n    <a href=\"javascript:;\" id=\"delitem\" target=\"_self\" class=\"modalbtn_disabled smodalbtn\">删 除</a><br>\r\n    <a href=\"javascript:;\" id=\"moveup\" target=\"_self\" class=\"modalbtn_disabled smodalbtn\"><span class=\"icon icon_wuparrow\"></span></a><br>\r\n    <a href=\"javascript:;\" id=\"movedown\" target=\"_self\" class=\"modalbtn_disabled smodalbtn\"><span class=\"icon icon_wdarrow\"></span></a><br>\r\n    <a href=\"javascript:;\" id=\"resetbtn\" target=\"_self\" class=\"modalbtn_default smodalbtn\">重 置</a><br>\r\n    <a href=\"javascript:;\" id=\"clearbtn\" target=\"_self\" class=\"modalbtn_default smodalbtn\">清 空</a><br>\r\n  </div><!-- modalbtn_disabled -->\r\n  <div class=\"zbsr\">\r\n    <div class=\"zbst\">自选股</div>\r\n    <select class=\"zbsselect sscroll\" multiple id=\"zbssel2\"></select>    \r\n  </div>\r\n  <div class=\"btns\">\r\n    <a href=\"javascript:;\" target=\"_self\" id=\"setting_submit\" class=\"modalbtn_default\">确 定</a>\r\n    <a href=\"javascript:;\" target=\"_self\" id=\"setting_cancel\" class=\"modalbtn_cancel\">取 消</a>\r\n  </div>\r\n</div>"

/***/ }),

/***/ "./node_modules/dateformat/lib/dateformat.js":
/*!***************************************************!*\
  !*** ./node_modules/dateformat/lib/dateformat.js ***!
  \***************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var __WEBPACK_AMD_DEFINE_RESULT__;/*
 * Date Format 1.2.3
 * (c) 2007-2009 Steven Levithan <stevenlevithan.com>
 * MIT license
 *
 * Includes enhancements by Scott Trenda <scott.trenda.net>
 * and Kris Kowal <cixar.com/~kris.kowal/>
 *
 * Accepts a date, a mask, or a date and a mask.
 * Returns a formatted version of the given date.
 * The date defaults to the current date/time.
 * The mask defaults to dateFormat.masks.default.
 */

(function(global) {
  'use strict';

  var dateFormat = (function() {
      var token = /d{1,4}|m{1,4}|yy(?:yy)?|([HhMsTt])\1?|[LloSZWN]|"[^"]*"|'[^']*'/g;
      var timezone = /\b(?:[PMCEA][SDP]T|(?:Pacific|Mountain|Central|Eastern|Atlantic) (?:Standard|Daylight|Prevailing) Time|(?:GMT|UTC)(?:[-+]\d{4})?)\b/g;
      var timezoneClip = /[^-+\dA-Z]/g;
  
      // Regexes and supporting functions are cached through closure
      return function (date, mask, utc, gmt) {
  
        // You can't provide utc if you skip other args (use the 'UTC:' mask prefix)
        if (arguments.length === 1 && kindOf(date) === 'string' && !/\d/.test(date)) {
          mask = date;
          date = undefined;
        }
  
        date = date || new Date;
  
        if(!(date instanceof Date)) {
          date = new Date(date);
        }
  
        if (isNaN(date)) {
          throw TypeError('Invalid date');
        }
  
        mask = String(dateFormat.masks[mask] || mask || dateFormat.masks['default']);
  
        // Allow setting the utc/gmt argument via the mask
        var maskSlice = mask.slice(0, 4);
        if (maskSlice === 'UTC:' || maskSlice === 'GMT:') {
          mask = mask.slice(4);
          utc = true;
          if (maskSlice === 'GMT:') {
            gmt = true;
          }
        }
  
        var _ = utc ? 'getUTC' : 'get';
        var d = date[_ + 'Date']();
        var D = date[_ + 'Day']();
        var m = date[_ + 'Month']();
        var y = date[_ + 'FullYear']();
        var H = date[_ + 'Hours']();
        var M = date[_ + 'Minutes']();
        var s = date[_ + 'Seconds']();
        var L = date[_ + 'Milliseconds']();
        var o = utc ? 0 : date.getTimezoneOffset();
        var W = getWeek(date);
        var N = getDayOfWeek(date);
        var flags = {
          d:    d,
          dd:   pad(d),
          ddd:  dateFormat.i18n.dayNames[D],
          dddd: dateFormat.i18n.dayNames[D + 7],
          m:    m + 1,
          mm:   pad(m + 1),
          mmm:  dateFormat.i18n.monthNames[m],
          mmmm: dateFormat.i18n.monthNames[m + 12],
          yy:   String(y).slice(2),
          yyyy: y,
          h:    H % 12 || 12,
          hh:   pad(H % 12 || 12),
          H:    H,
          HH:   pad(H),
          M:    M,
          MM:   pad(M),
          s:    s,
          ss:   pad(s),
          l:    pad(L, 3),
          L:    pad(Math.round(L / 10)),
          t:    H < 12 ? dateFormat.i18n.timeNames[0] : dateFormat.i18n.timeNames[1],
          tt:   H < 12 ? dateFormat.i18n.timeNames[2] : dateFormat.i18n.timeNames[3],
          T:    H < 12 ? dateFormat.i18n.timeNames[4] : dateFormat.i18n.timeNames[5],
          TT:   H < 12 ? dateFormat.i18n.timeNames[6] : dateFormat.i18n.timeNames[7],
          Z:    gmt ? 'GMT' : utc ? 'UTC' : (String(date).match(timezone) || ['']).pop().replace(timezoneClip, ''),
          o:    (o > 0 ? '-' : '+') + pad(Math.floor(Math.abs(o) / 60) * 100 + Math.abs(o) % 60, 4),
          S:    ['th', 'st', 'nd', 'rd'][d % 10 > 3 ? 0 : (d % 100 - d % 10 != 10) * d % 10],
          W:    W,
          N:    N
        };
  
        return mask.replace(token, function (match) {
          if (match in flags) {
            return flags[match];
          }
          return match.slice(1, match.length - 1);
        });
      };
    })();

  dateFormat.masks = {
    'default':               'ddd mmm dd yyyy HH:MM:ss',
    'shortDate':             'm/d/yy',
    'mediumDate':            'mmm d, yyyy',
    'longDate':              'mmmm d, yyyy',
    'fullDate':              'dddd, mmmm d, yyyy',
    'shortTime':             'h:MM TT',
    'mediumTime':            'h:MM:ss TT',
    'longTime':              'h:MM:ss TT Z',
    'isoDate':               'yyyy-mm-dd',
    'isoTime':               'HH:MM:ss',
    'isoDateTime':           'yyyy-mm-dd\'T\'HH:MM:sso',
    'isoUtcDateTime':        'UTC:yyyy-mm-dd\'T\'HH:MM:ss\'Z\'',
    'expiresHeaderFormat':   'ddd, dd mmm yyyy HH:MM:ss Z'
  };

  // Internationalization strings
  dateFormat.i18n = {
    dayNames: [
      'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat',
      'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'
    ],
    monthNames: [
      'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
      'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
    ],
    timeNames: [
      'a', 'p', 'am', 'pm', 'A', 'P', 'AM', 'PM'
    ]
  };

function pad(val, len) {
  val = String(val);
  len = len || 2;
  while (val.length < len) {
    val = '0' + val;
  }
  return val;
}

/**
 * Get the ISO 8601 week number
 * Based on comments from
 * http://techblog.procurios.nl/k/n618/news/view/33796/14863/Calculate-ISO-8601-week-and-year-in-javascript.html
 *
 * @param  {Object} `date`
 * @return {Number}
 */
function getWeek(date) {
  // Remove time components of date
  var targetThursday = new Date(date.getFullYear(), date.getMonth(), date.getDate());

  // Change date to Thursday same week
  targetThursday.setDate(targetThursday.getDate() - ((targetThursday.getDay() + 6) % 7) + 3);

  // Take January 4th as it is always in week 1 (see ISO 8601)
  var firstThursday = new Date(targetThursday.getFullYear(), 0, 4);

  // Change date to Thursday same week
  firstThursday.setDate(firstThursday.getDate() - ((firstThursday.getDay() + 6) % 7) + 3);

  // Check if daylight-saving-time-switch occurred and correct for it
  var ds = targetThursday.getTimezoneOffset() - firstThursday.getTimezoneOffset();
  targetThursday.setHours(targetThursday.getHours() - ds);

  // Number of weeks between target Thursday and first Thursday
  var weekDiff = (targetThursday - firstThursday) / (86400000*7);
  return 1 + Math.floor(weekDiff);
}

/**
 * Get ISO-8601 numeric representation of the day of the week
 * 1 (for Monday) through 7 (for Sunday)
 * 
 * @param  {Object} `date`
 * @return {Number}
 */
function getDayOfWeek(date) {
  var dow = date.getDay();
  if(dow === 0) {
    dow = 7;
  }
  return dow;
}

/**
 * kind-of shortcut
 * @param  {*} val
 * @return {String}
 */
function kindOf(val) {
  if (val === null) {
    return 'null';
  }

  if (val === undefined) {
    return 'undefined';
  }

  if (typeof val !== 'object') {
    return typeof val;
  }

  if (Array.isArray(val)) {
    return 'array';
  }

  return {}.toString.call(val)
    .slice(8, -1).toLowerCase();
};



  if (true) {
    !(__WEBPACK_AMD_DEFINE_RESULT__ = (function () {
      return dateFormat;
    }).call(exports, __webpack_require__, exports, module),
				__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
  } else {}
})(this);


/***/ }),

/***/ "./node_modules/dot/doT.js":
/*!*********************************!*\
  !*** ./node_modules/dot/doT.js ***!
  \*********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var __WEBPACK_AMD_DEFINE_RESULT__;// doT.js
// 2011-2014, Laura Doktorova, https://github.com/olado/doT
// Licensed under the MIT license.

(function () {
	"use strict";

	var doT = {
		name: "doT",
		version: "1.1.1",
		templateSettings: {
			evaluate:    /\{\{([\s\S]+?(\}?)+)\}\}/g,
			interpolate: /\{\{=([\s\S]+?)\}\}/g,
			encode:      /\{\{!([\s\S]+?)\}\}/g,
			use:         /\{\{#([\s\S]+?)\}\}/g,
			useParams:   /(^|[^\w$])def(?:\.|\[[\'\"])([\w$\.]+)(?:[\'\"]\])?\s*\:\s*([\w$\.]+|\"[^\"]+\"|\'[^\']+\'|\{[^\}]+\})/g,
			define:      /\{\{##\s*([\w\.$]+)\s*(\:|=)([\s\S]+?)#\}\}/g,
			defineParams:/^\s*([\w$]+):([\s\S]+)/,
			conditional: /\{\{\?(\?)?\s*([\s\S]*?)\s*\}\}/g,
			iterate:     /\{\{~\s*(?:\}\}|([\s\S]+?)\s*\:\s*([\w$]+)\s*(?:\:\s*([\w$]+))?\s*\}\})/g,
			varname:	"it",
			strip:		true,
			append:		true,
			selfcontained: false,
			doNotSkipEncoded: false
		},
		template: undefined, //fn, compile template
		compile:  undefined, //fn, for express
		log: true
	}, _globals;

	doT.encodeHTMLSource = function(doNotSkipEncoded) {
		var encodeHTMLRules = { "&": "&#38;", "<": "&#60;", ">": "&#62;", '"': "&#34;", "'": "&#39;", "/": "&#47;" },
			matchHTML = doNotSkipEncoded ? /[&<>"'\/]/g : /&(?!#?\w+;)|<|>|"|'|\//g;
		return function(code) {
			return code ? code.toString().replace(matchHTML, function(m) {return encodeHTMLRules[m] || m;}) : "";
		};
	};

	_globals = (function(){ return this || (0,eval)("this"); }());

	/* istanbul ignore else */
	if ( true && module.exports) {
		module.exports = doT;
	} else if (true) {
		!(__WEBPACK_AMD_DEFINE_RESULT__ = (function(){return doT;}).call(exports, __webpack_require__, exports, module),
				__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
	} else {}

	var startend = {
		append: { start: "'+(",      end: ")+'",      startencode: "'+encodeHTML(" },
		split:  { start: "';out+=(", end: ");out+='", startencode: "';out+=encodeHTML(" }
	}, skip = /$^/;

	function resolveDefs(c, block, def) {
		return ((typeof block === "string") ? block : block.toString())
		.replace(c.define || skip, function(m, code, assign, value) {
			if (code.indexOf("def.") === 0) {
				code = code.substring(4);
			}
			if (!(code in def)) {
				if (assign === ":") {
					if (c.defineParams) value.replace(c.defineParams, function(m, param, v) {
						def[code] = {arg: param, text: v};
					});
					if (!(code in def)) def[code]= value;
				} else {
					new Function("def", "def['"+code+"']=" + value)(def);
				}
			}
			return "";
		})
		.replace(c.use || skip, function(m, code) {
			if (c.useParams) code = code.replace(c.useParams, function(m, s, d, param) {
				if (def[d] && def[d].arg && param) {
					var rw = (d+":"+param).replace(/'|\\/g, "_");
					def.__exp = def.__exp || {};
					def.__exp[rw] = def[d].text.replace(new RegExp("(^|[^\\w$])" + def[d].arg + "([^\\w$])", "g"), "$1" + param + "$2");
					return s + "def.__exp['"+rw+"']";
				}
			});
			var v = new Function("def", "return " + code)(def);
			return v ? resolveDefs(c, v, def) : v;
		});
	}

	function unescape(code) {
		return code.replace(/\\('|\\)/g, "$1").replace(/[\r\t\n]/g, " ");
	}

	doT.template = function(tmpl, c, def) {
		c = c || doT.templateSettings;
		var cse = c.append ? startend.append : startend.split, needhtmlencode, sid = 0, indv,
			str  = (c.use || c.define) ? resolveDefs(c, tmpl, def || {}) : tmpl;

		str = ("var out='" + (c.strip ? str.replace(/(^|\r|\n)\t* +| +\t*(\r|\n|$)/g," ")
					.replace(/\r|\n|\t|\/\*[\s\S]*?\*\//g,""): str)
			.replace(/'|\\/g, "\\$&")
			.replace(c.interpolate || skip, function(m, code) {
				return cse.start + unescape(code) + cse.end;
			})
			.replace(c.encode || skip, function(m, code) {
				needhtmlencode = true;
				return cse.startencode + unescape(code) + cse.end;
			})
			.replace(c.conditional || skip, function(m, elsecase, code) {
				return elsecase ?
					(code ? "';}else if(" + unescape(code) + "){out+='" : "';}else{out+='") :
					(code ? "';if(" + unescape(code) + "){out+='" : "';}out+='");
			})
			.replace(c.iterate || skip, function(m, iterate, vname, iname) {
				if (!iterate) return "';} } out+='";
				sid+=1; indv=iname || "i"+sid; iterate=unescape(iterate);
				return "';var arr"+sid+"="+iterate+";if(arr"+sid+"){var "+vname+","+indv+"=-1,l"+sid+"=arr"+sid+".length-1;while("+indv+"<l"+sid+"){"
					+vname+"=arr"+sid+"["+indv+"+=1];out+='";
			})
			.replace(c.evaluate || skip, function(m, code) {
				return "';" + unescape(code) + "out+='";
			})
			+ "';return out;")
			.replace(/\n/g, "\\n").replace(/\t/g, '\\t').replace(/\r/g, "\\r")
			.replace(/(\s|;|\}|^|\{)out\+='';/g, '$1').replace(/\+''/g, "");
			//.replace(/(\s|;|\}|^|\{)out\+=''\+/g,'$1out+=');

		if (needhtmlencode) {
			if (!c.selfcontained && _globals && !_globals._encodeHTML) _globals._encodeHTML = doT.encodeHTMLSource(c.doNotSkipEncoded);
			str = "var encodeHTML = typeof _encodeHTML !== 'undefined' ? _encodeHTML : ("
				+ doT.encodeHTMLSource.toString() + "(" + (c.doNotSkipEncoded || '') + "));"
				+ str;
		}
		try {
			return new Function(c.varname, str);
		} catch (e) {
			/* istanbul ignore else */
			if (typeof console !== "undefined") console.log("Could not create a template function: " + str);
			throw e;
		}
	};

	doT.compile = function(tmpl, def) {
		return doT.template(tmpl, null, def);
	};
}());


/***/ }),

/***/ "./node_modules/lodash/_DataView.js":
/*!******************************************!*\
  !*** ./node_modules/lodash/_DataView.js ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var getNative = __webpack_require__(/*! ./_getNative */ "./node_modules/lodash/_getNative.js"),
    root = __webpack_require__(/*! ./_root */ "./node_modules/lodash/_root.js");

/* Built-in method references that are verified to be native. */
var DataView = getNative(root, 'DataView');

module.exports = DataView;


/***/ }),

/***/ "./node_modules/lodash/_Hash.js":
/*!**************************************!*\
  !*** ./node_modules/lodash/_Hash.js ***!
  \**************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var hashClear = __webpack_require__(/*! ./_hashClear */ "./node_modules/lodash/_hashClear.js"),
    hashDelete = __webpack_require__(/*! ./_hashDelete */ "./node_modules/lodash/_hashDelete.js"),
    hashGet = __webpack_require__(/*! ./_hashGet */ "./node_modules/lodash/_hashGet.js"),
    hashHas = __webpack_require__(/*! ./_hashHas */ "./node_modules/lodash/_hashHas.js"),
    hashSet = __webpack_require__(/*! ./_hashSet */ "./node_modules/lodash/_hashSet.js");

/**
 * Creates a hash object.
 *
 * @private
 * @constructor
 * @param {Array} [entries] The key-value pairs to cache.
 */
function Hash(entries) {
  var index = -1,
      length = entries == null ? 0 : entries.length;

  this.clear();
  while (++index < length) {
    var entry = entries[index];
    this.set(entry[0], entry[1]);
  }
}

// Add methods to `Hash`.
Hash.prototype.clear = hashClear;
Hash.prototype['delete'] = hashDelete;
Hash.prototype.get = hashGet;
Hash.prototype.has = hashHas;
Hash.prototype.set = hashSet;

module.exports = Hash;


/***/ }),

/***/ "./node_modules/lodash/_ListCache.js":
/*!*******************************************!*\
  !*** ./node_modules/lodash/_ListCache.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var listCacheClear = __webpack_require__(/*! ./_listCacheClear */ "./node_modules/lodash/_listCacheClear.js"),
    listCacheDelete = __webpack_require__(/*! ./_listCacheDelete */ "./node_modules/lodash/_listCacheDelete.js"),
    listCacheGet = __webpack_require__(/*! ./_listCacheGet */ "./node_modules/lodash/_listCacheGet.js"),
    listCacheHas = __webpack_require__(/*! ./_listCacheHas */ "./node_modules/lodash/_listCacheHas.js"),
    listCacheSet = __webpack_require__(/*! ./_listCacheSet */ "./node_modules/lodash/_listCacheSet.js");

/**
 * Creates an list cache object.
 *
 * @private
 * @constructor
 * @param {Array} [entries] The key-value pairs to cache.
 */
function ListCache(entries) {
  var index = -1,
      length = entries == null ? 0 : entries.length;

  this.clear();
  while (++index < length) {
    var entry = entries[index];
    this.set(entry[0], entry[1]);
  }
}

// Add methods to `ListCache`.
ListCache.prototype.clear = listCacheClear;
ListCache.prototype['delete'] = listCacheDelete;
ListCache.prototype.get = listCacheGet;
ListCache.prototype.has = listCacheHas;
ListCache.prototype.set = listCacheSet;

module.exports = ListCache;


/***/ }),

/***/ "./node_modules/lodash/_Map.js":
/*!*************************************!*\
  !*** ./node_modules/lodash/_Map.js ***!
  \*************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var getNative = __webpack_require__(/*! ./_getNative */ "./node_modules/lodash/_getNative.js"),
    root = __webpack_require__(/*! ./_root */ "./node_modules/lodash/_root.js");

/* Built-in method references that are verified to be native. */
var Map = getNative(root, 'Map');

module.exports = Map;


/***/ }),

/***/ "./node_modules/lodash/_MapCache.js":
/*!******************************************!*\
  !*** ./node_modules/lodash/_MapCache.js ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var mapCacheClear = __webpack_require__(/*! ./_mapCacheClear */ "./node_modules/lodash/_mapCacheClear.js"),
    mapCacheDelete = __webpack_require__(/*! ./_mapCacheDelete */ "./node_modules/lodash/_mapCacheDelete.js"),
    mapCacheGet = __webpack_require__(/*! ./_mapCacheGet */ "./node_modules/lodash/_mapCacheGet.js"),
    mapCacheHas = __webpack_require__(/*! ./_mapCacheHas */ "./node_modules/lodash/_mapCacheHas.js"),
    mapCacheSet = __webpack_require__(/*! ./_mapCacheSet */ "./node_modules/lodash/_mapCacheSet.js");

/**
 * Creates a map cache object to store key-value pairs.
 *
 * @private
 * @constructor
 * @param {Array} [entries] The key-value pairs to cache.
 */
function MapCache(entries) {
  var index = -1,
      length = entries == null ? 0 : entries.length;

  this.clear();
  while (++index < length) {
    var entry = entries[index];
    this.set(entry[0], entry[1]);
  }
}

// Add methods to `MapCache`.
MapCache.prototype.clear = mapCacheClear;
MapCache.prototype['delete'] = mapCacheDelete;
MapCache.prototype.get = mapCacheGet;
MapCache.prototype.has = mapCacheHas;
MapCache.prototype.set = mapCacheSet;

module.exports = MapCache;


/***/ }),

/***/ "./node_modules/lodash/_Promise.js":
/*!*****************************************!*\
  !*** ./node_modules/lodash/_Promise.js ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var getNative = __webpack_require__(/*! ./_getNative */ "./node_modules/lodash/_getNative.js"),
    root = __webpack_require__(/*! ./_root */ "./node_modules/lodash/_root.js");

/* Built-in method references that are verified to be native. */
var Promise = getNative(root, 'Promise');

module.exports = Promise;


/***/ }),

/***/ "./node_modules/lodash/_Set.js":
/*!*************************************!*\
  !*** ./node_modules/lodash/_Set.js ***!
  \*************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var getNative = __webpack_require__(/*! ./_getNative */ "./node_modules/lodash/_getNative.js"),
    root = __webpack_require__(/*! ./_root */ "./node_modules/lodash/_root.js");

/* Built-in method references that are verified to be native. */
var Set = getNative(root, 'Set');

module.exports = Set;


/***/ }),

/***/ "./node_modules/lodash/_Stack.js":
/*!***************************************!*\
  !*** ./node_modules/lodash/_Stack.js ***!
  \***************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var ListCache = __webpack_require__(/*! ./_ListCache */ "./node_modules/lodash/_ListCache.js"),
    stackClear = __webpack_require__(/*! ./_stackClear */ "./node_modules/lodash/_stackClear.js"),
    stackDelete = __webpack_require__(/*! ./_stackDelete */ "./node_modules/lodash/_stackDelete.js"),
    stackGet = __webpack_require__(/*! ./_stackGet */ "./node_modules/lodash/_stackGet.js"),
    stackHas = __webpack_require__(/*! ./_stackHas */ "./node_modules/lodash/_stackHas.js"),
    stackSet = __webpack_require__(/*! ./_stackSet */ "./node_modules/lodash/_stackSet.js");

/**
 * Creates a stack cache object to store key-value pairs.
 *
 * @private
 * @constructor
 * @param {Array} [entries] The key-value pairs to cache.
 */
function Stack(entries) {
  var data = this.__data__ = new ListCache(entries);
  this.size = data.size;
}

// Add methods to `Stack`.
Stack.prototype.clear = stackClear;
Stack.prototype['delete'] = stackDelete;
Stack.prototype.get = stackGet;
Stack.prototype.has = stackHas;
Stack.prototype.set = stackSet;

module.exports = Stack;


/***/ }),

/***/ "./node_modules/lodash/_Symbol.js":
/*!****************************************!*\
  !*** ./node_modules/lodash/_Symbol.js ***!
  \****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var root = __webpack_require__(/*! ./_root */ "./node_modules/lodash/_root.js");

/** Built-in value references. */
var Symbol = root.Symbol;

module.exports = Symbol;


/***/ }),

/***/ "./node_modules/lodash/_Uint8Array.js":
/*!********************************************!*\
  !*** ./node_modules/lodash/_Uint8Array.js ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var root = __webpack_require__(/*! ./_root */ "./node_modules/lodash/_root.js");

/** Built-in value references. */
var Uint8Array = root.Uint8Array;

module.exports = Uint8Array;


/***/ }),

/***/ "./node_modules/lodash/_WeakMap.js":
/*!*****************************************!*\
  !*** ./node_modules/lodash/_WeakMap.js ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var getNative = __webpack_require__(/*! ./_getNative */ "./node_modules/lodash/_getNative.js"),
    root = __webpack_require__(/*! ./_root */ "./node_modules/lodash/_root.js");

/* Built-in method references that are verified to be native. */
var WeakMap = getNative(root, 'WeakMap');

module.exports = WeakMap;


/***/ }),

/***/ "./node_modules/lodash/_arrayEach.js":
/*!*******************************************!*\
  !*** ./node_modules/lodash/_arrayEach.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * A specialized version of `_.forEach` for arrays without support for
 * iteratee shorthands.
 *
 * @private
 * @param {Array} [array] The array to iterate over.
 * @param {Function} iteratee The function invoked per iteration.
 * @returns {Array} Returns `array`.
 */
function arrayEach(array, iteratee) {
  var index = -1,
      length = array == null ? 0 : array.length;

  while (++index < length) {
    if (iteratee(array[index], index, array) === false) {
      break;
    }
  }
  return array;
}

module.exports = arrayEach;


/***/ }),

/***/ "./node_modules/lodash/_arrayFilter.js":
/*!*********************************************!*\
  !*** ./node_modules/lodash/_arrayFilter.js ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * A specialized version of `_.filter` for arrays without support for
 * iteratee shorthands.
 *
 * @private
 * @param {Array} [array] The array to iterate over.
 * @param {Function} predicate The function invoked per iteration.
 * @returns {Array} Returns the new filtered array.
 */
function arrayFilter(array, predicate) {
  var index = -1,
      length = array == null ? 0 : array.length,
      resIndex = 0,
      result = [];

  while (++index < length) {
    var value = array[index];
    if (predicate(value, index, array)) {
      result[resIndex++] = value;
    }
  }
  return result;
}

module.exports = arrayFilter;


/***/ }),

/***/ "./node_modules/lodash/_arrayLikeKeys.js":
/*!***********************************************!*\
  !*** ./node_modules/lodash/_arrayLikeKeys.js ***!
  \***********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var baseTimes = __webpack_require__(/*! ./_baseTimes */ "./node_modules/lodash/_baseTimes.js"),
    isArguments = __webpack_require__(/*! ./isArguments */ "./node_modules/lodash/isArguments.js"),
    isArray = __webpack_require__(/*! ./isArray */ "./node_modules/lodash/isArray.js"),
    isBuffer = __webpack_require__(/*! ./isBuffer */ "./node_modules/lodash/isBuffer.js"),
    isIndex = __webpack_require__(/*! ./_isIndex */ "./node_modules/lodash/_isIndex.js"),
    isTypedArray = __webpack_require__(/*! ./isTypedArray */ "./node_modules/lodash/isTypedArray.js");

/** Used for built-in method references. */
var objectProto = Object.prototype;

/** Used to check objects for own properties. */
var hasOwnProperty = objectProto.hasOwnProperty;

/**
 * Creates an array of the enumerable property names of the array-like `value`.
 *
 * @private
 * @param {*} value The value to query.
 * @param {boolean} inherited Specify returning inherited property names.
 * @returns {Array} Returns the array of property names.
 */
function arrayLikeKeys(value, inherited) {
  var isArr = isArray(value),
      isArg = !isArr && isArguments(value),
      isBuff = !isArr && !isArg && isBuffer(value),
      isType = !isArr && !isArg && !isBuff && isTypedArray(value),
      skipIndexes = isArr || isArg || isBuff || isType,
      result = skipIndexes ? baseTimes(value.length, String) : [],
      length = result.length;

  for (var key in value) {
    if ((inherited || hasOwnProperty.call(value, key)) &&
        !(skipIndexes && (
           // Safari 9 has enumerable `arguments.length` in strict mode.
           key == 'length' ||
           // Node.js 0.10 has enumerable non-index properties on buffers.
           (isBuff && (key == 'offset' || key == 'parent')) ||
           // PhantomJS 2 has enumerable non-index properties on typed arrays.
           (isType && (key == 'buffer' || key == 'byteLength' || key == 'byteOffset')) ||
           // Skip index properties.
           isIndex(key, length)
        ))) {
      result.push(key);
    }
  }
  return result;
}

module.exports = arrayLikeKeys;


/***/ }),

/***/ "./node_modules/lodash/_arrayPush.js":
/*!*******************************************!*\
  !*** ./node_modules/lodash/_arrayPush.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * Appends the elements of `values` to `array`.
 *
 * @private
 * @param {Array} array The array to modify.
 * @param {Array} values The values to append.
 * @returns {Array} Returns `array`.
 */
function arrayPush(array, values) {
  var index = -1,
      length = values.length,
      offset = array.length;

  while (++index < length) {
    array[offset + index] = values[index];
  }
  return array;
}

module.exports = arrayPush;


/***/ }),

/***/ "./node_modules/lodash/_assignValue.js":
/*!*********************************************!*\
  !*** ./node_modules/lodash/_assignValue.js ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var baseAssignValue = __webpack_require__(/*! ./_baseAssignValue */ "./node_modules/lodash/_baseAssignValue.js"),
    eq = __webpack_require__(/*! ./eq */ "./node_modules/lodash/eq.js");

/** Used for built-in method references. */
var objectProto = Object.prototype;

/** Used to check objects for own properties. */
var hasOwnProperty = objectProto.hasOwnProperty;

/**
 * Assigns `value` to `key` of `object` if the existing value is not equivalent
 * using [`SameValueZero`](http://ecma-international.org/ecma-262/7.0/#sec-samevaluezero)
 * for equality comparisons.
 *
 * @private
 * @param {Object} object The object to modify.
 * @param {string} key The key of the property to assign.
 * @param {*} value The value to assign.
 */
function assignValue(object, key, value) {
  var objValue = object[key];
  if (!(hasOwnProperty.call(object, key) && eq(objValue, value)) ||
      (value === undefined && !(key in object))) {
    baseAssignValue(object, key, value);
  }
}

module.exports = assignValue;


/***/ }),

/***/ "./node_modules/lodash/_assocIndexOf.js":
/*!**********************************************!*\
  !*** ./node_modules/lodash/_assocIndexOf.js ***!
  \**********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var eq = __webpack_require__(/*! ./eq */ "./node_modules/lodash/eq.js");

/**
 * Gets the index at which the `key` is found in `array` of key-value pairs.
 *
 * @private
 * @param {Array} array The array to inspect.
 * @param {*} key The key to search for.
 * @returns {number} Returns the index of the matched value, else `-1`.
 */
function assocIndexOf(array, key) {
  var length = array.length;
  while (length--) {
    if (eq(array[length][0], key)) {
      return length;
    }
  }
  return -1;
}

module.exports = assocIndexOf;


/***/ }),

/***/ "./node_modules/lodash/_baseAssign.js":
/*!********************************************!*\
  !*** ./node_modules/lodash/_baseAssign.js ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var copyObject = __webpack_require__(/*! ./_copyObject */ "./node_modules/lodash/_copyObject.js"),
    keys = __webpack_require__(/*! ./keys */ "./node_modules/lodash/keys.js");

/**
 * The base implementation of `_.assign` without support for multiple sources
 * or `customizer` functions.
 *
 * @private
 * @param {Object} object The destination object.
 * @param {Object} source The source object.
 * @returns {Object} Returns `object`.
 */
function baseAssign(object, source) {
  return object && copyObject(source, keys(source), object);
}

module.exports = baseAssign;


/***/ }),

/***/ "./node_modules/lodash/_baseAssignIn.js":
/*!**********************************************!*\
  !*** ./node_modules/lodash/_baseAssignIn.js ***!
  \**********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var copyObject = __webpack_require__(/*! ./_copyObject */ "./node_modules/lodash/_copyObject.js"),
    keysIn = __webpack_require__(/*! ./keysIn */ "./node_modules/lodash/keysIn.js");

/**
 * The base implementation of `_.assignIn` without support for multiple sources
 * or `customizer` functions.
 *
 * @private
 * @param {Object} object The destination object.
 * @param {Object} source The source object.
 * @returns {Object} Returns `object`.
 */
function baseAssignIn(object, source) {
  return object && copyObject(source, keysIn(source), object);
}

module.exports = baseAssignIn;


/***/ }),

/***/ "./node_modules/lodash/_baseAssignValue.js":
/*!*************************************************!*\
  !*** ./node_modules/lodash/_baseAssignValue.js ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var defineProperty = __webpack_require__(/*! ./_defineProperty */ "./node_modules/lodash/_defineProperty.js");

/**
 * The base implementation of `assignValue` and `assignMergeValue` without
 * value checks.
 *
 * @private
 * @param {Object} object The object to modify.
 * @param {string} key The key of the property to assign.
 * @param {*} value The value to assign.
 */
function baseAssignValue(object, key, value) {
  if (key == '__proto__' && defineProperty) {
    defineProperty(object, key, {
      'configurable': true,
      'enumerable': true,
      'value': value,
      'writable': true
    });
  } else {
    object[key] = value;
  }
}

module.exports = baseAssignValue;


/***/ }),

/***/ "./node_modules/lodash/_baseClone.js":
/*!*******************************************!*\
  !*** ./node_modules/lodash/_baseClone.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var Stack = __webpack_require__(/*! ./_Stack */ "./node_modules/lodash/_Stack.js"),
    arrayEach = __webpack_require__(/*! ./_arrayEach */ "./node_modules/lodash/_arrayEach.js"),
    assignValue = __webpack_require__(/*! ./_assignValue */ "./node_modules/lodash/_assignValue.js"),
    baseAssign = __webpack_require__(/*! ./_baseAssign */ "./node_modules/lodash/_baseAssign.js"),
    baseAssignIn = __webpack_require__(/*! ./_baseAssignIn */ "./node_modules/lodash/_baseAssignIn.js"),
    cloneBuffer = __webpack_require__(/*! ./_cloneBuffer */ "./node_modules/lodash/_cloneBuffer.js"),
    copyArray = __webpack_require__(/*! ./_copyArray */ "./node_modules/lodash/_copyArray.js"),
    copySymbols = __webpack_require__(/*! ./_copySymbols */ "./node_modules/lodash/_copySymbols.js"),
    copySymbolsIn = __webpack_require__(/*! ./_copySymbolsIn */ "./node_modules/lodash/_copySymbolsIn.js"),
    getAllKeys = __webpack_require__(/*! ./_getAllKeys */ "./node_modules/lodash/_getAllKeys.js"),
    getAllKeysIn = __webpack_require__(/*! ./_getAllKeysIn */ "./node_modules/lodash/_getAllKeysIn.js"),
    getTag = __webpack_require__(/*! ./_getTag */ "./node_modules/lodash/_getTag.js"),
    initCloneArray = __webpack_require__(/*! ./_initCloneArray */ "./node_modules/lodash/_initCloneArray.js"),
    initCloneByTag = __webpack_require__(/*! ./_initCloneByTag */ "./node_modules/lodash/_initCloneByTag.js"),
    initCloneObject = __webpack_require__(/*! ./_initCloneObject */ "./node_modules/lodash/_initCloneObject.js"),
    isArray = __webpack_require__(/*! ./isArray */ "./node_modules/lodash/isArray.js"),
    isBuffer = __webpack_require__(/*! ./isBuffer */ "./node_modules/lodash/isBuffer.js"),
    isMap = __webpack_require__(/*! ./isMap */ "./node_modules/lodash/isMap.js"),
    isObject = __webpack_require__(/*! ./isObject */ "./node_modules/lodash/isObject.js"),
    isSet = __webpack_require__(/*! ./isSet */ "./node_modules/lodash/isSet.js"),
    keys = __webpack_require__(/*! ./keys */ "./node_modules/lodash/keys.js");

/** Used to compose bitmasks for cloning. */
var CLONE_DEEP_FLAG = 1,
    CLONE_FLAT_FLAG = 2,
    CLONE_SYMBOLS_FLAG = 4;

/** `Object#toString` result references. */
var argsTag = '[object Arguments]',
    arrayTag = '[object Array]',
    boolTag = '[object Boolean]',
    dateTag = '[object Date]',
    errorTag = '[object Error]',
    funcTag = '[object Function]',
    genTag = '[object GeneratorFunction]',
    mapTag = '[object Map]',
    numberTag = '[object Number]',
    objectTag = '[object Object]',
    regexpTag = '[object RegExp]',
    setTag = '[object Set]',
    stringTag = '[object String]',
    symbolTag = '[object Symbol]',
    weakMapTag = '[object WeakMap]';

var arrayBufferTag = '[object ArrayBuffer]',
    dataViewTag = '[object DataView]',
    float32Tag = '[object Float32Array]',
    float64Tag = '[object Float64Array]',
    int8Tag = '[object Int8Array]',
    int16Tag = '[object Int16Array]',
    int32Tag = '[object Int32Array]',
    uint8Tag = '[object Uint8Array]',
    uint8ClampedTag = '[object Uint8ClampedArray]',
    uint16Tag = '[object Uint16Array]',
    uint32Tag = '[object Uint32Array]';

/** Used to identify `toStringTag` values supported by `_.clone`. */
var cloneableTags = {};
cloneableTags[argsTag] = cloneableTags[arrayTag] =
cloneableTags[arrayBufferTag] = cloneableTags[dataViewTag] =
cloneableTags[boolTag] = cloneableTags[dateTag] =
cloneableTags[float32Tag] = cloneableTags[float64Tag] =
cloneableTags[int8Tag] = cloneableTags[int16Tag] =
cloneableTags[int32Tag] = cloneableTags[mapTag] =
cloneableTags[numberTag] = cloneableTags[objectTag] =
cloneableTags[regexpTag] = cloneableTags[setTag] =
cloneableTags[stringTag] = cloneableTags[symbolTag] =
cloneableTags[uint8Tag] = cloneableTags[uint8ClampedTag] =
cloneableTags[uint16Tag] = cloneableTags[uint32Tag] = true;
cloneableTags[errorTag] = cloneableTags[funcTag] =
cloneableTags[weakMapTag] = false;

/**
 * The base implementation of `_.clone` and `_.cloneDeep` which tracks
 * traversed objects.
 *
 * @private
 * @param {*} value The value to clone.
 * @param {boolean} bitmask The bitmask flags.
 *  1 - Deep clone
 *  2 - Flatten inherited properties
 *  4 - Clone symbols
 * @param {Function} [customizer] The function to customize cloning.
 * @param {string} [key] The key of `value`.
 * @param {Object} [object] The parent object of `value`.
 * @param {Object} [stack] Tracks traversed objects and their clone counterparts.
 * @returns {*} Returns the cloned value.
 */
function baseClone(value, bitmask, customizer, key, object, stack) {
  var result,
      isDeep = bitmask & CLONE_DEEP_FLAG,
      isFlat = bitmask & CLONE_FLAT_FLAG,
      isFull = bitmask & CLONE_SYMBOLS_FLAG;

  if (customizer) {
    result = object ? customizer(value, key, object, stack) : customizer(value);
  }
  if (result !== undefined) {
    return result;
  }
  if (!isObject(value)) {
    return value;
  }
  var isArr = isArray(value);
  if (isArr) {
    result = initCloneArray(value);
    if (!isDeep) {
      return copyArray(value, result);
    }
  } else {
    var tag = getTag(value),
        isFunc = tag == funcTag || tag == genTag;

    if (isBuffer(value)) {
      return cloneBuffer(value, isDeep);
    }
    if (tag == objectTag || tag == argsTag || (isFunc && !object)) {
      result = (isFlat || isFunc) ? {} : initCloneObject(value);
      if (!isDeep) {
        return isFlat
          ? copySymbolsIn(value, baseAssignIn(result, value))
          : copySymbols(value, baseAssign(result, value));
      }
    } else {
      if (!cloneableTags[tag]) {
        return object ? value : {};
      }
      result = initCloneByTag(value, tag, isDeep);
    }
  }
  // Check for circular references and return its corresponding clone.
  stack || (stack = new Stack);
  var stacked = stack.get(value);
  if (stacked) {
    return stacked;
  }
  stack.set(value, result);

  if (isSet(value)) {
    value.forEach(function(subValue) {
      result.add(baseClone(subValue, bitmask, customizer, subValue, value, stack));
    });

    return result;
  }

  if (isMap(value)) {
    value.forEach(function(subValue, key) {
      result.set(key, baseClone(subValue, bitmask, customizer, key, value, stack));
    });

    return result;
  }

  var keysFunc = isFull
    ? (isFlat ? getAllKeysIn : getAllKeys)
    : (isFlat ? keysIn : keys);

  var props = isArr ? undefined : keysFunc(value);
  arrayEach(props || value, function(subValue, key) {
    if (props) {
      key = subValue;
      subValue = value[key];
    }
    // Recursively populate clone (susceptible to call stack limits).
    assignValue(result, key, baseClone(subValue, bitmask, customizer, key, value, stack));
  });
  return result;
}

module.exports = baseClone;


/***/ }),

/***/ "./node_modules/lodash/_baseCreate.js":
/*!********************************************!*\
  !*** ./node_modules/lodash/_baseCreate.js ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var isObject = __webpack_require__(/*! ./isObject */ "./node_modules/lodash/isObject.js");

/** Built-in value references. */
var objectCreate = Object.create;

/**
 * The base implementation of `_.create` without support for assigning
 * properties to the created object.
 *
 * @private
 * @param {Object} proto The object to inherit from.
 * @returns {Object} Returns the new object.
 */
var baseCreate = (function() {
  function object() {}
  return function(proto) {
    if (!isObject(proto)) {
      return {};
    }
    if (objectCreate) {
      return objectCreate(proto);
    }
    object.prototype = proto;
    var result = new object;
    object.prototype = undefined;
    return result;
  };
}());

module.exports = baseCreate;


/***/ }),

/***/ "./node_modules/lodash/_baseGetAllKeys.js":
/*!************************************************!*\
  !*** ./node_modules/lodash/_baseGetAllKeys.js ***!
  \************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var arrayPush = __webpack_require__(/*! ./_arrayPush */ "./node_modules/lodash/_arrayPush.js"),
    isArray = __webpack_require__(/*! ./isArray */ "./node_modules/lodash/isArray.js");

/**
 * The base implementation of `getAllKeys` and `getAllKeysIn` which uses
 * `keysFunc` and `symbolsFunc` to get the enumerable property names and
 * symbols of `object`.
 *
 * @private
 * @param {Object} object The object to query.
 * @param {Function} keysFunc The function to get the keys of `object`.
 * @param {Function} symbolsFunc The function to get the symbols of `object`.
 * @returns {Array} Returns the array of property names and symbols.
 */
function baseGetAllKeys(object, keysFunc, symbolsFunc) {
  var result = keysFunc(object);
  return isArray(object) ? result : arrayPush(result, symbolsFunc(object));
}

module.exports = baseGetAllKeys;


/***/ }),

/***/ "./node_modules/lodash/_baseGetTag.js":
/*!********************************************!*\
  !*** ./node_modules/lodash/_baseGetTag.js ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var Symbol = __webpack_require__(/*! ./_Symbol */ "./node_modules/lodash/_Symbol.js"),
    getRawTag = __webpack_require__(/*! ./_getRawTag */ "./node_modules/lodash/_getRawTag.js"),
    objectToString = __webpack_require__(/*! ./_objectToString */ "./node_modules/lodash/_objectToString.js");

/** `Object#toString` result references. */
var nullTag = '[object Null]',
    undefinedTag = '[object Undefined]';

/** Built-in value references. */
var symToStringTag = Symbol ? Symbol.toStringTag : undefined;

/**
 * The base implementation of `getTag` without fallbacks for buggy environments.
 *
 * @private
 * @param {*} value The value to query.
 * @returns {string} Returns the `toStringTag`.
 */
function baseGetTag(value) {
  if (value == null) {
    return value === undefined ? undefinedTag : nullTag;
  }
  return (symToStringTag && symToStringTag in Object(value))
    ? getRawTag(value)
    : objectToString(value);
}

module.exports = baseGetTag;


/***/ }),

/***/ "./node_modules/lodash/_baseIsArguments.js":
/*!*************************************************!*\
  !*** ./node_modules/lodash/_baseIsArguments.js ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var baseGetTag = __webpack_require__(/*! ./_baseGetTag */ "./node_modules/lodash/_baseGetTag.js"),
    isObjectLike = __webpack_require__(/*! ./isObjectLike */ "./node_modules/lodash/isObjectLike.js");

/** `Object#toString` result references. */
var argsTag = '[object Arguments]';

/**
 * The base implementation of `_.isArguments`.
 *
 * @private
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is an `arguments` object,
 */
function baseIsArguments(value) {
  return isObjectLike(value) && baseGetTag(value) == argsTag;
}

module.exports = baseIsArguments;


/***/ }),

/***/ "./node_modules/lodash/_baseIsMap.js":
/*!*******************************************!*\
  !*** ./node_modules/lodash/_baseIsMap.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var getTag = __webpack_require__(/*! ./_getTag */ "./node_modules/lodash/_getTag.js"),
    isObjectLike = __webpack_require__(/*! ./isObjectLike */ "./node_modules/lodash/isObjectLike.js");

/** `Object#toString` result references. */
var mapTag = '[object Map]';

/**
 * The base implementation of `_.isMap` without Node.js optimizations.
 *
 * @private
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is a map, else `false`.
 */
function baseIsMap(value) {
  return isObjectLike(value) && getTag(value) == mapTag;
}

module.exports = baseIsMap;


/***/ }),

/***/ "./node_modules/lodash/_baseIsNative.js":
/*!**********************************************!*\
  !*** ./node_modules/lodash/_baseIsNative.js ***!
  \**********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var isFunction = __webpack_require__(/*! ./isFunction */ "./node_modules/lodash/isFunction.js"),
    isMasked = __webpack_require__(/*! ./_isMasked */ "./node_modules/lodash/_isMasked.js"),
    isObject = __webpack_require__(/*! ./isObject */ "./node_modules/lodash/isObject.js"),
    toSource = __webpack_require__(/*! ./_toSource */ "./node_modules/lodash/_toSource.js");

/**
 * Used to match `RegExp`
 * [syntax characters](http://ecma-international.org/ecma-262/7.0/#sec-patterns).
 */
var reRegExpChar = /[\\^$.*+?()[\]{}|]/g;

/** Used to detect host constructors (Safari). */
var reIsHostCtor = /^\[object .+?Constructor\]$/;

/** Used for built-in method references. */
var funcProto = Function.prototype,
    objectProto = Object.prototype;

/** Used to resolve the decompiled source of functions. */
var funcToString = funcProto.toString;

/** Used to check objects for own properties. */
var hasOwnProperty = objectProto.hasOwnProperty;

/** Used to detect if a method is native. */
var reIsNative = RegExp('^' +
  funcToString.call(hasOwnProperty).replace(reRegExpChar, '\\$&')
  .replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, '$1.*?') + '$'
);

/**
 * The base implementation of `_.isNative` without bad shim checks.
 *
 * @private
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is a native function,
 *  else `false`.
 */
function baseIsNative(value) {
  if (!isObject(value) || isMasked(value)) {
    return false;
  }
  var pattern = isFunction(value) ? reIsNative : reIsHostCtor;
  return pattern.test(toSource(value));
}

module.exports = baseIsNative;


/***/ }),

/***/ "./node_modules/lodash/_baseIsSet.js":
/*!*******************************************!*\
  !*** ./node_modules/lodash/_baseIsSet.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var getTag = __webpack_require__(/*! ./_getTag */ "./node_modules/lodash/_getTag.js"),
    isObjectLike = __webpack_require__(/*! ./isObjectLike */ "./node_modules/lodash/isObjectLike.js");

/** `Object#toString` result references. */
var setTag = '[object Set]';

/**
 * The base implementation of `_.isSet` without Node.js optimizations.
 *
 * @private
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is a set, else `false`.
 */
function baseIsSet(value) {
  return isObjectLike(value) && getTag(value) == setTag;
}

module.exports = baseIsSet;


/***/ }),

/***/ "./node_modules/lodash/_baseIsTypedArray.js":
/*!**************************************************!*\
  !*** ./node_modules/lodash/_baseIsTypedArray.js ***!
  \**************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var baseGetTag = __webpack_require__(/*! ./_baseGetTag */ "./node_modules/lodash/_baseGetTag.js"),
    isLength = __webpack_require__(/*! ./isLength */ "./node_modules/lodash/isLength.js"),
    isObjectLike = __webpack_require__(/*! ./isObjectLike */ "./node_modules/lodash/isObjectLike.js");

/** `Object#toString` result references. */
var argsTag = '[object Arguments]',
    arrayTag = '[object Array]',
    boolTag = '[object Boolean]',
    dateTag = '[object Date]',
    errorTag = '[object Error]',
    funcTag = '[object Function]',
    mapTag = '[object Map]',
    numberTag = '[object Number]',
    objectTag = '[object Object]',
    regexpTag = '[object RegExp]',
    setTag = '[object Set]',
    stringTag = '[object String]',
    weakMapTag = '[object WeakMap]';

var arrayBufferTag = '[object ArrayBuffer]',
    dataViewTag = '[object DataView]',
    float32Tag = '[object Float32Array]',
    float64Tag = '[object Float64Array]',
    int8Tag = '[object Int8Array]',
    int16Tag = '[object Int16Array]',
    int32Tag = '[object Int32Array]',
    uint8Tag = '[object Uint8Array]',
    uint8ClampedTag = '[object Uint8ClampedArray]',
    uint16Tag = '[object Uint16Array]',
    uint32Tag = '[object Uint32Array]';

/** Used to identify `toStringTag` values of typed arrays. */
var typedArrayTags = {};
typedArrayTags[float32Tag] = typedArrayTags[float64Tag] =
typedArrayTags[int8Tag] = typedArrayTags[int16Tag] =
typedArrayTags[int32Tag] = typedArrayTags[uint8Tag] =
typedArrayTags[uint8ClampedTag] = typedArrayTags[uint16Tag] =
typedArrayTags[uint32Tag] = true;
typedArrayTags[argsTag] = typedArrayTags[arrayTag] =
typedArrayTags[arrayBufferTag] = typedArrayTags[boolTag] =
typedArrayTags[dataViewTag] = typedArrayTags[dateTag] =
typedArrayTags[errorTag] = typedArrayTags[funcTag] =
typedArrayTags[mapTag] = typedArrayTags[numberTag] =
typedArrayTags[objectTag] = typedArrayTags[regexpTag] =
typedArrayTags[setTag] = typedArrayTags[stringTag] =
typedArrayTags[weakMapTag] = false;

/**
 * The base implementation of `_.isTypedArray` without Node.js optimizations.
 *
 * @private
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is a typed array, else `false`.
 */
function baseIsTypedArray(value) {
  return isObjectLike(value) &&
    isLength(value.length) && !!typedArrayTags[baseGetTag(value)];
}

module.exports = baseIsTypedArray;


/***/ }),

/***/ "./node_modules/lodash/_baseKeys.js":
/*!******************************************!*\
  !*** ./node_modules/lodash/_baseKeys.js ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var isPrototype = __webpack_require__(/*! ./_isPrototype */ "./node_modules/lodash/_isPrototype.js"),
    nativeKeys = __webpack_require__(/*! ./_nativeKeys */ "./node_modules/lodash/_nativeKeys.js");

/** Used for built-in method references. */
var objectProto = Object.prototype;

/** Used to check objects for own properties. */
var hasOwnProperty = objectProto.hasOwnProperty;

/**
 * The base implementation of `_.keys` which doesn't treat sparse arrays as dense.
 *
 * @private
 * @param {Object} object The object to query.
 * @returns {Array} Returns the array of property names.
 */
function baseKeys(object) {
  if (!isPrototype(object)) {
    return nativeKeys(object);
  }
  var result = [];
  for (var key in Object(object)) {
    if (hasOwnProperty.call(object, key) && key != 'constructor') {
      result.push(key);
    }
  }
  return result;
}

module.exports = baseKeys;


/***/ }),

/***/ "./node_modules/lodash/_baseKeysIn.js":
/*!********************************************!*\
  !*** ./node_modules/lodash/_baseKeysIn.js ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var isObject = __webpack_require__(/*! ./isObject */ "./node_modules/lodash/isObject.js"),
    isPrototype = __webpack_require__(/*! ./_isPrototype */ "./node_modules/lodash/_isPrototype.js"),
    nativeKeysIn = __webpack_require__(/*! ./_nativeKeysIn */ "./node_modules/lodash/_nativeKeysIn.js");

/** Used for built-in method references. */
var objectProto = Object.prototype;

/** Used to check objects for own properties. */
var hasOwnProperty = objectProto.hasOwnProperty;

/**
 * The base implementation of `_.keysIn` which doesn't treat sparse arrays as dense.
 *
 * @private
 * @param {Object} object The object to query.
 * @returns {Array} Returns the array of property names.
 */
function baseKeysIn(object) {
  if (!isObject(object)) {
    return nativeKeysIn(object);
  }
  var isProto = isPrototype(object),
      result = [];

  for (var key in object) {
    if (!(key == 'constructor' && (isProto || !hasOwnProperty.call(object, key)))) {
      result.push(key);
    }
  }
  return result;
}

module.exports = baseKeysIn;


/***/ }),

/***/ "./node_modules/lodash/_baseTimes.js":
/*!*******************************************!*\
  !*** ./node_modules/lodash/_baseTimes.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * The base implementation of `_.times` without support for iteratee shorthands
 * or max array length checks.
 *
 * @private
 * @param {number} n The number of times to invoke `iteratee`.
 * @param {Function} iteratee The function invoked per iteration.
 * @returns {Array} Returns the array of results.
 */
function baseTimes(n, iteratee) {
  var index = -1,
      result = Array(n);

  while (++index < n) {
    result[index] = iteratee(index);
  }
  return result;
}

module.exports = baseTimes;


/***/ }),

/***/ "./node_modules/lodash/_baseUnary.js":
/*!*******************************************!*\
  !*** ./node_modules/lodash/_baseUnary.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * The base implementation of `_.unary` without support for storing metadata.
 *
 * @private
 * @param {Function} func The function to cap arguments for.
 * @returns {Function} Returns the new capped function.
 */
function baseUnary(func) {
  return function(value) {
    return func(value);
  };
}

module.exports = baseUnary;


/***/ }),

/***/ "./node_modules/lodash/_cloneArrayBuffer.js":
/*!**************************************************!*\
  !*** ./node_modules/lodash/_cloneArrayBuffer.js ***!
  \**************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var Uint8Array = __webpack_require__(/*! ./_Uint8Array */ "./node_modules/lodash/_Uint8Array.js");

/**
 * Creates a clone of `arrayBuffer`.
 *
 * @private
 * @param {ArrayBuffer} arrayBuffer The array buffer to clone.
 * @returns {ArrayBuffer} Returns the cloned array buffer.
 */
function cloneArrayBuffer(arrayBuffer) {
  var result = new arrayBuffer.constructor(arrayBuffer.byteLength);
  new Uint8Array(result).set(new Uint8Array(arrayBuffer));
  return result;
}

module.exports = cloneArrayBuffer;


/***/ }),

/***/ "./node_modules/lodash/_cloneBuffer.js":
/*!*********************************************!*\
  !*** ./node_modules/lodash/_cloneBuffer.js ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(module) {var root = __webpack_require__(/*! ./_root */ "./node_modules/lodash/_root.js");

/** Detect free variable `exports`. */
var freeExports =  true && exports && !exports.nodeType && exports;

/** Detect free variable `module`. */
var freeModule = freeExports && typeof module == 'object' && module && !module.nodeType && module;

/** Detect the popular CommonJS extension `module.exports`. */
var moduleExports = freeModule && freeModule.exports === freeExports;

/** Built-in value references. */
var Buffer = moduleExports ? root.Buffer : undefined,
    allocUnsafe = Buffer ? Buffer.allocUnsafe : undefined;

/**
 * Creates a clone of  `buffer`.
 *
 * @private
 * @param {Buffer} buffer The buffer to clone.
 * @param {boolean} [isDeep] Specify a deep clone.
 * @returns {Buffer} Returns the cloned buffer.
 */
function cloneBuffer(buffer, isDeep) {
  if (isDeep) {
    return buffer.slice();
  }
  var length = buffer.length,
      result = allocUnsafe ? allocUnsafe(length) : new buffer.constructor(length);

  buffer.copy(result);
  return result;
}

module.exports = cloneBuffer;

/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! ./../webpack/buildin/module.js */ "./node_modules/webpack/buildin/module.js")(module)))

/***/ }),

/***/ "./node_modules/lodash/_cloneDataView.js":
/*!***********************************************!*\
  !*** ./node_modules/lodash/_cloneDataView.js ***!
  \***********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var cloneArrayBuffer = __webpack_require__(/*! ./_cloneArrayBuffer */ "./node_modules/lodash/_cloneArrayBuffer.js");

/**
 * Creates a clone of `dataView`.
 *
 * @private
 * @param {Object} dataView The data view to clone.
 * @param {boolean} [isDeep] Specify a deep clone.
 * @returns {Object} Returns the cloned data view.
 */
function cloneDataView(dataView, isDeep) {
  var buffer = isDeep ? cloneArrayBuffer(dataView.buffer) : dataView.buffer;
  return new dataView.constructor(buffer, dataView.byteOffset, dataView.byteLength);
}

module.exports = cloneDataView;


/***/ }),

/***/ "./node_modules/lodash/_cloneRegExp.js":
/*!*********************************************!*\
  !*** ./node_modules/lodash/_cloneRegExp.js ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/** Used to match `RegExp` flags from their coerced string values. */
var reFlags = /\w*$/;

/**
 * Creates a clone of `regexp`.
 *
 * @private
 * @param {Object} regexp The regexp to clone.
 * @returns {Object} Returns the cloned regexp.
 */
function cloneRegExp(regexp) {
  var result = new regexp.constructor(regexp.source, reFlags.exec(regexp));
  result.lastIndex = regexp.lastIndex;
  return result;
}

module.exports = cloneRegExp;


/***/ }),

/***/ "./node_modules/lodash/_cloneSymbol.js":
/*!*********************************************!*\
  !*** ./node_modules/lodash/_cloneSymbol.js ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var Symbol = __webpack_require__(/*! ./_Symbol */ "./node_modules/lodash/_Symbol.js");

/** Used to convert symbols to primitives and strings. */
var symbolProto = Symbol ? Symbol.prototype : undefined,
    symbolValueOf = symbolProto ? symbolProto.valueOf : undefined;

/**
 * Creates a clone of the `symbol` object.
 *
 * @private
 * @param {Object} symbol The symbol object to clone.
 * @returns {Object} Returns the cloned symbol object.
 */
function cloneSymbol(symbol) {
  return symbolValueOf ? Object(symbolValueOf.call(symbol)) : {};
}

module.exports = cloneSymbol;


/***/ }),

/***/ "./node_modules/lodash/_cloneTypedArray.js":
/*!*************************************************!*\
  !*** ./node_modules/lodash/_cloneTypedArray.js ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var cloneArrayBuffer = __webpack_require__(/*! ./_cloneArrayBuffer */ "./node_modules/lodash/_cloneArrayBuffer.js");

/**
 * Creates a clone of `typedArray`.
 *
 * @private
 * @param {Object} typedArray The typed array to clone.
 * @param {boolean} [isDeep] Specify a deep clone.
 * @returns {Object} Returns the cloned typed array.
 */
function cloneTypedArray(typedArray, isDeep) {
  var buffer = isDeep ? cloneArrayBuffer(typedArray.buffer) : typedArray.buffer;
  return new typedArray.constructor(buffer, typedArray.byteOffset, typedArray.length);
}

module.exports = cloneTypedArray;


/***/ }),

/***/ "./node_modules/lodash/_copyArray.js":
/*!*******************************************!*\
  !*** ./node_modules/lodash/_copyArray.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * Copies the values of `source` to `array`.
 *
 * @private
 * @param {Array} source The array to copy values from.
 * @param {Array} [array=[]] The array to copy values to.
 * @returns {Array} Returns `array`.
 */
function copyArray(source, array) {
  var index = -1,
      length = source.length;

  array || (array = Array(length));
  while (++index < length) {
    array[index] = source[index];
  }
  return array;
}

module.exports = copyArray;


/***/ }),

/***/ "./node_modules/lodash/_copyObject.js":
/*!********************************************!*\
  !*** ./node_modules/lodash/_copyObject.js ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var assignValue = __webpack_require__(/*! ./_assignValue */ "./node_modules/lodash/_assignValue.js"),
    baseAssignValue = __webpack_require__(/*! ./_baseAssignValue */ "./node_modules/lodash/_baseAssignValue.js");

/**
 * Copies properties of `source` to `object`.
 *
 * @private
 * @param {Object} source The object to copy properties from.
 * @param {Array} props The property identifiers to copy.
 * @param {Object} [object={}] The object to copy properties to.
 * @param {Function} [customizer] The function to customize copied values.
 * @returns {Object} Returns `object`.
 */
function copyObject(source, props, object, customizer) {
  var isNew = !object;
  object || (object = {});

  var index = -1,
      length = props.length;

  while (++index < length) {
    var key = props[index];

    var newValue = customizer
      ? customizer(object[key], source[key], key, object, source)
      : undefined;

    if (newValue === undefined) {
      newValue = source[key];
    }
    if (isNew) {
      baseAssignValue(object, key, newValue);
    } else {
      assignValue(object, key, newValue);
    }
  }
  return object;
}

module.exports = copyObject;


/***/ }),

/***/ "./node_modules/lodash/_copySymbols.js":
/*!*********************************************!*\
  !*** ./node_modules/lodash/_copySymbols.js ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var copyObject = __webpack_require__(/*! ./_copyObject */ "./node_modules/lodash/_copyObject.js"),
    getSymbols = __webpack_require__(/*! ./_getSymbols */ "./node_modules/lodash/_getSymbols.js");

/**
 * Copies own symbols of `source` to `object`.
 *
 * @private
 * @param {Object} source The object to copy symbols from.
 * @param {Object} [object={}] The object to copy symbols to.
 * @returns {Object} Returns `object`.
 */
function copySymbols(source, object) {
  return copyObject(source, getSymbols(source), object);
}

module.exports = copySymbols;


/***/ }),

/***/ "./node_modules/lodash/_copySymbolsIn.js":
/*!***********************************************!*\
  !*** ./node_modules/lodash/_copySymbolsIn.js ***!
  \***********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var copyObject = __webpack_require__(/*! ./_copyObject */ "./node_modules/lodash/_copyObject.js"),
    getSymbolsIn = __webpack_require__(/*! ./_getSymbolsIn */ "./node_modules/lodash/_getSymbolsIn.js");

/**
 * Copies own and inherited symbols of `source` to `object`.
 *
 * @private
 * @param {Object} source The object to copy symbols from.
 * @param {Object} [object={}] The object to copy symbols to.
 * @returns {Object} Returns `object`.
 */
function copySymbolsIn(source, object) {
  return copyObject(source, getSymbolsIn(source), object);
}

module.exports = copySymbolsIn;


/***/ }),

/***/ "./node_modules/lodash/_coreJsData.js":
/*!********************************************!*\
  !*** ./node_modules/lodash/_coreJsData.js ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var root = __webpack_require__(/*! ./_root */ "./node_modules/lodash/_root.js");

/** Used to detect overreaching core-js shims. */
var coreJsData = root['__core-js_shared__'];

module.exports = coreJsData;


/***/ }),

/***/ "./node_modules/lodash/_defineProperty.js":
/*!************************************************!*\
  !*** ./node_modules/lodash/_defineProperty.js ***!
  \************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var getNative = __webpack_require__(/*! ./_getNative */ "./node_modules/lodash/_getNative.js");

var defineProperty = (function() {
  try {
    var func = getNative(Object, 'defineProperty');
    func({}, '', {});
    return func;
  } catch (e) {}
}());

module.exports = defineProperty;


/***/ }),

/***/ "./node_modules/lodash/_freeGlobal.js":
/*!********************************************!*\
  !*** ./node_modules/lodash/_freeGlobal.js ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(global) {/** Detect free variable `global` from Node.js. */
var freeGlobal = typeof global == 'object' && global && global.Object === Object && global;

module.exports = freeGlobal;

/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! ./../webpack/buildin/global.js */ "./node_modules/webpack/buildin/global.js")))

/***/ }),

/***/ "./node_modules/lodash/_getAllKeys.js":
/*!********************************************!*\
  !*** ./node_modules/lodash/_getAllKeys.js ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var baseGetAllKeys = __webpack_require__(/*! ./_baseGetAllKeys */ "./node_modules/lodash/_baseGetAllKeys.js"),
    getSymbols = __webpack_require__(/*! ./_getSymbols */ "./node_modules/lodash/_getSymbols.js"),
    keys = __webpack_require__(/*! ./keys */ "./node_modules/lodash/keys.js");

/**
 * Creates an array of own enumerable property names and symbols of `object`.
 *
 * @private
 * @param {Object} object The object to query.
 * @returns {Array} Returns the array of property names and symbols.
 */
function getAllKeys(object) {
  return baseGetAllKeys(object, keys, getSymbols);
}

module.exports = getAllKeys;


/***/ }),

/***/ "./node_modules/lodash/_getAllKeysIn.js":
/*!**********************************************!*\
  !*** ./node_modules/lodash/_getAllKeysIn.js ***!
  \**********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var baseGetAllKeys = __webpack_require__(/*! ./_baseGetAllKeys */ "./node_modules/lodash/_baseGetAllKeys.js"),
    getSymbolsIn = __webpack_require__(/*! ./_getSymbolsIn */ "./node_modules/lodash/_getSymbolsIn.js"),
    keysIn = __webpack_require__(/*! ./keysIn */ "./node_modules/lodash/keysIn.js");

/**
 * Creates an array of own and inherited enumerable property names and
 * symbols of `object`.
 *
 * @private
 * @param {Object} object The object to query.
 * @returns {Array} Returns the array of property names and symbols.
 */
function getAllKeysIn(object) {
  return baseGetAllKeys(object, keysIn, getSymbolsIn);
}

module.exports = getAllKeysIn;


/***/ }),

/***/ "./node_modules/lodash/_getMapData.js":
/*!********************************************!*\
  !*** ./node_modules/lodash/_getMapData.js ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var isKeyable = __webpack_require__(/*! ./_isKeyable */ "./node_modules/lodash/_isKeyable.js");

/**
 * Gets the data for `map`.
 *
 * @private
 * @param {Object} map The map to query.
 * @param {string} key The reference key.
 * @returns {*} Returns the map data.
 */
function getMapData(map, key) {
  var data = map.__data__;
  return isKeyable(key)
    ? data[typeof key == 'string' ? 'string' : 'hash']
    : data.map;
}

module.exports = getMapData;


/***/ }),

/***/ "./node_modules/lodash/_getNative.js":
/*!*******************************************!*\
  !*** ./node_modules/lodash/_getNative.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var baseIsNative = __webpack_require__(/*! ./_baseIsNative */ "./node_modules/lodash/_baseIsNative.js"),
    getValue = __webpack_require__(/*! ./_getValue */ "./node_modules/lodash/_getValue.js");

/**
 * Gets the native function at `key` of `object`.
 *
 * @private
 * @param {Object} object The object to query.
 * @param {string} key The key of the method to get.
 * @returns {*} Returns the function if it's native, else `undefined`.
 */
function getNative(object, key) {
  var value = getValue(object, key);
  return baseIsNative(value) ? value : undefined;
}

module.exports = getNative;


/***/ }),

/***/ "./node_modules/lodash/_getPrototype.js":
/*!**********************************************!*\
  !*** ./node_modules/lodash/_getPrototype.js ***!
  \**********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var overArg = __webpack_require__(/*! ./_overArg */ "./node_modules/lodash/_overArg.js");

/** Built-in value references. */
var getPrototype = overArg(Object.getPrototypeOf, Object);

module.exports = getPrototype;


/***/ }),

/***/ "./node_modules/lodash/_getRawTag.js":
/*!*******************************************!*\
  !*** ./node_modules/lodash/_getRawTag.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var Symbol = __webpack_require__(/*! ./_Symbol */ "./node_modules/lodash/_Symbol.js");

/** Used for built-in method references. */
var objectProto = Object.prototype;

/** Used to check objects for own properties. */
var hasOwnProperty = objectProto.hasOwnProperty;

/**
 * Used to resolve the
 * [`toStringTag`](http://ecma-international.org/ecma-262/7.0/#sec-object.prototype.tostring)
 * of values.
 */
var nativeObjectToString = objectProto.toString;

/** Built-in value references. */
var symToStringTag = Symbol ? Symbol.toStringTag : undefined;

/**
 * A specialized version of `baseGetTag` which ignores `Symbol.toStringTag` values.
 *
 * @private
 * @param {*} value The value to query.
 * @returns {string} Returns the raw `toStringTag`.
 */
function getRawTag(value) {
  var isOwn = hasOwnProperty.call(value, symToStringTag),
      tag = value[symToStringTag];

  try {
    value[symToStringTag] = undefined;
    var unmasked = true;
  } catch (e) {}

  var result = nativeObjectToString.call(value);
  if (unmasked) {
    if (isOwn) {
      value[symToStringTag] = tag;
    } else {
      delete value[symToStringTag];
    }
  }
  return result;
}

module.exports = getRawTag;


/***/ }),

/***/ "./node_modules/lodash/_getSymbols.js":
/*!********************************************!*\
  !*** ./node_modules/lodash/_getSymbols.js ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var arrayFilter = __webpack_require__(/*! ./_arrayFilter */ "./node_modules/lodash/_arrayFilter.js"),
    stubArray = __webpack_require__(/*! ./stubArray */ "./node_modules/lodash/stubArray.js");

/** Used for built-in method references. */
var objectProto = Object.prototype;

/** Built-in value references. */
var propertyIsEnumerable = objectProto.propertyIsEnumerable;

/* Built-in method references for those with the same name as other `lodash` methods. */
var nativeGetSymbols = Object.getOwnPropertySymbols;

/**
 * Creates an array of the own enumerable symbols of `object`.
 *
 * @private
 * @param {Object} object The object to query.
 * @returns {Array} Returns the array of symbols.
 */
var getSymbols = !nativeGetSymbols ? stubArray : function(object) {
  if (object == null) {
    return [];
  }
  object = Object(object);
  return arrayFilter(nativeGetSymbols(object), function(symbol) {
    return propertyIsEnumerable.call(object, symbol);
  });
};

module.exports = getSymbols;


/***/ }),

/***/ "./node_modules/lodash/_getSymbolsIn.js":
/*!**********************************************!*\
  !*** ./node_modules/lodash/_getSymbolsIn.js ***!
  \**********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var arrayPush = __webpack_require__(/*! ./_arrayPush */ "./node_modules/lodash/_arrayPush.js"),
    getPrototype = __webpack_require__(/*! ./_getPrototype */ "./node_modules/lodash/_getPrototype.js"),
    getSymbols = __webpack_require__(/*! ./_getSymbols */ "./node_modules/lodash/_getSymbols.js"),
    stubArray = __webpack_require__(/*! ./stubArray */ "./node_modules/lodash/stubArray.js");

/* Built-in method references for those with the same name as other `lodash` methods. */
var nativeGetSymbols = Object.getOwnPropertySymbols;

/**
 * Creates an array of the own and inherited enumerable symbols of `object`.
 *
 * @private
 * @param {Object} object The object to query.
 * @returns {Array} Returns the array of symbols.
 */
var getSymbolsIn = !nativeGetSymbols ? stubArray : function(object) {
  var result = [];
  while (object) {
    arrayPush(result, getSymbols(object));
    object = getPrototype(object);
  }
  return result;
};

module.exports = getSymbolsIn;


/***/ }),

/***/ "./node_modules/lodash/_getTag.js":
/*!****************************************!*\
  !*** ./node_modules/lodash/_getTag.js ***!
  \****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var DataView = __webpack_require__(/*! ./_DataView */ "./node_modules/lodash/_DataView.js"),
    Map = __webpack_require__(/*! ./_Map */ "./node_modules/lodash/_Map.js"),
    Promise = __webpack_require__(/*! ./_Promise */ "./node_modules/lodash/_Promise.js"),
    Set = __webpack_require__(/*! ./_Set */ "./node_modules/lodash/_Set.js"),
    WeakMap = __webpack_require__(/*! ./_WeakMap */ "./node_modules/lodash/_WeakMap.js"),
    baseGetTag = __webpack_require__(/*! ./_baseGetTag */ "./node_modules/lodash/_baseGetTag.js"),
    toSource = __webpack_require__(/*! ./_toSource */ "./node_modules/lodash/_toSource.js");

/** `Object#toString` result references. */
var mapTag = '[object Map]',
    objectTag = '[object Object]',
    promiseTag = '[object Promise]',
    setTag = '[object Set]',
    weakMapTag = '[object WeakMap]';

var dataViewTag = '[object DataView]';

/** Used to detect maps, sets, and weakmaps. */
var dataViewCtorString = toSource(DataView),
    mapCtorString = toSource(Map),
    promiseCtorString = toSource(Promise),
    setCtorString = toSource(Set),
    weakMapCtorString = toSource(WeakMap);

/**
 * Gets the `toStringTag` of `value`.
 *
 * @private
 * @param {*} value The value to query.
 * @returns {string} Returns the `toStringTag`.
 */
var getTag = baseGetTag;

// Fallback for data views, maps, sets, and weak maps in IE 11 and promises in Node.js < 6.
if ((DataView && getTag(new DataView(new ArrayBuffer(1))) != dataViewTag) ||
    (Map && getTag(new Map) != mapTag) ||
    (Promise && getTag(Promise.resolve()) != promiseTag) ||
    (Set && getTag(new Set) != setTag) ||
    (WeakMap && getTag(new WeakMap) != weakMapTag)) {
  getTag = function(value) {
    var result = baseGetTag(value),
        Ctor = result == objectTag ? value.constructor : undefined,
        ctorString = Ctor ? toSource(Ctor) : '';

    if (ctorString) {
      switch (ctorString) {
        case dataViewCtorString: return dataViewTag;
        case mapCtorString: return mapTag;
        case promiseCtorString: return promiseTag;
        case setCtorString: return setTag;
        case weakMapCtorString: return weakMapTag;
      }
    }
    return result;
  };
}

module.exports = getTag;


/***/ }),

/***/ "./node_modules/lodash/_getValue.js":
/*!******************************************!*\
  !*** ./node_modules/lodash/_getValue.js ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * Gets the value at `key` of `object`.
 *
 * @private
 * @param {Object} [object] The object to query.
 * @param {string} key The key of the property to get.
 * @returns {*} Returns the property value.
 */
function getValue(object, key) {
  return object == null ? undefined : object[key];
}

module.exports = getValue;


/***/ }),

/***/ "./node_modules/lodash/_hashClear.js":
/*!*******************************************!*\
  !*** ./node_modules/lodash/_hashClear.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var nativeCreate = __webpack_require__(/*! ./_nativeCreate */ "./node_modules/lodash/_nativeCreate.js");

/**
 * Removes all key-value entries from the hash.
 *
 * @private
 * @name clear
 * @memberOf Hash
 */
function hashClear() {
  this.__data__ = nativeCreate ? nativeCreate(null) : {};
  this.size = 0;
}

module.exports = hashClear;


/***/ }),

/***/ "./node_modules/lodash/_hashDelete.js":
/*!********************************************!*\
  !*** ./node_modules/lodash/_hashDelete.js ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * Removes `key` and its value from the hash.
 *
 * @private
 * @name delete
 * @memberOf Hash
 * @param {Object} hash The hash to modify.
 * @param {string} key The key of the value to remove.
 * @returns {boolean} Returns `true` if the entry was removed, else `false`.
 */
function hashDelete(key) {
  var result = this.has(key) && delete this.__data__[key];
  this.size -= result ? 1 : 0;
  return result;
}

module.exports = hashDelete;


/***/ }),

/***/ "./node_modules/lodash/_hashGet.js":
/*!*****************************************!*\
  !*** ./node_modules/lodash/_hashGet.js ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var nativeCreate = __webpack_require__(/*! ./_nativeCreate */ "./node_modules/lodash/_nativeCreate.js");

/** Used to stand-in for `undefined` hash values. */
var HASH_UNDEFINED = '__lodash_hash_undefined__';

/** Used for built-in method references. */
var objectProto = Object.prototype;

/** Used to check objects for own properties. */
var hasOwnProperty = objectProto.hasOwnProperty;

/**
 * Gets the hash value for `key`.
 *
 * @private
 * @name get
 * @memberOf Hash
 * @param {string} key The key of the value to get.
 * @returns {*} Returns the entry value.
 */
function hashGet(key) {
  var data = this.__data__;
  if (nativeCreate) {
    var result = data[key];
    return result === HASH_UNDEFINED ? undefined : result;
  }
  return hasOwnProperty.call(data, key) ? data[key] : undefined;
}

module.exports = hashGet;


/***/ }),

/***/ "./node_modules/lodash/_hashHas.js":
/*!*****************************************!*\
  !*** ./node_modules/lodash/_hashHas.js ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var nativeCreate = __webpack_require__(/*! ./_nativeCreate */ "./node_modules/lodash/_nativeCreate.js");

/** Used for built-in method references. */
var objectProto = Object.prototype;

/** Used to check objects for own properties. */
var hasOwnProperty = objectProto.hasOwnProperty;

/**
 * Checks if a hash value for `key` exists.
 *
 * @private
 * @name has
 * @memberOf Hash
 * @param {string} key The key of the entry to check.
 * @returns {boolean} Returns `true` if an entry for `key` exists, else `false`.
 */
function hashHas(key) {
  var data = this.__data__;
  return nativeCreate ? (data[key] !== undefined) : hasOwnProperty.call(data, key);
}

module.exports = hashHas;


/***/ }),

/***/ "./node_modules/lodash/_hashSet.js":
/*!*****************************************!*\
  !*** ./node_modules/lodash/_hashSet.js ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var nativeCreate = __webpack_require__(/*! ./_nativeCreate */ "./node_modules/lodash/_nativeCreate.js");

/** Used to stand-in for `undefined` hash values. */
var HASH_UNDEFINED = '__lodash_hash_undefined__';

/**
 * Sets the hash `key` to `value`.
 *
 * @private
 * @name set
 * @memberOf Hash
 * @param {string} key The key of the value to set.
 * @param {*} value The value to set.
 * @returns {Object} Returns the hash instance.
 */
function hashSet(key, value) {
  var data = this.__data__;
  this.size += this.has(key) ? 0 : 1;
  data[key] = (nativeCreate && value === undefined) ? HASH_UNDEFINED : value;
  return this;
}

module.exports = hashSet;


/***/ }),

/***/ "./node_modules/lodash/_initCloneArray.js":
/*!************************************************!*\
  !*** ./node_modules/lodash/_initCloneArray.js ***!
  \************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/** Used for built-in method references. */
var objectProto = Object.prototype;

/** Used to check objects for own properties. */
var hasOwnProperty = objectProto.hasOwnProperty;

/**
 * Initializes an array clone.
 *
 * @private
 * @param {Array} array The array to clone.
 * @returns {Array} Returns the initialized clone.
 */
function initCloneArray(array) {
  var length = array.length,
      result = new array.constructor(length);

  // Add properties assigned by `RegExp#exec`.
  if (length && typeof array[0] == 'string' && hasOwnProperty.call(array, 'index')) {
    result.index = array.index;
    result.input = array.input;
  }
  return result;
}

module.exports = initCloneArray;


/***/ }),

/***/ "./node_modules/lodash/_initCloneByTag.js":
/*!************************************************!*\
  !*** ./node_modules/lodash/_initCloneByTag.js ***!
  \************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var cloneArrayBuffer = __webpack_require__(/*! ./_cloneArrayBuffer */ "./node_modules/lodash/_cloneArrayBuffer.js"),
    cloneDataView = __webpack_require__(/*! ./_cloneDataView */ "./node_modules/lodash/_cloneDataView.js"),
    cloneRegExp = __webpack_require__(/*! ./_cloneRegExp */ "./node_modules/lodash/_cloneRegExp.js"),
    cloneSymbol = __webpack_require__(/*! ./_cloneSymbol */ "./node_modules/lodash/_cloneSymbol.js"),
    cloneTypedArray = __webpack_require__(/*! ./_cloneTypedArray */ "./node_modules/lodash/_cloneTypedArray.js");

/** `Object#toString` result references. */
var boolTag = '[object Boolean]',
    dateTag = '[object Date]',
    mapTag = '[object Map]',
    numberTag = '[object Number]',
    regexpTag = '[object RegExp]',
    setTag = '[object Set]',
    stringTag = '[object String]',
    symbolTag = '[object Symbol]';

var arrayBufferTag = '[object ArrayBuffer]',
    dataViewTag = '[object DataView]',
    float32Tag = '[object Float32Array]',
    float64Tag = '[object Float64Array]',
    int8Tag = '[object Int8Array]',
    int16Tag = '[object Int16Array]',
    int32Tag = '[object Int32Array]',
    uint8Tag = '[object Uint8Array]',
    uint8ClampedTag = '[object Uint8ClampedArray]',
    uint16Tag = '[object Uint16Array]',
    uint32Tag = '[object Uint32Array]';

/**
 * Initializes an object clone based on its `toStringTag`.
 *
 * **Note:** This function only supports cloning values with tags of
 * `Boolean`, `Date`, `Error`, `Map`, `Number`, `RegExp`, `Set`, or `String`.
 *
 * @private
 * @param {Object} object The object to clone.
 * @param {string} tag The `toStringTag` of the object to clone.
 * @param {boolean} [isDeep] Specify a deep clone.
 * @returns {Object} Returns the initialized clone.
 */
function initCloneByTag(object, tag, isDeep) {
  var Ctor = object.constructor;
  switch (tag) {
    case arrayBufferTag:
      return cloneArrayBuffer(object);

    case boolTag:
    case dateTag:
      return new Ctor(+object);

    case dataViewTag:
      return cloneDataView(object, isDeep);

    case float32Tag: case float64Tag:
    case int8Tag: case int16Tag: case int32Tag:
    case uint8Tag: case uint8ClampedTag: case uint16Tag: case uint32Tag:
      return cloneTypedArray(object, isDeep);

    case mapTag:
      return new Ctor;

    case numberTag:
    case stringTag:
      return new Ctor(object);

    case regexpTag:
      return cloneRegExp(object);

    case setTag:
      return new Ctor;

    case symbolTag:
      return cloneSymbol(object);
  }
}

module.exports = initCloneByTag;


/***/ }),

/***/ "./node_modules/lodash/_initCloneObject.js":
/*!*************************************************!*\
  !*** ./node_modules/lodash/_initCloneObject.js ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var baseCreate = __webpack_require__(/*! ./_baseCreate */ "./node_modules/lodash/_baseCreate.js"),
    getPrototype = __webpack_require__(/*! ./_getPrototype */ "./node_modules/lodash/_getPrototype.js"),
    isPrototype = __webpack_require__(/*! ./_isPrototype */ "./node_modules/lodash/_isPrototype.js");

/**
 * Initializes an object clone.
 *
 * @private
 * @param {Object} object The object to clone.
 * @returns {Object} Returns the initialized clone.
 */
function initCloneObject(object) {
  return (typeof object.constructor == 'function' && !isPrototype(object))
    ? baseCreate(getPrototype(object))
    : {};
}

module.exports = initCloneObject;


/***/ }),

/***/ "./node_modules/lodash/_isIndex.js":
/*!*****************************************!*\
  !*** ./node_modules/lodash/_isIndex.js ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/** Used as references for various `Number` constants. */
var MAX_SAFE_INTEGER = 9007199254740991;

/** Used to detect unsigned integer values. */
var reIsUint = /^(?:0|[1-9]\d*)$/;

/**
 * Checks if `value` is a valid array-like index.
 *
 * @private
 * @param {*} value The value to check.
 * @param {number} [length=MAX_SAFE_INTEGER] The upper bounds of a valid index.
 * @returns {boolean} Returns `true` if `value` is a valid index, else `false`.
 */
function isIndex(value, length) {
  var type = typeof value;
  length = length == null ? MAX_SAFE_INTEGER : length;

  return !!length &&
    (type == 'number' ||
      (type != 'symbol' && reIsUint.test(value))) &&
        (value > -1 && value % 1 == 0 && value < length);
}

module.exports = isIndex;


/***/ }),

/***/ "./node_modules/lodash/_isKeyable.js":
/*!*******************************************!*\
  !*** ./node_modules/lodash/_isKeyable.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * Checks if `value` is suitable for use as unique object key.
 *
 * @private
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is suitable, else `false`.
 */
function isKeyable(value) {
  var type = typeof value;
  return (type == 'string' || type == 'number' || type == 'symbol' || type == 'boolean')
    ? (value !== '__proto__')
    : (value === null);
}

module.exports = isKeyable;


/***/ }),

/***/ "./node_modules/lodash/_isMasked.js":
/*!******************************************!*\
  !*** ./node_modules/lodash/_isMasked.js ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var coreJsData = __webpack_require__(/*! ./_coreJsData */ "./node_modules/lodash/_coreJsData.js");

/** Used to detect methods masquerading as native. */
var maskSrcKey = (function() {
  var uid = /[^.]+$/.exec(coreJsData && coreJsData.keys && coreJsData.keys.IE_PROTO || '');
  return uid ? ('Symbol(src)_1.' + uid) : '';
}());

/**
 * Checks if `func` has its source masked.
 *
 * @private
 * @param {Function} func The function to check.
 * @returns {boolean} Returns `true` if `func` is masked, else `false`.
 */
function isMasked(func) {
  return !!maskSrcKey && (maskSrcKey in func);
}

module.exports = isMasked;


/***/ }),

/***/ "./node_modules/lodash/_isPrototype.js":
/*!*********************************************!*\
  !*** ./node_modules/lodash/_isPrototype.js ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/** Used for built-in method references. */
var objectProto = Object.prototype;

/**
 * Checks if `value` is likely a prototype object.
 *
 * @private
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is a prototype, else `false`.
 */
function isPrototype(value) {
  var Ctor = value && value.constructor,
      proto = (typeof Ctor == 'function' && Ctor.prototype) || objectProto;

  return value === proto;
}

module.exports = isPrototype;


/***/ }),

/***/ "./node_modules/lodash/_listCacheClear.js":
/*!************************************************!*\
  !*** ./node_modules/lodash/_listCacheClear.js ***!
  \************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * Removes all key-value entries from the list cache.
 *
 * @private
 * @name clear
 * @memberOf ListCache
 */
function listCacheClear() {
  this.__data__ = [];
  this.size = 0;
}

module.exports = listCacheClear;


/***/ }),

/***/ "./node_modules/lodash/_listCacheDelete.js":
/*!*************************************************!*\
  !*** ./node_modules/lodash/_listCacheDelete.js ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var assocIndexOf = __webpack_require__(/*! ./_assocIndexOf */ "./node_modules/lodash/_assocIndexOf.js");

/** Used for built-in method references. */
var arrayProto = Array.prototype;

/** Built-in value references. */
var splice = arrayProto.splice;

/**
 * Removes `key` and its value from the list cache.
 *
 * @private
 * @name delete
 * @memberOf ListCache
 * @param {string} key The key of the value to remove.
 * @returns {boolean} Returns `true` if the entry was removed, else `false`.
 */
function listCacheDelete(key) {
  var data = this.__data__,
      index = assocIndexOf(data, key);

  if (index < 0) {
    return false;
  }
  var lastIndex = data.length - 1;
  if (index == lastIndex) {
    data.pop();
  } else {
    splice.call(data, index, 1);
  }
  --this.size;
  return true;
}

module.exports = listCacheDelete;


/***/ }),

/***/ "./node_modules/lodash/_listCacheGet.js":
/*!**********************************************!*\
  !*** ./node_modules/lodash/_listCacheGet.js ***!
  \**********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var assocIndexOf = __webpack_require__(/*! ./_assocIndexOf */ "./node_modules/lodash/_assocIndexOf.js");

/**
 * Gets the list cache value for `key`.
 *
 * @private
 * @name get
 * @memberOf ListCache
 * @param {string} key The key of the value to get.
 * @returns {*} Returns the entry value.
 */
function listCacheGet(key) {
  var data = this.__data__,
      index = assocIndexOf(data, key);

  return index < 0 ? undefined : data[index][1];
}

module.exports = listCacheGet;


/***/ }),

/***/ "./node_modules/lodash/_listCacheHas.js":
/*!**********************************************!*\
  !*** ./node_modules/lodash/_listCacheHas.js ***!
  \**********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var assocIndexOf = __webpack_require__(/*! ./_assocIndexOf */ "./node_modules/lodash/_assocIndexOf.js");

/**
 * Checks if a list cache value for `key` exists.
 *
 * @private
 * @name has
 * @memberOf ListCache
 * @param {string} key The key of the entry to check.
 * @returns {boolean} Returns `true` if an entry for `key` exists, else `false`.
 */
function listCacheHas(key) {
  return assocIndexOf(this.__data__, key) > -1;
}

module.exports = listCacheHas;


/***/ }),

/***/ "./node_modules/lodash/_listCacheSet.js":
/*!**********************************************!*\
  !*** ./node_modules/lodash/_listCacheSet.js ***!
  \**********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var assocIndexOf = __webpack_require__(/*! ./_assocIndexOf */ "./node_modules/lodash/_assocIndexOf.js");

/**
 * Sets the list cache `key` to `value`.
 *
 * @private
 * @name set
 * @memberOf ListCache
 * @param {string} key The key of the value to set.
 * @param {*} value The value to set.
 * @returns {Object} Returns the list cache instance.
 */
function listCacheSet(key, value) {
  var data = this.__data__,
      index = assocIndexOf(data, key);

  if (index < 0) {
    ++this.size;
    data.push([key, value]);
  } else {
    data[index][1] = value;
  }
  return this;
}

module.exports = listCacheSet;


/***/ }),

/***/ "./node_modules/lodash/_mapCacheClear.js":
/*!***********************************************!*\
  !*** ./node_modules/lodash/_mapCacheClear.js ***!
  \***********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var Hash = __webpack_require__(/*! ./_Hash */ "./node_modules/lodash/_Hash.js"),
    ListCache = __webpack_require__(/*! ./_ListCache */ "./node_modules/lodash/_ListCache.js"),
    Map = __webpack_require__(/*! ./_Map */ "./node_modules/lodash/_Map.js");

/**
 * Removes all key-value entries from the map.
 *
 * @private
 * @name clear
 * @memberOf MapCache
 */
function mapCacheClear() {
  this.size = 0;
  this.__data__ = {
    'hash': new Hash,
    'map': new (Map || ListCache),
    'string': new Hash
  };
}

module.exports = mapCacheClear;


/***/ }),

/***/ "./node_modules/lodash/_mapCacheDelete.js":
/*!************************************************!*\
  !*** ./node_modules/lodash/_mapCacheDelete.js ***!
  \************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var getMapData = __webpack_require__(/*! ./_getMapData */ "./node_modules/lodash/_getMapData.js");

/**
 * Removes `key` and its value from the map.
 *
 * @private
 * @name delete
 * @memberOf MapCache
 * @param {string} key The key of the value to remove.
 * @returns {boolean} Returns `true` if the entry was removed, else `false`.
 */
function mapCacheDelete(key) {
  var result = getMapData(this, key)['delete'](key);
  this.size -= result ? 1 : 0;
  return result;
}

module.exports = mapCacheDelete;


/***/ }),

/***/ "./node_modules/lodash/_mapCacheGet.js":
/*!*********************************************!*\
  !*** ./node_modules/lodash/_mapCacheGet.js ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var getMapData = __webpack_require__(/*! ./_getMapData */ "./node_modules/lodash/_getMapData.js");

/**
 * Gets the map value for `key`.
 *
 * @private
 * @name get
 * @memberOf MapCache
 * @param {string} key The key of the value to get.
 * @returns {*} Returns the entry value.
 */
function mapCacheGet(key) {
  return getMapData(this, key).get(key);
}

module.exports = mapCacheGet;


/***/ }),

/***/ "./node_modules/lodash/_mapCacheHas.js":
/*!*********************************************!*\
  !*** ./node_modules/lodash/_mapCacheHas.js ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var getMapData = __webpack_require__(/*! ./_getMapData */ "./node_modules/lodash/_getMapData.js");

/**
 * Checks if a map value for `key` exists.
 *
 * @private
 * @name has
 * @memberOf MapCache
 * @param {string} key The key of the entry to check.
 * @returns {boolean} Returns `true` if an entry for `key` exists, else `false`.
 */
function mapCacheHas(key) {
  return getMapData(this, key).has(key);
}

module.exports = mapCacheHas;


/***/ }),

/***/ "./node_modules/lodash/_mapCacheSet.js":
/*!*********************************************!*\
  !*** ./node_modules/lodash/_mapCacheSet.js ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var getMapData = __webpack_require__(/*! ./_getMapData */ "./node_modules/lodash/_getMapData.js");

/**
 * Sets the map `key` to `value`.
 *
 * @private
 * @name set
 * @memberOf MapCache
 * @param {string} key The key of the value to set.
 * @param {*} value The value to set.
 * @returns {Object} Returns the map cache instance.
 */
function mapCacheSet(key, value) {
  var data = getMapData(this, key),
      size = data.size;

  data.set(key, value);
  this.size += data.size == size ? 0 : 1;
  return this;
}

module.exports = mapCacheSet;


/***/ }),

/***/ "./node_modules/lodash/_nativeCreate.js":
/*!**********************************************!*\
  !*** ./node_modules/lodash/_nativeCreate.js ***!
  \**********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var getNative = __webpack_require__(/*! ./_getNative */ "./node_modules/lodash/_getNative.js");

/* Built-in method references that are verified to be native. */
var nativeCreate = getNative(Object, 'create');

module.exports = nativeCreate;


/***/ }),

/***/ "./node_modules/lodash/_nativeKeys.js":
/*!********************************************!*\
  !*** ./node_modules/lodash/_nativeKeys.js ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var overArg = __webpack_require__(/*! ./_overArg */ "./node_modules/lodash/_overArg.js");

/* Built-in method references for those with the same name as other `lodash` methods. */
var nativeKeys = overArg(Object.keys, Object);

module.exports = nativeKeys;


/***/ }),

/***/ "./node_modules/lodash/_nativeKeysIn.js":
/*!**********************************************!*\
  !*** ./node_modules/lodash/_nativeKeysIn.js ***!
  \**********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * This function is like
 * [`Object.keys`](http://ecma-international.org/ecma-262/7.0/#sec-object.keys)
 * except that it includes inherited enumerable properties.
 *
 * @private
 * @param {Object} object The object to query.
 * @returns {Array} Returns the array of property names.
 */
function nativeKeysIn(object) {
  var result = [];
  if (object != null) {
    for (var key in Object(object)) {
      result.push(key);
    }
  }
  return result;
}

module.exports = nativeKeysIn;


/***/ }),

/***/ "./node_modules/lodash/_nodeUtil.js":
/*!******************************************!*\
  !*** ./node_modules/lodash/_nodeUtil.js ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(module) {var freeGlobal = __webpack_require__(/*! ./_freeGlobal */ "./node_modules/lodash/_freeGlobal.js");

/** Detect free variable `exports`. */
var freeExports =  true && exports && !exports.nodeType && exports;

/** Detect free variable `module`. */
var freeModule = freeExports && typeof module == 'object' && module && !module.nodeType && module;

/** Detect the popular CommonJS extension `module.exports`. */
var moduleExports = freeModule && freeModule.exports === freeExports;

/** Detect free variable `process` from Node.js. */
var freeProcess = moduleExports && freeGlobal.process;

/** Used to access faster Node.js helpers. */
var nodeUtil = (function() {
  try {
    // Use `util.types` for Node.js 10+.
    var types = freeModule && freeModule.require && freeModule.require('util').types;

    if (types) {
      return types;
    }

    // Legacy `process.binding('util')` for Node.js < 10.
    return freeProcess && freeProcess.binding && freeProcess.binding('util');
  } catch (e) {}
}());

module.exports = nodeUtil;

/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! ./../webpack/buildin/module.js */ "./node_modules/webpack/buildin/module.js")(module)))

/***/ }),

/***/ "./node_modules/lodash/_objectToString.js":
/*!************************************************!*\
  !*** ./node_modules/lodash/_objectToString.js ***!
  \************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/** Used for built-in method references. */
var objectProto = Object.prototype;

/**
 * Used to resolve the
 * [`toStringTag`](http://ecma-international.org/ecma-262/7.0/#sec-object.prototype.tostring)
 * of values.
 */
var nativeObjectToString = objectProto.toString;

/**
 * Converts `value` to a string using `Object.prototype.toString`.
 *
 * @private
 * @param {*} value The value to convert.
 * @returns {string} Returns the converted string.
 */
function objectToString(value) {
  return nativeObjectToString.call(value);
}

module.exports = objectToString;


/***/ }),

/***/ "./node_modules/lodash/_overArg.js":
/*!*****************************************!*\
  !*** ./node_modules/lodash/_overArg.js ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * Creates a unary function that invokes `func` with its argument transformed.
 *
 * @private
 * @param {Function} func The function to wrap.
 * @param {Function} transform The argument transform.
 * @returns {Function} Returns the new function.
 */
function overArg(func, transform) {
  return function(arg) {
    return func(transform(arg));
  };
}

module.exports = overArg;


/***/ }),

/***/ "./node_modules/lodash/_root.js":
/*!**************************************!*\
  !*** ./node_modules/lodash/_root.js ***!
  \**************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var freeGlobal = __webpack_require__(/*! ./_freeGlobal */ "./node_modules/lodash/_freeGlobal.js");

/** Detect free variable `self`. */
var freeSelf = typeof self == 'object' && self && self.Object === Object && self;

/** Used as a reference to the global object. */
var root = freeGlobal || freeSelf || Function('return this')();

module.exports = root;


/***/ }),

/***/ "./node_modules/lodash/_stackClear.js":
/*!********************************************!*\
  !*** ./node_modules/lodash/_stackClear.js ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var ListCache = __webpack_require__(/*! ./_ListCache */ "./node_modules/lodash/_ListCache.js");

/**
 * Removes all key-value entries from the stack.
 *
 * @private
 * @name clear
 * @memberOf Stack
 */
function stackClear() {
  this.__data__ = new ListCache;
  this.size = 0;
}

module.exports = stackClear;


/***/ }),

/***/ "./node_modules/lodash/_stackDelete.js":
/*!*********************************************!*\
  !*** ./node_modules/lodash/_stackDelete.js ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * Removes `key` and its value from the stack.
 *
 * @private
 * @name delete
 * @memberOf Stack
 * @param {string} key The key of the value to remove.
 * @returns {boolean} Returns `true` if the entry was removed, else `false`.
 */
function stackDelete(key) {
  var data = this.__data__,
      result = data['delete'](key);

  this.size = data.size;
  return result;
}

module.exports = stackDelete;


/***/ }),

/***/ "./node_modules/lodash/_stackGet.js":
/*!******************************************!*\
  !*** ./node_modules/lodash/_stackGet.js ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * Gets the stack value for `key`.
 *
 * @private
 * @name get
 * @memberOf Stack
 * @param {string} key The key of the value to get.
 * @returns {*} Returns the entry value.
 */
function stackGet(key) {
  return this.__data__.get(key);
}

module.exports = stackGet;


/***/ }),

/***/ "./node_modules/lodash/_stackHas.js":
/*!******************************************!*\
  !*** ./node_modules/lodash/_stackHas.js ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * Checks if a stack value for `key` exists.
 *
 * @private
 * @name has
 * @memberOf Stack
 * @param {string} key The key of the entry to check.
 * @returns {boolean} Returns `true` if an entry for `key` exists, else `false`.
 */
function stackHas(key) {
  return this.__data__.has(key);
}

module.exports = stackHas;


/***/ }),

/***/ "./node_modules/lodash/_stackSet.js":
/*!******************************************!*\
  !*** ./node_modules/lodash/_stackSet.js ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var ListCache = __webpack_require__(/*! ./_ListCache */ "./node_modules/lodash/_ListCache.js"),
    Map = __webpack_require__(/*! ./_Map */ "./node_modules/lodash/_Map.js"),
    MapCache = __webpack_require__(/*! ./_MapCache */ "./node_modules/lodash/_MapCache.js");

/** Used as the size to enable large array optimizations. */
var LARGE_ARRAY_SIZE = 200;

/**
 * Sets the stack `key` to `value`.
 *
 * @private
 * @name set
 * @memberOf Stack
 * @param {string} key The key of the value to set.
 * @param {*} value The value to set.
 * @returns {Object} Returns the stack cache instance.
 */
function stackSet(key, value) {
  var data = this.__data__;
  if (data instanceof ListCache) {
    var pairs = data.__data__;
    if (!Map || (pairs.length < LARGE_ARRAY_SIZE - 1)) {
      pairs.push([key, value]);
      this.size = ++data.size;
      return this;
    }
    data = this.__data__ = new MapCache(pairs);
  }
  data.set(key, value);
  this.size = data.size;
  return this;
}

module.exports = stackSet;


/***/ }),

/***/ "./node_modules/lodash/_toSource.js":
/*!******************************************!*\
  !*** ./node_modules/lodash/_toSource.js ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/** Used for built-in method references. */
var funcProto = Function.prototype;

/** Used to resolve the decompiled source of functions. */
var funcToString = funcProto.toString;

/**
 * Converts `func` to its source code.
 *
 * @private
 * @param {Function} func The function to convert.
 * @returns {string} Returns the source code.
 */
function toSource(func) {
  if (func != null) {
    try {
      return funcToString.call(func);
    } catch (e) {}
    try {
      return (func + '');
    } catch (e) {}
  }
  return '';
}

module.exports = toSource;


/***/ }),

/***/ "./node_modules/lodash/clone.js":
/*!**************************************!*\
  !*** ./node_modules/lodash/clone.js ***!
  \**************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var baseClone = __webpack_require__(/*! ./_baseClone */ "./node_modules/lodash/_baseClone.js");

/** Used to compose bitmasks for cloning. */
var CLONE_SYMBOLS_FLAG = 4;

/**
 * Creates a shallow clone of `value`.
 *
 * **Note:** This method is loosely based on the
 * [structured clone algorithm](https://mdn.io/Structured_clone_algorithm)
 * and supports cloning arrays, array buffers, booleans, date objects, maps,
 * numbers, `Object` objects, regexes, sets, strings, symbols, and typed
 * arrays. The own enumerable properties of `arguments` objects are cloned
 * as plain objects. An empty object is returned for uncloneable values such
 * as error objects, functions, DOM nodes, and WeakMaps.
 *
 * @static
 * @memberOf _
 * @since 0.1.0
 * @category Lang
 * @param {*} value The value to clone.
 * @returns {*} Returns the cloned value.
 * @see _.cloneDeep
 * @example
 *
 * var objects = [{ 'a': 1 }, { 'b': 2 }];
 *
 * var shallow = _.clone(objects);
 * console.log(shallow[0] === objects[0]);
 * // => true
 */
function clone(value) {
  return baseClone(value, CLONE_SYMBOLS_FLAG);
}

module.exports = clone;


/***/ }),

/***/ "./node_modules/lodash/debounce.js":
/*!*****************************************!*\
  !*** ./node_modules/lodash/debounce.js ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var isObject = __webpack_require__(/*! ./isObject */ "./node_modules/lodash/isObject.js"),
    now = __webpack_require__(/*! ./now */ "./node_modules/lodash/now.js"),
    toNumber = __webpack_require__(/*! ./toNumber */ "./node_modules/lodash/toNumber.js");

/** Error message constants. */
var FUNC_ERROR_TEXT = 'Expected a function';

/* Built-in method references for those with the same name as other `lodash` methods. */
var nativeMax = Math.max,
    nativeMin = Math.min;

/**
 * Creates a debounced function that delays invoking `func` until after `wait`
 * milliseconds have elapsed since the last time the debounced function was
 * invoked. The debounced function comes with a `cancel` method to cancel
 * delayed `func` invocations and a `flush` method to immediately invoke them.
 * Provide `options` to indicate whether `func` should be invoked on the
 * leading and/or trailing edge of the `wait` timeout. The `func` is invoked
 * with the last arguments provided to the debounced function. Subsequent
 * calls to the debounced function return the result of the last `func`
 * invocation.
 *
 * **Note:** If `leading` and `trailing` options are `true`, `func` is
 * invoked on the trailing edge of the timeout only if the debounced function
 * is invoked more than once during the `wait` timeout.
 *
 * If `wait` is `0` and `leading` is `false`, `func` invocation is deferred
 * until to the next tick, similar to `setTimeout` with a timeout of `0`.
 *
 * See [David Corbacho's article](https://css-tricks.com/debouncing-throttling-explained-examples/)
 * for details over the differences between `_.debounce` and `_.throttle`.
 *
 * @static
 * @memberOf _
 * @since 0.1.0
 * @category Function
 * @param {Function} func The function to debounce.
 * @param {number} [wait=0] The number of milliseconds to delay.
 * @param {Object} [options={}] The options object.
 * @param {boolean} [options.leading=false]
 *  Specify invoking on the leading edge of the timeout.
 * @param {number} [options.maxWait]
 *  The maximum time `func` is allowed to be delayed before it's invoked.
 * @param {boolean} [options.trailing=true]
 *  Specify invoking on the trailing edge of the timeout.
 * @returns {Function} Returns the new debounced function.
 * @example
 *
 * // Avoid costly calculations while the window size is in flux.
 * jQuery(window).on('resize', _.debounce(calculateLayout, 150));
 *
 * // Invoke `sendMail` when clicked, debouncing subsequent calls.
 * jQuery(element).on('click', _.debounce(sendMail, 300, {
 *   'leading': true,
 *   'trailing': false
 * }));
 *
 * // Ensure `batchLog` is invoked once after 1 second of debounced calls.
 * var debounced = _.debounce(batchLog, 250, { 'maxWait': 1000 });
 * var source = new EventSource('/stream');
 * jQuery(source).on('message', debounced);
 *
 * // Cancel the trailing debounced invocation.
 * jQuery(window).on('popstate', debounced.cancel);
 */
function debounce(func, wait, options) {
  var lastArgs,
      lastThis,
      maxWait,
      result,
      timerId,
      lastCallTime,
      lastInvokeTime = 0,
      leading = false,
      maxing = false,
      trailing = true;

  if (typeof func != 'function') {
    throw new TypeError(FUNC_ERROR_TEXT);
  }
  wait = toNumber(wait) || 0;
  if (isObject(options)) {
    leading = !!options.leading;
    maxing = 'maxWait' in options;
    maxWait = maxing ? nativeMax(toNumber(options.maxWait) || 0, wait) : maxWait;
    trailing = 'trailing' in options ? !!options.trailing : trailing;
  }

  function invokeFunc(time) {
    var args = lastArgs,
        thisArg = lastThis;

    lastArgs = lastThis = undefined;
    lastInvokeTime = time;
    result = func.apply(thisArg, args);
    return result;
  }

  function leadingEdge(time) {
    // Reset any `maxWait` timer.
    lastInvokeTime = time;
    // Start the timer for the trailing edge.
    timerId = setTimeout(timerExpired, wait);
    // Invoke the leading edge.
    return leading ? invokeFunc(time) : result;
  }

  function remainingWait(time) {
    var timeSinceLastCall = time - lastCallTime,
        timeSinceLastInvoke = time - lastInvokeTime,
        timeWaiting = wait - timeSinceLastCall;

    return maxing
      ? nativeMin(timeWaiting, maxWait - timeSinceLastInvoke)
      : timeWaiting;
  }

  function shouldInvoke(time) {
    var timeSinceLastCall = time - lastCallTime,
        timeSinceLastInvoke = time - lastInvokeTime;

    // Either this is the first call, activity has stopped and we're at the
    // trailing edge, the system time has gone backwards and we're treating
    // it as the trailing edge, or we've hit the `maxWait` limit.
    return (lastCallTime === undefined || (timeSinceLastCall >= wait) ||
      (timeSinceLastCall < 0) || (maxing && timeSinceLastInvoke >= maxWait));
  }

  function timerExpired() {
    var time = now();
    if (shouldInvoke(time)) {
      return trailingEdge(time);
    }
    // Restart the timer.
    timerId = setTimeout(timerExpired, remainingWait(time));
  }

  function trailingEdge(time) {
    timerId = undefined;

    // Only invoke if we have `lastArgs` which means `func` has been
    // debounced at least once.
    if (trailing && lastArgs) {
      return invokeFunc(time);
    }
    lastArgs = lastThis = undefined;
    return result;
  }

  function cancel() {
    if (timerId !== undefined) {
      clearTimeout(timerId);
    }
    lastInvokeTime = 0;
    lastArgs = lastCallTime = lastThis = timerId = undefined;
  }

  function flush() {
    return timerId === undefined ? result : trailingEdge(now());
  }

  function debounced() {
    var time = now(),
        isInvoking = shouldInvoke(time);

    lastArgs = arguments;
    lastThis = this;
    lastCallTime = time;

    if (isInvoking) {
      if (timerId === undefined) {
        return leadingEdge(lastCallTime);
      }
      if (maxing) {
        // Handle invocations in a tight loop.
        timerId = setTimeout(timerExpired, wait);
        return invokeFunc(lastCallTime);
      }
    }
    if (timerId === undefined) {
      timerId = setTimeout(timerExpired, wait);
    }
    return result;
  }
  debounced.cancel = cancel;
  debounced.flush = flush;
  return debounced;
}

module.exports = debounce;


/***/ }),

/***/ "./node_modules/lodash/eq.js":
/*!***********************************!*\
  !*** ./node_modules/lodash/eq.js ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * Performs a
 * [`SameValueZero`](http://ecma-international.org/ecma-262/7.0/#sec-samevaluezero)
 * comparison between two values to determine if they are equivalent.
 *
 * @static
 * @memberOf _
 * @since 4.0.0
 * @category Lang
 * @param {*} value The value to compare.
 * @param {*} other The other value to compare.
 * @returns {boolean} Returns `true` if the values are equivalent, else `false`.
 * @example
 *
 * var object = { 'a': 1 };
 * var other = { 'a': 1 };
 *
 * _.eq(object, object);
 * // => true
 *
 * _.eq(object, other);
 * // => false
 *
 * _.eq('a', 'a');
 * // => true
 *
 * _.eq('a', Object('a'));
 * // => false
 *
 * _.eq(NaN, NaN);
 * // => true
 */
function eq(value, other) {
  return value === other || (value !== value && other !== other);
}

module.exports = eq;


/***/ }),

/***/ "./node_modules/lodash/isArguments.js":
/*!********************************************!*\
  !*** ./node_modules/lodash/isArguments.js ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var baseIsArguments = __webpack_require__(/*! ./_baseIsArguments */ "./node_modules/lodash/_baseIsArguments.js"),
    isObjectLike = __webpack_require__(/*! ./isObjectLike */ "./node_modules/lodash/isObjectLike.js");

/** Used for built-in method references. */
var objectProto = Object.prototype;

/** Used to check objects for own properties. */
var hasOwnProperty = objectProto.hasOwnProperty;

/** Built-in value references. */
var propertyIsEnumerable = objectProto.propertyIsEnumerable;

/**
 * Checks if `value` is likely an `arguments` object.
 *
 * @static
 * @memberOf _
 * @since 0.1.0
 * @category Lang
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is an `arguments` object,
 *  else `false`.
 * @example
 *
 * _.isArguments(function() { return arguments; }());
 * // => true
 *
 * _.isArguments([1, 2, 3]);
 * // => false
 */
var isArguments = baseIsArguments(function() { return arguments; }()) ? baseIsArguments : function(value) {
  return isObjectLike(value) && hasOwnProperty.call(value, 'callee') &&
    !propertyIsEnumerable.call(value, 'callee');
};

module.exports = isArguments;


/***/ }),

/***/ "./node_modules/lodash/isArray.js":
/*!****************************************!*\
  !*** ./node_modules/lodash/isArray.js ***!
  \****************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * Checks if `value` is classified as an `Array` object.
 *
 * @static
 * @memberOf _
 * @since 0.1.0
 * @category Lang
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is an array, else `false`.
 * @example
 *
 * _.isArray([1, 2, 3]);
 * // => true
 *
 * _.isArray(document.body.children);
 * // => false
 *
 * _.isArray('abc');
 * // => false
 *
 * _.isArray(_.noop);
 * // => false
 */
var isArray = Array.isArray;

module.exports = isArray;


/***/ }),

/***/ "./node_modules/lodash/isArrayLike.js":
/*!********************************************!*\
  !*** ./node_modules/lodash/isArrayLike.js ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var isFunction = __webpack_require__(/*! ./isFunction */ "./node_modules/lodash/isFunction.js"),
    isLength = __webpack_require__(/*! ./isLength */ "./node_modules/lodash/isLength.js");

/**
 * Checks if `value` is array-like. A value is considered array-like if it's
 * not a function and has a `value.length` that's an integer greater than or
 * equal to `0` and less than or equal to `Number.MAX_SAFE_INTEGER`.
 *
 * @static
 * @memberOf _
 * @since 4.0.0
 * @category Lang
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is array-like, else `false`.
 * @example
 *
 * _.isArrayLike([1, 2, 3]);
 * // => true
 *
 * _.isArrayLike(document.body.children);
 * // => true
 *
 * _.isArrayLike('abc');
 * // => true
 *
 * _.isArrayLike(_.noop);
 * // => false
 */
function isArrayLike(value) {
  return value != null && isLength(value.length) && !isFunction(value);
}

module.exports = isArrayLike;


/***/ }),

/***/ "./node_modules/lodash/isBuffer.js":
/*!*****************************************!*\
  !*** ./node_modules/lodash/isBuffer.js ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(module) {var root = __webpack_require__(/*! ./_root */ "./node_modules/lodash/_root.js"),
    stubFalse = __webpack_require__(/*! ./stubFalse */ "./node_modules/lodash/stubFalse.js");

/** Detect free variable `exports`. */
var freeExports =  true && exports && !exports.nodeType && exports;

/** Detect free variable `module`. */
var freeModule = freeExports && typeof module == 'object' && module && !module.nodeType && module;

/** Detect the popular CommonJS extension `module.exports`. */
var moduleExports = freeModule && freeModule.exports === freeExports;

/** Built-in value references. */
var Buffer = moduleExports ? root.Buffer : undefined;

/* Built-in method references for those with the same name as other `lodash` methods. */
var nativeIsBuffer = Buffer ? Buffer.isBuffer : undefined;

/**
 * Checks if `value` is a buffer.
 *
 * @static
 * @memberOf _
 * @since 4.3.0
 * @category Lang
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is a buffer, else `false`.
 * @example
 *
 * _.isBuffer(new Buffer(2));
 * // => true
 *
 * _.isBuffer(new Uint8Array(2));
 * // => false
 */
var isBuffer = nativeIsBuffer || stubFalse;

module.exports = isBuffer;

/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! ./../webpack/buildin/module.js */ "./node_modules/webpack/buildin/module.js")(module)))

/***/ }),

/***/ "./node_modules/lodash/isFunction.js":
/*!*******************************************!*\
  !*** ./node_modules/lodash/isFunction.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var baseGetTag = __webpack_require__(/*! ./_baseGetTag */ "./node_modules/lodash/_baseGetTag.js"),
    isObject = __webpack_require__(/*! ./isObject */ "./node_modules/lodash/isObject.js");

/** `Object#toString` result references. */
var asyncTag = '[object AsyncFunction]',
    funcTag = '[object Function]',
    genTag = '[object GeneratorFunction]',
    proxyTag = '[object Proxy]';

/**
 * Checks if `value` is classified as a `Function` object.
 *
 * @static
 * @memberOf _
 * @since 0.1.0
 * @category Lang
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is a function, else `false`.
 * @example
 *
 * _.isFunction(_);
 * // => true
 *
 * _.isFunction(/abc/);
 * // => false
 */
function isFunction(value) {
  if (!isObject(value)) {
    return false;
  }
  // The use of `Object#toString` avoids issues with the `typeof` operator
  // in Safari 9 which returns 'object' for typed arrays and other constructors.
  var tag = baseGetTag(value);
  return tag == funcTag || tag == genTag || tag == asyncTag || tag == proxyTag;
}

module.exports = isFunction;


/***/ }),

/***/ "./node_modules/lodash/isLength.js":
/*!*****************************************!*\
  !*** ./node_modules/lodash/isLength.js ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/** Used as references for various `Number` constants. */
var MAX_SAFE_INTEGER = 9007199254740991;

/**
 * Checks if `value` is a valid array-like length.
 *
 * **Note:** This method is loosely based on
 * [`ToLength`](http://ecma-international.org/ecma-262/7.0/#sec-tolength).
 *
 * @static
 * @memberOf _
 * @since 4.0.0
 * @category Lang
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is a valid length, else `false`.
 * @example
 *
 * _.isLength(3);
 * // => true
 *
 * _.isLength(Number.MIN_VALUE);
 * // => false
 *
 * _.isLength(Infinity);
 * // => false
 *
 * _.isLength('3');
 * // => false
 */
function isLength(value) {
  return typeof value == 'number' &&
    value > -1 && value % 1 == 0 && value <= MAX_SAFE_INTEGER;
}

module.exports = isLength;


/***/ }),

/***/ "./node_modules/lodash/isMap.js":
/*!**************************************!*\
  !*** ./node_modules/lodash/isMap.js ***!
  \**************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var baseIsMap = __webpack_require__(/*! ./_baseIsMap */ "./node_modules/lodash/_baseIsMap.js"),
    baseUnary = __webpack_require__(/*! ./_baseUnary */ "./node_modules/lodash/_baseUnary.js"),
    nodeUtil = __webpack_require__(/*! ./_nodeUtil */ "./node_modules/lodash/_nodeUtil.js");

/* Node.js helper references. */
var nodeIsMap = nodeUtil && nodeUtil.isMap;

/**
 * Checks if `value` is classified as a `Map` object.
 *
 * @static
 * @memberOf _
 * @since 4.3.0
 * @category Lang
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is a map, else `false`.
 * @example
 *
 * _.isMap(new Map);
 * // => true
 *
 * _.isMap(new WeakMap);
 * // => false
 */
var isMap = nodeIsMap ? baseUnary(nodeIsMap) : baseIsMap;

module.exports = isMap;


/***/ }),

/***/ "./node_modules/lodash/isObject.js":
/*!*****************************************!*\
  !*** ./node_modules/lodash/isObject.js ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * Checks if `value` is the
 * [language type](http://www.ecma-international.org/ecma-262/7.0/#sec-ecmascript-language-types)
 * of `Object`. (e.g. arrays, functions, objects, regexes, `new Number(0)`, and `new String('')`)
 *
 * @static
 * @memberOf _
 * @since 0.1.0
 * @category Lang
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is an object, else `false`.
 * @example
 *
 * _.isObject({});
 * // => true
 *
 * _.isObject([1, 2, 3]);
 * // => true
 *
 * _.isObject(_.noop);
 * // => true
 *
 * _.isObject(null);
 * // => false
 */
function isObject(value) {
  var type = typeof value;
  return value != null && (type == 'object' || type == 'function');
}

module.exports = isObject;


/***/ }),

/***/ "./node_modules/lodash/isObjectLike.js":
/*!*********************************************!*\
  !*** ./node_modules/lodash/isObjectLike.js ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * Checks if `value` is object-like. A value is object-like if it's not `null`
 * and has a `typeof` result of "object".
 *
 * @static
 * @memberOf _
 * @since 4.0.0
 * @category Lang
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is object-like, else `false`.
 * @example
 *
 * _.isObjectLike({});
 * // => true
 *
 * _.isObjectLike([1, 2, 3]);
 * // => true
 *
 * _.isObjectLike(_.noop);
 * // => false
 *
 * _.isObjectLike(null);
 * // => false
 */
function isObjectLike(value) {
  return value != null && typeof value == 'object';
}

module.exports = isObjectLike;


/***/ }),

/***/ "./node_modules/lodash/isSet.js":
/*!**************************************!*\
  !*** ./node_modules/lodash/isSet.js ***!
  \**************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var baseIsSet = __webpack_require__(/*! ./_baseIsSet */ "./node_modules/lodash/_baseIsSet.js"),
    baseUnary = __webpack_require__(/*! ./_baseUnary */ "./node_modules/lodash/_baseUnary.js"),
    nodeUtil = __webpack_require__(/*! ./_nodeUtil */ "./node_modules/lodash/_nodeUtil.js");

/* Node.js helper references. */
var nodeIsSet = nodeUtil && nodeUtil.isSet;

/**
 * Checks if `value` is classified as a `Set` object.
 *
 * @static
 * @memberOf _
 * @since 4.3.0
 * @category Lang
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is a set, else `false`.
 * @example
 *
 * _.isSet(new Set);
 * // => true
 *
 * _.isSet(new WeakSet);
 * // => false
 */
var isSet = nodeIsSet ? baseUnary(nodeIsSet) : baseIsSet;

module.exports = isSet;


/***/ }),

/***/ "./node_modules/lodash/isSymbol.js":
/*!*****************************************!*\
  !*** ./node_modules/lodash/isSymbol.js ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var baseGetTag = __webpack_require__(/*! ./_baseGetTag */ "./node_modules/lodash/_baseGetTag.js"),
    isObjectLike = __webpack_require__(/*! ./isObjectLike */ "./node_modules/lodash/isObjectLike.js");

/** `Object#toString` result references. */
var symbolTag = '[object Symbol]';

/**
 * Checks if `value` is classified as a `Symbol` primitive or object.
 *
 * @static
 * @memberOf _
 * @since 4.0.0
 * @category Lang
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is a symbol, else `false`.
 * @example
 *
 * _.isSymbol(Symbol.iterator);
 * // => true
 *
 * _.isSymbol('abc');
 * // => false
 */
function isSymbol(value) {
  return typeof value == 'symbol' ||
    (isObjectLike(value) && baseGetTag(value) == symbolTag);
}

module.exports = isSymbol;


/***/ }),

/***/ "./node_modules/lodash/isTypedArray.js":
/*!*********************************************!*\
  !*** ./node_modules/lodash/isTypedArray.js ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var baseIsTypedArray = __webpack_require__(/*! ./_baseIsTypedArray */ "./node_modules/lodash/_baseIsTypedArray.js"),
    baseUnary = __webpack_require__(/*! ./_baseUnary */ "./node_modules/lodash/_baseUnary.js"),
    nodeUtil = __webpack_require__(/*! ./_nodeUtil */ "./node_modules/lodash/_nodeUtil.js");

/* Node.js helper references. */
var nodeIsTypedArray = nodeUtil && nodeUtil.isTypedArray;

/**
 * Checks if `value` is classified as a typed array.
 *
 * @static
 * @memberOf _
 * @since 3.0.0
 * @category Lang
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is a typed array, else `false`.
 * @example
 *
 * _.isTypedArray(new Uint8Array);
 * // => true
 *
 * _.isTypedArray([]);
 * // => false
 */
var isTypedArray = nodeIsTypedArray ? baseUnary(nodeIsTypedArray) : baseIsTypedArray;

module.exports = isTypedArray;


/***/ }),

/***/ "./node_modules/lodash/keys.js":
/*!*************************************!*\
  !*** ./node_modules/lodash/keys.js ***!
  \*************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var arrayLikeKeys = __webpack_require__(/*! ./_arrayLikeKeys */ "./node_modules/lodash/_arrayLikeKeys.js"),
    baseKeys = __webpack_require__(/*! ./_baseKeys */ "./node_modules/lodash/_baseKeys.js"),
    isArrayLike = __webpack_require__(/*! ./isArrayLike */ "./node_modules/lodash/isArrayLike.js");

/**
 * Creates an array of the own enumerable property names of `object`.
 *
 * **Note:** Non-object values are coerced to objects. See the
 * [ES spec](http://ecma-international.org/ecma-262/7.0/#sec-object.keys)
 * for more details.
 *
 * @static
 * @since 0.1.0
 * @memberOf _
 * @category Object
 * @param {Object} object The object to query.
 * @returns {Array} Returns the array of property names.
 * @example
 *
 * function Foo() {
 *   this.a = 1;
 *   this.b = 2;
 * }
 *
 * Foo.prototype.c = 3;
 *
 * _.keys(new Foo);
 * // => ['a', 'b'] (iteration order is not guaranteed)
 *
 * _.keys('hi');
 * // => ['0', '1']
 */
function keys(object) {
  return isArrayLike(object) ? arrayLikeKeys(object) : baseKeys(object);
}

module.exports = keys;


/***/ }),

/***/ "./node_modules/lodash/keysIn.js":
/*!***************************************!*\
  !*** ./node_modules/lodash/keysIn.js ***!
  \***************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var arrayLikeKeys = __webpack_require__(/*! ./_arrayLikeKeys */ "./node_modules/lodash/_arrayLikeKeys.js"),
    baseKeysIn = __webpack_require__(/*! ./_baseKeysIn */ "./node_modules/lodash/_baseKeysIn.js"),
    isArrayLike = __webpack_require__(/*! ./isArrayLike */ "./node_modules/lodash/isArrayLike.js");

/**
 * Creates an array of the own and inherited enumerable property names of `object`.
 *
 * **Note:** Non-object values are coerced to objects.
 *
 * @static
 * @memberOf _
 * @since 3.0.0
 * @category Object
 * @param {Object} object The object to query.
 * @returns {Array} Returns the array of property names.
 * @example
 *
 * function Foo() {
 *   this.a = 1;
 *   this.b = 2;
 * }
 *
 * Foo.prototype.c = 3;
 *
 * _.keysIn(new Foo);
 * // => ['a', 'b', 'c'] (iteration order is not guaranteed)
 */
function keysIn(object) {
  return isArrayLike(object) ? arrayLikeKeys(object, true) : baseKeysIn(object);
}

module.exports = keysIn;


/***/ }),

/***/ "./node_modules/lodash/now.js":
/*!************************************!*\
  !*** ./node_modules/lodash/now.js ***!
  \************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var root = __webpack_require__(/*! ./_root */ "./node_modules/lodash/_root.js");

/**
 * Gets the timestamp of the number of milliseconds that have elapsed since
 * the Unix epoch (1 January 1970 00:00:00 UTC).
 *
 * @static
 * @memberOf _
 * @since 2.4.0
 * @category Date
 * @returns {number} Returns the timestamp.
 * @example
 *
 * _.defer(function(stamp) {
 *   console.log(_.now() - stamp);
 * }, _.now());
 * // => Logs the number of milliseconds it took for the deferred invocation.
 */
var now = function() {
  return root.Date.now();
};

module.exports = now;


/***/ }),

/***/ "./node_modules/lodash/stubArray.js":
/*!******************************************!*\
  !*** ./node_modules/lodash/stubArray.js ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * This method returns a new empty array.
 *
 * @static
 * @memberOf _
 * @since 4.13.0
 * @category Util
 * @returns {Array} Returns the new empty array.
 * @example
 *
 * var arrays = _.times(2, _.stubArray);
 *
 * console.log(arrays);
 * // => [[], []]
 *
 * console.log(arrays[0] === arrays[1]);
 * // => false
 */
function stubArray() {
  return [];
}

module.exports = stubArray;


/***/ }),

/***/ "./node_modules/lodash/stubFalse.js":
/*!******************************************!*\
  !*** ./node_modules/lodash/stubFalse.js ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/**
 * This method returns `false`.
 *
 * @static
 * @memberOf _
 * @since 4.13.0
 * @category Util
 * @returns {boolean} Returns `false`.
 * @example
 *
 * _.times(2, _.stubFalse);
 * // => [false, false]
 */
function stubFalse() {
  return false;
}

module.exports = stubFalse;


/***/ }),

/***/ "./node_modules/lodash/throttle.js":
/*!*****************************************!*\
  !*** ./node_modules/lodash/throttle.js ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var debounce = __webpack_require__(/*! ./debounce */ "./node_modules/lodash/debounce.js"),
    isObject = __webpack_require__(/*! ./isObject */ "./node_modules/lodash/isObject.js");

/** Error message constants. */
var FUNC_ERROR_TEXT = 'Expected a function';

/**
 * Creates a throttled function that only invokes `func` at most once per
 * every `wait` milliseconds. The throttled function comes with a `cancel`
 * method to cancel delayed `func` invocations and a `flush` method to
 * immediately invoke them. Provide `options` to indicate whether `func`
 * should be invoked on the leading and/or trailing edge of the `wait`
 * timeout. The `func` is invoked with the last arguments provided to the
 * throttled function. Subsequent calls to the throttled function return the
 * result of the last `func` invocation.
 *
 * **Note:** If `leading` and `trailing` options are `true`, `func` is
 * invoked on the trailing edge of the timeout only if the throttled function
 * is invoked more than once during the `wait` timeout.
 *
 * If `wait` is `0` and `leading` is `false`, `func` invocation is deferred
 * until to the next tick, similar to `setTimeout` with a timeout of `0`.
 *
 * See [David Corbacho's article](https://css-tricks.com/debouncing-throttling-explained-examples/)
 * for details over the differences between `_.throttle` and `_.debounce`.
 *
 * @static
 * @memberOf _
 * @since 0.1.0
 * @category Function
 * @param {Function} func The function to throttle.
 * @param {number} [wait=0] The number of milliseconds to throttle invocations to.
 * @param {Object} [options={}] The options object.
 * @param {boolean} [options.leading=true]
 *  Specify invoking on the leading edge of the timeout.
 * @param {boolean} [options.trailing=true]
 *  Specify invoking on the trailing edge of the timeout.
 * @returns {Function} Returns the new throttled function.
 * @example
 *
 * // Avoid excessively updating the position while scrolling.
 * jQuery(window).on('scroll', _.throttle(updatePosition, 100));
 *
 * // Invoke `renewToken` when the click event is fired, but not more than once every 5 minutes.
 * var throttled = _.throttle(renewToken, 300000, { 'trailing': false });
 * jQuery(element).on('click', throttled);
 *
 * // Cancel the trailing throttled invocation.
 * jQuery(window).on('popstate', throttled.cancel);
 */
function throttle(func, wait, options) {
  var leading = true,
      trailing = true;

  if (typeof func != 'function') {
    throw new TypeError(FUNC_ERROR_TEXT);
  }
  if (isObject(options)) {
    leading = 'leading' in options ? !!options.leading : leading;
    trailing = 'trailing' in options ? !!options.trailing : trailing;
  }
  return debounce(func, wait, {
    'leading': leading,
    'maxWait': wait,
    'trailing': trailing
  });
}

module.exports = throttle;


/***/ }),

/***/ "./node_modules/lodash/toNumber.js":
/*!*****************************************!*\
  !*** ./node_modules/lodash/toNumber.js ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var isObject = __webpack_require__(/*! ./isObject */ "./node_modules/lodash/isObject.js"),
    isSymbol = __webpack_require__(/*! ./isSymbol */ "./node_modules/lodash/isSymbol.js");

/** Used as references for various `Number` constants. */
var NAN = 0 / 0;

/** Used to match leading and trailing whitespace. */
var reTrim = /^\s+|\s+$/g;

/** Used to detect bad signed hexadecimal string values. */
var reIsBadHex = /^[-+]0x[0-9a-f]+$/i;

/** Used to detect binary string values. */
var reIsBinary = /^0b[01]+$/i;

/** Used to detect octal string values. */
var reIsOctal = /^0o[0-7]+$/i;

/** Built-in method references without a dependency on `root`. */
var freeParseInt = parseInt;

/**
 * Converts `value` to a number.
 *
 * @static
 * @memberOf _
 * @since 4.0.0
 * @category Lang
 * @param {*} value The value to process.
 * @returns {number} Returns the number.
 * @example
 *
 * _.toNumber(3.2);
 * // => 3.2
 *
 * _.toNumber(Number.MIN_VALUE);
 * // => 5e-324
 *
 * _.toNumber(Infinity);
 * // => Infinity
 *
 * _.toNumber('3.2');
 * // => 3.2
 */
function toNumber(value) {
  if (typeof value == 'number') {
    return value;
  }
  if (isSymbol(value)) {
    return NAN;
  }
  if (isObject(value)) {
    var other = typeof value.valueOf == 'function' ? value.valueOf() : value;
    value = isObject(other) ? (other + '') : other;
  }
  if (typeof value != 'string') {
    return value === 0 ? value : +value;
  }
  value = value.replace(reTrim, '');
  var isBinary = reIsBinary.test(value);
  return (isBinary || reIsOctal.test(value))
    ? freeParseInt(value.slice(2), isBinary ? 2 : 8)
    : (reIsBadHex.test(value) ? NAN : +value);
}

module.exports = toNumber;


/***/ }),

/***/ "./node_modules/process/browser.js":
/*!*****************************************!*\
  !*** ./node_modules/process/browser.js ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports) {

// shim for using process in browser
var process = module.exports = {};

// cached from whatever global is present so that test runners that stub it
// don't break things.  But we need to wrap it in a try catch in case it is
// wrapped in strict mode code which doesn't define any globals.  It's inside a
// function because try/catches deoptimize in certain engines.

var cachedSetTimeout;
var cachedClearTimeout;

function defaultSetTimout() {
    throw new Error('setTimeout has not been defined');
}
function defaultClearTimeout () {
    throw new Error('clearTimeout has not been defined');
}
(function () {
    try {
        if (typeof setTimeout === 'function') {
            cachedSetTimeout = setTimeout;
        } else {
            cachedSetTimeout = defaultSetTimout;
        }
    } catch (e) {
        cachedSetTimeout = defaultSetTimout;
    }
    try {
        if (typeof clearTimeout === 'function') {
            cachedClearTimeout = clearTimeout;
        } else {
            cachedClearTimeout = defaultClearTimeout;
        }
    } catch (e) {
        cachedClearTimeout = defaultClearTimeout;
    }
} ())
function runTimeout(fun) {
    if (cachedSetTimeout === setTimeout) {
        //normal enviroments in sane situations
        return setTimeout(fun, 0);
    }
    // if setTimeout wasn't available but was latter defined
    if ((cachedSetTimeout === defaultSetTimout || !cachedSetTimeout) && setTimeout) {
        cachedSetTimeout = setTimeout;
        return setTimeout(fun, 0);
    }
    try {
        // when when somebody has screwed with setTimeout but no I.E. maddness
        return cachedSetTimeout(fun, 0);
    } catch(e){
        try {
            // When we are in I.E. but the script has been evaled so I.E. doesn't trust the global object when called normally
            return cachedSetTimeout.call(null, fun, 0);
        } catch(e){
            // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error
            return cachedSetTimeout.call(this, fun, 0);
        }
    }


}
function runClearTimeout(marker) {
    if (cachedClearTimeout === clearTimeout) {
        //normal enviroments in sane situations
        return clearTimeout(marker);
    }
    // if clearTimeout wasn't available but was latter defined
    if ((cachedClearTimeout === defaultClearTimeout || !cachedClearTimeout) && clearTimeout) {
        cachedClearTimeout = clearTimeout;
        return clearTimeout(marker);
    }
    try {
        // when when somebody has screwed with setTimeout but no I.E. maddness
        return cachedClearTimeout(marker);
    } catch (e){
        try {
            // When we are in I.E. but the script has been evaled so I.E. doesn't  trust the global object when called normally
            return cachedClearTimeout.call(null, marker);
        } catch (e){
            // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error.
            // Some versions of I.E. have different rules for clearTimeout vs setTimeout
            return cachedClearTimeout.call(this, marker);
        }
    }



}
var queue = [];
var draining = false;
var currentQueue;
var queueIndex = -1;

function cleanUpNextTick() {
    if (!draining || !currentQueue) {
        return;
    }
    draining = false;
    if (currentQueue.length) {
        queue = currentQueue.concat(queue);
    } else {
        queueIndex = -1;
    }
    if (queue.length) {
        drainQueue();
    }
}

function drainQueue() {
    if (draining) {
        return;
    }
    var timeout = runTimeout(cleanUpNextTick);
    draining = true;

    var len = queue.length;
    while(len) {
        currentQueue = queue;
        queue = [];
        while (++queueIndex < len) {
            if (currentQueue) {
                currentQueue[queueIndex].run();
            }
        }
        queueIndex = -1;
        len = queue.length;
    }
    currentQueue = null;
    draining = false;
    runClearTimeout(timeout);
}

process.nextTick = function (fun) {
    var args = new Array(arguments.length - 1);
    if (arguments.length > 1) {
        for (var i = 1; i < arguments.length; i++) {
            args[i - 1] = arguments[i];
        }
    }
    queue.push(new Item(fun, args));
    if (queue.length === 1 && !draining) {
        runTimeout(drainQueue);
    }
};

// v8 likes predictible objects
function Item(fun, array) {
    this.fun = fun;
    this.array = array;
}
Item.prototype.run = function () {
    this.fun.apply(null, this.array);
};
process.title = 'browser';
process.browser = true;
process.env = {};
process.argv = [];
process.version = ''; // empty string to avoid regexp issues
process.versions = {};

function noop() {}

process.on = noop;
process.addListener = noop;
process.once = noop;
process.off = noop;
process.removeListener = noop;
process.removeAllListeners = noop;
process.emit = noop;
process.prependListener = noop;
process.prependOnceListener = noop;

process.listeners = function (name) { return [] }

process.binding = function (name) {
    throw new Error('process.binding is not supported');
};

process.cwd = function () { return '/' };
process.chdir = function (dir) {
    throw new Error('process.chdir is not supported');
};
process.umask = function() { return 0; };


/***/ }),

/***/ "./node_modules/webpack/buildin/global.js":
/*!***********************************!*\
  !*** (webpack)/buildin/global.js ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports) {

var g;

// This works in non-strict mode
g = (function() {
	return this;
})();

try {
	// This works if eval is allowed (see CSP)
	g = g || new Function("return this")();
} catch (e) {
	// This works if the window reference is available
	if (typeof window === "object") g = window;
}

// g can still be undefined, but nothing to do about it...
// We return undefined, instead of nothing here, so it's
// easier to handle this case. if(!global) { ...}

module.exports = g;


/***/ }),

/***/ "./node_modules/webpack/buildin/module.js":
/*!***********************************!*\
  !*** (webpack)/buildin/module.js ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = function(module) {
	if (!module.webpackPolyfill) {
		module.deprecate = function() {};
		module.paths = [];
		// module.parent = undefined by default
		if (!module.children) module.children = [];
		Object.defineProperty(module, "loaded", {
			enumerable: true,
			get: function() {
				return module.l;
			}
		});
		Object.defineProperty(module, "id", {
			enumerable: true,
			get: function() {
				return module.i;
			}
		});
		module.webpackPolyfill = 1;
	}
	return module;
};


/***/ })

/******/ });
//# sourceMappingURL=main.js.map