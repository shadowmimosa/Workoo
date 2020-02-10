import requests

path = 'http://zdscxx.moa.gov.cn:8080/misportal/echartReport/webData/最新发布/page1.json?_=1581340376763'

header = {
    'Host':
    'zdscxx.moa.gov.cn:8080',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding':
    'gzip, deflate',
    'Accept-Language':
    'zh-CN,zh;q=0.9',
    # 'Cookie':
    # 'JSESSIONID=23B7C039CAD2766D326E9F2F5E7CDE11; wdcid=2445f1d8cb707e09; yfx_c_g_u_id_10002896=_ck20012123552813424782677373811; yfx_key_10002896=; yfx_mr_10002896=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_mr_f_10002896=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; _trs_uv=k5o28aun_299_axm6; _va_id=280c05c4cb0a958d.1579622129.1.1579622129.1579622129.; _va_ref=%5B%22%22%2C%22%22%2C1579622129%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DL3OuTEjJrzJAnxdvH4FbLJNf-bF7m_UaCMoftIigsZGRUkWonlP2fcoXnFVR14bN%26wd%3D%26eqid%3Defd04a060002f1ab000000025e271eb2%22%5D; yfx_f_l_v_t_10002896=f_t_1579622128261__r_t_1581340350619__v_t_1581340350619__r_c_1'
}

resp = requests.get(path, headers=header)

print(resp)
