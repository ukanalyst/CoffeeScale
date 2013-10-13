CoffeeScale
===========

Read a USB scale with RaspBerryPi store the data in a database and display coffee status. 
 


Requirements / Setup Commands
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install apache2
sudo apt-get install libusb-1.0
sudo apt-get install mysql-server
sudo apt-get install python-mysqldb
sudo apt-get install php5
sudo apt-get install php5-mysql
sudo apt-get install  phpmyadmin
sudo apt-get -y install ssh python apache2 libusb-1.0 mysql-server python-mysqldb php5 php5-mysql phpmyadmin
want arrays in python? use numpy
apt-get install -y python-numpy
 

PYUSB
https://github.com/walac/pyusb
wget https://github.com/walac/pyusb/archive/master.zip
unzip master.zip
 cd pyusb-master/
./setup.py install
 

mysql
when you install it above it will ask for a password - the username associated with that password is "root"
use phpmyadmin to create a database and tables http://rasp.unival.com/phpmyadmin/
Tables

--
-- Database: `coffeedb`
--
-- --------------------------------------------------------
--
-- Table structure for table `scales`
--


CREATE TABLE IF NOT EXISTS `scales` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `scale_name` varchar(255) NOT NULL,
  `vendor_id` varchar(64) NOT NULL,
  `product_id` varchar(64) NOT NULL,
  `serialno` varchar(255) NOT NULL,
  `data_mode_grams` varchar(32) NOT NULL,
  `data_mode_ounces` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;



--
-- Table structure for table `readings`
--
CREATE TABLE IF NOT EXISTS `readings` (
  `reading_time` datetime NOT NULL,
  `reading_value` int(11) NOT NULL,
  `scale_id` int(11) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reading_units` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=105 ;

Connect the Scale
run dmesg to see if it is connected. the output should be almost exactly like this:
 

[61539.300131] usb 1-1.2.1.4: new full-speed USB device number 6 using dwc_otg
[61539.405516] usb 1-1.2.1.4: New USB device found, idVendor=0922, idProduct=8004
[61539.405548] usb 1-1.2.1.4: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[61539.405568] usb 1-1.2.1.4: Product: M25 25 lb Digital Postal Scale
[61539.405584] usb 1-1.2.1.4: Manufacturer: DYMO
[61539.405596] usb 1-1.2.1.4: SerialNumber: 0000000022159
[61539.437452] generic-usb 0003:0922:8004.0001: hiddev0: USB HID v1.01 Device [DYMO M25 25 lb Digital Postal Scale] on usb-bcm2708_usb-1.2.1.4/input0

bash script to extract the vendor id and product id (would be nice to use python to parse dmesg to grab the stuffs but that may not be feasible)
in fact this may not be necessary as the scale id's are always the same...
# this gets just the vendor id
dmesg | grep -B6 DYMO | grep idVendor | cut -d"=" -f2 | cut -d"," -f1
# this gets just the Product id
dmesg | grep -B6 DYMO | grep idProduct | cut -d"=" -f3
Trouble
caused by udev permissions:
python /usr/local/coffee/readscale.py
usb.core.USBError: [Errno 13] Access denied (insufficient permissions)
the fix:
sudo vi /etc/udev/rules.d/98-dymo.rules
$ sudo cat /etc/udev/rules.d/98-dymo.rules
SUBSYSTEM=="usb", ATTR{idVendor}=="0922", ATTR{idProduct}=="8004", MODE="666"
Read the Scale
what if you have more than one scale?
according to pyusb documentation, usb devices sometimes have "bus" and "address" identifiers
devices = usb.core.find(find_all=True, idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
sys.stdout.write('There are ' + str(len(devices)) + ' scales connected!\n')
if len(devices) > 1:
	print "more than one scale found"
else:
	print "devices bus: " + str(devices[0].bus)
	print "device address: " + str(devices[0].address)
 
they also show serial numbers and here is how to get them
devices = usb.core.find(find_all=True, idVendor=VENDOR_ID)
sys.stdout.write('There are ' + str(len(devices)) + ' scales connected!\n')
scales=[]
i=1
for device in devices:
	scalename="scale "+str(i)
	print "scale #" + str(i)
	devbus = str(device.bus)
	devaddr = str(device.address)
	productid=str(device.idProduct)
# help found here http://stackoverflow.com/questions/5943847/get-string-descriptor-using-pyusb-usb-util-get-string
	serialno = str(usb.util.get_string(device,256,3))
	manufacturer = str(usb.util.get_string(device,256,1))
	description = str(usb.util.get_string(device,256,2))
read the scale should output just one number: the weight in grams
 

update 
02/8/2013
the SD card died so I have a new SD card and am glad I checked the code in 
I am trying "mobiuslinux" for the distro this time: http://moebiuslinux.sourceforge.net/ it is smaller and has no graphical stuff. I may come to need graphical stuff but for now just the basics will hopefully make a faster updating thinger
this required installing python! apt-get install python -y 
 

 

 

 

 

 

 

 