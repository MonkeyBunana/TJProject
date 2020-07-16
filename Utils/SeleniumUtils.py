# -*- coding: utf-8 -*-”
# 取消使用，暂时废弃
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumPage:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument("headless")
        chrome_options.add_argument('profile.managed_default_content_settings.images')
        chrome_options.add_argument('lang=zh_CN.UTF-8')
        chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
                                    '(KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"')

        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def get(self, url):
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get(url)

    def findElement(self, by, value):
        by_map = {'id': By.ID, 'name': By.NAME, 'class': By.CLASS_NAME, 'tag': By.TAG_NAME, 'link': By.LINK_TEXT,
                  'plink': By.PARTIAL_LINK_TEXT, 'css': By.CSS_SELECTOR, 'xpath': By.XPATH}
        if by in by_map.keys():
            try:
                element = WebDriverWait(self.driver, 10, ignored_exceptions=None).until(
                    EC.presence_of_element_located((by_map[by], value)))
                return element
            except NoSuchElementException:
                pass

    def findElements(self, by, value):
        by_map = {'id': By.ID, 'name': By.NAME, 'class': By.CLASS_NAME, 'tag': By.TAG_NAME, 'link': By.LINK_TEXT,
                  'plink': By.PARTIAL_LINK_TEXT, 'css': By.CSS_SELECTOR, 'xpath': By.XPATH}
        if by in by_map.keys():
            try:
                elements = WebDriverWait(self.driver, 10, ignored_exceptions=None).until(
                    EC.presence_of_all_elements_located((by_map[by], value)))
                return elements
            except NoSuchElementException:
                pass

    def quit(self):
        self.driver.close()