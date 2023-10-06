# Fluvius P1 to MQTT
MQTT client for Fluvius smart energy meter (DSMR5) - "Slimme Meter". Written in Python 3.x
 
Connect Smart Meter via a P1 USB cable to e.g. Raspberry Pi

Application will continuously read energy meter and parse telegrams which are send onto a MQTT broker

Includes Home Assistant MQTT Auto Discovery

**Supported data fields:**

| OBIS CODE	| Description | MQTT Tag | Unit |
| --- | --- | --- |--- |
0-0:96.1.4 | Version information | version | 
0-0:96.1.1 | Equipment identifier | serial | 
0-0:1.0.0 | Timestamp | timestamp | 
0-0:96.7.21.255 | Number power failures | power_failures | 
0-0:96.7.9.255 | Number long power failures | long_power_failures | 
0-0:96.14.0 | Tariff indicator electricity | tariff_indicator | 
1-0:21.7.0 | Instantaneous active power L1 +P | P_L1_consumed | kW
1-0:41.7.0 | Instantaneous active power L2 +P | P_L2_consumed | kW
1-0:61.7.0 | Instantaneous active power L3 +P | P_L3_consumed | kW
1-0:22.7.0 | Instantaneous active power L1 -P | P_L1_produced | kW
1-0:42.7.0 | Instantaneous active power L2 -P | P_L2_produced | kW
1-0:62.7.0 | Instantaneous active power L3 -P | P_L3_produced | kW
1-0:1.7.0 | Actual electricity power delivered +P | P_consumed | kW
1-0:2.7.0 | Actual electricity power received -P | P_produced | kW
0-1:24.2.1 | Gas consumption [m\u00b3] | gas_consumed | kW
0-1:96.1.0 | Equipment Identifier | serial | 
1-0:1.8.1 | Electricity consumed (Tariff 1) | elec_consumed_tar1 | kWh
1-0:1.8.2 | Electricity consumed (Tariff 2) | elec_consumed_tar2 | kWh
1-0:2.8.1 | Electricity produced (Tariff 1) | elec_produced_tar1 | kWh
1-0:2.8.2 | Electricity produced (Tariff 2) | elec_produced_tar2 | kWh
1-0:1.8.3 | Electricity consumed | elec_consumed | kWh
1-0:2.8.3 | Electricity produced | elec_produced | kWh
1-0:32.7.0 | Instantaneous voltage L1 | V_L1 | V
1-0:52.7.0 | Instantaneous voltage L2 | V_L2 | V
1-0:72.7.0 | Instantaneous voltage L3 | V_L3 | V
1-0:31.7.0 | Instantaneous current L1 | I_L1 | A
1-0:51.7.0 | Instantaneous current L2 | I_L2 | A
1-0:71.7.0 | Instantaneous current L3 | I_L3 | A
1-0:32.36.0 | Number of voltage swells L1 | V_L1_swells | 
1-0:52.36.0 | Number of voltage swells L2 | V_L2_swells | 
1-0:72.36.0 | Number of voltage swells L3 | V_L3_swells | 
1-0:32.32.0 | Number of voltage sags L1 | V_L1_sags | 
1-0:52.32.0 | Number of voltage sags L2 | V_L2_sags | 
1-0:72.32.0 | Number of voltage sags L3 | V_L3_sags | 
0-0:96.3.10 | Breaker state | breaker_state | 
0-0:17.0.0 | Limiter threshold | limiter_threshold | 
1-0:31.4.0 | Fuse supervision threshold L1 | fuse_threshold | 
0-0:96.13.0 | Text message | text_message | 
1-0:1.6.0 | Monthly peak | monthly_peak | kW
_0-0:98.1.0_ | _Historical peaks_ | _historical_peaks_ | 
1-0:1.4.0 | Current average demand | average_demand | kW

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
  * cd fluvius2mqtt/
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
For all SMR specs, see [Fluvius]([https://www.netbeheernederland.nl/dossiers/slimme-meter-15/documenten](https://www.fluvius.be/sites/fluvius/files/2019-12/e-mucs_h_ed_1_3.pdf)) or [netbeheer](https://www.netbeheernederland.nl/dossiers/slimme-meter-15/documenten)

## Licence
GPL v3

## Versions
1.0.0
* Updated OBIS codes to match the Fluvius meter readings including monthly peak
* Forked version 3.0.0 from https://github.com/hansij66/dsmr2mqtt
