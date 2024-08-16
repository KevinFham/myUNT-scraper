import pandas as pd
import numpy as np

db = pd.read_csv('./ENG_course_catalog_database.csv')

tarr=np.empty((db.shape[0],50,7),dtype=object)

def tnum_to_dig(number):
    tim = 0
    if number[-2:]=='PM':
        tim += 12
    number=number[:-2].split(':')
    tim += int(number[0])
    off = int(number[1])
    if off > 0:
        tim+=0.5
    if off > 30:
        tim +=0.5
    return int(tim*2)
def ttext_dig(text):
    days = np.array(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'])
    return np.where(text==days)[0][0]
def tnsplit(comb):
    # Splitting text and number in string
    text = ""
    numbers = ""
    x=True
    for i in comb:
        if x:
            if (i.isdigit()):
                numbers += i
                x=False
            else:
                text += i
        else:
            numbers += i
    text = text.split(' ')
    numbers = numbers.split(' to ')
    text = [ttext_dig(x) for x in text]
    numbers = [tnum_to_dig(x) for x in numbers]
    return text,numbers

def dtmask(dt,id):
    dtarr = np.empty((48,6),dtype=object)

    for d in dt[0]:
        dtarr[dt[1][0]:dt[1][1],d]=id
    return dtarr

times = np.linspace(0,23.5,48)

for i in range(db.shape[0]):
    dbi = db.iloc[i]
    tarr[i , 0,1:] = np.array(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'])
    tarr[i, -1,1:] = np.array([dbi['ID'], dbi['Class'], dbi['Name'], dbi['Room'], dbi['Instructor'], dbi['Status']],dtype=object)
    tarr[i,1:-1,0] = times
    if dbi['Room']!='unknown' and dbi['Days and Times']!='None':
        dt = dbi['Days and Times']
        if dt[:len(dt)//2]==dt[len(dt)//2:]:
            dt = dt[:len(dt)//2]
        daytime = tnsplit(dt)
        tarr[i,1:-1,1:] = dtmask(daytime,dbi['ID'])

 # np.savez('cl_mask',clmask=tarr)

uncl=np.unique(tarr[:,-1,1])
unrm=[x for x in  np.unique(tarr[:,-1,4]) if x.startswith('NTDP')]

rm_maz = []
for rm in unrm:
     grz = tarr[np.where(tarr[:,-1,4]==rm)]
     gr = grz[0][:-1]
     gr[0,0] = rm
     for r in grz[1:]:
         r[0]=False
         r[:,0]=False
         gr[np.where(r[:-1])]=r[-1,1]
     rm_maz.append(gr)
rm_maz=np.array(rm_maz)
