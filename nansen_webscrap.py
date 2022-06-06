from selenium import webdriver
from time import sleep
import json


def get_conf():
    content = open('config/nansenconnectivity.json')
    config = json.load(content)
    username = config['Username']
    password = config['Password']
    return username, password


def start_driver(driver_path, url, username, password):
    driver = webdriver.Chrome(driver_path)
    sleep(5)
    driver.get(url)
    sleep(5)
    driver.find_element(by='id', value="email").send_keys(username)
    driver.find_element(by='id', value="password").send_keys(password)
    driver.find_element(by='xpath', value='/html/body/div[1]/div/div[3]/div/div[1]/div/form/button').click()
    sleep(10)
    return driver


def get_top_news(driver):
    xpath_list = ['/html/body/div[1]/div/div[3]/div/main/div[4]/div/article/section[1]/div/div[1]/div[2]/a',
                  '/html/body/div[1]/div/div[3]/div/main/div[4]/div/article/section[1]/div/div[1]/div[3]/a',
                  '/html/body/div[1]/div/div[3]/div/main/div[4]/div/article/section[1]/div/div[1]/div[4]/a',
                  '/html/body/div[1]/div/div[3]/div/main/div[4]/div/article/section[1]/div/div[1]/div[5]/a',
                  '/html/body/div[1]/div/div[3]/div/main/div[4]/div/article/section[1]/div/div[1]/div[6]/a']
    get_news_title = []
    get_news_link = []
    for el in xpath_list:
        title = driver.find_element(by='xpath', value=el).text
        link = driver.find_element(by='xpath', value=el).get_attribute('href')
        get_news_title.append(title)
        get_news_link.append(link)
    return get_news_title, get_news_link


def main():
    driver_path = '/Users/thomasgrandguillot/Desktop/chromedriver'
    url = 'https://pro.nansen.ai/'
    username, password = get_conf()
    driver = start_driver(driver_path, url, username, password)
    get_news_title, get_news_link = get_top_news(driver)
    print('Extract news!')
    return get_news_title, get_news_link


if __name__ == '__main__':
    get_news = main()

# driver.find_element(by=By.CSS_SELECTOR, value=)
# driver.find_element_by_css_selector()
# driver.find_element_by_id()
# driver.find_element_by_class_name()
# driver.find_element_by_name()
# /html/body/div[1]/div/div[3]/div/div[1]/div/form/button
# /html/body/div[1]/div/div[3]/div/main/div[4]/div/article/section[1]/div/div[1]/div[2]
# /html/body/div[1]/div/div[3]/div/main/div[4]/div/article/section[1]/div/div[1]/div[2]/a
