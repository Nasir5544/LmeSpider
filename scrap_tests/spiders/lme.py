import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from scrapy_selenium import SeleniumRequest

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
    start_urls = [
        "https://google.com",
        "https://www.lme.com/en/news",
        #"https://www.lme.com/en/news?page=2"
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
            yield SeleniumRequest(url=url, callback=self.parse, meta={"driver": driver})

    def parse(self, response):
        driver = response.meta["driver"]

        # Wait for the elements to be present
        WebDriverWait(driver, 100).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.search-listing__item')))

        # Extract data from fields using CSS selectors into individual variables
        elements = driver.find_elements(By.CSS_SELECTOR, 'li.search-listing__item')

        for element in elements:
            title = element.find_element(By.CSS_SELECTOR, '.search-listing-card__link').text
            tag = element.find_element(By.CSS_SELECTOR, '.search-listing-card__meta.meta li:nth-child(1)').text
            date = element.find_element(By.CSS_SELECTOR, '.search-listing-card__meta.meta li:nth-child(2)').text
            article = element.find_element(By.CSS_SELECTOR, '.search-listing-card__meta.meta li:nth-child(3)').text
            description = element.find_element(By.CSS_SELECTOR, '.search-listing-card__description').text
            note = element.find_element(By.CSS_SELECTOR, '.search-listing-card__note').text
            tags = element.find_element(By.CSS_SELECTOR, '.tag-list__item').text
            file_element = element.find_element(By.CSS_SELECTOR, '.search-listing-card__cta a.button-secondary')

            print('Adding News: ' + title)
            print(title)
            print(tag)
            print(article)
            print(description)
            print(note)
            print(tags)
            print(file_element)
            # download file
            # download_url = file_element.get_attribute('href')
            # driver.get(download_url)

        # Click on the next button if available
            #next_page = response.xpath('//a[contains(@class, "pagination__link--next")]/@href').get()
            #next_page = response.xpath('//svg[contains(@class, "pagination__icon--next")]/ancestor::a/@href').getall()

            #if next_page is not None:
             #next_page_url = response.urljoin(next_page)
             #yield scrapy.Request(next_page_url, callback=self.parse, meta={"driver": driver})
             #print(next_page)
             
        

        # Close the Selenium WebDriver
        driver.quit()
