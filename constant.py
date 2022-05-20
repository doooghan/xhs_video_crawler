import os

CONF_DIR = os.path.dirname(os.path.abspath(__file__))
TOPIC_DIR = os.path.join(CONF_DIR, "topic")
VIDEO_DIR = os.path.join(CONF_DIR, "video")
XIAOHONGSHU_DIR = os.path.join(VIDEO_DIR, "xiaohongshu")
XIAOHONGSHU_DATA_DIR = os.path.join(XIAOHONGSHU_DIR, "data")


# xiaohongshu headers
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.douyin.com/",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
}

TOPIC_FILE_LIST = [
    os.path.join(TOPIC_DIR, "xhs_topics_p00.txt"),
    os.path.join(TOPIC_DIR, "xhs_topics_p0.txt"),
    os.path.join(TOPIC_DIR, "xhs_topics_p1.txt"),
    os.path.join(TOPIC_DIR, "xhs_topics_p2.txt"),
]

# xiaohognshu crawler url
# xhs_topics = "https://www.xiaohongshu.com/web_api/sns/v3/page/notes?page_size={page_size}&sort=hot&page_id={page_id}&cursor={cursor}&sid="
XHS_TOPIC_URL = "https://www.xiaohongshu.com/web_api/sns/v3/page/notes?page_size={page_size}&sort=hot&page_id={page_id}&cursor={cursor}&sid="

# 爬虫任务总文件
# result_all = "xhs_search_topic_result_all.txt"
XHS_RESULT_ALL_FILE = "xhs_search_topic_result_all.txt"
# 当日任务备份文件
# today_backup_file = "today_backup.txt"
TODAY_BACKUP_FILE = "today_backup.txt"
# 当日去重后的任务文件
# xhs_search_topic_result = "xhs_search_topic_result.txt"
XHS_SEARCH_TOPIC_RESULT_FILE = "xhs_search_topic_result.txt"
