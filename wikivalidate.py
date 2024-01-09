import requests

"""
Simple validation for Wiki links. 
If a page exists on English Wikipedia return 
True, else return false
"""



def validate(keyword):
    keyword = keyword.replace('"', '')
    url = f"https://en.wikipedia.org/wiki/{keyword}"
    r = requests.get(url)
    if 200 == r.status_code:
        return True
    return False



if __name__ == "__main__":
    keyword = "RMS_Titanic"
    res = validate(keyword)
    print(res, keyword)