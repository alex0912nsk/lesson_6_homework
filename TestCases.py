import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class FirstTestCase(unittest.TestCase):
    """
    Test Cases:
    Проверка фильтров организаций
    """

    def slide_move(self, hour, slider):
        """
        :param hour:  час, на который нужно передвинуть слайдер
        :param slider: сам слайдер
        :return: значение в px, на которое нужно сдвинуть слайдер
        340 - ширина слайдера
        """

        position = slider.get_attribute('style')
        length = len(position)
        position = float(position[6:length - 2])
        return 340 * (hour / 24 - position / 100)

    def setUp(self):
        """
        Preconditions:
        1. Находиться на сайте 2gis.ru
        2. Зайти в рубрику
        3. Зайти в фильтры рубрики
        """

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(20)
        self.driver.get('2gis.ru')

        action = ActionChains(self.driver)
        action.send_keys('компьютеры')
        action.perform()

        self.driver.find_element_by_class_name('searchBar__submit').click()
        self.driver.find_element_by_xpath("//div[@class='filters__primaryExtended']").click()

    def tearDown(self):
        self.driver.quit()

    def work_with_filters(self, filter_xpath, asserttext, day=None, hour=None):
        filt = self.driver.find_element_by_xpath(filter_xpath)
        if not filt.is_selected():
            filt.click()

        if 0 < day < 8 and filter_xpath == "//label[@class='radiogroup__label'][3]":
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'dataViewer__frames')))
            self.driver.find_element_by_xpath("//div[@class='radiogroup _week']/label[" + str(day) + "]").click()
        if -1 < hour < 25 and filter_xpath == "//label[@class='radiogroup__label'][3]":
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'dataViewer__frames')))
            action = ActionChains(self.driver)
            action.drag_and_drop_by_offset(self.driver.find_element_by_class_name('filters__raderRunnerIn'),
                                           self.slide_move(hour, self.driver.find_element_by_class_name('filters__raderRunner')), 0).perform()

        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'dataViewer__frames')))
        text = self.driver.find_element_by_class_name('mixedResults__header').text
        self.assertEqual(asserttext, text)

    def test_has_site(self):
        """
        Steps:
        1. нажать фильтр "есть сайт"
        Expected result:
        отфильтровываются организации не имеющие сайта(их становится меньше)
        """

        self.work_with_filters("//label[@class='checkbox' and @title='Есть сайт']", '621 организация')

    def test_has_photos(self):
        """
        Steps:
        1. нажать фильтр "есть фото"
        Expected result:
        отфильтровываются организации не имеющие фото(их становится меньше)
        """

        self.work_with_filters("//label[@class='checkbox' and @title='Есть фото']", '102 организации')

    def test_has_card(self):
        """
        Steps:
        1. нажать фильтр "расчет по картам"
        Expected result:
        отфильтровываются организации не имеющие расчета по картам(их становится меньше)
        """

        self.work_with_filters("//label[@class='checkbox' and @title='Расчет по картам']", '263 организации')

    def test_work_all_time(self):
        """
        Steps:
        1. нажать фильтр "круглосуточно"
        Expected result:
        отфильтровываются организации не работающие круглосуточно(их становится меньше)
        """

        self.work_with_filters("//label[@class='radiogroup__label'][2]", '13 организаций')

    def test_work_select_time(self):
        """
        Steps:
        1. нажать фильтр "В указанное время"
        2. выбрать день недели(выбран вторник)
        3. выбрать время (выбрано 20 часов)
        Expected result:
        отфильтровываются организации не работающие в данное время(их становится меньше)
        """

        self.work_with_filters("//label[@class='radiogroup__label'][3]", '192 организации', 2, 20)

if __name__ == "__main__":
    unittest.main()
