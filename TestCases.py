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

        width = 340
        position = slider.get_attribute('style')
        length = len(position)
        position = float(position[6:length - 2])
        return width * (hour / 24 - position / 100)

    def wait_load(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'dataViewer__frames')))

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

    def check_filter(self, filter_xpath):
        filt = self.driver.find_element_by_xpath(filter_xpath)
        if not filt.is_selected():
            filt.click()

    def test_filter(self, asserttext):
        self.wait_load()

        text = self.driver.find_element_by_class_name('mixedResults__header').text
        self.assertEqual(asserttext, text)

    def select_day(self, day):
        self.wait_load()

        day_xpath = "//div[@class='radiogroup _week']/label[" + str(day) + "]"
        self.driver.find_element_by_xpath(day_xpath).click()

    def select_hour(self, hour):
        self.wait_load()

        action = ActionChains(self.driver)
        rader_runner = self.driver.find_element_by_class_name('filters__raderRunner')
        rader_runner_in = self.driver.find_element_by_class_name('filters__raderRunnerIn')
        action.drag_and_drop_by_offset(rader_runner_in, self.slide_move(hour, rader_runner), 0).perform()

    def test_has_site(self):
        """
        Steps:
        1. нажать фильтр "есть сайт"
        Expected result:
        отфильтровываются организации не имеющие сайта(их становится меньше)
        """
        checkbox = "//label[@class='checkbox' and @title='Есть сайт']"
        asserttext = '622 организации'
        self.check_filter(checkbox)
        self.test_filter(asserttext)

    def test_has_photos(self):
        """
        Steps:
        1. нажать фильтр "есть фото"
        Expected result:
        отфильтровываются организации не имеющие фото(их становится меньше)
        """

        checkbox = "//label[@class='checkbox' and @title='Есть фото']"
        asserttext = '102 организации'
        self.check_filter(checkbox)
        self.test_filter(asserttext)

    def test_has_card(self):
        """
        Steps:
        1. нажать фильтр "расчет по картам"
        Expected result:
        отфильтровываются организации не имеющие расчета по картам(их становится меньше)
        """

        checkbox = "//label[@class='checkbox' and @title='Расчет по картам']"
        asserttext = '263 организации'
        self.check_filter(checkbox)
        self.test_filter(asserttext)

    def test_work_all_time(self):
        """
        Steps:
        1. нажать фильтр "круглосуточно"
        Expected result:
        отфильтровываются организации не работающие круглосуточно(их становится меньше)
        """

        checkbox = "//label[@class='radiogroup__label'][2]"
        asserttext = '13 организаций'
        self.check_filter(checkbox)
        self.test_filter(asserttext)

    def test_work_select_time(self):
        """
        Steps:
        1. нажать фильтр "В указанное время"
        2. выбрать день недели(выбран вторник)
        3. выбрать время (выбрано 20 часов)
        Expected result:
        отфильтровываются организации не работающие в данное время(их становится меньше)
        """

        checkbox = "//label[@class='radiogroup__label'][3]"
        asserttext = '193 организации'
        week = 2
        hour = 20
        self.check_filter(checkbox)
        self.select_day(week)
        self.select_hour(hour)
        self.test_filter(asserttext)

if __name__ == "__main__":
    unittest.main()
