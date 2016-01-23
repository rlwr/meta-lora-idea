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


import smbus
import time


#######################################
# Constants
#######################################

# I2C bus number
# 0 = /dev/i2c0, ...
BUS_NUMBER = 1

# I2C device address
# Note: 7 bit address (will be left-shifted to add the read write bit)
DEVICE_ADDRESS = 0x48

# Number of failed attempts when reading a string (sleeps 1ms in between)
TIMEOUT_RETRIES = 500

# Enable verbose debug
VERBOSE = True
VERBOSE_DUMP_REGS = False


#######################################
# Globals
#######################################

bus = ''


#######################################
# Private functions
#######################################

def _read_reg(reg):
    data = bus.read_byte_data(DEVICE_ADDRESS, reg)

    if VERBOSE_DUMP_REGS is True:
            print "SERIAL - READ  reg = %4s" % (hex(reg))
    return data

def _write_reg(reg, data):
    if VERBOSE_DUMP_REGS is True:
        print "SERIAL - WRITE reg = %4s, data = %4s" % (hex(reg), hex(data))

    return bus.write_byte_data(DEVICE_ADDRESS, reg, data)

# Sends a character converted to its hex code
def _send_char(c):
    return _write_reg(0x00, ord(c)) # Xmit Holding Register THR

def _flush():
    if VERBOSE is True:
        print "SERIAL - Flush"

    _write_reg(0x10, 0x07) #  FIFO Control Register in WRITE Mode (FCR) : reset TXFIFO, reset RXFIFO, enable FIFO mode


#######################################
# Public functions
#######################################

def init_serial():
    global bus
    bus = smbus.SMBus(BUS_NUMBER)

    # TODO: process return values
    _write_reg(0x18, 0x80) # Line Control Register (LCR): 0x80 to program baud rate divisor
    _write_reg(0x00, 0x03) # Divisor Latch LSB (DLL) 0x03 =38.42 kbauds with X1=1.8MHz
    _write_reg(0x08, 0x00) # Divisor Latch MSB (DLH)
    _write_reg(0x18, 0x03) # Line Control Register (LCR):  8 data bits, 1 stop bit, no parity
    _write_reg(0x10, 0x07) # FIFO Control Register in WRITE Mode (FCR) : reset TXFIFO, reset RXFIFO, enable FIFO mode

    _flush()

    if VERBOSE is True:
        print "SERIAL - SC16IS752 initialized at 38400 bps"

def receive_string():
    data = ''
    retries = TIMEOUT_RETRIES

    while retries > 0:
        # See if data is waiting
        val = _read_reg(0x28)    # Line status Register (LSR)
        if (val & 0x1) == 0x01:
            bytes_left = _read_reg(0x48) #  FIFO Level Register (RXLVL)

            i = bytes_left
            while i > 0:
                c = chr(_read_reg(0x00)) # Recv Holding Register (RHR)
                data += c
                i -= 1

            if c == '\n' and bytes_left == 0:
                break

            # Reset timeout
            retries = TIMEOUT_RETRIES
        else:
            time.sleep(0.001)
            retries -= 1

    return data

def send_string(s):
    if VERBOSE is True:
        print "SERIAL - Sending: " + s

    level_before = _read_reg(0x40)  # Xmit FIFO Level Register (TXLVL)
    
    for c in s:
        _send_char(c)
    _send_char('\n')

    level_after = _read_reg(0x40)   # Xmit FIFO Level Register(TXLVL)
    nb = level_before - level_after

    if VERBOSE is True:
        print "SERIAL - TX Fifo Level before=%d, after=%d,nb char written=%d\n" % (level_before,level_after,nb)

    # TODO: return value, catch exceptions



