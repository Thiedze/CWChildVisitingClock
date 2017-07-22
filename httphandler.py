import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import configparser

class HttpHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		try:
			if self.path.endswith(".html"):
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
				return
			return
		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)
	
	def do_POST(self):
		self.config = configparser.ConfigParser()
		self.config.read('cwchildvisitingclock.properties')
		# Parse the form data posted
		form = cgi.FieldStorage(
			fp=self.rfile, 
			headers=self.headers,
			environ={'REQUEST_METHOD':'POST',
					 'CONTENT_TYPE':self.headers['Content-Type'],
					 })

		# Begin the response
		self.send_response(200)
		self.end_headers()

		# Echo back information about what was posted in the form
		for field in form.keys():
			field_item = form[field]
			if field == 'visit_time':
				self.wfile.write('Besuchszeit: ')
				self.wfile.write('%s\n' % (form[field].value))
				self.config['DEFAULT']['visitTime'] = form[field].value.replace(" ", "") + ':00'
			elif field == 'color_hours':
				self.wfile.write('Farbe Stunden: ')
				self.wfile.write('%s\n' % (form[field].value))
				self.config['DEFAULT']['hourcolor'] = str(int(form[field].value[1:3], 16)) + ',' + str(int(form[field].value[3:5], 16)) + ',' + str(int(form[field].value[5:7], 16))
			elif field == 'color_minutes':
				self.wfile.write('Farbe Minuten: ')
				self.wfile.write('%s\n' % (form[field].value))
				self.config['DEFAULT']['minutecolor'] = str(int(form[field].value[1:3], 16)) + ',' + str(int(form[field].value[3:5], 16)) + ',' + str(int(form[field].value[5:7], 16))
			elif field == 'color_seconds':
				self.wfile.write('Farbe Sekunden: ')
				self.wfile.write('%s\n' % (form[field].value))
				self.config['DEFAULT']['secondcolor'] = str(int(form[field].value[1:3], 16)) + ',' + str(int(form[field].value[3:5], 16)) + ',' + str(int(form[field].value[5:7], 16))

		with open('cwchildvisitingclock.properties', 'w') as configfile:
			self.config.write(configfile)
		return
