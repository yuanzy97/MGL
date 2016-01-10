'''
Created on Dec 6, 2015

@author: Anirudh
'''

import csv
import numpy as np
import os
import statistics

year = 2005
buildingname = 'hospital'
location = 'jacksonMS'
aspectname = 'waterheating'
relevant_columns = [10]
signs = [1]




targetfolder = './%s-%s/%s-%s-generalfeatures/' %(buildingname, location,location,aspectname)
if not os.path.exists(os.path.dirname(targetfolder)):
    os.makedirs(os.path.dirname(targetfolder))

with open(targetfolder +'canonicalform-%s.csv' %aspectname,'wb') as process:
    processWriter = csv.writer(process)
    with open('%s-%s.csv' %(buildingname,location),'r') as data:
        dataReader = csv.reader(data)
        header = next(dataReader)
        processWriter.writerow(['Date']+range(25)[1:]) #Date and hours
        row = next(dataReader,None) #first data
        
        while True:
            fullday = [] #24 profile for a day
            if row == None:
                break
            
            date = row[0].split()[0]
            month = date.split('/')[0]
            day = date.split('/')[1]
                        
            fullday.append(date) #day and month
            while row[0].split()[0] == date:  #while we're in the same date
                targetvalue = 0
                for (sign,i) in zip(signs,relevant_columns):
                    targetvalue += sign*float(row[i])
                fullday.append(targetvalue) #append the hourly information for cooling
                row = next(dataReader,None) 
                if row == None:
                    break
            processWriter.writerow(fullday)
            
with open(targetfolder + 'Monthly24hourTotal-%s.csv' %aspectname,'wb') as process:
    processWriter = csv.writer(process)
    processWriter.writerow(['Month']+ range(25)[1:])
    with open(targetfolder +'canonicalform-%s.csv' %aspectname,'r') as data:
        dataReader = csv.reader(data)
        header = next(dataReader)
        row = next(dataReader)
        counter = 0
        while True:
            if row == None:
                break;
            
            date = row[0]
            currmonth = date.split('/')[0]
            monthprofile = []
            while row[0].split('/')[0] == currmonth: #loop over the month
                monthprofile.append(map(float,row[1:]))
                row = next(dataReader,None)
                if row == None:
                    break;
            #monthlyaverageprofile = map(statistics.mean,zip(*monthprofile))
            monthlytotalprofile = np.sum(np.array(monthprofile),axis = 0).tolist()
            processWriter.writerow([currmonth] + monthlytotalprofile)
            

with open(targetfolder + 'AverageForAnHour-%s.csv' %aspectname,'wb') as process:
    processWriter = csv.writer(process)
    processWriter.writerow(['Month','Average for Single Hour'])
    with open(targetfolder +'canonicalform-%s.csv' %aspectname,'r') as data:
        dataReader = csv.reader(data)
        header = next(dataReader)
        row = next(dataReader)
        counter = 0
        while True:
            if row == None:
                break;
            
            date = row[0]
            currmonth = date.split('/')[0]
            monthprofile = []
            while row[0].split('/')[0] == currmonth: #loop over the month
                monthprofile.extend(map(float,row[1:]))
                row = next(dataReader,None)
                if row == None:
                    break;
            monthlyavghourly = statistics.mean(monthprofile)
            processWriter.writerow([currmonth,monthlyavghourly])        

with open(targetfolder+ 'Monthly24hourprofile-%s.csv' %aspectname,'wb') as process:
    processWriter = csv.writer(process)
    processWriter.writerow(['Month']+ range(25)[1:])
    with open(targetfolder +'canonicalform-%s.csv' %aspectname,'r') as data:
        dataReader = csv.reader(data)
        header = next(dataReader)
        row = next(dataReader)
        counter = 0
        while True:
            if row == None:
                break;
            
            date = row[0]
            currmonth = date.split('/')[0]
            monthprofile = []
            while row[0].split('/')[0] == currmonth: #loop over the month
                monthprofile.append(map(float,row[1:]))
                row = next(dataReader,None)
                if row == None:
                    break;
            #monthlyaverageprofile = map(statistics.mean,zip(*monthprofile))
            monthlyaverageprofile = np.mean(np.array(monthprofile),axis = 0).tolist()
            processWriter.writerow([currmonth] + monthlyaverageprofile)    


with open(targetfolder + 'Monthlytop3Profiles-%s.csv' %aspectname,'wb') as process:
    processWriter = csv.writer(process)
    with open(targetfolder +'canonicalform-%s.csv' %aspectname,'r') as data:
        dataReader = csv.reader(data)
        header = next(dataReader)
        row = next(dataReader)
        counter = 0
        while True:
            if row == None:
                break;
            
            date = row[0]
            currmonth = date.split('/')[0]
            monthprofile = []
            while row[0].split('/')[0] == currmonth: #loop over the month
                monthprofile.append(map(float,row[1:]))
                row = next(dataReader,None)
                if row == None:
                    break;
            monthprofile_matrix = np.array(monthprofile)
            normprofile = np.linalg.norm(monthprofile_matrix, axis = 1)
            
            top3_indices = np.argsort(-normprofile)[:3].tolist()
            
            top3months = [monthprofile[i] for i in top3_indices]
            processWriter.writerow([currmonth])
            for topmonth in top3months:
                processWriter.writerow(topmonth)
            
            
            #monthlyavghourly = statistics.mean(monthprofile)
            #processWriter.writerow([currmonth,monthlyavghourly])    


with open(targetfolder + 'AbsoluteMonthlyPeak-%s.csv' %aspectname,'wb') as process:
    processWriter = csv.writer(process)
    processWriter.writerow(['Month','Absolute Peak Hour'])
    with open(targetfolder +'canonicalform-%s.csv' %aspectname,'r') as data:
        dataReader = csv.reader(data)
        header = next(dataReader)
        row = next(dataReader)
        counter = 0
        while True:
            if row == None:
                break;
            
            date = row[0]
            currmonth = date.split('/')[0]
            monthprofile = []
            while row[0].split('/')[0] == currmonth: #loop over the month
                monthprofile.extend(map(float,row[1:]))
                row = next(dataReader,None)
                if row == None:
                    break;
            peakhour = max(monthprofile)
            processWriter.writerow([currmonth,peakhour])    
    