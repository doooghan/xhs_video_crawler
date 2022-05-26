import constant


def read_xhs_topics_file(file_name):
    topics = []
    with open(file_name, "r") as topics_fd:
        topic_name = topic_url = ""
        for i, topic_line in enumerate(topics_fd):
            topic_line = topic_line.strip()
            if i % 2 == 0:
                topic_name = topic_line
            if i % 2 == 1:
                topic_url = topic_line
            if i % 2 == 1:
                topic_page_id = topic_url[topic_url.rfind("/") + 1 : topic_url.find("?")]
                topics.append((topic_name, topic_page_id, topic_url))
    return topics


def get_topic_list():
    file_list = constant.TOPIC_FILE_LIST
    topics = []
    for file in file_list:
        topics.extend(read_xhs_topics_file(file))
    return topics


if __name__ == "__main__":
    topics = get_topic_list()
    print(topics)
    print(len(topics))
