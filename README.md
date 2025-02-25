# Scrapyrt crawl JS website with splash

# Usage
```bash
docker compose up --build
```

Request
```url
http://localhost:9080/crawl.json?start_requests=true&spider_name=reviews
```

Search Google
```url
http://localhost:9080/crawl.json?start_requests=true&spider_name=google&crawl_args={"query":"scrapy splash", "page":3}
```

```url
https://9080-taiduongrep-scrapysplas-d1qvo8prqgj.ws-us117.gitpod.io/crawl.json?start_requests=true&spider_name=google&crawl_args={"query":"scrapy splash", "page":3}
```