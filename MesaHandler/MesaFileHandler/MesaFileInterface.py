import re
from collections import OrderedDict

from MesaHandler.support import *


class IMesaInterface:

    def __init__(self):
        self.dataDict = OrderedDict()

    def getParameters(self, text):
        parameters = OrderedDict()
        p = re.compile(regex_read_parameter, flags=re.MULTILINE)

        for matches in p.findall(text):
            if len(matches) != 2:
                raise AttributeError("Regex needs to match 2 items here! \
                                      Found " + str(len(matches)))

            parameters[matches[0]] = self.convertToPythonTypes(matches[1])

        return parameters

    def convertToPythonTypes(self, data):
        rx = re.compile(regex_floatingValue, re.VERBOSE)
        if data[0] == "." and data[-1] == ".":  # return boolean
            return True if data[1:-1] == "true" else False
        elif data[0] == "'":  # return string
            return data[1:-1]
        elif rx.match(data) is not None:
            matches = rx.findall(data)[0]
            if(matches):
                matches = matches.replace('d', 'e')
                matches = matches.replace('D', 'E')
            return float(matches)
        elif "." in data:
            return float(data)
        else:
            try:
                return int(data)
            except:
                raise AttributeError("Cannot convert " + data + 
                                     " to known type!")

    def convertToFortranType(self, data):
        if isinstance(data, bool):
            return "." + ("true" if data else "false") + "."
        elif isinstance(data, str):
            return "'" + data + "'"
        elif isinstance(data, float) or isinstance(data, int):
            if(isinstance(data, int)):
                datastr = '{:.0f}'.format(data)
            else:
                datastr = '{:.4E}'.format(data)
                if(int(datastr[-1]) >= 2 or int(datastr[-2]) != 0):
                    datastr = datastr.replace('E', 'd')
                    if('+' in datastr):
                        datastr = datastr.replace('+', '')
                    if(int(datastr[-2]) == 0):
                        datastr = datastr[:-2] + datastr[-1:]
                else:
                    datastr = str(data)
            return datastr
        else:
            raise AttributeError("Cannot convert type " + str(type(data)) +
                                 "to known type")

    def readFile(self, fileName):
        with open(fileName) as f:
            return f.read()

    def writeFile(self, fileName, content):
        with open(fileName, 'w') as f:
            f.write(content)

    def items(self):
        return self.dataDict.items()

    def keys(self):
        return self.dataDict.keys()

    def __getitem__(self, item):
        return self.dataDict[item]

    def __setitem__(self, key, value):
        raise NotImplementedError("Please implement the setItem Method!")
