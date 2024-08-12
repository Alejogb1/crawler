import asyncio
from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext

async def main() -> None:
    crawler = PlaywrightCrawler(
        max_requests_per_crawl=20,
    )

    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        context.log.info(f'Processing {context.request.url} ...')
        
        # Enqueue only links with the "btn" class
        await context.enqueue_links(
            selector='a.heading.show',
            strategy='same-domain',
        )

    await crawler.run(['https://uplabs.freshteam.com/jobs'])

if __name__ == '__main__':
    asyncio.run(main())