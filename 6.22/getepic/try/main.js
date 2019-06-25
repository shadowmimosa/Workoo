(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["main"],{

/***/ "./src/$$_lazy_route_resource lazy recursive":
/*!**********************************************************!*\
  !*** ./src/$$_lazy_route_resource lazy namespace object ***!
  \**********************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var map = {
	"./web-app/explore/explore.module": [
		"./src/app/web-app/explore/explore.module.ts",
		"web-app-explore-explore-module"
	]
};
function webpackAsyncContext(req) {
	var ids = map[req];
	if(!ids) {
		return Promise.resolve().then(function() {
			var e = new Error("Cannot find module '" + req + "'");
			e.code = 'MODULE_NOT_FOUND';
			throw e;
		});
	}
	return __webpack_require__.e(ids[1]).then(function() {
		var id = ids[0];
		return __webpack_require__(id);
	});
}
webpackAsyncContext.keys = function webpackAsyncContextKeys() {
	return Object.keys(map);
};
webpackAsyncContext.id = "./src/$$_lazy_route_resource lazy recursive";
module.exports = webpackAsyncContext;

/***/ }),

/***/ "./src/app/app-routing.module.ts":
/*!***************************************!*\
  !*** ./src/app/app-routing.module.ts ***!
  \***************************************/
/*! exports provided: Ng1Ng2UrlHandlingStrategy, AppRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Ng1Ng2UrlHandlingStrategy", function() { return Ng1Ng2UrlHandlingStrategy; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppRoutingModule", function() { return AppRoutingModule; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_test2_test2_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./shared/test2/test2.component */ "./src/app/shared/test2/test2.component.ts");
/* harmony import */ var _shared_page_not_found_page_not_found_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./shared/page-not-found/page-not-found.component */ "./src/app/shared/page-not-found/page-not-found.component.ts");
/* harmony import */ var _shared_empty_empty_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./shared/empty/empty.component */ "./src/app/shared/empty/empty.component.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};






var routes = [
    {
        path: 'explore',
        loadChildren: './web-app/explore/explore.module#ExploreModule',
        data: { title: 'Explore AppComponent' }
    },
    {
        path: 'test',
        component: _shared_test2_test2_component__WEBPACK_IMPORTED_MODULE_2__["Test2Component"],
        data: { title: 'Test AppComponent' }
    },
    {
        path: 'empty',
        component: _shared_empty_empty_component__WEBPACK_IMPORTED_MODULE_4__["EmptyComponent"],
    },
    {
        path: '',
        redirectTo: '',
        pathMatch: 'full'
    },
    {
        path: '**',
        component: _shared_page_not_found_page_not_found_component__WEBPACK_IMPORTED_MODULE_3__["PageNotFoundComponent"]
    }
];
var Ng1Ng2UrlHandlingStrategy = /** @class */ (function () {
    function Ng1Ng2UrlHandlingStrategy() {
    }
    Ng1Ng2UrlHandlingStrategy.prototype.shouldProcessUrl = function (url) {
        var routes = [
            '/explore',
            '/test',
            '/empty'
        ];
        return routes.includes(url.toString());
    };
    Ng1Ng2UrlHandlingStrategy.prototype.extract = function (url) {
        return url;
    };
    Ng1Ng2UrlHandlingStrategy.prototype.merge = function (url, whole) {
        return url;
    };
    return Ng1Ng2UrlHandlingStrategy;
}());

var AppRoutingModule = /** @class */ (function () {
    function AppRoutingModule() {
    }
    AppRoutingModule = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"])({
            imports: [
                _angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"].forRoot(routes, {
                    useHash: false,
                    initialNavigation: true,
                })
            ],
            declarations: [
                _shared_test2_test2_component__WEBPACK_IMPORTED_MODULE_2__["Test2Component"],
                _shared_page_not_found_page_not_found_component__WEBPACK_IMPORTED_MODULE_3__["PageNotFoundComponent"],
                _shared_empty_empty_component__WEBPACK_IMPORTED_MODULE_4__["EmptyComponent"]
            ],
            exports: [
                _angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"]
            ],
            providers: [
                {
                    provide: _angular_router__WEBPACK_IMPORTED_MODULE_1__["UrlHandlingStrategy"],
                    useClass: Ng1Ng2UrlHandlingStrategy
                }
            ]
        })
    ], AppRoutingModule);
    return AppRoutingModule;
}());



/***/ }),

/***/ "./src/app/app.component.html":
/*!************************************!*\
  !*** ./src/app/app.component.html ***!
  \************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n<router-outlet></router-outlet>"

/***/ }),

/***/ "./src/app/app.component.scss":
/*!************************************!*\
  !*** ./src/app/app.component.scss ***!
  \************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL2FwcC5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/app.component.ts":
/*!**********************************!*\
  !*** ./src/app/app.component.ts ***!
  \**********************************/
/*! exports provided: AppComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppComponent", function() { return AppComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var AppComponent = /** @class */ (function () {
    function AppComponent() {
    }
    AppComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-root',
            template: __webpack_require__(/*! ./app.component.html */ "./src/app/app.component.html"),
            styles: [__webpack_require__(/*! ./app.component.scss */ "./src/app/app.component.scss")]
        }),
        __metadata("design:paramtypes", [])
    ], AppComponent);
    return AppComponent;
}());



/***/ }),

/***/ "./src/app/app.module.ts":
/*!*******************************!*\
  !*** ./src/app/app.module.ts ***!
  \*******************************/
/*! exports provided: AppModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppModule", function() { return AppModule; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/platform-browser */ "./node_modules/@angular/platform-browser/fesm5/platform-browser.js");
/* harmony import */ var _angular_upgrade_static__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/upgrade/static */ "./node_modules/@angular/upgrade/fesm5/static.js");
/* harmony import */ var _app_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./app.component */ "./src/app/app.component.ts");
/* harmony import */ var _app_routing_module__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./app-routing.module */ "./src/app/app-routing.module.ts");
/* harmony import */ var _core_core_module__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./core/core.module */ "./src/app/core/core.module.ts");
/* harmony import */ var _service_bootstrap_service_bootstrap_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./service-bootstrap/service-bootstrap.component */ "./src/app/service-bootstrap/service-bootstrap.component.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};







var AppModule = /** @class */ (function () {
    function AppModule() {
    }
    AppModule.prototype.ngDoBootstrap = function () { };
    AppModule = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"])({
            imports: [_angular_platform_browser__WEBPACK_IMPORTED_MODULE_1__["BrowserModule"], _angular_upgrade_static__WEBPACK_IMPORTED_MODULE_2__["UpgradeModule"], _core_core_module__WEBPACK_IMPORTED_MODULE_5__["CoreModule"], _app_routing_module__WEBPACK_IMPORTED_MODULE_4__["AppRoutingModule"]],
            declarations: [_app_component__WEBPACK_IMPORTED_MODULE_3__["AppComponent"], _service_bootstrap_service_bootstrap_component__WEBPACK_IMPORTED_MODULE_6__["ServiceBootstrapComponent"]],
            providers: [_app_component__WEBPACK_IMPORTED_MODULE_3__["AppComponent"]],
            entryComponents: [_service_bootstrap_service_bootstrap_component__WEBPACK_IMPORTED_MODULE_6__["ServiceBootstrapComponent"]],
            bootstrap: [_app_component__WEBPACK_IMPORTED_MODULE_3__["AppComponent"]],
        }),
        __metadata("design:paramtypes", [])
    ], AppModule);
    return AppModule;
}());



/***/ }),

/***/ "./src/app/core/constants/EventConstants.ts":
/*!**************************************************!*\
  !*** ./src/app/core/constants/EventConstants.ts ***!
  \**************************************************/
/*! exports provided: EventConstants */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "EventConstants", function() { return EventConstants; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};

var EventConstants = /** @class */ (function () {
    function EventConstants() {
        // GENERAL GROUP OF EVENTS
        this.WEB_INITIALIZED = 'web_initialized';
        this.WEB_UNLOAD = 'web_unload';
        this.SEARCH_CONFIRMED = 'search_confirmed';
        this.SEARCH_FILTER_OPEN = 'search_filter_open';
        this.SEARCH_VOICE_ACTIVATED = 'search_voice_activated';
        this.SEARCH_SORT_CHANGED = 'search_sort_changed';
        this.SEARCH_SORT_ORDER_CHANGED = 'search_sort_order_changed';
        this.SEARCH_POPULAR = 'search_popular';
        this.SEARCH_MY_INTERESTS = 'search_my_interests';
        this.SEARCH_INTEREST = 'search_interest';
        this.SEARCH_TAB_SELECTED = 'search_tab_selected';
        this.SEARCH_CONTENT_OPENED = 'search_content_opened';
        this.SEARCH_LIST_VIEW = 'search_list_view';
        this.SEARCH_COVER_VIEW = 'search_cover_view';
        this.SEARCH_FILTER_SELECTED = 'search_filter_selected';
        // public readonly SEARCH_FILTER_SELECTED_AR: string = 'search_filter_selected_ar';
        // public readonly SEARCH_FILTER_SELECTED_AR_LEVEL: string = 'search_filter_selected_ar_level';
        // public readonly SEARCH_FILTER_SELECTED_FICTION: string = 'search_filter_selected_fiction';
        // public readonly SEARCH_FILTER_SELECTED_NON_FICTION: string = 'search_filter_selected_non_fiction';
        // public readonly SEARCH_FILTER_SELECTED_ENGLISH: string = 'search_filter_selected_english';
        // public readonly SEARCH_FILTER_SELECTED_SPANISH: string = 'search_filter_selected_spanish';
        // public readonly SEARCH_FILTER_SELECTED_CHINESE: string = 'search_filter_selected_chinese';
        // public readonly SEARCH_FILTER_SELECTED_QUIZ: string = 'search_filter_selected_quiz';
        // public readonly SEARCH_FILTER_SELECTED_NO_QUIZ: string = 'search_filter_selected_no_quiz';
        this.SEARCH_VIEW_CONVERSION_CHART = 'search_view_conversion_chart';
        this.BOOK_VIEW_CONVERSION_CHART = 'book_view_conversion_chart';
        this.BANNER_CLICKED = 'banner_pressed';
        this.CATEGORY_CHANGED = 'category_changed';
        this.PREFERENCES_CHANGED = 'preferences_changed';
        this.GOOGLE_CLASSROOM_SIGN_IN_START = 'google_classroom_sign_in_start';
        this.GOOGLE_CLASSROOM_SIGN_IN_COMPLETE = 'google_classroom_sign_in_complete';
        this.GOOGLE_CLASSROOM_SIGN_IN_FAILED = 'google_classroom_sign_in_failed';
        this.GOOGLE_CLASSROOM_IMPORT_COMPLETE = 'google_classroom_import_complete';
        this.ACCOUNT_CREATE = 'account_create';
        this.ACCOUNT_CREATE_WEBSITE = 'account_create_website';
        this.ACCOUNT_TRIAL_START = 'account_subscription_trial_start';
        this.ACCOUNT_SIGN_OUT = 'account_sign_out';
        this.CONTENT_OPENED_BOOK = 'content_opened_book';
        this.CONTENT_OPENED_BOOK_R2ME = 'content_opened_book_r2me';
        this.CONTENT_OPENED_AUDIOBOOK = 'content_opened_audiobook';
        this.CONTENT_OPENED_VIDEO = 'content_opened_video';
        this.CONTENT_OPENED_ORIGINALS_COLLECTION = 'content_opened_originals_collection';
        this.CONTENT_PAID_BOOK = 'content_paid_book';
        this.CONTENT_PAID_BOOK_R2ME = 'content_paid_book_r2me';
        this.CONTENT_FAVORITE = 'content_favorite';
        this.CONTENT_FINISH_ENABLED_BOOK = 'content_finish_enabled_book';
        this.CONTENT_FINISH_ENABLED_BOOK_R2ME = 'content_finish_enabled_book_r2me';
        this.CONTENT_FINISH_BOOK = 'content_finished_book';
        this.CONTENT_FINISH_BOOK_R2ME = 'content_finished_book_r2me';
        this.CONTENT_FINISH_AUDIOBOOK = 'content_finished_audiobook';
        this.CONTENT_FINISH_VIDEO = 'content_finished_video';
        this.CONTENT_FINISH_CLICK_BOOK = 'content_finish_click_book';
        this.CONTENT_FINISH_CLICK_BOOK_R2ME = 'content_finish_click_book_r2me';
        this.CONTENT_FINISH_VIEW_BOOK = 'content_finish_view_book';
        this.CONTENT_FINISH_VIEW_BOOK_R2ME = 'content_finish_view_book_r2me';
        this.CONTENT_CLOSED_BOOK = 'content_closed_book';
        this.CONTENT_CLOSED_BOOK_R2ME = 'content_closed_book_r2me';
        this.CONTENT_CLOSED_VIDEO = 'content_closed_video';
        this.CONTENT_CLOSED_AUDIOBOOK = 'content_closed_audiobook';
        this.CONTENT_AUTOPLAY_AUDIOBOOK = 'content_autoplay_audio';
        this.CONTENT_AUTOPLAY_VIDEO = 'content_autoplay_video';
        this.CONTENT_ZOOM_IN = 'content_zoom_in';
        this.CONTENT_ZOOM_OUT = 'content_zoom_out';
        this.CONTENT_FULL_SCREEN_IN = 'content_full_screen_in';
        this.CONTENT_FULL_SCREEN_OUT = 'content_full_screen_in_out';
        this.CONTENT_READTOME_PLAY = 'content_play_book_r2me';
        this.CONTENT_READTOME_PAUSE = 'content_pause_book_r2me';
        this.BOOK_AUTHOR_SEARCH_CLICK = 'book_author_search_click';
        this.BOOK_ILLUSTRATOR_SEARCH_CLICK = 'book_illustrator_search_click';
        this.CONTENT_SCRUB = 'content_scrub';
        this.BROWSE_SHUFFLE_PRESSED = 'browse_shuffle_pressed';
        this.READING_LOG_VIEW = 'reading_log_view';
        this.READING_LOG_CHANGE_DURATION = 'reading_log_change_duration';
        this.SUBSCRIBE_BLOCKER = 'subscribe_blocker';
        this.SUBSCRIBE_OVERLAY = 'subscribe_overlay';
        this.SUBSCRIBE_OVERLAY_PURCHASE_START = 'subscribe_purchase_start';
        this.SUBSCRIBE_OVERLAY_PURCHASE_SUCCEED = 'subscribe_purchase_succeed';
        this.SUBSCRIBE_OVERLAY_PROMO = 'subscribe_overlay_promo';
        this.SUBSCRIBE_OVERLAY_PURCHASE_PROMO_SUCCEED = 'subscribe_purchase_promo_succeed';
        this.SUBSCRIBE_PURCHASE_FAIL = 'subscribe_purchase_fail';
        this.SUBSCRIBE_WEBSITE = 'subscribe_website';
        this.SUBSCRIBE_OVERLAY_PROMO_CLICK = 'subscribe_overlay_promo_click';
        this.SUBSCRIBE_OVERLAY_SUCCESS_VIEW = 'subscribe_overlay_success_view';
        this.SUBSCRIBE_OVERLAY_SUCCESS_CLOSE = 'subscribe_overlay_success_close';
        this.NAVIGATION_BROWSE = 'navigation_browse';
        this.NAVIGATION_LIBRARY = 'navigation_library';
        this.NAVIGATION_MAILBOX = 'navigation_mailbox';
        this.NAVIGATION_SETTINGS = 'navigation_settings';
        this.NAVIGATION_SEARCH = 'navigation_search';
        this.NAVIGATION_PROFILE = 'navigation_profile';
        this.NAVIGATION_DASHBOARD = 'navigation_dashboard';
        this.NAVIGATION_ROSTER = 'navigation_roster';
        this.NAVIGATION_ACTIVITIES = 'navigation_activities';
        this.NUF_LOAD = 'nuf_load';
        this.NUF_COMPLETE = 'nuf_complete';
        // These are appended with _start and _complete
        this.NUF_STEP_ACCOUNT_TYPE = 'nuf_step_account_type';
        this.NUF_STEP_ACCOUNT_CREATE = 'nuf_step_account_create';
        this.NUF_STEP_EDUCATOR_WELCOME = 'nuf_step_educator_welcome';
        this.NUF_STEP_AGE = 'nuf_step_age';
        this.NUF_STEP_PROFILE_SUBJECTS = 'nuf_step_subjects';
        this.NUF_STEP_PROFILE_CREATE_START = 'nuf_step_profile_create_start';
        this.NUF_STEF_PROFILE_CREATE_COMPLETE = 'nuf_step_profile_create_complete';
        // Track are for a/b test interests
        this.NEW_INTEREST_VIEW = 'new_interest_view';
        this.NEW_INTEREST_CONTENT_OPEN = 'new_interest_content_open';
        // Steps not available on the web..
        // public readonly NUF_STEP_EDU_PERSONAL_INFO: string = "nuf_step_edu_personal_info";
        // public readonly NUF_STEP_EDU_SCHOOL_INFO: string = "nuf_step_edu_school_info";
        // public readonly NUF_STEP_EDU_SHARE: string = "nuf_step_edu_share";
        // public readonly NUF_STEP_PROFILE_CREATE: string = "nuf_step_profile_create";
        // public readonly NUF_ADD_PROFILE_MODAL_START: string = "nuf_add_profile_modal_start";
        // public readonly NUF_ADD_PROFILE_MODAL_SELECT_ADD: string = "nuf_add_profile_modal_select_add";
        // public readonly NUF_ADD_PROFILE_MODAL_SELECT_FINISH: string = "nuf_add_profile_modal_select_finish";
        this.NUF_STEP_EDU_PERSONAL_INFO = 'nuf_step_edu_personal_info';
        this.NUF_STEP_EDU_ADD_STUDENT = 'nuf_step_edu_add_student';
        this.NUF_STEP_EDU_ADD_STUDENT_SKIP = 'nuf_step_edu_add_student_skip';
        this.NUF_STEP_EDU_ADD_STUDENT_WHY_PARENTS = 'nuf_step_edu_add_student_why_parents';
        this.NUF_STEP_EDU_ADD_STUDENT_ADD = 'nuf_step_edu_add_student_add';
        this.NUF_STEP_EDU_ADD_STUDENT_CONFIRM_VIEW = 'nuf_step_edu_add_student_confirm_view';
        this.NUF_STEP_EDU_ADD_STUDENT_NAME_SWAP = 'nuf_step_edu_add_student_name_swap';
        this.NUF_STEP_EDU_ADD_STUDENT_SUCCESS = 'nuf_step_edu_add_student_success';
        // public readonly SUBSCRIBE_PURCHASE_CANCEL: string = "subscribe_purchase_cancel";
        this.TEXT_HIGHLIGHT_TOGGLED = 'text_highlight_toggled';
        this.TEXT_HIGHLIGHT_WORD_PRESSED = 'text_highlight_word_pressed';
        this.TEXT_HIGHLIGHT_DEFINITION_NOT_FOUND = 'text_highlight_definition_not_found';
        this.BLOCKED_WEB_MOBILE = 'blocked_web_mobile';
        this.CONSOLE_ERRORS = 'console_errors';
        this.SWITCH_TO_PARENT = 'account_switch_to_parent';
        this.ACCOUNT_SETTINGS = 'account_settings';
        this.MANAGE_ACCOUNT_STATUS = 'account_manage_status';
        this.ACCOUNT_DISABLE_AUTO_RENEW = 'account_disable_auto_renew';
        this.ACCOUNT_ENABLE_AUTO_RENEW = 'account_enable_auto_renew';
        this.ACCOUNT_SUBSCRIPTION_CANCEL = 'account_subscription_cancel';
        this.ACCOUNT_SUBSCRIPTION_CONTINUE = 'account_subscription_continue';
        this.ACCOUNT_SUBSCRIPTION_CONTINUE_EXIT = 'account_subscription_continue_exit';
        this.ACCOUNT_SUBSCRIPTION_CONTINUE_AGAIN = 'account_subscription_continue_again';
        this.ACCOUNT_SUBSCRIPTION_CHANGE_MIND = 'account_subscription_change_mind';
        this.ACCOUNT_SUBSCRIPTION_CANCEL_REASON = 'account_subscription_cancel_reason';
        this.ACCOUNT_SUBSCRIPTION_CANCEL_REASON_CHANGE_MIND = 'account_subscription_cancel_reason_change_mind';
        this.PROFILE_SELECT_VIEW = 'profile_select_view';
        this.PROFILE_SELECTED = 'profile_selected';
        this.PROFILE_SELECT_ADD = 'profile_select_add';
        this.PROFILE_SELECT_PARENT_DASHBOARD = 'profile_select_parent_dashboard';
        this.PROFILE_SELECT_PARENT_PASSWORD_CORRECT = 'profile_select_parent_password_correct';
        this.PROFILE_SELECT_PARENT_PASSWORD_INCORRECT = 'profile_select_parent_password_incorrect';
        this.PROFILE_SELECT_SIGNOUT = 'profile_select_signout';
        this.PROFILE_SELECT_MY_PROFILE_EXISTS = 'profile_select_my_profile_exists';
        this.MENU_VIEW = 'menu_view';
        this.MENU_VIEW_PROFILE = 'menu_view_profile';
        this.MENU_SWITCH_TO_CHILD = 'menu_switch_to_child';
        this.MENU_SWITCH_TO_PARENT = 'menu_switch_to_parent';
        this.MENU_ADD_PROFILE = 'menu_add_profile';
        this.MENU_SIGNOUT = 'menu_signout';
        this.ACCOUNT_MANAGE_LOAD = 'account_manage_load';
        this.EDU_ACTIVITIES_STUDENT_LOG = 'edu_activities_student_log';
        this.EDU_ACTIVITIES_CLASS_SUMMARY = 'edu_activities_class_summary';
        this.EDU_ACTIVITIES_CLASS_ASSIGNMENTS = 'edu_activities_class_assignments';
        this.EDU_ACTIVITIES_CLASS_QUIZ = 'edu_activities_class_quiz';
        this.EDU_ACTIVITIES_ASSIGNMENTS_SEARCH = 'edu_activities_assignments_search';
        this.EDU_ACTIVITIES_ASSIGNMENTS_EXPLORE = 'edu_activities_assignments_explore';
        this.EDU_ACTIVITIES_ASSIGNMENTS_VIEW = 'edu_activities_assignments_view';
        this.EDU_ACTIVITIES_ASSIGNMENTS_ASSIGN = 'edu_activities_assignments_assign';
        this.EDU_ACTIVITIES_QUIZ_SEARCH = 'edu_activities_quiz_search';
        this.EDU_ACTIVITIES_QUIZ_EXPLORE = 'edu_activities_quiz_explore';
        this.EDU_ACTIVITIES_QUIZ_OPTION = 'edu_activities_quiz_option';
        this.EDU_ACTIVITIES_QUIZ_OPTION_CLICK = 'edu_activities_quiz_option_click';
        // TEACHER OFFER EVENTS FOR ABTEST
        this.TEACHER_OFFER_VIEWED = 'teacher_offer_viewed';
        this.TEACHER_OFFER_CREATE_ACCOUNT_VIEWED = 'teacher_offer_create_account_viewed';
        this.TEACHER_OFFER_PAYMENT_DETAILS_VIEWED = 'teacher_offer_payment_details_viewed';
        this.TEACHER_OFFER_PAYMENT_SUCCESS_VIEWED = 'teacher_offer_payment_success_viewed';
        this.EDU_ROSTER_GOOGLE_CLASSROOM = 'edu_roster_google_classroom';
        this.EDU_ROSTER_GOOGLE_CLASSROOM_SUCCESS = 'edu_roster_google_classroom_success';
        this.EDU_ROSTER_ADD_STUDENT_START = 'edu_roster_add_student_start';
        this.EDU_ROSTER_ADD_STUDENT_ADD = 'edu_roster_add_student_add';
        this.EDU_ROSTER_ADD_STUDENT_CONFIRM_VIEW = 'edu_roster_add_student_confirm_view';
        this.EDU_ROSTER_ADD_STUDENT_NAME_SWAP = 'edu_roster_add_student_name_swap';
        this.EDU_ROSTER_ADD_STUDENT_SUCCESS = 'edu_roster_add_student_success';
        this.EDU_ROSTER_DROP_STUDENT_SUCCESS = 'edu_roster_drop_student_success';
        this.EDU_ROSTER_CREATE_GROUP_SUCCESS = 'edu_roster_create_group_success';
        this.EDU_ROSTER_DELETE_GROUP_SUCCESS = 'edu_roster_delete_group_success';
        this.EDU_ROSTER_TRANSFER_ATTEMPT = 'edu_roster_transfer_attempt';
        this.EDU_ROSTER_TRANSFER_SUCCESS = 'edu_roster_transfer_success';
        this.EDU_ROSTER_ARCHIVE_STUDENT = 'edu_roster_archive_student';
        this.EDU_ROSTER_ADD_STUDENT_TO_GROUP = 'edu_roster_add_student_to_group';
        this.EDU_ROSTER_STUDENT_LOGIN = 'edu_roster_student_login';
        this.EDU_ROSTER_SHARE = 'edu_roster_share';
        this.EDU_ROSTER_FREE = 'edu_roster_free';
        this.EDU_ROSTER_FREE_ENROLL = 'edu_roster_free_enroll';
        this.EDU_ROSTER_FREE_REDEEM = 'edu_roster_free_redeem';
        this.EDU_ROSTER_VIEW = 'edu_roster_view';
        this.EDU_ROSTER_ADD_EMAIL_CLICK = 'edu_roster_add_email_click';
        this.EDU_ROSTER_EMAIL_EDIT = 'edu_roster_email_edit';
        this.EDU_ROSTER_ADD_EMAIL_HOME_ACCESS_CLICK = 'edu_roster_add_email_home_access_click';
        this.EDU_ROSTER_ADD_EMAIL_SEND = 'edu_roster_add_email_send';
        this.EDU_ROSTER_ADD_EMAIL_RESEND = 'edu_roster_add_email_resend';
        this.EDU_ROSTER_MP_EMAIL_ENABLE_HOME_ACCESS = 'edu_roster_mp_email_enable_home_access';
        // EDU DASHBOARD
        this.EDU_DASHBOARD_VIEW = 'edu_dashboard_view';
        this.EDU_DASHBOARD_CLICK_ROSTER = 'edu_dashboard_click_roster';
        this.EDU_DASHBOARD_CLICK_EXPLORE = 'edu_dashboard_click_explore';
        this.EDU_DASHBOARD_CLICK_ASSIGN = 'edu_dashboard_click_assign';
        this.EDU_DASHBOARD_CLICK_QUIZ = 'edu_dashboard_click_quiz';
        this.EDU_DASHBOARD_CLICK_EXPLORE_VIDEO_ON = 'edu_dashboard_click_explore_video_on';
        this.EDU_DASHBOARD_CLICK_EXPLORE_VIDEO_OFF = 'edu_dashboard_click_explore_video_off';
        this.EDU_DASHBOARD_CLICK_DOWNLOAD_IOS = 'edu_dashboard_click_download_ios';
        this.EDU_DASHBOARD_CLICK_DOWNLOAD_ANDROID = 'edu_dashboard_click_download_android';
        this.EDU_DASHBOARD_CLICK_WEB_LOGIN = 'edu_dashboard_click_web_login';
        this.EDU_DASHBOARD_CLICK_CALENDAR = 'edu_dashboard_click_calendar';
        this.EDU_DASHBOARD_CLICK_RESOURCE_QUICK_START = 'edu_dashboard_click_resource_quick_start';
        this.EDU_DASHBOARD_CLICK_RESOURCE_FLYER = 'edu_dashboard_click_resource_flyer';
        this.EDU_DASHBOARD_CLICK_RESOURCE_DECORATIONS = 'edu_dashboard_click_resource_decorations';
        this.EDU_DASHBOARD_CLICK_RESOURCE_LESSON_PLANS = 'edu_dashboard_click_resource_lesson_plans';
        this.EDU_DASHBOARD_CLICK_RESOURCE_COLLEAGUE_PRESENTATION = 'edu_dashboard_click_resource_colleague_presentation';
        this.EDU_DASHBOARD_CLICK_RESOURCE_NO_ONE_TO_ONE = 'edu_dashboard_click_resource_no_one_to_one';
        this.EDU_DASHBOARD_CLICK_RESOURCE_BTS_NIGHT = 'edu_dashboard_click_resource_bts_night';
        this.EDU_DASHBOARD_CLICK_RESOURCE_EDUCATORS_HANDBOOK = 'edu_dashboard_click_resource_educators_handbook';
        this.EDU_DASHBOARD_CLICK_SEND_EMAIL = 'edu_dashboard_click_send_email';
        this.EDU_DASHBOARD_CLICK_LETTER = 'edu_dashboard_click_letter';
        this.EDU_DASHBOARD_CLICK_TEXT_MESSAGE = 'edu_dashboard_click_text_message';
        this.EDU_DASHBOARD_CLICK_MORE_LANGUAGE_INFO = 'edu_dashboard_click_more_language_info';
        this.EDU_DASHBOARD_HOME_ACCESS_EXPLAINER_VIEW = 'edu_dashboard_home_access_explainer_view';
        this.EDU_DASHBOARD_HOME_ACCESS_EXPLAINER_CLICK = 'edu_dashboard_home_access_explainer_click';
        this.EDU_DASHBOARD_HOME_ACCESS_EMAIL_VIEW = 'edu_dashboard_home_access_email_view';
        this.EDU_DASHBOARD_HOME_ACCESS_EMAIL_SEND = 'edu_dashboard_home_access_email_send';
        this.EDU_DASHBOARD_CLICK_HOME_ACCESS_EMAIL = 'edu_dashboard_click_home_access_email';
        this.EDU_DASHBOARD_VIEW_ACTIVE_USER = 'edu_dashboard_view_active_user';
        this.EDU_DASHBOARD_VIEW_NEW_USER = 'edu_dashboard_view_new_user';
        // EDU DASHBOARD SUMMER PROMO
        this.EDU_DASH_SUMMER2019_VIEWBANNER = 'edu_dash_summer2019_viewbanner';
        this.EDU_DASH_SUMMER2019_VIEWPOPUP = 'edu_dash_summer2019_viewpopup';
        this.EDU_DASH_SUMMER2019_CLICKFLYER = 'edu_dash_summer2019_clickflyer';
        this.EDU_DASH_SUMMER2019_CLICKBLURB = 'edu_dash_summer2019_clickblurb';
        this.EDU_DASH_SUMMER2019_VIEW2TEMAIL = 'edu_dash_summer2019_viewt2temail';
        this.EDU_DASH_SUMMER2019_SEND2TEMAIL = 'edu_dash_summer2019_sendt2temail';
        // Manhattan Project (removal)
        this.MANHATTAN_REDIRECT_PAGE_VIEW = 'manhattan_redirect_page_view';
        // Edu-resources
        this.SITE_EDU_RESOURCES_SEE_ALL_RESOURCES = 'site_edu_resources_see_all_resources';
        this.SITE_EDU_RESOURCES_CLICK_CALENDAR = 'site_edu_resources_click_calendar';
        this.SITE_EDU_RESOURCES_CLICK_RESOURCE_QUICK_START = 'site_edu_resources_click_resource_quick_start';
        this.SITE_EDU_RESOURCES_CLICK_RESOURCE_FLYER = 'site_edu_resources_click_resource_flyer';
        this.SITE_EDU_RESOURCES_CLICK_RESOURCE_DECORATIONS = 'site_edu_resources_click_resource_decorations';
        this.SITE_EDU_RESOURCES_CLICK_RESOURCE_LESSON_PLANS = 'site_edu_resources_click_resource_lesson_plans';
        this.SITE_EDU_RESOURCES_CLICK_RESOURCE_BTS_NIGHT = 'site_edu_resources_click_resource_bts_night';
        this.SITE_EDU_RESOURCES_CLICK_RESOURCE_COLLEAGUE_PRESENTATION = 'site_edu_resources_click_resource_colleague_presentation';
        this.SITE_EDU_RESOURCES_CLICK_RESOURCE_FAMILY_LETTER_ENGLISH = 'site_edu_resources_click_resource_family_letter_english';
        this.SITE_EDU_RESOURCES_CLICK_RESOURCE_FAMILY_LETTER_SPANISH = 'site_edu_resources_click_resource_family_letter_spanish';
        this.SITE_EDU_RESOURCES_CLICK_FULLGUIDE = 'site_edu_resources_click_fullguide';
        this.SITE_EDU_RESOURCES_CONTENT_COLLECTION_LOAD_MORE = 'site_edu_resources_content_collection_load_more';
        this.SITE_EDU_RESOURCES_READERPILLAR_DOWNLOAD = 'site_edu_resources_readerpillar_download';
        this.SITE_EDU_RESOURCES_ECR_GET_STARTED = 'site_edu_resources_ecr_get_started';
        this.SITE_EDU_RESOURCES_GET_SWAG = 'site_edu_resources_get_swag';
        this.SITE_EDU_RESOURCES_GET_HELP = 'site_edu_resources_get_help';
        this.SITE_EDU_RESOURCES_CLASSROOM_READING_CHALLENGE = 'site_edu_resources_classroom_reading_challenge';
        this.SITE_EDU_RESOURCES_VIDEO_TUTORIALS = 'site_edu_resources_video_tutorials';
        this.SITE_EDU_RESOURCES_WATCH_VIDEO = 'site_edu_resources_watch_video';
        this.SITE_EDU_RESOURCES_CONTENT_COLLECTION = 'site_edu_resources_content_collection';
        this.NUF_CONNECT_VIEW = 'nuf_connect_view';
        this.NUF_CONNECT_SKIP = 'nuf_connect_skip';
        // public readonly NUF_CONNECT_CLASS_CODE_SUBMIT: string = 'nuf_connect_class_code_submit';
        this.NUF_CONNECT_TEACHER_SEARCH_SUBMIT = 'nuf_connect_teacher_search_submit';
        this.NUF_CONNECT_CLASS_CODE_FAIL = 'nuf_connect_class_code_fail';
        this.NUF_CONNECT_CLASS_CODE_SUCCESS = 'nuf_connect_class_code_success';
        // public readonly NUF_CONNECT_EMAIL_SUBMIT: string = 'nuf_connect_email_submit';
        this.NUF_CONNECT_EMAIL_FAIL = 'nuf_connect_email_fail';
        this.NUF_CONNECT_EMAIL_SUCCESS = 'nuf_connect_email_success';
        this.NUF_CONNECT_CHILD_SEARCH_START = 'nuf_connect_child_search_start';
        this.NUF_CONNECT_CHILD_SEARCH_SUCCESS = 'nuf_connect_child_search_success';
        this.NUF_CONNECT_CHILD_SEARCH_FAIL = 'nuf_connect_child_search_fail';
        this.NUF_CONNECT_CHILD_SEARCH_ADD_STUDENT = 'nuf_connect_child_search_add_student';
        this.NUF_CONNECT_ADD_CHILD_VIEW = 'nuf_connect_add_child_view';
        this.NUF_CONNECT_ADD_CHILD_SUBMIT = 'nuf_connect_add_child_submit';
        this.NUF_CONNECT_ADD_CHILD_FAIL = 'nuf_connect_add_child_fail';
        this.NUF_CONNECT_ADD_CHILD_SUCCESS = 'nuf_connect_add_child_success';
        this.NUF_CONNECT_CONGRATS_VIEW = 'nuf_connect_congrats_view';
        this.NUF_CONNECT_CONGRATS_SUBMIT = 'nuf_connect_congrats_submit';
        // event for when profile is not connected or subbed
        this.AFTER_HOURS_BLOCK_VIEW = 'after_hours_block_view';
        // event for when profile is not connected or subbed
        this.AFTER_HOURS_GET_STARTED = 'after_hours_get_started';
        // profile is connected but not subbed
        this.AFTER_HOURS_SUBSCRIBE_PROMPT_POPUP = 'after_hours_subscribe_prompt_popup';
        // profile is connected but not subbed
        this.AFTER_HOURS_SUBSCRIBE_POPUP = 'after_hours_subscribe_popup';
        // profile is connected but not subbed
        this.AFTER_HOURS_SUBSCRIBE_SUCCESS = 'after_hours_subscribe_success';
        this.COLLECTION_START_CONTENT = 'collection_start_content';
        this.COLLECTION_START_SEARCH_ONE = 'collection_start_search_one';
        this.COLLECTION_START_SEARCH_BULK = 'collection_start_search_bulk';
        this.COLLECTION_ADD_TO_VIEW = 'collection_add_to_view';
        this.COLLECTION_ADD_TO_CLOSE = 'collection_add_to_close';
        this.COLLECTION_ADD_TO_FINISH = 'collection_add_to_finish';
        this.COLLECTION_CREATE_NEW = 'collection_create_new';
        this.COLLECTION_CREATE_NEW_CLOSE = 'collection_create_new_close';
        this.COLLECTION_CREATE_NEW_FINISH = 'collection_create_new_finish';
        this.COLLECTION_ASSIGN_CLICK = 'collection_assign_click';
        this.COLLECTION_ASSIGN_VIEW = 'collection_assign_view';
        this.COLLECTION_ASSIGN_GROUP_CHANGE = 'collection_assign_group_change';
        this.COLLECTION_ASSIGN_SELECT_ALL = 'collection_assign_select_all';
        this.COLLECTION_ASSIGN_FINISH = 'collection_assign_finish';
        this.COLLECTION_VIEW = 'collection_view';
        this.COLLECTION_LIKE = 'collection_like';
        this.COLLECTION_FAVORITE = 'collection_favorite';
        this.COLLECTION_EDIT = 'collection_edit';
        this.COLLECTION_EDIT_CLOSE = 'collection_edit_close';
        this.COLLECTION_EDIT_SAVE = 'collection_edit_save';
        this.COLLECTION_COPY_COLLECTION = 'collection_copy_collection';
        this.COLLECTION_COPY_COLLECTION_SAVE = 'collection_copy_collection_save';
        this.COLLECTION_ASSIGN = 'collection_assign';
        this.COLLECTION_SHARE = 'collection_share';
        this.COLLECTION_SHARE_EPIC_TEACHER = 'collection_share_epic_teacher';
        this.COLLECTION_SHARE_EPIC_TEACHER_SEND = 'collection_share_epic_teacher_send';
        this.COLLECTION_SHARE_EMAIL = 'collection_share_email';
        this.COLLECTION_SHARE_EMAIL_SEND = 'collection_share_email_send';
        this.COLLECTION_SHARE_PINTEREST = 'collection_share_pinterest';
        this.COLLECTION_SHARE_COPY_LINK = 'collection_share_copy_link';
        this.COLLECTION_SHARE_COPY_LINK_COPY = 'collection_share_copy_link_copy';
        this.FAVORITE_CLICK = 'favorite_click';
        this.SAVED_MY_LIBRARY_VIEW = 'saved_my_library_view';
        this.SAVED_MY_LIBRARY_COMPLETE = 'saved_my_library_complete';
        this.SAVE_TO_MY_LIBRARY_CREATE_NEW = 'save_to_my_library_crete_new';
        this.SAVE_TO_MY_LIBRARY_CREATE_NEW_CANCEL = 'save_to_my_library_crete_new_cancel';
        this.SAVE_TO_MY_LIBRARY_CREATE_NEW_SAVE = 'save_to_my_library_crete_new_save';
        this.MY_LIBRARY_FAVORITES_VIEW = 'my_library_favorites_view';
        this.MY_LIBRARY_COLLECTIONS_VIEW = 'my_library_collections_view';
        this.MY_LIBRARY_RECENTS_VIEW = 'my_library_recents_view';
        this.ASSIGN_ADD_STUDENT_VIEW = 'assign_add_student_view';
        this.ASSIGN_ADD_STUDENT_SELECT = 'assign_add_student_select';
        this.ASSIGN_ADD_STUDENT_SUCCESS_GOOGLE = 'assign_add_student_success_google';
        // public readonly ASSIGN_ADD_STUDENT_CONFIRM_VIEW: string = 'assign_add_student_confirm_view';
        // public readonly ASSIGN_ADD_STUDENT_SUCCESS_ROSTER: string = 'assign_add_student_success_roster';
        this.ASSIGN_ADD_STUDENT_START = 'assign_add_student_start';
        this.ASSIGN_ADD_STUDENT_ADD = 'assign_add_student_add';
        this.ASSIGN_ADD_STUDENT_CONFIRM_VIEW = 'assign_add_student_confirm_view';
        this.ASSIGN_ADD_STUDENT_NAME_SWAP = 'assign_add_student_name_swap';
        this.ASSIGN_ADD_STUDENT_SUCCESS = 'assign_add_student_success';
        this.CONTENT_ASSIGN_ADD_STUDENTS = 'content_assign_add_students';
        this.CONTENT_ASSIGN_STUDENTS_SEARCH = 'content_assign_students_search';
        this.EDU_DASHBOARD_READERPILLAR = 'edu_dashboard_readerpillar';
        this.READERPILLAR_VIEW = 'readerpillar_view';
        this.READERPILLAR_DOWNLOAD = 'readerpillar_download';
        this.READERPILLAR_BADGE_DOWNLOAD = 'readerpillar_badge_download';
        this.READERPILLAR_ACTIVITIES = 'readerpillar_activities';
        this.TAB_RIGHT_PRESSED = 'tab_right_pressed';
        this.TAB_LEFT_PRESSED = 'tab_left_pressed';
        // Experiment for educators that create a profile after clicking on experimental educator cta on /promo
        this.ACCOUNT_CREATE_FORM_VIEWED_WEBSITE = 'account_create_form_viewed_website';
        this.EDU_SWITCH_CTA_CLICKED = 'edu_switch_cta_clicked';
        // Events for Involuntary Churn Experiment V1 - Mar29, 2019
        this.INV_CHURN_SIGN_IN = 'inv_churn_sign_in';
        this.INV_CHURN_SEE_UPDATE_FIELDS = 'inv_churn_see_update_fields';
        this.INV_CHURN_CLICK_UPDATE_FIELDS = 'inv_churn_click_update_fields';
        this.INV_CHURN_UPDATE_SUCCESS = 'inv_churn_update_success';
        // Cancel flow AB Test Events - Apr12, 2019
        this.ACCOUNT_SUBSCRIPTION_CANCEL_FINAL_VIEW = 'account_subscription_cancel_final_view';
        this.ACCOUNT_SUBSCRIPTION_CANCEL_FINAL_STAY = 'account_subscription_cancel_final_stay';
        this.ACCOUNT_SUBSCRIPTION_CANCEL_REASON_VIEW = 'account_subscription_cancel_reason_view';
        this.ACCOUNT_SUBSCRIPTION_CANCEL_REASON_SUBMIT = 'account_subscription_cancel_reason_submit';
        this.SELECT_PAY_METHOD_CC_CARD = 'select_pay_method_cc_card';
        this.SELECT_PAY_METHOD_APPLE = 'select_pay_method_apple';
        this.SELECT_PAY_METHOD_APPLE_FAILED = 'select_pay_method_apple_failed';
        this.SELECT_PAY_METHOD_APPLE_CLOSED = 'select_pay_method_closed';
        this.SELECT_PAY_METHOD_APPLE_SUCCESS = 'select_pay_method_apple_success';
        this.SELECT_PAY_OPTIONS_VIEW = 'select_pay_options_view';
        this.SELECT_PAY_METHOD_APPLE_SUBMIT = 'select_pay_method_apple_submit'; // log when user submits payment info to get stripe token back via apple pay
        this.SELECT_PAY_METHOD_APPLE_FAIL = 'select_pay_method_apple_fail'; // just add product id parameter to and replace existing log
        this.SELECT_PAY_METHOD_CREDIT_SUBMIT = 'select_pay_method_credit_submit'; // logs on Get Started button press
        this.SELECT_PAY_METHOD_CREDIT_SUCCESS = 'select_pay_method_credit_success'; // logs on Get Started success return
        this.SELECT_PAY_METHOD_CREDIT_FAIL = 'select_pay_method_credit_fail'; // logs on Get Started fail return
        this.PAGE_VIEWED = 'page_viewed';
        // Events for Edu Explore V1
        this.EXPLORE_BY_GRADE_OPEN = 'explore_by_grade_open';
        this.EXPLORE_BY_GRADE_CHANGE = 'explore_by_grade_change';
        this.EXPLORE_BY_RL_OPEN = 'explore_by_rl_open';
        this.EXPLORE_BY_RL_CHANGE = 'explore_by_rl_change';
        this.EXPLORE_SELECT_RL_VIEW = 'explore_select_rl_view';
        this.EXPLORE_SELECT_RL_SELECTED = 'explore_select_rl_selected';
        this.TAB_READING_LEVEL_VIEW = 'tab_reading_level_view';
        this.BLOCKED_WEB_MOBILE_DOWNLOAD_APP = 'blocked_web_mobile_download_app';
        this.BLOCKED_WEB_MOBILE_ACCOUNT_MANAGE = 'blocked_web_mobile_account_manage';
        this.BLOCKED_WEB_MOBILE_SUPPORT = 'blocked_web_mobile_support';
        this.BLOCKED_WEB_MOBILE_OPEN_MENU = 'blocked_web_mobile_open_menu';
        this.BLOCKED_WEB_MOBILE_MENU_PARENT = 'blocked_web_mobile_menu_parent';
        this.BLOCKED_WEB_MOBILE_MENU_EDU = 'blocked_web_mobile_menu_edu';
        this.BLOCKED_WEB_MOBILE_MENU_GIFT = 'blocked_web_mobile_menu_gift';
        this.BLOCKED_WEB_MOBILE_MENU_GET_STARTED = 'blocked_web_mobile_menu_get_started';
        this.BLOCKED_WEB_MOBILE_MENU_SIGN_IN = 'blocked_web_mobile_menu_sign_in';
    }
    EventConstants = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root',
        })
    ], EventConstants);
    return EventConstants;
}());



/***/ }),

/***/ "./src/app/core/constants/PerformanceEventConstants.ts":
/*!*************************************************************!*\
  !*** ./src/app/core/constants/PerformanceEventConstants.ts ***!
  \*************************************************************/
/*! exports provided: PerformanceEventConstants */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PerformanceEventConstants", function() { return PerformanceEventConstants; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};

var PerformanceEventConstants = /** @class */ (function () {
    function PerformanceEventConstants() {
        this.APP_BUNDLE_ID_STRING = '/public/app/js/bundle.js';
        this.PERFORMANCE_OVER_TIME_ERROR = 'performance_over_time_error';
        this.PERFORMANCE_APP_LAUNCH_COMPLETE = 'performance_app_launch_complete';
        this.PERFORMANCE_SEARCH_RESULTS_LOADED = 'performance_search_results_loaded';
        this.PERFORMANCE_USER_CHANGE_COMPLETE = 'performance_user_change_complete';
        this.PERFORMANCE_BROWSE_CONTENT_LOADED = 'performance_browse_content_loaded';
        this.PERFORMANCE_CREATE_ACCOUNT = 'performance_create_account';
        this.PERFORMANCE_BUNDLE_DOWNLOAD = 'performance_bundle_download';
        this.PERFORMANCE_TTI = 'performance_tti';
        //// state change
        // site
        this.STATE_CHANGE_HOME_TO_PROMO = 'state_change_home_to_promo';
        this.STATE_CHANGE_HOME_TO_GIFT = 'state_change_home_to_gift';
        // app
        this.STATE_CHANGE_PROFILE_SELECT_TO_EXPLORE = 'state_change_profile_select_to_explore';
        this.STATE_CHANGE_EXPLORE_TO_SEARCH = 'state_change_explore_to_search';
        this.STATE_CHANGE_SEARCH_TO_EXPLORE = 'state_change_search_to_explore';
    }
    PerformanceEventConstants = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        })
    ], PerformanceEventConstants);
    return PerformanceEventConstants;
}());



/***/ }),

/***/ "./src/app/core/core.module.ts":
/*!*************************************!*\
  !*** ./src/app/core/core.module.ts ***!
  \*************************************/
/*! exports provided: CoreModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CoreModule", function() { return CoreModule; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");
/* harmony import */ var _module_import_guard__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./module-import-guard */ "./src/app/core/module-import-guard.ts");
/* harmony import */ var _services_captcha_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./services/captcha.service */ "./src/app/core/services/captcha.service.ts");
/* harmony import */ var _services_tax_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./services/tax.service */ "./src/app/core/services/tax.service.ts");
/* harmony import */ var _services_data_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./services/data.service */ "./src/app/core/services/data.service.ts");
/* harmony import */ var _services_message_handler_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./services/message-handler.service */ "./src/app/core/services/message-handler.service.ts");
/* harmony import */ var _services_account_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./services/account.service */ "./src/app/core/services/account.service.ts");
/* harmony import */ var _services_window_ref_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./services/window-ref.service */ "./src/app/core/services/window-ref.service.ts");
/* harmony import */ var _services_session_storage_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./services/session-storage.service */ "./src/app/core/services/session-storage.service.ts");
/* harmony import */ var _services_local_storage_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./services/local-storage.service */ "./src/app/core/services/local-storage.service.ts");
/* harmony import */ var _services_string_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./services/string.service */ "./src/app/core/services/string.service.ts");
/* harmony import */ var _services_logsly_service__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./services/logsly.service */ "./src/app/core/services/logsly.service.ts");
/* harmony import */ var _services_after_hours_service__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./services/after-hours.service */ "./src/app/core/services/after-hours.service.ts");
/* harmony import */ var _services_promo_service__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./services/promo.service */ "./src/app/core/services/promo.service.ts");
/* harmony import */ var _services_big_query_service__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @services/big-query.service */ "./src/app/core/services/big-query.service.ts");
/* harmony import */ var _services_sign_in_service__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./services/sign-in.service */ "./src/app/core/services/sign-in.service.ts");
/* harmony import */ var _services_user_agent_service__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! ./services/user-agent.service */ "./src/app/core/services/user-agent.service.ts");
/* harmony import */ var _services_query_string_service__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @services/query-string.service */ "./src/app/core/services/query-string.service.ts");
/* harmony import */ var _services_angularjs_translator_service__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @services/angularjs-translator.service */ "./src/app/core/services/angularjs-translator.service.ts");
/* harmony import */ var _services_gift_service__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! @services/gift.service */ "./src/app/core/services/gift.service.ts");
/* harmony import */ var _services_logging_source_translation_service__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! @services/logging-source-translation.service */ "./src/app/core/services/logging-source-translation.service.ts");
/* harmony import */ var _services_subscription_service__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! @services/subscription.service */ "./src/app/core/services/subscription.service.ts");
/* harmony import */ var _services_redirect_service__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! @services/redirect.service */ "./src/app/core/services/redirect.service.ts");
/* harmony import */ var _services_erc_books_read_service__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(/*! @services/erc-books-read.service */ "./src/app/core/services/erc-books-read.service.ts");
/* harmony import */ var _services_profile_service__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__(/*! @services/profile.service */ "./src/app/core/services/profile.service.ts");
/* harmony import */ var _directives_enter_directive__WEBPACK_IMPORTED_MODULE_26__ = __webpack_require__(/*! ./directives/enter.directive */ "./src/app/core/directives/enter.directive.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (undefined && undefined.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};

























// import { Profile } from '@models/profile/Profile';


var CoreModule = /** @class */ (function () {
    function CoreModule(parentModule) {
        Object(_module_import_guard__WEBPACK_IMPORTED_MODULE_2__["throwIfAlreadyLoaded"])(parentModule, 'CoreModule');
    }
    CoreModule = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"])({
            imports: [_angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpClientModule"]],
            providers: [
                _services_captcha_service__WEBPACK_IMPORTED_MODULE_3__["CaptchaService"],
                _services_tax_service__WEBPACK_IMPORTED_MODULE_4__["TaxService"],
                _services_data_service__WEBPACK_IMPORTED_MODULE_5__["DataService"],
                _services_message_handler_service__WEBPACK_IMPORTED_MODULE_6__["MessageHandlerService"],
                _services_account_service__WEBPACK_IMPORTED_MODULE_7__["AccountService"],
                _services_window_ref_service__WEBPACK_IMPORTED_MODULE_8__["WindowRefService"],
                _services_session_storage_service__WEBPACK_IMPORTED_MODULE_9__["SessionStorageService"],
                _services_local_storage_service__WEBPACK_IMPORTED_MODULE_10__["LocalStorageService"],
                _services_string_service__WEBPACK_IMPORTED_MODULE_11__["StringService"],
                _services_logsly_service__WEBPACK_IMPORTED_MODULE_12__["LogslyService"],
                _services_after_hours_service__WEBPACK_IMPORTED_MODULE_13__["AfterHoursService"],
                _services_query_string_service__WEBPACK_IMPORTED_MODULE_18__["QueryStringService"],
                _services_user_agent_service__WEBPACK_IMPORTED_MODULE_17__["UserAgentService"],
                _services_promo_service__WEBPACK_IMPORTED_MODULE_14__["PromoService"],
                _services_profile_service__WEBPACK_IMPORTED_MODULE_25__["ProfileService"],
                _services_sign_in_service__WEBPACK_IMPORTED_MODULE_16__["SignInService"],
                _services_big_query_service__WEBPACK_IMPORTED_MODULE_15__["BigQueryService"],
                _services_angularjs_translator_service__WEBPACK_IMPORTED_MODULE_19__["AngularjsTranslatorService"],
                _services_gift_service__WEBPACK_IMPORTED_MODULE_20__["GiftService"],
                _services_logging_source_translation_service__WEBPACK_IMPORTED_MODULE_21__["LoggingSourceTranslationService"],
                _services_subscription_service__WEBPACK_IMPORTED_MODULE_22__["SubscriptionService"],
                _services_redirect_service__WEBPACK_IMPORTED_MODULE_23__["RedirectService"],
                _services_erc_books_read_service__WEBPACK_IMPORTED_MODULE_24__["ErcBooksReadService"],
            ],
            declarations: [_directives_enter_directive__WEBPACK_IMPORTED_MODULE_26__["EnterDirective"]],
        }),
        __param(0, Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Optional"])()), __param(0, Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["SkipSelf"])()),
        __metadata("design:paramtypes", [CoreModule])
    ], CoreModule);
    return CoreModule;
}());



/***/ }),

/***/ "./src/app/core/directives/enter.directive.ts":
/*!****************************************************!*\
  !*** ./src/app/core/directives/enter.directive.ts ***!
  \****************************************************/
/*! exports provided: EnterDirective */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "EnterDirective", function() { return EnterDirective; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var EnterDirective = /** @class */ (function () {
    function EnterDirective() {
    }
    EnterDirective = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"])({
            selector: '[appEnter]'
        }),
        __metadata("design:paramtypes", [])
    ], EnterDirective);
    return EnterDirective;
}());



/***/ }),

/***/ "./src/app/core/models/account-model.ts":
/*!**********************************************!*\
  !*** ./src/app/core/models/account-model.ts ***!
  \**********************************************/
/*! exports provided: AccountModel */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AccountModel", function() { return AccountModel; });
var AccountModel = /** @class */ (function () {
    function AccountModel() {
        this.email = '';
        this.password = '';
        this.transferProfileId = '';
        this.captchaToken = '';
    }
    AccountModel.prototype.clearData = function () {
        this.email = '';
        this.password = '';
        this.transferProfileId = '';
        this.captchaToken = '';
    };
    ;
    AccountModel.prototype.getJSONFormattedData = function () {
        return JSON.stringify({
            email: this.email,
            password: this.password,
            transferProfileId: this.transferProfileId,
            captchaToken: this.captchaToken
        });
    };
    ;
    AccountModel.prototype.emailError = function () {
        if (!this.validateEmail(this.email)) {
            return "Please enter a valid email address.";
        }
        return false;
    };
    ;
    AccountModel.prototype.passwordError = function () {
        if (this.password == '') {
            return 'Please enter a password.';
        }
        else if (this.password.length < 6) {
            return 'Your password must be at least 6 characters.';
        }
        return false;
    };
    ;
    AccountModel.prototype.accountInfoValid = function () {
        return (!this.emailError() &&
            !this.passwordError());
    };
    ;
    AccountModel.prototype.validateEmail = function (email) {
        var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    };
    return AccountModel;
}());



/***/ }),

/***/ "./src/app/core/models/product.ts":
/*!****************************************!*\
  !*** ./src/app/core/models/product.ts ***!
  \****************************************/
/*! exports provided: Product */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Product", function() { return Product; });
var Product = /** @class */ (function () {
    function Product(data) {
        data = data || {};
        this.id = data.id;
        this.productId = data.product_id;
        this.price = data.price / 100;
        this.name = data.name;
        this.recurring = data.recurring;
        this.months = data.months;
        this.strikethrough_price = data.strikethrough_price;
        this.default_free_trial_length = data.default_free_trial_length;
        var strikethroughHTML = null;
        if (this.strikethrough_price) {
            strikethroughHTML = "<span class=\"textDecoration-linethrough\">$" + this
                .strikethrough_price / 100 + "</span>";
        }
        var desc = data.description &&
            data.description.replace(/PRICE/g, String(this.price));
        desc = desc.replace(/MONTHS/g, String(this.months));
        desc = desc.replace(/EXPIRATION/g, this.getFormattedExpDate());
        if (strikethroughHTML) {
            desc = desc.replace(/STRIKE/g, strikethroughHTML);
        }
        this.description = desc;
    }
    Product.prototype.getFormattedExpDate = function () {
        if (!this.months) {
            return "";
        }
        var date = new Date();
        date.setMonth(date.getMonth() + this.months);
        return (date.getMonth() +
            1 +
            "/" +
            date.getDate() +
            "/" +
            date.getFullYear());
    };
    return Product;
}());



/***/ }),

/***/ "./src/app/core/models/profile/ChildProfile.ts":
/*!*****************************************************!*\
  !*** ./src/app/core/models/profile/ChildProfile.ts ***!
  \*****************************************************/
/*! exports provided: ChildProfile */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ChildProfile", function() { return ChildProfile; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _Profile__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Profile */ "./src/app/core/models/profile/Profile.ts");
var __extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


var ChildProfile = /** @class */ (function (_super) {
    __extends(ChildProfile, _super);
    function ChildProfile(profileData) {
        return _super.call(this, profileData) || this;
    }
    ChildProfile_1 = ChildProfile;
    ChildProfile.prototype.getDefaultState = function () {
        if (!this.nufComplete) {
            return 'personalizeAge'; // First step for profile customization
        }
        return 'browse';
    };
    ChildProfile.prototype.setProfileData = function (profileData) {
        _super.prototype.setProfileData.call(this, profileData);
        if (profileData.hasOwnProperty('email'))
            this.email = profileData.email;
        if (profileData.hasOwnProperty('pin'))
            this.pin = profileData.pin;
        if (profileData.hasOwnProperty('name'))
            this.name = (this.firstName && this.lastName) ? this.firstName + ' ' + this.lastName.substring(0, 1) + '.' : (profileData.name && profileData.name.length > 0) ? profileData.name : 'New Profile';
    };
    /**
     * Reconstruct the profile with fresh data
     * @param profileData
     */
    ChildProfile.prototype.setAllProfileData = function (profileData) {
        _super.prototype.setAllProfileData.call(this, profileData);
        this.email = profileData.email || '';
        this.homeAccessStatus = profileData.homeAccessStatus;
        this.pin = profileData.pin || null;
        this.userAccountTransfer = profileData.userAccountTransfer || [];
        this.pendingAccountLink = [];
        this.approvedAccountLink = [];
        this.name = (this.firstName && this.lastName) ? this.firstName + ' ' + this.lastName.substring(0, 1) + '.' : (profileData.name && profileData.name.length > 0) ? profileData.name : 'New Profile';
        // Already filtered links data
        if (profileData.pendingAccountLink && profileData.approvedAccountLink) {
            this.pendingAccountLink = profileData.pendingAccountLink || [];
            this.approvedAccountLink = profileData.approvedAccountLink || [];
        }
        else { // Else filter userAccountLink into pending and approved (data returned from api)
            if (!profileData.userAccountLink)
                return;
            var link;
            for (var i = 0; i < profileData.userAccountLink.length; i++) {
                link = profileData.userAccountLink[i];
                if (!link)
                    continue;
                if (link.status === ChildProfile_1.linkStatus.ACCOUNT_USER_LINK_PENDING) {
                    this.pendingAccountLink.push(link);
                }
                else if (link.status === ChildProfile_1.linkStatus.ACCOUNT_USER_LINK_APPROVED) {
                    this.approvedAccountLink.push(link);
                }
            }
        }
        this.userType = (this.accountType === 1) ? 'student' : 'child';
        this.isParent = false;
    };
    /**
     * @returns boolean If user has any transfers/links (pending or not)
     */
    ChildProfile.prototype.hasLinksOrTransfer = function () {
        return this.userAccountTransfer.length > 0 || this.pendingAccountLink.length > 0 ||
            this.approvedAccountLink.length > 0;
    };
    /**
     * Checks if the profile is owned by the given account id
     *
     * @returns boolean True if the account owns this profile;
     *                  False otherwise
     */
    ChildProfile.prototype.isOwnedByAccountId = function (accountId) {
        return this.accountId == accountId;
    };
    ;
    /**
     * Function to check if this profile has any pending link or
     * transfer states
     *
     * @returns boolean True if there is a pending status;
     *                  False otherwise
     */
    ChildProfile.prototype.isProfilePendingApproval = function () {
        return this.hasPendingLink() || this.isProfilePendingTransfer();
    };
    /**
     * Function to determine if this profile has
     * pending linkages
     *
     * @returns boolean True if the profile has at least 1 pending link
     *                  False otherwise
     */
    ChildProfile.prototype.hasPendingLink = function () {
        return this.pendingAccountLink.length > 0;
    };
    ;
    /**
     * Function to check if this profile is pending transfer
     *
     * @returns boolean True if there is a pending transfer;
     *                  False otherwise
     */
    ChildProfile.prototype.isProfilePendingTransfer = function () {
        return this.userAccountTransfer.length > 0 && this.userAccountTransfer[0].status == ChildProfile_1.transferStatus.ACCOUNT_USER_TRANSFER_PENDING;
    };
    ;
    /**
     * Function to determine if the profile has any approved links
     *
     * @returns boolean True if there is at least 1 approved links;
     *                  False otherwise
     */
    ChildProfile.prototype.hasApprovedLinks = function () {
        return this.approvedAccountLink.length > 0;
    };
    ;
    /**
     * Deprecated from mp, leaving here in case we ever bring back mp
     * Function to determine if the profile has opted in through mp
     *
     * @returns boolean True if opted in to progress emails
     *                  False otherwise
     */
    ChildProfile.prototype.hasOptInLink = function () {
        // return this.userProgressEmail && this.userProgressEmail.optInStatus;
    };
    ;
    /**
     * Function to check if profile is approved for home access
     *
     * @returns boolean True if there is a home acccess approved link
     */
    ChildProfile.prototype.isApprovedForHomeAccess = function () {
        return this.hasApprovedLinks() && this.approvedAccountLink[0].type === ChildProfile_1.linkStatus.ACCOUNT_USER_LINK_TYPE_HOME;
    };
    ;
    /**
     * Function to retrieve the pending transfer
     *
     * @returns TransferDO Transfer data object;
     *          NULL if no object found
     */
    ChildProfile.prototype.getPendingTransfer = function () {
        if (!this.isProfilePendingTransfer()) {
            return null;
        }
        return this.userAccountTransfer[0];
    };
    ;
    /**
     * Function to retrieve the pending link
     *
     * @returns LinkDO Link data object;
     *          NULL if no object found
     */
    ChildProfile.prototype.getPendingLink = function () {
        if (!this.hasPendingLink()) {
            return null;
        }
        return this.pendingAccountLink[0];
    };
    ;
    /**
     * Function to retrieve the approved link
     *
     * @returns LinkDO Link data object;
     *          NULL if no object found
     */
    ChildProfile.prototype.getApprovedLink = function () {
        if (!this.hasApprovedLinks()) {
            return null;
        }
        return this.approvedAccountLink[0];
    };
    ;
    /**
     * Function to determine if a profile is
     * available for linkage
     *
     * @returns boolean True if the profile can be linked;
     *                  False otherwise
     */
    ChildProfile.prototype.isAvailableForLink = function () {
        return !this.hasApprovedLinks() && !this.hasPendingLink();
    };
    ;
    var ChildProfile_1;
    ChildProfile = ChildProfile_1 = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [Object])
    ], ChildProfile);
    return ChildProfile;
}(_Profile__WEBPACK_IMPORTED_MODULE_1__["Profile"]));



/***/ }),

/***/ "./src/app/core/models/profile/EducatorProfile.ts":
/*!********************************************************!*\
  !*** ./src/app/core/models/profile/EducatorProfile.ts ***!
  \********************************************************/
/*! exports provided: EducatorProfile */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "EducatorProfile", function() { return EducatorProfile; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _ParentProfile__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./ParentProfile */ "./src/app/core/models/profile/ParentProfile.ts");
var __extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


var EducatorProfile = /** @class */ (function (_super) {
    __extends(EducatorProfile, _super);
    function EducatorProfile(profileData) {
        return _super.call(this, profileData) || this;
    }
    EducatorProfile.prototype.getDefaultState = function () {
        return 'edu-dashboard';
    };
    EducatorProfile.prototype.setProfileData = function (profileData) {
        _super.prototype.setProfileData.call(this, profileData);
        if (profileData.hasOwnProperty('educatorPrefix'))
            this.educatorPrefix = profileData.educatorPrefix;
        if (profileData.hasOwnProperty('name'))
            this.name = (this.lastName) ? this.educatorPrefix + ' ' + this.lastName : (profileData.name && profileData.name.length > 0) ? profileData.name : 'New Profile';
    };
    EducatorProfile.prototype.setAllProfileData = function (profileData) {
        _super.prototype.setAllProfileData.call(this, profileData);
        this.educatorPrefix = profileData.educatorPrefix;
        this.onboardingComplete = profileData.onboardingComplete;
        this.name = (this.lastName) ? this.educatorPrefix + ' ' + this.lastName : (profileData.name && profileData.name.length > 0) ? profileData.name : 'New Profile';
        this.userType = 'teacher';
    };
    EducatorProfile = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [Object])
    ], EducatorProfile);
    return EducatorProfile;
}(_ParentProfile__WEBPACK_IMPORTED_MODULE_1__["ParentProfile"]));



/***/ }),

/***/ "./src/app/core/models/profile/ParentProfile.ts":
/*!******************************************************!*\
  !*** ./src/app/core/models/profile/ParentProfile.ts ***!
  \******************************************************/
/*! exports provided: ParentProfile */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ParentProfile", function() { return ParentProfile; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _Profile__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Profile */ "./src/app/core/models/profile/Profile.ts");
var __extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


var ParentProfile = /** @class */ (function (_super) {
    __extends(ParentProfile, _super);
    function ParentProfile(profileData) {
        return _super.call(this, profileData) || this;
        // this.name = (profileData.name && profileData.name.length > 0) ? profileData.name : 'New Profile';
        // this.userType = 'parent';
        // this.isParent = true;
    }
    ParentProfile.prototype.getDefaultState = function () {
        return 'profile';
    };
    ParentProfile.prototype.setAllProfileData = function (profileData) {
        _super.prototype.setAllProfileData.call(this, profileData);
        this.userType = 'parent';
        this.isParent = true;
    };
    ParentProfile = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [Object])
    ], ParentProfile);
    return ParentProfile;
}(_Profile__WEBPACK_IMPORTED_MODULE_1__["Profile"]));



/***/ }),

/***/ "./src/app/core/models/profile/Profile.ts":
/*!************************************************!*\
  !*** ./src/app/core/models/profile/Profile.ts ***!
  \************************************************/
/*! exports provided: Profile */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Profile", function() { return Profile; });
var Profile = /** @class */ (function () {
    function Profile(profileData) {
        this.setAllProfileData(profileData);
    }
    Profile.prototype.getFullName = function () {
        if (this.isDefault && this.firstName.toLowerCase() === 'guest') {
            return 'Guest Student';
        }
        if (this.firstName && this.lastName) {
            return this.firstName + ' ' + this.lastName;
        }
        else if (this.name) {
            return this.name;
        }
        else {
            return 'New Profile';
        }
    };
    Profile.prototype.getDefaultState = function () {
        return 'browse';
    };
    /**
     * Reconstruct the profile with fresh data
     * @param profileData
     */
    Profile.prototype.setAllProfileData = function (profileData) {
        this.id = profileData.id || 0;
        this.accountId = profileData.accountId || 0;
        this.accountType = profileData.accountType; // 1 for educator
        this.age = profileData.age || null;
        this.userId = profileData.userId;
        this.firstName = profileData.firstName || '';
        this.lastName = profileData.lastName || '';
        this.grade = (profileData.grade) ? profileData.grade : ((profileData.grade === 0) ? 0 : null);
        this.avatar = profileData.avatar || 15;
        this.journalFrameImage = this.frame = profileData.journalFrameImage || 1;
        this.avatarFrame = profileData.avatarFrame || 5;
        // this.isParent = data.isParent;
        this.isDefault = profileData.isDefault || 0;
        this.themeId = profileData.themeId || 0;
        this.xp = profileData.xp || 0;
        this.xpLevel = profileData.xpLevel || 1;
        this.dateCreated = profileData.dateCreated;
        this.dateModified = profileData.dateModified || 0;
        this.nufComplete = profileData.nufComplete || 0;
        this.validSub = profileData.validSub || false;
        this.paidSub = profileData.paidSub || false;
        // Stats for profile
        this.avgScore = profileData.avgScore || 0;
        this.booksFinished = profileData.booksFinished || 0;
        this.videosWatched = profileData.videosWatched || 0;
        this.lastActive = profileData.lastActive || 0;
        this.numAssignments = profileData.numAssignments || 0;
        this.readTime = profileData.readTime || 0;
        this.startingAge = profileData.startingAge || 0;
        this.readingAge = profileData.readingAge || 0;
        this.name = (profileData.name && profileData.name.length > 0) ? profileData.name : 'New Profile';
        this.isParent = profileData.isParent;
        this.userType = (this.accountType === 1) ? ((this.isParent) ? 'teacher' : 'student') : ((this.isParent) ? 'parent' : 'child');
        this.readingLevelSystem = profileData.accountReadingLevelSystem ? profileData.accountReadingLevelSystem.type : '';
    };
    /**
     * User customizable properties
     * @param profileData
     */
    Profile.prototype.setProfileData = function (profileData) {
        if (profileData.hasOwnProperty('age')) {
            this.age = profileData.age;
        }
        if (profileData.hasOwnProperty('name')) {
            this.name = (profileData.name && profileData.name.length > 0) ? profileData.name : 'New Profile';
        }
        if (profileData.hasOwnProperty('firstName')) {
            this.firstName = profileData.firstName || '';
        }
        if (profileData.hasOwnProperty('lastName')) {
            this.lastName = profileData.lastName || '';
        }
        if (profileData.hasOwnProperty('grade')) {
            this.grade = (profileData.grade) ? profileData.grade : ((profileData.grade === 0) ? 0 : null);
        }
        if (profileData.hasOwnProperty('avatar')) {
            this.avatar = profileData.avatar || 15;
        }
        if (profileData.hasOwnProperty('journalFrameImage')) {
            this.journalFrameImage = this.frame = profileData.journalFrameImage || 1;
        }
        if (profileData.hasOwnProperty('avatarFrame')) {
            this.avatarFrame = profileData.avatarFrame || 5;
        }
        if (profileData.hasOwnProperty('themeId')) {
            this.themeId = profileData.themeId || 0;
        }
        if (profileData.hasOwnProperty('readingLevelSystem')) {
            this.readingLevelSystem = profileData.readingLevelSystem;
        }
    };
    Profile.prototype.setProfileStats = function (profileStats) {
        this.booksFinished = profileStats.booksFinished;
        this.readTime = profileStats.readTime;
        this.videosWatched = profileStats.videosWatched;
        this.lastActive = profileStats.lastActive;
        this.numAssignments = profileStats.numAssignments;
        this.avgScore = profileStats.avgScore;
    };
    Profile.prototype.setReadingLevelSystem = function (system) {
        this.readingLevelSystem = system;
    };
    Profile.linkStatus = {
        ACCOUNT_USER_LINK_PENDING: 0,
        ACCOUNT_USER_LINK_APPROVED: 1,
        ACCOUNT_USER_LINK_TYPE_HOME: 0,
        ACCOUNT_USER_LINK_TYPE_OTHERS: 1
    };
    Profile.transferStatus = {
        ACCOUNT_USER_TRANSFER_TYPE_OTHER: 0,
        ACCOUNT_USER_TRANSFER_TYPE_HOME: 1,
        ACCOUNT_USER_TRANSFER_PENDING: 0
    };
    return Profile;
}());



/***/ }),

/***/ "./src/app/core/models/promo.ts":
/*!**************************************!*\
  !*** ./src/app/core/models/promo.ts ***!
  \**************************************/
/*! exports provided: Promo */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Promo", function() { return Promo; });
/* harmony import */ var _product__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./product */ "./src/app/core/models/product.ts");

var Promo = /** @class */ (function () {
    function Promo(data) {
        this.promoCodeStatus = data.promoCodeStatus;
        this.promoCodeLongDescription = data.promoCodeLongDescription;
        this.promoCodeValid = data.promoCodeValid;
        this.skipCreditCard = !!parseInt(data.promoSkipCreditCard);
        this.recurring = !!parseInt(data.productRecurring);
        this.productId = data.productId;
        this.product = data.product ? new _product__WEBPACK_IMPORTED_MODULE_0__["Product"](data.product) : undefined;
        this.promoCodeDuration = this.convertUnixTimetoMonths(data.promoCodeDuration);
    }
    Promo.prototype.convertUnixTimetoMonths = function (duration) {
        return Math.floor((duration / (60 * 60 * 24)) / 30); // seconds / (seconds * minutes * hours) = days / 30 = months
    };
    ;
    Promo.prototype.isValid = function () {
        return this.promoCodeValid;
    };
    ;
    return Promo;
}());



/***/ }),

/***/ "./src/app/core/models/subscription-model.ts":
/*!***************************************************!*\
  !*** ./src/app/core/models/subscription-model.ts ***!
  \***************************************************/
/*! exports provided: SubscriptionModel */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SubscriptionModel", function() { return SubscriptionModel; });
var SubscriptionModel = /** @class */ (function () {
    function SubscriptionModel(product) {
        this.email = '';
        this.promoCode = '';
        this.firstName = '';
        this.lastName = '';
        this.accountSource = '';
        this.productId = '';
        this.stripeToken = null;
        this.captchaToken = null;
        this.subPaymentType = null;
        this.initialProduct = product;
        this.product = product;
        this.productId = product.productId;
    }
    SubscriptionModel.prototype.clearData = function () {
        this.email = '';
        this.promoCode = '';
        this.firstName = '';
        this.lastName = '';
        this.accountSource = '';
        this.productId = '';
        this.stripeToken = null;
        this.captchaToken = null;
        this.subPaymentType = null;
    };
    ;
    SubscriptionModel.prototype.setPromoCode = function (promoCode) {
        this.promoCode = promoCode || '';
    };
    ;
    SubscriptionModel.prototype.clearPromoCode = function () {
        this.promoCode = '';
    };
    SubscriptionModel.prototype.setProduct = function (product) {
        this.product = product || this.initialProduct;
        this.productId = this.product.productId;
    };
    ;
    SubscriptionModel.prototype.setAccountSource = function (accountSource) {
        this.accountSource = accountSource;
    };
    SubscriptionModel.prototype.getJSONFormattedData = function () {
        return JSON.stringify({
            email: this.email,
            promoCode: this.promoCode,
            productId: this.productId,
            stripeToken: this.stripeToken,
            captchaToken: this.captchaToken,
            firstName: this.firstName,
            lastName: this.lastName,
            accountSource: this.accountSource,
            subPaymentType: this.subPaymentType
        });
    };
    ;
    SubscriptionModel.prototype.firstNameError = function () {
        return (this.firstName == '') ? 'Please enter your first name' : false;
    };
    ;
    SubscriptionModel.prototype.lastNameError = function () {
        return (this.lastName == '') ? 'Please enter your last name' : false;
    };
    ;
    SubscriptionModel.prototype.setEmail = function (email) {
        this.email = email;
        return;
    };
    ;
    SubscriptionModel.prototype.subValid = function () {
        return (!this.firstNameError() &&
            !this.lastNameError() &&
            this.product);
    };
    ;
    SubscriptionModel.prototype.updateValid = function () {
        return this.product;
    };
    ;
    return SubscriptionModel;
}());



/***/ }),

/***/ "./src/app/core/models/temp-factories.ts":
/*!***********************************************!*\
  !*** ./src/app/core/models/temp-factories.ts ***!
  \***********************************************/
/*! exports provided: AccountModelFactory, SubscriptionModelFactory, ProductFactory, PromoFactory */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AccountModelFactory", function() { return AccountModelFactory; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SubscriptionModelFactory", function() { return SubscriptionModelFactory; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProductFactory", function() { return ProductFactory; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PromoFactory", function() { return PromoFactory; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _account_model__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./account-model */ "./src/app/core/models/account-model.ts");
/* harmony import */ var _subscription_model__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./subscription-model */ "./src/app/core/models/subscription-model.ts");
/* harmony import */ var _product__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./product */ "./src/app/core/models/product.ts");
/* harmony import */ var _promo__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./promo */ "./src/app/core/models/promo.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};





var AccountModelFactory = /** @class */ (function () {
    function AccountModelFactory() {
        return _account_model__WEBPACK_IMPORTED_MODULE_1__["AccountModel"];
    }
    AccountModelFactory = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [])
    ], AccountModelFactory);
    return AccountModelFactory;
}());

var SubscriptionModelFactory = /** @class */ (function () {
    function SubscriptionModelFactory() {
        return _subscription_model__WEBPACK_IMPORTED_MODULE_2__["SubscriptionModel"];
    }
    SubscriptionModelFactory = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [])
    ], SubscriptionModelFactory);
    return SubscriptionModelFactory;
}());

var ProductFactory = /** @class */ (function () {
    function ProductFactory() {
        return _product__WEBPACK_IMPORTED_MODULE_3__["Product"];
    }
    ProductFactory = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [])
    ], ProductFactory);
    return ProductFactory;
}());

var PromoFactory = /** @class */ (function () {
    function PromoFactory() {
        return _promo__WEBPACK_IMPORTED_MODULE_4__["Promo"];
    }
    PromoFactory = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [])
    ], PromoFactory);
    return PromoFactory;
}());



/***/ }),

/***/ "./src/app/core/module-import-guard.ts":
/*!*********************************************!*\
  !*** ./src/app/core/module-import-guard.ts ***!
  \*********************************************/
/*! exports provided: throwIfAlreadyLoaded */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "throwIfAlreadyLoaded", function() { return throwIfAlreadyLoaded; });
function throwIfAlreadyLoaded(parentModule, moduleName) {
    if (parentModule) {
        throw new Error(moduleName + " has already been loaded. Import Core modules in the AppModule only.");
    }
}


/***/ }),

/***/ "./src/app/core/services/abtest.service.ts":
/*!*************************************************!*\
  !*** ./src/app/core/services/abtest.service.ts ***!
  \*************************************************/
/*! exports provided: ABTestService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ABTestService", function() { return ABTestService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _services_data_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @services/data.service */ "./src/app/core/services/data.service.ts");
/* harmony import */ var _services_profile_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @services/profile.service */ "./src/app/core/services/profile.service.ts");
/* harmony import */ var _services_account_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @services/account.service */ "./src/app/core/services/account.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};




var ABTestService = /** @class */ (function () {
    function ABTestService(data, profileService, accountService) {
        this.data = data;
        this.profileService = profileService;
        this.accountService = accountService;
        // {user: {userId: {expLabel: {Experimentdata}}, ...}, account: {accountId: {expLabel: {Experimentdata}}, ...}}
        this.experiments = { user: {}, account: {} };
        this.SELECT_PROFILE_POPUP = 'select-profile-popup';
        this.SELECT_PROFILE_POPUP_CONTROL = 'select-profile-popup-control';
        this.SELECT_PROFILE_POPUP_EXPERIMENT = 'select-profile-popup-experiment';
        this.TEACHER_OFFER = 'teacher-offer';
        this.TEACHER_OFFER_CONTROL = 'teacher-offer-control';
        this.TEACHER_OFFER_EXPERIMENT = 'teacher-offer-experiment';
        this.PROMO_PAGE = 'promo-page';
        this.PROMO_PAGE_CONTROL = 'promo-page-control';
        this.PROMO_PAGE_EXPERIMENT = 'promo-page-experiment';
        this.UPDATE_PAYMENT = 'update-payment';
        this.UPDATE_PAYMENT_CONTROL = 'update-payment-control';
        this.UPDATE_PAYMENT_EXPERIMENT = 'update-payment-experiment';
        this.MOBILE_PAYMENT_OPTIONS_LAYOUT = 'mobile-payment-options-layout';
        this.MOBILE_PAYMENT_OPTIONS_LAYOUT_CONTROL = 'mobile-payment-options-layout-control';
        this.MOBILE_PAYMENT_OPTIONS_LAYOUT_COPY_CHANGE = 'mobile-payment-options-layout-copy-change';
        this.MOBILE_PAYMENT_OPTIONS_LAYOUT_TOP = 'mobile-payment-options-layout-top';
        this.MOBILE_PAYMENT_OPTIONS_LAYOUT_BOTTOM = 'mobile-payment-options-layout-bottom';
        this.MOBILE_PAYMENT_OPTIONS_LAYOUT_CHOOSE = 'mobile-payment-options-layout-choose';
        this.CANCELLATION_SWEETENERS = 'cancellation_sweeteners';
        this.CANCELLATION_SWEETENERS_CONTROL = 'cancellation_sweeteners_control';
        this.CANCELLATION_SWEETENERS_FREEBIE = 'cancellation_sweeteners_freebie';
        this.CANCELLATION_SWEETENERS_REDUCED = 'cancellation_sweeteners_reduced';
        this.EDU_ASSIGNING = 'edu-assigning';
        this.EDU_ASSIGNING_CONTROL = 'edu-assigning-control';
        this.EDU_ASSIGNING_NEW = 'edu-assigning-new';
        this.EDU_ASSIGNING_HEADERS = 'edu-assigning-headers';
        this.SUMMER_OF_READING_SALE_BANNER = 'summer-of-reading-sale-banner';
        this.SUMMER_OF_READING_SALE_BANNER_SHOW_ON_LOAD = 'summer-of-reading-sale-banner-show-on-load';
        this.SUMMER_OF_READING_SALE_BANNER_DO_NOTHING = 'summer-of-reading-sale-banner-do-nothing';
        this.EDU_EXPLORE_TEACHER = 'edu-explore-teacher';
        this.EDU_EXPLORE_TEACHER_CONTROL = 'edu-explore-teacher-control';
        this.EDU_EXPLORE_TEACHER_FOR_YOU = 'edu-explore-teacher-for-you';
        this.EDU_EXPLORE_TEACHER_RL = 'edu-explore-teacher-rl';
        this.EDU_EXPLORE_STUDENT = 'edu-explore-student';
        this.EDU_EXPLORE_STUDENT_CONTROL = 'edu-explore-student-control';
        this.EDU_EXPLORE_STUDENT_RL = 'edu-explore-student-rl';
    }
    /*
     * Retrieve the experiment data by experiment LABEL
     * @type: 'account' or 'user'
     * @id: optional, accountid or userid
     */
    ABTestService.prototype.loadExperimentDataByLabel = function (expLabel, type, id, useAuthCall) {
        var _this = this;
        var params = { expLabel: expLabel, type: type, id: id };
        params.expLabel = expLabel;
        params.type = type;
        params.id =
            type === 'account'
                ? id || this.accountService.id || Globals.GLOBAL_ACCOUNT_ID
                : id || this.profileService.currentProfile.id;
        var apiCall = useAuthCall
            ? 'loadExperimentdataByLabel'
            : 'noAuthLoadExperimentdataByLabel';
        return this.data.get('WebABTest', apiCall, params).then(function (data) {
            if (data && data.result) {
                if (data.result.active) {
                    var testId = type === 'account'
                        ? data.result.accountId
                        : data.result.userId;
                    if (!_this.experiments[type].hasOwnProperty(testId)) {
                        _this.experiments[type][testId] = {};
                    }
                    _this.experiments[type][testId][expLabel] = data.result;
                }
                bbb('Experiment data loaded: ', data.result);
                return data.result.variantLabel;
            }
            return null;
        });
    };
    /*
     * Return variant by experiment label, return null if
     * experiment data for this account has not been retrieved yet
     */
    ABTestService.prototype.getVariantByExpLabel = function (expLabel, type, id) {
        id =
            type === 'account'
                ? id || this.accountService.id
                : id || this.profileService.currentProfile.id;
        if (this.experiments[type].hasOwnProperty(id)) {
            if (this.experiments[type][id].hasOwnProperty(expLabel)) {
                return this.experiments[type][id][expLabel].variantLabel;
            }
        }
        return null;
    };
    ABTestService.prototype.getVariantForEduAssign = function () {
        var v = this.getVariantByExpLabel(this.EDU_ASSIGNING, 'account');
        return this.profileService.currentProfile.isParent
            ? v || this.EDU_ASSIGNING_CONTROL
            : this.EDU_ASSIGNING_CONTROL;
    };
    ABTestService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root',
        }),
        __metadata("design:paramtypes", [_services_data_service__WEBPACK_IMPORTED_MODULE_1__["DataService"],
            _services_profile_service__WEBPACK_IMPORTED_MODULE_2__["ProfileService"],
            _services_account_service__WEBPACK_IMPORTED_MODULE_3__["AccountService"]])
    ], ABTestService);
    return ABTestService;
}());



/***/ }),

/***/ "./src/app/core/services/account.service.ts":
/*!**************************************************!*\
  !*** ./src/app/core/services/account.service.ts ***!
  \**************************************************/
/*! exports provided: AccountService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AccountService", function() { return AccountService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _data_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./data.service */ "./src/app/core/services/data.service.ts");
/* harmony import */ var ts_md5_dist_md5__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ts-md5/dist/md5 */ "./node_modules/ts-md5/dist/md5.js");
/* harmony import */ var ts_md5_dist_md5__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(ts_md5_dist_md5__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _session_storage_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./session-storage.service */ "./src/app/core/services/session-storage.service.ts");
/* harmony import */ var _local_storage_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./local-storage.service */ "./src/app/core/services/local-storage.service.ts");
/* harmony import */ var _window_ref_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./window-ref.service */ "./src/app/core/services/window-ref.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};






var AccountService = /** @class */ (function () {
    function AccountService(data, localStorage, sessionStorage, Window) {
        this.data = data;
        this.localStorage = localStorage;
        this.sessionStorage = sessionStorage;
        this.Window = Window;
        this.accountDataLoaded = false;
        this.isLoggedIn = false;
        this.EDU_MAX_PROFILES = 500;
        this.CONSUMER_MAX_PROFILES = 4;
        this.ACCOUNT_TYPE_STANDARD = 0;
        this.ACCOUNT_TYPE_EDUCATOR = 1;
        this.ACCOUNT_TYPE_HOMESCHOOLER = 2;
        this.classroomCodeTooltip = 'Have students enter this code on the sign in page as an easy way to log in and access their profiles.';
        // THESE MATCH ACCOUNT SUBSCRIPTION DATA OBJECT
        this.STATUS_FREE_TRIAL = 0;
        this.STATUS_NOT_SUBSCRIBED = 1;
        this.STATUS_SUBSCRIBED = 2;
        this.STATUS_SUBSCRIPTION_EXPIRED = 3;
        this.STATUS_SUBSCRIPTION_CANCELED = 4;
        this.STATUS_PROMO = 5;
        this.STATUS_GIFT_SUBSCRIPTION = 7;
        this.SUBSCRIPTION_TYPE_APPLE = 0;
        this.SUBSCRIPTION_TYPE_STRIPE = 1;
        this.eduv = this.sessionStorage.getSessionStorageWithKey('eduv') ?
            JSON.parse(this.sessionStorage.getSessionStorageWithKey('eduv')) : null;
        this.window = this.Window.nativeWindow;
    }
    AccountService.prototype.login = function (email, pass, key, loginAsDefault, loginCode) {
        var _this = this;
        var postData = {};
        if (email) {
            postData.email = email;
        }
        if (pass) {
            postData.pass = pass;
        }
        if (key) {
            postData.sessionKey = key;
        }
        if (loginAsDefault) {
            postData.loginAsDefault = 1;
        }
        if (loginCode) {
            postData.accountLoginCode = loginCode.replace(/-/g, '');
        } // Strip dashes
        return this.data.post('WebAccount', 'noAuthLogin', postData).then(function (data) {
            var result = {};
            if (!data.result) { // Server call failed
                result.error = 'Oops, login failed!';
            }
            else { // Success
                if (data.result.success) {
                    result.success = true;
                    Globals.GLOBAL_IS_AUTHED = 1;
                    _this.renewTimestamp();
                    _this.setAccountData(data.result.Account);
                    _this.addLocalLogin(_this.email, data.result.session_key);
                    // Failed
                }
                else if (data.result.not_found || data.result.incorrect_password) {
                    result.error = 'Invalid email or password. Please try again!';
                }
            }
            return result;
        });
    };
    // TODO: figure if this is still used, remove maybe
    AccountService.prototype.loginFromMobile = function (mobileToWebAppSigninToken, destinationRoute, sig) {
        var _this = this;
        var postData = {
            mobileToWebAppSigninToken: mobileToWebAppSigninToken,
            destinationRoute: destinationRoute,
            sig: sig
        };
        return this.data.post('WebAccount', 'noAuthLoginFromMobile', postData).then(function (data) {
            var result = {};
            if (!data.result) {
                // Server call failed
                result.error = 'Oops, login failed!';
            }
            else {
                // Success
                if (data.result.success) {
                    _this.renewTimestamp();
                    result.success = true;
                    Globals.GLOBAL_IS_AUTHED = 1;
                    _this.setAccountData(data.result.Account);
                    // Add account to list of classrooms
                    if (_this.isEducator()) {
                        _this.addLocalLogin(_this.email, data.result.session_key);
                    }
                    if (data.result.destinationRoute) {
                        result.destinationRoute = data.result.destinationRoute;
                    }
                    // Failed
                }
                else if (data.result.not_found || data.result.incorrect_password) {
                    result.error = 'Invalid email or password. Please try again!';
                }
            }
            return result;
        });
    };
    AccountService.prototype.logout = function (skipRedirect) {
        return this.logoutSilent(skipRedirect);
    };
    AccountService.prototype.logoutSilent = function (skipRedirect) {
        var _this = this;
        this.localStorage.set('date_profile_last_selected', null);
        this.invalidateTimestamp();
        var routeExtension = '';
        if (this.isEducator()) {
            routeExtension = 'educators';
        }
        return this.data.get('WebAccount', 'logout').then(function (data) {
            if (!skipRedirect) {
                _this.window.location.href = '/' + routeExtension;
            }
            // this.setAccountData({});
            _this.setEmptyAccountData();
            Globals.GLOBAL_IS_AUTHED = 0;
            return data;
        });
    };
    AccountService.prototype.updateAccountData = function () {
        var _this = this;
        return this.data.get('WebAccount', 'getAccountData').then(function (data) {
            console.log('-----', data);
            _this.setAccountData(data.result);
            return _this;
        });
    };
    AccountService.prototype.getLocalLogins = function () {
        var logins = this.localStorage.get('account_service_logins');
        // why is this here?
        // my current implementation parses as it gets from ls
        // if (typeof logins === 'string' || logins instanceof String) {
        //  logins = JSON.parse(logins);
        // }
        return logins || {};
    };
    AccountService.prototype.addLocalLogin = function (email, session_key) {
        if (!email) {
            return;
        }
        var logins = this.getLocalLogins();
        logins[email] = ({ session_key: session_key });
        this.saveLocalLogins(logins);
    };
    AccountService.prototype.removeLocalLogin = function (email) {
        var logins = this.getLocalLogins();
        for (var key in logins) {
            if (key === email) {
                delete logins[key];
            }
        }
        this.saveLocalLogins(logins);
    };
    AccountService.prototype.getSessionKeyForLogin = function (login) {
        var loginData = this.getLocalLogins();
        var key;
        if (loginData !== null && loginData.hasOwnProperty(login)) {
            key = loginData[login].session_key;
        }
        return key;
    };
    AccountService.prototype.isFresh = function () {
        return this.localStorage.get('date_account_last_selected') > Math.floor(Date.now() / 1000) || this.isAuth();
    };
    AccountService.prototype.invalidateTimestamp = function () {
        this.isLoggedIn = false;
        this.localStorage.set('date_account_last_selected', null);
    };
    AccountService.prototype.generateClassroomCode = function () {
        return this.data.post('WebAccount', 'generateLoginCode').then(function (data) {
            return data;
        });
    };
    AccountService.prototype.formatClassroomCode = function () {
        if (this.accountLoginCode) {
            return this.accountLoginCode.replace('-', '').toLowerCase();
        }
        else {
            return undefined;
        }
    };
    AccountService.prototype.isAuth = function () {
        return !!Globals.GLOBAL_IS_AUTHED;
    };
    AccountService.prototype.isSubscribed = function () {
        switch (this.status) {
            case 0: // Trial
            case 2: // Subscribed
            case 5: // Promotional
                return true;
            default:
                return false;
        }
    };
    AccountService.prototype.isEducator = function () {
        return this.type === this.ACCOUNT_TYPE_EDUCATOR;
    };
    AccountService.prototype.isHomeSchooler = function () {
        return this.type == this.ACCOUNT_TYPE_HOMESCHOOLER;
    };
    AccountService.prototype.getDeviceId = function () {
        var deviceId = this.localStorage.get('device_id');
        if (!deviceId) {
            deviceId = ts_md5_dist_md5__WEBPACK_IMPORTED_MODULE_2__["Md5"].hashStr(Math.random().toString());
            this.localStorage.set('device_id', deviceId);
        }
        return deviceId;
    };
    AccountService.prototype.createAccountWithModel = function (accountModel) {
        return this.data.post('WebAccount', 'noAuthCreateAccount', {
            accountData: accountModel.getJSONFormattedData(),
            enableEduEmailCheck: 0
        });
    };
    AccountService.prototype.renewTimestamp = function () {
        this.isLoggedIn = true;
        this.localStorage.set('date_account_last_selected', (Math.floor(Date.now() / 1000) + 60 * 15) + '');
    };
    AccountService.prototype.setAccountData = function (accountData) {
        this.id = accountData.id;
        this.email = accountData.login;
        this.uuid = accountData.modelId || accountData.uuid;
        this.type = accountData.type;
        this.status = accountData.status;
        this.dateCreated = accountData.createdTS;
        this.maxProfiles = (this.isEducator()) ? this.EDU_MAX_PROFILES : this.CONSUMER_MAX_PROFILES;
        this.videoEnabled = accountData.videoEnabled;
        this.accountLoginCode = accountData.accountLoginCode;
        this.afterHoursEnabled = accountData.afterHoursEnabled;
        this.currentGroupId = accountData.currentGroupId;
        this.tapEnrolled = accountData.tapEnabled;
        this.exTS = accountData.exTS;
        this.subscriptionType = accountData.subscriptionType;
        this.realSubscriptionStatus = accountData.realSubscriptionStatus;
        this.productId = accountData.productId;
        this.accountDataLoaded = true;
        // TODO use an observer pattern. The broadcast was nice
        // the watcher fix is sub optimal
        // $rootScope.$broadcast('accountData-loaded', accountData);
    };
    AccountService.prototype.setEmptyAccountData = function () {
        this.setAccountData({
            id: undefined,
            login: undefined,
            modelId: undefined,
            uuid: undefined,
            type: undefined,
            status: undefined,
            createdTS: undefined,
            videoEnabled: undefined,
            accountLoginCode: undefined,
            afterHoursEnabled: undefined,
            currentGroupId: undefined,
            tapEnabled: undefined,
            exTS: undefined,
            subscriptionType: undefined,
            realSubscriptionStatus: undefined,
            productId: undefined,
        });
    };
    AccountService.prototype.saveLocalLogins = function (logins) {
        // logins = JSON.stringify(logins);
        this.localStorage.set('account_service_logins', logins);
    };
    AccountService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [_data_service__WEBPACK_IMPORTED_MODULE_1__["DataService"],
            _local_storage_service__WEBPACK_IMPORTED_MODULE_4__["LocalStorageService"],
            _session_storage_service__WEBPACK_IMPORTED_MODULE_3__["SessionStorageService"],
            _window_ref_service__WEBPACK_IMPORTED_MODULE_5__["WindowRefService"]])
    ], AccountService);
    return AccountService;
}());



/***/ }),

/***/ "./src/app/core/services/after-hours.service.ts":
/*!******************************************************!*\
  !*** ./src/app/core/services/after-hours.service.ts ***!
  \******************************************************/
/*! exports provided: AfterHoursService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AfterHoursService", function() { return AfterHoursService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _local_storage_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./local-storage.service */ "./src/app/core/services/local-storage.service.ts");
/* harmony import */ var _account_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./account.service */ "./src/app/core/services/account.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var AfterHoursService = /** @class */ (function () {
    function AfterHoursService(localStorage, accountService) {
        this.localStorage = localStorage;
        this.accountService = accountService;
    }
    AfterHoursService_1 = AfterHoursService;
    AfterHoursService.prototype.afterHours = function () {
        var data = this.getDayData();
        var h = data.hour;
        return h < AfterHoursService_1.EDUCATOR_ALLOWED_START_TIME ||
            h >= AfterHoursService_1.EDUCATOR_ALLOWED_END_TIME ||
            this.isWeekend();
    };
    AfterHoursService.prototype.validAfterHoursTimestamp = function () {
        var data = this.localStorage.get(AfterHoursService_1.localStorageKey) || {};
        // var ts = data[this.accountService.email] || 0;
        var ts;
        if (this.accountService.email) {
            ts = data[this.accountService.email];
        }
        else {
            ts = 0;
        }
        return this.now() <= ts; // 1 hour
    };
    AfterHoursService.prototype.setAfterHoursTimestamp = function (email) {
        var data = this.localStorage.get(AfterHoursService_1.localStorageKey) || {};
        var email = email || this.accountService.email;
        if (email) {
            data[email] = this.now() + 60 * 60;
        }
        this.localStorage.set(AfterHoursService_1.localStorageKey, data);
    };
    AfterHoursService.prototype.currentDay = function () {
        // returns 0-6 for sunday-saturday
        var date = new Date();
        return date.getDay();
    };
    AfterHoursService.prototype.currentHour = function () {
        // returns 0-23 for military time hour
        var date = new Date();
        return date.getHours();
    };
    AfterHoursService.prototype.getDayData = function () {
        var date = new Date();
        var result = {
            day: date.getDay(),
            hour: date.getHours()
        };
        return result;
    };
    AfterHoursService.prototype.getCurrentTimestamp = function () {
        return this.now();
    };
    AfterHoursService.prototype.isWeekend = function () {
        var d = this.currentDay();
        return d === 0 || d === 6; // 0 - sunday, 6 - saturday
    };
    AfterHoursService.prototype.now = function () {
        return Math.floor(Date.now() / 1000);
    };
    var AfterHoursService_1;
    AfterHoursService.localStorageKey = 'after-hours-ts';
    AfterHoursService.EDUCATOR_ALLOWED_START_TIME = 6; // 6am
    AfterHoursService.EDUCATOR_ALLOWED_END_TIME = 16; // 4pm
    AfterHoursService = AfterHoursService_1 = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [_local_storage_service__WEBPACK_IMPORTED_MODULE_1__["LocalStorageService"],
            _account_service__WEBPACK_IMPORTED_MODULE_2__["AccountService"]])
    ], AfterHoursService);
    return AfterHoursService;
}());



/***/ }),

/***/ "./src/app/core/services/angularjs-translator.service.ts":
/*!***************************************************************!*\
  !*** ./src/app/core/services/angularjs-translator.service.ts ***!
  \***************************************************************/
/*! exports provided: AngularjsTranslatorService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AngularjsTranslatorService", function() { return AngularjsTranslatorService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var AngularjsTranslatorService = /** @class */ (function () {
    function AngularjsTranslatorService() {
        this.translations = {};
        this.ANGULARJS_LOCATION_SERVICE = 'angularjs_location_service';
        this.ANGULARJS_STATE_SERVICE = 'angularjs_state_service';
        this.ANGULARJS_STATE_PARAMS_SERVICE = 'angularjs_state_params_service';
        this.BROWSESERVICE_BROWSEDATA = 'browseservice_browsedata';
    }
    AngularjsTranslatorService.prototype.getObject = function (angularJsObjectName) {
        if (!this.translations.angularJsObjectName)
            return;
        return this.translations[angularJsObjectName];
    };
    AngularjsTranslatorService.prototype.setObject = function (angularJsObjectName, angularJsObject) {
        if (!angularJsObjectName || !angularJsObject)
            return;
        this.translations[angularJsObjectName] = angularJsObject;
    };
    AngularjsTranslatorService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [])
    ], AngularjsTranslatorService);
    return AngularjsTranslatorService;
}());



/***/ }),

/***/ "./src/app/core/services/asset.service.ts":
/*!************************************************!*\
  !*** ./src/app/core/services/asset.service.ts ***!
  \************************************************/
/*! exports provided: AssetService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AssetService", function() { return AssetService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var ts_md5_dist_md5__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ts-md5/dist/md5 */ "./node_modules/ts-md5/dist/md5.js");
/* harmony import */ var ts_md5_dist_md5__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(ts_md5_dist_md5__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _data_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./data.service */ "./src/app/core/services/data.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var AssetService = /** @class */ (function () {
    function AssetService(data) {
        this.data = data;
        this.getFinalAssetPath = function (assetPath) {
            var s1 = 'kje4fc6f017797e20e3gfdoijdro3498u';
            var s2 = 'ed8933800968d99bb73fgdjgh09234kdk';
            if (!assetPath) {
                return null;
            }
            assetPath = assetPath[0] === '/' ? assetPath : '/' + assetPath; // make sure url has a forward slash
            var s = getS(s1) + getS(s2);
            var expire = Number(Globals.GLOBAL_TIMESTAMP) + 600;
            var md5 = ts_md5_dist_md5__WEBPACK_IMPORTED_MODULE_1__["Md5"].hashStr(assetPath + '?ttl=' + expire + '&auth=' + s);
            var params = '?ttl=' + expire + '&token=' + md5;
            function getS(s) {
                return s.substr(3, 16);
            }
            return Globals.GLOBAL_CDN_BASE + assetPath + params;
        };
    }
    AssetService.prototype.resizeThumb = function (bookId, params) {
        if (params === void 0) { params = { url: '' }; }
        if (!bookId) {
            return '';
        }
        params.quality = params.quality || 90;
        params.url = "" + Globals.GLOBAL_SECURE_CDN_BASE + bookId.toString().slice(-1) + "/" + bookId + "/cover.jpg";
        return Globals.GLOBAL_RESIZE_BASE.replace(/.php/, '.jpg') + "?" + this.data.urlEncode(params);
    };
    AssetService.prototype.resizeUrl = function (params) {
        var data = { url: params.url || '' };
        var ext = params.url.slice(-3); // png or jpg?
        var base = Globals.GLOBAL_RESIZE_BASE.replace(/.php/, "." + ext);
        if (params.quality) {
            // Normalize png quality
            var qual = Number(params.quality);
            if (ext === 'png') {
                qual = Math.min(qual, 99); // 0-99
                qual = Math.floor(qual / 100) * 10; // 0-9
                qual = 9 - qual; // 0 = no compression
            }
            data[ext + '_quality'] = qual;
        }
        if (params.width) {
            data.width = params.width;
        }
        if (params.height) {
            data.width = params.height;
        }
        return base + "?" + this.data.urlEncode(data);
    };
    AssetService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [_data_service__WEBPACK_IMPORTED_MODULE_2__["DataService"]])
    ], AssetService);
    return AssetService;
}());



/***/ }),

/***/ "./src/app/core/services/big-query.service.ts":
/*!****************************************************!*\
  !*** ./src/app/core/services/big-query.service.ts ***!
  \****************************************************/
/*! exports provided: BigQueryService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "BigQueryService", function() { return BigQueryService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");
/* harmony import */ var _constants_EventConstants__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @constants/EventConstants */ "./src/app/core/constants/EventConstants.ts");
/* harmony import */ var _constants_PerformanceEventConstants__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @constants/PerformanceEventConstants */ "./src/app/core/constants/PerformanceEventConstants.ts");
/* harmony import */ var _window_ref_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./window-ref.service */ "./src/app/core/services/window-ref.service.ts");
/* harmony import */ var _services_data_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @services/data.service */ "./src/app/core/services/data.service.ts");
/* harmony import */ var _services_account_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @services/account.service */ "./src/app/core/services/account.service.ts");
/* harmony import */ var _services_user_agent_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @services/user-agent.service */ "./src/app/core/services/user-agent.service.ts");
/* harmony import */ var _services_profile_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @services/profile.service */ "./src/app/core/services/profile.service.ts");
/* harmony import */ var _services_angularjs_translator_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @services/angularjs-translator.service */ "./src/app/core/services/angularjs-translator.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};




// import { ttiPolyfill } from 'tti-polyfill';






var BigQueryService = /** @class */ (function () {
    function BigQueryService(events, performanceEvents, Window, data, http, accountService, userAgent, profileService, ng1Translator) {
        var _this = this;
        this.events = events;
        this.performanceEvents = performanceEvents;
        this.Window = Window;
        this.data = data;
        this.http = http;
        this.accountService = accountService;
        this.userAgent = userAgent;
        this.profileService = profileService;
        this.ng1Translator = ng1Translator;
        // if a performance event takes longer than this it will get logged as an over-time error
        this.errorMinTime = 5000;
        this.performanceEventParams = ['sts', 'du', 'me', 'met', 'src'];
        this.curContentSource = undefined;
        // big query service (table) names
        this.PERFORMANCE_SERVICE = 'performance';
        this.ERROR_SERVICE = 'app_error';
        this.httpHeaderConfig = {
            headers: new _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpHeaders"]({ 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' })
        };
        this.sessionKey = this.uuid();
        this.window = this.Window.nativeWindow;
        this.window.addEventListener("beforeunload", this.log(this.events.WEB_UNLOAD));
        // add performance events into the events array
        // to be able to reference all events as one array in this service
        Object.keys(this.performanceEvents).forEach(function (eventKey) {
            _this.events[eventKey] = _this.performanceEvents[eventKey];
        });
        this.calculateBundleLoadTime();
        if (this.window.ttiPolyfill) {
            this.window.ttiPolyfill.getFirstConsistentlyInteractive().then(function (tti) {
                var params = {};
                params.du = Math.floor(tti);
                if (_this.ng1Translator.translations[_this.ng1Translator.ANGULARJS_STATE_SERVICE]) {
                    params.state = _this.ng1Translator.translations[_this.ng1Translator.ANGULARJS_STATE_SERVICE].current.name;
                }
                _this.log(_this.events.PERFORMANCE_TTI, params);
            });
        }
    }
    BigQueryService.prototype.sendPerformanceLog = function (name, params) {
        if (!name || !params) {
            return;
        }
        if (params.du && params.du > this.errorMinTime) {
            this.log(this.performanceEvents.PERFORMANCE_OVER_TIME_ERROR, {
                eventName: name,
                time: params.du
            });
        }
        // TODO move the following line to here
        // params.service = 'performance'; // direct to the performance big Query table
        this.log(name, params);
    };
    BigQueryService.prototype.signOut = function () {
        this.log(this.events.ACCOUNT_SIGN_OUT);
    };
    BigQueryService.prototype.log = function (event, customParams) {
        var _this = this;
        if (customParams === void 0) { customParams = {}; }
        if (!event) {
            console.warn("BigQuery: log failed, event =", event);
            return;
        }
        // these will get logged in the app_error table
        // vs the (default) events table
        var errorEvents = [
            this.events.CONSOLE_ERRORS,
            this.performanceEvents.PERFORMANCE_OVER_TIME_ERROR
        ];
        var params = {};
        if (event.substring(0, 7) === "content" && this.curContentSource) {
            customParams['content_source'] = this.curContentSource;
        }
        // content items are using this mechanism to pass their
        // source to log
        if (event.substring(0, 7) === "content") {
            if (customParams.src) {
                params.src = customParams.src;
                delete customParams.src;
            }
        }
        // intercept custom params and turn them into normal params
        // in certain cases. I wonder if there are better ways to do this?
        var peKeys = Object.keys(this.performanceEvents).map(function (key) {
            return _this.performanceEvents[key];
        });
        if (peKeys.includes(event)) {
            params.service = this.PERFORMANCE_SERVICE; // direct to the performance big Query table
        }
        // if there are any custom params
        // todo: this is just to check for an empty object
        // https://stackoverflow.com/questions/679915/how-do-i-test-for-an-empty-javascript-object
        // can't typescript do this?
        if (Object.entries(customParams).length === 0 && customParams.constructor === Object) {
            Object.keys(customParams).forEach(function (key) {
                if (_this.performanceEventParams.includes(key)) {
                    params[key] = customParams[key];
                    delete customParams[key];
                }
            });
        }
        // done intercepting. Deal with the rest of the normal ones
        if (errorEvents.includes(event)) {
            params.service = this.ERROR_SERVICE; // direct to the app_error big Query table
        }
        var key;
        var val;
        var ip = {};
        var sp = {};
        for (key in customParams) {
            val = customParams[key];
            if (typeof val === "number") {
                ip[key] = val;
            }
            else if (typeof val === "string") {
                sp[key] = val;
            }
            else {
                console.warn("BigQuery: param", key + ":", val, "cannot be logged (int or string only)");
            }
        }
        params.a = this.accountService.id; // Account id
        params.ac = this.accountService.dateCreated; // Account created
        params.al = this.accountAge(); // Lifetime
        params.at = this.accountService.type; // Account type
        params.d = 'browser'; // Device
        params.did = this.accountService.getDeviceId(); // Device id
        params.dt = this.userAgent.browser.name; // Browser
        params.e = event; // Event name
        params.ip = JSON.stringify(ip); // Int params
        params.isp = this.profileService.currentProfile.isParent ? 1 : 0; // Parent?
        params.l = Globals.GLOBAL_LOCATION;
        params.oa = this.profileService.currentProfile.accountId; // Profile's owning account
        params.os = this.userAgent.os.name; // OS
        params.p = 'web'; // Platform
        params.ra = this.profileService.currentProfile.startingAge; // Starting Age
        params.rea = this.profileService.currentProfile.readingAge; // Reading Age
        params.sid = this.sessionKey; // Session id
        params.sp = JSON.stringify(sp); // String params
        params.st = Globals.GLOBAL_SESSION_LENGTH; // Session length
        params.ss = this.accountService.status; // Subscription status
        params.u = this.profileService.currentProfile.id; // Profile id
        params.v = Globals.GLOBAL_ASSETS_VERSION; // Asset version
        // state logging,
        if (this.ng1Translator.translations[this.ng1Translator.ANGULARJS_STATE_SERVICE]) {
            var state = {};
            var tempStateTranslation = this.ng1Translator.translations[this.ng1Translator.ANGULARJS_STATE_SERVICE];
            if (tempStateTranslation.current) {
                state.cur = tempStateTranslation.current.name;
                if (tempStateTranslation.current.previousState) {
                    state.prev = tempStateTranslation.current.previousState;
                }
            }
            params.state = JSON.stringify(state);
        }
        params = this.validateParams(params);
        if (Globals.GLOBAL_STAGING_MODE || Globals.GLOBAL_DEV_MODE) {
            // if (Globals.GLOBAL_STAGING_MODE) {
            bbb('BigQuery:', event, params, customParams);
        }
        var encodedParams = this.data.urlEncode(params, true);
        return this.http.post(Globals.GLOBAL_ANALYTICS_URL, encodedParams, this.httpHeaderConfig).toPromise()
            .then(function (result) {
            return result;
        })
            .catch(function () {
            //handle errors
        });
    };
    BigQueryService.prototype.accountAge = function () {
        if (!this.accountService.dateCreated)
            return undefined;
        var d1 = new Date(this.accountService.dateCreated * 1000);
        var d2 = new Date();
        var months;
        months = (d2.getFullYear() - d1.getFullYear()) * 12;
        months -= d1.getMonth() + 1;
        months += d2.getMonth();
        return months <= 0 ? 0 : months;
    };
    BigQueryService.prototype.validateParams = function (params) {
        var val, validated = {};
        for (var key in params) {
            val = params[key];
            if (val !== null && val !== undefined) {
                validated[key] = val;
            }
        }
        return validated;
    };
    BigQueryService.prototype.uuid = function () {
        var uuid = "", i, random;
        for (i = 0; i < 32; i++) {
            random = Math.random() * 16 | 0;
            if (i == 8 || i == 12 || i == 16 || i == 20) {
                uuid += "-";
            }
            uuid += (i == 12 ? 4 : (i == 16 ? (random & 3 | 8) : random)).toString(16);
        }
        return uuid;
    };
    // todo make sure rewrite works
    // the method feels a little suspect in general
    // public getCookie(name) {
    //   var value = "; " + this.window.document.cookie;
    //   var parts = value.split("; " + name + "=");
    //   if (parts.length == 2) return parts.pop().split(";").shift();
    // }
    BigQueryService.prototype.getCookie = function (name) {
        if (!this.window.document.cookie)
            return undefined;
        var value = "; " + this.window.document.cookie;
        var parts = value.split("; " + name + "=");
        if (parts.length == 2) {
            var temp = parts.pop();
            return temp ? temp.split(";").shift() : undefined;
        }
        else {
            return undefined;
        }
    };
    BigQueryService.prototype.setContentSource = function (name) {
        this.curContentSource = name;
    };
    // performance logging functionality
    // https://developer.mozilla.org/en-US/docs/Web/API/Resource_Timing_API/Using_the_Resource_Timing_API
    BigQueryService.prototype.calculateBundleLoadTime = function () {
        // Check performance support
        if (performance === undefined) {
            // console.log("= Calculate Load Times: performance NOT supported");
            return;
        }
        // Get a list of "resource" performance entries
        var resources = performance.getEntriesByType("resource");
        if (resources === undefined || resources.length <= 0) {
            // console.log("= Calculate Load Times: there are NO `resource` performance records");
            return;
        }
        // console.log("= Calculate Load Times for App bundle");
        for (var i = 0; i < resources.length; i++) {
            if (resources[i].name.includes(this.performanceEvents.APP_BUNDLE_ID_STRING)) {
                // console.log("== Resource[" + i + "] - " + resources[i].name);
                // console.log("... Start until response end time = " + t);
                var t = (resources[i].startTime > 0) ? resources[i].duration : 0;
                var params = {};
                params.du = Math.floor(t);
                this.sendPerformanceLog(this.performanceEvents.PERFORMANCE_BUNDLE_DOWNLOAD, params);
            }
        }
    };
    ;
    BigQueryService.prototype.mark_start = function (event) {
        if (performance.mark === undefined) {
            console.log("performance.mark Not supported");
            return;
        }
        // Create the performance mark
        var nameStart = event + "-start";
        performance.mark(nameStart);
    };
    BigQueryService.prototype.mark_end_and_send = function (event, params) {
        if (params === void 0) { params = {}; }
        if (performance.measure === undefined || performance.mark === undefined) {
            console.log("performance api Not supported");
            return;
        }
        var nameStart = event + "-start";
        var nameEnd = event + "-end";
        performance.mark(nameEnd);
        performance.measure(event, nameStart, nameEnd);
        var measures = performance.getEntriesByName(event);
        var measure = measures[0];
        params.du = Math.floor(measure.duration);
        this.sendPerformanceLog(event, params);
        // Clean up the stored markers.
        this.clear_mark(event);
        this.clear_measure(event);
    };
    BigQueryService.prototype.clear_mark = function (name) {
        if (performance.clearMarks === undefined) {
            console.log("performance.clearMarks Not supported");
            return;
        }
        // Remove all "mark" performance entry types with the specified name
        performance.clearMarks(name);
    };
    BigQueryService.prototype.clear_measure = function (name) {
        if (performance.clearMeasures === undefined) {
            console.log("performance.clearMeasures Not supported");
            return;
        }
        // Remove all "measure" performance entry types with the specified name
        performance.clearMeasures(name);
    };
    BigQueryService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [_constants_EventConstants__WEBPACK_IMPORTED_MODULE_2__["EventConstants"],
            _constants_PerformanceEventConstants__WEBPACK_IMPORTED_MODULE_3__["PerformanceEventConstants"],
            _window_ref_service__WEBPACK_IMPORTED_MODULE_4__["WindowRefService"],
            _services_data_service__WEBPACK_IMPORTED_MODULE_5__["DataService"],
            _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpClient"],
            _services_account_service__WEBPACK_IMPORTED_MODULE_6__["AccountService"],
            _services_user_agent_service__WEBPACK_IMPORTED_MODULE_7__["UserAgentService"],
            _services_profile_service__WEBPACK_IMPORTED_MODULE_8__["ProfileService"],
            _services_angularjs_translator_service__WEBPACK_IMPORTED_MODULE_9__["AngularjsTranslatorService"]])
    ], BigQueryService);
    return BigQueryService;
}());



/***/ }),

/***/ "./src/app/core/services/captcha.service.ts":
/*!**************************************************!*\
  !*** ./src/app/core/services/captcha.service.ts ***!
  \**************************************************/
/*! exports provided: CaptchaService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CaptchaService", function() { return CaptchaService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _data_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./data.service */ "./src/app/core/services/data.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


var CaptchaService = /** @class */ (function () {
    function CaptchaService(data) {
        this.data = data;
        this.siteKey = '6LfgU4YUAAAAAOBzEV1NQw2mO77CAVBnrGB98ufs';
        this.CAPTCHA_PAYMENT = 1;
        this.CAPTCHA_PAYMENT_GIFT = 2;
        this.CAPTCHA_PAYMENT_UPDATE = 3;
        this.CAPTCHA_ACCOUNT_CREATE = 4;
        this.elements = [];
    }
    CaptchaService.prototype.checkRequiresCaptcha = function (type) {
        return this.data.get('WebAccount', 'noAuthCheckRequiresCaptcha', { type: type })
            .then(function (data) {
            return (data && data.result && data.result.required == true);
        })
            .catch(function () {
            return null;
        });
    };
    CaptchaService.prototype.getToken = function () {
        if (this.recaptcha && this.recaptcha.getResponse()) {
            return this.recaptcha.getResponse();
        }
        return null;
    };
    CaptchaService.prototype.addOrResetCaptcha = function (element, callback) {
        this.elements.push({
            element: element,
            callback: callback
        });
        if (this.canRender(element)) {
            this.addCaptcha();
            this.registerReCaptchaCallback();
        }
        else {
            this.resetCaptcha();
        }
    };
    CaptchaService.prototype.addCaptcha = function () {
        bbb('Adding CAPTCHA');
        var script = document.createElement('script');
        script.src = "https://www.google.com/recaptcha/api.js?onload=reCaptchaLoad&render=explicit";
        script.async = true;
        script.defer = true;
        document.body.appendChild(script);
    };
    CaptchaService.prototype.registerReCaptchaCallback = function () {
        var _this = this;
        window.reCaptchaLoad = function () {
            _this.recaptcha = grecaptcha;
            var params = _this.elements.pop();
            var config = {
                'sitekey': _this.siteKey,
                'expired-callback': function () {
                    grecaptcha.reset();
                },
                'callback': params.callback
            };
            grecaptcha.render(params.element, config);
        };
    };
    CaptchaService.prototype.resetCaptcha = function () {
        if (!this.recaptcha)
            return;
        bbb('Resetting CAPTCHA');
        this.recaptcha.reset();
    };
    CaptchaService.prototype.canRender = function (element) {
        return (element && !element.children[0]);
    };
    CaptchaService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [_data_service__WEBPACK_IMPORTED_MODULE_1__["DataService"]])
    ], CaptchaService);
    return CaptchaService;
}());



/***/ }),

/***/ "./src/app/core/services/data.service.ts":
/*!***********************************************!*\
  !*** ./src/app/core/services/data.service.ts ***!
  \***********************************************/
/*! exports provided: DataService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DataService", function() { return DataService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");
/* harmony import */ var ts_md5_dist_md5__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ts-md5/dist/md5 */ "./node_modules/ts-md5/dist/md5.js");
/* harmony import */ var ts_md5_dist_md5__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(ts_md5_dist_md5__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _message_handler_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./message-handler.service */ "./src/app/core/services/message-handler.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


// import { Observable } from 'rxjs';


var DataService = /** @class */ (function () {
    function DataService(http, messageHandler) {
        this.http = http;
        this.messageHandler = messageHandler;
    }
    DataService.prototype.get = function (className, methodName, params) {
        var _this = this;
        if (!params) {
            params = {};
        }
        params.dev = 'web';
        var encodedParams = this.urlEncode(params);
        var serviceBase = Globals.GLOBAL_SERVICE_BASE;
        return this.http
            .get(serviceBase +
            '?class=' +
            className +
            '&method=' +
            methodName +
            '&' +
            encodedParams)
            .toPromise()
            .then(function (response) {
            _this.messageHandler.handleMessages(response.messages);
            var event = new CustomEvent('data-service-response', {
                detail: response,
            });
            document.dispatchEvent(event);
            return response;
        })
            .catch(function () { });
    };
    DataService.prototype.post = function (className, methodName, params) {
        var _this = this;
        if (!params) {
            params = {};
        }
        params.dev = 'web';
        var encodedParams = this.urlEncode(params);
        var serviceBase = Globals.GLOBAL_SERVICE_BASE;
        var config = {
            headers: new _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpHeaders"]({
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            }),
        };
        return this.http
            .post(serviceBase + '?class=' + className + '&method=' + methodName, encodedParams, config)
            .toPromise()
            .then(function (response) {
            _this.messageHandler.handleMessages(response.messages);
            var event = new CustomEvent('data-service-response', {
                detail: response,
            });
            document.dispatchEvent(event);
            return response;
        })
            .catch(function () { });
    };
    // Converts an object to x-www-form-urlencoded serialization
    // tony 3-19 making this public so the big query service can use it
    DataService.prototype.urlEncode = function (obj, signed) {
        if (signed === void 0) { signed = false; }
        var query = '';
        var key, value, subValue, fullSubName, innerObj;
        var keys = Object.keys(obj).sort();
        for (var i = 0; i < keys.length; i++) {
            key = keys[i];
            value = obj[key];
            if (value instanceof Array) {
                for (var j = 0; j < value.length; ++j) {
                    subValue = value[j];
                    fullSubName = key + '[' + j + ']';
                    innerObj = {};
                    innerObj[fullSubName] = subValue;
                    query += this.urlEncode(innerObj) + '&';
                }
            }
            else if (value instanceof Object) {
                for (var subName in value) {
                    subValue = value[subName];
                    fullSubName = key + '[' + subName + ']';
                    innerObj = {};
                    innerObj[fullSubName] = subValue;
                    query += this.urlEncode(innerObj) + '&';
                }
            }
            else {
                query +=
                    encodeURIComponent(key) +
                        '=' +
                        encodeURIComponent(value) +
                        '&';
            }
        }
        if (signed) {
            var sigStr = Globals.GLOBAL_SLT;
            for (var i = 0; i < keys.length; i++) {
                sigStr += keys[i] + obj[keys[i]];
            }
            var sig = ts_md5_dist_md5__WEBPACK_IMPORTED_MODULE_2__["Md5"].hashStr(sigStr);
            query += 'sig=' + sig;
        }
        if (query.substr(-1, 1) == '&') {
            query = query.slice(0, query.length - 1);
        }
        return query;
    };
    DataService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])(),
        __metadata("design:paramtypes", [_angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpClient"],
            _message_handler_service__WEBPACK_IMPORTED_MODULE_3__["MessageHandlerService"]])
    ], DataService);
    return DataService;
}());



/***/ }),

/***/ "./src/app/core/services/erc-books-read.service.ts":
/*!*********************************************************!*\
  !*** ./src/app/core/services/erc-books-read.service.ts ***!
  \*********************************************************/
/*! exports provided: ErcBooksReadService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ErcBooksReadService", function() { return ErcBooksReadService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var _data_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./data.service */ "./src/app/core/services/data.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var ErcBooksReadService = /** @class */ (function () {
    function ErcBooksReadService(data) {
        this.data = data;
        this.booksReadData = 0;
        this.pingPeriod = 30000;
        this.mockRunning = false;
        this.eventRunning = null;
        this.preEvent = null;
        this.postEvent = null;
        this.mockReadingInterval = Object(rxjs__WEBPACK_IMPORTED_MODULE_1__["interval"])(this.pingPeriod);
        /**  //////////////// MOCK FOR TESTING COUNTER /////////////////
         *
         * How to mock the counter - this only mocks the COUNTER and does not actually test the DB and API
         * 1. Uncomment below
         * 2. Ensure the constant READING_CHALLENGE_START - (WebReadingChallengeAPI.inc) is a timestamp prior to now.
         */
        // mock books read dynamic data. increment books read every 5 sec
        // this.mockRunning = true;
        // setTimeout( () => {
        //   const getRandInt = function (min: number, max: number) {
        //     return Math.floor((Math.random() * (max + 1)) + min);
        //   };
        //   this.booksReadData = 1234567;
        //   // this is to mock the pingForBooksRead function
        //   // TODO: check this replacement too
        //   // of rxjs interval swap out for $interval
        //   this.incrementOverDuration('booksRead', 0, this.booksReadData, this.pingPeriod);
        //   const mockReadingInterval = interval(this.pingPeriod);
        //   mockReadingInterval.subscribe(n => {
        //     console.log('mock is pinging...');
        //     const oldRead = this.booksReadData;
        //     this.booksReadData += getRandInt(100, 300);
        //     this.incrementOverDuration('booksRead', oldRead, this.booksReadData, this.pingPeriod);
        //   });
        // }, 2000);
        //////////////// END COUNTER MOCK ///////////////////
    }
    // todo: make sure the observable version of interval is working the same as $interval was
    ErcBooksReadService.prototype.incrementOverDuration = function (serviceProp, startVal, endVal, duration, cb) {
        var _this = this;
        var event = new CustomEvent('books-read-update', {});
        // endVal = 500;
        if (!cb) {
            cb = function () { };
        }
        if (!startVal || startVal === endVal) {
            this[serviceProp] = endVal;
            document.dispatchEvent(event);
            return;
        }
        this[serviceProp] = startVal;
        var subDuration = Math.floor(duration / (endVal - startVal));
        var bookThisWeekInterval = Object(rxjs__WEBPACK_IMPORTED_MODULE_1__["interval"])(subDuration);
        var bookThisWeekIntervalSubscription = bookThisWeekInterval.subscribe(function (n) {
            if (_this[serviceProp] >= endVal) {
                bookThisWeekIntervalSubscription.unsubscribe();
                cb();
            }
            else {
                _this[serviceProp] += 1;
                document.dispatchEvent(event);
            }
        });
    };
    ErcBooksReadService.prototype.pingForBooksRead = function () {
        var _this = this;
        this.data
            .get('WebReadingChallenge', 'noAuthTotalBooksReadByStudents', {})
            .then(function (data) {
            if (data &&
                data.result &&
                parseInt(data.result.bookCount) > 0) {
                var booksTarget = parseInt(data.result.bookCount);
                var booksStart = 0;
                if (_this.booksReadData) {
                    booksStart = _this.booksReadData;
                }
                else {
                    booksStart = booksTarget;
                }
                _this.incrementOverDuration('booksRead', booksStart, booksTarget, _this.pingPeriod);
                _this.booksReadData = booksTarget;
            }
        });
    };
    // TODO: never used??
    // private getBooksRead() {
    //   return this.booksReadData;
    // }
    // To hardset event status for testing ex: { hardStatus: 'eventRunning' }
    ErcBooksReadService.prototype.getEventStatus = function () {
        // return Data.get('WebReadingChallenge','noAuthGetReadingChallengeStatus', { hardStatus: 'postEvent' });
        return this.data.get('WebReadingChallenge', 'noAuthGetReadingChallengeStatus');
    };
    /**                 ///////////////// TESTING THE API //////////////////
     *
     * 1. Ensure the constant READING_CHALLENGE_START - (WebReadingChallengeAPI.inc) is a timestamp prior to now.
     * 2. Ensure that the counter mock above is commented out.
     * 3. Check the network tab in the browser for calls to:
     *    class=WebReadingChallenge&method=noAuthTotalBooksReadByStudent on the service.pingPeriod interval
     */
    ErcBooksReadService.prototype.init = function () {
        var _this = this;
        // fake the event status
        // this.preEvent = true;
        // this.eventRunning = true;
        // this.postEvent = true;
        // return;
        // ---------------------
        //  * Only ping if the event is running and we are not mocking counter. constant READING_CHALLENGE_START - (WebReadingChallengeAPI.inc)
        if (!this.mockRunning) {
            // Ping API to find out if the event is running
            this.getEventStatus()
                .then(function (data) {
                if (data && data.result) {
                    _this.initialized = true;
                    var preEvent = data.result.eventStatus === 'preEvent';
                    var eventRunning = data.result.eventStatus === 'eventRunning';
                    var postEvent = data.result.eventStatus === 'postEvent';
                    if (preEvent) {
                        _this.preEvent = true;
                    }
                    else if (eventRunning) {
                        // Initial ping
                        _this.pingForBooksRead();
                        _this.eventRunning = true;
                        // Ping at interval
                        // TODO: double check this $interval swap also
                        // const pingInterval = interval(this.pingPeriod)
                        _this.mockReadingInterval.subscribe(function (n) {
                            _this.pingForBooksRead();
                        });
                    }
                    else if (postEvent) {
                        // Just ping once for the final count
                        _this.postEvent = true;
                        _this.pingForBooksRead();
                    }
                    else {
                        // no event is present, reroute to homepage.
                    }
                }
            })
                .catch(function (err) { return console.log(err); });
        }
    };
    ErcBooksReadService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root',
        }),
        __metadata("design:paramtypes", [_data_service__WEBPACK_IMPORTED_MODULE_2__["DataService"]])
    ], ErcBooksReadService);
    return ErcBooksReadService;
}());



/***/ }),

/***/ "./src/app/core/services/gift.service.ts":
/*!***********************************************!*\
  !*** ./src/app/core/services/gift.service.ts ***!
  \***********************************************/
/*! exports provided: GiftService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "GiftService", function() { return GiftService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _services_logsly_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @services/logsly.service */ "./src/app/core/services/logsly.service.ts");
/* harmony import */ var _services_data_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @services/data.service */ "./src/app/core/services/data.service.ts");
/* harmony import */ var _services_promo_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @services/promo.service */ "./src/app/core/services/promo.service.ts");
/* harmony import */ var _services_angularjs_translator_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @services/angularjs-translator.service */ "./src/app/core/services/angularjs-translator.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};





var GiftService = /** @class */ (function () {
    function GiftService(data, promo, logsly, ng1Translator) {
        this.data = data;
        this.promo = promo;
        this.logsly = logsly;
        this.ng1Translator = ng1Translator;
        this.devKey = 'pk_test_4Wy9ZuNal2fDNcMu9o1QcdBD';
        this.prodKey = 'pk_live_4Wy94k6t1RpVKUu2VdsAbwem';
        this.flowStarted = false;
        this.productId = null;
        this.productData = null;
        this.selectedProduct = null;
        this.user = {};
        this.sendGift = false;
        this.ribbonText = 'GIVE THE SMARTEST GIFT';
        if (Stripe && Stripe.setPublishableKey) {
            if (Globals.GLOBAL_DEV_MODE == 1) {
                Stripe.setPublishableKey(this.devKey);
            }
            else {
                Stripe.setPublishableKey(this.prodKey);
            }
        }
    }
    GiftService.prototype.init = function () {
        this.productId = null;
        this.productData = null;
        this.selectedProduct = null;
        this.user = {};
        this.sendGift = false;
    };
    GiftService.prototype.startGiftFlow = function () {
        if (!this.flowStarted) {
            this.flowStarted = true;
            // tony 3-19 the following line was this
            // this.logsly.track('gift_flow', 'website', "step_0");
            // logsly.track takes 4 arguments in the following signature
            // eventAction: string, eventCategory: string, eventLabel: string | number, eventValue: any
            // adding blank last value for now to not disrupt existing data
            this.logsly.track('gift_flow', 'website', 'step_0', '');
        }
    };
    GiftService.prototype.getGiftProductData = function () {
        var _this = this;
        var promo = 0;
        // if ($stateParams.promo) {
        //     promo = $stateParams.promo;
        //     return fetchData();
        // }
        if (this.ng1Translator.translations[this.ng1Translator.ANGULARJS_STATE_PARAMS_SERVICE] &&
            this.ng1Translator.translations[this.ng1Translator.ANGULARJS_STATE_PARAMS_SERVICE].promo) {
            promo = this.ng1Translator.translations[this.ng1Translator.ANGULARJS_STATE_PARAMS_SERVICE].promo;
            return this.fetchData(promo);
        }
        else {
            return this.promo.getCurrentPromoData().then(function (data) {
                // Tony 03-19; this is currently not functional
                // only banner info will come back from backend not gift data
                // if (data && data.gift) {
                //   promo = data.gift.promo;
                //   service.ribbonText = data.gift.ribbonText || service.ribbonText;
                //   service.savingsText = data.gift.savingsText || service.savingsText;
                // }
                return _this.fetchData(promo);
            });
        }
    };
    GiftService.prototype.fetchData = function (promo) {
        var _this = this;
        if (!this.productData) {
            return this.data.get('Website', 'noAuthGiftProductData', { promo: promo }).then(function (data) {
                _this.productData = data.result;
                return _this.productData;
            });
        }
        else {
            return Promise.resolve(this.productData);
        }
    };
    GiftService.prototype.selectProduct = function (productId) {
        // https://stackoverflow.com/questions/40349987/how-to-suppress-typescript-error-ts2533-object-is-possibly-null-or-undefine
        if (!productId && !this.productData) {
            return;
        }
        this.productId = productId || this.productData[1] && this.productData[1].modelId;
        for (var i = 0; i < this.productData.length; i++) {
            var product = this.productData[i];
            if (product.modelId == productId) {
                this.selectedProduct = product;
                break;
            }
        }
    };
    GiftService.prototype.getUserData = function () {
        return this.user;
    };
    GiftService.prototype.setUserData = function (data) {
        this.user = data;
    };
    GiftService.prototype.setSendGift = function (val) {
        this.sendGift = val;
    };
    GiftService.prototype.getSendGift = function () {
        return this.sendGift;
    };
    GiftService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [_services_data_service__WEBPACK_IMPORTED_MODULE_2__["DataService"],
            _services_promo_service__WEBPACK_IMPORTED_MODULE_3__["PromoService"],
            _services_logsly_service__WEBPACK_IMPORTED_MODULE_1__["LogslyService"],
            _services_angularjs_translator_service__WEBPACK_IMPORTED_MODULE_4__["AngularjsTranslatorService"]])
    ], GiftService);
    return GiftService;
}());



/***/ }),

/***/ "./src/app/core/services/local-storage.service.ts":
/*!********************************************************!*\
  !*** ./src/app/core/services/local-storage.service.ts ***!
  \********************************************************/
/*! exports provided: LocalStorageService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LocalStorageService", function() { return LocalStorageService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _window_ref_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./window-ref.service */ "./src/app/core/services/window-ref.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


var LocalStorageService = /** @class */ (function () {
    function LocalStorageService(Window) {
        this.Window = Window;
        this.ls = this.Window.nativeWindow.localStorage;
    }
    LocalStorageService.prototype.get = function (key) {
        if (!this.storageAvailable()) {
            return false;
        }
        var val = this.ls.getItem(key);
        return val ? JSON.parse(val) : undefined;
    };
    LocalStorageService.prototype.set = function (key, data) {
        if (!this.storageAvailable()) {
            return false;
        }
        var val = JSON.stringify(data);
        try {
            this.ls.setItem(key, val);
            return true;
        }
        catch (e) {
            return e instanceof DOMException && (
            // everything except Firefox
            e.code === 22 ||
                // Firefox
                e.code === 1014 ||
                // test name field too, because code might not be present
                // everything except Firefox
                e.name === 'QuotaExceededError' ||
                // Firefox
                e.name === 'NS_ERROR_DOM_QUOTA_REACHED') &&
                // acknowledge QuotaExceededError only if there's something already stored
                this.ls.length !== 0;
        }
    };
    LocalStorageService.prototype.remove = function (key) {
        if (!this.storageAvailable()) {
            return false;
        }
        this.ls.removeItem(key);
        return true;
    };
    LocalStorageService.prototype.clear = function () {
        if (!this.storageAvailable()) {
            return false;
        }
        this.ls.clear();
        return true;
    };
    // checks if current browser supports localStorage
    LocalStorageService.prototype.storageAvailable = function () {
        try {
            var x = '__storage_test__';
            this.ls.setItem(x, x);
            this.ls.removeItem(x);
            return true;
        }
        catch (e) {
            return e instanceof DOMException && (
            // everything except Firefox
            e.code === 22 ||
                // Firefox
                e.code === 1014 ||
                // test name field too, because code might not be present
                // everything except Firefox
                e.name === 'QuotaExceededError' ||
                // Firefox
                e.name === 'NS_ERROR_DOM_QUOTA_REACHED') &&
                // acknowledge QuotaExceededError only if there's something already stored
                this.ls.length !== 0;
        }
    };
    LocalStorageService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [_window_ref_service__WEBPACK_IMPORTED_MODULE_1__["WindowRefService"]])
    ], LocalStorageService);
    return LocalStorageService;
}());



/***/ }),

/***/ "./src/app/core/services/logging-source-translation.service.ts":
/*!*********************************************************************!*\
  !*** ./src/app/core/services/logging-source-translation.service.ts ***!
  \*********************************************************************/
/*! exports provided: LoggingSourceTranslationService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LoggingSourceTranslationService", function() { return LoggingSourceTranslationService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _services_angularjs_translator_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @services/angularjs-translator.service */ "./src/app/core/services/angularjs-translator.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


/*
/  this service is a parser
/  to take all the logs throughout the app
/  and make the source string constant among
/  this web client as well as across the mobile
/  clients it's more just a standardization
/  than any real rhyme or reason
*/
var LoggingSourceTranslationService = /** @class */ (function () {
    function LoggingSourceTranslationService(ng1Translator) {
        var _this = this;
        this.ng1Translator = ng1Translator;
        this.browseSection = null;
        // TODO, figure out what the real solution to this is.
        setTimeout(function () {
            if (_this.ng1Translator.translations[_this.ng1Translator.ANGULARJS_STATE_SERVICE]) {
                _this.stateObj = _this.ng1Translator.translations[_this.ng1Translator.ANGULARJS_STATE_SERVICE];
            }
        });
        this.browseDataObject = this.ng1Translator.translations[this.ng1Translator.BROWSESERVICE_BROWSEDATA];
    }
    LoggingSourceTranslationService.prototype.translateSourceString = function (source, section, rowTitle, rowIndex, sourceId, parentLoggingContext, tabName, isFeaturedBanner, contentTitle) {
        rowTitle = this.getBrowseSectionRowTitle(rowTitle, rowIndex, source);
        if (!section) {
            section = this.getBrowseSection();
        }
        source = !!source ? source.toLowerCase().replace(/\s/g, '_') : null;
        rowIndex = this.adjustRowIndexToOneBased(rowTitle, rowIndex, isFeaturedBanner);
        source = this.adjustMyLibrarySource(source);
        if (parentLoggingContext === 'featured_collection') {
            return this.buildSourceString('featured_collection', sourceId);
        }
        else if (source === 'user-collection') {
            return this.buildSourceString('collection', sourceId);
        }
        else if (parentLoggingContext === 'reccommendRowVideo') {
            return this.buildSourceString('video', 'related', tabName);
        }
        else if (parentLoggingContext === 'recommendPage') {
            return 'book_end';
        }
        else if (parentLoggingContext === 'reccommendRow') {
            return 'recommend_row';
        }
        else if (source === 'standalone-quiz' && parentLoggingContext === 'quiz') {
            return this.buildSourceString('quiz', 'related', 'More Like This');
        }
        else if (source === 'assignments') {
            return 'mailbox';
        }
        else if (source === 'dashboard.activity') {
            return 'dashboard_activity';
        }
        else if ((source === 'browse' || source === 'read') &&
            // TODO: isFeaturedBanner function would be cleaner
            (parentLoggingContext !== 'featured_banner' && rowTitle !== 'FeaturedBanner')) {
            source = 'browse'; // for those instantiated under a read overlay (in the read state)
            return this.buildSourceString(source, section, rowTitle);
        }
        else if (source === 'original') {
            return this.buildSourceString(source, null, contentTitle);
        }
        else { // default. not sure what would fall through, things currently are though
            // console.log('falling through')
            return source;
        }
    };
    LoggingSourceTranslationService.prototype.buildSourceString = function (source, appendOne, appendTwo) {
        if (!appendOne && !appendTwo) {
            return source;
        }
        if (appendOne) {
            appendOne = !!appendOne && typeof appendOne !== 'number' ?
                appendOne.toLowerCase().replace(/\s/g, '_') :
                appendOne;
        }
        if (appendTwo) {
            appendTwo = !!appendTwo && typeof appendTwo !== 'number' ?
                appendTwo.toLowerCase().replace(/\s/g, '_') :
                appendTwo;
        }
        source = !!appendOne ? source + '|' + appendOne : source + '|null';
        source = !!appendTwo ? source + '|' + appendTwo : source;
        return source;
    };
    LoggingSourceTranslationService.prototype.adjustRowIndexToOneBased = function (rowTitle, rowIndex, isFeaturedBanner) {
        if (rowIndex === undefined || rowIndex === null) {
            return -1;
        }
        else if (rowIndex === 0 && !!rowTitle &&
            (rowTitle.slice(0, 13) === 'FeaturedPanel' || rowTitle === 'FeaturedBanner')) {
            return 0;
        }
        else {
            return rowIndex + 1;
        }
    };
    LoggingSourceTranslationService.prototype.adjustMyLibrarySource = function (source) {
        if (!this.stateObj) {
            return source;
        }
        var splitState = this.stateObj.current.name.split('.');
        if (splitState.length > 1 && splitState[0] === 'my-library') {
            source = splitState[1];
            if (source === 'recent-reads') {
                source = 'recent';
            }
        }
        return source;
    };
    LoggingSourceTranslationService.prototype.getBrowseSectionRowTitle = function (rowTitle, rowIndex, source) {
        if (!rowTitle && rowIndex >= 0 &&
            source === 'browse' &&
            this.browseDataObject.rows[rowIndex]) {
            return rowIndex >= 0 ?
                this.browseDataObject.rows[rowIndex].title ||
                    this.browseDataObject.rows[rowIndex].name :
                null;
        }
        else {
            return rowTitle || null;
        }
    };
    LoggingSourceTranslationService.prototype.setBrowseSection = function (section) {
        this.browseSection = section;
    };
    LoggingSourceTranslationService.prototype.getBrowseSection = function () {
        return this.browseSection;
    };
    LoggingSourceTranslationService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [_services_angularjs_translator_service__WEBPACK_IMPORTED_MODULE_1__["AngularjsTranslatorService"]])
    ], LoggingSourceTranslationService);
    return LoggingSourceTranslationService;
}());



/***/ }),

/***/ "./src/app/core/services/logsly.service.ts":
/*!*************************************************!*\
  !*** ./src/app/core/services/logsly.service.ts ***!
  \*************************************************/
/*! exports provided: LogslyService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LogslyService", function() { return LogslyService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _data_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./data.service */ "./src/app/core/services/data.service.ts");
/* harmony import */ var _local_storage_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./local-storage.service */ "./src/app/core/services/local-storage.service.ts");
/* harmony import */ var _window_ref_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./window-ref.service */ "./src/app/core/services/window-ref.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};




var LogslyService = /** @class */ (function () {
    function LogslyService(data, localStorage, Window) {
        this.data = data;
        this.localStorage = localStorage;
        this.Window = Window;
        this.window = this.Window.nativeWindow;
        // TODO: make sure all the Logsly.logs are gone
        // and then remove this. we have the gulp task to strip out
        // the console.logs from prod
        this.log = (Globals.GLOBAL_DEV_MODE || Globals.GLOBAL_STAGING_MODE) ?
            console.log.bind(window.console) :
            function () { };
    }
    LogslyService.prototype.track = function (eventAction, eventCategory, eventLabel, eventValue) {
        if (!this.window.ga)
            return;
        this.window.ga('send', 'event', eventCategory, eventAction, eventLabel, eventValue);
    };
    LogslyService.prototype.updateDeviceInfo = function () {
        var _this = this;
        if (!this.localStorage.get('epic_device_key')) {
            var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
                var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });
            this.data.get('WebAccount', 'updateAccountDevice', { uuid: uuid }).then(function (data) {
                _this.localStorage.set('epic_device_key', uuid);
            });
        }
    };
    // todo: product here is the subscription product which is obviously a particular object
    // it's the gift one in one case, and it's the regular one in another case so it's a
    // project which is debatably not worth the time.
    LogslyService.prototype.logTransaction = function (accountId, product) {
        if (!this.window.ga) {
            console.warn('ga = ', this.window.ga);
            return;
        }
        if (!product) {
            console.warn('Transaction could not be logged, product = ', product);
            return;
        }
        var pid;
        var price;
        // Gift
        if (!product.productId) {
            pid = '';
            price = product.price / 100;
            // Subscription product
        }
        else {
            pid = '-' + product.productId;
            price = product.price;
        }
        var transId = accountId + pid + '-' + Math.floor(Date.now() / 1000);
        this.window.ga('ecommerce:addTransaction', {
            'id': transId,
            'affiliation': 'Epic!',
            'revenue': price
        });
        this.window.ga('ecommerce:addItem', {
            'id': transId,
            'name': product.name,
            'sku': product.productId || 'gift',
            'category': product.recurring ? 'Recurring' : 'Term',
            'price': price,
            'quantity': '1'
        });
        this.window.ga('ecommerce:send');
    };
    LogslyService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [_data_service__WEBPACK_IMPORTED_MODULE_1__["DataService"],
            _local_storage_service__WEBPACK_IMPORTED_MODULE_2__["LocalStorageService"],
            _window_ref_service__WEBPACK_IMPORTED_MODULE_3__["WindowRefService"]])
    ], LogslyService);
    return LogslyService;
}());



/***/ }),

/***/ "./src/app/core/services/message-handler.service.ts":
/*!**********************************************************!*\
  !*** ./src/app/core/services/message-handler.service.ts ***!
  \**********************************************************/
/*! exports provided: MessageHandlerService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MessageHandlerService", function() { return MessageHandlerService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var MessageHandlerService = /** @class */ (function () {
    function MessageHandlerService() {
        // Handles the messages from Data Service, notifies through an Observer Pattern
        // Observers can be any object that subscribe themselves to MessageHandler
        // Service AND implements a handleMessage method
        this.observers = [];
    }
    MessageHandlerService.prototype.subscribeObserver = function (observer) {
        this.observers.push(observer);
    };
    MessageHandlerService.prototype.unsubscribeObserver = function (observer) {
        var index = this.observers.indexOf(observer);
        if (index > -1) {
            this.observers.splice(index, 1);
        }
    };
    MessageHandlerService.prototype.handleMessages = function (messages) {
        var _this = this;
        if (!messages || messages.length < 1) {
            return;
        }
        messages.forEach(function (message) {
            _this.notifyAll(message);
        });
    };
    MessageHandlerService.prototype.notifyAll = function (message) {
        for (var i = 0; i < this.observers.length; i++) {
            this.observers[i].handleMessage(message);
        }
    };
    MessageHandlerService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [])
    ], MessageHandlerService);
    return MessageHandlerService;
}());



/***/ }),

/***/ "./src/app/core/services/optimize.service.ts":
/*!***************************************************!*\
  !*** ./src/app/core/services/optimize.service.ts ***!
  \***************************************************/
/*! exports provided: OptimizeService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "OptimizeService", function() { return OptimizeService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _services_window_ref_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @services/window-ref.service */ "./src/app/core/services/window-ref.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


var OptimizeService = /** @class */ (function () {
    function OptimizeService(Window) {
        this.Window = Window;
        this.window = this.Window.nativeWindow;
    }
    // also here is an interesting idea on how/where to put this when we
    // implement an optimize test via datalayer push activation
    // http://blog.stack.foundation/2017/06/02/using-google-optimize-with-angular/
    // (vs our old watcher implementation, left commented below)
    // here's a pass at a basic implementation
    OptimizeService.prototype.sendDataLayerActivationEvent = function () {
        if (this.isReady()) {
            this.window.dataLayer.push({ event: 'optimize.activate' });
            return true;
        }
        else {
            return false;
        }
    };
    OptimizeService.prototype.isReady = function () {
        return (this.window.gaData &&
            this.window.gaData[Globals.GID] &&
            this.window.dataLayer);
    };
    OptimizeService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root',
        }),
        __metadata("design:paramtypes", [_services_window_ref_service__WEBPACK_IMPORTED_MODULE_1__["WindowRefService"]])
    ], OptimizeService);
    return OptimizeService;
}());



/***/ }),

/***/ "./src/app/core/services/profile.service.ts":
/*!**************************************************!*\
  !*** ./src/app/core/services/profile.service.ts ***!
  \**************************************************/
/*! exports provided: ProfileService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProfileService", function() { return ProfileService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _account_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./account.service */ "./src/app/core/services/account.service.ts");
/* harmony import */ var _data_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./data.service */ "./src/app/core/services/data.service.ts");
/* harmony import */ var _local_storage_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./local-storage.service */ "./src/app/core/services/local-storage.service.ts");
/* harmony import */ var _session_storage_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./session-storage.service */ "./src/app/core/services/session-storage.service.ts");
/* harmony import */ var _models_profile_Profile__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @models/profile/Profile */ "./src/app/core/models/profile/Profile.ts");
/* harmony import */ var _models_profile_ChildProfile__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @models/profile/ChildProfile */ "./src/app/core/models/profile/ChildProfile.ts");
/* harmony import */ var _models_profile_EducatorProfile__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @models/profile/EducatorProfile */ "./src/app/core/models/profile/EducatorProfile.ts");
/* harmony import */ var _models_profile_ParentProfile__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @models/profile/ParentProfile */ "./src/app/core/models/profile/ParentProfile.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};









var ProfileService = /** @class */ (function () {
    function ProfileService(accountService, Data, localStorage, sessionStorage) {
        var _this = this;
        this.accountService = accountService;
        this.Data = Data;
        this.localStorage = localStorage;
        this.sessionStorage = sessionStorage;
        this.SUBSCRIPTION_STATUS_FREE_TRIAL = 0;
        this.SUBSCRIPTION_STATUS_NOT_SUBSCRIBED = 1;
        this.SUBSCRIPTION_STATUS_SUBSCRIBED = 2;
        this.HOME_ACCESS_STATUS_CAN_ENABLE = 0;
        this.HOME_ACCESS_STATUS_PENDING = 1;
        this.HOME_ACCESS_STATUS_ENABLED = 2;
        this.HOME_ACCESS_STATUS_UNKNOWN = 3;
        this.isLoggedIn = false;
        this.parentProfile = null;
        this.currentProfile = new _models_profile_Profile__WEBPACK_IMPORTED_MODULE_5__["Profile"]({});
        this.childProfiles = [];
        this.classroomGroups = [];
        this.initialized = false;
        this.passwordChecked = false;
        this.profileIsAuthed = false;
        /**
         * Get data for currently logged in profile and create a fresh Profile
         */
        this.getCurrentProfile = function () {
            if (Globals.GLOBAL_IS_AUTHED == 1) {
                return _this.Data.get('WebUser', 'getProfileData').then(function (data) {
                    if (data && data.result) {
                        _this.currentProfile = _this.getNewProfile(data.result); // Set currentProfile
                        _this.findProfile(data.result.id, _this.currentProfile); // Replace the reference in parent/childProfiles with this new profile
                        // Indicate that data has been fetched/set 
                        _this.initialized = true;
                    }
                    return data;
                });
            }
            return null;
        };
        this.deleteProfiles = function (profiles) {
            var i, userIds = [], length = profiles.length;
            for (i = 0; i < length; i++) {
                userIds.push(profiles[i].id);
            }
            return _this.Data.get('WebAccount', 'removeProfiles', { userIds: userIds }).then(function (data) {
                if (data && data.result && data.result.profiles)
                    _this.setChildProfiles(data.result.profiles);
                return data;
            });
        };
        this.archiveProfiles = function (profiles) {
            var i, userIds = [], length = profiles.length;
            for (i = 0; i < length; i++) {
                userIds.push(profiles[i].id);
            }
            return _this.Data.get('WebAccount', 'archiveEducatorProfiles', { userIds: userIds }).then(function (data) {
                if (data && data.result && data.result.profiles)
                    _this.setChildProfiles(data.result.profiles);
                return data;
            });
        };
        /* Params
        *  userIds: array, legacy it came in as a single item and as a string
        *  email: string
        */
        this.transferProfiles = function (userIds, email) {
            return _this.Data.post('WebUserAccountTransfer', 'requestUserTransferToEmail', {
                userIds: userIds,
                email: email
            }).then(function (data) {
                return data;
            });
        };
    }
    /**
     * Factory: creates the appropriate Profile
     * @param profileData profile data from endpoint
     */
    ProfileService.prototype.getNewProfile = function (profileData) {
        if (!profileData) {
            return new _models_profile_Profile__WEBPACK_IMPORTED_MODULE_5__["Profile"]({});
        }
        else if (profileData.isParent) {
            return profileData.accountType === 1 ? new _models_profile_EducatorProfile__WEBPACK_IMPORTED_MODULE_7__["EducatorProfile"](profileData) : new _models_profile_ParentProfile__WEBPACK_IMPORTED_MODULE_8__["ParentProfile"](profileData);
        }
        else {
            return new _models_profile_ChildProfile__WEBPACK_IMPORTED_MODULE_6__["ChildProfile"](profileData);
        }
    };
    /**
     * Retrieves all profile data and sets them to this.childProfiles
     * @param includeStats boolean: pull reading stats for users or not
     */
    ProfileService.prototype.reloadProfiles = function (includeStats) {
        var _this = this;
        if (includeStats === undefined) {
            includeStats = 1;
        }
        this.childProfiles = [];
        return this.loadProfiles(null, null, includeStats).then(function (data) { _this.setChildProfiles(data); });
    };
    // Get and set all profiles including stats
    ProfileService.prototype.loadProfileStats = function () {
        var _this = this;
        var includeStats = 1;
        return this.loadProfiles(null, null, includeStats).then(function (data) { _this.setChildProfiles(data); });
    };
    /**
     * Get profile data from server
     * @param groupId
     * @param excludeParent
     * @param includeStats boolean: include reading stats
     */
    ProfileService.prototype.loadProfiles = function (groupId, excludeParent, includeStats) {
        var _this = this;
        var params = {};
        if (groupId)
            params.groupId = groupId;
        if (excludeParent)
            params.excludeParent = excludeParent;
        params.includeStats = (includeStats === undefined) ? 1 : includeStats;
        return this.Data.get('WebAccount', 'getProfiles', params).then(function (data) {
            return _this.buildProfiles(data.result);
        });
    };
    ProfileService.prototype.loadClassroomGroups = function () {
        var _this = this;
        return this.Data.get('WebClassroomGroup', 'getClassroomGroupsForAccount').then(function (data) {
            _this.classroomGroups = (data && data.result) ? data.result : [];
        });
    };
    /**
     *
     * @param data Array of Profile or profile data
     */
    ProfileService.prototype.buildProfiles = function (data) {
        if (!data)
            return [];
        var profile, profiles = [], length = data.length;
        for (var i = 0; i < length; i++) {
            profile = data[i];
            profile = (profile instanceof _models_profile_Profile__WEBPACK_IMPORTED_MODULE_5__["Profile"]) ? profile : this.getNewProfile(profile);
            profiles.push(profile);
        }
        return profiles;
    };
    ProfileService.prototype.setChildProfiles = function (profiles) {
        profiles = this.buildProfiles(profiles);
        this.childProfiles = [];
        var profile, length = profiles.length;
        for (var i = 0; i < length; i++) {
            profile = profiles[i];
            if (profile.isParent) {
                this.parentProfile = profile;
            }
            else {
                this.childProfiles.push(profile);
            }
        }
        return this.childProfiles;
    };
    ProfileService.prototype.getChildProfilesWithoutGuest = function () {
        return this.childProfiles.filter(function (p) { return !(p.firstName.toLowerCase() === 'guest' && p.isDefault); });
    };
    /**
     * Return child profiles with the current profile first
     */
    ProfileService.prototype.getChildProfilesSorted = function () {
        var _this = this;
        var profiles = [];
        this.childProfiles.forEach(function (p, index) {
            if (_this.currentProfile && (p.id === _this.currentProfile.id)) {
                profiles.unshift(p);
            }
            else {
                profiles.push(p);
            }
        });
        return profiles;
    };
    /**
     * Create new child profile
     * @param profile
     */
    ProfileService.prototype.createProfile = function (profile) {
        var _this = this;
        profile = JSON.stringify(profile);
        return this.Data.post('WebAccount', 'createChildProfile', { profile: profile }).then(function (data) {
            if (data && data.result && data.result.newProfile) {
                _this.childProfiles.push(_this.getNewProfile(data.result.newProfile));
            }
            return data;
        });
    };
    /**
     *
     * @param profile Profile to update/set -- if updates is not passed in, use this
     * @param updates Optional Object of properties to update (IGNORE updates to Profile) -
     *      this is to prevent us from blowing away changes made to profiles from other sessions
     *      (if we make changes to the profile object and pass it in to try and update, it's possible
     *      that some of the data may have changed since we loaded that profile)
     */
    ProfileService.prototype.updateProfile = function (profile, updates) {
        var _this = this;
        if (!updates) {
            return this.Data.post('WebUser', 'updateProfile', { profile: JSON.stringify(profile) }).then(function (updatedProfileData) {
                if (updatedProfileData && updatedProfileData.result && updatedProfileData.result.id === profile.id) {
                    profile.setAllProfileData(updatedProfileData.result);
                }
                return updatedProfileData;
            });
        }
        else {
            // could remove the getProfileDataById call if updateProfile just updates what is passed in
            return this.Data.post('WebAccount', 'getProfileDataById', { userId: profile.id }).then(function (data) {
                if (data && data.result && data.result.id === profile.id) {
                    var profileUpdates = data.result;
                    var updateItems = Object.entries(updates);
                    for (var _i = 0, updateItems_1 = updateItems; _i < updateItems_1.length; _i++) {
                        var _a = updateItems_1[_i], key = _a[0], val = _a[1];
                        profileUpdates[key] = val;
                    }
                    return _this.Data.post('WebUser', 'updateProfile', { profile: JSON.stringify(profileUpdates) }).then(function (updatedProfileData) {
                        if (updatedProfileData && updatedProfileData.result && updatedProfileData.result.id === profile.id) {
                            profile.setProfileData(updatedProfileData.result); // Update directly on the Profile object
                        }
                        return updatedProfileData;
                    });
                }
                else {
                    bbb("Failed to update profile");
                    return null;
                }
            });
        }
    };
    /**
     * Update the Profile's data with the most up to date
     * @param profile Profile to update
     */
    ProfileService.prototype.getProfileData = function (profile) {
        return this.Data.post('WebAccount', 'getProfileDataById', { userId: profile.id }).then(function (data) {
            if (data && data.result) {
                profile.setAllProfileData(data.result);
            }
        });
    };
    /**
     * Get the most up to date stats (book stats)
     */
    ProfileService.prototype.updateProfileStats = function () {
        var _this = this;
        if (Globals.GLOBAL_IS_AUTHED == 1 && this.currentProfile) {
            return this.Data.get('WebUserActivity', 'getUserActivitySummaryByUserId').then(function (data) {
                if (data.result && _this.currentProfile) {
                    _this.currentProfile.setProfileStats(data.result);
                }
                return data;
            });
        }
        return;
    };
    // Select a current profile
    ProfileService.prototype.selectProfile = function (userId) {
        var _this = this;
        this.initialized = false;
        return this.Data.get('WebAccount', 'selectProfile', { userId: userId }).then(function (data) {
            if (data && data.result) {
                var selectedProfile = _this.getNewProfile(data.result);
                _this.findProfile(userId, selectedProfile);
                _this.currentProfile = selectedProfile;
                _this.renewTimestamp();
                return data.result;
            }
            // var selectedProfile = this.findProfile(userId);
            // if (selectedProfile) {
            //     this.currentProfile = selectedProfile;
            // }
            // this.renewTimestamp();
            // return data.result;
        });
    };
    /**
     *
     * @param userId Profile to find amongst parent/childProfiles
     * @param replacementProfile Replace the reference with this new profile
     */
    ProfileService.prototype.findProfile = function (userId, replacementProfile) {
        if (this.parentProfile && this.parentProfile.id === userId) {
            if (replacementProfile) {
                this.parentProfile = replacementProfile;
            }
            return this.parentProfile;
        }
        else {
            for (var i = 0; i < this.childProfiles.length; i++) {
                if (this.childProfiles[i].id === userId) {
                    if (replacementProfile)
                        this.childProfiles[i] = replacementProfile;
                    return this.childProfiles[i];
                }
            }
            // return this.childProfiles.find((p) => {return p.id === userId});
        }
        return null;
    };
    /**
     * Get the parent Profile of the authed account
     */
    ProfileService.prototype.getParentProfile = function () {
        var _this = this;
        return this.Data.get('WebAccount', 'getParentProfile').then(function (data) {
            return _this.getNewProfile(data.result);
        });
    };
    // Group methods
    ProfileService.prototype.createGroup = function (name, userIds) {
        var _this = this;
        return this.Data.post('WebClassroomGroup', 'createClassroomGroup', {
            name: name,
            userIds: userIds
        }).then(function (data) {
            if (data && data.result) {
                _this.classroomGroups = data.result;
                return _this.classroomGroups;
            }
            return null;
        });
    };
    ProfileService.prototype.selectGroup = function (groupId) {
        var _this = this;
        this.childProfiles = [];
        var params = {};
        if (groupId)
            params[groupId] = groupId;
        return this.Data.get('WebAccount', 'selectGroup', params).then(function (data) {
            return _this.setChildProfiles(data.result);
        });
    };
    ProfileService.prototype.renameGroup = function (groupId, name) {
        var _this = this;
        return this.Data.post('WebClassroomGroup', 'renameClassroomGroup', {
            groupId: groupId,
            name: name
        }).then(function (data) {
            if (data && data.result) {
                _this.classroomGroups = data.result;
                return _this.classroomGroups;
            }
            return null;
        });
    };
    ProfileService.prototype.deleteGroup = function (groupId) {
        var _this = this;
        return this.Data.post('WebClassroomGroup', 'deleteClassroomGroup', {
            groupId: groupId
        }).then(function (data) {
            if (data && data.result) {
                _this.classroomGroups = data.result;
                return _this.classroomGroups;
            }
            return null;
        });
    };
    ProfileService.prototype.setProfilesForGroups = function (groupIds, addIds, removeIds) {
        var _this = this;
        var params = {
            groupIds: groupIds
        };
        if (addIds)
            params.addIds = addIds;
        if (removeIds)
            params['removeIds'] = removeIds;
        return this.Data.post('WebClassroomGroup', 'setProfilesForClassroomGroups', params).then(function (data) {
            if (data && data.result) {
                _this.classroomGroups = data.result;
                return _this.classroomGroups;
            }
            return null;
        });
    };
    ProfileService.prototype.setGroupsForProfiles = function (groupIds, userIds) {
        var _this = this;
        return this.Data.post('WebClassroomGroup', 'setGroupsForProfiles', {
            groupIds: groupIds,
            userIds: userIds
        }).then(function (data) {
            if (data && data.result) {
                _this.classroomGroups = data.result;
                return _this.classroomGroups;
            }
            return null;
        });
    };
    ProfileService.prototype.getGroupIdsForProfile = function (userId) {
        return this.Data.post('WebClassroomGroup', 'getClassroomGroupIdsByUserId', {
            userId: userId
        }).then(function (data) {
            if (data && data.result) {
                return data.result;
            }
        });
    };
    ProfileService.prototype.getProfilesInGroup = function (groupId) {
        var profiles = this.childProfiles.slice();
        if (!groupId)
            return profiles;
        var group = this.getGroupById(groupId) || {};
        group.userIds = group.userIds || [];
        var i, profile, members = [], length = profiles.length;
        for (i = 0; i < length; i++) {
            profile = profiles[i];
            if (group.userIds.indexOf(String(profile.id)) > -1) {
                members.push(profile);
            }
        }
        return members;
    };
    ProfileService.prototype.getProfilesNotInGroup = function (groupId) {
        var profiles = this.childProfiles.slice();
        if (!groupId)
            return [];
        var group = this.getGroupById(groupId) || {};
        group.userIds = group.userIds || [];
        var i, profile, nonMembers = [], length = profiles.length;
        for (i = 0; i < length; i++) {
            profile = profiles[i];
            if (group.userIds.indexOf(String(profile.id)) < 0) {
                nonMembers.push(profile);
            }
        }
        return nonMembers;
    };
    ProfileService.prototype.getGroupById = function (groupId) {
        var i, group, length = this.classroomGroups.length;
        for (i = 0; i < length; i++) {
            group = this.classroomGroups[i];
            if (group.id == groupId) {
                return group;
            }
        }
        return null;
    };
    ProfileService.prototype.getGroupByName = function (name) {
        var i, group, length = this.classroomGroups.length;
        for (i = 0; i < length; i++) {
            group = this.classroomGroups[i];
            if (group.name == name) {
                return group;
            }
        }
        return null;
    };
    // End group methods
    ProfileService.prototype.isFresh = function () {
        var isTeacher = false;
        if (this.currentProfile) {
            isTeacher = this.currentProfile.isParent &&
                this.accountService.isEducator() &&
                this.localStorage.get('eduAccountSkipProfileSelect');
        }
        var isFreshByTimeStamp = this.localStorage.get('date_profile_last_selected') > Math.floor(Date.now() / 1000);
        var isFreshByMobileAccountManage = this.sessionStorage.getSessionStorageWithKey('fromMobileRedirect');
        return isTeacher || isFreshByMobileAccountManage || isFreshByTimeStamp || this.isLoggedIn;
    };
    ProfileService.prototype.renewTimestamp = function () {
        this.isLoggedIn = true;
        this.localStorage.set('date_profile_last_selected', (Math.floor(Date.now() / 1000) + 60 * 15) + "");
    };
    ProfileService.prototype.invalidateTimestamp = function () {
        this.isLoggedIn = false;
        this.localStorage.set('date_profile_last_selected', null);
    };
    ProfileService.prototype.obfuscateId = function (profileId) {
        return profileId ? (parseInt(profileId) * 1111 + 2) : null;
    };
    ProfileService.prototype.unObfuscateId = function (obfuscatedId) {
        return obfuscatedId ? (parseInt(obfuscatedId) - 2) / 1111 : null;
    };
    ProfileService.prototype.daysSinceProfileWasCreated = function () {
        if (!this.currentProfile) {
            return null;
        }
        var profileDateCreated = this.currentProfile.dateCreated;
        var daysSinceProfileWasCreated = Math.floor(((Date.now() / 1000) - profileDateCreated) / 86400); // 60*60*24
        return daysSinceProfileWasCreated;
    };
    ProfileService.prototype.isTeacher = function () {
        return this.currentProfile && this.currentProfile.isParent && this.accountService.isEducator();
    };
    ProfileService.prototype.isValidEmail = function (email) {
        var pattern = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return !email || (pattern.test(email) && email.length <= 255);
    };
    ;
    // Benson testing some stuff to know when a profile is logged in,
    // not relying on current profile because current profile is filled when on profile select
    // profileIsAuthed
    ProfileService.prototype.setProfileIsAuthed = function (setting) {
        this.profileIsAuthed = setting;
    };
    ProfileService.prototype.getProfileIsAuthed = function () {
        return this.profileIsAuthed;
    };
    ProfileService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [_account_service__WEBPACK_IMPORTED_MODULE_1__["AccountService"],
            _data_service__WEBPACK_IMPORTED_MODULE_2__["DataService"],
            _local_storage_service__WEBPACK_IMPORTED_MODULE_3__["LocalStorageService"],
            _session_storage_service__WEBPACK_IMPORTED_MODULE_4__["SessionStorageService"]])
    ], ProfileService);
    return ProfileService;
}());



/***/ }),

/***/ "./src/app/core/services/promo.service.ts":
/*!************************************************!*\
  !*** ./src/app/core/services/promo.service.ts ***!
  \************************************************/
/*! exports provided: PromoService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PromoService", function() { return PromoService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _data_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./data.service */ "./src/app/core/services/data.service.ts");
/* harmony import */ var _session_storage_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./session-storage.service */ "./src/app/core/services/session-storage.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



;
var PromoService = /** @class */ (function () {
    function PromoService(data, sessionStorage) {
        this.data = data;
        this.sessionStorage = sessionStorage;
        this.TEACHER_OFFER_ANNUAL_ID_DEV = 34;
        this.TEACHER_OFFER_ANNUAL_ID_PROD = 25;
        this.livePromo = null;
        this.GENERIC_PAGE_PROMO = {
            sessionStorageKey: 'gen',
            productId: null
        };
        this.TEACHER_OFFER_MONTHLY = {
            sessionStorageKey: 'toff',
            productId: 20
        };
        this.TEACHER_OFFER_ANNUAL = {
            sessionStorageKey: 'toffAnn',
            productId: this.getTeacherOfferAnnualId() // 34 dev, 25 prod
        };
        this.TEACHER_OFFER_AFTER_HOURS = {
            sessionStorageKey: 'AHLinkInfo',
            productId: 20
        };
        // the currentLivePromos array is in the order of offer importance
        // ie if the user has activated more than one offer by landing on a page
        // and has more than one of these keys in their session storage
        // the offer they will be given will be in this order
        this.currentLivePromos = [
            this.TEACHER_OFFER_MONTHLY,
            this.TEACHER_OFFER_ANNUAL,
            this.TEACHER_OFFER_AFTER_HOURS,
        ];
        this.promoData = undefined;
    }
    PromoService.prototype.getTeacherOfferAnnualId = function () {
        return Globals.GLOBAL_DEV_MODE ? this.TEACHER_OFFER_ANNUAL_ID_DEV : this.TEACHER_OFFER_ANNUAL_ID_PROD;
    };
    PromoService.prototype.setLivePromo = function (promo) {
        this.livePromo = promo;
    };
    PromoService.prototype.getLivePromo = function () {
        return this.livePromo;
    };
    PromoService.prototype.getCurrentPromoData = function () {
        var _this = this;
        if (this.promoData) {
            return new Promise(function (resolve, reject) {
                resolve(_this.promoData);
            });
        }
        else {
            return this.data.get('WebsitePromo', 'noAuthCurrentWebsitePromotion', null)
                .then(function (data) {
                if (data && data.result) {
                    _this.promoData = data.result;
                }
                else {
                    _this.promoData = undefined;
                }
                return _this.promoData;
            });
        }
    };
    PromoService.prototype.setGenericPagePromo = function (productId) {
        if (!productId)
            return;
        this.GENERIC_PAGE_PROMO.productId = productId;
        this.currentLivePromos.unshift(this.GENERIC_PAGE_PROMO);
    };
    PromoService.prototype.removeGenericPagePromo = function () {
        this.GENERIC_PAGE_PROMO.productId = null;
        if (this.currentLivePromos[0] === this.GENERIC_PAGE_PROMO) {
            this.currentLivePromos.shift();
        }
    };
    PromoService.prototype.getGenericPageProductId = function () {
        if (this.currentLivePromos[0] === this.GENERIC_PAGE_PROMO) {
            return this.currentLivePromos[0].productId;
        }
    };
    // this method parses the items in session storage
    // into the order of the currentLivePromos 
    PromoService.prototype.getLocalPromoData = function () {
        var _this = this;
        var localPromoData = [];
        this.currentLivePromos.forEach(function (promoDef) {
            var promoSessionObj = _this.sessionStorage.getSessionStorageWithKey(promoDef.sessionStorageKey);
            if (promoSessionObj) {
                var obj = {};
                obj[promoDef.sessionStorageKey] = promoSessionObj;
                localPromoData.push(obj);
            }
        });
        return localPromoData;
    };
    PromoService.prototype.getHighestPriorityPromo = function () {
        // return generic page as first prio always
        var genericPageProductId = this.getGenericPageProductId();
        if (genericPageProductId) {
            this.GENERIC_PAGE_PROMO.productId = genericPageProductId;
            return this.GENERIC_PAGE_PROMO;
        }
        var localPromoData = this.getLocalPromoData();
        if (!localPromoData) {
            return null;
        }
        // bad 0N. real bad. for now anyway, both loops are short
        for (var i = 0; i < this.currentLivePromos.length; i++) {
            for (var j = 0; j < localPromoData.length; j++) {
                if (Object.keys(localPromoData[j])[0] === this.currentLivePromos[i].sessionStorageKey) {
                    return this.currentLivePromos[i];
                }
            }
        }
        return null;
    };
    PromoService.prototype.getPromoDetails = function (product) {
        if (!product || !product.sessionStorageKey)
            return undefined;
        return this.sessionStorage.getSessionStorageWithKey(product.sessionStorageKey);
    };
    PromoService.prototype.removePromosFromSessionStore = function () {
        var _this = this;
        this.currentLivePromos.forEach(function (promoObj) {
            if (_this.sessionStorage.getSessionStorageWithKey(promoObj.sessionStorageKey)) {
                _this.sessionStorage.removeSessionStorageKey(promoObj.sessionStorageKey);
            }
        });
    };
    PromoService.prototype.getAfterHoursLinkData = function () {
        return this.sessionStorage.getSessionStorageWithKey('AHLinkInfo');
    };
    PromoService.prototype.removeAfterHoursLinkData = function () {
        this.sessionStorage.removeSessionStorageKey('AHLinkInfo');
    };
    PromoService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [_data_service__WEBPACK_IMPORTED_MODULE_1__["DataService"],
            _session_storage_service__WEBPACK_IMPORTED_MODULE_2__["SessionStorageService"]])
    ], PromoService);
    return PromoService;
}());



/***/ }),

/***/ "./src/app/core/services/query-string.service.ts":
/*!*******************************************************!*\
  !*** ./src/app/core/services/query-string.service.ts ***!
  \*******************************************************/
/*! exports provided: QueryStringService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "QueryStringService", function() { return QueryStringService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _services_session_storage_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @services/session-storage.service */ "./src/app/core/services/session-storage.service.ts");
/* harmony import */ var _services_angularjs_translator_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @services/angularjs-translator.service */ "./src/app/core/services/angularjs-translator.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var QueryStringService = /** @class */ (function () {
    function QueryStringService(sessionStorage, ng1Translator) {
        this.sessionStorage = sessionStorage;
        this.ng1Translator = ng1Translator;
        this.supported = this.sessionStorage.sessionStorageIsSupported;
        this.queryParams = {};
    }
    Object.defineProperty(QueryStringService.prototype, "translatedLocationSearch", {
        get: function () {
            return (this.ng1Translator.translations[this.ng1Translator.ANGULARJS_LOCATION_SERVICE] &&
                this.ng1Translator.translations[this.ng1Translator.ANGULARJS_LOCATION_SERVICE].search());
        },
        enumerable: true,
        configurable: true
    });
    QueryStringService.prototype.sessionStoreQueryParams = function () {
        if (!this.supported) {
            return;
        }
        var queryParams = this
            .translatedLocationSearch;
        if (!queryParams) {
            return;
        }
        for (var _i = 0, _a = Object.keys(queryParams); _i < _a.length; _i++) {
            var prop = _a[_i];
            this.queryParams[prop] = queryParams[prop];
            this.sessionStorage.setSessionStorageWithKey(prop, queryParams[prop]);
        }
    };
    QueryStringService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root',
        }),
        __metadata("design:paramtypes", [_services_session_storage_service__WEBPACK_IMPORTED_MODULE_1__["SessionStorageService"],
            _services_angularjs_translator_service__WEBPACK_IMPORTED_MODULE_2__["AngularjsTranslatorService"]])
    ], QueryStringService);
    return QueryStringService;
}());



/***/ }),

/***/ "./src/app/core/services/redirect.service.ts":
/*!***************************************************!*\
  !*** ./src/app/core/services/redirect.service.ts ***!
  \***************************************************/
/*! exports provided: RedirectService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RedirectService", function() { return RedirectService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _window_ref_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./window-ref.service */ "./src/app/core/services/window-ref.service.ts");
/* harmony import */ var _services_data_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @services/data.service */ "./src/app/core/services/data.service.ts");
/* harmony import */ var _services_string_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @services/string.service */ "./src/app/core/services/string.service.ts");
/* harmony import */ var _services_account_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @services/account.service */ "./src/app/core/services/account.service.ts");
/* harmony import */ var _services_user_agent_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @services/user-agent.service */ "./src/app/core/services/user-agent.service.ts");
/* harmony import */ var _services_angularjs_translator_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @services/angularjs-translator.service */ "./src/app/core/services/angularjs-translator.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};







var RedirectService = /** @class */ (function () {
    function RedirectService(Window, data, accountService, userAgent, ng1Translator, stringService) {
        this.Window = Window;
        this.data = data;
        this.accountService = accountService;
        this.userAgent = userAgent;
        this.ng1Translator = ng1Translator;
        this.stringService = stringService;
        this.allowRedirect = true;
        this.lastState = "";
        this.lastParams = {};
        this.window = this.Window.nativeWindow;
    }
    Object.defineProperty(RedirectService.prototype, "translatedLocationUrl", {
        get: function () {
            return this.ng1Translator.translations[this.ng1Translator.ANGULARJS_LOCATION_SERVICE]
                && this.ng1Translator.translations[this.ng1Translator.ANGULARJS_LOCATION_SERVICE].url();
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(RedirectService.prototype, "translatedStateService", {
        get: function () {
            return this.ng1Translator.translations[this.ng1Translator.ANGULARJS_STATE_SERVICE];
        },
        enumerable: true,
        configurable: true
    });
    RedirectService.prototype.storeLastStateWithParams = function (state, stateParams) {
        if (state) {
            this.lastState = state;
            this.lastParams = Object.assign({}, stateParams);
        }
    };
    RedirectService.prototype.getLastState = function () {
        var output = this.lastState;
        this.lastState = "";
        return output;
    };
    ;
    RedirectService.prototype.getLastParams = function () {
        var output = this.lastParams;
        this.lastParams = {};
        return output;
    };
    ;
    RedirectService.prototype.getLastStateNoDelete = function () {
        var output = this.lastState;
        return output;
    };
    ;
    RedirectService.prototype.getLastParamsNoDelete = function () {
        var output = this.lastParams;
        return output;
    };
    ;
    // Choose mobile site for redirect
    RedirectService.prototype.redirectMobileUser = function () {
        if (this.userAgent.device.type === 'mobile' && this.allowRedirect) {
            var isEducator = '';
            if (this.accountService.isEducator()) {
                isEducator = '?iseducator=true';
            }
            // grab the current query string to pass along to mobile redirect page
            var queryStr = this.translatedLocationUrl.split('?')[1];
            queryStr = queryStr ? '?' + queryStr : queryStr;
            console.log('queryStr', queryStr);
            if (this.userAgent.os.name === 'iOS') {
                this.window.location.href = Globals.GLOBAL_URL + 'iphone-redirect' + (queryStr ? queryStr : '') + isEducator;
            }
            if (this.userAgent.os.name === 'Android') {
                this.window.location.href = Globals.GLOBAL_URL + 'android-redirect' + (queryStr ? queryStr : '') + isEducator;
            }
            else {
                console.log('mobile but unknown device');
            }
        }
    };
    // TODO: this should be referenced back from the Bookservice (or some single place that makes sense)
    // once we get upgraded to angular. For now I am duplicating the code 
    RedirectService.prototype.getObfuscatedBookId = function (bookId) {
        return bookId ? (parseInt(bookId) * 1111 + 2) : null;
    };
    ;
    RedirectService.prototype.noAuthRedirect = function (stateName, params) {
        var _this = this;
        if (stateName === 'read' && params.bookId) {
            // var obfuscatedBookId = BookService.getObfuscatedBookId(params.bookId);
            var obfuscatedBookId = this.getObfuscatedBookId(params.bookId);
            var contentUrlDict = {
                1: 'book',
                2: 'audiobook',
                4: 'video'
            };
            // get book title
            this.data.get('WebBook', 'noAuthGetBookDataForWeb', { bookURLID: obfuscatedBookId }).then(function (res) {
                if (res.result && res.result.book) {
                    var book = res.result.book;
                    // redirect to marketing book page
                    _this.window.location.href = Globals.GLOBAL_URL + (contentUrlDict[book.type] || 'book') + '/' + obfuscatedBookId + '/' + _this.stringService.getSEOFriendlyString(book.title);
                }
                else {
                    // book not found, just go to /sign-in
                    _this.translatedStateService.go('signIn');
                }
            });
        }
        else if (stateName === 'user-collection' && params.collectionId) {
            this.data.get('WebPlaylist', 'noAuthGetPlaylistAndBooksData', { playlistId: params.collectionId }).then(function (res) {
                if (res.result && res.result.title) {
                    // redirect to marketing collection page
                    _this.window.location.href = Globals.GLOBAL_URL +
                        'collection/' +
                        params.collectionId +
                        '/' +
                        _this.stringService.getSEOFriendlyString(res.result.title);
                }
                else {
                    // collection not found, just go to /sign-in
                    _this.translatedStateService.go('signIn');
                }
            });
        }
        else {
            if (stateName !== "browse") {
                this.storeLastStateWithParams(stateName, params);
            }
            this.translatedStateService.go('signIn');
        }
    };
    ;
    RedirectService.prototype.defaultRedirect = function (stateName, params) {
        this.translatedStateService.go(stateName, params);
    };
    ;
    RedirectService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [_window_ref_service__WEBPACK_IMPORTED_MODULE_1__["WindowRefService"],
            _services_data_service__WEBPACK_IMPORTED_MODULE_2__["DataService"],
            _services_account_service__WEBPACK_IMPORTED_MODULE_4__["AccountService"],
            _services_user_agent_service__WEBPACK_IMPORTED_MODULE_5__["UserAgentService"],
            _services_angularjs_translator_service__WEBPACK_IMPORTED_MODULE_6__["AngularjsTranslatorService"],
            _services_string_service__WEBPACK_IMPORTED_MODULE_3__["StringService"]])
    ], RedirectService);
    return RedirectService;
}());



/***/ }),

/***/ "./src/app/core/services/session-storage.service.ts":
/*!**********************************************************!*\
  !*** ./src/app/core/services/session-storage.service.ts ***!
  \**********************************************************/
/*! exports provided: SessionStorageService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SessionStorageService", function() { return SessionStorageService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _services_window_ref_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @services/window-ref.service */ "./src/app/core/services/window-ref.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


var SessionStorageService = /** @class */ (function () {
    function SessionStorageService(Window) {
        this.Window = Window;
        this.sessionStorageUnsupportedMessage = "Web browser does not support storing settings locally. In\n    Safari, the most common cause of this is using \"Private Browsing Mode.\" Some settings may not\n    save or some features may not work properly for you.";
        this.sessionStorageIsSupported = false;
        this.ss = this.Window.nativeWindow.sessionStorage;
        if (typeof this.ss === 'object') {
            try {
                this.setSessionStorageWithKey('sessStoreTest', 1);
                this.removeSessionStorageKey('sessStoreTest');
                this.sessionStorageIsSupported = true;
            }
            catch (e) {
                this.sessionStorageIsSupported = false;
            }
        }
    }
    SessionStorageService.prototype.setSessionStorageWithConfig = function (key, configObj, overwrite) {
        // Check session storage and don't overwrite if exists
        if (this.getSessionStorageWithKey(key) && !overwrite) {
            // console.log('sessionStorage already set');
            return;
        }
        else if (typeof configObj === 'object' && typeof key === 'string') {
            this.ss.setItem(key, JSON.stringify(configObj));
        }
        else {
            // TODO: handle error better
            // console.log('sessions storage not set with config. variable typing problem');
        }
    };
    SessionStorageService.prototype.setSessionStorageWithKey = function (key, val) {
        if (typeof key === 'string') {
            this.ss.setItem(key, JSON.stringify(val));
            // console.log('sessionStorage set with: ', `${key}:`, this.getSessionStorageWithKey(key));
        }
        else {
            // console.log('sessionStorage input is incorrect, key must be a string got:', `key: ${key}`);
        }
    };
    SessionStorageService.prototype.getSessionStorageWithKey = function (sessionKey) {
        if (typeof sessionKey === 'string') {
            var item = this.ss.getItem(sessionKey);
            return item ? JSON.parse(item) : null;
        }
        else {
            // console.log('sessionKey must be a string');
        }
    };
    SessionStorageService.prototype.removeSessionStorageKey = function (sessionKey) {
        this.ss.removeItem(sessionKey);
    };
    // TODO: these two last functions seem like they could maybe better be in the redirect service
    SessionStorageService.prototype.getRedirectData = function () {
        var item = this.ss.getItem('redirectData');
        return item ? JSON.parse(item) : null;
    };
    SessionStorageService.prototype.removeRedirectData = function () {
        this.removeSessionStorageKey('redirectData');
    };
    SessionStorageService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root',
        }),
        __metadata("design:paramtypes", [_services_window_ref_service__WEBPACK_IMPORTED_MODULE_1__["WindowRefService"]])
    ], SessionStorageService);
    return SessionStorageService;
}());



/***/ }),

/***/ "./src/app/core/services/sign-in.service.ts":
/*!**************************************************!*\
  !*** ./src/app/core/services/sign-in.service.ts ***!
  \**************************************************/
/*! exports provided: SignInService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SignInService", function() { return SignInService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _account_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./account.service */ "./src/app/core/services/account.service.ts");
/* harmony import */ var _window_ref_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./window-ref.service */ "./src/app/core/services/window-ref.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var SignInService = /** @class */ (function () {
    function SignInService(account, Window) {
        this.account = account;
        this.Window = Window;
        this.signIn = 'sign-in';
        this.app = 'app';
        this.eduDashboard = 'app/edu-dashboard';
        this.payment = 'promo/payment';
        this.window = this.Window.nativeWindow;
    }
    SignInService.prototype.redirectToSignIn = function () {
        this.handleRedirectToSignIn();
    };
    SignInService.prototype.handleRedirectOnSignIn = function () {
        // let subStatuses: any = {
        //   STATUS_FREE_TRIAL: number = 0,
        //   STATUS_NOT_SUBSCRIBED: number = 1,
        //   STATUS_SUBSCRIBED: number = 2,
        //   STATUS_SUBSCRIPTION_EXPIRED: number = 3,
        //   STATUS_SUBSCRIPTION_CANCELED: number = 4,
        //   STATUS_PROMO: number = 5,
        //   STATUS_GIFT_SUBSCRIPTION: number = 7,
        // };
        var accountStatus = this.account.realSubscriptionStatus;
        if (this.account.isEducator()) {
            this.handleEduRedirect();
            return;
        }
        // handle web sub users
        if ((!accountStatus && accountStatus !== 0) ||
            accountStatus === this.account.STATUS_NOT_SUBSCRIBED) {
            this.handleNeverSubbedRedirect();
            return;
        }
        else if (accountStatus === this.account.STATUS_SUBSCRIPTION_CANCELED ||
            (accountStatus === this.account.STATUS_SUBSCRIPTION_EXPIRED && this.account.type === this.account.SUBSCRIPTION_TYPE_APPLE)) {
            this.handleCanceledRedirect();
            return;
        }
        else if (accountStatus === this.account.STATUS_SUBSCRIPTION_EXPIRED) {
            this.handleExpiredRedirect();
            return;
        }
        // else if (accountStatus === this.account.STATUS_FREE_TRIAL || 
        //            accountStatus === this.account.STATUS_SUBSCRIBED || 
        //            accountStatus === this.account.STATUS_PROMO ||
        //            accountStatus === this.account.STATUS_GIFT_SUBSCRIPTION) {
        this.handledSubbedRedirect();
        // } 
        return;
    };
    SignInService.prototype.handleNeverSubbedRedirect = function () {
        // route to website payment details
        this.handleRedirectToRoute(this.payment);
        return;
    };
    // splitting these behaviors for in case we ever want to handle the two flows differently
    SignInService.prototype.handleCanceledRedirect = function () {
        // route to inapp for popup blocker
        this.handleRedirectToRoute(this.app);
        return;
    };
    SignInService.prototype.handleExpiredRedirect = function () {
        // route to inapp for popup blocker
        this.handleRedirectToRoute(this.app);
        return;
    };
    SignInService.prototype.handledSubbedRedirect = function () {
        // route to app
        this.handleRedirectToRoute(this.app);
        return;
    };
    SignInService.prototype.handleEduRedirect = function () {
        // route to edu dashboard
        this.handleRedirectToRoute(this.eduDashboard);
        return;
    };
    SignInService.prototype.handleRedirectToSignIn = function () {
        this.handleRedirectToRoute(this.signIn);
        return;
    };
    SignInService.prototype.handleRedirectToRoute = function (route) {
        // Replace this with the eventual ngRouter that will be implemented to avoid reloading the website for promo/payment
        this.window.location.href = Globals.GLOBAL_URL + route;
        return;
    };
    SignInService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [_account_service__WEBPACK_IMPORTED_MODULE_1__["AccountService"],
            _window_ref_service__WEBPACK_IMPORTED_MODULE_2__["WindowRefService"]])
    ], SignInService);
    return SignInService;
}());



/***/ }),

/***/ "./src/app/core/services/site-constants.service.ts":
/*!*********************************************************!*\
  !*** ./src/app/core/services/site-constants.service.ts ***!
  \*********************************************************/
/*! exports provided: SiteConstantsService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SiteConstantsService", function() { return SiteConstantsService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var SiteConstantsService = /** @class */ (function () {
    function SiteConstantsService() {
        this.BOOK_TYPE_STANDARD = 1;
        this.BOOK_TYPE_AUDIOBOOK = 2;
        this.BOOK_TYPE_ARTICLE = 3;
        this.BOOK_TYPE_VIDEO = 4;
        this.BOOK_TYPE_QUIZ = 5;
        this.PROMO = {
            NUM_BOOKS: '35,000',
            DEFAULT_PRICE: '7.99',
            DEFAULT_PRODUCT_ID: 'epic_monthly_799',
            SOURCES: [
                { key: "school_flyer", title: 'School Flyer' },
                { key: "teacher", title: 'My child\'s teacher' },
                { key: "my_child", title: 'My child' },
                { key: "family_member", title: 'Friend or Family member' },
                { key: "search_engine", title: 'Google or Bing Search' },
                { key: "social_media", title: 'Social Media (Facebook, Pinterest, etc.)' },
                { key: "today_show_or_magazine", title: 'The TODAY Show or a Magazine' },
                { key: "other_website", title: 'Other website (please name)', otherField: 'Other website:' },
                { key: "other", title: 'Other (please specify)', otherField: 'Other:' }
            ]
        };
        this.STRIPE = {
            DEV_KEY: 'pk_test_4Wy9ZuNal2fDNcMu9o1QcdBD',
            PROD_KEY: 'pk_live_4Wy94k6t1RpVKUu2VdsAbwem',
            FORM_DATA: {
                STATES: ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WA(DC)', 'WV', 'WI', 'WY', 'OTHER']
            }
        };
        this.READING_CHALLENGE_ARCHIVE = {
            fallIntoReading2018: {
                LEADERBOARD: '[{"school_name":"North Decatur Elementary","city":"GREENSBURG","state":"IN","books_finished":"6542"},{"school_name":"Spaulding Elementary","city":"LAMAR","state":"SC","books_finished":"5855"},{"school_name":"Arbuckle Elementary School","city":"ARBUCKLE","state":"CA","books_finished":"4565"},{"school_name":"East Elementary School","city":"JENKS","state":"OK","books_finished":"4543"},{"school_name":"Price Elementary","city":"SAN ANTONIO","state":"TX","books_finished":"4223"},{"school_name":"Arctic Light","city":"FAIRBANKS","state":"AK","books_finished":"3873"},{"school_name":"Granite Elementary","city":"SANDY","state":"UT","books_finished":"3754"},{"school_name":"Foley Intermediate School","city":"FOLEY","state":"AL","books_finished":"3689"},{"school_name":"Kipp Valiant Cmty Prep Cs","city":"PALO ALTO","state":"CA","books_finished":"3590"},{"school_name":"Castle Heights Elementary","city":"PRICE","state":"UT","books_finished":"3464"},{"school_name":"Whittier Elementary School","city":"GENEVA","state":"IL","books_finished":"3446"},{"school_name":"Union Grove Elementary","city":"GLADEWATER","state":"TX","books_finished":"3402"},{"school_name":"Kennedy Primary Academy","city":"SOUTH BEND","state":"IN","books_finished":"3389"},{"school_name":"scottsburg elementary school","city":"SCOTTSBURG","state":"IN","books_finished":"3256"},{"school_name":"Cortez Elementary School","city":"POMONA","state":"CA","books_finished":"2932"}]',
                TOTAL_BOOKS_READ: 8500424
            }
        };
        // Ported from settings service so I could remove it, deprecated!
        this.NUM_BOOKS = '35,000';
        this.PRICE = '7.99';
        this.PROGRESS_PROMO_PRICE = '5.99';
    }
    SiteConstantsService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [])
    ], SiteConstantsService);
    return SiteConstantsService;
}());



/***/ }),

/***/ "./src/app/core/services/string.service.ts":
/*!*************************************************!*\
  !*** ./src/app/core/services/string.service.ts ***!
  \*************************************************/
/*! exports provided: StringService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StringService", function() { return StringService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var StringService = /** @class */ (function () {
    function StringService() {
    }
    StringService.prototype.toHours = function (t) {
        return Math.floor(t / 3600 * 10) / 10;
    };
    StringService.prototype.toDate = function (t) {
        t *= 1000;
        var d = new Date(t);
        return (d.getMonth() + 1) + '/' + d.getDate() + '/' + d.getFullYear();
    };
    StringService.prototype.toTime = function (t) {
        var formattedTime = '';
        var minutes;
        if (t > 3600) {
            var hours = Math.floor(t / 3600 * 10) / 10;
            formattedTime = hours + ' hour';
            if (hours > 1) {
                formattedTime += 's';
            }
        }
        else if (t > 60) {
            minutes = Math.floor(t / 60);
            formattedTime = minutes + ' minute';
            if (minutes > 1) {
                formattedTime += 's';
            }
        }
        else {
            var seconds = Math.floor(t);
            formattedTime = seconds + ' second';
            if (seconds > 1) {
                formattedTime += 's';
            }
        }
        return formattedTime;
    };
    // todo: t SEEMS to always come in as a number so
    // at some point simplify the type callout and for the arg
    // and remove the var sec_num = parseInt(t, 10); line
    StringService.prototype.toHHMMSS = function (t) {
        var sec_num;
        if (typeof t === 'string') {
            sec_num = parseInt(t, 10); // don't forget the second param
        }
        else {
            sec_num = parseInt(t.toString(10), 10);
        }
        var hours = Math.floor(sec_num / 3600);
        var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
        var seconds = sec_num - (hours * 3600) - (minutes * 60);
        var hoursAsString = hours.toString();
        var minutesAsString = minutes.toString();
        var secondsAsString = seconds.toString();
        // if (hours < 10) {
        //     hours = "0" + hours;
        // }
        if (minutes < 10 && hours > 0) {
            minutesAsString = "0" + minutesAsString;
        }
        if (seconds < 10) {
            secondsAsString = "0" + secondsAsString;
        }
        if (hours > 0) {
            return hoursAsString + ':' + minutesAsString + ':' + secondsAsString;
        }
        else {
            return minutesAsString + ':' + secondsAsString;
        }
    };
    StringService.prototype.truncate = function (string, maxLength) {
        if (!string)
            return '';
        var notNumOrLetter = /[^a-zA-Z0-9]/g;
        if (string.length >= maxLength) {
            string = string.slice(0, maxLength - 2);
            // if end is in the middle of a word, cut it off
            if (string.slice(-10).indexOf(' ') > -1) {
                string = string.split(' ').slice(0, -1).join(' ');
            }
            // pop off non numbers and letters
            if (string.slice(-10).match(notNumOrLetter)) {
                var stringAsArray = string.split('');
                while (stringAsArray.slice(-1)[0].match(notNumOrLetter)) {
                    stringAsArray.pop();
                }
                string = stringAsArray.join('');
            }
            string += '...';
        }
        return string;
    };
    StringService.prototype.getSEOFriendlyString = function (str) {
        return str.toLowerCase().replace(/[^a-z0-9_\s-]/g, '').replace(/[\s-]+/g, ' ').trim().replace(/[\s_]/g, '-');
    };
    StringService.prototype.encodeUrlString = function (str) {
        return encodeURIComponent(str).replace(/'/g, '%27').replace(/"/g, '%22');
    };
    StringService.prototype.decodeUrlString = function (str) {
        return decodeURIComponent(str.replace(/\+/g, ' '));
    };
    StringService.prototype.urldecode = function (str) {
        return unescape((str + '').replace(/\+/g, '%20'));
    };
    StringService.prototype.hasUnicode = function (str) {
        for (var i = 0; i < str.length; i++) {
            if (str.charCodeAt(i) > 127)
                return true;
        }
        return false;
    };
    StringService.prototype.validateEmail = function (email) {
        return /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$/.test(email);
    };
    StringService.prototype.intToPrice = function (int) {
        var price = int.toString().split('');
        price.splice(-2, 0, '.');
        price.unshift('$');
        return price.join('');
    };
    StringService.prototype.hyphenRouteToCamel = function (hyphenedUrl) {
        var camelCasedString = hyphenedUrl.replace(/-([a-z]|[0-9])/g, function (g) { return g[1].toUpperCase(); });
        return camelCasedString;
    };
    StringService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [])
    ], StringService);
    return StringService;
}());



/***/ }),

/***/ "./src/app/core/services/subscription.service.ts":
/*!*******************************************************!*\
  !*** ./src/app/core/services/subscription.service.ts ***!
  \*******************************************************/
/*! exports provided: SubscriptionService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SubscriptionService", function() { return SubscriptionService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _services_data_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @services/data.service */ "./src/app/core/services/data.service.ts");
/* harmony import */ var _services_tax_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @services/tax.service */ "./src/app/core/services/tax.service.ts");
/* harmony import */ var _services_logsly_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @services/logsly.service */ "./src/app/core/services/logsly.service.ts");
/* harmony import */ var _services_big_query_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @services/big-query.service */ "./src/app/core/services/big-query.service.ts");
/* harmony import */ var _services_account_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @services/account.service */ "./src/app/core/services/account.service.ts");
/* harmony import */ var _services_promo_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @services/promo.service */ "./src/app/core/services/promo.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};







var SubscriptionService = /** @class */ (function () {
    function SubscriptionService(data, taxService, logsly, bigQuery, accountService, promoService) {
        this.data = data;
        this.taxService = taxService;
        this.logsly = logsly;
        this.bigQuery = bigQuery;
        this.accountService = accountService;
        this.promoService = promoService;
        this.devKey = "pk_test_4Wy9ZuNal2fDNcMu9o1QcdBD";
        this.prodKey = "pk_live_4Wy94k6t1RpVKUu2VdsAbwem";
        this.key = Globals.GLOBAL_DEV_MODE ? this.devKey : this.prodKey;
        this.checkingSubStatus = false;
        this.status = {};
        this.stripeCardInfo = null;
        this.readableExpiration = null;
        this.activeCCBrand = null;
        this.isPaymentDelinquent = false;
        this.paymentMethod = 0;
    }
    Object.defineProperty(SubscriptionService.prototype, "stripe", {
        get: function () {
            return Stripe(this.key);
        },
        enumerable: true,
        configurable: true
    });
    SubscriptionService.prototype.setPaymentMethodName = function (paymentMethod) {
        // Look at AccountSubscription.inc on backend for
        // SUBSCRIPTION_SUB_TYPE_* for number associations
        if (paymentMethod === 'basic-card') {
            this.paymentMethod = 1;
        }
        else if (paymentMethod === 'apple-pay') {
            this.paymentMethod = 2;
        }
        else if (paymentMethod === ' google-pay') {
            this.paymentMethod = 3;
        }
        else {
            this.paymentMethod = 0;
        }
    };
    SubscriptionService.prototype.subscribeWithModel = function (subscriptionModel) {
        var _this = this;
        // If no stripeToken, try to subscribe without card 
        var fn = (subscriptionModel.stripeToken) ? 'noAuthSubscribe' : 'noAuthSubscribeWithoutToken';
        subscriptionModel.subPaymentType = this.paymentMethod; // set payment method onto the subscription model
        return this.data.post('WebAccount', fn, {
            accountData: subscriptionModel.getJSONFormattedData(),
            zipCode: this.taxService.getPostalCode(),
            calculateAdded: this.taxService.getChargeTax()
        })
            .then(function (data) {
            var error;
            if (!data || !data.result)
                error = 'Whoops! Something went wrong. Please try again later.';
            if (!data.result.subscribeSuccess)
                error = data.result.error || 'Whoops! Something went wrong.';
            if (error) {
                // Log error
                _this.logsly.track('subscription_flow_subscription_failed', 'subscription_flow', error, '');
                _this.bigQuery.log(_this.bigQuery.events.SUBSCRIBE_PURCHASE_FAIL, { eduv: _this.accountService.eduv });
                return { error: error };
            }
            // Set account id if not already set
            _this.accountService.id = _this.accountService.id || data.result.accountId;
            // this updates the account service so the account data can be loaded in case the client moves to a different page after subbing instead of going straight to the app
            _this.accountService.updateAccountData();
            // Log success
            _this.logSubscribeSuccess(subscriptionModel);
            return data.result;
        })
            .catch(function () {
        });
    };
    SubscriptionService.prototype.updateCardWithModel = function (subscriptionModel) {
        return this.data.post('WebAccount', 'updatePaymentMethod', {
            stripeToken: subscriptionModel.stripeToken,
            captchaToken: subscriptionModel.captchaToken,
        })
            .then(function (data) {
            if (!data || !data.result)
                return { error: 'Whoops! Something went wrong. Please try again later.' };
            if (!data.result.success || !data.result.cardInfo)
                return { error: "Failed to update payment info." };
            return data.result;
        })
            .catch(function () {
            return { error: 'Whoops! Something went wrong. Please try again later.' };
        });
    };
    SubscriptionService.prototype.checkSubscriptionStatus = function (refresh) {
        var _this = this;
        if (refresh)
            this.status = {};
        if (this.checkingSubStatus || this.status.valid)
            return Promise.resolve();
        this.checkingSubStatus = true;
        return this.data.get('WebAccount', 'getSubscriptionStatus').then(function (data) {
            _this.checkingSubStatus = false;
            if (data.result && data.result.status) {
                _this.status = data.result.status;
                _this.readableExpiration = new Date(data.result.status.expiration).toDateString();
                _this.stripeCardInfo = data.result.cardInfo;
                _this.activeCCBrand = data.result.cardInfo ? _this.formatCCBrand(data.result.cardInfo.brand) : null;
                _this.isPaymentDelinquent = data.result.status.isPaymentDelinquent;
                // Invalid sub?
                if (!_this.status.valid) {
                    // if (service.isPaymentDelinquent) {
                    // Show deliquent payment dialog
                    _this.openSubscriptionDialog();
                    // } else {
                    //   // Redirect to payment page
                    //   $window.location = Globals.GLOBAL_URL + 'promo/payment';
                    // }
                }
            }
            else {
                console.log('Problem getting account subscription status.');
            }
        });
    };
    SubscriptionService.prototype.logSubscribeSuccess = function (subscriptionModel) {
        var livePromo = this.promoService.getLivePromo();
        if (livePromo) {
            var currentLivePromoSessionData = this.promoService.getPromoDetails(livePromo);
        }
        var bqParams = {};
        bqParams.source_after_hours = 'no';
        // if the offer is after hours
        if (livePromo === this.promoService.TEACHER_OFFER_AFTER_HOURS) {
            bqParams.source_after_hours = 'yes';
            bqParams.student_id = currentLivePromoSessionData && currentLivePromoSessionData.c;
            bqParams.teacher_account_id = currentLivePromoSessionData && currentLivePromoSessionData.t;
        }
        this.bigQuery.log(this.bigQuery.events.SUBSCRIBE_WEBSITE, Object.assign(bqParams, { eduv: this.accountService.eduv }));
        this.logsly.logTransaction(this.accountService.id, subscriptionModel.product);
    };
    SubscriptionService.prototype.getPayState = function () {
        if (this.isPaymentDelinquent) {
            return "past_due";
        }
        else {
            return "new";
        }
    };
    // Format incoming CC brands to actual CC images
    SubscriptionService.prototype.formatCCBrand = function (brandString) {
        switch (brandString) {
            case 'Visa':
                return 'visa';
            case 'American Express':
                return 'am';
            case 'MasterCard':
                return 'mastercard';
            case 'Discover':
                return 'discover';
            case 'JCB':
                return 'jcb';
            case 'Diners Club':
                return 'diners';
            default:
                return 'general';
        }
    };
    SubscriptionService.prototype.openSubscriptionDialog = function (data, clickOutsideToClose) {
        console.log('openSubscriptionDialog');
        var openSubscriptionDialogEvent = new CustomEvent('openSubscriptionDialog', {
            detail: {
                data: data,
                clickOutsideToClose: clickOutsideToClose
            }
        });
        document.dispatchEvent(openSubscriptionDialogEvent);
    };
    SubscriptionService.prototype.openSubscriptionSuccessDialog = function (details) {
        console.log('openSubscriptionSuccessDialog');
        var openSubscriptionDialogEvent = new CustomEvent('openSubscriptionSuccessDialog', {
            detail: { details: details }
        });
        document.dispatchEvent(openSubscriptionDialogEvent);
    };
    SubscriptionService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [_services_data_service__WEBPACK_IMPORTED_MODULE_1__["DataService"],
            _services_tax_service__WEBPACK_IMPORTED_MODULE_2__["TaxService"],
            _services_logsly_service__WEBPACK_IMPORTED_MODULE_3__["LogslyService"],
            _services_big_query_service__WEBPACK_IMPORTED_MODULE_4__["BigQueryService"],
            _services_account_service__WEBPACK_IMPORTED_MODULE_5__["AccountService"],
            _services_promo_service__WEBPACK_IMPORTED_MODULE_6__["PromoService"]])
    ], SubscriptionService);
    return SubscriptionService;
}());



/***/ }),

/***/ "./src/app/core/services/tap.service.ts":
/*!**********************************************!*\
  !*** ./src/app/core/services/tap.service.ts ***!
  \**********************************************/
/*! exports provided: TapService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "TapService", function() { return TapService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _data_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./data.service */ "./src/app/core/services/data.service.ts");
/* harmony import */ var _account_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./account.service */ "./src/app/core/services/account.service.ts");
/* harmony import */ var _profile_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./profile.service */ "./src/app/core/services/profile.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};




var TapService = /** @class */ (function () {
    function TapService(dataService, accountService, profileService) {
        this.dataService = dataService;
        this.accountService = accountService;
        this.profileService = profileService;
        this.tapEnrolled = false;
        this.tapFunds = 0;
        this.classroomCode = '';
        this.tapStudentProfilesLoading = false;
        this.tapStudentProfiles = [];
        this.giftCardCatalog = [];
        this.giftCardCatalogLoading = false;
        this.tapFundsLoading = false;
        this.selectedCard = null;
        this.errorDictionary = {
            0: 'TAP redemption error. Please try again later.',
            1: 'Incorrect Password.',
            2: 'Insufficient Balance',
            3: 'TAP redemption error. Please try again later.',
            4: 'Error: Open redemption pending.'
        };
        this.gcImages = {
            'Amazon.com': '/assets/app/tap/amazon-card.png',
            'Barnes & Noble': '/assets/app/tap/barnes-and-noble-card.png',
            'Staples': '/assets/app/tap/staples-card.png',
            'Target': '/assets/app/tap/target-card.png'
        };
        this.gcFineprint = {
            'Amazon.com': 'Amazon.com Gift Cards* never expire and can be redeemed towards millions of items at www.amazon.com. *Amazon.com is not a sponsor of this promotion. Except as required by law, Amazon.com Gift Cards ("GCs") cannot be transferred for value or redeemed for cash. GCs may be used only for purchases of eligible goods on Amazon.com or certain of its affiliated websites. GCs cannot be redeemed for purchases of gift cards. Purchases are deducted from the GC balance. To redeem or view a GC balance, visit "Your Account" on Amazon.com. Amazon is not responsible if a GC is lost, stolen, destroyed or used without permission. For complete terms and conditions, see www.amazon.com/gc-legal. GCs are issued by ACI Gift Cards, Inc., a Washington corporation. All Amazon ®, ™ & © are IP of Amazon.com, Inc. or its affiliates. No expiration date or service fees.',
            'Barnes & Noble': 'Barnes & Noble is not a sponsor or co-sponsor of this promotion. The logos and other identifying marks attached are trademarks of and owned by each represented company and/or its affiliates.  Please visitwww.bn.com for terms and conditions of use. Barnes & Noble is not liable for any alleged or actual claims related to this offer.',
            'Staples': 'Staples, Inc. is not a sponsor or co-sponsor of this promotion. The logos and other identifying marks attached are trademarks of and owned by each represented company and/or its affiliates.  Please visit www.staples.com for terms and conditions of use. Staples, Inc. is not liable for any alleged or actual claims related to this offer.',
            'Target': 'This Gift Card can be redeemed for merchandise or services (other than American Express and Visa gift cards and prepaid cards) at Target stores in the U.S. or Target.com, and cannot be redeemed for cash or credit except where required by law. No value until purchased. For balance information, visit www.target.com/giftcards or call 1-800-544-2943. To replace the remaining value on a lost, stolen or damaged card with the original purchase receipt, 1-800-544-2943. © 2016 Target Brands, Inc. The Bullseye Design, Bullseye Dog and Target are trademarks of Target Brands, Inc. 1212 1897.'
        };
        this.defaultError = 'TAP redemption error. Please try again later.';
        this.shouldEnableRedeemOption = false;
        this.childProfiles = this.profileService.childProfiles;
    }
    TapService.prototype.enrollTap = function (enroll) {
        var enrollOptions = { enroll: enroll ? 1 : 0 };
        var service = this;
        return this.dataService.post('WebTAP', 'enrollTAP', enrollOptions).then(function (res) {
            if (res.result && res.result.tapEnrolled) {
                service.tapEnrolled = true;
                service.accountService.tapEnrolled = 1;
            }
            else {
                console.warn('Problem enrolling in TAP.');
            }
            return res;
        });
    };
    ;
    TapService.prototype.getClassroomCode = function () {
        var service = this;
        return this.dataService.get('WebAccount', 'getClassroomCode', {}).then(function (res) {
            if (res.result && res.result.classroomCode) {
                service.classroomCode = res.result.classroomCode;
            }
            else {
                // user doesn't have a classroom code yet
            }
            return res;
        });
    };
    ;
    TapService.prototype.refreshTapGiftCardCatalog = function () {
        this.giftCardCatalogLoading = true;
        var service = this;
        return this.dataService.get('WebTAP', 'getTangoCardRewardItems', {}).then(function (res) {
            if (res.result) {
                service.giftCardCatalog = [];
                var replaceBrand = function (item) {
                    item.brandDescription = correctedBrandName;
                };
                for (var prop in res.result) {
                    var correctedBrandName = (prop.slice(-1) === '*' ? prop.slice(0, -1) : prop);
                    res.result[prop].brand = correctedBrandName;
                    res.result[prop].rewards.forEach(replaceBrand);
                    service.giftCardCatalog.push(res.result[prop]);
                }
                return res.result;
            }
            else {
                console.warn('Problem getting TAP gift card catalog');
                service.giftCardCatalog = [];
            }
            service.giftCardCatalogLoading = false;
        });
    };
    ;
    TapService.prototype.setShouldEnableRedeemOption = function () {
        this.shouldEnableRedeemOption = this.getMinimumPointsForRedemption() <= this.tapFunds;
    };
    TapService.prototype.getMinimumPointsForRedemption = function () {
        var minimumForRedemption = Infinity;
        if (!this.giftCardCatalog.length)
            return minimumForRedemption;
        this.giftCardCatalog.forEach(function (brand) {
            brand.rewards.forEach(function (reward) {
                if (reward.tapPoints < minimumForRedemption) {
                    minimumForRedemption = reward.tapPoints;
                }
            });
        });
        return minimumForRedemption;
    };
    TapService.prototype.refreshTapFunds = function () {
        this.tapFundsLoading = true;
        var service = this;
        return this.dataService.get('WebTAP', 'getTAPPointsForAccount').then(function (res) {
            service.tapFundsLoading = false;
            if (res.result || res.result === 0) {
                service.tapFunds = res.result;
                return res.result;
            }
            else {
                console.warn('Problem getting TAP student profiles');
            }
        });
    };
    ;
    TapService.prototype.refereshTapStudentProfiles = function () {
        this.tapStudentProfilesLoading = true;
        var service = this;
        this.dataService.get('WebTAP', 'getTAPStudentProfiles', {}).then(function (res) {
            service.tapStudentProfilesLoading = false;
            if (Array.isArray(res.result)) {
                var tempArr = service.childProfiles.map(function (childProfile) {
                    var tapProfile = service.formatTapObject(childProfile, res.result);
                    if (tapProfile) {
                        return Object.assign({}, childProfile, {
                            connectionState: tapProfile.connectionState,
                            cumulativeTAPPoints: tapProfile.cumulativeTAPPoints,
                            journalName: tapProfile.profile.journalName,
                            journalFrameImage: tapProfile.profile.journalFrameImage,
                            isApprovedForHomeAccess: childProfile.isApprovedForHomeAccess(),
                            isPendingApproval: childProfile.isProfilePendingApproval()
                        });
                    }
                });
                service.tapStudentProfiles = tempArr.filter(function (obj) {
                    return obj && !obj.isParent;
                });
            }
            else {
                console.warn('Problem getting TAP student profiles');
                service.tapStudentProfiles = [];
            }
        });
    };
    ;
    TapService.prototype.formatIntWithCommas = function (int) {
        if (int || parseInt(int) === 0) {
            int = int.toString();
            var res_1 = [];
            var savedNegative = int[0] === '-' ? int[0] : null;
            int = savedNegative ? int.slice(1) : int;
            int.split('').reverse().forEach(function (item, index) {
                if (index !== 0 && index % 3 === 0) {
                    res_1.push(',');
                }
                res_1.push(item);
            });
            if (savedNegative) {
                res_1.push(savedNegative);
            }
            return res_1.reverse().join('');
        }
        else {
            return null;
        }
    };
    ;
    TapService.prototype.getFormattedFunds = function (funds) {
        funds = (funds || parseInt(funds) === 0) ? funds : this.tapFunds;
        return this.formatIntWithCommas(funds);
    };
    ;
    TapService.prototype.formatPrice = function (cents) {
        if (!cents)
            return null;
        cents = cents.toString().split('');
        cents.splice(-2, 0, '.');
        return '$' + cents.join('');
    };
    ;
    TapService.prototype.formatTapObject = function (childProfile, tapArray) {
        if (childProfile && tapArray) {
            return tapArray.find(function (tapStudentObj) {
                return tapStudentObj.profile.modelId == childProfile.userId;
            });
        }
    };
    ;
    TapService.prototype.filterProfilesByConnectionState = function (states) {
        if (Array.isArray(this.tapStudentProfiles) && this.tapStudentProfiles.length > 0) {
            return this.tapStudentProfiles
                .filter(function (profile) {
                if (profile.accountType === 1) {
                    return false;
                }
                if (Array.isArray(states)) {
                    return states.indexOf(profile.connectionState) > -1;
                }
                else {
                    return states === profile.connectionState;
                }
            });
        }
        else {
            return [];
        }
    };
    ;
    TapService.prototype.selectTapCardForRedemption = function (card) {
        this.selectedCard = card;
    };
    ;
    TapService.prototype.confirmTapCardRedemption = function (password) {
        var redeemOptions = {
            password: password,
            sku: this.selectedCard.sku,
            amount: this.selectedCard.amount
        };
        return this.dataService.post('WebTAP', 'redeemTAPReward', redeemOptions);
    };
    ;
    TapService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [_data_service__WEBPACK_IMPORTED_MODULE_1__["DataService"],
            _account_service__WEBPACK_IMPORTED_MODULE_2__["AccountService"],
            _profile_service__WEBPACK_IMPORTED_MODULE_3__["ProfileService"]])
    ], TapService);
    return TapService;
}());



/***/ }),

/***/ "./src/app/core/services/tax.service.ts":
/*!**********************************************!*\
  !*** ./src/app/core/services/tax.service.ts ***!
  \**********************************************/
/*! exports provided: TaxService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "TaxService", function() { return TaxService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _data_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./data.service */ "./src/app/core/services/data.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


var TaxService = /** @class */ (function () {
    function TaxService(data) {
        this.data = data;
        this.giftTaxEstimate = '-------';
        this.taxEstimate = '-------';
        this.postalCode = 0;
        this.chargeTax = false;
    }
    TaxService.prototype.getTaxEstimate = function (productId, postalCode) {
        return this.data.get('WebTax', 'noAuthGetTaxEstimate', {
            productId: productId,
            zipCode: postalCode
        })
            .catch(function () {
            return null;
        });
    };
    TaxService.prototype.getGiftTaxEstimate = function (productId, postalCode) {
        return this.data.get('WebTax', 'noAuthGetGiftTaxEstimate', {
            productId: productId,
            zipCode: postalCode
        })
            .catch(function () {
            return null;
        });
    };
    TaxService.prototype.getChargeTax = function () {
        return this.chargeTax;
    };
    TaxService.prototype.setChargeTax = function (chargeTax) {
        this.chargeTax = chargeTax;
    };
    TaxService.prototype.getPostalCode = function () {
        return this.postalCode;
    };
    TaxService.prototype.setPostalCode = function (postalCode) {
        this.postalCode = postalCode;
    };
    TaxService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [_data_service__WEBPACK_IMPORTED_MODULE_1__["DataService"]])
    ], TaxService);
    return TaxService;
}());



/***/ }),

/***/ "./src/app/core/services/user-agent.service.ts":
/*!*****************************************************!*\
  !*** ./src/app/core/services/user-agent.service.ts ***!
  \*****************************************************/
/*! exports provided: USER_AGENT, UserAgentService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "USER_AGENT", function() { return USER_AGENT; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserAgentService", function() { return UserAgentService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var ua_parser_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ua-parser-js */ "./node_modules/ua-parser-js/src/ua-parser.js");
/* harmony import */ var ua_parser_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(ua_parser_js__WEBPACK_IMPORTED_MODULE_1__);
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (undefined && undefined.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
// import { Inject, , InjectionToken } from '@angular/core';

/// <reference path="../../declarations/ua-parser-js.d.ts"/>

// export const USER_AGENT = new InjectionToken<IUAParser.IResult>('UserAgent.service', {
var USER_AGENT = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["InjectionToken"]('UserAgent.service', {
    providedIn: 'root',
    // factory: () => new UAParserModule.UAParser().getResult()
    factory: function () { return new ua_parser_js__WEBPACK_IMPORTED_MODULE_1__["UAParser"](); }
});
var UserAgentService = /** @class */ (function () {
    function UserAgentService(uaParser) {
        this.uaParser = uaParser;
    }
    Object.defineProperty(UserAgentService.prototype, "ua", {
        get: function () {
            return this.uaParser.getResult().ua;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(UserAgentService.prototype, "browser", {
        get: function () {
            return this.uaParser.getResult().browser;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(UserAgentService.prototype, "device", {
        get: function () {
            return this.uaParser.getResult().device;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(UserAgentService.prototype, "engine", {
        get: function () {
            return this.uaParser.getResult().engine;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(UserAgentService.prototype, "os", {
        get: function () {
            return this.uaParser.getResult().os;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(UserAgentService.prototype, "cpu", {
        get: function () {
            return this.uaParser.getResult().cpu;
        },
        enumerable: true,
        configurable: true
    });
    UserAgentService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __param(0, Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"])(USER_AGENT)),
        __metadata("design:paramtypes", [ua_parser_js__WEBPACK_IMPORTED_MODULE_1__["UAParser"]])
    ], UserAgentService);
    return UserAgentService;
}());

// export const UserAgentService = new InjectionToken<UAParserModule.UAParser>('UserAgent.service');
// export namespace UserAgentService {}


/***/ }),

/***/ "./src/app/core/services/window-ref.service.ts":
/*!*****************************************************!*\
  !*** ./src/app/core/services/window-ref.service.ts ***!
  \*****************************************************/
/*! exports provided: WindowRefService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "WindowRefService", function() { return WindowRefService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

// https://juristr.com/blog/2016/09/ng2-get-window-ref/
function _window() {
    // return the global native browser window object
    return window;
}
var WindowRefService = /** @class */ (function () {
    function WindowRefService() {
    }
    Object.defineProperty(WindowRefService.prototype, "nativeWindow", {
        get: function () {
            return _window();
        },
        enumerable: true,
        configurable: true
    });
    WindowRefService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [])
    ], WindowRefService);
    return WindowRefService;
}());



/***/ }),

/***/ "./src/app/service-bootstrap/service-bootstrap.component.ts":
/*!******************************************************************!*\
  !*** ./src/app/service-bootstrap/service-bootstrap.component.ts ***!
  \******************************************************************/
/*! exports provided: ServiceBootstrapComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ServiceBootstrapComponent", function() { return ServiceBootstrapComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var ServiceBootstrapComponent = /** @class */ (function () {
    function ServiceBootstrapComponent() {
        this.initialized = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
    }
    ServiceBootstrapComponent.prototype.ngAfterViewInit = function () {
        console.log('ServiceBootstrapComponent ready');
        this.initialized.emit();
    };
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"])(),
        __metadata("design:type", _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"])
    ], ServiceBootstrapComponent.prototype, "initialized", void 0);
    ServiceBootstrapComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'service-bootstrap',
            template: ""
        })
    ], ServiceBootstrapComponent);
    return ServiceBootstrapComponent;
}());



/***/ }),

/***/ "./src/app/shared/empty/empty.component.html":
/*!***************************************************!*\
  !*** ./src/app/shared/empty/empty.component.html ***!
  \***************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/app/shared/empty/empty.component.scss":
/*!***************************************************!*\
  !*** ./src/app/shared/empty/empty.component.scss ***!
  \***************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3NoYXJlZC9lbXB0eS9lbXB0eS5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/shared/empty/empty.component.ts":
/*!*************************************************!*\
  !*** ./src/app/shared/empty/empty.component.ts ***!
  \*************************************************/
/*! exports provided: EmptyComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "EmptyComponent", function() { return EmptyComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var EmptyComponent = /** @class */ (function () {
    function EmptyComponent() {
    }
    EmptyComponent.prototype.ngOnInit = function () {
    };
    EmptyComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-empty',
            template: __webpack_require__(/*! ./empty.component.html */ "./src/app/shared/empty/empty.component.html"),
            styles: [__webpack_require__(/*! ./empty.component.scss */ "./src/app/shared/empty/empty.component.scss")]
        }),
        __metadata("design:paramtypes", [])
    ], EmptyComponent);
    return EmptyComponent;
}());



/***/ }),

/***/ "./src/app/shared/page-not-found/page-not-found.component.html":
/*!*********************************************************************!*\
  !*** ./src/app/shared/page-not-found/page-not-found.component.html ***!
  \*********************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<h2>Page not found</h2>\n"

/***/ }),

/***/ "./src/app/shared/page-not-found/page-not-found.component.scss":
/*!*********************************************************************!*\
  !*** ./src/app/shared/page-not-found/page-not-found.component.scss ***!
  \*********************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3NoYXJlZC9wYWdlLW5vdC1mb3VuZC9wYWdlLW5vdC1mb3VuZC5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/shared/page-not-found/page-not-found.component.ts":
/*!*******************************************************************!*\
  !*** ./src/app/shared/page-not-found/page-not-found.component.ts ***!
  \*******************************************************************/
/*! exports provided: PageNotFoundComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PageNotFoundComponent", function() { return PageNotFoundComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var PageNotFoundComponent = /** @class */ (function () {
    function PageNotFoundComponent() {
    }
    PageNotFoundComponent.prototype.ngOnInit = function () {
    };
    PageNotFoundComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-page-not-found',
            template: __webpack_require__(/*! ./page-not-found.component.html */ "./src/app/shared/page-not-found/page-not-found.component.html"),
            styles: [__webpack_require__(/*! ./page-not-found.component.scss */ "./src/app/shared/page-not-found/page-not-found.component.scss")]
        }),
        __metadata("design:paramtypes", [])
    ], PageNotFoundComponent);
    return PageNotFoundComponent;
}());



/***/ }),

/***/ "./src/app/shared/test2/test2.component.html":
/*!***************************************************!*\
  !*** ./src/app/shared/test2/test2.component.html ***!
  \***************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n<h2 class=\"test\">TEST</h2>\n<p>Test works</p>\n\n<button routerLink=\"/explore\">Go to explore</button>"

/***/ }),

/***/ "./src/app/shared/test2/test2.component.scss":
/*!***************************************************!*\
  !*** ./src/app/shared/test2/test2.component.scss ***!
  \***************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3NoYXJlZC90ZXN0Mi90ZXN0Mi5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/shared/test2/test2.component.ts":
/*!*************************************************!*\
  !*** ./src/app/shared/test2/test2.component.ts ***!
  \*************************************************/
/*! exports provided: Test2Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Test2Component", function() { return Test2Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var Test2Component = /** @class */ (function () {
    function Test2Component() {
    }
    Test2Component.prototype.ngOnInit = function () {
    };
    Test2Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-test2',
            template: __webpack_require__(/*! ./test2.component.html */ "./src/app/shared/test2/test2.component.html"),
            styles: [__webpack_require__(/*! ./test2.component.scss */ "./src/app/shared/test2/test2.component.scss")]
        }),
        __metadata("design:paramtypes", [])
    ], Test2Component);
    return Test2Component;
}());



/***/ }),

/***/ "./src/environments/environment.ts":
/*!*****************************************!*\
  !*** ./src/environments/environment.ts ***!
  \*****************************************/
/*! exports provided: environment */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "environment", function() { return environment; });
// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.
var environment = {
    production: false
};
/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.


/***/ }),

/***/ "./src/main.ts":
/*!*********************!*\
  !*** ./src/main.ts ***!
  \*********************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _app_app_module__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./app/app.module */ "./src/app/app.module.ts");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./environments/environment */ "./src/environments/environment.ts");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_platform_browser_dynamic__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/platform-browser-dynamic */ "./node_modules/@angular/platform-browser-dynamic/fesm5/platform-browser-dynamic.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/upgrade/static */ "./node_modules/@angular/upgrade/fesm5/static.js");
/* harmony import */ var _app_service_bootstrap_service_bootstrap_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./app/service-bootstrap/service-bootstrap.component */ "./src/app/service-bootstrap/service-bootstrap.component.ts");
/* harmony import */ var _app_core_services_data_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./app/core/services/data.service */ "./src/app/core/services/data.service.ts");
/* harmony import */ var _app_core_services_message_handler_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./app/core/services/message-handler.service */ "./src/app/core/services/message-handler.service.ts");
/* harmony import */ var _app_core_services_captcha_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./app/core/services/captcha.service */ "./src/app/core/services/captcha.service.ts");
/* harmony import */ var _app_core_services_tax_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./app/core/services/tax.service */ "./src/app/core/services/tax.service.ts");
/* harmony import */ var _app_core_services_account_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./app/core/services/account.service */ "./src/app/core/services/account.service.ts");
/* harmony import */ var _app_core_services_session_storage_service__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./app/core/services/session-storage.service */ "./src/app/core/services/session-storage.service.ts");
/* harmony import */ var _app_core_services_local_storage_service__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./app/core/services/local-storage.service */ "./src/app/core/services/local-storage.service.ts");
/* harmony import */ var _app_core_services_string_service__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./app/core/services/string.service */ "./src/app/core/services/string.service.ts");
/* harmony import */ var _app_core_services_logsly_service__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./app/core/services/logsly.service */ "./src/app/core/services/logsly.service.ts");
/* harmony import */ var _app_core_services_after_hours_service__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./app/core/services/after-hours.service */ "./src/app/core/services/after-hours.service.ts");
/* harmony import */ var _app_core_services_user_agent_service__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! ./app/core/services/user-agent.service */ "./src/app/core/services/user-agent.service.ts");
/* harmony import */ var _app_core_services_promo_service__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! ./app/core/services/promo.service */ "./src/app/core/services/promo.service.ts");
/* harmony import */ var _services_big_query_service__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @services/big-query.service */ "./src/app/core/services/big-query.service.ts");
/* harmony import */ var _app_core_services_profile_service__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! ./app/core/services/profile.service */ "./src/app/core/services/profile.service.ts");
/* harmony import */ var _app_core_services_sign_in_service__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! ./app/core/services/sign-in.service */ "./src/app/core/services/sign-in.service.ts");
/* harmony import */ var _services_abtest_service__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! @services/abtest.service */ "./src/app/core/services/abtest.service.ts");
/* harmony import */ var _services_query_string_service__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! @services/query-string.service */ "./src/app/core/services/query-string.service.ts");
/* harmony import */ var _services_angularjs_translator_service__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(/*! @services/angularjs-translator.service */ "./src/app/core/services/angularjs-translator.service.ts");
/* harmony import */ var _app_core_services_site_constants_service__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__(/*! ./app/core/services/site-constants.service */ "./src/app/core/services/site-constants.service.ts");
/* harmony import */ var _app_core_services_tap_service__WEBPACK_IMPORTED_MODULE_26__ = __webpack_require__(/*! ./app/core/services/tap.service */ "./src/app/core/services/tap.service.ts");
/* harmony import */ var _services_logging_source_translation_service__WEBPACK_IMPORTED_MODULE_27__ = __webpack_require__(/*! @services/logging-source-translation.service */ "./src/app/core/services/logging-source-translation.service.ts");
/* harmony import */ var _services_subscription_service__WEBPACK_IMPORTED_MODULE_28__ = __webpack_require__(/*! @services/subscription.service */ "./src/app/core/services/subscription.service.ts");
/* harmony import */ var _services_redirect_service__WEBPACK_IMPORTED_MODULE_29__ = __webpack_require__(/*! @services/redirect.service */ "./src/app/core/services/redirect.service.ts");
/* harmony import */ var _services_erc_books_read_service__WEBPACK_IMPORTED_MODULE_30__ = __webpack_require__(/*! @services/erc-books-read.service */ "./src/app/core/services/erc-books-read.service.ts");
/* harmony import */ var _services_asset_service__WEBPACK_IMPORTED_MODULE_31__ = __webpack_require__(/*! @services/asset.service */ "./src/app/core/services/asset.service.ts");
/* harmony import */ var _services_optimize_service__WEBPACK_IMPORTED_MODULE_32__ = __webpack_require__(/*! @services/optimize.service */ "./src/app/core/services/optimize.service.ts");
/* harmony import */ var _app_core_models_temp_factories__WEBPACK_IMPORTED_MODULE_33__ = __webpack_require__(/*! ./app/core/models/temp-factories */ "./src/app/core/models/temp-factories.ts");
/* harmony import */ var _services_gift_service__WEBPACK_IMPORTED_MODULE_34__ = __webpack_require__(/*! @services/gift.service */ "./src/app/core/services/gift.service.ts");




if (_environments_environment__WEBPACK_IMPORTED_MODULE_1__["environment"].production) {
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["enableProdMode"])();
    if (window) {
        window.console.log = function () { };
    }
}



var bootstrapFn = function (extraProviders) {
    var platformRef = Object(_angular_platform_browser_dynamic__WEBPACK_IMPORTED_MODULE_3__["platformBrowserDynamic"])(extraProviders);
    return platformRef.bootstrapModule(_app_app_module__WEBPACK_IMPORTED_MODULE_0__["AppModule"]);
};
var downgradedModule = Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeModule"])(bootstrapFn);
angular.module('ng-up', [Globals.GLOBAL_APP_NAME, downgradedModule]);


























// Temporary factories


angular
    .module('ng-up')
    // Services go here
    .factory('ng2UrlHandlingStrategy', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_angular_router__WEBPACK_IMPORTED_MODULE_4__["UrlHandlingStrategy"]))
    .factory('ng2Router', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"]))
    .factory('ngZone', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgZone"]))
    .factory('CaptchaService', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_app_core_services_captcha_service__WEBPACK_IMPORTED_MODULE_9__["CaptchaService"]))
    .factory('TaxService', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_app_core_services_tax_service__WEBPACK_IMPORTED_MODULE_10__["TaxService"]))
    .factory('Data', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_app_core_services_data_service__WEBPACK_IMPORTED_MODULE_7__["DataService"]))
    .factory('MessageHandler', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_app_core_services_message_handler_service__WEBPACK_IMPORTED_MODULE_8__["MessageHandlerService"]))
    .factory('AccountService', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_app_core_services_account_service__WEBPACK_IMPORTED_MODULE_11__["AccountService"]))
    .service('SessionStorageService', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_app_core_services_session_storage_service__WEBPACK_IMPORTED_MODULE_12__["SessionStorageService"]))
    .service('LocalStorageService', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_app_core_services_local_storage_service__WEBPACK_IMPORTED_MODULE_13__["LocalStorageService"]))
    .service('StringService', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_app_core_services_string_service__WEBPACK_IMPORTED_MODULE_14__["StringService"]))
    .service('Logsly', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_app_core_services_logsly_service__WEBPACK_IMPORTED_MODULE_15__["LogslyService"]))
    .service('AfterHoursService', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_app_core_services_after_hours_service__WEBPACK_IMPORTED_MODULE_16__["AfterHoursService"]))
    .service('UserAgent', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_app_core_services_user_agent_service__WEBPACK_IMPORTED_MODULE_17__["UserAgentService"]))
    .service('PromoService', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_app_core_services_promo_service__WEBPACK_IMPORTED_MODULE_18__["PromoService"]))
    .service('ProfileService', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_app_core_services_profile_service__WEBPACK_IMPORTED_MODULE_20__["ProfileService"]))
    .service('ABTestService', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_services_abtest_service__WEBPACK_IMPORTED_MODULE_22__["ABTestService"]))
    .service('SignInService', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_app_core_services_sign_in_service__WEBPACK_IMPORTED_MODULE_21__["SignInService"]))
    .service('QueryStringService', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_services_query_string_service__WEBPACK_IMPORTED_MODULE_23__["QueryStringService"]))
    .service('AngularjsTranslatorService', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_services_angularjs_translator_service__WEBPACK_IMPORTED_MODULE_24__["AngularjsTranslatorService"]))
    .service('SiteConstants', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_app_core_services_site_constants_service__WEBPACK_IMPORTED_MODULE_25__["SiteConstantsService"]))
    .service('BigQuery', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_services_big_query_service__WEBPACK_IMPORTED_MODULE_19__["BigQueryService"]))
    .service('TapService', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_app_core_services_tap_service__WEBPACK_IMPORTED_MODULE_26__["TapService"]))
    .service('GiftService', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_services_gift_service__WEBPACK_IMPORTED_MODULE_34__["GiftService"]))
    .service('LoggingSourceTranslation', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_services_logging_source_translation_service__WEBPACK_IMPORTED_MODULE_27__["LoggingSourceTranslationService"]))
    .service('SubscriptionService', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_services_subscription_service__WEBPACK_IMPORTED_MODULE_28__["SubscriptionService"]))
    .service('RedirectService', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_services_redirect_service__WEBPACK_IMPORTED_MODULE_29__["RedirectService"]))
    .service('ErcBooksReadService', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_services_erc_books_read_service__WEBPACK_IMPORTED_MODULE_30__["ErcBooksReadService"]))
    .service('AssetService', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_services_asset_service__WEBPACK_IMPORTED_MODULE_31__["AssetService"]))
    .service('OptimizeService', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_services_optimize_service__WEBPACK_IMPORTED_MODULE_32__["OptimizeService"]))
    // Temporary factories
    .service('AccountModel', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_app_core_models_temp_factories__WEBPACK_IMPORTED_MODULE_33__["AccountModelFactory"]))
    .service('SubscriptionModel', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_app_core_models_temp_factories__WEBPACK_IMPORTED_MODULE_33__["SubscriptionModelFactory"]))
    .service('Product', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_app_core_models_temp_factories__WEBPACK_IMPORTED_MODULE_33__["ProductFactory"]))
    .service('Promo', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeInjectable"])(_app_core_models_temp_factories__WEBPACK_IMPORTED_MODULE_33__["PromoFactory"]))
    // Service bootstrap component
    .directive('serviceBootstrap', Object(_angular_upgrade_static__WEBPACK_IMPORTED_MODULE_5__["downgradeComponent"])({
    component: _app_service_bootstrap_service_bootstrap_component__WEBPACK_IMPORTED_MODULE_6__["ServiceBootstrapComponent"],
}))
    .directive('ng1App', ng1App)
    .directive('routerLink', routerLink);
function ng1App() {
    return {
        template: "\n        <service-bootstrap (initialized)=\"onInit()\"></service-bootstrap>\n        <epic-header ng-if=\"initialized\"></epic-header>\n        <ui-view ng-if=\"initialized\" id=\"ng-view\" ng-controller=\"MainCtrl\"></ui-view>\n      ",
        controller: function ($scope, $state, $rootScope, $http, $q, $timeout) {
            $scope.onInit = onInit;
            $scope.initialized = false;
            function onInit() {
                $scope.initialized = true;
                // Remove app loader
                var doc = document;
                if (doc) {
                    var loader = doc.getElementById('app-loader');
                    if (loader) {
                        loader.style.display = 'none';
                    }
                }
            }
            var removeListener = $rootScope.$on('$stateChangeStart', function (e, toState, toParams, fromState, fromParams) {
                e.preventDefault();
                console.log('main.ts capture initial state change');
                var targetState = toState.name;
                var targetParams = angular.copy(toParams);
                Globals.initialStateChange = function () {
                    $state.go(targetState, targetParams);
                };
                removeListener();
            });
        },
        scope: {},
    };
}
function routerLink(ng2Router, ngZone) {
    return {
        restrict: 'A',
        scope: {
            routerLink: '@',
        },
        link: function (scope, element, attr) {
            element.on('click', function () {
                ngZone.run(function () { return ng2Router.navigate([scope.routerLink]); });
            });
        },
    };
}
console.log('Bootstrap AngularJS');
angular.bootstrap(document, ['ng-up']);


/***/ }),

/***/ 0:
/*!***************************!*\
  !*** multi ./src/main.ts ***!
  \***************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! /var/www/web/src/src/main.ts */"./src/main.ts");


/***/ })

},[[0,"runtime","vendor"]]]);
//# sourceMappingURL=main.js.map