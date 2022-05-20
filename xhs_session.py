import constant

import requests

requests.packages.urllib3.disable_warnings()

def get_proxy():
    # 接口返回10个IP内的任意一个，15分钟ip池变一次
    r = requests.get(
        "http://xiaoicecrawlerproxy.trafficmanager.cn/random",
        headers={"Authorization": "Basic eGlhb2ljZXByb3h5OkFkbWluMDEjcHJveHk="},
    )
    return r.text

def xhs_topic_session():
    session = requests.Session()
    proxyMeta = get_proxy()

    session.headers.update(constant.HEADERS)
    session.proxies = {"http": proxyMeta, "https": proxyMeta}
    session.cookies.update(
        {
            "xhsTrackerId": "45233f9a-ca79-4be9-cbba-2409d5314f9e",
            # "xhsSEM": "d36c8334-8509-49b4-9cda-09e5092e88f3",
            # "xhsSEM.sig": "W_7-GfPafwzQEODLMiR_vhLzZ8kiPEdF8f3NaxCq1x4",
            "timestamp2": "1652946867567150f444d8e7b34caba0c1b652dddb2d40ccbe7f5df60cf1037",
            "timestamp2.sig": "ZuXvaNw0rdQxiiF_L2YOsKtoDoZO4yRoVtwQDAIuXuQ",
            "smidV2": "2022051812100817cafc97676841fbb0fe4e5c5505debd00ba6f4807fd84bf0",
            "extra_exp_ids": "recommend_comment_hide_exp3,recommend_comment_hide_v2_exp1,recommend_comment_hide_v3_origin,supervision_exp,supervision_v2_exp,commentshow_clt1,gif_exp1,ques_clt2",
        }
    )
    return session
