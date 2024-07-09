from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import autoit
import pyautogui
import os
import json
import datetime
import allure
import pytest
import random
import string

binary_yandex_driver_file = r'C:\yandex_driver\chromedriver.exe' # ПУТЬ К ДРАЙВЕРУ
extension_path = r"C:\yandex_driver\1.2.13_0.crx" # Путь к директории расширения
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
options.add_extension(extension_path)
options.add_argument('--enable-logging')
options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
options.add_argument('--force-device-scale-factor=0.75') # Установка масштаба
service = ChromeService(executable_path=binary_yandex_driver_file)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)
driver.implicitly_wait(10)
driver.maximize_window()
cookies_file_path = os.path.join(r'D:\Allure\Cookies', 'cookies.json')
log_file_path_17 = "D:\Allure\Логи\Ошибки_при_формировании_отчета.txt"
log_file_path_18 = "D:\Allure\Логи\Ошибки_при_скачивании_отчета.txt"


try:
    driver.get("https://auth.pgs.gosuslugi.ru/auth/realms/DigitalgovTorkndProd1Auth/protocol/openid-connect/auth?client_id=DigitalgovTorkndProd1Auth-Proxy&state=b6fa62fc48c9м04787fa5bf095da2bafa&nonce=8bf3d529b0af28816d18e97bf560c4d3&response_type=code&redirect_uri=https%3A%2F%2Fpgs.gosuslugi.ru%2Fopenid-connect-auth%2Fredirect_uri&scope=openid")
    def load_session(driver, cookies_file_path):
        with open(cookies_file_path, 'r') as cookie_file:
            cookies = json.load(cookie_file)
            for cookie in cookies:
                # Пропускаем HttpOnly куки, так как их нельзя установить через WebDriver
                if 'sameSite' in cookie:
                    del cookie['sameSite']
                driver.add_cookie(cookie)
        print(f"Куки загружены из '{cookies_file_path}'.")
    ready_state = driver.execute_script("return document.readyState")
    load_session(driver, cookies_file_path)
    driver.get("https://pgs.gosuslugi.ru/select-application")
finally:
    time.sleep(5)


@allure.title('Тест Формирование, скачивание отчета')
@allure.description("Проверка формирования и скачивания отчета")
def test_object():
    
    with allure.step("Смена организации"):
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-main-menu/div/div[1]/div[1]/div/div/a"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-select-branch/div/div[2]/div[2]/div/div/div[1]"))).click()
        time.sleep(3)
        allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
    
    with allure.step("Переход в модуль Отчеты"):
        driver.get('https://pgs.gosuslugi.ru/reports/reports')
        # Ждем, пока страница загрузится
        ready_state = driver.execute_script("return document.readyState")
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)


    with allure.step("Нажатие кнопки Новый отчет"):
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-universal-collection-page/evolenta-adaptive-navbar/div/div/div/button/b")))
        next_button.click()
        allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)
        time.sleep(3)

        # Активация, заполнение поля "Наименование вида отчета"
        input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-universal-collection-page/div[2]/div[1]/div/evolenta-filters-bar/evolenta-scrollbar/div/div/div/div/div/div[2]/div/div/form/div/input")))
        input_field.click() 
        input_field.send_keys("Перечень пользователей в разрезе КНО по региону")
        time.sleep(3)
        element_to_hover_over = driver.find_element(By.XPATH, '/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-universal-collection-page/div[2]/div[2]/div/div/div[1]/div/evolenta-infinite-scrollbar/div/div/div[1]/div')
        # Наведение на элемент
        hover = ActionChains(driver).move_to_element(element_to_hover_over)
        hover.perform()
        # Дождаться, когда появится скрытая кнопка (примерно)
        hidden_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-universal-collection-page/div[2]/div[2]/div/div/div[1]/div/evolenta-infinite-scrollbar/div/div/div[1]/div[2]/button")))
        # Нажать на скрытую кнопку
        hidden_button.click()
        
    with allure.step("Нажатие кнопки Сформировать"):    
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-report-wrapper/evolenta-custom-report/div/evolenta-sidebar-wrapper/div/div[1]/div/div/div[2]/button[1]")))
        next_button.click()
        time.sleep(4)
        allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)

        with allure.step("Сбор сетевых логов"):
            driver.execute_cdp_cmd('Network.enable', {})
            # Запись записей в сетевом журнале
            log_entries = driver.get_log("performance") 
            # Открываем файл для записи ошибок
            with open(log_file_path_17, "w") as log_file:
            # Добавляем текущую дату и время перед записью логов
                current_datetime = datetime.datetime.now()
                log_file.write("Дата и время: " + current_datetime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                # Записываем заголовок
                log_file.write("Ошибки при нажатии кнопки 'Сформировать отчет'\n\n")    
                for entry in log_entries:
                    try:
                        message_obj = json.loads(entry.get("message"))
                        message = message_obj.get("message")
                        method = message.get("method")
                        if method == 'Network.responseReceived':
                            response = message.get('params', {}).get('response', {})
                            response_url = response.get('url', '')
                            response_status = response.get('status', 0)
                            response_headers = response.get('headers', {})
                            response_body = response.get('body', '')
                            if response_status >= 400:
                                log_file.write("Response URL: {}\n".format(response_url))
                                log_file.write("Response Status: {}\n".format(response_status))
                                log_file.write("Response Headers: {}\n".format(response_headers))
                                log_file.write("Response Body: {}\n".format(response_body))
                                log_file.write("\n")
                    except Exception as e:
                        print(e)
                # Добавляем разделитель в конце файла
                log_file.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            allure.attach.file(log_file_path_17, name="network_log", attachment_type=allure.attachment_type.TEXT)
            print(f"Файл '{log_file_path_17}' с результатом теста создан.")
            time.sleep(5)
        
    with allure.step("Нажатие кнопки Скачать"):     
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/evolenta-sidebar/evolenta-section/evolenta-report-wrapper/evolenta-custom-report/div/evolenta-sidebar-wrapper/div/div[1]/div/div/div[2]/button[2]")))
        next_button.click()
        time.sleep(1)
        allure.attach(driver.get_screenshot_as_png(), name="Скрин", attachment_type=allure.attachment_type.PNG)

        with allure.step("Сбор сетевых логов"):
            driver.execute_cdp_cmd('Network.enable', {})
            # Запись записей в сетевом журнале
            log_entries = driver.get_log("performance") 
            # Открываем файл для записи ошибок
            with open(log_file_path_18, "w") as log_file:
            # Добавляем текущую дату и время перед записью логов
                current_datetime = datetime.datetime.now()
                log_file.write("Дата и время: " + current_datetime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                # Записываем заголовок
                log_file.write("Ошибки при нажатии кнопки 'Скачать отчет'\n\n")    
                for entry in log_entries:
                    try:
                        message_obj = json.loads(entry.get("message"))
                        message = message_obj.get("message")
                        method = message.get("method")
                        if method == 'Network.responseReceived':
                            response = message.get('params', {}).get('response', {})
                            response_url = response.get('url', '')
                            response_status = response.get('status', 0)
                            response_headers = response.get('headers', {})
                            response_body = response.get('body', '')
                            if response_status >= 400:
                                log_file.write("Response URL: {}\n".format(response_url))
                                log_file.write("Response Status: {}\n".format(response_status))
                                log_file.write("Response Headers: {}\n".format(response_headers))
                                log_file.write("Response Body: {}\n".format(response_body))
                                log_file.write("\n")
                    except Exception as e:
                        print(e)
                # Добавляем разделитель в конце файла
                log_file.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            allure.attach.file(log_file_path_17, name="network_log", attachment_type=allure.attachment_type.TEXT)
            print(f"Файл '{log_file_path_18}' с результатом теста создан.")
            time.sleep(5)
