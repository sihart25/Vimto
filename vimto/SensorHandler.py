import xml.etree.ElementTree as ET

class SensorHandler():
    """XML Read of Config for each Sensor class"""

    def __init__(self):
        self.Version = ""
        self.NameSpace = ""
        self.ClusterName = ""
        self.ChannelScaleArray = []
        self.ChannelNamesArray = []
        self.ChannelTypesArray = []
        self.ChannelMAXArray = []
        self.ChannelSensitivityArray = []
        self.ChannelMINArray = []
        self.ChannelIexArray = []
        self.ChannelTitlesArray = []
        self.DataRate = 0
        self.SamplesperRead = 0
        self.NumberofReadstoSave = 0
        self.DataFileName = ""
        self.NumberofChannels = 0
        self.LogContinuously = True
        self.timeout = 0
        self.TermChar = '\t'
        self.baudrate = 9600
        self.databits = 8
        self.parity = 0
        self.stopbits = 0
        self.flowcontrol = 0
        self.VISAresource = ""
        self.DataUserName = ""
        self.Passwd = ""
        self.LocalIP = ""
        self.LocalDirectory = ""
        self.RemoteDirectory = ""
        self.inputterminal = ""
        self.currentexcitationsource = ""
        self.sensitivityunits = ""
        self.units = ""
        self.arraynames=["Channel Scale Array","Channel Names Array","Channel Types Array","Channel MAX Array","Channel Sensitivity Array","Channel MIN Array","Channel Iex Array","Channel Titles Array",]
        self.names= ["Acquisition and Logging","Data Rate (Hz)","Samples per Read","Number of Reads to Save","Data File Name",\
                     "Number of Channels","TDMS Properties","Log Continuously","timeout (10sec)","termination char (0xA = '\n' = LF) ",\
                     "Enable Termination Char (T)","baud rate (9600)","data bits (8)","parity (0:none)","stop bits (10: 1 bit)",\
                     "flow control (0:none)","VISA resource name","String","DataUserName","Passwd","Local IP",\
                     "Local Directory","Remote Directory","input terminal configuration",\
                     "current excitation source","sensitivity units","units",]

    def parse(self, file):
        tree = ET.parse(file)
        root = tree.getroot()
        root = root.find('{http://www.ni.com/LVData}Cluster')
        for child in root.iter():
            self.ParseTAG(child.tag, child.text, child)

        return self

    def characters(self, data):
        self._charBuffer.append(data)

    def ParseTAG(self, tag, text, child):
        if tag == "{http://www.ni.com/LVData}Cluster":
            self.getnameCLUSTRstr(tag, text, child)
        elif tag == "{http://www.ni.com/LVData}NumElts":
            # print("passing:",tag)
            pass
        elif tag == "{http://www.ni.com/LVData}DBL":
            self.getDBLName(tag, text, child)
        elif tag == "{http://www.ni.com/LVData}I32":
            self.getI32NAME(tag, text, child)
        elif tag == "{http://www.ni.com/LVData}String":
            # print("passing:", tag)
            pass
        elif tag == "{http://www.ni.com/LVData}Array":
            self.ArrayName(child)
        elif tag == "{http://www.ni.com/LVData}Boolean":
            # print("passing:", tag)
            pass
        elif tag == "{http://www.ni.com/LVData}U32":
            # print("passing:", tag)
            pass
        elif tag == "{http://www.ni.com/LVData}U8":
            # print("passing:", tag)
            pass
        elif tag == "{http://www.ni.com/LVData}U16":
            # print("passing:", tag)
            pass
        elif tag == "{http://www.ni.com/LVData}EW":
            # print("passing:", tag)
            pass

    def getDBLName(self, tag, text, child):
        if child[0].text == "Data Rate (Hz)":
            self.DataRate = float(child[1].text)

    def getI32NAME(self, tag, text, child):
        if child[0].text == "input terminal configuration":
            self.inputterminal = self.convertinputTerminalConfig(child[1].text)
        elif child[0].text == "current excitation source":
            self.currentexcitationsource = self.convertCurrentExcitationSource(child[1].text)
        elif child[0].text == "sensitivity units":
            self.sensitivityunits = self.ConvertSensitivity(child[1].text)
        elif child[0].text == "units":
            self.units = self.convertUnit(child[1].text)
        elif child[0].text == "Number of Reads to Save":
            self.NumberofReadstoSave = int(child[1].text)
        elif child[0].text == "Samples per Read":
            self.SamplesperRead = int(child[1].text)

    def convertinputTerminalConfig(self, value):
        """ http://zone.ni.com/reference/en-XX/help/370469AC-01/lvdaqmx/mxcreatechannel/ """
        if value == -1:
            return "default"
        elif value == 10106:
            return "Differential"
        elif value == 10078:
            return "NRSE:Non-referenced single-ended mode."
        elif value == 12529:
            return "Pseudodifferential."
        elif value == 10083:
            return "RSE:Referenced single-ended mode."

    def convertCurrentExcitationSource(self, value):
        if value == 10167:
            return "External"
        elif value == 10200:
            return "Internal"
        elif value == 10230:
            return "None"

    def ConvertSensitivity(self, value):
        """ http://zone.ni.com/reference/en-XX/help/370469AG-01/daqmxprop/attr21 """
        if value == 12509:
            return "mVolts/g"
        elif value == 12510:
            return "Volts/g"
        return ""

    def convertUnit(self, value):
        """http://zone.ni.com/reference/en-XX/help/370469AC-01/lvdaqmx/mxcreatechannel/ """
        """ 1 g is approximately equal to 9.81 m/s/s. """
        if value == 10186:
            return "g"

    def getnameCLUSTRstr(self, tag, text, child):
        # print(child[0].text)
        # print(child[1].text)
        pass

    def getDBL(self, tag, text, child):
        # print("getI32:Name",child[0].text)
        # print("getI32:Val",child[1].text)
        pass

    def getI32(self, tag, text, child):
        # print("getI32:Name",child[0].text)
        # print("getI32:Val",child[1].text)
        pass

    def getStr(self, tag, text, child):
        # print("getStr:Name",child[0].text)
        # print("getStr:Val",child[1].text)
        pass

    def ArrayName(self, child):
        # print("getStr:Name", child[0].text)
        name = child[0].text
        if name == "Channel Scale Array":
            self.getChannelScaleArray(child)
        elif name == "Channel Names Array":
            self.getChannelNamesArray(child)
        elif name == "Channel Types Array":
            self.getChannelTypesArray(child)
        elif name == "Channel MAX Array":
            self.getChannelMAXArray(child)
        elif name == "Channel Sensitivity Array":
            self.getChannelSensitivityArray(child)
        elif name == "Channel MIN Array":
            self.getChannelMINArray(child)
        elif name == "Channel Iex Array":
            self.getChannelIexArray(child)
        elif name == "Channel Titles Array":
            self.getChannelTitlesArray(child)

    def getChannelNamesArray(self, child):
            #  <Array>
            #       <Name>Channel Names Array</Name>
            #       <Dimsize>5</Dimsize>
            #       <String>
            #           <Name>String</Name>
            #           <Val>Slot0/ai0</Val>
            #       </String>
            # print("Dimsize:Val", child[1].text)
            k = int(child[1].text)
            # get Dimsize
            for i in range(2, k + 2):
                self.ChannelNamesArray.append(child[i][1].text)

    def getChannelMAXArray(self, child):
        # print("getChannelMAXArray:Dimsize:Val",child[1].text)
        k = int(child[1].text)
        # get Dimsize
        for i in range(2, k + 2):
            self.ChannelMAXArray.append(float(child[i][1].text))

    def getChannelTypesArray(self, child):
            k = int(child[1].text)
            # get Dimsize
            for i in range(2, k + 2):
                self.ChannelTypesArray.append(child[i][1].text)

    def getChannelScaleArray(self, child):
        k = int(child[1].text)
        # get Dimsize
        for i in range(2, k + 2):
            self.ChannelScaleArray.append(float(child[i][1].text))

    def getChannelSensitivityArray(self, child):
        k = int(child[1].text)
        # get Dimsize
        for i in range(2, k + 2):
            self.ChannelSensitivityArray.append(float(child[i][1].text))

    def getChannelMINArray(self, child):
        k = int(child[1].text)
        # get Dimsize
        for i in range(2, k + 2):
            self.ChannelMINArray.append(float(child[i][1].text))

    def getChannelIexArray(self, child):
        k = int(child[1].text)
        # get Dimsize
        for i in range(2, k + 2):
            self.ChannelIexArray.append(float(child[i][1].text))

    def getChannelTitlesArray(self, child):
        k = int(child[1].text)
        # get Dimsize
        for i in range(2, k + 2):
            self.ChannelTitlesArray.append(child[i][1].text)

