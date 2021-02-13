"""Config file for Qiita API 
"""

# Qiita API token
token = "XXXXXX"


def get_header():
    """Get header to connect qiita.com
    """
    return {'Authorization': "Bearer {}".format(token)}
