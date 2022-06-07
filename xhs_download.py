import os
import json
import time
import traceback

import requests

import constant
from xhs_topic import get_topic_list
from logger import logger

def http_download(url, save_file, session=None):
    with open(save_file, "wb+") as save_file_fd:
        r = session.get(
            url,
            verify=False,
            timeout=constant.TIMEOUT
        )
        # logger.debug(r.status_code)
        r.raise_for_status()
        content = r.content

        save_file_fd.write(content)
    return save_file


def xhs_topic_download(today_dir, xhs_search_topic_result):
    # read topics
    root_path = today_dir

    topic_list = get_topic_list()
    topics = {}
    for topic in topic_list:
        topic_name, topic_page_id, topic_url = topic
        topics[topic_page_id] = {}
        topics[topic_page_id]["topic_name"] = topic_name
        topics[topic_page_id]["topic_url"] = topic_url

    header, cookies = constant.HEADERS, constant.COOKIES
    session = requests.Session()
    session.headers.update(header)
    session.headers.update({'referer': 'https://www.xiaohongshu.com/'})
    session.cookies.update(cookies)

    with open(xhs_search_topic_result, "r") as topic_fd:
        for line_no, topic_line in enumerate(topic_fd):
            try:
                fields = topic_line.split("\t")
                topic_page_id = fields[0]
                item_id = fields[1]
                item_type = fields[2]
                topic_title = fields[3]
                video_url = fields[4]
                images_list = json.loads(fields[5])

                if topic_page_id not in topics:
                    logger.info(f"{topic_page_id} pass")
                    continue
                topic_name = topics[topic_page_id]["topic_name"].strip()
                os.makedirs(os.path.join(root_path, topic_name), exist_ok=True)
                if item_type == "normal":
                    topic_path = os.path.join(root_path, topic_name, "picture")
                elif item_type == "video":
                    topic_path = os.path.join(root_path, topic_name, "video")
                else:
                    raise Exception(f"invalid topic type: {item_type}")
                os.makedirs(topic_path, exist_ok=True)


                if item_type == "normal":
                    for i, image_url in enumerate(images_list):
                        save_file = os.path.join(topic_path, f"{item_id}-{i}.jpg")
                        http_download(image_url, save_file, session)
                        time.sleep(0.2)
                elif item_type == "video":
                    save_file = os.path.join(topic_path, f"{item_id}.mp4")
                    http_download(video_url, save_file, session)
                    time.sleep(0.2)
                else:
                    raise Exception(f"invalid topic type: {item_type}")

                logger.info(f"lineno: {line_no} downloaded... {topic_name}, {topic_page_id}, {item_id}")
            except requests.exceptions.ReadTimeout:
                logger.warning(f"download ReadTimeout error,  lineno:{line_no}, : {topic_name}, {topic_page_id}, {item_id}")
            except Exception as e:
                logger.warning(f"download error lineno:{line_no}, : {traceback.format_exc()}, {topic_name}, {topic_page_id}, {item_id}")
            # break

def main():
    # 创建今日文件夹
    today_dir = os.path.join(
        constant.XIAOHONGSHU_DATA_DIR, f"xhs_{time.strftime('%Y%m%d', time.localtime())}"
    )
    os.makedirs(today_dir, exist_ok=True)

    # 备份文件
    today_backup_file = os.path.join(today_dir, constant.TODAY_BACKUP_FILE)

    # 根据记载文件进行下载
    xhs_topic_download(today_dir, today_backup_file)


if __name__ == "__main__":
    main()