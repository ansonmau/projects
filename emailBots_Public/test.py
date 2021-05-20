from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from datetime import date


def main():
    today = date.today().strftime("%m/%d")

    driver = webdriver.Chrome()

    driver.maximize_window()

    driver.get("http://amazon.ca")

    input()

    driver.get(
        "https://sellercentral.amazon.ca/orders-v3/order/702-6841957-0050664")

    sleep(5)

    sellerNotes = driver.find_element_by_xpath(
        '//*[@id="MYO-app"]/div/div[1]/div[2]/div[2]/div/div[1]/textarea')

    sellerNotes.send_keys(Keys.ENTER + "RFP: {}".format(today))

    input("Enter to end.")

    driver.quit()

    return


if __name__ == "__main__":
    main()
