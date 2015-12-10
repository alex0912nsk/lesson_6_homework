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
        return 340 * (hour/24 - position/100)

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
        self.driver.close()

    def test_has_site(self):
        """
        Steps:
        1. нажать фильтр "есть сайт"
        Expected result:
        отфильтровываются организации не имеющие сайта(их становится меньше)
        """

        self.driver.find_element_by_xpath("//div[@class='filters__main']/div[3]/label[1]").click()
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'dataViewer__frames')))
        text = self.driver.find_element_by_class_name('mixedResults__header').text
        self.assertEqual('621 организация', text)

    def test_has_photos(self):
        """
        Steps:
        1. нажать фильтр "есть фото"
        Expected result:
        отфильтровываются организации не имеющие фото(их становится меньше)
        """

        self.driver.find_element_by_xpath("//div[@class='filters__main']/div[3]/label[2]").click()
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'dataViewer__frames')))
        text = self.driver.find_element_by_class_name('mixedResults__header').text
        self.assertEqual('101 организация', text)

    def test_has_card(self):
        """
        Steps:
        1. нажать фильтр "расчет по картам"
        Expected result:
        отфильтровываются организации не имеющие расчета по картам(их становится меньше)
        """

        self.driver.find_element_by_xpath("//div[@class='filters__main']/div[3]/label[3]").click()
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'dataViewer__frames')))
        text = self.driver.find_element_by_class_name('mixedResults__header').text
        self.assertEqual('263 организации', text)

    def test_work_all_time(self):
        """
        Steps:
        1. нажать фильтр "круглосуточно"
        Expected result:
        отфильтровываются организации не работающие круглосуточно(их становится меньше)
        """

        self.driver.find_element_by_xpath("//div[@class='filters__workhours']/div/div/label[2]").click()
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'dataViewer__frames')))
        text = self.driver.find_element_by_class_name('mixedResults__header').text
        self.assertEqual('13 организаций', text)

    def test_work_select_time(self):
        """
        Steps:
        1. нажать фильтр "В указанное время"
        2. выбрать день недели(выбран вторник)
        3. выбрать время (выбрано 20 часов)
        Expected result:
        отфильтровываются организации не работающие в данное время(их становится меньше)
        """

        self.driver.find_element_by_xpath("//div[@class='filters__workhours']/div/div/label[3]").click()
        self.driver.find_element_by_xpath("//div[@class='radiogroup _week']/label[2]").click()

        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(self.driver.find_element_by_class_name('filters__raderRunnerIn'),
                                       self.slide_move(20, self.driver.find_element_by_class_name('filters__raderRunner')), 0).perform()

        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'dataViewer__frames')))
        text = self.driver.find_element_by_class_name('mixedResults__header').text
        self.assertEqual('192 организации', text)


if __name__ == "__main__":
    unittest.main()