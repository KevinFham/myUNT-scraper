'''
 heatmap.py
'''
import argparse
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import sys, os


f_scheds = np.load('./class_schedules.npz', allow_pickle=True)
master_scheds = f_scheds['clmask']

'''
 schedule_merge(filters=None)
 - @filters: Array of filters for resulting heat map. Schedules' IDs must match at least one of these filters to be shown in the final heat map
             Note: Such filters can be 'BMEN', 'CSCE', 'EENG2', 'EENG3', etc
 - @return: A 2D array (48x6)
 - desc: Produces a 2D array that contains enrollment data per half hour of the days in the Mon-Sat week. Enrollment data can be
         filtered by department in a whitelist fashion
'''
def schedule_merge(filters=None):
    enroll_heatmap = np.zeros((48,6), dtype=int)

    for sched in master_scheds:
        class_id = sched[-1][1]
        enrolled = int(sched[-1][3])

        if filters:
            for filt in filters:
                    if class_id.find(filt) >= 0:
                        break
            else:
                continue

        for i, arr in enumerate(sched[1:-1]):                           	# Set each half hour time block to the enrolled count
            arr = [enrolled if x == class_id else 0 for x in arr]
            enroll_heatmap[i] = np.add(enroll_heatmap[i], arr[1:])      	# And add to head map

    return enroll_heatmap


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Display an aggregated heatmap of class schedules under specific department(s). Has the ability to filter by course ID. Requires class_schedules.npz to have been packed')
    parser.add_argument('filter_args', nargs='*',
                        type=str, 
                        help='whitelist course ids to the heatmap. Example filters: BMEN, CSCE2, CSCE1040, EENG3, etc.')
    parser.add_argument('-s', '--save',
                        action='store_true', 
                        help=f'save figure to a directory specified using --save_dir')
    parser.add_argument('-d', '--save_dir',
                        type=str, default='./',
                        help=f'save figure to a specified directory')
    
    args = parser.parse_args()
    filter_args = args.filter_args
    heatmap_save_dir = os.path.abspath(args.save_dir)

    heatmap = schedule_merge(filters=filter_args)
    df = pd.DataFrame(heatmap, index=np.linspace(0, 23.5, 48), columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',' Saturday'])
    disp = sns.heatmap(df, annot=True, fmt='.4g')               			# Print at 4 significant figures
    disp.set(xlabel="Enrollment Heatmap (filters: " + str(filter_args) + ")", ylabel="Time of Day (24 HR)")
    disp.xaxis.tick_top()
    
    plt.gcf().set_size_inches(20, 18)
    if args.save:
        plt.savefig(heatmap_save_dir)
    else:
        plt.show()

