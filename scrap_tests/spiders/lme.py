import time
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

class LmeSpider(scrapy.Spider):
    
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36",
        "ROBOTSTXT_OBEY": False,
        "CONCURRENT_REQUESTS": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 16,
        "CONCURRENT_REQUESTS_PER_IP": 16,
        "DOWNLOAD_DELAY": 3,
    }
    name = "lme_spider"
    #page_number=2
    
    start_urls = [
        "https://google.com",
        "https://www.lme.com/News",
       # "https://www.lme.com/News?page=1",
       # "https://www.lme.com/en/news?page=3"
    ]

    download_directory = "C:/Users/muham/Downloads/scrapdata"

    def start_requests(self):
        # Set up Selenium WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--enable-logging")  # Enable logging

        # Disable page load metrics update dispatcher
        options.add_argument("--disable-features=PageLoadMetrics")

        # Configure Chrome options for downloads
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f"--download.default_directory={self.download_directory}")
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": self.download_directory,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "plugins.always_open_pdf_externally": True,
        })

        # Initialize the Chrome browser with the configured options
        driver = webdriver.Chrome(options=chrome_options)

        for url in self.start_urls:
            driver.get(url)
            yield scrapy.Request(url, self.parse, meta={"driver": driver})

    def parse(self, response):
        
        driver = response.meta["driver"]
        
        # Wait for the elements to be present
        WebDriverWait(driver, 200).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.search-listing__item')))

        # Extract data from fields using CSS selectors into individual variables
        elements = driver.find_elements(By.CSS_SELECTOR, 'li.search-listing__item')

        for element in elements:
            #button_text = element.find_element(By.CSS_SELECTOR, '.search-listing-card__cta a.button-primary-alt').text.strip()
           # if button_text == "Find out more":
               # continue
            title = element.find_element(By.CSS_SELECTOR, '.search-listing-card__link').text
            tag = element.find_element(By.CSS_SELECTOR, '.search-listing-card__meta.meta li:nth-child(1)').text
            date = element.find_element(By.CSS_SELECTOR, '.search-listing-card__meta.meta li:nth-child(2)').text
            article = element.find_element(By.CSS_SELECTOR, '.search-listing-card__meta').text
            description = element.find_element(By.CSS_SELECTOR, '.search-listing-card__description').text
           # note = element.find_element(By.CSS_SELECTOR, '.search-listing-card__note').text
            #tags = element.find_element(By.CSS_SELECTOR, '.tag-list__item').text
            #file_element = element.find_element(By.CSS_SELECTOR, '.search-listing-card__cta a.button-secondary')

            print('Adding News: ' + title)
            print(title)
            print(tag)
            print(article)
            print(description)
            print(date)
            
            
            
            
            
        # try:
        #     # Assuming you have extracted data from the current page here
        #     # Now, check if there's a next page available
        #     if LmeSpider.page_number < 11:  # Or however many pages you want to scrape
        #         # Increment page number for the next request
        #         LmeSpider.page_number += 1
        #         next_page = f"https://www.lme.com/News?page={LmeSpider.page_number}"
        #         yield response.follow(next_page, callback=self.parse)
        #         time.sleep(3)  # Adjust the delay as needed
                
        #         # Additional processing example
        #         # For demonstration purposes, printing the title and next_page
        #         title = response.css('.search-listing-card__link::text').extract_first()
        #         print(title)
        #         print(next_page)
        # except Exception as e:
        #     print(f"Error occurred: {str(e)}")
             
             
            #print(note)
           # print(tags)
          #  print(file_element)
            # download file
          #  download_url = file_element.get_attribute('href')
           # driver.get(download_url)
            
        # Extract next page URL
          # Click on the next button if available
          
            # next_page_link = response.xpath('//a[contains(@class, "pagination__link") and contains(@class, "pagination__link--next")]//i[contains(@class, "pagination__icon") and contains(@class, "pagination__icon--next")]/parent::a/@href').get()

            # print("Next Page Link:", next_page_link)  # Debugging statement

            # if next_page_link:
            #  next_page_url = response.urljoin(next_page_link)
            #  print("Next Page URL:", next_page_url)  # Debugging statement
            #  yield scrapy.Request(next_page_url, callback=self.parse, meta={"driver": driver})
            # else:
            #  print("Next page link not found!")  # Debugging statement
            
            
            
            
            ###############################atleast print a next page links here is code 

        try:
            # Wait for the next page link to be present
             next_page_links = WebDriverWait(driver, 20).until(
             EC.presence_of_all_elements_located((By.XPATH, '//a[@class="pagination__link pagination__link--next"]'))
            # //a[@class='pagination__link pagination__link--next']
            #'//a[contains(@class, "pagination__link") and contains(@class, "pagination__link--next")]'


             )
             #//nav[contains(@class, 'search-listing__pagination')]/ol[@class='pagination']/li[@class='pagination__item']/a[@class='pagination__link pagination__link--next']


             next_page_hrefs = [link.get_attribute("href") for link in next_page_links]
    
             print("Next Page Links:", next_page_hrefs)  # Debugging statement
    
             if next_page_hrefs:
               for next_page_href in next_page_hrefs:
                next_page_url = response.urljoin(next_page_href)
                print("Next Page URL:", next_page_url)  # Debugging statement
                driver.get(next_page_url)
                yield scrapy.Request(next_page_url, callback=self.parse, meta={"driver": driver})
                
                
                
               
                WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.search-listing__item'))
                 )
                
                elements = driver.find_elements(By.CSS_SELECTOR, 'li.search-listing__item')
                #ActionChains(driver).move_to_element(driver.find_element_by_css_selector('li.search-listing__item')).perform()
                time.sleep(3)
              

                for element in elements:
                    
                 title = element.find_element(By.CSS_SELECTOR, '.search-listing-card__link').text
                 tag = element.find_element(By.CSS_SELECTOR, '.search-listing-card__meta.meta li:nth-child(1)').text
                 date = element.find_element(By.CSS_SELECTOR, '.search-listing-card__meta.meta li:nth-child(2)').text
                 article = element.find_element(By.CSS_SELECTOR, '.search-listing-card__meta').text
                 description = element.find_element(By.CSS_SELECTOR, '.search-listing-card__description').text
                 # note = element.find_element(By.CSS_SELECTOR, '.search-listing-card__note').text
                # tags = element.find_element(By.CSS_SELECTOR, '.tag-list__item').text
                # file_element = element.find_element(By.CSS_SELECTOR, '.search-listing-card__cta a.button-secondary')

                 print('Adding News: ' + title)
                 print(title)
                 print(tag)
                # print(article)
                 print(description)
                 print(date)
                 # print(note)
                # print(tags)
                # print(file_element)
                
              
             else:
                print("Next page links not found!")  # Debugging statement

        except:
              print("Next page links not found!")  # Debugging statement
              return  # or handle the absence of next page links in a way that fits your needs
              
        
       
         # Close the Selenium WebDriver
        driver.quit()
