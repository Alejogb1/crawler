import asyncio
from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext

async def main() -> None:
    crawler = PlaywrightCrawler(
        max_requests_per_crawl=20,
    )

    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        context.log.info(f'Processing {context.request.url} ...')
        
        # Wait for the page to load
        await context.page.wait_for_selector('._8tk7', state='visible')

        # Click to open the dropdown for selecting the number of results per page
        await context.page.click('div._6vz6 > div._6a > div.uiPopover > a')
        
        await context.page.screenshot(path='screenshot.png')

        # Wait for the dropdown options to be visible
        await context.page.wait_for_selector('li._54ni._6v-l._97fe.__MenuItem', state='visible')

        # Wait for the dropdown options to be visible
        await context.page.wait_for_selector('li._54ni._6v-l._97fe.__MenuItem', state='visible')

        # Find and click the option for 100 results per page
        await context.page.evaluate('''
            () => {
                const items = Array.from(document.querySelectorAll('li._54ni._6v-l._97fe.__MenuItem div._6v-k'));
                const item = items.find(element => element.textContent.trim() === '100');
                if (item) {
                    item.click();
                }
            }
        ''')
        # Wait for the jobs to be displayed
        await context.page.wait_for_selector('div._af0h', state='visible')

        # Extract job data using the evaluate method correctly
        job_links = await context.page.evaluate('''
            () => {
                const job_elements = Array.from(document.querySelectorAll('div._af0h'));
                return job_elements.map(job_element => ({
                    title: job_element.querySelector('div._8sel').textContent,
                    location: job_element.querySelector('div._8see').textContent,
                    link: job_element.querySelector('a').href
                }));
            }
        ''')

        # Save the extracted links
        for job in job_links:
            await context.push_data(job)
            context.log.info(f"Saved job: {job['title']} - {job['location']}")

    await crawler.run(['https://www.metacareers.com/areas-of-work/artificial-intelligence/?p[teams][0]=Artificial%20Intelligence&teams[0]=Artificial%20Intelligence&offices[0]=Huntsville%2C%20AL&offices[1]=Montgomery%2C%20AL&offices[2]=Chandler%2C%20AZ&offices[3]=Mesa%2C%20AZ&offices[4]=Burlingame%2C%20CA&offices[5]=Foster%20City%2C%20CA&offices[6]=Fremont%2C%20CA&offices[7]=Irvine%2C%20CA&offices[8]=Los%20Angeles%2C%20CA&offices[9]=Menlo%20Park%2C%20CA&offices[10]=Mountain%20View%2C%20CA&offices[11]=Newark%2C%20CA&offices[12]=Northridge%2C%20CA&offices[13]=San%20Diego%2C%20CA&offices[14]=San%20Francisco%2C%20CA&offices[15]=Santa%20Clara%2C%20CA&offices[16]=Sausalito%2C%20CA&offices[17]=Sunnyvale%2C%20CA&offices[18]=Denver%2C%20CO&offices[19]=Washington%2C%20DC&offices[20]=Miami%2C%20Florida&offices[21]=Atlanta%2C%20GA&offices[22]=Newton%20County%2C%20GA&offices[23]=Stanton%20Springs%2C%20GA&offices[24]=Kuna%2C%20ID&offices[25]=Aurora%2C%20IL&offices[26]=Chicago%2C%20IL&offices[27]=DeKalb%2C%20IL&offices[28]=Jeffersonville%2C%20IN&offices[29]=Altoona%2C%20IA&offices[30]=Polk%20County%2C%20IA&offices[31]=Boston%2C%20MA&offices[32]=Cambridge%2C%20MA&offices[33]=Detroit%2C%20MI&offices[34]=Rosemount%2C%20MN&offices[35]=Kansas%20City%2C%20MO&offices[36]=Papillion%2C%20NE&offices[37]=Sarpy%20County%2C%20NE&offices[38]=Los%20Lunas%2C%20NM&offices[39]=Valencia%2C%20NM&offices[40]=New%20York%2C%20NY&offices[41]=Durham%2C%20NC&offices[42]=Forest%20City%2C%20NC&offices[43]=New%20Albany%2C%20OH&offices[44]=Crook%20County%2C%20OR&offices[45]=Hillsboro%2C%20OR&offices[46]=Prineville%2C%20OR&offices[47]=Pittsburgh%2C%20PA&offices[48]=Gallatin%2C%20TN&offices[49]=Austin%2C%20TX&offices[50]=Fort%20Worth%2C%20TX&offices[51]=Garland%2C%20TX&offices[52]=Houston%2C%20TX&offices[53]=Temple%2C%20TX&offices[54]=Eagle%20Mountain%2C%20UT&offices[55]=Salt%20Lake%2C%20UT&offices[56]=Utah%20County%2C%20UT&offices[57]=Ashburn%2C%20VA&offices[58]=Henrico%2C%20VA&offices[59]=Loudoun%20County%2C%20VA&offices[60]=Reston%2C%20VA&offices[61]=Richmond%2C%20VA&offices[62]=Sandston%2C%20VA&offices[63]=Sterling%2C%20VA&offices[64]=Bellevue%2C%20WA&offices[65]=Redmond%2C%20WA&offices[66]=Seattle%2C%20WA&offices[67]=Vancouver%2C%20WA&offices[68]=Remote%2C%20US&offices[69]=Cheyenne%2C%20WY#openpositions'])

if __name__ == '__main__':
    asyncio.run(main())
