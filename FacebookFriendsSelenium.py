import unittest
from selenium import webdriver
import re
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
class FaceFriends(unittest.TestCase):
    def setUp(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("dom.webnotifications.enabled", False)
        options = Options()
        # options.add_argument("--headless")
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")


        self.driver=webdriver.Firefox(profile,executable_path='/usr/local/bin/geckodriver')

    def test_facebookfriends(self):
        driver=self.driver
        print(driver.title)


        def login():
            # following 3 lines to wait until elements become visible
            driver.get("https://www.facebook.com")
            email = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id("email"))
            psw = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id("pass"))
            clickbutton = WebDriverWait(driver, 10).until(
                lambda driver: driver.find_element_by_id('loginbutton'))
            username = input("Username")
            password = input('Password:')
            print("checking")
            email.clear()
            email.send_keys(username)
            psw.clear()
            psw.send_keys(password)
            clickbutton.click()

        while(True):
            login()
            try:
                fbLogo = WebDriverWait(driver, 3).until(
                    lambda driver: driver.find_element_by_xpath('(//a[contains(@href, "logo")])[1]'))
                print("You succesfully Logged In")
                break
            except:
                print("Check your username and password and try again!")
                print("Redirecting Login Page")
                continue

        profile = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath("(//div[@dir='ltr'])[1]"))
        driver.execute_script("arguments[0].click();", profile)
        friends=WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath("//html//div[@id='fbTimelineHeadline']//li[3]/a[1]"))
        print(driver.current_url)
        friends.click()
        print("We are checking your friend list it may take 1-2 minutes")
        SCROLL_PAUSE_TIME = 2

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        elements=driver.find_elements_by_xpath("//a[@class='_5q6s _8o _8t lfloat _ohe']")
        print("we found",len(elements),"friends")
        message = input("press enter to see")
        i=0
        for element in elements:
            i+=1
            FACEBOOK_LINK=element.get_attribute('href')
            try:
                regex = re.compile(r'(?<=com/).*?(?=[\\?]fref)')
                match = re.search(regex, FACEBOOK_LINK)
                print("#{}:{}-link:{}".format(i, match.group(), FACEBOOK_LINK))
            except:
                regex = re.compile(r'(?<=id=).*?(?=[\\&]fref)')
                match = re.search(regex, FACEBOOK_LINK)
                print("#{}:{}-link:{}".format(i,match.group(),FACEBOOK_LINK))


    def tearDown(self):
        self.driver.quit()


if __name__=="__main__":
    unittest.main