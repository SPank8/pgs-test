import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import os
import datetime
import json
import pytest

binary_yandex_driver_file = r'C:\yandex_driver\chromedriver.exe' # ПУТЬ К ДРАЙВЕРУ
extension_path = r"C:\yandex_driver\1.2.13_0.crx" # Путь к директории расширения
options = webdriver.ChromeOptions()
options.add_experimental_option('detach',True)
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

# Функция для сохранения сессии (куков)
def save_session(driver, cookies_file_path):
    cookies = driver.get_cookies()
    with open(cookies_file_path, 'w') as cookie_file:
        json.dump(cookies, cookie_file, indent=4)
    print(f"Куки сохранены в '{cookies_file_path}'.")

# АВТОРИЗАЦИЯ
@allure.title("Тест авторизации через ЕСИА")
@allure.description("Проверка авторизации через ЕСИА и запись сетевых логов.")
def test_esia_auth():
    with allure.step("Открытие страницы авторизации"):
        driver.get("https://auth.pgs.gosuslugi.ru/auth/realms/DigitalgovTorkndProd1Auth/protocol/openid-connect/auth?client_id=DigitalgovTorkndProd1Auth-Proxy&state=b6fa62fc48c9м04787fa5bf095da2bafa&nonce=8bf3d529b0af28816d18e97bf560c4d3&response_type=code&redirect_uri=https%3A%2F%2Fpgs.gosuslugi.ru%2Fopenid-connect-auth%2Fredirect_uri&scope=openid")
        allure.attach(driver.get_screenshot_as_png(), name="auth_page", attachment_type=allure.attachment_type.PNG)

    with allure.step("Нажатие кнопки 'Вход через ЕСИА'"):
        esia_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='kc-social-providers']/ul")))
        esia_button.click()
        allure.attach(driver.get_screenshot_as_png(), name="esia_button_click", attachment_type=allure.attachment_type.PNG)

    driver.implicitly_wait(2)

    with allure.step("Ввод телефона"):
        login_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/esia-root/div/esia-login/div/div[1]/form/div[1]/esia-input/input")))
        login_input = driver.find_element(By.XPATH, "/html/body/esia-root/div/esia-login/div/div[1]/form/div[1]/esia-input/input")
        login_input.click()
        time.sleep(2)
        login_input.send_keys("+79374426231")
        allure.attach(driver.get_screenshot_as_png(), name="phone_input", attachment_type=allure.attachment_type.PNG)

    with allure.step("Ввод пароля"):
        password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/esia-root/div/esia-login/div/div[1]/form/div[2]/esia-input-password/div/input")))
        password_input = driver.find_element(By.XPATH, "/html/body/esia-root/div/esia-login/div/div[1]/form/div[2]/esia-input-password/div/input")
        password_input.click()
        time.sleep(2)
        password_input.send_keys("S.pank470")
        allure.attach(driver.get_screenshot_as_png(), name="password_input", attachment_type=allure.attachment_type.PNG)

    with allure.step("Нажатие кнопки 'Войти'"):
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/esia-root/div/esia-login/div/div[1]/form/div[4]/button")))
        login_button.click()
        allure.attach(driver.get_screenshot_as_png(), name="login_button_click", attachment_type=allure.attachment_type.PNG)

    with allure.step("Генерация и ввод TOTP-кода"):
        driver.execute_script("window.open('https://piellardj.github.io/totp-generator/?secret=AFDQSZB3NFBUCTBRSUEZ6NWCQIWCR66S&digits=6&period=30&algorithm=SHA-1')")
        driver.switch_to.window(driver.window_handles[1])
        copy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[3]/div/div[2]/div[1]/button")))
        copy_button.click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[0])
        code_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/esia-root/div/esia-login/div/div/esia-enter-mfa/esia-ttp/form/div[2]/div/esia-code-input/div/code-input/span[1]/input")))
        code_input.click()
        time.sleep(1)
        code_input.send_keys(Keys.CONTROL + 'v')
        allure.attach(driver.get_screenshot_as_png(), name="totp_input", attachment_type=allure.attachment_type.PNG)

    time.sleep(15)
    driver.refresh()

    with allure.step("Нажатие кнопки 'Далее'"):
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/form/div/button[2]/div")))
        next_button.click()
        allure.attach(driver.get_screenshot_as_png(), name="next_button_click", attachment_type=allure.attachment_type.PNG)

    time.sleep(5)
    # Сохранение куков после успешной авторизации
    save_session(driver, cookies_file_path)
    time.sleep(3)

    with allure.step("Сбор сетевых логов"):
        driver.execute_cdp_cmd('Network.enable', {})
        log_entries = driver.get_log("performance")
        log_file_path = "network_log.txt"
        with open(log_file_path, "w") as log_file:
            current_datetime = datetime.datetime.now()
            log_file.write("Дата и время: " + current_datetime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
            log_file.write("Ошибки_при_авторизации\n\n")
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
            log_file.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
        allure.attach.file(log_file_path, name="network_log", attachment_type=allure.attachment_type.TEXT)

    time.sleep(3)
    print(f"Файл '{log_file_path}' с результатом теста создан.")
    time.sleep(3)
    driver.quit()
