(function() {
    'use strict';
    NFBR.GlobalConfig = {
        /* viewer */
        /**
         * license server domain name.
         *
         * @const
         * @type {string}
         */
        SERVER_DOMAIN : 'https://pcreader.bookwalker.com.tw/browserWebApi',

        /**
         * webAPI response header argument 'status'.
         *
         * @const
         * @type {string}
         */
        JSON_KEY_STATUS_CODE : 'status',
        /**
         * webAPI response header argument 'url'.
         *
         * @const
         * @type {string}
         */
        JSON_KEY_CONTENT_URL : 'url',
        /**
         * webAPI response header argument 'lp'.
         *
         * @const
         * @type {string}
         */
        JSON_KEY_PREVIEW_PAGE : 'lp',
        /**
         * webAPI response header argument 'cti'.
         *
         * @const
         * @type {string}
         */
        JSON_KEY_CONTENT_TITLE : 'cti',
        /**
         * webAPI response header argument 'cty'.
         *
         * @const
         * @type {string}
         */
        JSON_KEY_CONTENT_TYPE : 'cty',
        /**
         * webAPI response header argument 'lin'.
         *
         * @const
         * @type {string}
         */
        JSON_KEY_LOOKINSIDE_SPEC : 'lin',
        /**
         * webAPI response header argument 'lpd'.
         *
         * @const
         * @type {string}
         */
        JSON_KEY_LAST_PAGE_SPEC : 'lpd',
        /**
         * webAPI response header argument 'bs'.
         *
         * @const
         * @type {string}
         */
        JSON_KEY_BOOKMARK_SHERED : 'bs',
        /**
         * webAPI response header argument 'ms'.
         *
         * @const
         * @type {string}
         */
        JSON_KEY_MARKER_SHARED : 'ms',
        /**
         * webAPI response header argument 'tw'.
         *
         * @const
         * @type {string}
         */
        JSON_KEY_TWITTER_ENABLED : 'tw',
        /**
         * webAPI response header argument 'fb'.
         *
         * @const
         * @type {string}
         */
        JSON_KEY_FACEBOOK_ENABLED : 'fb',
        /**
         * webAPI response header argument 'uid'.
         *
         * @const
         * @type {string}
         */
        JSON_KEY_USER_ID : 'uid',
        /**
         * webAPI response header argument 'tri'
         * content auth info key.
         *
         * @const
         * @type {string}
         */
        JSON_KEY_TRACKING_IMAGE : 'tri',
        /**
         * content auth info key.
         *
         * @const
         * @type {string}
         */
        JSON_KEY_AUTH_INFO : 'auth_info',
        /**
         * content limited free key.
         *
         * @const
         * @type {string}
         */
        JSON_KEY_LIMITED_FREE : 'limited_free',
        /**
         * webAPI location rate_page method.
         *
         * @const
         * @type {string}
         */
        WEBAPI_RATE_PAGE : '/rate_page',
        /**
         * webAPI location content check method.
         *
         * @const
         * @type {string}
         */
        WEBAPI_CONTENT_CHECK : '/c',
        /**
         * webAPI location last page information method.
         *
         * @const
         * @type {string}
         */
        WEBAPI_LAST_PAGE_INFO : '/lpi',
        /**
         * webAPI location look indie check method.
         *
         * @const
         * @type {string}
         */
        WEBAPI_LOOKINSIDE_CHECK : '/lc',
        /**
         * webAPI location get bookmark method.
         *
         * @const
         * @type {string}
         */
        WEBAPI_GET_BOOKMARK : '/gb',
        /**
         * webAPI location put bookmark method.
         *
         * @const
         * @type {string}
         */
        WEBAPI_PUT_BOOKMARK : '/pb',
        /**
         * webAPI location get marker method.
         *
         * @const
         * @type {string}
         */
        WEBAPI_GET_MARKER : '/gm',
        /**
         * webAPI location put marker method.
         *
         * @const
         * @type {string}
         */
        WEBAPI_PUT_MARKER : '/pm',
        /**
         * webAPI location page from cfi method.
         *
         * @const
         * @type {string}
         */
        WEBAPI_PAGE_FROM_CFI : '/pfc',
        /**
         * webAPI location region index from cfi method.
         *
         * @const
         * @type {string}
         */
        WEBAPI_REGION_INDEX_FROM_CFI : '/ric',
        /**
         * webAPI location get cfi from region index method.
         *
         * @const
         * @type {string}
         */
        WEBAPI_GET_CFI_FROM_REGION_INDEX : '/cri',
        /**
         * webAPI search content method.
         *
         * @const
         * @type {string}
         */
        WEBAPI_SEARCH_CONTENT : '/s',
        /**
         * webAPI location twitter message method.
         *
         * @const
         * @type {string}
         */
        WEBAPI_TWITTER_MESSAGE : '/tm',
        /**
         * webAPI location facebook message method.
         *
         * @const
         * @type {string}
         */
        WEBAPI_FACEBOOK_MESSAGE : '/fm',
        /**
         * webAPI location pseudo reflow method.
         *
         * @const
         * @type {string}
         */
        WEBAPI_CONTENT_BY_RESOLUTION : '/cbr',
        /**
         * webAPI location count viewing time method.
         *
         * @const
         * @type {string}
         */
        WEBAPI_COUNT_VIEWING_TIME : '/cvt',
        /**
         * interval between getting response of count viewing time method and sending next request of it.
         * unit is millisecond.
         *
         * @const
         * @type {number}
         */
        COUNT_VIEWING_TIME_INTERVAL : 10000,
        /**
         * if true when http request POST method Content-Type=text/plain.
         * othewise default Content-type.
         *
         * @const
         * @type {boolean}
         */
        WEBAPI_POST_TEXT_PLAIN : false,
        /**
         * If true, it sends Browser ID to the server.
         *
         * @const
         * @type {boolean}
         */
        SEND_BROWSER_ID : true,
        /**
         * publis webapi parameter BID value suffix.
         *
         * @const
         * @type {string}
         */
        BROWSER_ID_SUFFIX : 'NFBR',
        /**
         * publis webapi parameter sessionId value suffix.
         *
         * @const
         * @type {string}
         */
        SESSION_ID_SUFFIX : 'SESSION',
        /**
         * local storage save key name for 'BrowserID'.
         *
         * @const
         * @type {string}
         */
        LOCALSTORAGE_KEY_BID : 'NFBR.Global/BrowserId'
    };
    Cldr._resolved = {};
    Globalize.loadTranslations('ja', {nfbr: {global_api: {err_msg_400:"指定された書籍は現在閲覧できません。<br>（エラー400）"}}});
    Globalize.loadTranslations('en', {nfbr: {global_api: {err_msg_400:"The eBook chosen cannot be viewed.<br>（ERROR400）"}}});
    Globalize.loadTranslations('zh-TW', {nfbr: {global_api: {err_msg_400:"您所選的書籍現在無法閱覽。<br>（ERROR 400）"}}});
    Globalize.loadTranslations('ja', {nfbr: {global_api: {err_msg_401:"指定された書籍は閲覧できません。<br>認証されていない、または認証期限が切れています。再度ログインしてください。"}}});
    Globalize.loadTranslations('en', {nfbr: {global_api: {err_msg_401:"The eBook chosen cannot be viewed, since authorization is invalid or expired . Please sign-in again."}}});
    Globalize.loadTranslations('zh-TW', {nfbr: {global_api: {err_msg_401:"您所選的書籍無法閱覽。<br>您的帳號未認證或已超過認證期限，請重新登入。"}}});
    Globalize.loadTranslations('ja', {nfbr: {global_api: {err_msg_403:"指定された書籍は閲覧できません。<br>購入されていない書籍です。購入してから再度お試しください。"}}});
    Globalize.loadTranslations('en', {nfbr: {global_api: {err_msg_403:"The eBook chosen cannot open since not yet purchased.  Please make a purchase and try again."}}});
    Globalize.loadTranslations('zh-TW', {nfbr: {global_api: {err_msg_403:"您所選的書籍無法閱覽。<br>您尚未購入此書，請購買後再重試。"}}});
    Globalize.loadTranslations('ja', {nfbr: {global_api: {err_msg_404:"指定された書籍は閲覧できません。<br>書籍が存在しないか、公開されていないため、閲覧できません。"}}});
    Globalize.loadTranslations('en', {nfbr: {global_api: {err_msg_404:"The eBook chosen cannot open since it is not available or released."}}});
    Globalize.loadTranslations('zh-TW', {nfbr: {global_api: {err_msg_404:"您所選的書籍無法閱覽。<br>由於此書不存在或未公開，無法閱覽。"}}});
    Globalize.loadTranslations('ja', {nfbr: {global_api: {err_msg_503:"指定された書籍は現在閲覧できません。<br>サーバが混み合っているか、メンテナンス中のため、しばらく経ってから再度お試しください。"}}});
    Globalize.loadTranslations('en', {nfbr: {global_api: {err_msg_503:"The eBook chosen cannot be viewed due to heavy traffic or maintainance. Please try again after a while."}}});
    Globalize.loadTranslations('zh-TW', {nfbr: {global_api: {err_msg_503:"您所選的書籍無法閱覽。<br>伺服器可能過載或在維護中，請過一段時間後再重試。"}}});
    Globalize.loadTranslations('ja', {nfbr: {global_api: {err_msg_991:"指定された書籍は書庫に入っているため、閲覧できません。<br>閲覧するには書庫から取り出してください。"}}});
    Globalize.loadTranslations('en', {nfbr: {global_api: {err_msg_991:"The eBook chosen cannot open since it is archived. Please retrieve it from your archive."}}});
    Globalize.loadTranslations('zh-TW', {nfbr: {global_api: {err_msg_991:"error991"}}});
    Globalize.loadTranslations('ja', {nfbr: {global_api: {err_msg_992:"指定された書籍は削除されたため、閲覧できません。"}}});
    Globalize.loadTranslations('en', {nfbr: {global_api: {err_msg_992:"The eBook chosen cannot open since it dose not exist or is non-public."}}});
    Globalize.loadTranslations('zh-TW', {nfbr: {global_api: {err_msg_992:"error992"}}});
    Globalize.loadTranslations('ja', {nfbr: {global_api: {err_msg_993:"指定された書籍は現在閲覧できません。<br>（エラー993）"}}});
    Globalize.loadTranslations('en', {nfbr: {global_api: {err_msg_993:"The eBook chosen cannot open.<br>（ERROR993）"}}});
    Globalize.loadTranslations('zh-TW', {nfbr: {global_api: {err_msg_993:"error993"}}});
    Globalize.loadTranslations('ja', {nfbr: {global_api: {err_msg_994:"お使いのブラウザはサポートしていません。"}}});
    Globalize.loadTranslations('en', {nfbr: {global_api: {err_msg_994:"Sorry, but your browser is out of our support."}}});
    Globalize.loadTranslations('zh-TW', {nfbr: {global_api: {err_msg_994:"您使用的瀏覽器不支援此功能。"}}});
    Globalize.loadTranslations('ja', {nfbr: {global_api: {err_msg_995:"指定された書籍は現在閲覧できません。<br>しばらく経ってから再度お試しください。<br>（エラー995）"}}});
    Globalize.loadTranslations('en', {nfbr: {global_api: {err_msg_995:"The eBook chosen cannot open. Please try again after a while.<br>（ERROR995）"}}});
    Globalize.loadTranslations('zh-TW', {nfbr: {global_api: {err_msg_995:"您所選的書籍無法閱覽。<br>請過一段時間後再重試。<br>（ERROR 995）"}}});
    Globalize.loadTranslations('ja', {nfbr: {global_api: {err_msg_996:"指定された書籍はブラウザビューアで閲覧できません。"}}});
    Globalize.loadTranslations('en', {nfbr: {global_api: {err_msg_996:"The eBook chosen cannot open by browser viewer."}}});
    Globalize.loadTranslations('zh-TW', {nfbr: {global_api: {err_msg_996:"您所選的書籍無法在PC閱讀器觀看。"}}});
    Globalize.loadTranslations('ja', {nfbr: {global_api: {err_msg_997:"指定された書籍は閲覧できません。<br>閲覧期限が切れています。"}}});
    Globalize.loadTranslations('en', {nfbr: {global_api: {err_msg_997:"The eBook chosen cannot open since already passed display period."}}});
    Globalize.loadTranslations('zh-TW', {nfbr: {global_api: {err_msg_997:"您所選的書籍無法閱覽。<br>已超過閱覽期限。"}}});
    Globalize.loadTranslations('ja', {nfbr: {global_api: {err_msg_998:"指定された書籍は閲覧できません。<br>ログアウトを行い、再度ログインを行ってください。<br>（エラー998）"}}});
    Globalize.loadTranslations('en', {nfbr: {global_api: {err_msg_998:"The eBook chosen cannot be viewed. Please sign-out, then sign-in again.<br>（ERROR998）"}}});
    Globalize.loadTranslations('zh-TW', {nfbr: {global_api: {err_msg_998:"您所選的書籍無法閱覽。<br>請過一段時間後再重試。<br>（ERROR 998）"}}});
    Globalize.loadTranslations('ja', {nfbr: {global_api: {err_msg_999:"指定された書籍は現在閲覧できません。<br>しばらく経ってから再度お試しください。<br>（エラー999）"}}});
    Globalize.loadTranslations('en', {nfbr: {global_api: {err_msg_999:"The eBook chosen cannot be viewed. Please try again after a while.<br>（ERROR999）"}}});
    Globalize.loadTranslations('zh-TW', {nfbr: {global_api: {err_msg_999:"您所選的書籍無法閱覽。<br>請過一段時間後再重試。<br>（ERROR 999）"}}});
    NFBR.a0X.a3u='http://www.bookwalker.com.tw/';
    NFBR.a0X.a3U=true;
    NFBR.a0X.a4L='0.4';
    NFBR.a0X.a4N='0.35';
    NFBR.a0X.POST_HELP_URL='http://www.bookwalker.com.tw/explanation/problem';
    NFBR.a0X.VIEWER_LANDSCAPE_RATIO='0.8';
    NFBR.a0X.ADD_SUFFIX_TO_COVER_PAGE_ENABLED=true;
    NFBR.LocaleConfig.supportedLanguage=['ja','en','zh-TW'];
    NFBR.LocaleConfig.FAIL_SAFE_LOCALE='en';
    NFBR.Locale.setLocale(NFBR.LocaleConfig.DEFAULT_LOCALE);
    NFBR.a0X.SELECT_CHARACTER_ENABLED_DEFAULT=false;
    NFBR.a0X.EXTERNAL_SCRIPT = "";
    if (NFBR.a0X.EXTERNAL_SCRIPT) {
        var script = document.createElement("script");
        script.type = "text/javascript";
        script.src = NFBR.a0X.EXTERNAL_SCRIPT;
        document.getElementsByTagName("head")[0].appendChild(script);
    }
    NFBR.a0X.SHOW_SEARCH_BOX=false;
    NFBR.a0X.SEND_ERROR_INFO_URL='https://pcreader.bookwalker.com.tw/browserWebApi/error';
}).call(this);
