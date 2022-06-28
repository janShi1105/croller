import time
import json
import requests

PAGE_URL_LIST = [
    'https://example.com/1.page',
    'https://example.com/2.page',
    'https://example.com/3.page',
]

def fetch_pages():
    """ページ内容を取得する"""
    with open('crawler_info.log', 'a') as f_info_log, \
         open('crawler_error.log', 'a') as f_error_log:

        page_contents = {}

        msg = "クロールを開始します\n"
        print(msg)
        f_info_log.write(msg)



        for page_url in PAGE_URL_LIST:
            r = requests.get(page_url, timeout=30)
            try:
                r.raise_for_status()
            except requests.exceptions.RequestException as e:
                msg = "[ERROR] {exception}\n.format(exception=e)"
                print(msg)
                f_error_log.write(msg)
                continue
            
            page_contents[page_url] = r.text
            time.sleep(1)

        return page_contents

if __name__ == '__main__':
    page_contents = fetch_pages()
    with open('page_contents.json', 'w') as f_page_contents:
        json.dump(page_contents, f_page_contents, ensure_ascii=False)
    