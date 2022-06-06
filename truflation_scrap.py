from selenium import webdriver
from time import sleep
import json


def get_trusted_inflation():
    driver_path = '/Users/thomasgrandguillot/Desktop/chromedriver'
    url = 'https://app.truflation.com/'
    driver = webdriver.Chrome(driver_path)
    driver.get(url)
    sleep(5)
    truflation = driver.find_element(by='xpath', value='/html/body/div/div/div/main/div/div[1]/section[1]/div/div/div[1]/div[1]/div/div/div[2]/div[1]/div/div[2]/div[1]').text
    return truflation


if __name__ == '__main__':
    truflation = get_trusted_inflation()
