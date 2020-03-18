try {
  (function(d) {
    try {
      var e = d.localStorage;
    } catch (b) {}
    function a(g) {
      var i = g.split(".");
      var h = i.length;
      if (i[h - 1] == "com") {
        return i[h - 2] + "." + i[h - 1];
      } else {
        if (i[h - 1] == "cn") {
          if (i[h - 2] == "com") {
            return i[h - 3] + "." + i[h - 2] + "." + i[h - 1];
          } else {
            return i[h - 2] + "." + i[h - 1];
          }
        }
      }
      return "";
    }
    var c = a(emtj_currentHostName);
    function f() {
      var g = this;
      this._ec = {};
      this.set = function(h, i) {
        g._evercookie(h, function() {}, i);
      };
      this._evercookie = function(i, h, j) {
        if (g._evercookie === undefined) {
          g = this;
        }
        g.evercookie_indexdb_storage(i, j);
        g._ec.cookieData = g.evercookie_cookie(i, j);
        g._ec.localData = g.evercookie_local_storage(i, j);
      };
      this.evercookie_local_storage = function(h, i) {
        try {
          if (e) {
            e.setItem(h, i);
          }
        } catch (j) {}
      };
      this.evercookie_indexdb_storage = function(j, l) {
        try {
          var i =
            d.indexedDB || d.mozIndexedDB || d.webkitIndexedDB || d.msIndexedDB;
          if (!i) {
            return;
          }
          var h = 1;
          var k = i.open("idb_evercookie", h);
          k.onerror = function(n) {};
          k.onupgradeneeded = function(p) {
            var o = p.target.result;
            var n = o.createObjectStore("evercookie", {
              keyPath: "name",
              unique: false
            });
          };
          k.onsuccess = function(r) {
            var n = r.target.result;
            if (n.objectStoreNames.contains("evercookie")) {
              var p = n.transaction(["evercookie"], "readwrite");
              var q = p.objectStore("evercookie");
              var o = q.put({ name: j, value: l });
            }
            n.close();
          };
        } catch (m) {}
      };
      this.evercookie_cookie = function(i, k) {
        var h = new Date();
        var j = 7300;
        h.setTime(h.getTime() + j * 24 * 3600 * 1000);
        document.cookie =
          i + "=; expires=Mon, 20 Sep 2010 00:00:00 UTC; path=/; domain=" + c;
        document.cookie =
          i +
          "=" +
          encodeURIComponent(k) +
          ";domain=" +
          c +
          ";path=/;expires=" +
          h.toGMTString();
      };
    }
    d.bigdataEvercookie = f;
  })(window);
} catch (ex) {}
(function(ah) {
  var ag = true;
  var aD = true;
  if (typeof emtj_logSet != "undefined" && emtj_logSet.substr(0, 1) == 0) {
    ag = false;
  }
  if (typeof emtj_logSet != "undefined" && emtj_logSet.substr(1, 1) == 0) {
    aD = false;
  }
  if (emtj_trueURL.indexOf("isTest=1&") >= 1) {
    setTimeout(function() {
      var aO = h("*[tracker-eventcode]");
      var aR = Array.prototype.slice.call(aO);
      var aN = h("*[data-tracker-eventcode]");
      var aL = Array.prototype.slice.call(aN);
      var aS = aR.concat(aL);
      len = aS.length;
      for (var aM = 0; aM < len; ++aM) {
        var aQ = aS[aM];
        var aP = aQ.getAttribute("class");
        var k =
          aQ.getAttribute("tracker-eventcode") ||
          aQ.getAttribute("data-tracker-eventcode");
        if (!aP) {
          aP = "";
        }
        aQ.setAttribute("class", aP + " " + k);
      }
    }, 3000);
    var aj = true;
    if (emtj_trueURL.indexOf("&openview=false") > 0) {
      aj = false;
    }
    var L = I("batchNum");
    var c = I("pageId");
    var U = L + "_" + c + "_pgresult";
    var E = true;
    var aI;
    var Y = { result: E, mes: aI };
    if (typeof emtj_isUpload != "undefined" && emtj_isUpload == 0 && aj) {
      aI = "109";
      Y = { result: E, mes: aI };
      localStorage.setItem(U, JSON.stringify(Y));
      return;
    }
    if (typeof emtj_logSet != "undefined" && !ag && aj) {
      aI = "108";
      Y = { result: E, mes: aI };
      localStorage.setItem(U, JSON.stringify(Y));
    }
  }
  if (typeof emtj_isUpload != "undefined" && emtj_isUpload == 0) {
    return;
  }
  var ay = ah.jQuery || ah.Zepto;
  var M = 0;
  var a = navigator.userAgent.toLowerCase();
  var aa = false;
  if (a.indexOf("ttjj") >= 0 || a.indexOf("eastmoney") >= 0) {
    aa = true;
  }
  var aw = "st_";
  var B = "20190910";
  var ap = "";
  var D = "";
  var Q = "";
  var aB = "";
  var w = "";
  var m;
  if (typeof emtj_sampleRate == "undefined") {
    emtj_sampleRate = 1;
  }
  if (
    networkProtocol.indexOf("http") >= 0 ||
    networkProtocol.indexOf("https") >= 0
  ) {
    if (emtj_trueURL.indexOf("isTest=1") >= 1) {
      ap = "//bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_JS_Test.gif";
      D =
        "//bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_Event_Test.gif";
    } else {
      ap = "//bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_JS.gif";
      D = "//bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_Event.gif";
      fingerUrl =
        "//bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_EmToken.gif";
      stayUrl =
        "//bdwblog.eastmoney.com/bd-blink-server/asyncgapi/web_other.gif";
    }
  } else {
    ap = "https://bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_JS.gif";
    D = "https://bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_Event.gif";
    stayUrl =
      "https://bdwblog.eastmoney.com/bd-blink-server/asyncgapi/web_other.gif";
  }
  var X = "";
  var au = "";
  var N = "";
  var n = "";
  var ae = "";
  var aC = "";
  var O = "";
  var aF = "4.5.2";
  var r = false;
  var az = "";
  var A = "";
  var ai = "";
  var b = "";
  var R = "";
  var e = "";
  var C = "";
  var av = "";
  var j = "";
  var Z = "";
  var F = "";
  var q = "";
  var af = "";
  var y = aH();
  var aG = -1;
  var W = new bigdataEvercookie();
  var v = new bigdataEvercookie();
  var al = new bigdataEvercookie();
  try {
    var at = window.localStorage;
  } catch (aJ) {}
  var H = emtj_getCookie("qgqp_b_id");
  var ab = undefined;
  var J = !!(window.attachEvent && !window.opera);
  var x = document.getElementsByTagName("script");
  if (x.length > 0) {
    for (var K = 0; K < x.length; K++) {
      var g = x[K].src;
      if (g && g.indexOf("jump_tracker.js") >= 0 && g.indexOf("stg") >= 0) {
        if (
          networkProtocol.indexOf("http") >= 0 ||
          networkProtocol.indexOf("https") >= 0
        ) {
          if (emtj_trueURL.indexOf("isTest=1") >= 1) {
            ap =
              "//bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_JS_Test.gif";
            D =
              "//bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_Event_Test.gif";
          } else {
            ap =
              "//blinkhd.eastmoney.com/bd-blink-server/asyncgapi/T_Web_JS.gif";
            D =
              "//blinkhd.eastmoney.com/bd-blink-server/asyncgapi/T_Web_Event.gif";
            fingerUrl =
              "//stg-bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_EmToken.gif";
            stayUrl =
              "//stg-bdwblog.eastmoney.com/bd-blink-server/asyncgapi/web_other.gif";
          }
        } else {
          ap =
            "https://stg-bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_JS.gif";
          D =
            "https://stg-bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_Event.gif";
          stayUrl =
            "https://stg-bdwblog.eastmoney.com/bd-blink-server/asyncgapi/web_other.gif";
        }
      }
    }
  }
  u(aw + "orirUrl");
  function emtj_getCookie(j) {
    var i,
      k = new RegExp("(^| )" + j + "=([^;]*)(;|$)");
    if ((i = document.cookie.match(k))) {
      if (decodeURIComponent(i[2]) == "delete") {
        return "";
      } else {
        return decodeURIComponent(i[2]);
      }
    } else {
      return "";
    }
  }
  function ao() {
    ae = l();
    aC = emtj_getCookie(aw + "si");
    if (!aC) {
      aC = emtj_getRandomStrBy(14);
      aE(aw + "si", aC);
    }
    if (aG == 0 || aG == 5 || aG == 2) {
      return;
    }
    N = emtj_getCookie(aw + "pvi");
    if (N) {
      aG = 1;
    }
    O = emtj_getCookie(aw + "sp");
    orirUrl = emtj_getCookie(aw + "inirUrl");
    if (!N) {
      if (at && at.getItem("st_pvi")) {
        N = at.getItem("st_pvi");
        O = at.getItem("st_sp");
        orirUrl = at.getItem("st_inirUrl");
        aG = 2;
      } else {
        if (y) {
          ar("st_pvi");
          ar("st_sp");
          ar("st_inirUrl");
        }
      }
    }
    if (N) {
      W.set("st_pvi", N);
      if (!O) {
        O = emtj_getNowFormatDate(new Date(), 2);
      }
      v.set("st_sp", O);
      if (!orirUrl) {
        orirUrl = document.referrer.split("?")[0];
      }
      al.set("st_inirUrl", orirUrl);
    } else {
      if (y) {
        setTimeout(function() {
          if (N) {
            W.set("st_pvi", N);
            if (!O) {
              O = emtj_getNowFormatDate(new Date(), 2);
            }
            v.set("st_sp", O);
            if (!orirUrl) {
              orirUrl = document.referrer.split("?")[0];
            }
            al.set("st_inirUrl", orirUrl);
          } else {
            ak();
          }
        }, 50);
      } else {
        ak();
      }
    }
  }
  ao();
  function ak() {
    N = emtj_getRandomStrBy(14);
    W.set("st_pvi", N);
    O = emtj_getNowFormatDate(new Date(), 2);
    v.set("st_sp", O);
    orirUrl = document.referrer.split("?")[0];
    al.set("st_inirUrl", orirUrl);
    aG = 0;
  }
  function aH() {
    if (
      (window.indexedDB =
        window.indexedDB ||
        window.mozIndexedDB ||
        window.webkitIndexedDB ||
        window.msIndexedDB)
    ) {
      return true;
    } else {
      return false;
    }
  }
  function ar(k) {
    try {
      var i = 1;
      var aL = indexedDB.open("idb_evercookie", i);
      aL.onerror = function(aN) {};
      aL.onupgradeneeded = function(aP) {
        var aO = aP.target.result;
        var aN = aO.createObjectStore("evercookie", {
          keyPath: "name",
          unique: false
        });
      };
      aL.onsuccess = function(aR) {
        var aN = aR.target.result;
        if (!aN.objectStoreNames.contains("evercookie")) {
          self._ec.idbData = undefined;
        } else {
          var aP = aN.transaction(["evercookie"]);
          var aQ = aP.objectStore("evercookie");
          var aO = aQ.get(k);
          aO.onsuccess = function(aS) {
            if (N && aG == 0) {
              return;
            }
            if (aO.result) {
              if (k == "st_pvi") {
                N = aO.result.value;
                aG = 5;
              } else {
                if (k == "st_sp") {
                  O = aO.result.value;
                } else {
                  if (k == "st_inirUrl") {
                    orirUrl = aO.result.value;
                  }
                }
              }
            }
          };
        }
        aN.close();
      };
    } catch (aM) {}
  }
  function z() {
    var k = document.location.toString();
    var i = k.split("?");
    if (i.length > 1) {
      w = "?" + i[1];
      return w;
    }
    return "";
  }
  function l() {
    if (
      networkProtocol.indexOf("http") < 0 &&
      networkProtocol.indexOf("https") < 0
    ) {
      return am();
    } else {
      return window.location.href.replace(/(^\s*)|(\s*$)/g, "");
    }
  }
  function am() {
    w = z();
    if (x.length > 0) {
      for (var i = 0; i < x.length; i++) {
        var aL = x[i].src;
        if (
          (aL && aL.indexOf("jump_tracker.js") >= 0) ||
          (aL && aL.indexOf("emtj_tracker.js") >= 0)
        ) {
          Q = x[i].getAttribute("emtj-url");
          aB = x[i].getAttribute("emtj-param");
        }
      }
    }
    if (aB == null) {
      aB = "";
    }
    if (aB != "" && w != "") {
      aB = "&" + aB + "&isFile=1";
    } else {
      if (aB != "" && w == "") {
        aB = "?" + aB + "&isFile=1";
      } else {
        if (aB == "" && w == "") {
          aB = "?isFile=1";
        } else {
          if (aB == "" && w != "") {
            aB = "&isFile=1";
          }
        }
      }
    }
    return (Q + w + aB).replace(/(^\s*)|(\s*$)/g, "");
  }
  function G(aM, aL) {
    var i = aM.split(".");
    var k = aL.split(".");
    if (i[0] * 1 > k[0] * 1) {
      return true;
    }
    if (i[0] * 1 >= k[0] * 1 && i[1] * 1 > k[1] * 1) {
      return true;
    }
    if (i[0] * 1 >= k[0] * 1 && i[1] * 1 >= k[1] * 1 && i[2] * 1 > k[2] * 1) {
      return true;
    }
    return false;
  }
  function d() {
    var i = navigator.userAgent.toLowerCase();
    if (i.indexOf("iphone") >= 0) {
      return "iphone";
    }
    if (i.indexOf("android") >= 0) {
      return "android";
    }
    if (i.indexOf("ipad") >= 0) {
      return "ipad";
    }
    return "";
  }
  function ac(i) {
    var aL = i.split(".");
    var k = aL.length;
    if (aL[k - 1] == "com") {
      return aL[k - 2] + "." + aL[k - 1];
    } else {
      if (aL[k - 1] == "cn") {
        if (aL[k - 2] == "com") {
          return aL[k - 3] + "." + aL[k - 2] + "." + aL[k - 1];
        } else {
          return aL[k - 2] + "." + aL[k - 1];
        }
      }
    }
    return "";
  }
  function aE(i, aM, aN) {
    var aL = ac(emtj_currentHostName);
    if (!aN) {
      document.cookie =
        i + "=" + encodeURIComponent(aM) + ";domain=" + aL + ";path=/";
      return;
    }
    var k = V(aN);
    var aO = new Date();
    aO.setTime(aO.getTime() + k * 1);
    document.cookie =
      i +
      "=" +
      encodeURIComponent(aM) +
      ";domain=" +
      aL +
      ";path=/;expires=" +
      aO.toGMTString();
  }
  function V(aL) {
    var k = aL.substring(1, aL.length) * 1;
    var i = aL.substring(0, 1);
    if (i == "s") {
      return k * 1000;
    } else {
      if (i == "h") {
        return k * 60 * 60 * 1000;
      } else {
        if (i == "d") {
          return k * 24 * 60 * 60 * 1000;
        }
      }
    }
  }
  function u(i) {
    var k = ac(emtj_currentHostName);
    var aM = new Date();
    aM.setTime(aM.getTime() - 1);
    var aL = emtj_getCookie(i);
    if (aL != null) {
      document.cookie =
        i + "=" + aL + ";domain=" + k + ";path=/;expires=" + aM.toGMTString();
    }
  }
  function t(aL, aN, k, i) {
    if (i) {
      var aM = k;
      k = function(aO) {
        aM.call(aL, aO);
      };
    }
    if (aL.addEventListener) {
      aL.addEventListener(aN, k);
    } else {
      if (aL.attachEvent) {
        aL.attachEvent("on" + aN, k);
      } else {
        aL["on" + aN] = k;
      }
    }
    return k;
  }
  function p(k, aL, i) {
    if (k.removeEventListener) {
      k.removeEventListener(aL, i);
    } else {
      if (k.detachEvent) {
        k.detachEvent("on" + aL, i);
      } else {
        k["on" + aL] = null;
      }
    }
  }
  function h(aX) {
    if (ay) {
      return ay(aX);
    }
    var aY = /([\*a-zA-Z1-6]*)?(\[(\w+)\s*(\^|\$|\*|\||~|!)?=?\s*([\w\u00C0-\uFFFF\s\-_\.]+)?\])?/,
      aO = arguments[1] || document,
      aQ = aX.match(aY),
      aY = aQ[1] || "*",
      aM = aQ[3],
      aT = aQ[4] + "=",
      aU = aQ[5],
      aV = { class: "className", for: "htmlFor" },
      aP = [],
      k = aY === "*" && aO.all ? aO.all : aO.getElementsByTagName(aY),
      aL = k.length;
    if (!!document.querySelectorAll && aT != "!=") {
      k = document.querySelectorAll(aX);
      for (var aR = 0, aL = k.length; aR < aL; aR++) {
        aP.push(k[aR]);
      }
      return aP;
    }
    if (!+"\v1") {
      aM = aV[aM] ? aV[aM] : aM;
    }
    while (aL--) {
      var aS = k[aL],
        aW = !+"\v1" ? aS[aM] : aS.getAttribute(aM);
      if (typeof aW === "string" && aW.length > 0) {
        if (!!aU) {
          var aN =
            aT === "="
              ? aW === aU
              : aT === "!="
              ? aW != aU
              : aT === "*="
              ? aW.indexOf(aU) >= 0
              : aT === "~="
              ? (" " + aW + " ").indexOf(aU) >= 0
              : aT === "^="
              ? aW.indexOf(aU) === 0
              : aT === "$="
              ? aW.slice(-aU.length) === aU
              : aT === "|="
              ? aW === aU || aW.substring(0, aU.length + 1) === aU + "-"
              : false;
          aN && aP.push(aS);
        } else {
          aP.push(aS);
        }
      }
    }
    return aP;
  }
  function aq(aM) {
    var aL = [];
    for (var i in aM) {
      aL.push(i + "=" + encodeURIComponent(aM[i]));
    }
    var aN = aL.join("&");
    P(ap + "?" + aN);
  }
  function I(aL) {
    var k = [];
    var aP = "";
    var aQ = window.location.href.split("?")[1];
    k = aQ.split("&");
    for (var aM = 0; aM < k.length; aM++) {
      if (k[aM].indexOf("#") == -1) {
        aP += "&" + k[aM];
      }
    }
    var aN = new RegExp("(^|&)" + aL + "=([^&]*)(&|$)");
    var aO = aP.match(aN);
    if (aO != null) {
      return decodeURIComponent(aO[2]);
    }
    return null;
  }
  function P(k) {
    if (emtj_trueURL.indexOf("isTest=1&") >= 1) {
      var aO = L + "_" + c + "_data";
      var aM = localStorage.getItem(aO);
      var aL = k + "&jsVersion=" + B;
      if (!aM) {
        localStorage.setItem(aO, aL);
      } else {
        localStorage.setItem(aO, aM + "@@@@@" + aL);
      }
    }
    function aP(aQ) {
      if (emtj_trueURL.indexOf("isTest=1&") >= 1) {
        if (k.indexOf("Web_JS") > 0) {
          U = L + "_" + c + "_pgresult";
          if (typeof emtj_isUpload == "undefined") {
            aQ = false;
            aI = 101;
          } else {
            if (c != emtj_pageId) {
              aQ = false;
              aI = 104;
            } else {
              if (aQ == false) {
                aI = 102;
              }
            }
          }
        } else {
          if (k.indexOf("Web_Event") > 0) {
            U = L + "_" + c + "_ecresult";
            if (aQ == false) {
              aI = 102;
            }
          }
        }
        if (aQ == true) {
          aI = 200;
        }
        Y = { result: aQ, mes: aI };
        localStorage.setItem(U, JSON.stringify(Y));
      }
    }
    var i = new Image();
    var aN = "_img_" + Math.random();
    window[aN] = i;
    i.onload = function() {
      window[aN] = null;
      aP(true);
    };
    i.onerror = function(aQ) {
      window[aN] = null;
      aP(false);
    };
    i.src = k + "&jsVersion=" + B;
  }
  function T(aN, aL, aM, i, k) {
    M++;
    m = emtj_userActionId + "-" + aM + "-" + M;
    ae = l();
    aE(aw + "asi", m);
    P(
      D +
        "?elem=" +
        aN +
        "&EventType=" +
        aL +
        "&EventCode=" +
        encodeURIComponent(aM) +
        "&ExtInfo=" +
        encodeURIComponent(i) +
        "&UID=" +
        n +
        "&UVNO=" +
        N +
        "&url=" +
        encodeURIComponent(ae) +
        "&gtu=" +
        encodeURIComponent(k) +
        "&deviceId=" +
        A +
        "&deviceType=" +
        ai +
        "&tradeID=" +
        b +
        "&tradeIDType=" +
        R +
        "&phoneModle=" +
        e +
        "&preEventCode=" +
        C +
        "&gt=" +
        av +
        "&appKey=" +
        Z +
        "&deviceBrand=" +
        F +
        "&phoneAppVersion=" +
        j +
        "&appSeid=" +
        q +
        "&appEuid=" +
        af +
        "&sr=" +
        emtj_sampleRate +
        "&pi=" +
        emtj_pageId +
        "&mt=" +
        encodeURIComponent(m) +
        "&passc=" +
        H +
        "&cerr=" +
        au
    );
  }
  function s(k) {
    var aL = [];
    for (var aM = 0; aM < k.length; aM++) {
      if (aL.indexOf(k[aM]) == -1) {
        aL.push(k[aM]);
      }
    }
    return aL;
  }
  function ax(i) {
    return i
      .split("")
      .reverse()
      .join("");
  }
  var ad = function() {
    if (aa) {
      k();
    } else {
      i();
    }
    function i() {
      var aM = new Date();
      var aN = {};
      aN.url = ae;
      aN.rUrl = document.referrer
        .replace(/<\/?.+?>/g, "")
        .replace(/[\r\n]/g, "");
      aN.si = aC;
      aN.sn = parseInt(emtj_getCookie(aw + "sn")) + 1;
      if (!aN.sn) {
        aN.sn = 1;
      }
      aE(aw + "sn", aN.sn);
      aN.scr = window.screen.width + "x" + window.screen.height;
      aN.dpr = window.devicePixelRatio;
      var aS = "";
      if (navigator.language) {
        aS = navigator.language;
      } else {
        aS = navigator.browserLanguage;
      }
      aN.lg = aS;
      aN.tz = "" + (aM.getTimezoneOffset() / 60) * -1;
      if (typeof emtj_startTime != "undefined") {
        var aL = emtj_startTime;
      } else {
        aL = 0;
      }
      aN.domreadyt = emtj_endTime - aL;
      aN.wt = -1;
      if (
        window.performance ||
        window.webkitPerformance ||
        window.msPerformance ||
        window.mozPerformance
      ) {
        var aR =
          window.performance ||
          window.webkitPerformance ||
          window.msPerformance ||
          window.mozPerformance;
        aN.domreadyt =
          aR.timing.domContentLoadedEventEnd - aR.timing.navigationStart;
        aN.wt = aR.timing.responseStart - aR.timing.navigationStart;
      }
      var aO = emtj_getCookie(aw + "psi");
      var aQ = emtj_getCookie(aw + "asi");
      if (!aO) {
        aN.psi = "";
      } else {
        aN.psi = aO;
      }
      if (!aQ) {
        aN.asi = "";
      } else {
        aN.asi = aQ;
      }
      aE(aw + "psi", emtj_userActionId);
      aE(aw + "asi", "delete");
      n = aN.ui = emtj_getUI();
      aN.deviceId = "";
      aN.deviceType = "";
      var aP = emtj_getCookie("fund_trade_trackid");
      if (!aP || aP == "undefined" || aP == undefined) {
        aN.tradeID = "";
        aN.tradeIDType = "";
      } else {
        aN.tradeID = aP;
        aN.tradeIDType = 2;
      }
      aN.phoneModle = "";
      aN.preEventCode = "";
      aN.gt = "";
      aN.phoneAppVersion = "";
      aN.appKey = "";
      aN.deviceBrand = "";
      aN.appSeid = "";
      aN.appEuid = "";
      if (r == true) {
        return;
      } else {
        if (az != "") {
          n = aN.ui = emtj_appUID;
          aN.deviceId = A;
          aN.deviceType = ai;
          aN.tradeID = b;
          aN.tradeIDType = R;
          aN.phoneModle = e;
          aN.preEventCode = C;
          aN.gt = av;
          aN.phoneAppVersion = j;
          aN.appKey = Z;
          aN.deviceBrand = F;
          aN.appSeid = q;
          aN.appEuid = af;
        }
      }
      aN.pi = emtj_pageId;
      aN.mt = emtj_userActionId;
      aN.err = X;
      aN.tus = "";
      aN.eti = "";
      aN.passc = H;
      if (N || !y) {
        aN.pvi = N;
        aN.sp = O;
        aN.orirUrl = orirUrl;
        aN.extinfo = aG;
        aq(aN);
        aG = 1;
      } else {
        if (y) {
          setTimeout(function() {
            aN.pvi = N;
            aN.sp = O;
            aN.orirUrl = orirUrl;
            aN.extinfo = aG;
            aq(aN);
            aG = 1;
          }, 50);
        }
      }
    }
    function k() {
      function aO(aR) {
        var aR = aR;
        var aS = document.createElement("iframe");
        aS.style.width = "1px";
        aS.style.height = "1px";
        aS.style.display = "none";
        aS.src = aR;
        document.body.appendChild(aS);
        setTimeout(function() {
          aS.remove();
        }, 1000);
      }
      if (a.indexOf("ttjj") >= 0) {
        var aM = a.match(/ttjj\/(.*)[\s]*/);
        if (aM != null) {
          j = aM = aM[1];
          window.logsession = function(aR) {
            az = JSON.stringify(aR);
            try {
              if (!aR.DeviceId) {
                A = "";
              } else {
                A = window.btoa(ax(emtj_getRandomStrBy(6) + "-" + aR.DeviceId));
              }
              emtj_appUID = aR.UID;
              ai = aR.DeviceType;
              b = aR.TradeID;
              if (b != "") {
                R = 2;
              } else {
                R = "";
              }
              C = aR.preEventCode;
              if (!aR.preEventCode) {
                C = "";
              }
              if (!aR.phoneModle) {
                e = "";
              } else {
                e = aR.phoneModle;
              }
              if (!aR.deviceBrand) {
                F = "";
              } else {
                F = aR.deviceBrand;
              }
              if (!aR.appKey) {
                Z = "";
              } else {
                Z = aR.appKey;
              }
              if (!aR.euid) {
                af = "";
              } else {
                af = window.btoa(ax(emtj_getRandomStrBy(6) + "-" + aR.euid));
              }
            } catch (aS) {
              X = aS;
            }
            r = false;
            i();
          };
          if (G(aM, aF)) {
            r = true;
            aO('emfundapp:applogsession({"callbackMethodName":"logsession"})');
          } else {
            r = false;
            i();
          }
        }
      } else {
        if (a.indexOf("eastmoney") >= 0) {
          var aP = true;
          r = true;
          setonReady = setTimeout(function() {
            aP = false;
            r = false;
            i();
          }, 1000);
          window.cb_appinfo = function(aR) {
            az = aR;
            var aT = JSON.parse(
              aR.replace(/\n/g, "\\\\n").replace(/\r/g, "\\\\r")
            );
            try {
              if (!aT.data.deviceInfo.deviceID) {
                A = "";
              } else {
                A = window.btoa(
                  ax(emtj_getRandomStrBy(6) + "-" + aT.data.deviceInfo.deviceID)
                );
              }
              if (!aT.data.passport || !aT.data.passport.uid) {
                emtj_appUID = "";
              } else {
                emtj_appUID = aT.data.passport.uid;
              }
              ai = aT.data.deviceInfo.deviceType;
              if (
                !aT.data.trade ||
                !aT.data.trade.length ||
                !aT.data.trade[0].tradeCustomId
              ) {
                b = "";
                R = "";
              } else {
                b = aT.data.trade[0].tradeCustomId;
                R = 1;
              }
              e = aT.data.deviceInfo.phoneModle;
              if (!aT.data.deviceInfo.gToken) {
                av = "";
              } else {
                av = aT.data.deviceInfo.gToken;
              }
              j = aT.data.deviceInfo.appversion;
              if (
                !aT.data.deviceInfo.appKey &&
                aT.data.deviceInfo.ProductType == "uufund"
              ) {
                Z = "62yhha34";
              } else {
                if (!aT.data.deviceInfo.appKey) {
                  Z = "";
                } else {
                  Z = aT.data.deviceInfo.appKey;
                }
              }
              if (!aT.data.deviceInfo.deviceBrand) {
                F = "";
              } else {
                F = aT.data.deviceInfo.deviceBrand;
              }
              C = "";
              if (!aT.data.deviceInfo.appSessionid) {
                q = "";
              } else {
                q = aT.data.deviceInfo.appSessionid;
              }
              if (!aT.data.deviceInfo.euid) {
                af = "";
              } else {
                af = window.btoa(
                  ax(emtj_getRandomStrBy(6) + "-" + aT.data.deviceInfo.euid)
                );
              }
            } catch (aS) {
              X = aS;
            }
            if (aP) {
              clearTimeout(setonReady);
              r = false;
              i();
            }
          };
          var aQ =
            '{"callbackname": "cb_appinfo","type": "passport,deviceInfo,trade"}';
          function aL() {
            if (/(iPhone|iPod|iPad|iTouch|iOS)/i.test(navigator.userAgent)) {
              return true;
            } else {
              return false;
            }
          }
          function aN() {
            if (aL()) {
              if (
                emtj_currentHostName == "gubatestapi.eastmoney.com" ||
                emtj_currentHostName == "gubaapi.eastmoney.com" ||
                emtj_currentHostName == "gubaapihttps.eastmoney.com"
              ) {
                if (a.indexOf("appversion_") >= 0) {
                  aO("h5GetModuleInfo:" + aQ);
                } else {
                  clearTimeout(setonReady);
                  aP = false;
                  r = false;
                  i();
                }
              } else {
                aO("h5GetModuleInfo:" + aQ);
              }
            } else {
              prompt("h5GetModuleInfo", aQ + "$&&$java.lang.String");
            }
          }
          aN();
        }
      }
    }
  };
  var S = function() {
    function i() {
      var aM = d();
      if (aM) {
        var aL = {
          tap: function(aP, aQ) {
            var aO,
              aN,
              aR = 10;
            aP.addEventListener(
              "touchstart",
              function(aT) {
                var aS = aT.targetTouches[0];
                aO = aS.pageX;
                aN = aS.pageY;
              },
              false
            );
            aP.addEventListener(
              "touchend",
              function(aU) {
                var aT = aU.changedTouches[0],
                  aS = aT.pageX,
                  aV = aT.pageY;
                if (Math.abs(aO - aS) < aR && Math.abs(aN - aV) < aR) {
                  aQ();
                }
              },
              false
            );
          }
        };
        aL.tap(document, k);
      } else {
        t(document.body, "mousedown", k, true);
      }
    }
    function k(aQ) {
      var aR = emtj_willHandle(emtj_sampleRate);
      if (!aR) {
        return;
      }
      aQ = aQ || window.event;
      var aT = aQ.target || aQ.srcElement;
      var aM = aT.tagName;
      var aP = 0;
      try {
        while (
          !aT.getAttribute("tracker-eventcode") &&
          !aT.getAttribute("data-tracker-eventcode") &&
          aP < 5
        ) {
          if (aT == document.body || aT == document.documentElement) {
            return;
          }
          aP++;
          aT = aT.parentNode;
        }
        var aO =
          aT.getAttribute("tracker-eventcode") ||
          aT.getAttribute("data-tracker-eventcode");
        if (aO) {
          var aL =
            aT.getAttribute("tracker-extinfo") ||
            aT.getAttribute("data-tracker-extinfo");
          var aS = aT.getAttribute("href");
          if (!aS) {
            aS = "";
          }
          T(aM, "click", aO, aL, aS);
        }
      } catch (aN) {
        au = aN;
      }
    }
    i();
  };
  var aK = function() {
    var ba = -1;
    var bc = -1;
    var a7 = -1;
    var aR = [];
    var a6 = 0;
    var aL = (mainPage = 0);
    var aV = 0;
    var a8 = 0;
    var a4, aZ;
    var a0 = 0;
    var aY;
    var a9 = "in";
    var bk = false;
    var a5 = 10;
    var a1 = "default";
    var bh = 0;
    var a3 = l();
    if (
      window.performance ||
      window.webkitPerformance ||
      window.msPerformance ||
      window.mozPerformance
    ) {
      var a2 =
        window.performance ||
        window.webkitPerformance ||
        window.msPerformance ||
        window.mozPerformance;
      var bf = a2.timing;
      emtj_startTime = bf.navigationStart;
      a4 = new Date(emtj_startTime);
      aZ = emtj_getNowFormatDate(a4, 2);
      be(emtj_startTime);
    } else {
      if (typeof emtj_startTime != "undefined") {
        a4 = new Date(emtj_startTime);
        aZ = emtj_getNowFormatDate(a4, 2);
        be(emtj_startTime);
      }
    }
    function bj() {
      if (a9 == "in") {
        a5 = 10;
      }
    }
    function be(bn) {
      bh =
        document.documentElement.scrollTop ||
        document.body.scrollTop ||
        window.pageYOffset;
      aR.push(bh);
      window.keeptime = setInterval(function() {
        a5 -= 1;
        if (0 == a5) {
          a9 = "out";
          bk = true;
          a1 = "wait";
          aN();
          clearInterval(keeptime);
        }
      }, 1000);
      var i = {
        tap: function(br, bs) {
          var bq,
            bp,
            bt = 10;
          br.addEventListener(
            "touchstart",
            function(bv) {
              var bu = bv.targetTouches[0];
              bq = bu.pageX;
              bp = bu.pageY;
            },
            false
          );
          br.addEventListener(
            "touchend",
            function(bw) {
              var bv = bw.changedTouches[0],
                bu = bv.pageX,
                bx = bv.pageY;
              if (Math.abs(bq - bu) < bt && Math.abs(bp - bx) < bt) {
                bs();
              } else {
                if (Math.abs(bq - bu) > bt || Math.abs(bp - bx) > bt) {
                  bs();
                }
              }
            },
            false
          );
        }
      };
      i.tap(document, bj);
      function bo(bq) {
        var br = document.getElementsByTagName(bq);
        for (var bp = 0; bp < br.length; bp++) {
          if (
            br[bp].type == "text" ||
            br[bp].type == "textarea" ||
            br[bp].type == "select-one"
          ) {
            br[bp].addEventListener(
              "input",
              function() {
                bj();
              },
              false
            );
          }
        }
      }
      bo("input");
      bo("textarea");
      bo("select");
    }
    function aQ() {
      var bq = document.querySelector(".info-info");
      var bn = bq.innerText.length;
      var bp = (bn / 400) * 60;
      var bo = 0;
      var br = bq.getElementsByTagName("img");
      if (br.length) {
        var bs = 6;
        for (var i = 0; i < br.length; i++) {
          if (i >= 2) {
            bs = 3;
          } else {
            bs = bs - 1;
          }
          bo = bo + bs;
        }
      }
      a8 = Math.round(bp + bo);
    }
    function aN() {
      aY = new Date();
      var bn = emtj_getNowFormatDate(aY, 2);
      a0 = (aY.getTime() - emtj_startTime) / 1000;
      aV = window.innerHeight || document.documentElement.clientHeight;
      aL = document.documentElement.scrollHeight;
      if (aV) {
        ba = Math.floor((aL / aV) * 100) / 100;
      }
      if (document.querySelector(".info-info") && aV) {
        mainPage =
          document.querySelector(".info-info").offsetHeight +
          document.querySelector(".info-info").offsetTop;
        bc = Math.floor((mainPage / aV) * 100) / 100;
        aQ();
      }
      var i = s(aR);
      if (i.length > 1 && aV) {
        a6 = Math.max.apply(null, i);
        a7 = Math.floor((a6 / aV + 1) * 100) / 100;
      } else {
        if (aV) {
          bh =
            document.documentElement.scrollTop ||
            document.body.scrollTop ||
            window.pageYOffset;
          a7 = Math.floor((bh / aV + 1) * 100) / 100;
        }
      }
      P(
        stayUrl +
          "?url=" +
          encodeURIComponent(a3) +
          "&st=" +
          a0 +
          "&sd=" +
          aZ +
          "&ed=" +
          bn +
          "&mt=" +
          emtj_userActionId +
          "&pvi=" +
          N +
          "&si=" +
          aC +
          "&flag=" +
          bk +
          "&type=" +
          "stayTime" +
          "&snum=" +
          ba +
          "&msc=" +
          bc +
          "&maxsc=" +
          a7 +
          "&estime=" +
          a8 +
          "&leavet=" +
          a1 +
          "&rnd=" +
          Math.random()
      );
    }
    window.addEventListener("scroll", bg, false);
    if (!Date.now) {
      Date.now = function() {
        return new Date().getTime();
      };
    }
    var aO = ["webkit", "moz"];
    for (var bi = 0; bi < aO.length && !window.requestAnimationFrame; ++bi) {
      var aW = aO[bi];
      window.requestAnimationFrame = window[aW + "RequestAnimationFrame"];
    }
    if (
      /iP(ad|hone|od).*OS 6/.test(window.navigator.userAgent) ||
      !window.requestAnimationFrame
    ) {
      var bm = 0;
      window.requestAnimationFrame = function(bo) {
        var bn = Date.now();
        var i = Math.max(bm + 16, bn);
        return setTimeout(function() {
          bo((bm = i));
        }, i - bn);
      };
    }
    scheduledAnimationFrame = false;
    function bg() {
      if (scheduledAnimationFrame) {
        return;
      }
      scheduledAnimationFrame = true;
      window.requestAnimationFrame(function() {
        scheduledAnimationFrame = false;
        bj();
        bh =
          document.documentElement.scrollTop ||
          document.body.scrollTop ||
          window.pageYOffset;
        aR.push(bh);
      });
    }
    function aM() {
      if (a9 == "in") {
        a9 = "out";
        clearInterval(keeptime);
        aN();
      }
    }
    if (
      a.indexOf("iphone") >= 0 ||
      a.indexOf("ipad") >= 0 ||
      a.indexOf("android") >= 0
    ) {
      window.addEventListener("pagehide", bb, false);
    } else {
      window.addEventListener("beforeunload", k, false);
    }
    function bb() {
      a1 = "pagehide";
      aM();
    }
    function k() {
      a1 = "beforeunload";
      aM();
    }
    var aX = !!(window.history && history.pushState);
    if (aX) {
      var bl = function(i) {
        var bn = window.history[i];
        return function() {
          var bp = bn.apply(this, arguments);
          var bo = new Event(i.toLowerCase());
          bo.arguments = arguments;
          window.dispatchEvent(bo);
          return bp;
        };
      };
      window.history.pushState = bl("pushState");
      window.history.replaceState = bl("replaceState");
    }
    window.addEventListener("pushstate", aP, false);
    window.addEventListener("replacestate", aP, false);
    window.addEventListener("popstate", aP, false);
    function aP(i) {
      a1 = "spa";
      aM();
      emtj_startTime = new Date().getTime();
      a4 = new Date(emtj_startTime);
      aZ = emtj_getNowFormatDate(a4, 2);
      a0 = 0;
      bk = false;
      a5 = 10;
      a9 = "in";
      a1 = "default";
      aR = [];
      bc = -1;
      a8 = 0;
      a3 = l();
      be(emtj_startTime);
    }
    function aU() {
      var bo = ["webkit", "moz", "ms", "o"];
      if ("hidden" in document) {
        return "hidden";
      }
      for (var bn = 0; bn < bo.length; bn++) {
        if (bo[bn] + "Hidden" in document) {
          return bo[bn] + "Hidden";
        }
      }
      return null;
    }
    var aT = aU();
    if (aT) {
      var bd = aT.replace(/[H|h]idden/, "") + "visibilitychange";
      document.addEventListener(bd, aS, false);
    }
    function aS() {
      if (document[aU()]) {
        a1 = "visibilitychange";
        aM();
      } else {
        emtj_startTime = new Date().getTime();
        a4 = new Date(emtj_startTime);
        aZ = emtj_getNowFormatDate(a4, 2);
        a0 = 0;
        bk = false;
        a5 = 10;
        a9 = "in";
        a1 = "default";
        aR = [];
        bc = -1;
        a8 = 0;
        a3 = l();
        be(emtj_startTime);
      }
    }
  };
  var aA = [
    117016300211,
    113300301472,
    117001300541,
    112101300783,
    117003300159
  ];
  var o = false;
  for (var K = 0; K < aA.length; K++) {
    if (emtj_pageId == aA[K]) {
      o = true;
    }
  }
  if (
    ae.indexOf("emwap.eastmoney.com/news/info/detail/") >= 0 ||
    ae.indexOf("stg-webjs-test.dfcfw.com/hsf10") >= 0 ||
    ae.indexOf("https://peh5.uufund.com") >= 0 ||
    ae.indexOf("https://www.uufund.com") >= 0 ||
    o
  ) {
    if (emtj_trueURL.indexOf("isTest=1&") < 0) {
      try {
        aK();
      } catch (an) {}
    }
  }
  if (emtj_trueURL.indexOf("isTest=1") >= 1) {
    if (typeof emtj_logSet == "undefined" && aj) {
      ad();
    }
    if (typeof emtj_logSet != "undefined" && ag && aj) {
      ad();
    }
    if (typeof emtj_logSet != "undefined" && aD) {
      S();
    }
  } else {
    if (typeof emtj_logSet == "undefined") {
      ad();
    }
    if (typeof emtj_logSet != "undefined" && ag) {
      ad();
    }
    if (typeof emtj_logSet != "undefined" && aD) {
      S();
    }
  }
  window.emtjLaunch = function() {
    emtj_creUserAcId();
    ao();
    ad();
  };
  window.bindPageTracker = function() {};
  window.sendTrackLog = T;
  window.sendRequestLog = P;
  while (send_arr.length) {
    var f = send_arr.shift();
    if (f[0] == "sendTrackLog") {
      T(f[1], f[2], f[3], f[4], f[5]);
    } else {
      if (f[0] == "bindPageTracker") {
      } else {
        if (f[0] == "emtjLaunch") {
          emtj_creUserAcId();
          ao();
          ad();
        } else {
          if (f[0] == "sendRequestLog") {
            P(f[1]);
          }
        }
      }
    }
  }
})(window);
