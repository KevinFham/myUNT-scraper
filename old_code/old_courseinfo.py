'''
 courseinfo.py
 - Takes the .html produced by the scraper and parses the important information into a .csv file
'''
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import numpy as np
import os


# Input Setup
folder = './course/'
courses = [x for x in os.listdir(folder) if x.endswith('.html')]

# Output Setup
database = np.array(['Option','Status', 'Session', 'Class', 'Meeting Dates', 'Days and Times', 'Room', 'Instructor', 'Seats', 'ID', 'Name'], ndmin=2)
save_file = 'ENG_course_catalog_database'


# Parsing
for c in courses:
#c=courses[1]
#html = urllib.request.urlopen(c).read()

    # Pre setup
    fp = open(folder+c)
    soup = BeautifulSoup(fp, "html.parser")
    
    # Find the course name
    if soup.find('span', class_='ps_box-value', id='SSR_CRSE_INFO_V_SSS_SUBJ_CATLG'):
    
        # Set "Name" to course name in the .csv entry
        id = np.array(soup.find('span', class_='ps_box-value', id='SSR_CRSE_INFO_V_SSS_SUBJ_CATLG').get_text())
        name = np.array(soup.find('span', class_='ps_box-value', id='SSR_CRSE_INFO_V_COURSE_TITLE_LONG').get_text())
        
        # Find the div with all the data we want to collect
        if soup.find('div', class_='ps_box-grid-flex psc_grid-nohbar psc_show-actionable psc_gridlist-standard psc_grid-headernoborder psc_float-clear psc_grid-notitle'):
            table = soup.find('div', class_='ps_box-grid-flex psc_grid-nohbar psc_show-actionable psc_gridlist-standard psc_grid-headernoborder psc_float-clear psc_grid-notitle').get_text()
            
            # Split up entries (TODO: Some sections double up with main and recitation rooms, which break the final csv. Needs further analyzing)
            table = table.split('\n')
            table = np.array([x for x in table if (x != '' and x != '\xa0')])[1:]		#Clean empty entries, non-breaking spaces (\xa0), and get rid of the first entry ('Class Options')
            print(table)
            
            if (np.shape(table)[0] % 9 == 0):
                table = table.reshape((-1, 9))
                course_info = table[1:]
                info=np.array([id,name] * np.shape(course_info)[0]).reshape((-1, 2))
                course_info = np.append(course_info, info, axis=1)
                database = np.append(database, course_info, axis=0)

	# In case there is no div
        else:
            course_info = np.append(np.array(['unknown'] * 9).reshape((1, 9)), np.array([id, name]).reshape((1, 2)), axis=1)
            database = np.append(database, course_info, axis=0)
      
# Save
bd = pd.DataFrame(database[:,1:])
bd.to_csv("{}.csv".format(save_file), mode='a', index=False, header=False, encoding='utf-8')
print('done')
