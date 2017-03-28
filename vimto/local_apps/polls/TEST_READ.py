import json
import pandas
import sys
import getopt

from django.conf import settings


def functionJSON(CSVfilename):
    # with open("text", "w") as outfile:
    #     json.dump({'numbers':n, 'strings':s, 'x':x, 'y':y}, outfile, indent=4))

    strTitle1 = 'Latitude'
    strTitle2 = 'Longitude'

    csv_file = settings.VIMTO_FILE_EDITED_ROOT+"Tram19_Data_20160811-080443.4490.csv"
    print("opening file:"+csv_file)
    df = pandas.read_csv(csv_file)

    for n in df[strTitle1]:
        for m in df[strTitle2]:
            print("lt:"+n+"lng"+m)


def findClosestStation(lat, lng):
        #  for s in STATIONS:
        #    print("s.lat:"+s.lat+"lng"+s.lng)
    pass


def processArgs(arg):
    pass


def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error as msg:
        print(msg)
        print("for help use --help")
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print (__doc__)
            sys.exit(0)
    # process arguments
    for arg in args:
        processArgs(arg)  # process() is defined elsewhere

    functionJSON("testfile")


if __name__ == "__main__":
    main()
