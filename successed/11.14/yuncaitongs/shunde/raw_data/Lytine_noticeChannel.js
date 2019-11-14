//加载公告接口
function loadNoticeData() {
  let _this = this;
  if (_this.loading) {
    return;
  }
  _this.bidsPage = {
    rows: [],
    total: 0
  };

  let params = {
    rows: _this.queryParams.rows,
    page: _this.queryParams.page,
    Mode: _this.mode
  };

  let publicId = null;
  const [COMPOSITE, CUSTOMIZE] = [1, 2];
  switch (_this.platformType) {
    case COMPOSITE:
      publicId = "313";
      break;
    case CUSTOMIZE:
      publicId = _this.queryParams.publicId;
      break;
  }
  if (publicId) {
    /* 存在平台ID才放进去*/
    params.PublicId = publicId;
  }

  if (_this.mode === 0) {
    if (_this.infoType === 1) {
      /*竞价 即将报名*/
      params.State = "3";
      params.NoticeType = "0";
      params["ApplyFromTime>"] = moment(new Date())
        .add(8, "h")
        .toDate();
    } else if (_this.infoType === 2) {
      /*正在报名*/
      params.State = "3";
      params.NoticeType = "0";
      params["ApplyFromTime<"] = moment(new Date())
        .add(8, "h")
        .toDate();
      params["ApplyToTime>"] = moment(new Date())
        .add(8, "h")
        .toDate();
    } else if (_this.infoType === 3) {
      /*即将报价*/
      params.State = "3";
      params.NoticeType = "0";
      params["ApplyToTime<"] = moment(new Date())
        .add(8, "h")
        .toDate();
      params["UppriceFromTime>"] = moment(new Date())
        .add(8, "h")
        .toDate();
    } else if (_this.infoType === 4) {
      /*正在报价*/
      params.State = "3";
      params.NoticeType = "0";
      params["UppriceFromTime<"] = moment(new Date())
        .add(8, "h")
        .toDate();
      params["UppriceToTime>"] = moment(new Date())
        .add(8, "h")
        .toDate();
    } else if (_this.infoType === 5) {
      /*报价结束*/
      params.State = "3";
      params.NoticeType = "0";
      params["UppriceToTime<"] = moment(new Date())
        .add(8, "h")
        .toDate();
    } else if (_this.infoType === 7) {
      params.NoticeType = "5";
    } else if (_this.infoType === 8) {
      params.NoticeType = "1";
    } else if (_this.infoType === 9) {
      params.NoticeType = "6";
    }
  } else if (_this.mode === 1) {
    if (_this.infoType === 1) {
      /*调研 即将报名*/
      params.State = "3";
      params.NoticeType = "7";
      params["ApplyFromTime>"] = moment(new Date())
        .add(8, "h")
        .toDate();
    } else if (_this.infoType === 2) {
      /* 正在报名*/
      params.State = "3";
      params.NoticeType = "7";
      params["ApplyFromTime<"] = moment(new Date())
        .add(8, "h")
        .toDate();
      params["ApplyToTime>"] = moment(new Date())
        .add(8, "h")
        .toDate();
    } else if (_this.infoType === 6) {
      /* 报名结束*/
      params.State = "3";
      params.NoticeType = "7";
      params["ApplyToTime<"] = moment(new Date())
        .add(8, "h")
        .toDate();
    } else if (_this.infoType === 7) {
      params.NoticeType = "8";
    } else if (_this.infoType === 8) {
      params.NoticeType = "1";
    } else if (_this.infoType === 9) {
      params.NoticeType = "3";
    }
  }

  let today = new Date(new Date(new Date().toLocaleDateString()).getTime()); // 当天0点
  if (_this.timeLimit === 6 && _this.queryParams.period != null) {
    params["NoticeDate>"] = moment(_this.queryParams.period[0])
      .add(8, "h")
      .toDate();
    params["NoticeDate<"] = moment(_this.queryParams.period[1])
      .add(1, "d")
      .add(8, "h")
      .toDate();
  } else if (_this.timeLimit === 1) {
    params["NoticeDate>"] = moment(today)
      .add(8, "h")
      .toDate();
    params["NoticeDate<"] = moment(today)
      .add(1, "d")
      .add(8, "h")
      .toDate();
  } else if (_this.timeLimit === 2) {
    params["NoticeDate>"] = moment(today)
      .add(-2, "d")
      .add(8, "h")
      .toDate();
    params["NoticeDate<"] = moment(today)
      .add(1, "d")
      .add(8, "h")
      .toDate();
  } else if (_this.timeLimit === 3) {
    params["NoticeDate>"] = moment(today)
      .add(-6, "d")
      .add(8, "h")
      .toDate();
    params["NoticeDate<"] = moment(today)
      .add(1, "d")
      .add(8, "h")
      .toDate();
  } else if (_this.timeLimit === 4) {
    params["NoticeDate>"] = moment(today)
      .add(-1, "M")
      .add(1, "d")
      .add(8, "h")
      .toDate();
    params["NoticeDate<"] = moment(today)
      .add(1, "d")
      .add(8, "h")
      .toDate();
  } else if (_this.timeLimit === 5) {
    params["NoticeDate>"] = moment(today)
      .add(-1, "y")
      .add(1, "d")
      .add(8, "h")
      .toDate();
    params["NoticeDate<"] = moment(today)
      .add(1, "d")
      .add(8, "h")
      .toDate();
  }

  if (_this.queryParams.projectName) {
    //搜索项目名称
    params["Project_Name%"] = _this.queryParams.projectName;
  }

  _this.loading = true;
  axios({
    url: NOTICE_PAGE_URL,
    method: "get",
    params
  })
    .then(resp => {
      _this.bidsPage.rows = resp.data.rows;
      _this.bidsPage.total = resp.data.total;
      _this.loading = false;
    })
    .catch(err => {
      _this.loading = false;
    });
}

const noticeChannelApp = new Vue({
  el: "#notice-channel-app",
  data: () => {
    return {
      loading: false,
      platformType: 0,
      infoType: 0,
      timeLimit: 0,
      queryParams: {
        period: null,
        publicId: null,
        projectName: "",
        rows: 30, // 每一页的数据条数
        page: 1, // 当前页
        type: "0" // 公告类型
      },
      mode: 0, // 0: 竞价 1：调研
      bidsPage: {
        rows: [],
        total: 0
      },
      activeName: "first",
      platforms: PLATFORMS.filter(i => i.publicId),
      platformsForSelector: [],
      selectedPlatform: ""
    };
  },
  computed: {
    timeText: function() {
      let text = "结束时间";
      switch (this.infoType) {
        case 0:
          text = "结束时间";
          break;
        case 1:
          text = "距离开始报名时间";
          break;
        case 2:
          text = "剩余报名时间";
          break;
        case 3:
          text = "距离开始报价时间";
          break;
        case 4:
          text = "剩余报价时间";
          break;
        case 5:
          text = "";
          break;
        case 6:
          text = "报名结束时间";
          break;
        case 7:
          text = "";
          break;
        case 8:
          text = "";
          break;
        case 9:
          text = "";
          break;
      }
      return text;
    }
  },
  watch: {
    mode: function() {
      this.generatePlatformTree();
    }
  },
  methods: {
    loadNoticeData,
    handleSelectPlatform(value) {
      let id;
      if (value.length) {
        id = value[value.length - 1];
      }
      let platform = findPlatformById(id);
      if (platform) {
        this.queryParams.publicId = platform.publicId;
      } else {
        this.queryParams.publicId = null;
      }
      this.platformType = 2;
      this.search();
    },
    generatePlatformTree() {
      let tree = [];
      if (this.mode === 0) {
        tree = createPlatformTreeForSelector(1);
      } else if (this.mode === 1) {
        tree = createPlatformTreeForSelector(1, 2);
      }
      let treeForSelector = [];

      function convert(node1, node2) {
        if (node1.isOldPlatform) {
          return;
        }
        let node = {
          value: node1.id,
          label: node1.name
        };
        node2.push(node);
        if (!node1.children.length) {
          return;
        }
        node.children = [];
        node1.children.forEach(n => convert(n, node.children));
      }

      tree.forEach(p => convert(p, treeForSelector));
      this.platformsForSelector = treeForSelector;
    },
    goNoticePage(publicId, id) {
      let p = this.getPlatform(publicId);
      window.open(`${p.noticePageLink}?Id=${id}`);
    },
    getPlatform(publicId) {
      let target = this.platforms.filter(p => p.publicId == publicId);
      return target[0];
    },
    goPage: function(page) {
      // window.location.href = '#bids';
      this.queryParams.page = page;
      this.loadNoticeData();
    },
    setPlatformType(type) {
      let _this = this;
      if (_this.loading) {
        return;
      }
      if (type !== 2) {
        _this.selectedPlatform = "";
      }
      _this.platformType = type;
      _this.search();
    },
    setInfoType(type) {
      let _this = this;
      if (_this.loading) {
        return;
      }
      _this.infoType = type;
      _this.search();
    },
    setTimeLimit(type) {
      let _this = this;
      if (_this.loading) {
        return;
      }
      _this.timeLimit = type;
      if (type !== 6) {
        _this.queryParams.period = null;
        _this.search();
      }
    },
    search() {
      this.queryParams.page = 1;
      this.loadNoticeData();
    },
    getPeriod(bid) {
      let result = {
        start: 0,
        end: 0
      };
      let status = this.getStatus(bid);
      let noticeDate = new Date(bid.NoticeDate).getTime();

      if (status === 0) {
        result.start = noticeDate;
        result.end = new Date(bid.ApplyFromTime).getTime();
      } else if (status === 1) {
        result.start = new Date(bid.ApplyFromTime).getTime();
        result.end = new Date(bid.ApplyToTime).getTime();
      } else if (status === 2) {
        result.start = new Date(bid.ApplyToTime).getTime();
        result.end = new Date(bid.UppriceFromTime).getTime();
      } else if (status === 3) {
        result.start = new Date(bid.UppriceFromTime).getTime();
        result.end = new Date(bid.UppriceToTime).getTime();
      }
      return result;
    },
    getStatus: function(bid) {
      //获取竞价公告的各个时间段
      let currentTime = new Date().getTime();
      let applyTimeBegin = new Date(bid.ApplyFromTime).getTime();
      let applyTimeEnd = new Date(bid.ApplyToTime).getTime();
      let uppriceTimeBegin = new Date(bid.UppriceFromTime).getTime();
      let uppriceTimeEnd = new Date(bid.UppriceToTime).getTime();
      if (currentTime < applyTimeBegin) {
        return 0;
      } else if (applyTimeBegin < currentTime && currentTime <= applyTimeEnd) {
        return 1;
      } else if (
        applyTimeEnd < currentTime &&
        currentTime <= uppriceTimeBegin
      ) {
        return 2;
      } else if (
        uppriceTimeBegin < currentTime &&
        currentTime <= uppriceTimeEnd
      ) {
        return 3;
      } else if (currentTime > uppriceTimeEnd) {
        return 4;
      }
    },
    getDays: function(millis) {
      // 1min = 60000ms, 1h = 3600000ms
      return parseInt(millis / 86400000);
    },
    getHours: function(millis) {
      // 1min = 60000ms, 1h = 3600000ms
      return parseInt((millis % 86400000) / 3600000);
    },
    getMinutes: function(millis) {
      return parseInt(((millis % 86400000) % 3600000) / 60000);
    },
    getSeconds: function(millis) {
      return parseInt((((millis % 86400000) % 3600000) % 60000) / 1000);
    },
    handleChangeMode(tab, event) {
      //竞价与调研切换
      if (tab.name === "first") {
        this.mode = 0;
      } else if (tab.name === "second") {
        this.mode = 1;
      }
      this.timeLimit = 0;
      this.platformType = 0;
      this.infoType = 0;
      this.search();
    }
  },
  created: created,
  filters: {
    formatTime: function(t) {
      return moment(t).format("YYYY-MM-DD HH:mm:ss");
    }
  }
});

function created() {
  this.loadNoticeData();
  this.generatePlatformTree();
}
