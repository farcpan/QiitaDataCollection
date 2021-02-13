# QiitaDataCollection

Data collection project via Qiita API. Here are some scripts to get information of Qiita:

* Get tags with more than or equals to 30 followers.
* Get items with the tags you collect.

---

## Preparation

You have to get Qiita API token on your Qiita page and add it in `common.py`. 

```
# Qiita API token
- token = "XXXXX"
+ token = "<Your Qiita API token>"
```

---

## Get the number of articles on Qiita

```
$ python check_article_num.py 
Total Count of articles: 640054
```

## Get Tags

You can get tags with more than or equals to `count_threshold` followers. The result `.tsv` file will be in `tsv` directory. The `.tsv` file name can be changed by the `file_name` argument. 

```
$ python get_tags --page_num=100 --count_threshold=30 --file_name=tags
```

|Argument Name|Description|Default Value|
|:---|:---|:---|
|page_num|Qiita API pagenation value.|10|
|count_threshold|The minimum value of followers bound to each tag to be collected.|30|
|file_name|The file name of tag list to be in `tag` directory.|tags|

---

## Get articles

T.B.D.

---
