'''
 scraper.py
'''
import argparse
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import selenium.common.exceptions as Exceptions
from selenium.webdriver.common.by import By
from random import random
from time import sleep
from warnings import warn
import sys

service = webdriver.ChromeService()
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('disable-infobars')
options.page_load_strategy = 'eager'

'''
 scroll_view_click(wd, elem)
 - desc: The idiot that coded myUNT prevents certain elements from being clickable if outside the current viewable window.
         This command supposedly executes Javascript code to force a specific action
'''
def scroll_view_click(wd, elem):
    wd.execute_script("arguments[0].scrollIntoView(true);", elem)
    elem.click()
    
'''
 myUNT_synchro(wd, timeout=60, quick=False)
 - @wd: webdriver obj
 - @timeout: to prevent infinite looping
 - @quick: choose whether to skip the wait until pointer events are disabled
 - desc: myUNT disables input in HTML by changing the style of the body to "pointer-events: none;". We exploit this
         to synchronize with load times. 
'''
def myUNT_synchro(wd, timeout=60, quick=False):

    clk = 0.0
    print("Awaiting event disable.", end='')
    while clk < timeout:
        try:
            if quick or wd.find_element(by=By.XPATH, value="/html/body").get_attribute("style") in ["pointer-events: none;", "pointer-events: none; overflow: hidden;"]:
                break
            print(".", end='')
        except Exceptions.StaleElementReferenceException:
            print("(Captured stale reference)", end='')
            continue
        sleep(.1)
        clk += .1

    clk = 0.0
    print(" Awaiting event reenable.", end='')
    while clk < timeout:
        try:
            if not wd.find_element(by=By.XPATH, value="/html/body").get_attribute("style") in ["pointer-events: none;", "pointer-events: none; overflow: hidden;"]:
                break
            print(".", end='')
        except Exceptions.StaleElementReferenceException:
            print("(Captured stale reference)", end='')
            continue
        sleep(2)
        clk += 2
    print("")

'''
 clsindept(department)
 - @department: department to search for
 - desc: myUNT Browsing functionality
'''
def clsindept(department):
    course_history = []

    with webdriver.Chrome(service=service, options=options) as driver:
        driver.set_page_load_timeout(10)
        driver.get("https://my.unt.edu")

        # Login with given user and pass
        driver.implicitly_wait(10)
        id_box = driver.find_element(by=By.ID,value='userid')
        pass_box = driver.find_element(by=By.ID,value='pwd')

        id_box.send_keys(USER)
        pass_box.send_keys(PWRD)
        try:
            driver.find_element(by=By.CLASS_NAME,value="btn.btn-block.btn-lg").click()
        except Exceptions.TimeoutException:										# Firefox sometimes freezes at this part
            print("Timeout Warning")


        # "Enrollment" click
        WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="PTNUI_LAND_REC_GROUPLET_LBL$2"))			# Wait for the "Enrollment" button to appear
        driver.find_element(by=By.ID, value="PTNUI_LAND_REC_GROUPLET_LBL$2").click()

        # "Class Search and Enroll" click
        driver.implicitly_wait(10)
        myUNT_synchro(driver)
        driver.find_element(by=By.ID,value="SCC_LO_FL_WRK_SCC_VIEW_BTN$2").click()

        # "FALL/SPRING 20XX" click (THIS HTML ELEMENT WILL BE DIFFERENT EACH SEMESTER)
        driver.implicitly_wait(10)
        myUNT_synchro(driver)
        try:
            driver.find_element(by=By.XPATH, value="//*[contains(text(), \'" + SMSTER + "\')]").click()
        except Exceptions.NoSuchElementException:
            # There is no Academic term of the name SMSTER
            print("No academic term found by the name of", "\"" + SMSTER + "\"")
            exit()

        # Search database for department #*** (# = 1 through 6)
        for course_level in COURSE_LEVEL_RANGE:

            try:
                driver.implicitly_wait(10)
                cl_srch = driver.find_element(by=By.ID,value='PTS_KEYWORDS3')
                print("Querying for", department, str(course_level))
                cl_srch.send_keys(department + " " + str(course_level))
                driver.find_element(by=By.ID,value="PTS_SRCH_BTN$IMG").click()

                # Remove "Open classes" filter, if it exists (see all classes; filter only exists if there exists open classes)
                try:
                    driver.implicitly_wait(0)
                    WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(by=By.XPATH, value="//*[contains(text(),'Open Classes')]"))       # Wait for the "Open Classes" filter button to appear
                    driver.find_element(by=By.XPATH, value="//*[contains(text(),'Open Classes')]").click()
                    myUNT_synchro(driver)
                except Exceptions.TimeoutException:
                    print("No open classes warning")

                # Filter for only Main Campus classes
                driver.find_element(by=By.XPATH, value="//*[contains(text(),'UNT Main Campus')]").click()
                myUNT_synchro(driver)


                # Time to click a shit ton
                i = 0
                while True:
                    print("i=" + str(i))

                    try:
                        # Click on a class in the tracked index
                        butt = "PTS_RSLTS_LIST$0_row_" + str(i)
                        sleep(max(.4 + random(), .9))
                        scroll_view_click(driver, driver.find_element(by=By.ID, value=butt))
                        myUNT_synchro(driver)
                            
                        course_name = driver.find_element(By.ID, 'SSR_CRSE_INFO_V_SSS_SUBJ_CATLG').text				    # For creating the file name
                        course_name = course_name.replace(' ', '')

                        # Individually click on every Section hyperlink (contains meeting info and exact class enrollment totals)
                        j = 0
                        has_recit = True
                        while True:
                                
                            # Try clicking through sections until out of bounds
                            try:

                                # First, check if the class has no meeting period (Days and Times = 'None')
                                print("Searching for section", j + 1)
                                if driver.find_element(by=By.ID, value="SSR_CLSRCH_F_WK_SSR_MTG_SCHED_L_1$134$$" + str(j)).text == 'None':
                                    print("No meeting session; skipping subsequent checks")
                                    break                                                                                   # Do not continue search loop; return to search results
                                    

                                # Open main section (i.e., Lecture class)
                                sleep(max(.4 + random(), .9))
                                section_html = "SSR_CLSRCH_F_WK_SSR_CMPNT_DESCR_1$294$$" + str(j)
                                
                                try: 												# Timing Optimization (doesnt work?)
                                    driver.implicitly_wait(0)
                                    WebDriverWait(driver, timeout=0).until(lambda d: d.find_element(by=By.ID, value=section_html))
                                except Exceptions.TimeoutException:
                                    raise Exceptions.NoSuchElementException
                                
                                section_number = driver.find_element(by=By.ID,value=section_html).text[8:11]			# For creating the file name ('Section ### - Class Nbr #####')
                                course_uid = ''.join(filter(str.isdigit, course_name)) + section_number

                                # Skip courses already recorded
                                if course_uid in course_history:
                                    print(course_name, section_number, "already recorded, skipping")
                                else:
                                    course_history.append(course_uid)
                                    print(course_name, section_number, "found")
                                    scroll_view_click(driver, driver.find_element(by=By.ID, value=section_html))

                                    # A <form> will be layed on top of another <form> within an <iframe>; switch to this <iframe>
                                    WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(by=By.XPATH, value="//iframe[@title='Course Information Popup window']"))	# Wait for iframe
                                    sleep(1)
                                    iframe = driver.find_element(by=By.XPATH, value="//iframe[@title='Course Information Popup window']")
                                    driver.switch_to.frame(iframe)								    # Switch
                                    myUNT_synchro(driver, quick=True)								# Switched context; "/html/body" XPATH is corrected

                                    # Open "Meeting Information" and save HTML data
                                    driver.find_element(by=By.XPATH, value="//*[contains(text(),'Meeting Information')]").click()
                                    myUNT_synchro(driver, quick=True)
                                    page = driver.page_source.encode('utf-8')
                                    file_ = open("course/" + course_name + "_" + section_number + '.html', 'wb')
                                    file_.write(page)

                                    # Open "Class Availability" and save HTML data
                                    driver.find_element(by=By.XPATH, value="//*[contains(text(),'Class Availability')]").click()
                                    myUNT_synchro(driver, quick=True)
                                    page = driver.page_source.encode('utf-8')
                                    file_.write(page)
                                    file_.close()

                                    # Close out of section
                                    driver.find_element(by=By.ID, value="#ICCancel").click()					# X button
                                    driver.switch_to.default_content()								# Switch out of iframe context
                                    sleep(1)
                                    myUNT_synchro(driver, quick=True)

                                sleep(1)
                                
                                
                                # Only try finding a recitation section if it exists, otherwise skip (if one section does not have a recitation section, assuming all sections dont have it)
                                if has_recit:
                                    try:
                                        # Open secondary section (i.e., Recitation)
                                        section_html = "SSR_CLSRCH_F_WK_SSR_CMPNT_DESCR_2$295$$" + str(j)
                                        
                                        try: 												# Timing Optimization (doesnt work?)
                                            driver.implicitly_wait(0)
                                            WebDriverWait(driver, timeout=0).until(lambda d: d.find_element(by=By.ID, value=section_html))
                                        except Exceptions.TimeoutException:
                                            raise Exceptions.NoSuchElementException
                                        
                                        section_number = driver.find_element(by=By.ID,value=section_html).text[8:11]		# For creating the file name ('Section ### - Class Nbr #####')
                                        course_uid = ''.join(filter(str.isdigit, course_name)) + section_number

                                        # Skip courses already recorded
                                        if course_uid in course_history:
                                            print(course_name, section_number, "already recorded, skipping")
                                        else:
                                            course_history.append(course_uid)
                                            print(course_name, section_number, "found")
                                            scroll_view_click(driver, driver.find_element(by=By.ID, value=section_html))
                                        
                                            # A <form> will be layed on top of another <form> within an <iframe>; switch to this <iframe>
                                            WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(by=By.XPATH, value="//iframe[@title='Course Information Popup window']"))	# Wait for iframe
                                            iframe = driver.find_element(by=By.XPATH, value="//iframe[@title='Course Information Popup window']")
                                            driver.switch_to.frame(iframe)								    # Switch
                                            myUNT_synchro(driver, quick=True)							    # Switched context; "/html/body" XPATH is corrected

                                            # Open "Meeting Information" and save HTML data
                                            driver.find_element(by=By.XPATH, value="//*[contains(text(),'Meeting Information')]").click()
                                            myUNT_synchro(driver, quick=True)
                                            page = driver.page_source.encode('utf-8')
                                            file_ = open("course/" + course_name + "_" + section_number + '.html', 'wb')
                                            file_.write(page)

                                            # Open "Class Availability" and save HTML data
                                            driver.find_element(by=By.XPATH, value="//*[contains(text(),'Class Availability')]").click()
                                            myUNT_synchro(driver, quick=True)
                                            page = driver.page_source.encode('utf-8')
                                            file_.write(page)
                                            file_.close()

                                            # Close out of section
                                            driver.find_element(by=By.ID, value="#ICCancel").click()					# X button
                                            driver.switch_to.default_content()								# Switch out of iframe context
                                            sleep(1)
                                            myUNT_synchro(driver, quick=True)
                                            
                                    except Exceptions.NoSuchElementException:
                                        print("No recitation section; skipping recitation checks")
                                        has_recit = False
                                
                            except Exceptions.NoSuchElementException:
                                # Notify in terminal
                                print(course_name, "complete")
                                break
                                
                            j += 1

                        sleep(1)

                        # Back to search results (while reserving myUNT table integrity)
                        print("Returning to Search Results")
                        driver.find_element(by=By.ID, value="PT_WORK_PT_BUTTON_BACK$IMG").click()
                        WebDriverWait(driver, timeout=40).until(lambda d: d.find_element(by=By.XPATH, value="//*[contains(text(),'UNT Main Campus')]"))       # Wait specifically for the "Main Campus" filter to appear
                        myUNT_synchro(driver, quick=True)
                        i += 1
                    except Exceptions.TimeoutException:
                        print("Timeout Warning")
                        continue
                    except Exceptions.NoSuchElementException:
                        # Continue to next course level
                        print("Finished", department, str(course_level) + "***")
                        break

                # Go back to class search to continue to next course level
                print("Searching for next course level")
                driver.find_element(by=By.ID, value="PT_WORK_PT_BUTTON_BACK$IMG").click()
                myUNT_synchro(driver)

            except Exceptions.NoSuchElementException:
                # Likely due to no #*** level classes in the department. Continue.
                print("No classes in", department, str(course_level) + "***")
                driver.find_element(by=By.ID, value="PT_WORK_PT_BUTTON_BACK$IMG").click()
                myUNT_synchro(driver)
                continue

    print(department + ' done')
    return



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Automated web scraper of myUNT for course data. Saves .html files to the ./course/ directory for parsing')
    parser.add_argument('departments', nargs='+',
                        type=str, 
                        help='course department(s) to search by. Example queries: CSCE, EENG, INFO, MTSE, ART, etc.')
    parser.add_argument('-u', '--username',
                        type=str, 
                        help='myUNT username')
    parser.add_argument('-t', '--academic_term',
                        type=str, 
                        help='academic term to search by, in quotations. Example queries:  \"2023 Fall\", \"2024 Spring\". Must be available to select in Class Search and Enroll')
    parser.add_argument('-x', '--range_minimum',
                        type=int, default=21,
                        help='minimum course id query range (e.g., 21 == CSCE 21XX)')
    parser.add_argument('-y', '--range_maximum',
                        type=int, default=79,
                        help='minimum course id query range (e.g., 79 == CSCE 79XX)')  
                                  

    args = parser.parse_args()
    if len(sys.argv) == 1:
        print("Invalid usage. Use \"python3 " + sys.argv[0] + " --help\" for instructions")
        exit()
    if args.username:
        USER = args.username
    else:
        USER = input("Enter UNT User: ")

    PWRD = getpass("Enter Password: ")

    if args.academic_term:
        SMSTER = args.academic_term
    else:
        SMSTER = input("Enter Academic Term (e.g., \"2023 Fall\", \"2024 Spring\". Must be available to select in Class Search and Enroll): ")

    DEPARTMENTS = args.departments
    COURSE_LEVEL_RANGE = range(args.range_minimum, args.range_maximum)	# 21 through 79 is extremely thorough and redundant, but reliably consistent as of Fall2024

    for d in DEPARTMENTS:
        clsindept(d)
