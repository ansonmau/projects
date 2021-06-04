from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from datetime import date
import secret

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.maximize_window()

myOS = 'win'

gmail_username = secret.usernames['gmail']
gmail_password = secret.passwords['gmail']

amazon_username = secret.usernames['amazon']
amazon_password = secret.passwords['amazon']

today = date.today().strftime("%m/%d")

global emailWindow
global messagesWindow
global ordersWindow

failed_orders_codes = []


def writeStuffToFile():
    file = open('info-amazon.txt', 'w')
    message = '\n>>>  Orders that the program could not complete\n'
    file.write(('-'*len(message)) + message +
               ('-'*len(message)) + "\n")
    for code in failed_orders_codes:
        file.write("{}\n".format(code))
    file.close()
    return


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

        # check for captcha
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

        # Check for if amazon is fed up with my shit and needs me to use authenticator
        try:
            text = driver.find_element_by_xpath(
                '//*[@id="authportal-main-section"]/div[2]/div/div/div/div/p').text
            checkFor = 'Choose where to receive the One Time Password (OTP)'
            if checkFor in text:
                driver.find_element_by_xpath(
                    '//*[@id="auth-select-device-form"]/div[1]/fieldset/div[3]').click()
                driver.find_element_by_xpath('//*[@id="a-autoid-0"]').click()
        except:
            pass

        # check if OTP is needed
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="auth-mfa-otpcode"]')
            ))
            # Use a while loop in case the user messes up OTP code
            while True:
                try:
                    OTP_box = driver.find_element_by_xpath(
                        '//*[@id="auth-mfa-otpcode"]')
                    OTP = input("Enter OTP: ")
                    OTP_box.send_keys(OTP + Keys.ENTER)
                    sleep(1)
                except:
                    print("OTP Passed.")
                    break
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


def log(message, level=1):
    # 1 = INFO    2 = ERROR    3 = FATAL
    if level == 1:
        print('::> [INFO]  {}'.format(message))
    elif level == 2:
        print('::> [ERROR] {}'.format(message))
    elif level == 3:
        print('::> [FATAL] {}'.format(message))


def getOrderConfirmationNumber(text):

    index1 = text.find('Order confirmation number')
    index2 = text.find('\n', index1)
    index3 = text.find('\n', index2 + 1)
    confirmation_number = text[index2 + 1:index3]

    return confirmation_number


def getTrackingNum(text):

    index1 = text.find('Tracking number')
    index2 = text.find('\n', index1)
    index3 = text.find('\n', index2 + 1)
    tracking_num = text[index2 + 1:index3]
    return tracking_num


def getMessageForClient(text):
    index1 = text.find('Your parcel is ready for pickup')
    index2 = text.find('Your pickup location')
    index3 = text.find('To pick up your parcel')

    # check if there's no pick up location (checking if theres anything between the 2 strings)
    pickup_loc = text[index2:index3].strip()

    if pickup_loc == 'Your pickup location':
        # no pick up location
        message = text[index1:index2]
    else:
        message = text[index1:index3]

    return message


def checkAmazon(confirmation_code, tracking_num):
    global messagesWindow

    need2Send = True

    sleep(1)

    driver.switch_to.window(messagesWindow)

    messages_search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH,
         '//*[@id="threads-list-search-bar"]/kat-input')
    ))
    if myOS == "win":
        messages_search_box.send_keys(Keys.CONTROL + 'a')
    else:
        messages_search_box.send_keys(Keys.COMMAND + 'a')
    messages_search_box.send_keys(
        Keys.BACK_SPACE + confirmation_code + Keys.ENTER)

    sleep(3)

    try:
        my_messages = driver.find_elements_by_class_name(
            'thread-message-max-width-container-right')

        for message in my_messages:
            curr_text = message.text
            if confirmation_code in curr_text and tracking_num in curr_text:
                need2Send = False
                break
    except:
        pass

    return need2Send


def sendAmazon(code, text):

    driver.execute_script(
        "window.open('https://sellercentral.amazon.ca/orders-v3/order/{}')".format(code))

    driver.switch_to.window(driver.window_handles[2])

    # click on the name which is also a link
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="MYO-app"]/div/div[1]/div[1]/div/div[3]/div[2]/div/div/div/div/div[2]/div/table/tbody/tr[1]/td[2]/span')
    )).click()

    # Now loading the send message page

    sleep(2)

    driver.switch_to.window(driver.window_handles[3])

    try:
        other_button = driver.find_element_by_xpath(
            '//*[@id="ayb-contact-buyer"]/div[3]/kat-box/div/kat-radiobutton[5]')

        other_button.click()

        WebDriverWait(driver, 2).until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="ayb-contact-buyer"]/div[4]/form/div[1]/div/div[1]/kat-textarea')
        ))
    except:
        problems_button = driver.find_element_by_xpath(
            '//*[@id="ayb-contact-buyer"]/div[3]/kat-box/div/kat-radiobutton[4]')

        problems_button.click()

    text_area = driver.find_element_by_css_selector(
        "[unique-id='katal-id-20']")

    driver.execute_script(
        'arguments[0].setAttribute("value", `{}`)'.format(text), text_area)

    # Text area is hidden behind a shadow root so we use this to get around it.
    box = driver.execute_script(
        "return arguments[0].shadowRoot.querySelector('textarea')", text_area)

    # send a space so that the thing updates (if i dont do this, the page doesn't think that anything is in the text box)
    box.send_keys(" ")

    input("Press enter to continue the program.")

    sleep(0.5)

    # Hit the submit button
    driver.find_element_by_xpath(
        '//*[@id="ayb-contact-buyer"]/div[8]/kat-button').click()

    sleep(1)

    driver.close()

    driver.switch_to.window(driver.window_handles[2])

    try:
        log('Adding RFP to Seller Notes')
        sellerNotes = driver.find_element_by_xpath(
            '//*[@id="MYO-app"]/div/div[1]/div[2]/div[2]/div/div[1]/textarea')
        sellerNotes.send_keys(Keys.ENTER + "RFP - {}".format(today))
    except:
        log('Cant add rfp to seller notes', 2)

    sleep(2)

    driver.close()

    sleep(0.5)

    return


def main():
    global emailWindow
    global messagesWindow
    global ordersWindow

    starting_date = input("Enter starting date (YYYY/MM/DD): ")

    driver.get("http://gmail.com")

    emailWindow = driver.window_handles[0]

    log('Logging into gmail')
    if not loginGmail():
        log("Error logging into gmail.", 3)
        return

    log('Logging into amazon')
    if not loginAmazon():
        log("Error logging into amazon.", 3)
        return

    log('Opening messaging service')
    driver.execute_script(
        "window.open('https://sellercentral.amazon.ca/messaging/inbox-v2')")

    messagesWindow = driver.window_handles[1]

    log('Looking for relevant emails')

    driver.switch_to.window(emailWindow)

    search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="gs_lc50"]/input[1]')
    ))

    search_box.send_keys('"Ready for pickup" from:canadapost after:{}'.format(
        starting_date) + Keys.ENTER)

    sleep(1)

    sendKeysToBody(Keys.ENTER)

    while True:
        try:
            log('Looking for confirmation code')
            WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element(
                (By.CLASS_NAME, 'gs'), 'Order confirmation number'
            ))
        except:
            log('Last email finished.')
            break

        try:
            info = driver.find_element_by_class_name('gs')

            text = info.text

            confirmation_code = getOrderConfirmationNumber(text)
            tracking_num = getTrackingNum(text)

            log('Checking for message on amazon')
            needToSend = checkAmazon(confirmation_code, tracking_num)

            if needToSend:
                log('{} - Message not found, sending now'.format(confirmation_code))
                message = getMessageForClient(text)
                if 'reminder' in text:
                    message = "[FINAL REMINDER]\n" + message
                sendAmazon(confirmation_code, message)
            else:
                log('{} - Message found'.format(confirmation_code))

        except:
            log("[!!!] Error occured on order {}".format(confirmation_code), 2)
            failed_orders_codes.append(confirmation_code)
            # Make sure the other windows are all closed other than the email and messages windows.
            for i in [3, 2]:
                try:
                    driver.switch_to.window(driver.window_handles[i])
                    driver.close()
                except:
                    pass

        log('Moving to next email')
        driver.switch_to.window(emailWindow)

        sendKeysToBody('j')

    if failed_orders_codes:
        writeStuffToFile()

    return


if __name__ == "__main__":
    main()
    input("::> Program finished.")
    driver.quit()
