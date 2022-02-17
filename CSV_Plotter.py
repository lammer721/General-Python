import matplotlib.pyplot as plt
import pandas as pd
#import numpy as np
from pathlib import Path

#prompt the user to input the file name and path name to be used in the program
while True:
    try:
        pathName = input("Type in the pathname where the data file is located:")
        dataDir = Path(pathName)
        filename = input("Type in the name of the file, excluding the file extension (.csv):")
        filename = filename + ".csv"
        fullName = dataDir / filename
        data = pd.read_csv(fullName,',',header=None, names=['Time (s)', 'HX_1', 'HX_5', 'HX_3', 'HX_6', 'HX_4'], low_memory=False)
        break
    except:
        print("The file was not found, or the file extension is not valid.  Please try again.")

df = pd.DataFrame(data)

#typecast the data as a floating point
df = df.astype(float)

#df.columns = df.columns.str.replace('rel_time_sec','Time (s)')

#strip leading whitespace since it seems to be inconsistent in the data files
#df.columns = df.columns.str.lstrip()

df.set_index('Time (s)')

HX_1 = 'HX_1'
HX_5 = 'HX_5'
HX_3 = 'HX_3'
HX_6 = 'HX_6'
HX_4 = 'HX_4'

#to select a column (series), you can manipulate and index this data
#here, we find the max current, max temp, and time that the max current occurs

#for index, row in df.iterrows():
 #   if abs(df.at[row,actRes] - df.at[row+10,actRes])>0.001:

fig = plt.figure()
fig.set_size_inches(15,10)
#define each subplot
ax1 = fig.add_subplot(2,3,1)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('HX_1')

ax2 = fig.add_subplot(2,3,2)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('HX_5')

ax3 = fig.add_subplot(2,3,3)
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('HX_3')

ax4 = fig.add_subplot(2,3,4)
ax4.set_xlabel('Time (s)')
ax4.set_ylabel('HX_6')

ax5 = fig.add_subplot(2,3,5)
ax5.set_xlabel('Time (s)')
ax5.set_ylabel('HX_4')

ax6 = fig.add_subplot(2,3,6)
ax6.set_xlabel('HX_6')
ax6.set_ylabel('HX_3')

#plot what we want to plot, and set the linewidth=.25 (default 1.5)
#the next command was used to fix an issue when the data being plotted is too dense. this will force it
plt.rcParams['agg.path.chunksize'] = 10000
plt.rc('lines', linewidth=.25)

ax1.plot(df['Time (s)'],df[HX_1], color='r')

ax2.plot(df['Time (s)'],df[HX_5])

ax3.plot(df['Time (s)'],df[HX_3])

ax4.plot(df['Time (s)'],df[HX_6])

ax5.plot(df['Time (s)'],df[HX_4], label='Probably ded')

ax6.plot(df[HX_6],df[HX_3])

#display the plot
#title the full figure
plt.suptitle(fullName)
#save the figure (uncomment if needed)
#plt.savefig('Name.png')
plt.show()