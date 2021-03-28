import argparse
import json
import os
import pandas as pd
import requests
import time

import common


def get_args():
    parser = argparse.ArgumentParser(description="Parser for get_tags.")
    parser.add_argument("token", help="You have to specify your token to access Qiita.com")
    parser.add_argument("tag", help="You have to specify tag to select articles.")
    parser.add_argument("-p", "--page_num", type=int, default=10, help="The number of pages.")
    parser.add_argument("-pp", "--per_page", type=int, default=1, help="The number of items in each page.")
    parser.add_argument("-o", "--output", default="./output/output.tsv", help="The list of obtained articles.")
    return parser.parse_args()


def check_output_exists(path):
    return os.path.exists(path)


def main():
    args = get_args()
    token = args.token
    selected_tag = args.tag
    output_path = args.output
    page_num, per_page = common.get_correct_page_counts(args.page_num, args.per_page)

    h = common.get_header(token)
    url = "https://qiita.com/api/v2/items?page={}&per_page={}&query=tag%3A{}"

    # for preventing from duplication of the same articles
    already_counted_id_list = []
    if check_output_exists(output_path):
        df = pd.read_table(output_path)
        print(df.head(5))
        already_counted_id_list = df["id"].values

    # create new output file if it does not exist.
    if not os.path.exists(output_path):
        with open(output_path, "w") as f:
            f.write("id\ttags\n")

    # Qiita API call
    with open(output_path, "a") as f:
        print("----- TAG: {} -----".format(selected_tag))
        for page in range(1, page_num + 1):
            api_req = url.format(page, per_page, selected_tag)
            print(api_req)
            res = requests.get(api_req, headers=h)
            data = res.text

            if res.status_code != 200:
                print("Status code: {}".format(res.status_code))
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
