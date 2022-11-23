from abc import ABC, abstractmethod
from pathlib import Path
import uuid

class Device(ABC):
    def serial(self) -> str:
        return self._serial().replace(':','').replace('0x', '')

    @abstractmethod
    def _serial() -> str:
        pass

    @abstractmethod
    def model() -> str:
        pass

    def __str__(self) -> str:
        return f"serial: {self.serial()}, model: {self.model()}"

class RPI(Device):
    def model(self) -> str:
        return Path('/proc/device-tree/model').read_text()

class RPI3(RPI):
    # Combine eth and wifi mac because thers no unique serial number on pi3
    def _serial(self) -> str:
        ethSerial = Path('/sys/class/net/eth0/address').read_text()
        wifiSerial = Path('/sys/class/net/wlan0/address').read_text()
        return ethSerial + wifiSerial

    def __str__(self):
        return "RPI3Device: " + super().__str__()

class RPI4(RPI):
    def _serial(self) -> str:
        return Path('/proc/device-tree/serial-number').read_text()

    def __str__(self):
        return "RPI4Device: " + super().__str__()

class GenericAMD64(Device):
    # Return the primary mac address without formatting
    def _serial(self) -> str:
        return hex(uuid.getnode())

    def model(self) -> str:
        return "GenericAMD64"

    def __str__(self):
        return "GenericAMD64Device: " + super().__str__()