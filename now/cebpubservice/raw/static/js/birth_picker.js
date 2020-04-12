!function(win){
    var x_panel = new X_panel({
        title : "请选择生日"
    });
    var create_year = function(){
        var arr = [];
        for(var i=1900; i<2050; i++){
            arr.push(i + "年");
        }
        return arr;
    }
    var create_month = function(){
        var arr = [];
        for(var i=1; i<13; i++){
            arr.push(i + '月');
        }
        return arr;
    }
    var create_date = function(){
        var a = [];//30
        var b = [];//31
        var c = [];//28
        var d = [];//29
        for(var i=1; i<31; i++){
            a.push(i+'日');
        }
        for(var i=1; i<32; i++){
            b.push(i+'日');
        }
        for(var i=1; i<29; i++){
            c.push(i+'日');
        }
        for(var i=1; i<30; i++){
            d.push(i+'日');
        }
        return {
            "30" : a
            ,"31" : b
            ,"28" : c
            ,"29" : d
        }
    }
    
    var year = new X_picker({
        data:create_year()
    });
    var month =new X_picker({
        data:create_month()
    });
    var date = new X_picker({
        data:(create_date())["31"]
    });
    var set_date = function(){
        var year_value = year.value.slice(0,year.value.length-1);
        var month_value = month.value.slice(0,month.value.length - 1);
        var day = new Date(year_value,month_value,0);
        var count = day.getDate();
        var list = (create_date())["" + count];
        date.set_opts(list);
        if(date.index >= date.index_count)date.set(date.index_count - 1);
    }
    var mount_value = function(){
        x_panel.rs.year = year.value;
        x_panel.rs.month = month.value;
        x_panel.rs.date = date.value;
    }
    year.set(100);
    set_date();
    mount_value();
    year.changed(function(){
        set_date();
        mount_value();
    })
    month.changed(function(){
        set_date();
        mount_value();
    })
    date.changed(function(){
        mount_value();
    })
    x_panel.add(year.el,month.el,date.el);
    win.birth_picker = x_panel;
}(this);