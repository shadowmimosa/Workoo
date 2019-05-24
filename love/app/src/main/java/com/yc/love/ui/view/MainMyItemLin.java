package com.yc.love.ui.view;

import android.content.Context;
import android.content.res.TypedArray;
import android.graphics.drawable.Drawable;
import android.text.TextUtils;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.yc.love.R;

/**
 * Created by mayn on 2019/4/28.
 */

public class MainMyItemLin extends LinearLayout {


//    private TextView mTvDes;

    public MainMyItemLin(Context context, AttributeSet attrs) {
        super(context, attrs);
        initView(context, attrs);
    }

    private void initView(Context context, AttributeSet attrs) {
        TypedArray typedArray = context.obtainStyledAttributes(attrs, R.styleable.MainMyItemLin);
        String text = typedArray.getString(R.styleable.MainMyItemLin_textNameMyItem);
        Drawable imgSrc = typedArray.getDrawable(R.styleable.MainMyItemLin_imgSrc);
        boolean isAddIntervalTop = typedArray.getBoolean(R.styleable.MainMyItemLin_isAddIntervalTop, false);
        boolean isAddIntervalBom = typedArray.getBoolean(R.styleable.MainMyItemLin_isAddIntervalBom, false);

        View inflate = LayoutInflater.from(context).inflate(R.layout.layout_main_my_item_lin, this, true);
        TextView tvDes = inflate.findViewById(R.id.main_my_item_lin_tv_des);
        View viewLineTop = inflate.findViewById(R.id.main_my_item_lin_view_line_top);
        View viewLineBom = inflate.findViewById(R.id.main_my_item_lin_view_line_bom);
        ImageView ivIcon = inflate.findViewById(R.id.main_my_item_lin_iv_icon);
        if (!isAddIntervalTop) {
            viewLineTop.setVisibility(GONE);
        }
        if (!isAddIntervalBom) {
            viewLineBom.setVisibility(GONE);
        }
        tvDes.setText(text);
        ivIcon.setImageDrawable(imgSrc);
    }

/*    public void setDes(String des) {
        if (!TextUtils.isEmpty(des)) {
            mTvDes.setText(des);
        }
    }*/
}
