self.info = {
    "网上竞价编号": "",
    "网上竞价名称": "",
    "采购人": "",
    "联系人": "",
    "联系电话": "",
    "竞价开始时间": "",
    "竞价截止时间": "",
    "品目类型": "",
    "金额上限": "",
}
{
    "参数": "",
    "单位": item_goods_unti,
    "招标编号": item_code,
    "序号": item_goods_index,
    "产品名称": item_goods_name,
    "产品类别": "",
    "品牌": item_goods_brand,
    "数量": item_goods_number,
    "标配": "",
    "型号": item_goods_type,
    "url": self.page_url,
    "招标平台": "云采链采购一体化平台",
    "售后服务": "",
}
"""INSERT INTO `bidpython`.`tb_bid` 
( `title`, `inviter_number`, `announce_time`, `end_time`, `budget_money`, `platform_id`, `url`, `company` ) 
VALUES 
( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截止时间}', '{金额上限}', 14, '{path}', '{采购人}' );"""
"""
INSERT INTO `bidpython`.`tb_bid_json` 
( `shot`, `platform_name`, `inviter_number`, `url`, `json_kv`, `create_time` ) 
VALUES 
( '', '顺德电子化采购平台', '{网上竞价编号}', '{path}', '{json_kv}', '{time}');
"""
"""INSERT INTO `bidpython`.`tb_bid_result` 
( `title`, `inviter_number`, `announce_date`, `platform_id`, `url`, `company`, `announce_result` ) 
VALUES 
( '{网上竞价名称}', '{网上竞价编号}', '{成交公告时间}', 14, '{path}', '{采购人}', '{中标公司}');
`announce_result`"""

[{
    "规格配置":
    "微软（Microsoft）Surface Laptop 2 超轻薄触控笔记本（13.5英寸 第八代Core i5 8G 256G SSD ）典雅黑 请配蓝牙鼠标，surface原装触控笔，投影仪转换接头，内胆包。",
    "中标供应商": "市北区仁义康电子服务中心",
    "设备名称": "微软surface laptop2 13.5英寸笔记本电脑",
    "品牌": "微软surface",
    "售后服务": "按行业标准提供服务。要求送货上门并提供安装服务。要求原厂原包装正品。最终用户登记为中国海洋大学且序列号官网可查。",
    "中标单价": "9170.0",
    "型号":
    "微软（Microsoft）Surface Laptop 2 超轻薄触控笔记本（13.5英寸 第八代Core i5 8G 256G SSD ）典雅黑",
    "数量": "1"
}]

([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8])))
