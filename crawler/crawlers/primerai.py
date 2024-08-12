import asyncio
from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext

async def main() -> None:

    crawler = PlaywrightCrawler(
        max_requests_per_crawl=10,  # Adjust as needed
    )

    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        page = context.page
        url = context.request.url
        context.log.info(f'Processing {url} ...')

        # Wait for the job listings to load
        await page.wait_for_selector('tr.job-post', state='visible')

        # Extract all job links
        job_links = await page.evaluate('''
            () => {
                const links = Array.from(document.querySelectorAll('tr.job-post td.cell a'));
                return links.map(link => ({
                    url: link.href,
                    title: link.querySelector('p.body:not(.body__secondary)').textContent.trim(),
                    location: link.querySelector('p.body__secondary').textContent.trim()
                }));
            }
        ''')

        # Save the extracted links
        for job in job_links:
            await context.push_data(job)
            context.log.info(f"Saved job: {job['title']} - {job['location']}")

    # Start with the initial URL
    initial_url = 'https://job-boards.greenhouse.io/primerai'
    await crawler.run([initial_url])

if __name__ == '__main__':
    asyncio.run(main())