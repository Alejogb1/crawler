import asyncio
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler, BeautifulSoupCrawlingContext
from urllib.parse import urlparse

async def main() -> None:
    # Let's limit our crawls to make our tests shorter and safer.
    crawler = BeautifulSoupCrawler(max_requests_per_crawl=10)

    @crawler.router.default_handler
    async def request_handler(context: BeautifulSoupCrawlingContext) -> None:
        url = context.request.url
        title = context.soup.title.string if context.soup.title else ''
        context.log.info(f'The title of {url} is: {title}.')

        # The enqueue_links function is available as one of the fields of the context.
        # It is also context aware, so it does not require any parameters.

        def filter_urls(url):
            parsed_url = urlparse(url)
            return parsed_url.netloc == 'careers.icf.com' and parsed_url.path.startswith('/us/en/job/')
        
        await context.enqueue_links(strategy="all")
            
    await crawler.run(['https://careers.icf.com/us/en/search-results?keywords=artificial%20intelligence'])

if __name__ == '__main__':
    asyncio.run(main())