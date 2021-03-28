import argparse
import csv
import json
import requests
import time

import common


def get_args():
    parser = argparse.ArgumentParser(description="Parser for get_tags.")
    parser.add_argument("token", help="You have to specify your token to access Qiita.com")
    parser.add_argument("-p", "--page_num", type=int, default=10, help="The number of pages.")
    parser.add_argument("-t", "--count_threshold", type=int, default=30, help="The minimum number of each tag to be saved.")
    parser.add_argument("-f", "--file_name", default="tags", help="The output file name without extension: the extension will be .tsv.")
    return parser.parse_args()


def main():
    args = get_args()
    token = args.token
    page_num = args.page_num
    count_threshold = args.count_threshold
    file_name = args.file_name

    h = common.get_header(token)
    url = "https://qiita.com/api/v2/tags?page={}&per_page=100&sort=count"

    with open("./tags/{}.tsv".format(file_name), "w") as f:
        for page in range(1, page_num + 1):
            print("----------- page={}".format(page))
            res = requests.get(url.format(page).encode("utf-8"), headers=h)
            data = res.text
            d = json.loads(data)

            if res.status_code != 200:
                print("Response status code: {}".format(res.status_code))
                break

            for item in d:
                if item["items_count"] >= count_threshold:
                    data_written = "{}\t{}\t{}\n".format(item["id"], item["followers_count"], item["items_count"])
                    f.write(data_written)

if __name__ == "__main__":
    main()