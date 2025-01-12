'''
 htmlparser.py
 - Takes the .html produced by the scraper and parses the important information into a .csv file
 - Requires ./course/ to be populated with scraped html data
'''
from bs4 import BeautifulSoup
import numpy as np
import os
import csv


folder = './course/'
courses = [x for x in os.listdir(folder) if x.endswith('.html')]
courses.sort()

with open('ENG_course_catalog_database.csv', 'w', newline='') as csvfile:
    p_csv = csv.writer(csvfile)
    p_csv.writerow(['ID', 'Class', 'Enroll Count', 'Session', 'Meeting Days', 'Meeting Times', 'Room', 'Instructor'])
    
    for c in courses:
        p_coursefile = open(folder + c)
        soup = BeautifulSoup(p_coursefile, "html.parser")
    
        class_name = soup.find('span', class_='ps_box-value', id='DERIVED_SSR_FL_SSR_SBJ_CAT_NBR').get_text()
        table = soup.find('tr', class_='ps_grid-row').get_text()								# Meeting Information parsing
        table = table.split('\n')
        table = np.array([x for x in table if (x != '' and x != '\xa0')])
        
        #enrolled = soup.find_all('span', class_='ps_box-value', id='DERIVED_SSR_FL_SSR_DTL_FIELD2$0')[-1].get_text()		
        
        enrolled = soup.find_all('tbody', class_='ps_grid-body')[-1].get_text()				    # Enrollment count Information parsing
        enrolled = enrolled.split('\n')												            # Some classes have combined
        enrolled = np.array([x for x in enrolled if (x != '' and x != '\xa0')])
        
        if len(enrolled) > 5:													                # >5 if it has combined class data
            for i, entry in enumerate(enrolled):
                if entry.find(class_name[:class_name.find(' ', 5)]) > -1:						    # Set @enrolled to the enrollment total adjacent to the class section in the table
                    enrolled = enrolled[i + 3]
                    break
            else:
                enrolled = 0														                # In case an enrollment value cannot be found
        else:
            enrolled = enrolled[1]												                # Otherwise grab from the 2nd element

        
        # If class has no meeting time
        if table[0] == 'None' or table[2] == 'None':
            continue 

        p_csv.writerow([c[0:c.find('.')], class_name[class_name.find(' ', 5) + 1:len(class_name)], str(enrolled)] + [x for x in table[:5]])	
        
print("Parsing Complete")		

