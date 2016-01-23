#! /usr/bin/python

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>

import lora_serial

def start():
    lora_serial.init_serial()

    # Start radio in RF mode (not LoRaWAN)
    lora_serial.send_string("AT+RF=ON\n")
    print lora_serial.receive_string()

    # Set LoRa parameters
    # Freq 868100000, TX power 14dbm, bandwidth 125KHz, SF7
    lora_serial.send_string("AT+RFTX=SET,LORA,868100000,14,125000,7")
    print lora_serial.receive_string()

    # Get LoRa parameters
    lora_serial.send_string("AT+RFTX=?\n")
    print lora_serial.receive_string()

def stop():
    lora_serial.send_string("AT+RF=OFF\n")
    print lora_serial.receive_string()

# Send text string
# Note: do not know how to escape ',' '{', ...
def send(msg):
    lora_serial.send_string("AT+RFTX=SNDTXT," + msg + ",1")
    print lora_serial.receive_string()

# Send text string encoded as hex
def send_bin(msg):
    msg = msg.encode("hex").upper()
    lora_serial.send_string("AT+RFTX=SNDBIN," + msg + ",1")
    print lora_serial.receive_string()

# Send "CAFE" (hex message)
def send_cafe(msg):
    lora_serial.send_string("AT+RFTX=SNDBIN,CAFE,1")
    print lora_serial.receive_string()

# TODO: Other commands
#  lora_serial.send_string("AT+MAC=HELP\n")
#  print lora_serial.receive_string()

#  lora_serial.send_string("AT+DEBUG=MVON\n")
#  print lora_serial.receive_string()

#  lora_serial.send_string("AT+DEBUG=MVER\n")
#  print lora_serial.receive_string()

