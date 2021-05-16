import csv
import os
import fitparse
import pytz
import matplotlib.pyplot as plt
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

##### GLOBAL VARIABLES #####
allowed_fields = ['timestamp','power']
required_fields = ['timestamp', 'power']
UTC = pytz.UTC
EST = pytz.timezone('US/Eastern')

##### MAIN #####
def main():
    print('----- Strating App -----')
    print('----- Fetching files in directory -----')
    files = selectFiles()

    print('----- Parsing Data -----')
    data = parseData(files)

    print('----- Plotting Data -----')
    plotData(data)

##### PLOT DATA #####
def plotData(data):
    power0 = []
    power1 = []
    timestamp0 = []
    timestamp1 = []
    for item in data[0].get('data'):
        power0.append(item['power'])
        timestamp0.append(item['timestamp'])
    for item in data[1].get('data'):
        power1.append(item['power'])
        timestamp1.append(item['timestamp'])

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    # ax1.plot(timestamp0, power0, label=data[0].get('file'))
    ax1.plot(timestamp1, power1, label=data[1].get('file'))
    ax1.plot(timestamp0, power0, label=data[0].get('file'))
    plt.legend(loc='upper left');
    plt.show()

##### SELECT FILES #####
def selectFiles():
    fit_files = []
    files_list = []
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename1 = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    filename2 = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    fit_files.append(filename1)
    fit_files.append(filename2)
    for file in fit_files:
        fitfile = fitparse.FitFile(file,  
            data_processor=fitparse.StandardUnitsDataProcessor())
        files_list.append({'fitfile':fitfile, 'file':file})
    return files_list

##### PARSE DATA #####
def parseData(fitfiles):
    retVal = []
    for fitfile in fitfiles:
        messages = fitfile.get('fitfile').messages
        data = []
        for m in messages:
            skip=False
            if not hasattr(m, 'fields'):
                continue
            fields = m.fields
            #check for important data types
            mdata = {}
            for field in fields:
                if field.name in allowed_fields:
                    if field.name=='timestamp':
                        mdata[field.name] = UTC.localize(field.value).astimezone(EST)
                    else:
                        mdata[field.name] = field.value
            for rf in required_fields:
                if rf not in mdata:
                    skip=True
            if not skip:
                data.append(mdata)

        retVal.append({'data':data, 'file':fitfile.get('file')})
    return retVal


if __name__=='__main__':
    main()