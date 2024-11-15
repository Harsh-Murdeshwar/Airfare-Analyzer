import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome import options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import dill

CODES = ["IXA","AGX","AGR","AMD","AJL","ATQ","IXU","AYJ","IXB","BEK","IXG","BLR","BHO","BBI","IXC","MAA","CJB","DBR","DED","DEL","DGH","DHM","DIB","DMU","DIU","RDP","GAY","GOI","GDB","GOP","GAU","GWL","HSR","HBX","HYD","IMF","IDR","HGI","JLR","JGB","JAI","JSA","IXJ","JRG","JDH","JRH","CDP","CNN","KNU","HJR","COK","KLH","CCU","CCJ","KJB","IXL","LKO","IXM","IXE","BOM","MYQ","NAG","ISK","GOX","PGH","PAT","IXZ","IXD","PNQ","RPR","RJA","RAJ","IXR","SXV","SHL","SAG","RQY","IXS","SXR","STV","TRV","TRZ","TIR","TCR","UDR","BDQ","VNS","VGA","VTZ"]

def press_tab():
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB)
    actions.perform()
    time.sleep(1)

def press_esc():
    actions = ActionChains(driver)
    actions.send_keys(Keys.ESCAPE)
    actions.perform()
    time.sleep(1)
    
def get_today_date():
    xpath = "//*[@aria-label='Departure']"
    date = driver.find_element(By.XPATH, xpath)
    return date.get_attribute("value")[0:3]

def get_next_date():    
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/div[3]/button'))
            )

            # Click the button
            button.click()

            time.sleep(5)
            
def get_count(from_city, to_city):
    global driver
    global counter
    
    # Open URL
    url = "https://www.google.com/travel/flights/search?tfs=CBwQAhomEgoyMDI0LTExLTEwKABqBwgBEgNCT01yDQgCEgkvbS8wMjJ0cTRAAUgBcAGCAQsI____________AZgBAg&tfu=EgYIAhAAGAA"
    driver.get(url)
    time.sleep(1)
    
    # Fill From
    from_box_xp = "//*[@aria-label='Where from? Mumbai BOM']" 
    from_box = driver.find_element(By.XPATH, from_box_xp)

    from_box.send_keys("\b"*100 + from_city)
    time.sleep(1)
    press_tab()
    press_tab()
    
    # Fill To
    to_box_xp = "//*[@aria-label='Where to?']" 
    to_box = driver.find_element(By.XPATH, to_box_xp)

    to_box.send_keys("\b"*100 + to_city)
    time.sleep(1)
    press_tab()
    press_tab()
    time.sleep(1)
    press_esc()
    
    for ix in range(7):
        # Get Count
        try:
            h3_element = driver.find_element(By.XPATH, '//h3[text()="All flights"]')
            ul_element = h3_element.find_element(By.XPATH, 'following-sibling::ul')
            li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
            li_count = len(li_elements)
        except Exception as e:
            li_count = 0
        day = get_today_date()
        
        # Update
        info = from_city, to_city, day
        counter[info] = li_count
        print(info, li_count)
        
        # Next
        get_next_date()
    
driver = webdriver.Chrome()
driver.maximize_window()
counter = {}
for from_city in CODES:
    for to_city in CODES:
        if from_city!=to_city:
            get_count(from_city, to_city)
            
with open('data.dill', 'wb') as f:
    dill.dump(counter, f)