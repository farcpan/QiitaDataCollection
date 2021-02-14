import argparse
import json
import os
import pandas as pd
import requests
import time

import common


PER_PAGE = 100
OUT_PATH = "./output/output.tsv"


def get_args():
    parser = argparse.ArgumentParser(description="Parser for get_tags.")
    parser.add_argument("-p", "--page_num", type=int, default=10, help="The number of pages.")
    parser.add_argument("-l", "--list_name", default="./tags/tags.tsv", help="The input file path of the tag list.")
    return parser.parse_args()


def get_tag_list(path):
    df = pd.read_table(path, header=None)
    tag_list = df[0].values
    return tag_list


def check_output_exists():
    return os.path.exists("./output/output.tsv")


def main():
    args = get_args()
    list_name = args.list_name
    page_num = args.page_num

    h = common.get_header()
    url = "https://qiita.com/api/v2/items?page={}&per_page={}&query=tag%3A{}"

    # for preventing from duplication of the same articles
    already_counted_id_list = []
    if check_output_exists():
        df = pd.read_table(OUT_PATH)
        print(df.head(5))
        already_counted_id_list = df["id"].values

    error_flg = False

    tag_list = get_tag_list(list_name)

    with open(OUT_PATH, "a") as f:
        f.write("id\ttags\n")

        for tag_index, tag in enumerate(tag_list):
            print("----- [{}]: {} -----".format(tag_index+1, tag))

            if error_flg:
                print("API Error!")
                break

            for page in range(1, page_num + 1):
                api_req = url.format(page, PER_PAGE, tag)
                res = requests.get(api_req, headers=h)
                data = res.text

                if res.status_code != 200:
                    print("Status code: {}".format(res.status_code))
                    error_flg = True
                    break

                if data is None or data is '':
                    continue
                
                try:
                    d = json.loads(data)
                    for d_item in d:
                        # ignoring already saved article
                        article_id = d_item["id"]
                        if article_id in already_counted_id_list:
                            print("Skip article with id: {}".format(article_id))
                            continue

                        # tag list -> tag concatenated by ","
                        tags = d_item["tags"]
                        tag_list = []
                        for tag in tags:
                            single_tag = tag["name"]
                            tag_list.append(single_tag)
                        tags_str = ",".join(tag_list)
                        #print("id={}, tag_list={}".format(article_id, tags_str))
                        f.write("{}\t{}\n".format(article_id, tags_str))

                        # body
                        body = d_item["body"]
                        with open("./docs/{}.md".format(article_id), "w") as doc_f:
                            doc_f.write(body)
                
                except Exception:
                    pass


if __name__ == '__main__':
    main()
