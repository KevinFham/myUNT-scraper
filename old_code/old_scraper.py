import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

options = Options()
options.BinaryLocation = "/usr/bin/chromium-browser"


deptartment = ['meen']#'bmen','eeng','meen','mtse','csce'

user = input("enter username")
pword = input("enter Password")

dept = deptartment[0]

# def clinfo(htmlcode):
#
#     course_num = soup.find_all('div', class_='ps_box-value')
#     course_name = soup.find_all('div', class_='ps_box-label')
#     course_name = soup.find_all('div', class_='ps_box-label')
#     course_name = soup.find_all('div', class_='ps_box-label')
#     print(course_name)
#     print(course_num)


driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=options)

driver.get("https://my.unt.edu")
# Locate id and password
time.sleep(2)
id_box = driver.find_element(by=By.ID,value='userid')
pass_box = driver.find_element(by=By.ID,value='pwd')
time.sleep(4)
# Send login information
id_box.send_keys(user)
pass_box.send_keys(pword)

#login button
driver.find_element(by=By.CLASS_NAME,value="btn.btn-block.btn-lg").click()

#rest then enrollment
time.sleep(2)
driver.find_element(by=By.ID,value="PTNUI_LAND_REC_GROUPLET_LBL$2").click()

#rest then class search and enroll
time.sleep(2)
driver.find_element(by=By.ID,value="SCC_LO_FL_WRK_SCC_VIEW_BTN$1").click()

#rest then fall 2022
time.sleep(2)
driver.find_element(by=By.ID,value="win6divSSR_CSTRMCUR_VW_DESCRFORMAL$0").click()

#rest then enter dept
time.sleep(2)
cl_srch = driver.find_element(by=By.ID,value='PTS_KEYWORDS3')
cl_srch.send_keys(dept)
driver.find_element(by=By.ID,value="PTS_SRCH_BTN$IMG").click()

i = 0
while (True):
    # rest then main campus click
    time.sleep(4)
    if driver.find_element(by=By.ID, value="PTS_SELECT$10").is_selected() == False:
        if dept == 'csce':
            time.sleep(10)
        driver.find_element(by=By.ID, value="PTS_SELECT$10").click()
    # rest then remove open class filter
    time.sleep(4)
    if driver.find_element(by=By.ID, value="PTS_SELECT$0").is_selected() == False:
        if dept == 'csce':
            time.sleep(10)
        driver.find_element(by=By.ID, value="PTS_SELECT$0").click()
    try:
        butt="PTS_RSLTS_LIST$0_row_"+str(i)
        time.sleep(5)
        if dept == 'csce':
            time.sleep(20)
        driver.find_element(by=By.ID, value=butt).click()
        time.sleep(3)
        # Storing the page source in page variable
        page = driver.page_source.encode('utf-8')

        #open result.html
        file_ = open("course/"+dept+str(i)+'.html', 'wb')
        # Write the entire page content in result.html
        file_.write(page)
        # Closing the file
        file_.close()
        #clinfo(page)
        time.sleep(2)
        #back to previous page with back()
        driver.back()
        i+=1
    except:
        break
# go back  to search
driver.back()
print(dept + ' done')
driver.close()
