# scraping
from playwright.async_api import async_playwright

# best work
import asyncio
from pprint import pprint
import time
import re

# automatization 
from multiprocessing import Process, Queue
from threading import Thread, Semaphore


class main_exercise:
    def __init__(self):
        self.current_page = []
        self.code_urls_page = []
    async def main(self):
        #print("work")
        self.code_urls_page = await self.get_items_url_catalog()

        pprint(self.code_urls_page)

    async def get_items_url_catalog(self):
        p = await async_playwright().start()

        website = await p.chromium.launch(headless = False)

        page_categories = await website.new_page()
        
        await page_categories.goto("https://ecosystem.hubspot.com/marketplace/solutions/all")
        time.sleep(3)

        
        for i in range(10):
            start_page = page_categories.url
            con_scroll_wait_items = Queue()
            await asyncio.gather(
                self.scroll_down(page_categories,con_scroll_wait_items)
                , self.wait_for_items_page(page_categories,con_scroll_wait_items)
                , self.get_data_page(page_categories)
            )
            next_page = page_categories.url
            if start_page != next_page:
                print(start_page)
            else:
                print(next_page)
                break
            
        
        pprint(self.code_urls_page)
        print(len(self.code_urls_page))
        time.sleep(5)
        
        await website.close()
        # # return urls_page()
            
    async def get_data_page(self,page_categories):
        # get_data page
        await page_categories.wait_for_selector("main > div > div > div > div > div > div > div > a > div > div > div > div > span > h2")
        page_companies = await page_categories.query_selector_all("main > div > div > div > div > div > div > div > a > div > div > div > div > span > h2")

        for page_category in page_companies:
            code_url = {
                'url': None,
            }
            url_page_company = await  (await page_category.query_selector("../../../../../..")).get_attribute("href")
            code_url["url"] = str(url_page_company).replace("/marketplace/solutions/","")
            self.code_urls_page.append(code_url)
        return None

    async def scroll_down(self,page_categories,con_scroll_wait_items):
        while True:
            try:
                con_scroll_wait_items.get(timeout=0.001)
                return None
            except:
                await page_categories.mouse.wheel(0,100)
                time.sleep(0.1)
    
    async def wait_for_items_page(self,page_categories,con_scroll_wait_items):
        await page_categories.wait_for_selector('body div div div main div div div div div div nav span button span')
        con_scroll_wait_items.put("stop") 
        # Click on button
        selector_all_pages = await page_categories.query_selector_all('body div div div main div div div div div div nav span button span')
        for pages in selector_all_pages:
            next_page = await pages.text_content()
            if str(next_page) == "Next":
                # Is it last page?
                aria_work = await (await pages.query_selector("..")).get_attribute("aria-disabled")
                if aria_work != "false":
                    return None
                else:
                    await pages.click()
                    return None
            else:
                try:
                    self.current_page = int(re.match(r"You are currently on Page (\d)",str(next_page)).group(1))
                except:
                    None

# Last
# You are currently on Page 1
# Prev everytime

async def run_class():
    class_main = main_exercise()
    await class_main.main()

if __name__ == "__main__":
    asyncio.run(run_class())