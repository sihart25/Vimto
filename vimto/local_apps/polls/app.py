from django.apps import AppConfig

import os
import sys 
# import the logging library
import logging
from django.conf import settings
from Tram.settings import TRAM_CSV_DATA,TRAM_19,TRAM_CSV_HEADER,DIRECTIONS,SENSORS,LOCATIONS
from datetime import datetime
import time 
import re
import csv as csvimporter  
import app.SensorHandler as SensorHandler 

# Get an instance of a logger
logger = logging.getLogger(__name__)

class AppConfig(AppConfig):
    name = 'app'
    verbose_name = "My Application"

    @staticmethod 
    def ReadXMLConfig(): 
       global XMLSensor   
       XMLSensor = SensorHandler.SensorHandler()
       XMLSensor.parse(os.path.join(settings.STATIC_ROOT,'app/TestData','Config.xml')) #a list of all XML
       print(XMLSensor.ChannelTitlesArray)

#    0           1                    2                  3                    4                 5                  6           7         8
# 'Time', 'P2_49_92slot1_ai0','p4_49_75slot1_ai1','P1_48_18slot1_ai2','p3_50_23slot1_ai3','t1_49_16slot2_ai3','Latitude','Longitude','Speed'
# 2016-08-11T08:27:15.984088500,4.42889475333,-3.45222826195,-1.43509783531,1.95329927179,2.89047570136,5234.5045N,00206.2660W,18.33


    @staticmethod 
    def dms2dd(degrees, minutes, seconds, direction):
        dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
        if direction == 'E' or direction == 'N':
            dd *= -1
        return dd;

    @staticmethod 
    def dd2dms(deg):
        d = int(deg)
        md = abs(deg - d) * 60
        m = int(md)
        sd = (md - m) * 60
        return [d, m, sd]

    @staticmethod 
    def parse_dms(dms):
        parts = re.split('[^\d\w]+', dms)
        # lat = dms2dd(parts[0], parts[1], parts[2], parts[3])
        a = parts[0]
        b = parts[1]
        c = parts[2] + "." + parts[3]
        d = parts[4] 
        lat = AppConfig.dms2dd(a,b,c,d)
        return (lat)
     
 # Wolverhampton St George's   
 # 52.584081, -2.124236
 # 52° 35' 2.6916"N 2° 7' 27.2496"W
    def ready(self):
        global TRAM_CSV_DATA
        global TRAM_CSV_HEADER 
        global TRAM_19  
        self.ReadXMLConfig()  
        TRAM_19['name'] = "TRAM 19"  
        TRAM_19['numsensors'] =  5
        strinput = '2016-08-11T08:04:43.308776000'
        date,dt = strinput.split('.')
        timeformat= '%Y-%m-%dT%H:%M:%S' 
        strtme = (time.strptime(date, timeformat))
        TRAM_19['currTime'] = strtme
        TRAM_19['dt'] = int(dt)
        
        #lat, lon = u'5234.5045N,00206.2660W'.split(',') 
        lat  = """52° 35' 2.6916"N"""
        lon  = """2° 7' 27.2496"W"""
        lat_degrees  = self.parse_dms(lat)
        lon_degrees  = self.parse_dms(lon)
        logger.error("AppConfig.ready deg:%s",lat_degrees)
        logger.error("AppConfig.ready deg:%s",lon_degrees)
        TRAM_19['gpslat'] = lat_degrees
        TRAM_19['gpslng'] = lon_degrees
        TRAM_19['estspeed'] = 18.33
        if  not TRAM_CSV_DATA:
            logger.error( 'AppConfig.ready ... ')
            logger.error( 'AppConfig.ready ... Reading ')
            
            #with open(os.path.join(settings.STATIC_ROOT,'app/TestData','Tram19_Data_20160811-080443.4490.csv'), mode='r') as infile:
            with open(os.path.join(settings.STATIC_ROOT,'app/TestData','Tram19_Data_SMALLTEST.csv'), mode='r') as infile:
                reader = csvimporter.DictReader(infile)
                TRAM_CSV_DATA = {}
                numrow = 0
                try: 
                    for row in reader: 
                        hdrnum = 0 
                        for column, value in row.items():
                            TRAM_CSV_DATA.setdefault(column, []).append(value)
                            if numrow == 0:
                                TRAM_CSV_HEADER[hdrnum] = column 
                                hdrnum += 1
                       # if numrow < 10:
                       #     logger.error("%s:%d:%s",column,numrow,TRAM_CSV_DATA[column])
                        numrow = numrow + 1
                except StopIteration:
                    logger.error("AppConfig:All items weren't successful")
                    #raise Exception("All items weren't successful")
        logger.error("%d:%s:",numrow,TRAM_CSV_HEADER)
        logger.error( 'AppConfig.ready ... Loaded ')
        pass # startup code here


