# --- Modbus Serial Port Settings ---
COM_PORT = 'COM16'
BAUDRATE = 9600
TIMEOUT = 3

# --- Modbus Device Settings ---
SLAVE_ID = 1

# --- UI Settings ---
APP_TITLE = "Modbus Relay Controller"
RELAY_COUNT = 8

# --- Modbus Addresses & Values (ตาม Datasheet) ---
RELAY_ADDRESSES = {
    1: 0x0000, 2: 0x0001, 3: 0x0002, 4: 0x0003,
    5: 0x0004, 6: 0x0005, 7: 0x0006, 8: 0x0007,
}
COIL_ON = True
COIL_OFF = False

# --- Logging Settings ---
LOG_FILE_PATH = 'data/logs/app.log'