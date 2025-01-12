'''
 schedulepacker.py
 - Turns the parsed .csv into several usable numpy arrays and packs them into .npz
 - "class_schedules.npz" holds the Mon-Sat schedule of every class, as well as additional meeting info
 - "room_bookings.npz" holds the schedule of every room at NTDP and what classes are booked when (legacy feature)
'''
import pandas as pd
import numpy as np


db = pd.read_csv('./ENG_course_catalog_database.csv')
tarr = np.empty((db.shape[0], 50, 7), dtype=object)		# Object to store schedule of all classes ("db.shape[0]" entries, each having 50 arrays of length 7)
                                                        # Each entry has 50 arrays representing a class section's schedule. The first array in the entry contains Monday-Saturday
                                                        # labels and the last array contains more class info, such as enrollment numbers and classroom designation

                                                        # The middle 48 arrays are each labeled by incrementing half-hours in their 0th indices. A mask of class
                                                        # blocks is created using the two dimensions, the Mon-Sat labels and the incrementing half-hours


def clocktime_to_float(clocktime):
    digtime = 0
    if int(clocktime[:clocktime.find(':')]) != 12 and clocktime[-2:]=='PM':
        digtime += 12
    clocktime = clocktime[:-2].split(':')
    digtime += int(clocktime[0])
    offset = int(clocktime[1])
    if offset > 0:
        digtime += 0.5
    if offset > 30:
        digtime += 0.5
    return int(digtime * 2)

def weekday_to_digit(text):
    days = np.array(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
    return np.where(text == days)[0]

'''
 dtmask(dt, classid)
 - @dt: An array [@days, @times] of when a class takes place. @days and @times must have been run through clocktime_to_float() and weekday_to_digit() 
 - @classid: The class ID, containing the course ID and section number
 - desc: Create a mask of the 7 day work week based on class meeting time data
'''    
def dtmask(dt,classid):
    dtarr = np.empty((48,6),dtype=object)
    for d in dt[0]:
        dtarr[dt[1][0]:dt[1][1], d] = classid
    return dtarr



if __name__ == '__main__':

    for i in range(db.shape[0]):
        dbi = db.iloc[i]
        tarr[i,0] = np.array([None, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
        tarr[i,-1] = np.array([None, dbi['ID'], dbi['Class'], dbi['Enroll Count'], dbi['Room'], dbi['Instructor'], None],dtype=object)
        tarr[i,1:-1,0] = np.linspace(0,23.5,48)												                                    # Set first index of the 48 middle arrays
                                                                                                                                # to a value between 0.0 and 23.5
        ddays = dbi['Meeting Days']
        dtimes = dbi['Meeting Times']	
        
        #if dtimes[:len(dtimes)//2] == dtimes[len(dtimes)//2:]:			# From old code; might be redundant
        #    dtimes = dtimes[:len(dtimes)//2]
        
        ddays = ddays.split(' ')
        dtimes = dtimes.split(' to ')
        ddays = [weekday_to_digit(x) for x in ddays]
        dtimes = [clocktime_to_float(x) for x in dtimes]
        
        tarr[i,1:-1,1:] = dtmask([ddays, dtimes], dbi['ID'])

    # print(tarr[0])
    np.savez('class_schedules', clmask=tarr)
    

    # Sort by room at NTDP, creating a schedule of every class slot booked for each room
    room_scheds = []
    unique_rooms = [x for x in  np.unique(tarr[:,-1,4]) if x.startswith('NTDP')]        # Only grab if located at NTDP

    for rm in unique_rooms:
        grz = tarr[np.where(tarr[:,-1,4] == rm)]                        # Grab all entries in @tarr that match current unique room
        gr = grz[0][:-1]                                                # Use the first class's entry as a base for the room schedule (omitting the class info in the last array)
        gr[0,0] = rm                                                    # Set the top left of this entry to the Room #

        for r in grz[1:]:                                               # Comb through the rest of the matching room entries for merging
            r[0] = False                                                    # Set Mon-Sat labels to False
            r[:,0] = False                                                  # Set half hour increment labels to False
            gr[np.where(r[:-1])] = r[-1,1]                                  # Merge this entry's and the room schedule base's masks

        room_scheds.append(gr)

    room_scheds = np.array(room_scheds)

    # print(room_scheds[0])
    np.savez('room_bookings', clmask=room_scheds)
    
    
    # Sort by professor, creating a schedule of every professor
    #TODO:
    
    print("Packing Complete")
