import asyncio
from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext
from typing import List

class Website:
    def __init__(self, name: str, url: str, title_selector: str, body_selector: str):
        self.name = name
        self.url = url
        self.title_selector = title_selector
        self.body_selector = body_selector

async def main() -> None:
    siteData = [
        ['O\'Reilly', 'https://www.oreilly.com', 'h1', 'div.title-description'],
        ['Reuters', 'https://www.reuters.com', 'h1', 'div.ArticleBodyWrapper'],
        ['Brookings', 'https://www.brookings.edu', 'h1', 'div.post-body'],
        ['CNN', 'https://www.cnn.com', 'h1', 'div.article__content'],
    ]
    
    websites: List[Website] = [
        Website(name, url, title, body) for name, url, title, body in siteData
    ]

    async def handle_website(website: Website, page_url: str) -> None:
        crawler = PlaywrightCrawler(
            max_requests_per_crawl=60,
        )

        @crawler.router.default_handler
        async def request_handler(context: PlaywrightCrawlingContext) -> None:
            page = context.page
            await page.goto(context.request.url)

            # Wait for title and body selectors to be visible
            await page.wait_for_selector(website.title_selector, state='visible')
            await page.wait_for_selector(website.body_selector, state='visible')

            # Extract title and body
            title = await page.inner_text(website.title_selector)
            body = await page.inner_html(website.body_selector)

            print(f"Title: {title}")
            print(f"Body: {body[:500]}...")  # Print the first 500 characters of the body

        # Start the crawl with the initial page URL
        await crawler.run([page_url])

    # Example usage with the given website data
    await handle_website(websites[0], '/library/view/web-scraping-with/9781491910283')
    await handle_website(websites[1], '/article/us-usa-epa-pruitt-idUSKBN19W2D0')
    await handle_website(websites[2], '/blog/techtank/2016/03/01/idea-to-retire-old-methods-of-policy-education/')
    await handle_website(websites[3], '/2023/04/03/investing/dogecoin-elon-musk-twitter/index.html')

if __name__ == '__main__':
    asyncio.run(main())