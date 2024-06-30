from selenium.webdriver.common.by import By

from .base import FunctionalTest, SHOP_BUTTON, CART_BUTTON

class LayoutAndStylingTest(FunctionalTest):
    '''Тест макета и стилевого оформления'''
    def test_layout_and_styling_main_page(self):
        '''Тест: макет и стилевое оформление главной страницы'''
        # Билл открывает главную страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1480, 800)

        # Билл видит аккуратное меню навигация в левом верхнем углу
        self.the_correct_location_of_the_navigation_buttons()

        # Он замечает, что на страницу отображается картинка
        main_img = self.browser.find_element(By.CSS_SELECTOR, '.main_img')
        self.assertAlmostEqual(main_img.location['x'], 150, delta=15)
        self.assertAlmostEqual(main_img.location['y'], 150, delta=10)
        # Тут же отображается текст в одну линию с картинкой
        main_text = self.browser.find_element(By.CSS_SELECTOR, '.main_text')
        self.assertAlmostEqual(main_text.location['x'], 740, delta=15)
        self.assertAlmostEqual(
            main_text.location['y'] + main_text.size['height'] / 2, 
            main_img.location['y'] + main_img.size['height'] / 2, 
            delta=2
        )

        

    def test_layout_and_styling_shop_page(self):
        '''Тест: макет и стилевое оформление страницы магазин'''
        # Билл открывает главную страницу и переходит в раздел "Магазин"
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1480, 800)

        self.browser.find_element(By.LINK_TEXT, SHOP_BUTTON).click()

        # Здесь билл так же видит лого и кнопки меню рядом с ним
        self.the_correct_location_of_the_navigation_buttons()

        # Билл видит карточки товаров
        products = self.browser.find_elements(By.CLASS_NAME, 'product_card')
        self.assertTrue(products.count() > 0)
        
        # Карточки расположены по центру
        first_product = products[0]
        second_product = products[1]
        self.assertAlmostEqual(first_product.location['x'] + first_product.size['width'],
                               740, delta=20)
        self.assertAlmostEqual(second_product.location['x'],
                               740, delta=20)
        # Первая и вторая карточка расположены рядом друг с другом:
        # вторая карточка справа от первой карточки 
        # и они располагаются на одном уровне
        self.assertAlmostEqual(
            second_product.location['x'], 
            first_product.location['x'] + first_product.size['width'] + 40, 
            delta=20
        )
        self.assertEqual(first_product.location['y'], second_product.location['y'])
        
        third_product = products[2]
        # Третья карточка расоложена слева под первой карточкой
        self.assertEqual(first_product.location['x'], third_product.location['x'])
        self.assertAlmostEqual(
            third_product.location['y'], 
            first_product.location['y'] + first_product.size['height'] + 40, 
            delta=20
        )

        # Билл смотрит на первую карточку и видит, что в ней есть картинка
        first_product_img = first_product.find_element(By.CSS_SELECTOR, 'product_img')
        self.assertAlmostEqual(
            first_product_img.location['x'],
            first_product.location['x'] + 10,
            delta=5
        )
        # Под картинкой расположено название товара
        first_product_name = first_product.find_element(By.CSS_SELECTOR, 'product_name')
        self.assertAlmostEqual(
            first_product_name.location['x'],
            first_product_img.location['y'] + first_product_img.size['height'] + 20,
            delta=10
        )
        # Еще чуть ниже он видит оценку этого товара
        first_product_evaluation = first_product.find_element(By.CSS_SELECTOR, 'product_evaluation')
        self.assertAlmostEqual(
            first_product_evaluation.location['x'],
            first_product_name.location['y'] + first_product_name.size['height'] + 15,
            delta=5
        )
        # Справа расположена стоимость товара
        first_product_price = first_product.find_element(By.CLASS_NAME, 'product_price')
        self.assertAlmostEqual(
            first_product_price.location['x'] + first_product_price.size['width'],
            first_product_img.location['x'] + first_product_img.size['width'] - 10,
            delta=5
        )
        # Под ценой находится кнопка "Добавить"
        first_product_add_button = first_product.find_element(By.CLASS_NAME, 'price_add_button')
        self.assertAlmostEqual(
            first_product_add_button.location['x'] + first_product.size['width'],
            first_product.location['x'] + first_product.size['width'] - 20,
            delta=10
        )
        
    def test_layout_and_styling_cart_page(self):
        '''Тест: макет и стилевое оформление страницы корзины'''
        # Билл открывает главную страницу и переходит в раздел "Корзина"
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1480, 800)

        self.browser.find_element(By.LINK_TEXT, CART_BUTTON).click()

        # Здесь Билл так же видит лого и кнопки меню рядом с ним
        self.the_correct_location_of_the_navigation_buttons(self)

        # Он видит список добавленных товаров в его корзину
        self.assertTrue(self.browser.find_elements(By.CLASS_NAME, 'product_in_cart').count() > 0)
        # Его покупки размещены в середине экрана
        products = self.browser.find_elements(By.CSS_SELECTOR, 'product_in_cart')
        self.assertAlmostEqual(products[0].size['width'] / 2, 740, delta=10)
        # Все продукты размещены друг под другом в один столбик
        self.assertEqual(products[0].location['x'], products[1].location['x'])
        self.assertAlmostEqual(
            products[0].location['y'] + products[0].size['height'], 
            products[1].location['y'], 
            delta=40
        )

        # Билл видит внутри первой карточки картинку
        first_product_cart = products[0]
        first_product_cart_img = first_product_cart.find_element(By.CLASS_NAME, 'product_cart_img')
        self.assertAlmostEqual(
            first_product_cart_img.location['x'],
            first_product_cart.location['x'] + 10,
            delta=5
        )

        # Справа от картинки расположено название товара
        first_product_cart_name = first_product_cart.find_element(By.CLASS_NAME, 'product_cart_name')
        self.assertAlmostEqual(
            first_product_cart_name.location['x'],
            first_product_cart_img.location['x'] + first_product_cart_img.size['width'] + 20,
            delta=10
        )

        # Под названием товара кнопки, с помощью которых можно изменить количество товара
        first_product_cart_reduce_button = first_product_cart.find_element(
            By.CSS_SELECTOR, 'product_cart_reduce_button')
        first_product_cart_increase_button = first_product_cart.find_element(
            By.CSS_SELECTOR, 'product_cart_increase_button')
        self.assertAlmostEqual(
            first_product_cart_reduce_button.location['y'],
            first_product_cart_name.location['y'] + 40,
            delta=20
        )
        self.assertAlmostEqual(
            first_product_cart_reduce_button.location['y'],
            first_product_cart_increase_button.location['y'],
            delta=20
        )
        self.assertTrue(
            first_product_cart_reduce_button.location['x'] > 
            first_product_cart_increase_button.location['x']
        )

        # Справа в карточке указана общая стоимость товара
        first_product_cart_price = first_product_cart.find_element(
            By.CSS_SELECTOR, 'product_cart_price')
        self.assertAlmostEqual(
            first_product_cart_price.location['x'] + first_product_cart_price.size['width'],
            first_product_cart.location['x'] + first_product_cart.size['width'] - 20,
            delta=10
        )

        # Внизу по центру расположена кнопка для оформления заказов
        button = self.browser.find_element(By.CSS_SELECTOR, 'order_button')
        self.assertAlmostEqual(button.size['width'] / 2, 740, delta=10)
        