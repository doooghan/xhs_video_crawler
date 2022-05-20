import os
import time
import re
import json
import traceback
import logging
import logging.handlers
import datetime

import constant

from xhs_topic import get_topic_list
from xhs_session import xhs_topic_session
from http_download import http_download

logger = logging.getLogger("mylogger")
logger.setLevel(logging.DEBUG)

rf_handler = logging.handlers.TimedRotatingFileHandler(
    "crawler.log",
    when="midnight",
    interval=1,
    backupCount=7,
    atTime=datetime.time(0, 0, 0, 0),
)
rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logger.addHandler(rf_handler)


def xhs_topic_download(today_dir, xhs_search_topic_result):
    # session = xhs_topic_session()

    # read topics
    root_path = today_dir

    topic_list = get_topic_list()
    topics = {}
    for topic in topic_list:
        topic_name, topic_url = topic
        topic_page_id = topic_url[topic_url.rfind("/") + 1 : topic_url.find("?")]
        topics[topic_page_id] = {}
        topics[topic_page_id]["topic_name"] = topic_name
        topics[topic_page_id]["topic_url"] = topic_url

    with open(xhs_search_topic_result, "r") as topic_fd:
        for line_no, topic_line in enumerate(topic_fd):
            if line_no % 1000 == 0:
                session = xhs_topic_session()
            try:
                fields = topic_line.split("\t")
                page_id = fields[0]
                topic_id = fields[1]
                topic_type = fields[2]
                topic_title = fields[3]
                video_url = fields[4]
                images_list = json.loads(fields[5])

                if page_id not in topics:
                    logger.warning(f"{page_id} pass")
                    continue
                topic_name = topics[page_id]["topic_name"].strip()
                os.makedirs(os.path.join(root_path, topic_name), exist_ok=True)
                if topic_type == "normal":
                    topic_path = os.path.join(root_path, topic_name, "picture")
                elif topic_type == "video":
                    topic_path = os.path.join(root_path, topic_name, "video")
                else:
                    raise Exception(f"invalid topic type: {topic_type}")
                os.makedirs(topic_path, exist_ok=True)
                if topic_type == "normal":
                    for i, image_url in enumerate(images_list):
                        save_file = os.path.join(topic_path, f"{topic_id}-{i}.jpg")
                        http_download(session, image_url, save_file)
                        time.sleep(0.2)
                if topic_type == "video":
                    save_file = os.path.join(topic_path, f"{topic_id}.mp4")
                    http_download(session, video_url, save_file)
                    time.sleep(0.2)
                logger.info(f"lineno: {line_no} downloaded...")
            except Exception as e:
                logger.error(f"download error lineno:{line_no}, : {e}")
            # break


def string_format(s):
    ss = re.findall("[\u4e00-\u9fa5a-zA-Z0-9]+", s, re.S)
    return "".join(ss)


def search(session, page_id, count=-1, fd=None):
    final_result = []
    cur_page = 1
    cur_count = 0
    cursor = ""
    while True:
        result = search_once(session, page_id, cursor, cur_page=cur_page)
        if fd:
            for r in result["data"]:
                fd.write(
                    "\t".join(
                        [
                            page_id,
                            r["id"],
                            r["type"],
                            r["title"],
                            r["video_url"],
                            json.dumps(r["images_list"], separators=(",", ":")),
                        ]
                    )
                    + "\n"
                )
                fd.flush()
                cur_count += 1
        else:
            final_result.extend(result["data"])
        cursor = result["cursor"]
        cur_page += 1
        if not result.get("has_more", False) or (
            count > 0 and (len(final_result) >= count or cur_count >= count)
        ):
            break
        time.sleep(2)
        # break
    return final_result


def search_once(session, page_id, cursor="", page_size=20, cur_page=1):
    results = {"data": [], "cursor": cursor}
    search_url = constant.XHS_TOPIC_URL.format(
        page_size=page_size, page_id=page_id, cursor=cursor
    )
    try:
        response = session.get(search_url, verify=False).text
        resp_dict = json.loads(response)
        if "data" not in resp_dict:
            logger.warn(resp_dict)

        records = resp_dict["data"]["notes"]
        for i, record in enumerate(records):
            try:
                results["data"].append(
                    {
                        "id": record["id"],
                        "type": record["type"],
                        "title": string_format(record["title"]),
                        "video_url": record.get("video_info", {}).get("url", ""),
                        "images_list": [
                            r.get("url") or r.get("url_size_large")
                            for r in record.get("images_list", [])
                        ],
                        "cursor": record["cursor"],
                    }
                )
            except:
                logger.error(
                    f"search error, page_num:{cur_page}-{i} {traceback.format_exc()}"
                )
        del resp_dict["data"]["notes"]
        logger.info(f"{page_id} - {resp_dict}")
        results.update(resp_dict["data"])
    except:
        logger.error(f"search error, page_num:{cur_page} {traceback.format_exc()}")
    return results


def xhs_topic_crawler_task(file):
    # 将今天需要抓取的任务生成到 file 中
    topic_list = get_topic_list()
    file_fd = open(file, "w")

    for topic in topic_list:
        session = xhs_topic_session()

        topic_name, topic_url = topic
        topic_page_id = topic_url[topic_url.rfind("/") + 1 : topic_url.find("?")]

        # search topics
        session.headers.update({"referer": topic_url[: topic_url.find("?")]})
        search(session, topic_page_id, fd=file_fd)
        # break
    file_fd.close()


def crawler_id_deduplication(all_file, backup_file, dedup_file):
    # 将今天的任务去重
    all_set = set()
    with open(all_file) as all_fd:
        for line_no, topic_line in enumerate(all_fd):
            fields = topic_line.split("\t")
            topic_id = fields[1]
            all_set.add(topic_id)

    dedup_set = set()
    with open(all_file, "a+") as all_fd, open(backup_file) as backup_fd, open(
        dedup_file, "w"
    ) as dedup_fd:
        for line_no, topic_line in enumerate(backup_fd):
            fields = topic_line.split("\t")
            topic_id = fields[1]
            if topic_id not in all_set and topic_id not in dedup_set:
                dedup_fd.write(topic_line)
                all_fd.write(topic_line)
                dedup_set.add(topic_id)


def main():
    """小红书抓取思路
    1. 生成任务，根据 topic 文件内生成对应的 topic_list , 根据 topic_list 将预计需要抓取的数据存入 today_backup_file
    2. 去重，将backup的文件与总文件对比并和自身对比，生成新文件(xhs_search_topic_result)
    3. 根据新文件进行下载
    """

    # 创建今日文件夹
    today_dir = os.path.join(
        constant.XIAOHONGSHU_DATA_DIR, f"xhs_{time.strftime('%Y%m%d', time.localtime())}"
    )
    os.makedirs(today_dir, exist_ok=True)

    # 备份文件
    today_backup_file = os.path.join(today_dir, constant.TODAY_BACKUP_FILE)
    # 总文件
    xhs_result_all_file = os.path.join(constant.XIAOHONGSHU_DIR, constant.XHS_RESULT_ALL_FILE)
    # 去重后的文件
    xhs_search_topic_result_file = os.path.join(
        today_dir, constant.XHS_SEARCH_TOPIC_RESULT_FILE
    )

    logger.info("task start")
    xhs_topic_crawler_task(today_backup_file)
    logger.info("task end")

    # logger.info("dedup start")
    # crawler_id_deduplication(
    #     xhs_result_all_file, today_backup_file, xhs_search_topic_result_file
    # )
    # logger.info("dedup end")

    # logger.info("download start")
    # xhs_topic_download(today_dir, xhs_search_topic_result_file)
    # logger.info("download end")


if __name__ == "__main__":
    main()
