from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

"""
Arguments: None.
Returns: options, the firefox options object adjusted with the relevant options.

Adds options to the Firefox driver.
Commented line is the option to run the driver in headless mode.
"""


def makefirefoxoptions():
    options = FirefoxOptions()
    # options.add_argument("--headless")
    options.add_argument("interactive")
    return options


"""
Arguments:  driver, the selenium firefox gecko driver.
            urls, the url for the coolblue product page.
            wait, wait object which specifies how long to wait before throwing an error for each action.
Returns: options, the firefox options object adjusted with the relevant options.

Clicks the buttons and fills in the fields needed to buy a product from the specified coolblue url.
"""


def buyfromcoolblue(driver, url, wait):
    driver.get(url)
    accept_cookies_if_exists(driver)

    # logging in
    click_element_by_name(driver, wait, "text()", "Account")
    try:
        click_element_by_name(driver, wait, "@class", "js-show-login-form")
    except:
        print("could not find login button")

    emailfield = driver.find_element(By.XPATH,
                                     "//*[contains(@name, 'emailaddress')]")
    emailfield.send_keys("1ax7vznrk4cx@opayq.com")
    passwordfield = driver.find_element(By.XPATH,
                                        "//*[contains(@name, 'password')]")
    passwordfield.send_keys("%8HSi9LXXyYV%i")

    forms = driver.find_elements(By.XPATH, "//*[contains(@type, 'submit')]")
    inlogbutton = []
    for form in forms:
        if "Inloggen" in form.text:
            inlogbutton.append(form)
    wait.until(EC.element_to_be_clickable(inlogbutton[0]))
    inlogbutton[0].click()
    sleep(5)

    # go back to product page
    driver.get(url)
    sleep(1)

    # add to basket
    click_element_by_name(driver, wait, "@class", "js-order-button")
    click_element_by_name(driver, wait, "text()", "bestellen")

    # This element has extra protection to hide it for the XPATH selector so it must be selected by javascript
    toorderelement2 = driver.find_element(By.XPATH,
                                          "//*[contains(text(), 'Ik ga bestellen')]")
    driver.execute_script("arguments[0].click();", toorderelement2)

    # Onderstaande delen zijn weggehaald omdat een order plaatsen zonder te betalen tegen Coolblue's terms of service is

    # Place order

    # Payment details and processing


'''
Arguments:  driver, the selenium driver object.
            wait, selenium wait object which specifies how long to wait.
            element_type, html object type to search in the div.
            element_name, the name of the object to find.
Returns: None, this method clicks a button so it has no return value.
'''


def click_element_by_name(driver, wait, element_type, element_name):
    addtocartelement = driver.find_element(By.XPATH,
                                           "//*[contains(%s, '%s')]" % (
                                               element_type, element_name))
    wait.until(EC.element_to_be_clickable(addtocartelement))
    addtocartelement.click()
    sleep(1)


'''
Arguments:  driver, the selenium driver object.
Returns: None, this method clicks a button so it has no return value.
'''


def accept_cookies_if_exists(driver):
    cookiebuttons = driver.find_elements(By.NAME, "accept_cookie")
    if cookiebuttons[0]:
        cookiebuttons[0].click()


"""
Arguments:  driver_path, path string to the location of geckodriver.exe.
            wesbites, list of websites to be accessed.
Runs the specific website method based on the url 
"""


def run_and_buy_from_websites(driver_path, websites):
    # driver_path = r"D:\Downloads\geckodriver\geckodriver.exe"
    driver = wd.Firefox(service=Service(driver_path),
                        options=makefirefoxoptions())
    wait = WebDriverWait(driver, 1)
    for website in websites:
        if "coolblue" in website:
            buyfromcoolblue(driver, website, wait)


if __name__ == '__main__':
    driver_path = input(
        "Paste geckodriver Path (e.g. D:\Downloads\geckodriver\geckodriver.exe) : ")
    websites = [
        "https://www.coolblue.nl/product/874077/game-onderweg-pakket-nintendo-switch-rood-blauw.html"]
    run_and_buy_from_websites(driver_path, websites)
