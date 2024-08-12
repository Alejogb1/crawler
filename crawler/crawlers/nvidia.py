 wimport asyncio
from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext

async def main() -> None:
    crawler = PlaywrightCrawler(
        max_requests_per_crawl=60,
    )

    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        page = context.page

        await page.wait_for_selector('a[data-automation-id="jobTitle"]', state='visible')

        # Enqueue all job links on the page
        await context.enqueue_links(
            selector='a[data-automation-id="jobTitle"]',
            strategy='same-domain',
        )
https://docs.google.com/spreadsheets/d/1j8VaYzHQ0BNY0_LkvHMrfHAkBTOH2QXPuuZ3QIKQ7nc/edit?usp=sharing
        # Check for a "Next" button and click it if it exists
        next_button = page.locator('button[aria-label="next"]')
        if await next_button.count() > 0 and await next_button.is_enabled():
            # Click the "Next" button
            await next_button.click()
            # Wait for the page to load
            await page.wait_for_load_state('networkidle')
            # Enqueue the URL of the next page
            await context.enqueue_request(page.url)

    # Start with the initial URL
    initial_url = 'https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite'

   

    await crawler.run([initial_url])

if __name__ == '__main__':
    asyncio.run(main())