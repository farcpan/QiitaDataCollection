import requests

import common


def main():
    h = common.get_header()
    url = "https://qiita.com/api/v2/items?page=1&per_page=1"
    res = requests.get(url, headers=h)
    total_count = int(res.headers['Total-Count'])
    
    print("Total Count of articles: {}".format(total_count))


if __name__ == "__main__":
    main()
