from fastapi import FastAPI, Query
import requests
import time

app = FastAPI()

SCRAPYRT_URL = "http://localhost:9080/crawl.json"

@app.get("/search")
def search_google(
    site: str,  # Tên website (vd: "motcuocsong.vn")
    keyword: str,  # Từ khóa tìm kiếm (vd: "Trấn Thành")
    time_range: str = Query("day", enum=["hour", "day", "week", "month", "year"]),
    page: int = Query(1, ge=1)  # Page phải >= 1
):
    """
    API tìm kiếm Google bằng ScrapyRT, có đo thời gian thực hiện và số lượng link lấy được.
    - `site`: Tên trang web để tìm kiếm (ví dụ: "motcuocsong.vn")
    - `keyword`: Từ khóa cần tìm (ví dụ: "Trấn Thành")
    - `time_range`: Khoảng thời gian ('hour', 'day', 'week', 'month', 'year')
    - `page`: Số trang cần lấy (mặc định = 1)
    """

    # Tự động thêm dấu `""` vào keyword
    formatted_keyword = f'"{keyword}"'

    # Tạo truy vấn theo cú pháp `site:website "keyword"`
    query = f"site:{site} {formatted_keyword}"

    # Bắt đầu đo thời gian
    start_time = time.perf_counter()

    payload = {
        "start_requests": True,
        "spider_name": "google",
        "crawl_args": {
            "query": query,
            "time_range": time_range,
            "page": page
        },
    }

    response = requests.post(SCRAPYRT_URL, json=payload)

    # Kết thúc đo thời gian
    end_time = time.perf_counter()
    elapsed_time = round(end_time - start_time, 4)  # Tính thời gian chạy

    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])  # Danh sách link lấy được
        items_count = len(items)  # Số lượng bài viết lấy được

        return {
            "status": "success",
            "site": site,
            "keyword": keyword,
            "formatted_keyword": formatted_keyword,  # Hiển thị keyword đã được thêm dấu `""`
            "query": query,  # Hiển thị truy vấn đã tạo
            "time_range": time_range,
            "page": page,
            "elapsed_time_seconds": elapsed_time,  # Thời gian cào dữ liệu
            "items_count": items_count,  # Số link lấy được
            "data": items  # Danh sách bài viết
            
        }
    else:
        return {
            "status": "error",
            "error_code": response.status_code,
            "message": response.text,
            "elapsed_time_seconds": elapsed_time  # Trả về thời gian dù lỗi
        }
