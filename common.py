"""Config file for Qiita API 
"""


def get_header(token):
    """Get header to connect qiita.com
    """
    return {'Authorization': "Bearer {}".format(token)}


def get_correct_page_counts(page_num, per_page):
    """Get correct value for `page count` and `page count per page`. 
    Both values have to be between 1 to 100.
    """
    if page_num < 1:
        page_num = 1
    if page_num > 100:
        page_num = 100
    if per_page < 1:
        per_page = 1
    if per_page > 100:
        per_page = 100

    return page_num, per_page
