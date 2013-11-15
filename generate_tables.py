#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import urllib2
import traceback
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import fromstring as etreefromstring

sys.path.append(os.path.join(os.getcwd(), '..', '..', 'generators'))
from device_identifiers import device_identifiers

lang = 'en'

         # display,        uri
tools = [('Brick Daemon', 'brickd'),
         ('Brick Viewer', 'brickv')]

            # display,  uri1     is_language, uri2
bindings = [('Modbus', 'modbus', False,       None),
            ('TCP/IP', 'tcpip',  False,       None),
            ('C/C++',  'c',      True,        'C'),
            ('C#',     'csharp', True,        'CSharp'),
            ('Delphi', 'delphi', True,        'Delphi'),
            ('Java',   'java',   True,        'Java'),
            ('PHP',    'php',    True,        'PHP'),
            ('Python', 'python', True,        'Python'),
            ('Ruby',   'ruby',   True,        'Ruby'),
            ('Shell',  'shell',  True,        'Shell'),
            ('VB.NET', 'vbnet',  True,        'VBNET')]

                  # display,                      uri,                         bindings, description, is_published
bricks =         [['DC',                         'dc',                         bindings, "",          True],
                  ['Debug',                      'debug',                      [],       "",          True],
                  ['IMU',                        'imu',                        bindings, "",          True],
                  ['Master',                     'master',                     bindings, "",          True],
                  ['Servo',                      'servo',                      bindings, "",          True],
                  ['Stepper',                    'stepper',                    bindings, "",          True]]


                  # display,                      uri,                         bindings, description, is_published
bricklets =      [['Ambient Light',              'ambient_light',              bindings, "",          True],
                  ['Analog In',                  'analog_in',                  bindings, "",          True],
                  ['Analog Out',                 'analog_out',                 bindings, "",          True],
                  ['Barometer',                  'barometer',                  bindings, "",          True],
                  ['Breakout',                   'breakout',                   [],       "",          True],
                  ['Current12',                  'current12',                  bindings, "",          True],
                  ['Current25',                  'current25',                  bindings, "",          True],
                  ['Distance IR',                'distance_ir',                bindings, "",          True],
                  ['Distance US',                'distance_us',                bindings, "",          False],
                  ['Dual Button',                'dual_button',                bindings, "",          False],
                  ['Dual Relay',                 'dual_relay',                 bindings, "",          True],
                  ['GPS',                        'gps',                        bindings, "",          True],
                  ['Hall Effect',                'hall_effect',                bindings, "",          False],
                  ['Humidity',                   'humidity',                   bindings, "",          True],
                  ['Industrial Digital In 4',    'industrial_digital_in_4',    bindings, "",          True],
                  ['Industrial Digital Out 4',   'industrial_digital_out_4',   bindings, "",          True],
                  ['Industrial Dual 0-20mA',     'industrial_dual_0_20ma',     bindings, "",          True],
                  ['Industrial Quad Relay',      'industrial_quad_relay',      bindings, "",          True],
                  ['IO-16',                      'io16',                       bindings, "",          True],
                  ['IO-4',                       'io4',                        bindings, "",          True],
                  ['Joystick',                   'joystick',                   bindings, "",          True],
                  ['LCD 16x2',                   'lcd_16x2',                   bindings, "",          True],
                  ['LCD 20x4',                   'lcd_20x4',                   bindings, "",          True],
                  ['LED Strip',                  'led_strip',                  bindings, "",          False],
                  ['Line',                       'line',                       bindings, "",          False],
                  ['Linear Poti',                'linear_poti',                bindings, "",          True],
                  ['Moisture',                   'moisture',                   bindings, "",          False],
                  ['Motion Detector',            'motion_detector',            bindings, "",          False],
                  ['Multi Touch',                'multi_touch',                bindings, "",          False],
                  ['Piezo Buzzer',               'piezo_buzzer',               bindings, "",          True],
                  ['Piezo Speaker',              'piezo_speaker',               bindings, "",         False],
                  ['PTC',                        'ptc',                        bindings, "",          True],
                  ['Remote Switch',              'remote_switch',              bindings, "",          False],
                  ['Rotary Encoder',             'rotary_encoder',             bindings, "",          False],
                  ['Rotary Poti',                'rotary_poti',                bindings, "",          True],
                  ['Segment Display 4x7',        'segment_display_4x7',        bindings, "",          False],
                  ['Sound Intensity',            'sound_intensity',            bindings, "",          False],
                  ['Temperature',                'temperature',                bindings, "",          True],
                  ['Temperature IR',             'temperature_ir',             bindings, "",          True],
                  ['Tilt',                       'tilt',                       bindings, "",          False],
                  ['Voltage',                    'voltage',                    bindings, "",          True],
                  ['Voltage/Current',            'voltage_current',            bindings, "",          True],
                 ]

                  # display,                      uri,                         bindings, description, is_published
extensions =     [['Chibi Extension',            'chibi',                      [],       "",          True],
                  ['Ethernet Extension',         'ethernet',                   [],       "",          True],
                  ['RS485 Extension',            'rs485',                      [],       "",          True],
                  ['WIFI Extension',             'wifi',                       [],       "",          True]]

                  # display,                      uri,                         bindings, description, is_published
power_supplies = [['Step-Down Power Supply',     'step_down',                  [],       "",          True]]

                  # display,                      uri,                         bindings, description, is_published
accessories =    [['DC Jack Adapter',            'dc_jack_adapter',            [],       "",          True]]


brick_descriptions = {
'dc': {
    'en': 'Drives one brushed DC motor with max. 28V and 5A',
    'de': 'Steuert einen DC Motor mit max. 28V und 5A'
    },
'debug': {
    'en': 'For Firmware Developers: JTAG and serial console',
    'de': 'Für Firmware Entwickler: JTAG und serielle Konsole'
    },
'imu': {
    'en': 'Full fledged AHRS with 9 degrees of freedom',
    'de': 'Voll ausgestattetes AHRS mit 9 Freiheitsgraden'
    },
'master': {
    'en': 'Is the basis to build stacks and has 4 Bricklet Ports',
    'de': 'Ist Grundlage um Stapel zu bauen und bietet 4 Bricklet Anschlüsse'
    },
'servo': {
    'en': 'Drives up to 7 RC Servos with max. 3A',
    'de': 'Steuert bis zu 7 RC Servos mit max. 3A'
    },
'stepper': {
    'en': 'Drives one bipolar stepper motor with max. 38V and 2.5A per phase',
    'de': 'Steuert einen bipolaren Schrittmotor mit max. 38V und 2,5A pro Phase'
    }
}

bricklet_descriptions = {
'ambient_light': {
    'en': 'Measures ambient light up to 900lux',
    'de': 'Misst Umgebungslicht bis zu 900Lux'
    },
'analog_in': {
    'en': 'Measures voltages up to 45V',
    'de': 'Misst elektrische Spannungen bis zu 45V'
    },
'analog_out': {
    'en': 'Generates configurable voltages up to 5V',
    'de': 'Erzeugt konfigurierbare elektrische Spannungen bis zu 5V'
    },
'barometer': {
    'en': 'Measures air pressure and altitude changes',
    'de': 'Misst Luftdruck und Höhenänderungen'
    },
'breakout': {
    'en': 'Makes all Bricklet signals available',
    'de': 'Macht alle Bricklet Signale zugänglich'
    },
'current12': {
    'en': 'Bidirectional current sensor for up to 12.5A',
    'de': 'Bidirektionaler Stromsensor für bis zu 12,5A'
    },
'current25': {
    'en': 'Bidirectional current sensor for up to 25A',
    'de': 'Bidirektionaler Stromsensor für bis zu 25A'
    },
'distance_ir': {
    'en': 'Measures distances up to 150cm with IR light',
    'de': 'Misst Entfernungen bis zu 150cm mit IR Licht'
    },
'distance_us': {
    'en': 'Measures distances from 2cm to 400cm with ultrasound',
    'de': 'Misst Entfernungen von 2cm bis 400cm mit Ultraschall'
    },
'dual_button': {
    'en': 'Two tactile buttons with built-in blue LEDs',
    'de': 'Zwei Taster mit eingebauten blauen LEDs'
    },
'dual_relay': {
    'en': 'Two relays to switch AC/DC devices',
    'de': 'Zwei Relais um AC/DC Geräte zu schalten'
    },
'gps': {
    'en': 'Determine position, velocity and altitude',
    'de': 'Bestimmt Position, Geschwindigkeit und Höhe'
    },
'hall_effect': {
    'en': 'Detects presence of magnetic field',
    'de': 'Detektiert Magnetfelder'
    },
'humidity': {
    'en': 'Measures relative humidity',
    'de': 'Misst relative Luftfeuchtigkeit'
    },
'industrial_digital_in_4': {
    'en': '4 galvanically isolated digital inputs',
    'de': '4 galvanisch getrennte digitale Eingänge'
    },
'industrial_digital_out_4': {
    'en': '4 galvanically isolated digital outputs',
    'de': '4 galvanisch getrennte digitale Ausgänge'
    },
'industrial_dual_0_20ma': {
    'en': 'Senses two currents between 0 and 20mA (IEC 60381-1)',
    'de': 'Misst zwei Stromquellen zwischen 0 und 20mA (IEC 60381-1)'
    },
'industrial_quad_relay': {
    'en': '4 galvanically isolated solid state relays',
    'de': '4 galvanisch getrennte Solid State Relais'
    },
'io16': {
    'en': '16-channel digital input/output',
    'de': '16 digitale Ein- und Ausgänge'
    },
'io4': {
    'en': '4-channel digital input/output',
    'de': '4 digitale Ein- und Ausgänge'
    },
'joystick': {
    'en': '2-axis joystick with push-button',
    'de': '2-Achsen Joystick mit Taster'
    },
'lcd_16x2': {
    'en': '16x2 character alphanumeric display with blue backlight',
    'de': '16x2 Zeichen alphanumerisches Display'
    },
'lcd_20x4': {
    'en': '20x4 character alphanumeric display with blue backlight',
    'de': '20x4 Zeichen alphanumerisches Display'
    },
'led_strip': {
    'en': 'Controls up to 320 RGB LEDs',
    'de': 'Steuert bis zu 320 RGB LEDs'
    },
'line': {
    'en': 'Measures the reflectivity of a surface',
    'de': 'Misst die Reflektivität einer Oberfläche'
    },
'linear_poti': {
    'en': '59mm linear potentiometer',
    'de': '59mm Linear-Potentiometer'
    },
'moisture': {
    'en': 'Measures moisture between two probes',
    'de': 'Misst Feuchtigkeit zwischen zwei Elektroden'
    },
'motion_detector': {
    'en': 'Passive Infrared Motion Sensor, 7m range',
    'de': 'Passiver Infrarot Bewegungssensor, 7m Reichweite'
    },
'multi_touch': {
    'en': 'Capacitive Touch Sensor for 12 electrodes',
    'de': 'Kapazitiver Touch Sensor für 12 Elektroden'
    },
'piezo_buzzer': {
    'en': 'Creates 1kHz beep',
    'de': 'Erzeugt 1kHz Piepton'
    },
'piezo_speaker': {
    'en': 'Creates beep with configurable frequency',
    'de': 'Erzeugt Piepton mit konfigurierbarer Frequenz'
    },
'ptc': {
    'en': 'Reads temperatures from Pt100/1000 sensors',
    'de': 'Liest Temperaturen von Pt100/1000-Sensoren'
    },
'remote_switch': {
    'en': 'Controls remote mains switches',
    'de': 'Steuert Funksteckdosen'
    },
'rotary_encoder': {
    'en': '360° rotary encoder with push-button',
    'de': '360° Drehgeber / Drehencoder mit Taster'
    },
'rotary_poti': {
    'en': '300° rotary potentiometer',
    'de': '300° Dreh-Potentiometer'
    },
'segment_display_4x7': {
    'en': 'Four 7-segment displays with switchable colon',
    'de': 'Vier 7-Segment Anzeigen mit schaltbarem Doppelpunkt'
    },
'sound_intensity': {
    'en': 'Measures sound intensity',
    'de': 'Misst Schallintensität'
    },
'temperature': {
    'en': 'Measures ambient temperature with 0.5°C accuracy',
    'de': 'Misst Umgebungstemperatur mit 0,5°C Genauigkeit'
    },
'temperature_ir': {
    'en': 'Measures contactless object temperature from -70°C to 380°C',
    'de': 'Kontaktlose Objekttemperaturmessung von -70°C bis 380°C'
    },
'tilt': {
    'en': 'Detects inclination of Bricklet (tilt switch open/closed)',
    'de': 'Erkennt Neigung des Bricklets (Neigungsschalter offen/geschlossen)'
    },
'voltage': {
    'en': 'Measures voltages up to 50V',
    'de': 'Misst Spannungen bis zu 50V'
    },
'voltage_current': {
    'en': 'Measure power, voltage and current up to 720W/36V/20A',
    'de': 'Misst Leistung, Spannung und Strom bis zu 720W/36V/20A'
    },
}

extension_descriptions = {
'chibi': {
    'en': 'Wireless Chibi Master Extension',
    'de': 'Drahtlose Chibi Master Extension'
    },
'ethernet': {
    'en': 'Cable based Ethernet Master Extension',
    'de': 'Kabelgebundene Ethernet Master Extension'
    },
'rs485': {
    'en': 'Cable based RS485 Master Extension',
    'de': 'Kabelgebundene RS485 Master Extension'
    },
'wifi': {
    'en': 'Wireless WIFI Master Extension',
    'de': 'Drahtlose WIFI Master Extension'
    }
}

power_supply_descriptions = {
'step_down': {
    'en': 'Powers a stack of Bricks with 5V',
    'de': 'Versorgt einen Stapel von Bricks mit 5V'
    }
}

accessory_descriptions = {
'dc_jack_adapter': {
    'en': 'Adapter between a 5mm DC jack and 2 Pole Black Connector',
    'de': 'Adapter zwischen einem 5mm DC Stecker und 2 Pin Stecker Schwarz'
    }
}

index_table_head = {
'en':
""".. csv-table::
 :header: "", "API"
 :delim: |
 :widths: 15, 40

{0}
 |
 **Bricks** |
{1}
 |
 **Bricklets** |
{2}
 |
 **Master Extensions** |
{3}
 |
 **Power Supplies** |
{4}
 |
 **Accessories** |
{5}
""",
'de':
""".. csv-table::
 :header: "", "API"
 :delim: |
 :widths: 15, 40

{0}
 |
 **Bricks** |
{1}
 |
 **Bricklets** |
{2}
 |
 **Master Extensions** |
{3}
 |
 **Stromversorgungen** |
{4}
 |
 **Zubehör** |
{5}
"""
}

product_overview_table_head = {
'en':
"""
.. csv-table::
   :header: "Name", "Description"
   :widths: 30, 70

""",
'de':
"""
.. csv-table::
   :header: "Name", "Beschreibung"
   :widths: 30, 70

"""
}

download_tools_source_code = {
'en': 'Source Code',
'de': 'Quelltext'
}

download_tools_archive = {
'en': 'Archive',
'de': 'Archiv'
}

download_tools_table_head = {
'en':
""".. csv-table::
 :header: "Tool", "Downloads", "Version", "Archive", "Changelog"
 :delim: |
 :widths: 17, 32, 5, 5, 8

""",
'de':
""".. csv-table::
 :header: "Tool", "Downloads", "Version", "Archiv", "Changelog"
 :delim: |
 :widths: 17, 32, 5, 5, 8

"""
}

download_bindings_bindings_and_examples = {
'en': 'Bindings and Examples',
'de': 'Bindings und Beispiele'
}

download_bindings_archive = {
'en': 'Archive',
'de': 'Archiv'
}

download_bindings_table_head = {
'en':
""".. csv-table::
 :header: "Language", "Downloads", "Version", "Archive", "Changelog"
 :delim: |
 :widths: 17, 32, 5, 5, 8

""",
'de':
""".. csv-table::
 :header: "Sprache", "Downloads", "Version", "Archiv", "Changelog"
 :delim: |
 :widths: 17, 32, 5, 5, 8

"""
}

download_firmwares_source_code = {
'en': 'Source Code',
'de': 'Quelltext'
}

download_firmwares_archive = {
'en': 'Archive',
'de': 'Archiv'
}

download_firmwares_table_head = {
'en':
""".. csv-table::
 :header: "", "Downloads", "Version", "Archive", "Changelog"
 :delim: |
 :widths: 17, 32, 5, 5, 8

 **Bricks** | |
{0}
 | |
 **Bricklets** | |
 {1}""",
'de':
""".. csv-table::
 :header: "", "Downloads","Version",  "Archiv", "Changelog"
 :delim: |
 :widths: 17, 32, 5, 5, 8

 **Bricks** | |
{0}
 | |
 **Bricklets** | |
{1}"""
}

source_code_gits_table_head = {
'en':
""".. csv-table::
 :header: "", "Repository", "Bug Tracking"
 :delim: |
 :widths: 15, 30, 10

 **Tools** | |
 Brick Daemon | `git://github.com/Tinkerforge/brickd.git <https://github.com/Tinkerforge/brickd/>`__ | `Report Bug <https://github.com/Tinkerforge/brickd/issues>`__
 Brick Viewer | `git://github.com/Tinkerforge/brickv.git <https://github.com/Tinkerforge/brickv/>`__ | `Report Bug <https://github.com/Tinkerforge/brickv/issues>`__
 Brick Bootloader | `git://github.com/Tinkerforge/brickboot.git <https://github.com/Tinkerforge/brickboot/>`__ | `Report Bug <https://github.com/Tinkerforge/brickboot/issues>`__
 Brick Library | `git://github.com/Tinkerforge/bricklib.git <https://github.com/Tinkerforge/bricklib/>`__ | `Report Bug <https://github.com/Tinkerforge/bricklib/issues>`__
 Bricklet Library | `git://github.com/Tinkerforge/brickletlib.git <https://github.com/Tinkerforge/brickletlib/>`__ | `Report Bug <https://github.com/Tinkerforge/brickletlib/issues>`__
 API Generator | `git://github.com/Tinkerforge/generators.git <https://github.com/Tinkerforge/generators/>`__ | `Report Bug <https://github.com/Tinkerforge/generators/issues>`__
 KiCad Libraries | `git://github.com/Tinkerforge/kicad-libraries.git <https://github.com/Tinkerforge/kicad-libraries/>`__ | `Report Bug <https://github.com/Tinkerforge/kicad-libraries/issues>`__
 | |
 **Bricks** | |
{0}
 | |
 **Bricklets** | |
{1}
 | |
 **Master Extensions** | |
{2}
 | |
 **Power Supplies** | |
 Step-Down Power Supply | `git://github.com/Tinkerforge/step-down-powersupply.git <https://github.com/Tinkerforge/step-down-powersupply/>`__ | `Report Bug <https://github.com/Tinkerforge/step-down-powersupply/issues>`__
 | |
 **Accessories** | |
 DC Jack Adapter | `git://github.com/Tinkerforge/dc-adapter.git <https://github.com/Tinkerforge/dc-adapter/>`__ | `Report Bug <https://github.com/Tinkerforge/dc-adapter/issues>`__
""",
'de':
 """.. csv-table::
 :header: "", "Repository", "Bug Tracking"
 :delim: |
 :widths: 15, 30, 10

 **Tools** | |
 Brick Daemon | `git://github.com/Tinkerforge/brickd.git <https://github.com/Tinkerforge/brickd/>`__ | `Problem melden <https://github.com/Tinkerforge/brickd/issues>`__
 Brick Viewer | `git://github.com/Tinkerforge/brickv.git <https://github.com/Tinkerforge/brickv/>`__ | `Problem melden <https://github.com/Tinkerforge/brickv/issues>`__
 Brick Bootloader | `git://github.com/Tinkerforge/brickboot.git <https://github.com/Tinkerforge/brickboot/>`__ | `Problem melden <https://github.com/Tinkerforge/brickboot/issues>`__
 Brick Library | `git://github.com/Tinkerforge/bricklib.git <https://github.com/Tinkerforge/bricklib/>`__ | `Problem melden <https://github.com/Tinkerforge/bricklib/issues>`__
 Bricklet Library | `git://github.com/Tinkerforge/brickletlib.git <https://github.com/Tinkerforge/brickletlib/>`__ | `Problem melden <https://github.com/Tinkerforge/brickletlib/issues>`__
 API Generator | `git://github.com/Tinkerforge/generators.git <https://github.com/Tinkerforge/generators/>`__ | `Problem melden <https://github.com/Tinkerforge/generators/issues>`__
 KiCad Libraries | `git://github.com/Tinkerforge/kicad-libraries.git <https://github.com/Tinkerforge/kicad-libraries/>`__ | `Problem melden <https://github.com/Tinkerforge/kicad-libraries/issues>`__
 | |
 **Bricks** | |
{0}
 | |
 **Bricklets** | |
{1}
 | |
 **Master Extensions** | |
{2}
 | |
 **Stromversorgungen** | |
 Step-Down Power Supply | `git://github.com/Tinkerforge/step-down-powersupply.git <https://github.com/Tinkerforge/step-down-powersupply/>`__ | `Problem melden <https://github.com/Tinkerforge/step-down-powersupply/issues>`__
 | |
 **Zubehör** | |
 DC Jack Adapter | `git://github.com/Tinkerforge/dc-adapter.git <https://github.com/Tinkerforge/dc-adapter/>`__ | `Problem melden <https://github.com/Tinkerforge/dc-adapter/issues>`__
"""
}

source_code_gits_brick_row_cell = {
'en': ' {0} | `git://github.com/Tinkerforge/{1}-brick.git <https://github.com/Tinkerforge/{1}-brick/>`__ | `Report Bug <https://github.com/Tinkerforge/{1}-brick/issues>`__',
'de': ' {0} | `git://github.com/Tinkerforge/{1}-brick.git <https://github.com/Tinkerforge/{1}-brick/>`__ | `Problem melden <https://github.com/Tinkerforge/{1}-brick/issues>`__'
}

source_code_gits_bricklet_row_cell = {
'en': ' {0} | `git://github.com/Tinkerforge/{1}-bricklet.git <https://github.com/Tinkerforge/{1}-bricklet/>`__ | `Report Bug <https://github.com/Tinkerforge/{1}-bricklet/issues>`__',
'de': ' {0} | `git://github.com/Tinkerforge/{1}-bricklet.git <https://github.com/Tinkerforge/{1}-bricklet/>`__ | `Problem melden <https://github.com/Tinkerforge/{1}-bricklet/issues>`__',
}

source_code_gits_extension_row_cell = {
'en': ' {0} | `git://github.com/Tinkerforge/{1}-extension.git <https://github.com/Tinkerforge/{1}-extension/>`__ | `Report Bug <https://github.com/Tinkerforge/{1}-extension/issues>`__',
'de': ' {0} | `git://github.com/Tinkerforge/{1}-extension.git <https://github.com/Tinkerforge/{1}-extension/>`__ | `Problem melden <https://github.com/Tinkerforge/{1}-extension/issues>`__',
}

api_bindings_links_table_head = {
'en':
""".. csv-table::
 :header: "", "API", "Examples"
 :delim: |
 :widths: 20, 10, 10

{0}
 | |
 **Bricks** | |
{1}
 | |
 **Bricklets** | |
{2}
""",
'de':
""".. csv-table::
 :header: "", "API", "Beispiele"
 :delim: |
 :widths: 20, 10, 10

{0}
 | |
 **Bricks** | |
{1}
 | |
 **Bricklets** | |
{2}
"""
}

api_bindings_links_ipcon_row = {
'en': ' :ref:`IP Connection <api_bindings_ip_connection>` | :ref:`API <ipcon_{0}>` | :ref:`Examples <ipcon_{0}_examples>`',
'de': ' :ref:`IP Connection <api_bindings_ip_connection>` | :ref:`API <ipcon_{0}>` | :ref:`Beispiele <ipcon_{0}_examples>`'
}

api_bindings_links_brick_row = {
'en': ' :ref:`{2} <{0}_brick>` | :ref:`API <{0}_brick_{1}_api>` | :ref:`Examples <{0}_brick_{1}_examples>`',
'de': ' :ref:`{2} <{0}_brick>` | :ref:`API <{0}_brick_{1}_api>` | :ref:`Beispiele <{0}_brick_{1}_examples>`'
}

api_bindings_links_bricklet_row = {
'en': ' :ref:`{2} <{0}_bricklet>` | :ref:`API <{0}_bricklet_{1}_api>` | :ref:`Examples <{0}_bricklet_{1}_examples>`',
'de': ' :ref:`{2} <{0}_bricklet>` | :ref:`API <{0}_bricklet_{1}_api>` | :ref:`Beispiele <{0}_bricklet_{1}_examples>`'
}

def fill_dicts():
    for brick in bricks:
        brick[3] = brick_descriptions[brick[1]][lang]

    for bricklet in bricklets:
        bricklet[3] = bricklet_descriptions[bricklet[1]][lang]

    for extension in extensions:
        extension[3] = extension_descriptions[extension[1]][lang]

    for power_supply in power_supplies:
        power_supply[3] = power_supply_descriptions[power_supply[1]][lang]

    for accessory in accessories:
        accessory[3] = accessory_descriptions[accessory[1]][lang]

LATEST_VERSIONS_URL = 'http://download.tinkerforge.com/latest_versions.txt'

tool_versions = {}
bindings_versions = {}
firmware_versions = {}
plugin_versions = {}

def get_latest_version_info():
    print 'Discovering latest versions on tinkerforge.com'

    try:
        response = urllib2.urlopen(LATEST_VERSIONS_URL)
        latest_versions_data = response.read()
    except urllib2.URLError:
        raise Exception('Latest version information on tinkerforge.com is not available (error code 1)')

    for line in latest_versions_data.split('\n'):
        line = line.strip()

        if len(line) < 1:
            continue

        parts = line.split(':')

        if len(parts) != 3:
            raise Exception('Latest version information on tinkerforge.com is malformed (error code 2)')

        latest_version_parts = parts[2].split('.')

        if len(latest_version_parts) != 3:
            raise Exception('Latest version information on tinkerforge.com is malformed (error code 3)')

        try:
            latest_version = int(latest_version_parts[0]), int(latest_version_parts[1]), int(latest_version_parts[2])
        except:
            raise Exception('Latest version information on tinkerforge.com is malformed (error code 4)')

        if parts[0] == 'tools':
            tool_versions[parts[1]] = latest_version
        elif parts[0] == 'bindings':
            bindings_versions[parts[1]] = latest_version
        elif parts[0] == 'bricks':
            firmware_versions[parts[1]] = latest_version
        elif parts[0] == 'bricklets':
            plugin_versions[parts[1]] = latest_version

def make_product_overview_table(devices, category, add_category_to_name=True):
    table_head = product_overview_table_head[lang]

    if add_category_to_name:
        row_head = '   ":ref:`{0} <{1}_' + category + '>`", "{2}"'
        row_cell = '":ref:`{0} <{1}_' + category + '_{2}>`"'
    else:
        row_head = '   ":ref:`{0} <{1}>`", "{2}"'
        row_cell = '":ref:`{0} <{1}_{2}>`"'

    rows = []

    for device in devices:
        if device[4]:
            rows.append(row_head.format(device[0], device[1], device[3]))

    return table_head + '\n'.join(rows) + '\n'

def make_download_tools_table():
    source_code = download_tools_source_code[lang]
    archive = download_tools_archive[lang]
    table_head = download_tools_table_head[lang]
    row_multi_cell = ' :ref:`{0} <{1}>` | Linux (`amd64 <http://download.tinkerforge.com/tools/{1}/linux/{1}-{4}.{5}.{6}_amd64.deb>`__, `i386 <http://download.tinkerforge.com/tools/{1}/linux/{1}-{4}.{5}.{6}_i386.deb>`__, `armhf <http://download.tinkerforge.com/tools/{1}/linux/{1}-{4}.{5}.{6}_armhf.deb>`__), `Mac OS X <http://download.tinkerforge.com/tools/{1}/macos/{1}_macos_{4}_{5}_{6}.dmg>`__, `Windows <http://download.tinkerforge.com/tools/{1}/windows/{1}_windows_{4}_{5}_{6}.exe>`__, `{2} <https://github.com/Tinkerforge/{1}/archive/v{4}.{5}.{6}.zip>`__ | {4}.{5}.{6} | `{3} <http://download.tinkerforge.com/tools/{1}/>`__ | `Changelog <https://raw.github.com/Tinkerforge/{1}/master/changelog>`__'
    row_all_cell = ' :ref:`{0} <{1}>` | `Linux <http://download.tinkerforge.com/tools/{1}/linux/{1}-{4}.{5}.{6}_all.deb>`__, `Mac OS X <http://download.tinkerforge.com/tools/{1}/macos/{1}_macos_{4}_{5}_{6}.dmg>`__, `Windows <http://download.tinkerforge.com/tools/{1}/windows/{1}_windows_{4}_{5}_{6}.exe>`__, `{2} <https://github.com/Tinkerforge/{1}/archive/v{4}.{5}.{6}.zip>`__ | {4}.{5}.{6} | `{3} <http://download.tinkerforge.com/tools/{1}/>`__ | `Changelog <https://raw.github.com/Tinkerforge/{1}/master/changelog>`__'
    rows = []

    for tool in tools:
        if tool[1] == 'brickd':
            row_cell = row_multi_cell
        else:
            row_cell = row_all_cell

        rows.append(row_cell.format(tool[0], tool[1], source_code, archive, *tool_versions[tool[1]]))

    return table_head + '\n'.join(rows) + '\n'

def make_download_bindings_table():
    bindings_and_examples = download_bindings_bindings_and_examples[lang]
    archive = download_bindings_archive[lang]
    table_head = download_bindings_table_head[lang]
    row_cell = ' `{0} <http://www.tinkerforge.com/' + lang + '/doc/Software/API_Bindings_{2}.html>`__ | `{4} <http://download.tinkerforge.com/bindings/{1}/tinkerforge_{1}_bindings_{5}_{6}_{7}.zip>`__ | {5}.{6}.{7} | `{3} <http://download.tinkerforge.com/bindings/{1}/>`__ | `Changelog <https://raw.github.com/Tinkerforge/generators/master/{1}/changelog.txt>`__'
    rows = []

    for binding in bindings:
        if binding[2]:
            rows.append(row_cell.format(binding[0], binding[1], binding[3], archive, bindings_and_examples, *bindings_versions[binding[1]]))

    return table_head + '\n'.join(rows) + '\n'

def make_download_firmwares_table():
    archive = download_firmwares_archive[lang]
    source_code = download_firmwares_source_code[lang]
    table_head = download_firmwares_table_head[lang]
    brick_row_cell = ' :ref:`{0} <{1}_brick>` | `Firmware <http://download.tinkerforge.com/firmwares/bricks/{1}/brick_{1}_firmware_{5}_{6}_{7}.bin>`__, `{3} <https://github.com/Tinkerforge/{2}-brick/archive/v{5}.{6}.{7}.zip>`__ | {5}.{6}.{7} | `{4} <http://download.tinkerforge.com/firmwares/bricks/{1}/>`__ | `Changelog <https://raw.github.com/Tinkerforge/{2}-brick/master/software/changelog>`__'
    bricklet_row_cell = ' :ref:`{0} <{1}_bricklet>` | `Plugin <http://download.tinkerforge.com/firmwares/bricklets/{3}/bricklet_{3}_firmware_{6}_{7}_{8}.bin>`__, `{4} <https://github.com/Tinkerforge/{2}-bricklet/archive/v{6}.{7}.{8}.zip>`__ | {6}.{7}.{8} | `{5} <http://download.tinkerforge.com/firmwares/bricklets/{1}/>`__ | `Changelog <https://raw.github.com/Tinkerforge/{2}-bricklet/master/software/changelog>`__'
    brick_rows = []
    bricklet_rows = []

    for brick in bricks:
        if len(brick[2]) > 0 and brick[4]:
            brick_rows.append(brick_row_cell.format(brick[0], brick[1], brick[1].replace('_', '-').replace('/', '-'), source_code, archive, *firmware_versions[brick[1]]))

    def handle_bricklet(name, common_url_part, plugin_url_part):
        bricklet_rows.append(bricklet_row_cell.format(name, common_url_part, common_url_part.replace('_', '-').replace('/', '-'), plugin_url_part, source_code, archive, *plugin_versions[plugin_url_part]))

    for bricklet in bricklets:
        if len(bricklet[2]) > 0 and bricklet[4]:
            if bricklet[1] == 'lcd_20x4':
                handle_bricklet(bricklet[0] + ' 1.1', bricklet[1], bricklet[1] + '_v11')
                handle_bricklet(bricklet[0] + ' 1.2', bricklet[1], bricklet[1] + '_v12')
            else:
                handle_bricklet(bricklet[0], bricklet[1], bricklet[1])

    return table_head.format('\n'.join(brick_rows), '\n'.join(bricklet_rows)) + '\n'

def make_api_bindings_bindings_table():
    row = '* :ref:`{0} <ipcon_{1}>`'
    rows = []

    for binding in bindings:
        if binding[2]:
            rows.append(row.format(binding[0], binding[1]))

    return '\n'.join(rows) + '\n'

def make_api_bindings_links_table(binding):
    ipcon_line = api_bindings_links_ipcon_row[lang].format(binding[1])

    brick_lines = []
    for brick in bricks:
        if brick[4] and len(brick[2]) > 0: # released and has bindings
            brick_lines.append(api_bindings_links_brick_row[lang].format(brick[1], binding[1], brick[0]))

    bricklet_lines = []
    for bricklet in bricklets:
        if bricklet[4] and len(bricklet[2]) > 0: # released and has bindings
            bricklet_lines.append(api_bindings_links_bricklet_row[lang].format(bricklet[1], binding[1], bricklet[0]))

    return api_bindings_links_table_head[lang].format(ipcon_line,
                                                      '\n'.join(brick_lines),
                                                      '\n'.join(bricklet_lines))

def make_source_code_gits_table():
    table_head = source_code_gits_table_head[lang]
    brick_row_cell = source_code_gits_brick_row_cell[lang]
    bricklet_row_cell = source_code_gits_bricklet_row_cell[lang]
    extension_row_cell = source_code_gits_extension_row_cell[lang]
    brick_rows = []
    bricklet_rows = []
    extension_rows = []

    for brick in bricks:
        if brick[4]:
            brick_rows.append(brick_row_cell.format(brick[0], brick[1].replace('_', '-').replace('/', '-')))

    for bricklet in bricklets:
        if bricklet[4]:
            bricklet_rows.append(bricklet_row_cell.format(bricklet[0], bricklet[1].replace('_', '-').replace('/', '-')))

    for extension in extensions:
        if extension[4]:
            extension_rows.append(extension_row_cell.format(extension[0], extension[1].replace('_', '-').replace('/', '-')))

    return table_head.format('\n'.join(brick_rows), '\n'.join(bricklet_rows), '\n'.join(extension_rows)) + '\n'

def make_index_table_block(devices, category, add_category_to_name=True):
    if add_category_to_name:
        row_head = ' :ref:`{0} <{1}_' + category + '>` | '
        row_cell = ' :ref:`{0} <{1}_' + category + '_{2}>`'
    else:
        row_head = ' :ref:`{0} <{1}>` | '
        row_cell = ' :ref:`{0} <{1}_{2}>`'

    rows = []

    for device in devices:
        if not device[4]:
            continue

        cells = []

        for binding in device[2]:
            cells.append(row_cell.format(binding[0], device[1], binding[1]))

        row = row_head.format(device[0], device[1]) + ', '.join(cells)
        rows.append(row)

    return '\n'.join(rows)

def make_index_table():
    ipcon_head = ' :ref:`IP Connection <api_bindings_ip_connection>` | '
    ipcon_cell = ':ref:`{0} <ipcon_{1}>`'
    ipcon_cell_llproto = ':ref:`{0} <llproto_{1}>`'
    ipcon_cells = []

    for binding in bindings:
        if binding[2]:
            ipcon_cells.append(ipcon_cell.format(binding[0], binding[1]))
        else:
            ipcon_cells.append(ipcon_cell_llproto.format(binding[0], binding[1]))

    return index_table_head[lang].format(ipcon_head + ', '.join(ipcon_cells),
                                         make_index_table_block(bricks, 'brick'),
                                         make_index_table_block(bricklets, 'bricklet'),
                                         make_index_table_block(extensions, 'extension'),
                                         make_index_table_block(power_supplies, 'power_supply'),
                                         make_index_table_block(accessories, 'accessory', False))

hlpi_table_head = {
'en':
"""
.. csv-table::
   :header: "Language", "API", "Examples", "Installation"
   :widths: 25, 10, 10, 10

""",
'de':
"""
.. csv-table::
   :header: "Sprache", "API", "Beispiele", "Installation"
   :widths: 25, 10, 10, 10

"""
}

hlpi_row_source = {
'en': '   "{0}", ":ref:`API <{1}_{2}_{3}_api>`", ":ref:`Examples <{1}_{2}_{3}_examples>`", ":ref:`Installation <api_bindings_{3}>`"',
'de': '   "{0}", ":ref:`API <{1}_{2}_{3}_api>`", ":ref:`Beispiele <{1}_{2}_{3}_examples>`", ":ref:`Installation <api_bindings_{3}>`"'
}

hlpi_row = {
'en': '   "{0}", ":ref:`API <{1}_{2}_{3}_api>`"',
'de': '   "{0}", ":ref:`API <{1}_{2}_{3}_api>`"'
}

def make_hlpi_table(device, category):
    table_head = hlpi_table_head[lang]
    row_source = hlpi_row_source[lang]
    row = hlpi_row[lang]
    rows = []

    for binding in device[2]:
        if binding[2]:
            rows.append(row_source.format(binding[0], device[1], category, binding[1]))
        else:
            rows.append(row.format(binding[0], device[1], category, binding[1]))

    return table_head + '\n'.join(rows) + '\n'

device_identifier_table_head = {
'en':
"""
.. csv-table::
   :header: "Device Identifier", "Device Name"
   :widths: 30, 100

""",
'de':
"""
.. csv-table::
   :header: "Device Identifier", "Device Name"
   :widths: 30, 100

"""
}

device_identifier_row = {
'en': '   "{0}", "{1}"',
'de': '   "{0}", "{1}"'
}

def make_device_identifier_table():
    table_head = device_identifier_table_head[lang]
    row = device_identifier_row[lang]
    rows = []

    for device_identifier in device_identifiers:
        rows.append(row.format(device_identifier[0], device_identifier[1]))

    return table_head + '\n'.join(rows) + '\n'

def write_if_changed(path, content):
    if os.path.exists(path):
        f = open(path, 'rb')
        existing = f.read()
        f.close()
        if existing == content:
            return

    f = open(path, 'wb')
    f.write(content)
    f.close()

def generate(path):
    global lang

    if path.endswith('/en'):
        lang = 'en'
    elif path.endswith('/de'):
        lang = 'de'
    else:
        print('Wrong working directory')
        sys.exit(1)

    fill_dicts()
    get_latest_version_info()

    print('Generating index_links.table')
    write_if_changed(os.path.join(path, 'source', 'index_links.table'), make_index_table())

    print('Generating Product_Overview_bricks.table')
    write_if_changed(os.path.join(path, 'source', 'Product_Overview_bricks.table'), make_product_overview_table(bricks, 'brick'))

    print('Generating Product_Overview_bricklets.table')
    write_if_changed(os.path.join(path, 'source', 'Product_Overview_bricklets.table'), make_product_overview_table(bricklets, 'bricklet'))

    print('Generating Product_Overview_extensions.table')
    write_if_changed(os.path.join(path, 'source', 'Product_Overview_extensions.table'), make_product_overview_table(extensions, 'extension'))

    print('Generating Product_Overview_power_supplies.table')
    write_if_changed(os.path.join(path, 'source', 'Product_Overview_power_supplies.table'), make_product_overview_table(power_supplies, 'power_supply'))

    print('Generating Product_Overview_accessories.table')
    write_if_changed(os.path.join(path, 'source', 'Product_Overview_accessories.table'), make_product_overview_table(accessories, 'accessory', False))

    print('Generating Downloads_tools.table')
    write_if_changed(os.path.join(path, 'source', 'Downloads_tools.table'), make_download_tools_table())

    print('Generating Downloads_bindings.table')
    write_if_changed(os.path.join(path, 'source', 'Downloads_bindings.table'), make_download_bindings_table())

    print('Generating Downloads_firmwares.table')
    write_if_changed(os.path.join(path, 'source', 'Downloads_firmwares.table'), make_download_firmwares_table())

    print('Generating API_Bindings_bindings.table')
    write_if_changed(os.path.join(path, 'source', 'Software', 'API_Bindings_bindings.table'), make_api_bindings_bindings_table())

    print('Generating Source_Code_gits.table')
    write_if_changed(os.path.join(path, 'source', 'Source_Code_gits.table'), make_source_code_gits_table())

    for brick in bricks:
        if len(brick[2]) == 0:
            continue

        name = brick[0].replace(' ', '_').replace('-', '').replace('/', '_')

        print('Generating {0}_Brick_hlpi.table'.format(name))
        write_if_changed(os.path.join(path, 'source', 'Hardware', 'Bricks', name + '_Brick_hlpi.table'), make_hlpi_table(brick, 'brick'))

    for bricklet in bricklets:
        if len(bricklet[2]) == 0:
            continue

        name = bricklet[0].replace(' ', '_').replace('-', '').replace('/', '_')

        print('Generating {0}_hlpi.table'.format(name))
        write_if_changed(os.path.join(path, 'source', 'Hardware', 'Bricklets', name + '_hlpi.table'), make_hlpi_table(bricklet, 'bricklet'))

    print('Generating Device_Identifier.table')
    write_if_changed(os.path.join(path, 'source', 'Software', 'Device_Identifier.table'), make_device_identifier_table())

    for binding in bindings:
        if binding[2]:
            print('Generating API_Bindings_{0}_links.table'.format(binding[3]))
            write_if_changed(os.path.join(path, 'source', 'Software', 'API_Bindings_{0}_links.table'.format(binding[3])), make_api_bindings_links_table(binding))

if __name__ == "__main__":
    generate(os.getcwd())
