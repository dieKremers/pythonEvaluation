from camera_threaded import MyPiVideoStream
from threading import Thread
import cv2

class MyTemplateSearcher:
	def __init__(self, templatePath='template_one.png'):
		# initialize the camera and stream
		self.vs = MyPiVideoStream()
		self.template = cv2.imread(templatePath)
		self.w, self.h = self.template.shape[::2]
		self.template = cv2.cvtColor(self.template, cv2.COLOR_RGB2GRAY)
		self.text = "Trefferwahrscheinlichkeit: "
		self.method = cv2.TM_CCOEFF_NORMED
		# initialize the frame and the variable used to indicate
		# if the thread should be stopped
		self.lastHit = None
		self.result = None
		self.stopped = False
		self.top_val = 0
		self.newHit = False
		
	def start(self):
		# start the thread to read frames from the video stream
		self.vs.start()
		Thread(target=self.update, args=()).start()
		return self
 
	def update(self):
		# keep looping infinitely until the thread is stopped
		while not (self.stopped):
			# grab the frame from the stream and clear the stream in
			# preparation for the next frame
			frame = self.vs.read()
			if( frame is None ):
                            continue
			frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
			#search for Template
			self.result = cv2.matchTemplate(frame, self.template, self.method)
			self.min_val, self.max_val, self.min_loc, self.max_loc = cv2.minMaxLoc(self.result)
			self.top_val = self.min_val
			if self.method == cv2.TM_SQDIFF_NORMED:
                            self.top_left = self.min_loc
                            self.text = self.text + str(self.min_val)
                        
			if self.method != cv2.TM_SQDIFF_NORMED:
				self.top_left = self.max_loc
				self.text = self.text + str(self.max_val)
				self.top_val = self.max_val

			self.bottom_right = (self.top_left[0] + self.w, self.top_left[1] + self.h)

			if(self.top_val > 0):
				cv2.rectangle(frame,self.top_left, self.bottom_right, 255, 2)
				cv2.putText(frame, self.text, (10 , 100), 0, 1, (1,1,1))
				self.lastHit = frame
				self.newHit = True
			# if the thread indicator variable is set, stop the thread
			# and resource camera resources
			if self.stopped:
				self.vs.stop()
				return

	def read(self):
		# return the frame most recently read
		if self.newHit:
			self.newHit = False
			return self.lastHit
		return None
                
 
	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
