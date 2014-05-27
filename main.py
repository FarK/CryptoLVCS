from kivy.app import App
from kivy.uix.image import Image as WImage
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.factory import Factory
from msgbox import *
from LVCS.api import *
from image.processor import *
from kivy.vector import Vector
import os

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    filechooser = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
	FloatLayout.__init__(self, *args, **kwargs)

	self.filechooser.filters = ['*.png']	
	self.filechooser.path = os.path.dirname(os.path.abspath(__file__))

class MainWidget(BoxLayout):
	text_input = ObjectProperty(None)
	secret_image = ObjectProperty(None)
        algorithm = ObjectProperty(None)
	parameters = ObjectProperty(None)
        shades = ObjectProperty(None)
	result_image = ObjectProperty(None)

	valid_algorithms = ['DVCS','LVCS-DVCS','LVCS-PVCS']
	valid_parameters = {'(2,2)':(2,2,None),'(2,3)':(2,3,None),'(3,3)':(3,3,6)}
	
	generate_counter = 0

	def validate(self):
		return self.parameters.text in self.valid_parameters.keys() and \
		       self.algorithm.text in self.valid_algorithms
	 
	def clean_dir(self,folder):

		for the_file in os.listdir(folder):
    			file_path = os.path.join(folder, the_file)
    			try:
        			if os.path.isfile(file_path):
            				os.unlink(file_path)
    			except Exception, e:
        			pass	
		
	def generateShadows(self):
		if self.validate():
		   k = self.valid_parameters[self.parameters.text][0]
		   n = self.valid_parameters[self.parameters.text][1]
		   m = self.valid_parameters[self.parameters.text][2]

		   if self.algorithm.text == self.valid_algorithms[1] or \
                      self.algorithm.text == self.valid_algorithms[2]:

			image = Image.open(self.secret_image.source)
			(w,h) = image.size
                        
			if self.algorithm.text == self.valid_algorithms[1]:
			    shades_info = LVCS_DVCS(image=image, k=k, n=n, m=m)
			elif self.algorithm.text == self.valid_algorithms[2]:
			    shades_info = LVCS_PVCS(image=image, k=k, n=n, m=m)

			self.shades.clear_widgets()
			
			pos = (0,0)
			result = None
			self.clean_dir('./temp')
			for i in range(0,len(shades_info)):
				#get shades
				shade_info = shades_info[i]
				shade = addtext(shade_info, None, w, rows = h, alpha=True)
				path = './temp/shade%s%s.png'%(self.generate_counter,i)
				 
				#shave images
				shade.save(path, 'PNG')
				
				#set spacing of the container
				self.shades.spacing = self.size[0]*float(0.1)/len(shades_info)
				rw = float(0.9) / len(shades_info)
				wimage = Factory.Image(
						source=path, 
						allow_stretch=True,
						size_hint=(rw,1)
					)
		

				wimage.pos = pos
				self.shades.add_widget(wimage)
				dx = self.size[0] / len(shades_info)
				pos = (pos[0] + dx + self.spacing, 0)

				if result is None:
					result = addtext(shade_info, None, w, rows=h, alpha=False)
				else:
					result = overlaping(addtext(shade_info, None, w, rows=h, alpha=False),
						            result)
		   elif self.algorithm.text == self.valid_algorithms[0]:

			image = Image.open(self.secret_image.source)
			(w,h) = image.size
                        
			shades_info = DVCS(image=image, k=k, n=n, m=m)
			self.shades.clear_widgets()
			
			pos = (0,0)
			result = None
			self.clean_dir('./temp')
			for i in range(0,len(shades_info)):
				#get shades
				shade_info = shades_info[i]
				shade = get_image(shade_info, image = None, w = w, h = h, alpha=True)
				path = './temp/shade%s%s.png'%(self.generate_counter,i)
				 
				#shave images
				shade.save(path, 'PNG')
				
				#set spacing of the container
				self.shades.spacing = self.size[0]*float(0.1)/len(shades_info)
				rw = float(0.9) / len(shades_info)
				wimage = Factory.Image(
						source=path, 
						allow_stretch=True,
						size_hint=(rw,1)
					)
		

				wimage.pos = pos
				self.shades.add_widget(wimage)
				dx = self.size[0] / len(shades_info)
				pos = (pos[0] + dx + self.spacing, 0)

				if result is None:
					result = get_image(shade_info, image=None, w=w, h=h, alpha=False)
				else:
					result = overlaping(get_image(shade_info, 
							image=None, w=w, h=h, alpha=False),
						            result)

			if not result is None:
				result.save('./temp/result%s.png'%self.generate_counter, 'PNG')
				self.result_image.source = './temp/result%s.png'%self.generate_counter

			self.generate_counter += 1
		else:
		   
		   msg = MsgBox(text='You should set the algorithm and\n the parameters and load a secret image')
		   msg.open()


    	def dismiss_popup(self):
        	self._popup.dismiss()

	def show_load(self):
	        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        	self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        	self._popup.open()

    	def load(self, path, filename):
		self.secret_image.source = os.path.join(path, filename[0])
		self.secret_image.keep_ratio = False

        	#with open(os.path.join(path, filename[0])) as stream:
            	#	self.id_loadImageText.text = stream.read()
        	self.dismiss_popup()

class ShadeLayout(FloatLayout):
	currentImage = None

	def on_touch_move(self, touch):
		try:
			if not self.currentImage is None:
				(dx, dy) = touch.dpos
				(cx, cy) = self.currentImage.pos
				newx = cx + dx
				newy = cy
		
				if self.collide_point(newx,newy):
					self.currentImage.pos = (newx, newy)

				for ch in self.children:
					if not ch is self.currentImage:
						(x,y) = ch.pos
						d = Vector(ch.pos).distance(self.currentImage.pos) 
						if d < 20:
							self.currentImage.pos = ch.pos[:]
							self.currentImage = None
		except:
			pass
			
	def on_touch_up(self, touch):
		self.currentImage = None

	def on_touch_down(self, touch):
		try:
			for ch in self.children:
				if ch.collide_point(*touch.pos):
					self.currentImage = ch
				
					for ch in self.children:
						if not ch is self.currentImage:
							(x,y) = self.currentImage.pos
							d = Vector(ch.pos).distance(self.currentImage.pos) 
							if d < 20:
								self.currentImage.pos = (x+21,y)
								self.currentImage = None
								pass
			
					pass

		except:
			pass
class Shade(WImage):
	moving = False
	
	def on_touch_move(self,touch):
		if self.moving:
			(dx, dy) = touch.dpos
			(cx, cy) = self.pos
			newx = cx + dx
			newy = cy + dy 

			(pw, ph) = self.parent.size

			if newx > 0 and newy > 0 and \
                   	   newx < pw and newy < ph:
		  		self.pos = (newx, newy)

		
			print self.pos

        def on_touch_up(self, touch):
		self.moving = False
		
	def on_touch_down(self, touch):
		(px, py) = self.process_pos(touch.pos) 
		(cx, cy) = self.pos
		(w,h) = self.size

		print (px,py)
		print self.pos
		print self.size

		if px > cx and py > cy and \
		   px < cx + w and py < cy + h:
			self.moving = True
			print 'moving'
		print '-----------'

	def process_pos(self, pos):
		(x,y) = pos
		(px,py) = self.parent.pos
		print 'Parent pos: %s,%s'%(px,py)
		return (x-px, y-py)

class MainApp(App):
	def build(self):
		return MainWidget()

if __name__ == '__main__':
	MainApp().run()

Factory.register('Shade', cls=Shade)
Factory.register('ShadeLayout', cls=ShadeLayout)
