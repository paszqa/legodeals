import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
#Count execution time
from datetime import datetime
startTime = datetime.now()

##################################
# CONFIG
##################################
path = "/home/pi/legodeals/"
f = open(path+"allegro.csv", "r")
resultsFilename = 'results'+str(datetime.now()).replace(" ","_")+'.csv'
g = open(path+resultsFilename, "w")
print("Writing to file: "+path+resultsFilename)
g.write("auction_name;website_url;set_id;auction_type;auction_price;new_quantity;new_price;good_deal_new;used_quantity;used_price;good_deal_used;priceZKlockow\n")
g.close()
##################################
# FUNCTIONS
##################################
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

##################################
# SETUP WEB DRIVER
##################################
stageStartTime = datetime.now()
print("Setting up web driver...")
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in headless mode to avoid opening a graphical interface
options.add_argument('--no-sandbox')  # Required for running as root user on Raspberry Pi
options.add_argument('--window-size=800,600')  # Set window size to 800x600 pixels
options.add_argument('--disable-gpu') 
options.add_argument('--mute-audio')
options.add_argument('--disable-notifications')
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.headless = True
driver = webdriver.Chrome('chromedriver', options=options)
stageTime=str(round(datetime.now().timestamp() - stageStartTime.timestamp(),2))
print("Done ("+stageTime+")s")
i = 0
for line in f:
    i += 1
    if i > 10:
        break
    auction_name = line.split(";")[0]
    desired_set_id = line.split(";")[1]
    auction_type = line.split(";")[2]
    auction_price = line.split(";")[3]
    ##################################
    # CHECK IF SET ID IS VALID
    ##################################
    if desired_set_id.isnumeric():
        if int(desired_set_id) < 1:
            continue
    else:
        continue
    ##################################
    # GET WEBSITE AND WAIT
    ##################################
    stageStartTime = datetime.now()
    website_url = "https://www.bricklink.com/v2/search.page?q="+desired_set_id+"-1#T=S"
    print("Getting site from: "+website_url+'')
    try:
        driver.get(website_url)
    except TimeoutException as ex:
       print(ex.Message)
       driver.navigate().refresh()
       continue

    # Wait for specific elements to load, if needed
    wait = WebDriverWait(driver, 10)

    ##################################
    # GET CONTENTS FROM BRICKLINK
    ##################################

    # Find the first <div> with id="_idItemTableForS"
    try:
        div_element = driver.find_element(By.CSS_SELECTOR, 'div#_idItemTableForS')
    except NoSuchElementException:
        print("[ERROR] Element not found")
        continue
    # Find all <td> elements with class="pspItemUsedClick" within the <div>
    new_elements = div_element.find_elements(By.CSS_SELECTOR, 'td.pspItemNewClick')
    new_content_list = [element.get_attribute('innerHTML') for element in new_elements]
    new_content = ";".join(new_content_list)
    new_quantity = new_content.split(";")[2]
    new_price = new_content.split(";")[3].replace("PLN","").replace("+","").replace(" ","").replace("\n","").replace(",","")
    #print(desired_set_id, ";" , new_content)

    # Find all <td> elements with class="pspItemUsedClick" within the <div>
    used_elements = div_element.find_elements(By.CSS_SELECTOR, 'td.pspItemUsedClick')
    used_content_list = [element.get_attribute('innerHTML') for element in used_elements]
    used_content = ";".join(used_content_list)
    used_quantity = used_content.split(";")[2]
    used_price = used_content.split(";")[3].replace("PLN","").replace("+","").replace(" ","").replace(",","")
    good_deal_new = "-"
    good_deal_used = "-"
    if new_price != '-':
        good_deal_new = str(round(float(auction_price) / float(new_price), 2))
    if used_price != '-':
        good_deal_used = str(round(float(auction_price) / float(used_price), 2))
    
    ##################################
    # GET PRICE FROM ZKLOCKOW
    ##################################
    url = "https://zklockow.pl/lego-"+desired_set_id
    response = requests.get(url)
    responseDivided = response.text.split('WraPri">')
    priceZKlockow = "9999"
    good_deal_zKlo = "-"
    if len(responseDivided) > 1:
        if "Produkt aktualnie" not in responseDivided[1]:
            priceZKlockow = responseDivided[1].split('</div>')[0].replace('<span class="pp">','').replace('<span>','').replace('</sup>','').replace('<sup>','').replace('</span>','').replace('od','').replace(' ','').replace("zł",'').split(",")[0]
            if priceZKlockow.isnumeric():
                good_deal_zKlo = str(round(float(auction_price) / float(priceZKlockow), 2))
    
    ##################################
    # PRINT OUTPUT AND SAVE TO FILE
    ##################################
    
    print(auction_name + "; " + website_url + " ;" + desired_set_id + ";" + auction_type + ";" + auction_price.replace("\n","") + ";" + new_quantity + ";" + new_price + ";" + good_deal_new + ";" + used_quantity + ";" + used_price + ";" + good_deal_used + ";" + priceZKlockow + ";" + good_deal_zKlo + "\n")
    g = open(path+resultsFilename, "a")
    g.write(auction_name + "; " + website_url + " ;" + desired_set_id + ";" + auction_type + ";" + auction_price.replace("\n","") + ";" + new_quantity + ";" + new_price + ";" + good_deal_new + ";" + used_quantity + ";" + used_price + ";" + good_deal_used+ ";" + priceZKlockow + ";" + good_deal_zKlo + "\n")
    g.close()
    stageTime=str(round(datetime.now().timestamp() - stageStartTime.timestamp(),2))
    print("Done ("+stageTime+"s)")
##################################
# CLOSE
##################################
f.close()
#g.close()
driver.quit()

