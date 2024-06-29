import time
import os

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

MAX_WAIT = 10
SHOP_BUTTON = 'Магазин'
CART_BUTTON = 'Корзина'

class FunctionalTest(StaticLiveServerTestCase):
    '''Функциональный тест'''

    def setUp(self):
        '''Установка'''
        self.browser = WebDriver()
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server
    
    def tearDown(self):
        '''Удаление'''
        self.browser.quit()
    
    def wait_for(self, fn):
        '''Ожидать'''
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def the_correct_location_of_the_navigation_buttons(self):
        '''Корректное расположение кнопок навигации'''
        # Проверка расположения лого
        logo = self.browser.find_element(By.ID, 'logo')
        self.assertAlmostEqual(logo.location['x'], 100, delta=15)
        self.assertAlmostEqual(logo.location['y'], 25, delta=10)

        # Проверка расположения кнопки "Магазин"
        shop = self.browser.find_element(By.LINK_TEXT, SHOP_BUTTON)
        self.assertAlmostEqual(shop.location['x'], 500, delta=15)
        self.assertAlmostEqual(shop.location['y'], 40, delta=10)

        # Проверка расположения кнопки "Корзина"
        cart = self.browser.find_element(By.LINK_TEXT, CART_BUTTON)
        self.assertAlmostEqual(
            cart.location['x'] - shop.location['x'] - shop.size['width'], 60, delta=10)
        # Кнопки навигации расположены на одном уровне
        self.assertAlmostEqual(shop.location['y'], cart.location['y'])
