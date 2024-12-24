import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from scrapy.selector import Selector
from random import randint
import time

from links.vnexpress import category_links
from crawl_news.settings import USER_AGENT


class VnExpressSpider(scrapy.Spider):
    name = 'vnexpress'
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net']

    def start_requests(self):
        # Bắt đầu từ các category_links
        for category_link in category_links:
            yield scrapy.Request(url=category_link, callback=self.parse_category)

    def parse_category(self, response):
        # Lấy tất cả article links từ trang category
        article_links = response.xpath('//h2/a/@href | //h3/a/@href').getall()

        # Theo dõi từng article link
        for article_link in article_links:
            if article_link:
                yield response.follow(article_link, self.parse_comment)

    def parse_comment(self, response):
        edge_service = Service(EdgeChromiumDriverManager().install())
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f'user-agent={USER_AGENT[randint(0, len(USER_AGENT) - 1)]}')
        options.add_argument("--disable-gpu")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")

        driver = webdriver.Edge(service=edge_service, options=options)
        try:
            driver.get(response.url)

            # Wait for comments to load
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "content-comment")))

            # Expand comments and get status
            has_comments, expanded_html = self.expand_all_comments_and_replies(driver)

            if has_comments:
                # Convert HTML to Scrapy selector
                sel = Selector(text=expanded_html)

                # Parse all comments (including replies)
                all_comments = []
                for comment in sel.css('.content-comment'):
                    try:
                        content = comment.css('.full_content::text').get()
                        # Lấy phần text sau nickname
                        if not content:
                            content = comment.xpath('.//p[@class="full_content"]/text()').get()

                        comment_data = {
                            'comment_id': comment.css('.link_reply::attr(rel)').get(),
                            'content': content
                        }
                        all_comments.append(comment_data)
                    except Exception as e:
                        self.logger.error(f"Error parsing comment: {str(e)}")
                        continue

                # Yield kết quả
                yield {
                    'comments': all_comments
                }


        except Exception as e:
            self.logger.error(f"Error processing {response.url}: {str(e)}")

        finally:
            driver.close()


    def expand_all_comments_and_replies(self, driver):
        # Check for the specific HTML snippet first
        try:
            # Look for the exact HTML snippet with comment count
            driver.find_element(
                By.XPATH,
                "//div[@class='left'][.//h3[@rel='time' and contains(text(),'Ý kiến')] and .//label[@id='total_comment']]"
            )
            has_comments = True
        except:
            try:
                # Look for the section without comment count
                comment_section = driver.find_element(
                    By.XPATH,
                    "//div[@class='left'][.//h3[@rel='time' and contains(text(),'Ý kiến')]]"
                )
                has_comments = False
            except:
                # Neither snippet found
                return False, None

        # Check for the existence of total_comment label
        try:
            driver.find_element(By.CSS_SELECTOR, "div.left > h3[rel='time'] + label#total_comment")
        except:
            return has_comments, None

        # Expand all replies
        while True:
            found_reply_link = False
            reply_buttons = driver.find_elements(By.CLASS_NAME, "view_all_reply")

            if not reply_buttons:
                break

            for button in reply_buttons:
                try:
                    if button.is_displayed() and button.is_enabled():
                        driver.execute_script("arguments[0].click();", button)
                        found_reply_link = True
                        time.sleep(0.5)
                except:
                    continue

            if not found_reply_link:
                break

        # Return the comment section status and expanded HTML
        return has_comments, driver.page_source

