from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import cv2
import numpy as np
import urlparse
from math import sqrt

# ======================== CONFIG =========================
PORT = 8360
HOSTNAME = '127.0.0.1'
DEVICE = 0 # TODO PUT THIS IN UI
DEST_WIDTH = 2048 # TODO PUT THIS IN UI
DEST_HEIGHT = 512 # TODO PUT THIS IN UI
# =========================================================

BOUNDARY = '--ILOVETOPARTYWITHMJPG'

def picture(self):
	rc,img = capture.read()
	rc,cv2mat = cv2.imencode(".jpg",img)
	jpeg = cv2mat.tostring() + "\r\n\r\n\r\n"
	self.wfile.write((
		"Content-Type: image/jpeg\r\n"
		"Content-Length: "+str(len(jpeg))+"\r\n\r\n"
		+jpeg
	))

def live(self):
	self.wfile.write((
		"Cache-Control: no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0\r\n"
		"Connection: close\r\n"
		"Pragma: no-cache\r\n"
		"Expires: Mon, 3 Jan 2000 12:34:56 GMT\r\n"
		"Content-Type: multipart/x-mixed-replace; boundary=%s\r\n\r\n" % BOUNDARY
	))

	while True:
		try:
			rc,img = capture.read()
			if not rc:
				continue
			rc,cv2mat = cv2.imencode(".jpg",img)
			jpeg = cv2mat.tostring() 
			self.wfile.write((
				BOUNDARY + "\r\n"
				"Content-Type: image/jpeg\r\n"
				"Content-Length: "+str(len(jpeg + "\r\n\r\n"))+"\r\n\r\n"
				+ jpeg + "\r\n\r\n\r\n"
			))
		except Exception, e:
			raise e
			break

def panorama(self):
	self.wfile.write((
		"Cache-Control: no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0\r\n"
		"Connection: close\r\n"
		"Pragma: no-cache\r\n"
		"Expires: Mon, 3 Jan 2000 12:34:56 GMT\r\n"
		"Content-Type: multipart/x-mixed-replace; boundary=%s\r\n\r\n" % BOUNDARY
	))

	while True:
		try:
			rc,img = capture.read()
			if not rc:
				continue
			#bigImg = cv2.resize(img, (0, 0), fx=SCALE, fy=SCALE, interpolation=cv2.INTER_CUBIC)
			img2 = cv2.remap(img,map_x,map_y,cv2.INTER_AREA)
			rc,cv2mat = cv2.imencode(".jpg",img2)
			jpeg = cv2mat.tostring() 
			self.wfile.write((
				BOUNDARY + "\r\n"
				"Content-Type: image/jpeg\r\n"
				"Content-Length: "+str(len(jpeg + "\r\n\r\n"))+"\r\n\r\n"
				+jpeg + "\r\n\r\n\r\n"
			))
		except Exception, e:
			raise e
			break

def rift(self):
	self.wfile.write((
		"Cache-Control: no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0\r\n"
		"Connection: close\r\n"
		"Pragma: no-cache\r\n"
		"Expires: Mon, 3 Jan 2000 12:34:56 GMT\r\n"
		"Content-Type: multipart/x-mixed-replace; boundary=%s\r\n\r\n" % BOUNDARY
	))

	while True:
		try:
			rc,img = capture.read()
			if not rc:
				continue
			#bigImg = cv2.resize(img, (0, 0), fx=SCALE, fy=SCALE, interpolation=cv2.INTER_CUBIC)
			remap[511:1023, 0:2048, 0:3] = cv2.remap(img,map_x,map_y,cv2.INTER_AREA)
			rc,cv2mat = cv2.imencode(".jpg",remap)
			jpeg = cv2mat.tostring() 
			self.wfile.write((
				BOUNDARY + "\r\n"
				"Content-Type: image/jpeg\r\n"
				"Content-Length: "+str(len(jpeg + "\r\n\r\n"))+"\r\n\r\n"
				+jpeg + "\r\n\r\n\r\n"
			))
		except Exception, e:
			raise e
			break
			

def buildMap(self, x, y, width, height):
	global map_x
	global map_y
	map_x = np.zeros((DEST_HEIGHT,DEST_WIDTH),np.float32)
	map_y = np.zeros((DEST_HEIGHT,DEST_WIDTH),np.float32)
	
	cx = x + (width / 2)
	cy = y + (height / 2)
	R = int(min(width, height) / 2)

	for dy in range(0, int(DEST_HEIGHT-1)):
		for dx in range(int(DEST_WIDTH-1), 0, -1):
			r = sqrt(float(dy)/float(DEST_HEIGHT)) * R
			theta = (float(dx)/float(DEST_WIDTH)) * 2.0 * np.pi
			xS = cx + r*np.sin(theta)
			yS = cy - r*np.cos(theta)
			map_x.itemset(DEST_HEIGHT - (dy+1), DEST_WIDTH - (dx+1), int(xS))
			map_y.itemset(DEST_HEIGHT - (dy+1), DEST_WIDTH - (dx+1), int(yS))

class CameraRequestHandler(SimpleHTTPRequestHandler):
	def do_GET(self):
		# All requests must contain '360'
		if '360' in self.path:
			if self.path.endswith('live.mjpg'):
				self.send_response(200)
				live(self)
			elif self.path.endswith('pano.mjpg'):
				self.send_response(200)
				panorama(self)
			elif self.path.endswith('rift.mjpg'):
				self.send_response(200)
				rift(self)
			elif self.path.endswith('jpg'):
				self.send_response(200)
				picture(self)
		else:
			SimpleHTTPRequestHandler.do_GET(self)

	def do_POST(self):
		length = int(self.headers.getheader('content-length'))
		postvars = urlparse.parse_qs(self.rfile.read(length), keep_blank_values=1)
		buildMap(self, int(postvars['x'][0]), int(postvars['y'][0]), int(postvars['w'][0]), int(postvars['h'][0]))

		self.send_response(303)
		self.wfile.write('Location: panorama.html')
		self.end_headers()
		self.wfile.write(postvars)

def main():
	global capture
	capture = cv2.VideoCapture(DEVICE)

	global CAM_WIDTH
	CAM_WIDTH = capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
	global CAM_HEIGHT
	CAM_HEIGHT = capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)

	capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
	capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)

	global img
	global remap
	remap = np.zeros((DEST_HEIGHT + DEST_HEIGHT,DEST_WIDTH, 3),np.uint8)

	try:
		server = HTTPServer((HOSTNAME,PORT),CameraRequestHandler)
		print("Sphere2Pano Server started\nGo to http://" + HOSTNAME + ":" + str(PORT) + " to start.")
		server.serve_forever()
	except KeyboardInterrupt:
		server.socket.close()
		capture.release()

if __name__ == '__main__':
	main()