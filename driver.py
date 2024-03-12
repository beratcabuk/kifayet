from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


WEBSITE_URL = 'https://shopping.google.com/'
ACCEPT_COOKIES_CSS_SELECTOR = '.VtwTSb > form:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(1)'
FIRST_SEARCH_BAR_XPATH = '//*[@id="REsRA"]'
SECOND_SEARCH_BAR_XPATH = '//*[@id="APjFqb"]'
FIRST_HIT_CSS_SELECTOR = 'div.mnIHsc:nth-child(2) > a:nth-child(1)'


class GoogleShopping:
    def __init__(self) -> None:
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=self.options)
        self.driver.get(WEBSITE_URL)
        sleep(2)
        # Accept cookies to make the cookiewall go away.
        cookie_acc_btn = self.driver.find_element(By.CSS_SELECTOR,
                                                  ACCEPT_COOKIES_CSS_SELECTOR)
        cookie_acc_btn.click()
        sleep(1)
    
    def keywords_to_links(self, keywords: list[str]) -> list[str]:
        """
        Takes a list of keywords and returns a list of links of fitting
        products.
        """
        links = []

        # The search bar has a different path for the first time.
        search_bar = self.driver.find_element(By.XPATH, FIRST_SEARCH_BAR_XPATH)
        search_bar.click()
        search_bar.send_keys(keywords[0])
        search_bar.send_keys(Keys.ENTER)
        sleep(5)
        first_hit = self.driver.find_element(By.CSS_SELECTOR,
                                             FIRST_HIT_CSS_SELECTOR)
        links.append(first_hit.get_attribute('href'))

        for kw in keywords[1:]:
            # Search bar changes once you run the initial search.
            search_bar = self.driver.find_element(By.XPATH,
                                                  SECOND_SEARCH_BAR_XPATH)
            search_bar.click()
            search_bar.clear()
            search_bar.send_keys(kw)
            search_bar.send_keys(Keys.ENTER)
            sleep(5)
            first_elem = self.driver.find_element(By.CSS_SELECTOR,
                                                  FIRST_HIT_CSS_SELECTOR)
            links.append(first_elem.get_attribute('href'))
        
        return links


    def __del__(self) -> None:
        sleep(0.5)
        self.driver.quit()

if __name__ == '__main__':
    keywords = ['Denim trucker jacket blue', 'White crew neck t-shirt',
                'Khaki jogger pants', 'Retro sneakers gray black.']
    gs = GoogleShopping()
    assert WEBSITE_URL in gs.driver.current_url
    links = gs.keywords_to_links(keywords)
    assert len(links) != 0
