# Fluvius P1 to MQTT
MQTT client for Fluvius smart energy meter (DSMR5) - "Slimme Meter". Written in Python 3.x
 
Connect Smart Meter via a P1 USB cable to e.g. Raspberry Pi

Application will continuously read energy meter and parse telegrams which are send onto a MQTT broker

Includes Home Assistant MQTT Auto Discovery

**Supported data fields:**

| OBIS CODE	| MEANING |
| ---|---|
| 0-0:96.1.4	| ID	|
| 0-0:96.1.1	| Serial number of electricity meter (in ASCII hex)	|
| 0-0:1.0.0	| Timestamp of the telegram	|
| 1-0:1.8.1	| Rate 1 (day) – total consumption	|
| 1-0:1.8.2	| Rate 2 (night) – total consumption	|
| 1-0:2.8.1	| Rate 1 (day) – total production	|
| 1-0:2.8.2	| Rate 2 (night) – total production	|
| 0-0:96.14.0	| Current rate (1=day,2=night)	|
| 1-0:1.7.0	| All phases consumption	|
| 1-0:2.7.0	| All phases production	|
| 1-0:21.7.0	| L1 consumption	|
| 1-0:41.7.0	| L2 consumption	|
| 1-0:61.7.0	| L3 consumption	|
| 1-0:22.7.0	| L1 production	|
| 1-0:42.7.0	| L2 production	|
| 1-0:62.7.0	| L3 production	|
| 1-0:32.7.0	| L1 voltage	|
| 1-0:52.7.0	| L2 voltage	|
| 1-0:72.7.0	| L3 voltage	|
| 1-0:31.7.0	| L1 current	|
| 1-0:51.7.0	| L2 current	|
| 1-0:71.7.0	| L3 current	|
| 0-0:96.3.10	| Switch position electricity	|
| 0-0:17.0.0	| Max. allowed power/phase	|
| 1-0:31.4.0	| Max. allowed current/plase	|
| 0-0:96.13.0	| Message	|
| 0-1:24.1.0	| Other devices on bus	|
| 0-1:96.1.1	| Serial number of natural gas meter (in ASCII hex)	|
| 0-1:24.4.0	| Switch position natural gas	|
| 0-1:24.2.3	| Reading from natural gas meter (timestamp) (value)	|

In `dsmr50.py`, specify:
* Which messages to be parsed
* Description and units
* MQTT topics and tags
* MQTT broadcast frequency
* Possible multiplications to apply to the measurements
* Auto discovery for Home Assistant

A typical MQTT message broadcasted with meter data
```json
{
    "I_L1": 1.82,
    "P_L1_cons": 0,
    "P_L1_prod": 0.169,
    "P_cons": 0,
    "P_prod": 0.169,
    "V_L1": 235.5,
    "avg_dem": 0,
    "breaker": "1",
    "elec_cons": 9099.085,
    "elec_cons_t1": 4533.804,
    "elec_cons_t2": 4565.281,
    "elec_prod": 6464.323,
    "elec_prod_t1": 4580.828,
    "elec_prod_t2": 1883.495,
    "fuse": 999,
    "limiter": 999.9,
    "m_peak": "03.924",
    "serial": "1SAG0000000262",
    "tariff_indicator": "0001",
    "text": "",
    "timestamp": 230906095410,
    "version": "50217"
}
```
A typical MQTT message broadcasted with Home Assistant configuration
```json
{
    "unique_id": "m_peak",
    "state_topic": "fluvius_262/elec",
    "name": "Monthly peak",
    "value_template": "{{ value_json.m_peak }}",
    "icon": "mdi:gauge",
    "device": {
        "identifiers": [
            "fluvius"
        ]
    }
}
```

A virtual DSMR parameter is implemented (el_consumed and el_returned, which is sum of tarif1 and tarif2 (nacht/low en dag/normal tariff)) - as some have a dual tariff meter, while energy company administratively considers this as a mono tarif meter.

In `config.rename.py`, specify:
* MQTT server details
* Logging level
* Auto discovery on/off

```diff
-ATTENTION:
-Please open your P1 port through the Fluvius portal: https://mijn.fluvius.be/
-See Poortbeheer > Check that "Poort open"
```

## Requirements
* paho-mqtt
* pyserial
* python 3.x

## Test the USB connection before starting the scripts:
* Install packages and dependencies:
  * sudo apt-get install -y python3-paho-mqtt python3-serial python3-pip python3-crcmod python3-tabulatesudo
  * pip3 install paho-mqtt --usersudo
  * pip3 install persist-queue --user
  * sudo chmod o+rw /dev/ttyUSB0
* Test if you can read the P1 with your USB device:
  *  python3 -m serial.tools.miniterm /dev/ttyUSB0 115200 --xonxoff

* Results should be:
   ```python
    --- Miniterm on /dev/ttyUSB0  115200,8,N,1 ---
    --- Quit: Ctrl+] | Menu: Ctrl+T | Help: Ctrl+T followed by Ctrl+H ---
    925*m3)
    !CE4E
    /FLU5\253xxxxxx_A

    0-0:96.1.4(xxxxx)
    0-0:96.1.1(xxxxxxxxxxxxxxxxxxxxxxxxxxxx)
    0-0:1.0.0(210204163628W)
    1-0:1.8.1(000439.094kWh)```

## Installation:
* Install Python packages:
  * sudo pip3 install paho-mqtt --user
  * sudo pip3 install persist-queue --user
* Install from Git and configure:
  * cd /opt
  * git clone https://github.com/smartathome/fluvius2mqtt.git
  * cd dsmr2mqtt/
  * sudo vi systemd/fluvius-mqtt.service
* Adapt ExecStart under [Service] to ExecStart=/opt/fluvius2mqtt/fluvius-mqtt.py
  * sudo cp -p systemd/fluvius-mqtt.service /etc/systemd/system
* Edit the MQTT configuration and know that the MQTT_TOPIC_PREFIX = "fluvius" with last 3 digits of meter serial will show these messages as topic fluvius_XXX/. Configuration will be shown as homeassistant/sensor/fluvius_XXX/
  * sudo cp -p config.rename.py config.py && sudo vi config.py
  * sudo systemctl enable fluvius-mqtt
  * sudo systemctl start fluvius-mqtt
* And check if it is running properly
  * sudo systemctl status fluvius-mqtt
    ```python
    user@server:/opt/fluvius2mqtt $ sudo systemctl status fluvius-mqtt
    fluvius-mqtt.service - Fluvius smart energy meter P1
     Loaded: loaded (/etc/systemd/system/fluvius-mqtt.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2023-09-26 22:21:06 CEST; 18h ago
     Main PID: 1026 (fluvius-mqtt.py)
      Tasks: 6 (limit: 1595)
        CPU: 56.349s
     CGroup: /system.slice/fluvius-mqtt.service
             └─1026 /usr/bin/python3 /opt/fluvius2mqtt/fluvius-mqtt.py
             ```

Use http://mqtt-explorer.com/ to test & inspect MQTT messages or use the MQTT browser from within Home Assistant

A `test/dsmr.raw` simulation file is provided.
Set `PRODUCTION = False` in `config.py` to use the simulation file. In that case, no P1/serial connection is required.

Tested under Debian/Raspbian.
Tested with DSMR v5.0 meter in Belgium. For other DSMR versions, `dsmr50.py` needs to be adapted.
For all SMR specs, see [netbeheer](https://www.netbeheernederland.nl/dossiers/slimme-meter-15/documenten)

## Licence
GPL v3

## Versions
1.0.0
* Updated OBIS codes to match the Fluvius meter readings including monthly peak
* Forked version 3.0.0 from https://github.com/hansij66/dsmr2mqtt
