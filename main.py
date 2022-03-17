from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options


google_sheets_send = "GOOGLE SHEET LINK TO SEND FORM DATA TO A GOOGLE SHEET"
google_input_form = "GOOGLE SHEET INPUT FORM"

zillow = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_driver_path = "PATH TO CHROME DRIVER"
ser = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=ser)
driver.maximize_window()

def get_zillow_data():
    driver.get(zillow)
    time.sleep(5)

    ### to collect the data and for all the javascript and css to render, we have to scroll down on the web page
    # we will try to emulate scrolling down on the page by pressing the tab key a bunch of times
    action = ActionChains(driver=driver)
    # takes 20 tab clicks to get to get to the housing data part
    for _ in range(20):
        action.key_down(Keys.TAB).perform()
    
    # it's about 2 tab downs per house. So if there are 40 potential listings, then we will tab twice per listing.
    for _ in range(40):
        action.key_down(Keys.TAB).perform()
        action.key_down(Keys.TAB).perform()
    
    # collect the data
    prices = driver.find_elements(by = By.CSS_SELECTOR, value="div.list-card-price") 
    links = driver.find_elements(by = By.CSS_SELECTOR, value="div.list-card-info a.list-card-link") 
    addresses = driver.find_elements(by = By.CSS_SELECTOR, value=".list-card-addr") 

    price_data = []
    # reformat price
    for i in prices:
        price = i.text
        price = price.split("$")[1]
        price = price.replace("1 bd","")
        price = price.replace("2 bd","")
        price = price.replace("/mo","")
        price = price.replace("+","")
        price = price.replace(",","")
        price = price.replace("s","")
        price_data.append(int(price.strip()))

    link_data = []
    for i in links:
        link_data.append(i.get_attribute('href'))

    address_data = []
    for i in addresses:
        address_data.append(i.text)
    


    return [price_data,link_data,address_data]

data = get_zillow_data()


def google_form():

    price_data = data[0]
    link_data = data[1]
    address_data = data[2]

    driver.get(google_input_form)
    time.sleep(1)

    for i in range(len(link_data)):
        address_prompt = driver.find_element(by = By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input') 
        price_prompt = driver.find_element(by = By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input') 
        link_prompt = driver.find_element(by = By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input') 
        submit = driver.find_element(by = By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span') 


        address_prompt.send_keys(address_data[i])
        price_prompt.send_keys(price_data[i])
        link_prompt.send_keys(link_data[i])

        submit.click()
        
        time.sleep(1.5)
        # click the submit another response button
        submit_again = driver.find_element(by = By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
        submit_again.click()

        time.sleep(1)
    
    driver.quit()


google_form()
        
