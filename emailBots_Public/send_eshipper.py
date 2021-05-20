from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
import secret

STARTDATE = ''
ENDDATE = ''

eshipper_username = secret.usernames['eshipper']
eshipper_password = secret.passwords['eshipper']

PAUSE_AFTER_FILLING = 1
LOADINGTIME = 2

num_links_total = 0
num_page = 1

failed_links = []
# rfs = ready for shipping
rfs_codes = []


def log(message):

    print(" " * 50, end='\r')
    print(message, end='\r')

    return


def writeStuffToFile():
    if failed_links or rfs_codes:
        file = open("info-eshipper.txt", "w")

        if failed_links:
            message = '\n>>> Links that the program could not complete\n'
            file.write(('-'*len(message)) + message +
                       ('-'*len(message)) + "\n")
            for link in failed_links:
                file.write("{}\n".format(link))

        if rfs_codes:
            message = '\n>>> Codes of orders that are "ready for shipping" after 3+ days.\n'
            file.write(('-'*len(message)) + message +
                       ('-'*len(message)) + "\n")
            for code in rfs_codes:
                file.write("{}\n".format(code))

        file.close()
    return


def fillUPS(driver):

    # Get rid of the annoying cookies thing
    try:
        log('Removing annoying cookies banner...')
        driver.execute_script("""
    var l = document.getElementsByClassName("implicit_privacy_prompt implicit_consent")[0];
    l.parentNode.removeChild(l);
    """)
    except:
        pass

    log('Looking for get updates button...')
    getUpdates_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="stApp_btnSendMeUpdate"]')))
    getUpdates_button.click()

    log('Choosing settings...')
    forThisDeliveryOnly_button = driver.find_element_by_xpath(
        '//*[@id="upsAng2Modal"]/div/div/div[2]/fieldset/div[2]/label/strong')
    forThisDeliveryOnly_button.click()

    continue_button = driver.find_element_by_xpath(
        '//*[@id="upsAng2Modal"]/div/div/div[2]/div/button[1]')
    continue_button.click()

    try:
        updateSetting1_button = driver.find_element_by_xpath(
            '//*[@id="stApp_pkgUpdatesDelaylbl"]')
        updateSetting1_button.click()
    except:
        pass

    try:
        updateSetting2_button = driver.find_element_by_xpath(
            '//*[@id="stApp_pkgUpdatesDeliveredlbl"]')
        updateSetting2_button.click()
    except:
        pass

    log('Filling info...')

    email_box = driver.find_element_by_xpath(
        '//*[@id="stApp_pkgUpdatesEmailPhone1"]')
    email_box.send_keys('RMA@INFONEC.COM')

    done_button = driver.find_element_by_xpath(
        '//*[@id="stApp_sendUpdateDoneBtn"]')

    log('Submitting...')

    sleep(PAUSE_AFTER_FILLING)

    done_button.click()

    sleep(PAUSE_AFTER_FILLING)

    return


def fillCP(driver):

    hasButton = True
    try:
        log('Looking for email notification button...')
        emailNotif_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="track-main-content"]/app-track-search-result/main/div[1]/track-page-actions/div/track-emails/a')))

        emailNotif_button.click()
    except:
        pass

    sleep(1)  # Sleep to let the page load the new stuff

    try:
        log('Checking if max emails reached...')
        addMessage_box = driver.find_element_by_xpath(
            '//*[@id="cdk-overlay-0"]/mat-dialog-container/track-email-dialog/div[2]/p/span')
        if 'You’ve reached the maximum of' in addMessage_box.text:
            hasButton = False
    except:
        pass

    try:
        # if email already added, there will be an extra prompt.
        log('Checking for add button...')
        add_button = driver.find_element_by_xpath(
            '//*[@id="cdk-overlay-0"]/mat-dialog-container/track-email-dialog/div[2]/div/div[1]/button')
        add_button.click()
    except:
        pass

    if hasButton:
        log('Filling information...')
        email_box = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH,
             '//*[@id="postal-code-filter"]/form/div[1]/div/div[1]/input')
        ))
        email_box.send_keys('RMA@D2AMICRO.COM')

        save_button = driver.find_element_by_xpath('//*[@id="submitButton"]')

        log('Submitting...')

        save_button.click()

    try:
        complete_message = WebDriverWait(driver, 2).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="cdk-overlay-5"]')
        ))
        if "Sorry" in complete_message.text:
            ok_button = driver.find_element_by_xpath(
                '//*[@id="cdk-overlay-5"]/mat-dialog-container/track-email-dialog/div[2]/result-tmpl/div/mat-dialog-content/div/div/button')
            ok_button.click()
            fillCP(driver)
    except:
        pass

    return


def fillCPX(driver):
    log('Looking for CP button...')
    CP_link = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
        (By.LINK_TEXT, 'Click here to check Canada Post Tracking')
    ))
    CP_link.send_keys(Keys.COMMAND + Keys.ENTER)
    driver.switch_to.window(driver.window_handles[2])
    log('Sending to CP...')
    fillCP(driver)
    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    return


def fillPurolator(driver):

    log('Looking for button...')

    getEmailNotif_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="tracking-detail"]/div[1]/div[8]/button')
    ))

    getEmailNotif_button.click()

    log('Filling information...')

    sleep(1)

    yourName_box = driver.find_element_by_xpath('//*[@id="sender-name-1"]')
    yourName_box.send_keys('deals2you.ca')

    yourEmail_box = driver.find_element_by_xpath('//*[@id="sender-email-1"]')
    yourEmail_box.send_keys('onlinesales@deals2you.ca')

    RecName_box = driver.find_element_by_xpath('//*[@id="recipient-name-1"]')
    RecName_box.send_keys('Kenneth Mau')

    RecEmail_box = driver.find_element_by_xpath('//*[@id="recipient-email-1"]')
    RecEmail_box.send_keys('rma@infonec.com')

    getExceptions_box = driver.find_element_by_xpath(
        '//*[@id="detailed-email-notifs"]/div/div/div[2]/div[4]/div[2]/label')
    getExceptions_box.click()

    submit_button = driver.find_element_by_xpath(
        '//*[@id="subscription-submit"]')

    log('Submitting...')

    submit_button.click()

    sleep(PAUSE_AFTER_FILLING)

    return


def goNextPage(driver):
    global num_page

    hasNext = True
    try:
        pagelinks = driver.find_element_by_class_name('pagelinks')
        pagelinks.find_element_by_link_text('Next').click()
        num_page += 1
    except:
        print("Last page reached")
        hasNext = False

    sleep(1)

    return hasNext


def executeLinks(driver, links):

    failed = []

    for link in links:
        link.send_keys(Keys.COMMAND + Keys.ENTER)
        driver.switch_to.window(driver.window_handles[1])

        sleep(LOADINGTIME)
        log('Determining type...')
        curr_url = driver.current_url

        search_url = curr_url[0:25]

        if 'ups' in search_url:
            try:
                log('Filling UPS...')
                fillUPS(driver)
            except:
                log('FAILED.')
                failed.append(curr_url)
        elif 'canadapost' in search_url:
            try:
                log('Filling Canadapost...')
                fillCP(driver)
            except:
                log('FAILED.')
                failed.append(curr_url)
        elif 'eshipper' in search_url:
            try:
                log('Filling CPX...')
                fillCPX(driver)
            except:
                log('FAILED.')
                failed.append(curr_url)
        elif 'purolator' in search_url:
            try:
                log('Filling purolator')
                fillPurolator(driver)
            except:
                log('FAILED.')
                failed.append(curr_url)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    if failed:
        print("(!!!) Error completing the following ({}):".format(len(failed)))
        for num_fail in range(len(failed)):
            print("({}) {}".format(num_fail + 1, failed[num_fail]))
            failed_links.append(failed[num_fail])

    return


def main():
    global STARTDATE
    global ENDDATE
    global num_links_total
    global num_page

    link_elements = []

    while True:
        STARTDATE = input("Enter start date (YYYY-MM-DD): ")

        ENDDATE = input("Enter end date (YYYY-MM-DD): ")

        if STARTDATE[4] == '-' and ENDDATE[4] == '-' and STARTDATE[7] == '-' and ENDDATE[7] == '-':
            break

        print("::> One of your dates does not follow the correct format. Try again.")

    while True:
        try:
            start_from_order = int(
                input("Start from order (0 = Beginning): "))
            break
        except:
            print('Invalid input.')

    try:

        log('Opening browser...')

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        driver.get('https://web.eshipper.com/login.jsp')

        log('Logging in...')

        username_box = driver.find_element_by_xpath('//*[@id="j_username2"]')
        password_box = driver.find_element_by_xpath('//*[@id="j_password"]')
        login_button = driver.find_element_by_xpath(
            '//*[@id="loginForm"]/div[4]/input')

        username_box.send_keys(eshipper_username)
        password_box.send_keys(eshipper_password)

        login_button.click()

        log('Opening eshipper...')

        # open up tracking page
        driver.get('https://web.eshipper.com/OrderManager.do?method=track')

        log('Looking for orders...')

        specifiedDate_button = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/div[3]/div/form/div[2]/div[1]/div/div/div[1]/div/div[2]/span/label')

        specifiedDate_button.click()

        from_date_box = driver.find_element_by_xpath('//*[@id="f_date_c"]')
        to_date_box = driver.find_element_by_xpath('//*[@id="f_date_e"]')
        submit_ordermanager = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/div[3]/div/form/div[3]/div/input[3]')

        from_date_box.send_keys(STARTDATE)
        to_date_box.send_keys(ENDDATE)
        submit_ordermanager.click()

        run = True
        while run:
            log('Looking for links...')
            link_elements = []
            found = 0

            order_table = driver.find_element_by_id('order_table')

            orders = order_table.find_element_by_tag_name(
                'tbody').find_elements_by_tag_name('tr')

            for order in orders:
                order_columns = order.find_elements_by_tag_name('td')
                status = order_columns[9]
                status_text = status.text.lower()

                if 'in transit' in status_text:
                    if start_from_order > 0:
                        start_from_order -= 1
                    else:
                        link_element = status.find_element_by_tag_name(
                            'a')
                        link_elements.append(link_element)

                    found += 1
                    num_links_total += 1
                elif 'ready for shipping' in status_text:
                    # If it's older than 3 days and it's still ready for shipping, then alert the user.
                    order_num = order_columns[3].text
                    date = order_columns[6].text

                    # Convert to datetime object
                    date = datetime.strptime(date, "%d %b, %Y")

                    # Get difference in time
                    difference = datetime.today() - date

                    if difference.days > 3:
                        print("[WARNING] Order #{} is still 'ready for shipping' after 3 days.".format(
                            order_num))
                        rfs_codes.append(order_num)

            print("Page: {:2} | Found on page: {:2} | Total found: {}".format(
                num_page, found, num_links_total))

            if link_elements:
                log('Opening links...')
                executeLinks(driver, link_elements)

            log('Moving to next page...')
            run = goNextPage(driver)

            sleep(1)
    except:
        input("Error occured. Press enter to exit.")
    finally:
        writeStuffToFile()
        input("::> program finished.")
        driver.quit()

    return


if __name__ == "__main__":
    main()
