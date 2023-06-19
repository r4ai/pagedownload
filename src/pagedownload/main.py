import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# menu.htmlが存在するURLを指定します。
base_url = 'http://example.com/menu.html'

def download(url, pathname):
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get("Content-Length", 0))

    # ファイルのダウンロード
    with open(pathname, 'wb') as f:
        for data in response.iter_content(1024):
            f.write(data)

def get_all_images(url):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    urls = []
    for img in soup.find_all("img"):
        img_url = img.attrs.get("src")
        if not img_url:
            continue
        img_url = urljoin(url, img_url)
        urls.append(img_url)
    return urls

def main(url):
    # ページのHTMLを取得し、解析します。
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    links = soup.find_all("a")
    href_list: list[str] = list(map(
        lambda x: urljoin(base_url, x.get('href')), links))
    href_list.append(url) # `menu.html`もダウンロード対象に含める

    for href in href_list:
        # 画像を取得してダウンロード
        try:
            images = get_all_images(href)
            for image in images:
                download(image, os.path.join('page', os.path.basename(image)))

            # hrefページをダウンロード
            download(href, os.path.join('page', os.path.basename(href)))
        except requests.exceptions.RequestException as e:
            print(f"Error accessing {href}: {str(e)}")

main(base_url)
