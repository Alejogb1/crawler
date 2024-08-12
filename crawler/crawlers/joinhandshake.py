from urllib.parse import urlparse
from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext
from crawlee.storages import KeyValueStore
import asyncio

async def main() -> None:
    crawler = PlaywrightCrawler(
        max_requests_per_crawl=50,
    )
    kvs = await KeyValueStore.open()

    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        context.log.info(f'Processing {context.request.url}')

        await handle_cookie_banner(context)
        screenshot = await context.page.screenshot()
        await kvs.set_value(
            key=f'screenshot-ats',
            value=screenshot,
            content_type='image/png',
        )

        try:
            screenshot = await context.page.screenshot()
            await kvs.set_value(
                key=f'screenshot-ats',
                value=screenshot,
                content_type='image/png',
            )
            await context.page.wait_for_selector('table', timeout=15000)
        except Exception as e:
            context.log.error(f"Timeout waiting for table on {context.request.url}: {str(e)}")
            screenshot = await context.page.screenshot()
            await kvs.set_value(
                key=f'screenshot-ats',
                value=screenshot,
                content_type='image/png',
            )
            return
        
        def filter_urls(url):
            parsed_url = urlparse(url)
            return parsed_url.netloc == 'joinhandshake.com' and parsed_url.path.startswith('/careers/open-roles/job/')

        await context.enqueue_links(
            label='ATS',
            strategy="all",
            filter=filter_urls,
        )
    async def handle_cookie_banner(context: PlaywrightCrawlingContext):
        try:
            # Wait for the cookie banner to appear
            cookie_banner = await context.page.wait_for_selector('#onetrust-banner-sdk', timeout=5000)
            if cookie_banner:
                # Look for the "Accept All Cookies" button
                accept_button = await context.page.query_selector('#onetrust-accept-btn-handler')
                if accept_button:
                    await accept_button.click()
                    context.log.info("Accepted cookies")
                else:
                    context.log.warning("Accept button not found in cookie banner")
        except Exception as e:
            context.log.info(f"No cookie banner found or error occurred: {str(e)}")

    await crawler.run(['https://joinhandshake.com/careers/open-roles/'])


if __name__ == '__main__':
    asyncio.run(main())