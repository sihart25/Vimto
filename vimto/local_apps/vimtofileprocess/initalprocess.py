'''
Created on  Nov 2016

@author: Simon Hartley
'''
from nptdms import TdmsFile
import sys
import pandas
import numpy
import pynmea2
from calendar import month
import datetime

from polls.StationHandler import STATIONS


class GpsFile:
    """Represents a GPS file with timestamps and NMEA data"""

    def __init__(self, gps_file_name):
        self.index = 0
        self.file = open(gps_file_name, "r")
        firstline = self.file.readline()
        n = firstline.find('$')
        self.datepart = firstline[8:16]
        self.stimepart = firstline[17:28]
        self.timepart = firstline[28:n]
        self.nmeapart = firstline[n:]
        self.file.seek(n)
        self.file.readline()

    def get_next_sentance(self):
        result = [self.datepart, self.timepart, self.nmeapart]
        nextline = self.file.readline()
        n = nextline.find('$')
        self.timepart = nextline[:n]
        self.nmeapart = nextline[n:]
        return result


class vimtoprocessor(object):
    '''
    vimtoprocessor
    '''

    def __init__(self, params):
        '''
        Constructor for vimtoprocessor
        '''
        pass

    def didMove(self, filename):
        return True

    # 'Tram19_Data_gps20161005-060326.9768'
    def getFileDateTime(self, filename):
        # print(filename)
        prefixcount = len('Tram19_Data')
        postfixcount = len('.tdms')
        # print(prefixcount)
        if((prefixcount+prefixcount) < len(filename)):
            timestr = filename[(prefixcount+1):-postfixcount]
            timestr = timestr.split('-')
            # print(timestr)
            year = int(timestr[0][0:4])
            # print("year:",year)
            month = int(timestr[0][4:6])
            # print("month:",month)
            day = int(timestr[0][6:8])
            # print("day:",day)
            hour = int(timestr[1][0:2])
            # print("hour:",hour)
            mins = int(timestr[1][2:4])
            # print("min:",mins)
            sec = int(timestr[1][4:6])
            # print("sec:",sec)
            msec = int(timestr[1][7:])
            # print("msec:", msec)
            # dt = numpy.datetime64(filename[(prefixcount+1):-postfixcount])
            # print(dt)
            filedatetime = datetime.datetime(year, month, day, hour, mins, sec, msec, None)
            # print(filedatetime)
            return filedatetime
        else:
            return "failed"

    def gpsname_from_tdmsname(self, name):
        """Returns a GPS file name given a TDMS file name"""
        return name[:12] + 'gps' + name[12:].replace('.tdms', '.txt')

    def ProcessToCSV(self, tdmsfilename, gpsfilename):

        print('initialprocess.vimtoprocessor.ProcessToCSV')

        if tdmsfilename:
            tdms_file_name = tdmsfilename
        else:
            print("No TDMS file specified.")
            exit()

        # Allow user to specify GPS file, but in general it can be
        # computed. (Older GPS file names had spaces in them.)
        if gpsfilename:
            gps_file_name = gpsfilename
        else:
            gps_file_name = self.gpsname_from_tdmsname(tdms_file_name)

        csv_file_name = tdms_file_name.replace('.tdms', '.csv')
        nmea_file_name = tdms_file_name.replace('.tdms', '.nmea')
        ge_file_name = tdms_file_name.replace('.tdms', '.ge.nmea')

        gps = GpsFile(gps_file_name)
        tdms = TdmsFile(tdms_file_name)
        csv = open(csv_file_name, 'w')
        nmea = open(nmea_file_name, 'w')
        ge = open(ge_file_name, 'w')

        all_channels = tdms.group_channels('Time Domain')
        channels = []

        for channel in all_channels:
            if 'wf_increment' in channel.properties:
                channels.append(channel)
            else:
                continue

        time_track = channels[0].time_track(True)
        date, time, nmeasent = gps.get_next_sentance()
        # gps_time is the DAQ time in the GPS file, not the time as provided GPs
        gps_time = numpy.datetime64(date[0:4] + '-' + date[4:6] + '-' +
                                    date[6:8] + 'T' + time[0:2] + ':' +
                                    time[2:4] + ':' + time[4:])

        lon = ""
        lat = ""
        speed = ""
        gps_stamp = ""
        hdop = ""

        csvhdr = "'Time','GPS Time'"

        for channel in channels:
            csvhdr += "'" + channel.channel + "',"

        csvhdr += "'Latitude','Longitude','Speed','HDOP'"

        csv.write(csvhdr + '\n')

        for i in range(0, len(time_track)):
            tdms_time = time_track[i]

            if (tdms_time > gps_time):
                # print("New NMEA: ", date, time, nmeasent)
                sentence = pynmea2.parse(nmeasent)
                if hasattr(sentence, 'lon'):
                    lon = str(sentence.lon) + sentence.lon_dir
                    lat = str(sentence.lat) + sentence.lat_dir

                if hasattr(sentence, 'spd_over_grnd'):
                    speed = str(sentence.spd_over_grnd)
                elif hasattr(sentence, 'spd_over_grnd_kts'):
                    speed = str(sentence.spd_over_grnd_kts)

                if hasattr(sentence, 'hdop'):
                    hdop = str(sentence.hdop)

                if (sentence.sentence_type == 'ZDA'):
                    gps_stamp = str('{:04d}'.format(sentence.year) + '-' +
                                    '{:02d}'.format(sentence.month) + '-' +
                                    '{:02d}'.format(sentence.day) + 'T' +
                                    "{:%H:%M:%S.%f}".format(sentence.timestamp)[:10])

                nmea.write(str(sentence) + '\r\n')

                if(sentence.sentence_type in ['GGA', 'GLL', 'VTG', 'ZDA', 'RMC']):
                    sentence.talker = 'GP'  # Bodge for Google Earth / other tools
                    ge.write(str(sentence) + '\r\n')  # Recomputes checksum

                date, time, nmeasent = gps.get_next_sentance()
                gps_time = numpy.datetime64(date[0:4] + '-' + date[4:6] + '-' +
                                            date[6:8] + 'T' + time[0:2] + ':' +
                                            time[2:4] + ':' + time[4:])

            csvout = str(tdms_time) + ',' + gps_stamp

            for channel in channels:
                csvout += "," + str(channel.data[i])

            csvout += "," + lat + "," + lon + "," + speed + ',' + hdop
            csv.write(csvout + '\n')

            def CreatePlayFileProcessToCSV(self, csvfilename):
                pass
