'''
Created on Nov 10, 2015

@author: Anirudh
'''
import csv
import os
import numpy

description = 'UMMC'
aspect = 'POI'
rel_index = 1
coefficient = 2

skipnumber = 6

targetfolder = './%s-solar/' %description
if not os.path.exists(os.path.dirname(targetfolder)):
    os.makedirs(os.path.dirname(targetfolder))

with open(targetfolder + 'canonicalform-%s-%s.csv' %(description,aspect),'wb') as process:
    processWriter = csv.writer(process)
    processWriter.writerow(['Date'] + range(25)[1:])
    with open('%s-solar.csv' %description,'r') as data:
        dataReader = csv.reader(data)
        for i in range(skipnumber):
            next(dataReader)
        row = next(dataReader)
        while True:
            date = row[0].split(',')[0]
            fullday = [date]
            while row[0].split(',')[0] == date:
                fullday.append(row[rel_index])
                row = next(dataReader,None)
                if row == None:
                    break
            processWriter.writerow(fullday)
            if row == None:
                break
            
with open(targetfolder + '%s-%s-DERCAM.csv' %(description,aspect),'wb') as process:
    processWriter = csv.writer(process)
    processWriter.writerow(['Month'] + range(25)[1:]+['Number of counted days','Total no. of days in month'])
    with open(targetfolder + 'canonicalform-%s-%s.csv' %(description,aspect),'r') as data:
        dataReader = csv.reader(data)
        next(dataReader) #skip header
        row = next(dataReader)
        while True: 
            month = row[0].split()[0] 
            monthprofile = []
            while row[0].split()[0] == month:
                monthprofile.append(map(float,row[1:25]))
                row = next(dataReader,None)
                if row ==None:
                    break
            
            array_monthprofile = numpy.asarray(monthprofile)
            mean_monthprofile = numpy.mean(array_monthprofile,axis = 0)
            mean_atnoon = mean_monthprofile[11]
            #print mean_atnoon
            stdev_atnoon= numpy.std(array_monthprofile[:,11])
            #print stdev_atnoon
            threshold1 = mean_atnoon + coefficient*stdev_atnoon
            threshold2 = mean_atnoon - coefficient*stdev_atnoon
            #print threshold1
            #print threshold2
            #print "\n"
            
            distinguished_monthprofile = []
            for day in monthprofile:
                array_day = numpy.asarray(day)
                if array_day[11] <threshold1 and array_day[11] >threshold2:
                    distinguished_monthprofile.append(day)
            
            mean_actualmonthprofile = numpy.mean(numpy.asarray(distinguished_monthprofile),axis=0)
            processWriter.writerow([month]+ mean_actualmonthprofile.tolist()+[len(distinguished_monthprofile),len(monthprofile)])
            if row == None:
                break;

        
