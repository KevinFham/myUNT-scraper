#!/usr/bin/env python3
'''
 roombookingview.py
'''
import argparse
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import sys, os


f_bookings = np.load('./room_bookings.npz', allow_pickle=True)
master_bookings = f_bookings['clmask']

'''
 schedule_merge(filt)
 - @filt: Single filter for the resulting room booking map. Schedules' room numbers must match at least one of these filters to be shown in the final map
      Note: Such filters can be 'NTDP', 'B242', 'B207', 'B1', etc.
      Warning: Some room numbers may still contain "\xa0" within their labels, so be weary of searching for IDs such as 'NTDP B242'
 - desc: Produces a 2D array that contains a schedule of unavailable times per half hour of the days in the Mon-Sat week. Occupancy data can be
         filtered by room in a whitelist fashion
'''
def schedule_merge(filt):
    booking_map = np.array([[0 for x in range(6)] for x in range(48)])
    booking_map_console = np.array([[None for x in range(7)] for x in range(49)])
    booking_map_console[0, 1:] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', ' Saturday']
    booking_map_console[1:, 0] = np.linspace(0, 23.5, 48)
    booking_map_console[0][0] = filt
    
    for booking in master_bookings:
        if filt in booking[0][0]:
        
            for i, arr in enumerate(booking[1:]):
                for j, elem in enumerate(arr[1:]):
                    if elem:
                        booking_map[i][j] = 1
                        booking_map_console[i+1][j+1] = elem

    return booking_map, booking_map_console


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Display a heatmap of class schedules under a specific room. Has the ability to filter via general query. Requires room_bookings.npz to have been packed')
    parser.add_argument('room_id',
                        type=str, 
                        help='room to display scheduled classes. Example arguments: NTDP, B242, B207, B1, etc.')
    parser.add_argument('-s', '--save',
                        action='store_true', 
                        help=f'save figure to a directory specified using --save_dir')
    parser.add_argument('-d', '--save_dir',
                        type=str, default='./',
                        help=f'save figure to a specified directory')

    if len(sys.argv) != 2:
        print("Invalid usage. Use \"python3 " + sys.argv[0] + " --help\" for instructions")
        exit()
        
    args = parser.parse_args()
    bookings_save_dir = os.path.abspath(args.save_dir)

    room_booking, console_output = schedule_merge(args.room_id)
    print(console_output)
    df = pd.DataFrame(room_booking, index=np.linspace(0, 23.5, 48), columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',' Saturday'])
    disp = sns.heatmap(df, annot=False, fmt='.4g') 
    disp.set(xlabel="Room " + sys.argv[1] + " Availability", ylabel="Time of Day (24 HR)")
    disp.xaxis.tick_top()
    
    plt.gcf().set_size_inches(20, 18)
    if args.save:
        plt.savefig(bookings_save_dir)
    else:
        plt.show()
    
