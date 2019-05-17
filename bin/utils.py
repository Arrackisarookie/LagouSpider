import requests


def get_proxy():
    url = 'http://localhost:5000/random'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


def get_page(url):
    headers = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/71.0.3578.98 Safari/537.36",
        "Referer": url
    }
    proxy = get_proxy()
    proxies = {'http': proxy}
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.status_code == 200:
        return response.text
    print(response.status_code)
    return None
