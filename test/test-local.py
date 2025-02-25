# script.py
import requests

# URL của ScrapyRT
scrapyrt_url = "http://localhost:9080/crawl.json"

# Dữ liệu để gửi request (nếu cần)
payload = {
    'start_requests': 'true',
    'spider_name': 'google',
    "crawl_args": {'query': 'site:www.24h.com.vn "mono"', 'page': 3}
}

# Gửi request đến ScrapyRT
response = requests.post(scrapyrt_url, json=payload)

# In kết quả
if response.status_code == 200:
    result = response.json()
    items = result.get('items', [])
    links = [item.get('link') for item in items]
    print(links)
else:
    print(f"Error: {response.status_code}")
    print(response.text)