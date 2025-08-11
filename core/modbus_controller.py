from pymodbus.client.sync import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException
from config.settings import COM_PORT, BAUDRATE, TIMEOUT, SLAVE_ID, RELAY_ADDRESSES


class ModbusController:
    """
    Class responsible for handling Modbus RTU communication with the relay board.
    """

    def __init__(self):
        self.client = ModbusSerialClient(
            method='rtu',
            port=COM_PORT,
            baudrate=BAUDRATE,
            timeout=TIMEOUT
        )
        self.is_connected = False

    def connect(self):
        """Establishes a connection to the Modbus device."""
        if not self.is_connected:
            try:
                self.is_connected = self.client.connect()
                return self.is_connected
            except Exception:
                self.is_connected = False
                return False
        return True

    def disconnect(self):
        """Closes the Modbus serial connection."""
        if self.is_connected:
            self.client.close()
            self.is_connected = False

    def write_relay_state(self, relay_number, state):
        """Writes a new state (True for ON, False for OFF) to a specific relay."""
        if not self.is_connected:
            return False, "Not connected to the device."

        if relay_number not in RELAY_ADDRESSES:
            return False, f"Invalid relay number: {relay_number}"

        address = RELAY_ADDRESSES[relay_number]
        try:
            # Use write_coil which takes a boolean value
            response = self.client.write_coil(address, state, unit=SLAVE_ID)
            if response.isError():
                return False, f"Modbus error: {response}"

            return True, "Success"

        except ModbusIOException as e:
            return False, f"Communication error: {e}"
        except Exception as e:
            return False, f"An unexpected error occurred: {e}"

    # Optional: Add a method to read the current state of a coil
    def read_relay_state(self, relay_number):
        """Reads the current state of a specific relay."""
        if not self.is_connected:
            return None, "Not connected."

        if relay_number not in RELAY_ADDRESSES:
            return None, f"Invalid relay number: {relay_number}"

        address = RELAY_ADDRESSES[relay_number]
        try:
            response = self.client.read_coils(address, 1, unit=SLAVE_ID)
            if response.isError():
                return None, f"Modbus error: {response}"

            return response.bits[0], "Success"

        except ModbusIOException as e:
            return None, f"Communication error: {e}"
        except Exception as e:
            return None, f"An unexpected error occurred: {e}"