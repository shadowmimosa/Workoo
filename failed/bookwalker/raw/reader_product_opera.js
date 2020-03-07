/*********************************
* 商品頁js控制
* *******************************/

var Product = function(){}
Product.prototype =
{
    // 點擊更多
    click_more : function (id, thisId, num, content)
    {
        var decode_content = decodeURIComponent(content).replace(/\+/g, " ");

        $("#"+id).html(decode_content).css({"height":"auto"});

        if (thisId == 'more_intro'+num)
        {
            $("#more_intro"+num).remove();
        }
        else if (thisId == 'more_author_intro')
        {
            $("#more_author_intro").remove();
        }

        // 重設 dotdotdot 套件的設定(PC單書頁會用到)
        $(".dotdotdot_box, .prod_dotdotdot_box").css({"height":"auto"});

    },
    // 偵測購書、租書的切換
    switch_buy_type_buttom : function ()
    {
        var buy_type = $("input[name='buy_type']").val();
        if (buy_type == 1)
        {
            $("li.bwbook_btnbuy").addClass('active');
            $("li.bwbook_btnrent").removeClass('active');
        }
        else if (buy_type == 2)
        {
            $("li.bwbook_btnrent").addClass('active');
            $("li.bwbook_btnbuy").removeClass('active');

        }
    },
    // 切換購書、租書的按鈕
    change_buy_rent_info : function (id)
    {
        var buy_class = $("#bw_buy").attr('class'),
            rent_class = $("#bw_rent").attr('class');
        var shopping_type = 1;  //購買類型
        var cart_id = 1;
        if (id == 'bw_rent') //租書
        {
            shopping_type = 2;
            cart_id = 2;
            if($("input[name='product_rent_status']").val() == 1) //正在租閱中
            {
                $(".btn-rented").show();
                $("button#add_cart").hide();
                $("button.cartbtn_fast").hide();
            }
            $("#bw_buy").attr('class', buy_class.replace("active", ""));
            $("#side_price").html('租書：<span class="bw_total">'+$("#"+id).find('.bw_total').html()+'</span>元');
            $("div#rent_hidden").css({"display":"none"});
            $("button.cartbtn_fast").css({"display":"none"});
            $("button.cartbtn_subscribe").css({"display":"none"});
        }
        else //購書
        {
            if($("input[name='product_rent_status']").val() == 1) //正在租閱中
            {
                $(".btn-rented").hide();
                $("button#add_cart").show();
                $("button.cartbtn_fast").show();
            }
            $("#bw_rent").attr('class', buy_class.replace("active", ""));
            $("#side_price").html('購書：<span class="bw_total">'+$("#"+id).find('.bw_total').html()+'</span>元');
            $("div#rent_hidden").css({"display":"block"});
            $("button.cartbtn_fast").css({"display":"block"});
            $("button.cartbtn_subscribe").css({"display":"block"});
        }

        $("input[name='buy_type']").val(shopping_type);
        $("input[name='cart_id']").val(shopping_type);
        $("#"+id).addClass('active');
        $("button#add_cart").attr("onclick","product.add_shopping_cart(['"+$("#input_product_id").val()+"'], '"+$("input[name='buy_type']").val()+"', '"+$("input[name='path']").val()+"', '', '"+cart_id+"');");
        // $("button.cartbtn_fast").attr("onclick","product.add_shopping_cart(['"+$("#input_product_id").val()+"'], '"+$("input[name='buy_type']").val()+"', '"+$("input[name='path']").val()+"', '', '4');");
    },
    // 會員追蹤 ajax
    track_set : function()
    {
        var user_id = $("input[name='user_id']").val(),
        author_id = $("input[name='author_id']").val(),
        vendor_id = $("input[name='vendor_id']").val();

        $('#track-author').on('switchChange.bootstrapSwitch',function (event, state) {
            state = (state === true) ? 1 : 0;

            var request = $.ajax({
                url: "/mobile/product_ajax/track_set",
                method: "get",
                data: {
                    user_id : user_id,
                    author_id : author_id,
                    state : state,
                    _token: '{{ csrf_token() }}'
                }
            });

            request.done(function( msg ) {
                if (state == 1 && msg == 'true')
                {
                    alert('您已追蹤此作者');
                }
                else
                {
                    alert('您已取消追蹤此作者');
                }
            });

            request.fail(function( jqXHR, textStatus ) {
                alert( "Request failed: " + textStatus );
            });
        });

        $('#track-vendor').on('switchChange.bootstrapSwitch',function (event, state) {
            state = (state === true) ? 1 : 0;

            var request = $.ajax({
                url: "/mobile/product_ajax/track_set",
                method: "get",
                data: {
                    user_id : user_id,
                    vendor_id : vendor_id,
                    state : state,
                    _token: '{{ csrf_token() }}'
                }
            });

            request.done(function( msg ) {
                if (state == 1 && msg == 'true')
                {
                    alert('您已追蹤此出版社');
                }
                else
                {
                    alert('您已取消追蹤此出版社');
                }
            });

            request.fail(function( jqXHR, textStatus ) {
                alert( "Request failed: " + textStatus );
            });
        });
    },
    /**
     * 系列整批、單筆寫入商品暫存
     * @param json      product_id 商品id陣列(被json_encode)
     * @param int       type       購買型態
     * @param string    path       pc或 mobile的路徑
     * @param int       batch      是否整批加入購物車
     * @param int       cart_id    購物車代號
     */
    add_shopping_cart : function(product_id,type,path,batch,cart_id)
    {
        var collection_id = $("input[name='collection_id']").val(),
        //購買類型 1.購書(預購、儲值金、快速購書)、2.租書、3.訂閱(只能有此3種狀態)
        buy_type = (type != '')? type : $("input[name='buy_type']").val(),
        cart_id = (cart_id != '')? cart_id : $("input[name='cart_id']").val(),
        cart_cnt = $("#cart_cnt").text(),
        _token = $("input[name='_token']").val(),
        http_host = $("input[name='http_host']").val(),
        id = '';

        if (product_id == '')
        {
            id = collection_id;
        }
        else
        {
            id = product_id;
        }
        //console.log(id+'|'+buy_type+'|'+cart_id+'|'+cart_cnt+'|'+http_host+'|'+_token);return false;
        //執行 ajax
        var request = $.ajax({
            url: "/ajax/add_shopping_cart",
            method: "POST",
            data: {
                product_id_ary : id,
                buy_type : buy_type,
                cart_id : cart_id,
                _token: _token
            }
        });

        request.done(function( msg ) {
            // alert(msg);return false;
            msg = JSON.parse(msg);

            if (msg.code == false)
            {
                alert('加入購物車失敗');
            }
            else if (msg.code == 'already_all_buy')     //在搜尋頁點系列顯示購買整個系列時，如果都買過了，就顯示錯誤訊息
            {
                alert('您已購買過');
            }
            else if (msg.code == 'under_18')      //未滿18歲
            {
                alert('抱歉，您尚未年滿18歲，無法購買限制級書籍。');
            }
            else if (msg.code == 'no_login')      //未登入
            {
                var result = confirm('抱歉，此為限制級書籍，您必須年滿18歲，並先登入方能購書。\n\n確定前往登入?');
                if (result == true)
                {
                    parent.location.href = http_host + path + '/user/login';
                }
                return false;
            }
            else if (msg.code == 'already')      //單一商品已加入時，變換字樣及連結
            {
                if ($.inArray(cart_id, ['3','4','6']) != -1)
                {
                    //導到快速購書頁面
                    if(credit_card_binding == 2)
                    {
                        parent.location.href = http_host + path+'/cart/simple_pay/'+cart_id;
                    }
                    else
                    {
                        parent.location.href = http_host + path+'/explanation/shortcut_service/'+cart_id;
                    }
                }
                else
                {
                    parent.location.href = http_host + path+'/cart/'+buy_type;
                }

            }
            else
            {
                // console.log(id+'-'+buy_type+'-'+path+'-'+batch+'-'+cart_id);return;
                //整批加入
                if (batch == 1)
                {
                    //已加入過
                    if (msg.code == '-1')
                    {
                        parent.location.href = http_host + path+'/cart/'+buy_type;
                    }
                    else
                    {
                        $("#cart_cnt").html('<i class="fa fa-circle fa-stack-1x iconcolor_red"></i><i class="fa fa-inverse fa-stack-1x iconcolor_number">'+msg.count+'</i>');
                        alert('您已將整套加入購物車');
                        $("#collection_shopping").html('進入購物車');
                    }
                }
                else
                {
                    //已加入過
                    if (msg.code == '-1')
                    {
                        //切換成詳細顯示時加入購物車、長期訂購的按鈕判斷
                        if ($.inArray(cart_id, ['3','4','6']) != -1)
                        {
                            //導到快速購書頁面
                            if(credit_card_binding == 2)
                            {
                                parent.location.href = http_host + path+'/cart/simple_pay/'+cart_id;
                            }
                            else
                            {
                                parent.location.href = http_host + path+'/explanation/shortcut_service/'+cart_id;
                            }
                        }
                        else
                        {
                            parent.location.href = http_host + path+'/cart/'+buy_type;
                        }
                    }
                    else
                    {
                        //訂閱、快速購書、儲值金、預購
                        if($.inArray(cart_id, ['3','4','5','6']) != -1 && (buy_type == 1 || buy_type == 2))
                        {
                            $("#cart_cnt").html('<i class="fa fa-circle fa-stack-1x iconcolor_red"></i><i class="fa fa-inverse fa-stack-1x iconcolor_number">'+msg.count+'</i>');
                            //導到快速購書頁面
                            if(credit_card_binding == 2)
                            {
                                parent.location.href = http_host + path+'/cart/simple_pay/'+cart_id;
                            }
                            else
                            {
                                parent.location.href = http_host + path+'/explanation/shortcut_service/'+cart_id;
                            }

                        }
                        //購書、租書
                        else if (buy_type == 1 || buy_type == 2)
                        {
                            if (msg.first == 'true')
                            {
                                alert('已加入購物車');
                            }

                            $(".cartbtn_shoppingcart").html('<i class="fa fa-shopping-cart"></i>  進入購物車');
                        }
                    }
                }
            }
        });

        request.fail(function( jqXHR, textStatus ) {
            console.log(jqXHR);
            console.log(textStatus);
            alert('加入購物車失敗');
        });
    }
}

//星星評價(暫無使用)
// $(document).ready(function() {

//     $('.starrr:eq(0)').on('starrr:change', function(e, value){
//           if (value) {
//             $('.your-choice-was').show();
//             $('.choice').text(value);
//           } else {
//             $('.your-choice-was').hide();
//           }
//     });

// });
