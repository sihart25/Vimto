

class Station():
    def __init__(self, num, lat, lng, nme):
        self.num = num
        self.nme = nme
        self.lat = lat
        self.lng = lng

#########################################################################
# Settings
STATIONS = {}
STATIONS[0] = Station(0, 52.478732, -1.899240, 'Grand Central New Street')
STATIONS[1] = Station(1, 52.479932, -1.897152, 'Corporation Street')
STATIONS[2] = Station(2, 52.481887, -1.896281, 'Bull Street')
STATIONS[3] = Station(3, 52.483556, -1.899273, 'Birmingham, Snow Hill')
STATIONS[4] = Station(4, 52.486663, -1.903911, 'St. Pauls')
STATIONS[5] = Station(5, 52.489686, -1.913182, 'Jewellery Quarter')
STATIONS[6] = Station(6, 52.496907, -1.931041, 'Soho, Benson Road')
STATIONS[7] = Station(7, 52.498867, -1.938733, 'Winson Green, Outer Circle')
STATIONS[8] = Station(8, 52.502373, -1.951652, 'Handsworth, Booth Street')
STATIONS[9] = Station(9, 52.505723, -1.964655, 'The Hawthorns')
STATIONS[10] = Station(10, 52.508779, -1.982677, 'Kenrick Park')
STATIONS[11] = Station(11, 52.511784, -1.988073, 'Trinity Way')
STATIONS[12] = Station(12, 52.516604, -1.994781, 'West Bromwich Central')
STATIONS[13] = Station(13, 52.518639, -1.999724, 'Lodge Road, West Bromwich Town Hall')
STATIONS[14] = Station(14, 52.520463, -2.004534, 'Dartmouth Street ')
STATIONS[15] = Station(15, 52.525122, -2.008589, 'Dudley Street, Guns Village')
STATIONS[16] = Station(16, 52.531002, -2.011202, 'Black Lake')
STATIONS[17] = Station(17, 52.548893, -2.025621, 'Wednesbury, Great Western Street')
STATIONS[18] = Station(18, 52.549482, -2.030593, 'Wednesbury Parkway')
STATIONS[19] = Station(19, 52.555668, -2.057287, 'Bradley Lane')
STATIONS[20] = Station(20, 52.559794, -2.065500, 'Loxdale')
STATIONS[21] = Station(21, 52.565810, -2.074917, 'Bilston Central')
STATIONS[22] = Station(22, 52.567891, -2.080698, 'The Crescent')
STATIONS[23] = Station(23, 52.571903, -2.098076, 'Priestfield')
STATIONS[24] = Station(24, 52.581056, -2.116881, 'The Royal')
STATIONS[25] = Station(25, 52.584081, -2.124243, 'Wolverhampton, St. Georges')


class Section():
    def __init__(self, name, startnum, endnum, dirn, minlat, minlng, maxlat, maxlng, startlat, startlng, endlat,  endlng):
        self.name = name
        self.startnum = startnum
        self.endnum = endnum
        self.section_direction = dirn
        self.minlat = minlat
        self.minlng = minlng
        self.maxlat = maxlat
        self.maxlng = maxlng
        self.startlat = startlat
        self.startlng = startlng
        self.endlat = endlat
        self.endlng = endlng

