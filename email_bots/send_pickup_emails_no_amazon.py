from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.maximize_window()

gmail_username = 'rma@d2amicro.com'
gmail_password = 'D2AMicroHA0'

amazon_username = 'maux7910@mylaurier.ca'
amazon_password = '3t2cuqs@A'

global emailWindow
global messagesWindow
global ordersWindow


def expand_shadow_element(element):
    shadow_root = driver.execute_script(
        'return arguments[0].shadowRoot', element)
    return shadow_root


def loginAmazon():
    try:
        driver.execute_script(
            "window.open('https://sellercentral.amazon.ca/home')")

        driver.switch_to.window(driver.window_handles[1])

        username_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, 'ap_email')
        ))
        password_box = driver.find_element_by_id('ap_password')

        username_box.send_keys(amazon_username)
        password_box.send_keys(amazon_password + Keys.ENTER)

        # Check if the error where it says "text me at my number" happens. (can't get past it)
        try:
            text = driver.find_element_by_xpath(
                '//*[@id="authportal-main-section"]/div[2]/div/div/div/div/p').text
            checkFor = 'Choose where to receive the One Time Password (OTP)'
            if checkFor in text:
                print("Locked out... RIP.")
                return False
        except:
            pass

        while True:
            sleep(1)
            try:
                captcha_box = driver.find_element_by_id('auth-captcha-guess')
                captcha = input("Captcha detected. Enter captcha: ")
                captcha_box.send_keys(captcha)
                driver.find_element_by_id(
                    'ap_password').send_keys(amazon_password)
                driver.find_element_by_id('signInSubmit').click()
            except:
                break

        OTP_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="auth-mfa-otpcode"]')
        ))

        OTP = input("Enter OTP: ")

        try:
            OTP_box.send_keys(OTP + Keys.ENTER)
            while EC.element_to_be_clickable((By.XPATH, '//*[@id="auth-mfa-otpcode"]')):
                OTP = input("OTP Incorrect. Try again: ")
                OTP_box.send_keys(OTP + Keys.ENTER)
        except:
            pass

        sleep(1)

        driver.close()
        driver.switch_to.window(emailWindow)

        return True
    except:
        return False


def loginGmail():
    global gmail_username
    global gmail_password

    try:
        username_box = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="identifierId"]')
        ))

        sleep(0.5)

        username_box.send_keys(gmail_username + Keys.ENTER)

        password_box = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
        ))

        sleep(0.5)

        password_box.send_keys(gmail_password + Keys.ENTER)
        return True
    except:
        return False


def sendKeysToBody(send):
    body = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.TAG_NAME, 'body')
    ))

    body.send_keys(send)

    return


def log(level, message):
    # 1 = WARNING    2 = ERROR    3 = FATAL
    if level == 1:
        print('::> [WARNING]: {}'.format(message))
    elif level == 2:
        print('::> [ERROR]: {}'.format(message))
    elif level == 3:
        print('::> [FATAL]: {}'.format(message))


def getOrderConfirmationNumber(text):

    index1 = text.find('Order confirmation number')
    index2 = text.find('\n', index1)
    index3 = text.find('\n', index2 + 1)
    confirmation_number = text[index2 + 1:index3]

    return confirmation_number


def getMessageForClient(text):
    index1 = text.find('Your parcel is ready for pickup')
    index2 = text.find('Your pickup location')
    index3 = text.find('To pick up your parcel')

    # check if there's no pick up location
    pickup_loc = text[index2:index3].strip()

    if pickup_loc == 'Your pickup location':
        message = text[index1:index2]
    else:
        message = text[index1:index3]

    return message


def checkAmazon(code):
    global messagesWindow
    global amazon_username
    global amazon_password

    notSent = True

    sleep(1)

    driver.switch_to.window(messagesWindow)

    messages_search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="threads-list-search-bar"]/kat-input')

    ))

    messages_search_box.send_keys(code + Keys.ENTER)

    sleep(1)

    try:
        driver.find_elements_by_xpath(
            '//*[@id="all-messages-link"]/kat-button')
    except:
        notSent = False

    return notSent


def sendAmazon(code, text):

    driver.execute_script(
        "window.open('https://sellercentral.amazon.ca/orders-v3/order/{}')".format(code))

    driver.switch_to.window(driver.window_handles[2])

    # click on the name which is also a link
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="MYO-app"]/div/div[1]/div[1]/div/div[3]/div[2]/div/div/div/div/div[2]/div/table/tbody/tr[1]/td[2]/span')
    )).click()

    sleep(2)

    # Now loading the send message page

    driver.switch_to.window(driver.window_handles[3])

    problems_button = driver.find_element_by_xpath(
        '//*[@id="ayb-contact-buyer"]/div[3]/kat-box/div/kat-radiobutton[4]')
    other_button = driver.find_element_by_xpath(
        '//*[@id="ayb-contact-buyer"]/div[3]/kat-box/div/kat-radiobutton[5]')

    try:
        other_button.click()
    except:
        problems_button.click()

    messages_box = WebDriverWait(driver, 3).until(EC.element_to_be_clickable(
        (By.XPATH,
            '//*[@id="katal-id-20"]')
    ))

    messages_box.send_keys(text)

    input("WE MADE IT!!!")

    # Hit the submit button

    driver.find_element_by_xpath(
        '//*[@id="ayb-contact-buyer"]/div[8]/kat-button').click()

    sleep(1)

    driver.close()

    return


def main():
    global emailWindow
    global messagesWindow
    global ordersWindow

    # starting_date = input("Enter starting date (YYYY/MM/DD): ")
    starting_date = '2021/05/12'

    driver.get("http://gmail.com")

    emailWindow = driver.window_handles[0]

    if not loginGmail():
        print("Error logging in gmail.")
        return

    """
    if not loginAmazon():
        print("Error logging in Amazon.")
        return
    """

    # driver.execute_script(
    #   "window.open('https://sellercentral.amazon.ca/messaging/inbox-v2')")

    # messagesWindow = driver.window_handles[1]

    driver.switch_to.window(emailWindow)

    search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="gs_lc50"]/input[1]')
    ))

    search_box.send_keys('Ready for pickup after:{}'.format(
        starting_date) + Keys.ENTER)

    sleep(1)

    sendKeysToBody(Keys.ENTER)

    while True:
        try:
            WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element(
                (By.CLASS_NAME, 'gs'), 'Order confirmation number'
            ))
        except:
            print("Can't find body of email.")
            break

        info = driver.find_element_by_class_name('gs')

        text = info.text

        confirmation_code = getOrderConfirmationNumber(text)

        print('"{}"'.format(confirmation_code))

        # needToSend = checkAmazon(confirmation_code)
        needToSend = True

        if needToSend:
            message = getMessageForClient(text)
            print(message)
            break
            # sendAmazon(confirmation_code, message)

        driver.switch_to.window(emailWindow)

        sendKeysToBody('j')

    return


if __name__ == "__main__":
    main()
    input("::> Program finished.")
    driver.quit()
