#!/usr/bin/python

# this reports the latest scale reading so the web page can grab it

import MySQLdb as mdb
import os
import sys
print "Content-type: text/html\n\n"

debug = 1 
con = None
full = float(1700)
empty = float(198) 
try:
	## connect to the database
	con = mdb.connect('localhost', 'coffeeuser', 'coffee16', 'coffeedb');
	cur = con.cursor(mdb.cursors.DictCursor)
	# get scale info from the database
	# how many scales are there? 

	#for each scale, get its reading and add it to the database
	cur.execute("select id,serialno,scale_name from scales")
	scalerows = cur.fetchall()
	serialnos={}
	for scale in scalerows:
		serialnos[scale["serialno"]]=scale["id"] 

	for s,i in serialnos.items():		
		serialno=str(s)
		scale_id=str(i)
		## put the readings into columns
		if int(scale_id) & 1: 
			print "<div id=\"left\" >\n"
		else:
			print "<div id=\"right\" >\n"
			
		print "scale id "+ scale_id+" serial: "+ serialno + "\n" #" named: " + scale_name + "\n"
		# get most recently added reading
		if not cur.execute("select * from readings where reading_time = (select MAX(reading_time) from readings where scale_id = '"+scale_id+"' )"):
			lastreading=0
			if debug: print "no reading found for scale "+ scale_id + "<br/>\n"
		else:
			# this should produce ONE row but in case it does not I'll refer to the rows by their numeric index
			rows = cur.fetchall() # fetchall so we can refer to the columns by name
			reading_time = rows[0]["reading_time"]
			#if debug: print reading_time
			lastreading = float(rows[0]["reading_value"])
			units=rows[0]["reading_units"]

		if debug: print "\n<br />reading from database"+"<br />\n"
		if debug: print "most recent reading time: " + str(reading_time) +"<br />\n"
		if debug: print "most recent value : " + str(lastreading) + units +"<br />\n"

		print "<br />\n"
		print "full is " + str(full) + "<br />\n"
		print "empty is " + str(empty) + "<br />\n"
		print "CURRENT READING: " + str(lastreading) + units +"<br />\n"
		
		### calculate fullness
		if lastreading == 0 or lastreading < (empty + 10) :
			print "water bottle missing<br />\n"
			pctfull = 0
			pctpx = 0
		elif lastreading == empty :
			print "water bottle empty<br />\n"
			pctfull = 0 
			pctpx = 0
		else:
			print "there are " + str(lastreading-empty) +"g of water<br />\n"
			pctfull = (((lastreading-empty) / full)*100)
			#pctfull = round((((lastreading - empty) / full)*100),2)
			print str(pctfull)+"% full<br />\n"
			pctpx = int(500 * ((lastreading - empty) / full))
		print """
			<div class="graph">
				<div>
				  <!-- height would be percent times 5 -->
					  <div style="height: 520px;width:1px;" class="barholder"></div>
		"""
		print "			  <div id=\"scale"+scale_id+"\" style=\"height: "+ str(pctpx) +"px;\" class=\"bar\"></div>"
		print """
				</div>
			</div>
			</div>
		"""


except mdb.Error, e:
  
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
		