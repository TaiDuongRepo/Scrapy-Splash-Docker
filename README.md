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
http://localhost:9080/crawl.json?start_requests=true&spider_name=google&crawl_args={"query":"site:www.24h.com.vn \"mono\""}
```
