import concurrent.futures
import blog_craw

# crawl
with concurrent.futures.ThreadPoolExecutor() as pool:
    htmls = pool.map(blog_craw.craw, blog_craw.urls)
    htmls = list(zip(blog_craw.urls, htmls))
    for url, html in htmls:
        print(url, len(html))

print("crawl over")


# parse
with concurrent.futures.ThreadPoolExecutor() as pool:
    futures = {}
    for url, html in htmls:
        future = pool.submit(blog_craw.parse, html)
        futures[future] = url

    for future, url in futures.items():
        print(url, future.result())
