# QiitaDataCollection

Data collection project via Qiita API. Here are some scripts to get information of Qiita:

* Get tags with more than or equals to 30 followers.
* Get items with the tags you collect.

---

## Preparation

You have to get `Qiita API token` on your Qiita page. In this project, the token with `read_qiita` scope is required. `write_qiita` is not unnecessary. 

---

## Get the number of articles on Qiita

```
$ python check_article_num.py 
Total Count of articles: 640054
```

## Get Tags

You can get tags with more than or equals to `count_threshold` followers. The result `.tsv` file will be in `tsv` directory. The `.tsv` file name can be changed by the `file_name` argument. `XXXXXXXXXX` is your Qiita API token.

```
$ python get_tags.py XXXXXXXXXX --page_num=100 --count_threshold=30 --file_name=tags
```

|Argument Name|Description|Default Value|
|:---|:---|:---|
|token|Qiita API token.|-|
|page_num|(Optional) Qiita API pagenation value.|10|
|count_threshold|(Optional) The minimum value of followers bound to each tag to be collected.|30|
|file_name|(Optional) The file name of tag list to be in `tag` directory.|tags|

---

## Get articles

You can download Qiita article with the specified single tag. If you want to know the popular tag in Qiita, check the `tags/tags.tsv` directory in this project. To avoid duplication of downloading the same article, `output` argument will be used (this file will be created when you execute `get_items.py` for the first time). 

|Argument Name|Description|Default Value|
|:---|:---|:---|
|token|Qiita API token.|-|
|tag|The tag attached to the articles. You can only one tag to select.|-|
|page_num|(Optional) Qiita API pagenation value.|10|
|per_page|(Optional) The number of articles in each page.|1|
|output|(Optional) The path of output file to avoid duplication of downloading articles. |./output/output.tsv|

For example, if you execute the script with the following arguments, 

```
$ python get_items.py XXXXXXXXXX Python --page_num=10 --per_page=5 --output=./output/output.tsv
```

the maximum number of articles with tag `Python` are `10x5=50`. `XXXXXXXXXX` is your Qiita API token.

---
