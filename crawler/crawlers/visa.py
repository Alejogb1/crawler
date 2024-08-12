import asyncio
from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext

async def main() -> None:
    crawler = PlaywrightCrawler(
        max_requests_per_crawl=20,
    )

    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        context.log.info(f'Processing {context.request.url} ...')
        
        await context.page.wait_for_selector('a.vs-h3.vs-link-job.vs-link-new-window', state='visible', timeout=2000)

        # Enqueue only links with the "btn" class
        await context.enqueue_links(
            selector='a.vs-h3.vs-link-job.vs-link-new-window',
            strategy='same-domain',
        )

    await crawler.run(['https://corporate.visa.com/en/jobs/?cities=Ashburn&cities=Atlanta&cities=Austin&cities=Bellevue&cities=Denver&cities=Foster%20City&cities=Highlands%20Ranch&cities=Lehi&cities=Miami&cities=New%20York&cities=San%20Francisco&cities=Washington'])

if __name__ == '__main__':
    asyncio.run(main())