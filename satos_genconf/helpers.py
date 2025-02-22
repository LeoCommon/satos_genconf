import os
import sys
import configparser
from .devices import *

MOCK_FOLDER = 'mock'
MOCK_RAUC_CONFIG = os.path.join(MOCK_FOLDER, "rauc-config.ini")

class RaucConfig:
    # Available device compatible strings, keep in sync with added devices!
    COMPAT_STRING_RPI3 = 'satos-rpi3-64'
    COMPAT_STRING_RPI4 = 'satos-rpi4-64'
    COMPAT_STRING_RPI5 = 'satos-rpi5-64'

    DEFAULT_CONFIG_LOCATION = str("/etc/rauc/system.conf")
    config = None | configparser.ConfigParser

    def _is_open(self):
        if not self.config:
            raise ValueError('No config to operate on!')

    # Open the rauc config file at the specified path
    def open(self, path: str):
        conf = configparser.ConfigParser()
        fRead = conf.read(path)
        if not fRead:
            raise ValueError(f"Rauc config file at {path} not found.")

        self.config = conf

    # Grabs the compatible string from the RAUC config
    def compatible(self) -> str: 
        self._is_open()
        
        return str(self.config['system']['compatible'])

    def __init__(self, config = DEFAULT_CONFIG_LOCATION) -> None:
        self.open(config)
    
class DeviceInfo:
    rauc = RaucConfig | None
    MOCK = False

    dev = Device

    # This fetches the RAUCs compatible string, we rely on the right software being present
    def getCompatible(self) -> str:
        return self.rauc.compatible()

    # This fetches the actual model name of the device!
    def model(self) -> str:
        return self.dev.model()

    # Returns the product name, atm theres only one
    def product(self) -> str:
        return "LeoCommon-GroundStation"

    def hw_revision(self) -> str:
        print("Warning: hardware revision is not implemented")
        return "NOT_IMPLEMENTED"

    # Get serial number
    def serialnumber(self) -> str:
        return self.dev.serial()
    
    def __detectDevice(self) -> Device:
        compatibleString = self.getCompatible()

        if compatibleString == RaucConfig.COMPAT_STRING_RPI5:
            return RPI5()

        if compatibleString == RaucConfig.COMPAT_STRING_RPI4:
            return RPI4()
        
        if compatibleString == RaucConfig.COMPAT_STRING_RPI3:
            return RPI3()
        
        print(f"Unsupported device found {compatibleString}, please add support")
        return GenericAMD64()

    def __init__(self, mock=False) -> None:
        self.MOCK = mock

        if mock:
            self.rauc = RaucConfig(MOCK_RAUC_CONFIG)
        else:
            self.rauc = RaucConfig()
    
        self.dev = self.__detectDevice()
        print(f"Detected {self.dev}")
