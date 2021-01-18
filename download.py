import sys
import requests
import os
import pathlib as pl

class Downloader(object):
    def __init__(self, url, file_path):
        self.url = url
        self.file_path = file_path

    def start(self):
        res_length = requests.get(self.url, stream=True)
        total_size = int(res_length.headers['Content-Length'])
        print(res_length.headers)
        print(res_length)
        if os.path.exists(self.file_path):
            temp_size = os.path.getsize(self.file_path)
            print("Now：{:.2f} MB， Total：{:.2f} MB， Downloaded：{:.2f} "\
                  .format(temp_size/1048576, 
                          total_size/1048576, 
                          100 * temp_size / total_size))
        else:
            temp_size = 0
            print("Total：{:.2f} MB，Downloading...".format(total_size / 1048576))

        headers = {'Range': 'bytes=%d-' % temp_size,
                   "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"}
        res_left = requests.get(self.url, stream=True, headers=headers)

        with open(self.file_path, "ab") as f:
            for chunk in res_left.iter_content(chunk_size=1024):
                temp_size += len(chunk)
                f.write(chunk)
                f.flush()

                done = int(50 * temp_size / total_size)
                sys.stdout.write("\r[%s%s] %d%%" % ('█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
                sys.stdout.flush()


if __name__ == '__main__':
    url = "http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.COLA-RSMAS-CCSM4/.MONTHLY/.sst/M/(1.0)/(1.0)/RANGEEDGES/data.nc"
    p_file = "/disk1/tywang/code/NMME_toolkit/COLA-RSMAS-CCSM4_1.nc"
    downloader = Downloader(url, p_file)
    downloader.start()