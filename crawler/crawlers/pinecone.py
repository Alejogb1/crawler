import asyncio
from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext

async def main() -> None:
    crawler = PlaywrightCrawler(
        max_requests_per_crawl=10,
    )

    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        context.log.info(f'Processing {context.request.url} ...')
        
        # Enqueue only links with the "btn" class
        await context.enqueue_links(
            selector='a.group.cursor-pointer.px-4.py-5.text-small.bg-alpha3',
            strategy='all',
        )

    await crawler.run(['https://www.pinecone.io/careers/'])

if __name__ == '__main__':
    asyncio.run(main())