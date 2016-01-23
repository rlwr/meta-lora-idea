SUMMARY = "Bluetooth scanner that sends info on LoRa"

SRC_URI = "	\
      file://bt_scanner.py  \
	   	file://lora_module.py \
	   	file://lora_serial.py"

LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://bt_scanner.py;beginline=3;endline=14;md5=ff620a27ab0c6eb3b80825033a352d8e"

RDEPENDS_${PN} = "python python-smbus"

#INSANE_SKIP_${PN} += "installed-vs-shipped"

S = "${WORKDIR}"

PREFIX = "/opt/lora-btscan"

do_install() {
	install -d ${D}/${PREFIX}

	install -m 644  ${S}/bt_scanner.py ${D}/${PREFIX}
  install -m 644  ${S}/lora_module.py ${D}/${PREFIX}
  install -m 644  ${S}/lora_serial.py ${D}/${PREFIX}
}

FILES_${PN} = "${PREFIX}/*.py"
