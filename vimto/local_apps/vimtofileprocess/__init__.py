from django.conf import settings
import sys
from polls.StationHandler import STATIONS


def func():

    if (settings.DEBUG is True):
        print("func() in vimtofileprocess.__init__.py")

if (settings.DEBUG is True):
    print("top-level in vimtofileprocess.__init__.py")

if __name__ == "__main__":
    if (settings.DEBUG is True):
        print("vimtofileprocess.__init__.py is being run directly")

else:

    if (settings.DEBUG is True):
        print("vimtofileprocess.__init__.py is being imported into another module")
