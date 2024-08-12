import asyncio
from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext

async def main():
    crawler = PlaywrightCrawler(
        max_requests_per_crawl=1,  # We're only crawling one page, but loading all jobs

    )

    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext):
        page = context.page
        url = context.request.url
        context.log.info(f'Processing {url} ...')

        # Screenshot 1: Initial page load
        await page.screenshot(path='screenshot_initial_load.png', full_page=True)

        # Wait for the initial job listings to load
        await page.wait_for_selector('div[role="link"][class*="position-card"]', state='visible', timeout=60000)

        # Screenshot 2: After initial job cards have loaded
        await page.screenshot(path='screenshot_initial_jobs_loaded.png', full_page=True)

        # Function to load more jobs
        async def load_more_jobs():
            load_more_count = 0
            while True:
                try:
                    load_more_button = await page.query_selector('button.btn.btn-sm.btn-secondary.show-more-positions')
                    if load_more_button:
                        await load_more_button.click()
                        await page.wait_for_timeout(2000)  # Wait for new jobs to load
                        load_more_count += 1
                        if load_more_count % 5 == 0:  # Take a screenshot every 5 "Load More" clicks
                            await page.screenshot(path=f'screenshot_load_more_{load_more_count}.png', full_page=True)
                    else:
                        break  # No more "Load More" button, we've loaded all jobs
                except:
                    break  # If any error occurs, we've probably reached the end

        # Load all jobs
        await load_more_jobs()

        # Screenshot 3: After all jobs have been loaded
        await page.screenshot(path='screenshot_all_jobs_loaded.png', full_page=True)

        # Extract all job links
        job_links = await page.evaluate('''
            () => {
                const cards = Array.from(document.querySelectorAll('div[role="link"][class*="position-card"]'));
                return cards.map(card => ({
                    title: card.querySelector('.position-title')?.textContent.trim(),
                    location: card.querySelector('.position-location')?.textContent.trim(),
                    department: card.querySelector('.position-priority-container')?.textContent.trim(),
                    url: window.location.origin + card.getAttribute('data-job-id')
                }));
            }
        ''')

        # Save the extracted links
        for index, job in enumerate(job_links):
            print("OUR JOB IS: ", job)
            if job['url']:
                await context.push_data(job)
                context.log.info(f"Saved job: {job['title']} - {job['location']} - {job['department']}")
                
                # Screenshot 4: Individual job cards (limit to first 5 for example)
                if index < 5:
                    await page.evaluate(f"document.querySelector('div[role=\"link\"][class*=\"position-card\"]:nth-child({index + 1})').scrollIntoView()")
                    await page.screenshot(path=f'screenshot_job_card_{index}.png')

    # Start with the initial URL
    initial_url = 'https://careers.appliedmaterials.com/careers?location=united%20states&domain=appliedmaterials.com&sort_by=relevance&triggerGoButton=true'
    await crawler.run([initial_url])

if __name__ == '__main__':
    asyncio.run(main())