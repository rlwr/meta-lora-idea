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

import subprocess
import json

import lora_module

def run_cmd(cmd):
    return subprocess.check_output(cmd)

# Scan BT devices and return JSON list
def parse_hcitool(s):
    devs = []

    lines = s.splitlines()[1:]

    for l in lines:
        if not l:
            continue

        d = {}
        d['a'] = l.split()[0] # Address
        d['n'] = l.split()[1] # Name
        devs.append(d)

    return json.dumps(devs)

# Make sure BT is enabled
print ">>>> BT: enabling Bluetooth"
run_cmd(["rfkill", "unblock", "bluetooth"])
# Scan BT devices around
print ">>>> BT: scanning devices"
s = run_cmd(["hcitool", "scan"])
s_js = parse_hcitool(s)

# Send LoRa message
print ">>>> LORA: sending message"
lora_module.start()
lora_module.send_bin(s_js)
lora_module.stop()

print ">>>> DONE"

