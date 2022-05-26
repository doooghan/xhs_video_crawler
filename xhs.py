import os
import json
import re
import time
import traceback

import requests

import constant
from xhs_topic import get_topic_list
from logger import logger


def get_proxy():
    # 接口返回10个IP内的任意一个，15分钟ip池变一次
    r = requests.get(
        "http://xiaoicecrawlerproxy.trafficmanager.cn/random",
        headers={"Authorization": "Basic eGlhb2ljZXByb3h5OkFkbWluMDEjcHJveHk="},
    )
    return r.text

def get_good_proxy(topic_page_id):
    # ip池内的ip不一定可以访问小红书，需要进行选择
    while True:
        try:
            proxyMeta = get_proxy()
            proxies = {"http": proxyMeta, "https": proxyMeta}

            header, cookies = constant.HEADERS, constant.COOKIES
            r = requests.get(f"https://www.xiaohongshu.com/page/topics/{topic_page_id}?fullscreen=true&naviHidden=yes&xhsshare=CopyLink&appuid=5a6c523811be1024170371e3&apptime=1641374883",
                headers=header,
                cookies=cookies,
                proxies=proxies,
                timeout=constant.TIMEOUT
            )

            r.raise_for_status()
            logger.debug(r.text)
            logger.info(f'proxies success: {proxyMeta}')
            logger.info(f'response header[xhs-real-ip]: {r.headers["xhs-real-ip"]}')
            return proxies
        except Exception as e:
            logger.info(f'proxies error {proxyMeta}')

def req(url, proxies):
    header, cookies = constant.HEADERS, constant.COOKIES

    r = requests.get(
        url, # "https://www.xiaohongshu.com/web_api/sns/v3/page/notes?page_size=6&sort=hot&page_id=5be4161813138c000140f9f3&cursor=&sid=",
        headers=header,
        cookies=cookies,
        proxies=proxies,
        # verify=False,
        timeout=constant.TIMEOUT
    )
    # logger.info(r.status_code)
    r.raise_for_status()
    text = r.text
    # logger.info(text)
    return json.loads(text)

def string_format(s):
    ss = re.findall("[\u4e00-\u9fa5a-zA-Z0-9]+", s, re.S)
    return "".join(ss)

def topic_api_once(topic_page_id, cursor="", page_size=20, sort="hot", proxies=None):
    data = {"cursor": "", "notes":[], "has_more":False}
    api = f'https://www.xiaohongshu.com/web_api/sns/v3/page/notes?page_size={page_size}&sort={sort}&page_id={topic_page_id}&cursor={cursor}&sid='
    logger.info(f'{topic_page_id} 请求 {api} ')
    res = req(api, proxies)
    # logger.debug(res)
    if "data" not in res:
        return data
    else:
        notes = res["data"]["notes"]
        for note in notes:
            my_note = {
                "id": note["id"],
                "type": note["type"],
                "title": string_format(note["title"]),
                "video_url": note.get("video_info", {}).get("url", ""),
                "images_list": [
                    r.get("url") or r.get("url_size_large")
                    for r in note.get("images_list", [])
                ],
                "cursor": note["cursor"],
            }
            data["notes"].append(my_note)
        data["cursor"] = res["data"]["cursor"]
        data["has_more"] = res["data"]["has_more"]
        return data

def topic_crawler_task(topic_page_id, file=None):
    cursor = ""
    count = 0
    proxies = get_good_proxy(topic_page_id)

    while True:
        logger.info(f'{topic_page_id} 的第 {count} 次')
        count += 1

        try:
            data = topic_api_once(topic_page_id, cursor, page_size=constant.PAGE_SIZE, sort="time", proxies=proxies)
        except requests.exceptions.ConnectTimeout:
            logger.warning(f'ConnectTimeout, 任务超时，退出')
            break
        except requests.exceptions.HTTPError:
            logger.warning(f'HTTPError, 一般是 461 错误（谈滑块了）, 退出')
            break
        except Exception as e:
            logger.warning(f'收尾， {traceback.format_exc()}')
            break

        all_file = os.path.join(constant.XIAOHONGSHU_DIR,  constant.XHS_RESULT_ALL_FILE)
        # 写入总文件和 today 文件
        with open(file, "a+") as fd, open(all_file, "a+") as all_fd:
            for note in data["notes"]:
                line = "\t".join([
                            topic_page_id,
                            note["id"],
                            note["type"],
                            note["title"],
                            note["video_url"],
                            json.dumps(note["images_list"], separators=(",", ":")),
                            ])+ "\n"
                logger.debug(line)
                fd.write(line)
                fd.flush()
                all_fd.write(line)
                all_fd.flush()

        cursor = data["cursor"]
        has_more = data["has_more"]
        if not has_more:
            break

        time.sleep(constant.REQ_SLEEP_TIME)

def all_topic(today_backup_file):
    topic_list = get_topic_list()
    for num, topic in enumerate(topic_list):
        topic_name, topic_page_id, topic_url = topic
        # logger.info("-" * 60)
        logger.info(f"topic: {num}, {topic_name}, {topic_page_id} start")
        # search topics
        topic_crawler_task(topic_page_id, today_backup_file)
        logger.info(f"topic: {num}, {topic_name}, {topic_page_id} end")
        # logger.info("-" * 60)
        
        time.sleep(60)

def main():
    # 创建今日文件夹
    today_dir = os.path.join(
        constant.XIAOHONGSHU_DATA_DIR, f"xhs_{time.strftime('%Y%m%d', time.localtime())}"
    )
    os.makedirs(today_dir, exist_ok=True)

    # 备份文件
    today_backup_file = os.path.join(today_dir, constant.TODAY_BACKUP_FILE)

    # 在今日文件夹下，生成任务，将任务记载在文件中
    all_topic(today_backup_file)
    # topic_crawler_task("5bef71b7ffd6080001bf9eb3", today_backup_file)


if __name__ == "__main__":
    main()