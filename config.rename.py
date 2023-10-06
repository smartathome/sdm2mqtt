"""
Rename to config.py

Configure:
- MQTT client
- Home Assistant Discovery
- USB P1 serial port
- Debug level

Adapt the DSMR messages to be parsed from the meter in dsmr50.py

To test run:
python3 fluvius-mqtt.py

"""

# [ LOGLEVELS ]
# DEBUG, INFO, WARNING, ERROR, CRITICAL
loglevel = "DEBUG"
#loglevel = "INFO"

# [ PRODUCTION ]
# True if run in production
# False when running in simulation
#PRODUCTION = False
PRODUCTION = True

# File below is used when PRODUCTION is set to False
# Own simulation file can be created in bash/Linux:
# tail -f /dev/ttyUSB0 > fluvius.raw (wait 10-15sec and hit ctrl-C)
# (assuming that P1 USB is connected as ttyUSB0)
# Add string "EOF" (without quotes) as last line
SIMULATORFILE = "test/fluvius.raw"

# [ MQTT Parameters ]
# Using local dns names was not always reliable with PAHO
MQTT_BROKER = "192.168.1.1"
MQTT_PORT = 1883
MQTT_CLIENT_UNIQ = 'mqtt-fluvius'
MQTT_QOS = 1
MQTT_USERNAME = "username"
MQTT_PASSWORD = "secret"

# You can use the last 10 characters of the meter serial number to make this device and the MQTT_TOPIC_PREFIX unique
# When left blank, the MQTT_TOPIC_PREFIX will just be fluvius by default
MQTT_METER_UNIQUE = "0123456789"

if PRODUCTION:
  if MQTT_METER_UNIQUE == "":
    MQTT_TOPIC_PREFIX = "fluvius"
  else:
    MQTT_TOPIC_PREFIX = "fluvius" + "_" + MQTT_METER_UNIQUE
else:
  if MQTT_METER_UNIQUE == "":
    MQTT_TOPIC_PREFIX = "fluvius"
  else:
    MQTT_TOPIC_PREFIX = "fluvius" + "_" + MQTT_METER_UNIQUE
  MQTT_CLIENT_UNIQ = 'mqtt-fluvius-test'

# [ Home Assistant ]
HA_DISCOVERY = True
#HA_DISCOVERY = False

# Default is False, removes the auto config message when this program exits
HA_DELETECONFIG = False

# Discovery messages per hour
# At start-up, always a discovery message is send
# Default is 12 ==> 1 message every 5 minutes. If the MQTT broker is restarted
# it can take up to 5 minutes before the fluvius device re-appears in HA
HA_INTERVAL = 12

# [ P1 USB serial ]
ser_port = "/dev/ttyUSB0"
ser_baudrate = 115200
