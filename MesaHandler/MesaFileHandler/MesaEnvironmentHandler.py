import os
import re

from MesaHandler.support import *
from MesaHandler.MesaFileHandler.MesaFileInterface import IMesaInterface


class MesaEnvironmentHandler(IMesaInterface):
    def __init__(self):
        IMesaInterface.__init__(self)
        self.mesaDir, self.defaultsDir = self.readMesaDirs(mesa_env)
        for section, file in defaultsFileDict.items():
            fileContent = self.readFile(self.defaultsDir + file)
            self.dataDict[section] = self.getParameters(fileContent)

    def readMesaDirs(self, envVar):
        try:
            mesaDir = os.environ[envVar]
        except KeyError:
            raise EnvironmentError("MESA_DIR is not set in your enviroment. \
                                   Be sure to set it properly!!")
        defaultsDir = mesaDir + defaultsPath

        if not os.path.exists(mesaDir):
            raise FileNotFoundError("Mesa dir " + mesaDir + " does not exist. \
                                    Be sure that it exists on your machine")

        if not os.path.exists(defaultsDir):
            raise FileNotFoundError("Defaults directory " + defaultsDir +
                                    " does not exist.")

        return mesaDir, defaultsDir

    def checkParameter(self, parameter, value=None):
        regex = r'(\w*) (\( [0-9]+ \))'
        x_ctrls = ['x_ctrl', 'x_integer_ctrl', 'x_logical_ctrl']
        for section, paramDict in self.dataDict.items():
            if parameter in paramDict.keys():
                if value is None or type(value) == type(paramDict[parameter]):
                    return section, paramDict[parameter]
                else:
                    raise TypeError("Type of value for parameter " +
                                    parameter + " is wrong, expected type " +
                                    str(type(value)))
            else:
                match = re.search(regex, parameter, re.VERBOSE)
                if(match):
                    prefix = match.group(1)
                    if(prefix in x_ctrls):
                        suffix = '(1:num_x_ctrls)'
                    else:
                        suffix = '(:)'
                    p = prefix + suffix
                else:
                    return "", value

                if(p in paramDict.keys()):
                    if(value is None or type(value) == type(paramDict[p])):
                        return section, paramDict[p]
                    else:
                        raise TypeError('Type of value for parameter ' +
                                        p + ' is wrong, expected type ' +
                                        str(type(value)))                    
            #  to-do: Add exception for controls like x_ctrl(1); these
            #  don't work right now

        return "", value
