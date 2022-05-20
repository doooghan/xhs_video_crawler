def http_download(session, url, save_file):
    save_file_fd = open(save_file, "wb+")
    save_file_fd.write(session.get(url).content)
    save_file_fd.close()
    return save_file
