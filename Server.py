from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import cv2

# ======================== CONFIG =========================
PORT = 8360
HOSTNAME = '127.0.0.1'
DEVICE = 0 # TODO PUT THIS IN UI
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


class CameraRequestHandler(SimpleHTTPRequestHandler):
	def do_GET(self):
		# All requests must contain '360'
		if '360' in self.path:
			if self.path.endswith('live.mjpg'):
				self.send_response(200)
				live(self)
			elif self.path.endswith('jpg'):
				self.send_response(200)
				picture(self)
		else:
			SimpleHTTPRequestHandler.do_GET(self)

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

	try:
		server = HTTPServer((HOSTNAME,PORT),CameraRequestHandler)
		print("Sphere2Pano Server started\nGo to http://" + HOSTNAME + ":" + str(PORT) + " to start.")
		server.serve_forever()
	except KeyboardInterrupt:
		server.socket.close()
		capture.release()

if __name__ == '__main__':
	main()