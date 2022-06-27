import os

CONF_DIR = os.path.dirname(os.path.abspath(__file__))
TOPIC_DIR = os.path.join(CONF_DIR, "topic")
VIDEO_DIR = os.path.join(CONF_DIR, "video")
XIAOHONGSHU_DIR = os.path.join(VIDEO_DIR, "xiaohongshu")
XIAOHONGSHU_DATA_DIR = os.path.join(XIAOHONGSHU_DIR, "data")


# xiaohongshu headers
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Referer": "https://www.douyin.com/",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
}

COOKIES = {
    "extra_exp_ids": "recommend_comment_hide_exp1,recommend_comment_hide_v2_exp2,recommend_comment_hide_v3_origin,supervision_exp,supervision_v2_exp,commentshow_exp1,gif_clt1,ques_clt2",
    "xhsTracker": "url=index&searchengine=google",
    "smidV2": "202205231722121337f6caf923150a28e721735086788f00868cffac71a6580",
    "timestamp2.sig": "0gpfZMhL6VSgZWXKTpqYJ5eUkEa0oCfr5aJEFLKZp6I",
    "timestamp2": "165329772044499eda76d2f99f0f823e3d20ffbdfa663c42316d3ea0e987fac",
    "xhsTrackerId": "e0e61121-3740-4c30-ccca-bfa70685d7a1",
}

TOPIC_FILE_LIST = [
    os.path.join(TOPIC_DIR, "xhs_topics_p00.txt"),
    os.path.join(TOPIC_DIR, "xhs_topics_p0.txt"),
    os.path.join(TOPIC_DIR, "xhs_topics_p1.txt"),
    os.path.join(TOPIC_DIR, "xhs_topics_p2.txt"),
    os.path.join(TOPIC_DIR, "xhs_topics_p3.txt"),
]

# xiaohognshu crawler url
XHS_TOPIC_URL = "https://www.xiaohongshu.com/web_api/sns/v3/page/notes?page_size={page_size}&sort=hot&page_id={page_id}&cursor={cursor}&sid="

# 爬虫任务总文件
XHS_RESULT_ALL_FILE = "xhs_search_topic_result_all.txt"
# 当日任务备份文件
TODAY_BACKUP_FILE = "today_backup.txt"
# 当日去重后的任务文件
XHS_SEARCH_TOPIC_RESULT_FILE = "xhs_search_topic_result.txt"

# 接口timeout时间
TIMEOUT = 5
# 每次请求的数据量
PAGE_SIZE = 20
# 每次请求之间的休眠
REQ_SLEEP_TIME = 1