from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
import os

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MainWidget(BoxLayout):
	text_input = ObjectProperty(None)
	secret_image = ObjectProperty(None)
        algorithm = ObjectProperty(None)
	parameters = ObjectProperty(None)
	valid_algorithms = ['LVCS-DVCS']
	valid_parameters = {'(2,2)':(2,2),'(2,3)':(2,2),'(3,3)':(3,3)}
	def validate(self):
		return self.parameters.text in self.valid_parameters.keys() and \
		       self.algorithm.text in self.valid_algorithms
	 
		
	def generateShadows(button):
		print "Shadows generated:"
		if button.validate():
			print 'OK'

	def loadImage(button, text):
		print "Image \"" + text + "\" loaded"

    	def dismiss_popup(self):
        	self._popup.dismiss()

	def show_load(self):
	        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        	self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        	self._popup.open()

    	def load(self, path, filename):
		self.secret_image.source = os.path.join(path, filename[0])
        	#with open(os.path.join(path, filename[0])) as stream:
            	#	self.id_loadImageText.text = stream.read()
        	self.dismiss_popup()

class MainApp(App):
	def build(self):
		return MainWidget()

if __name__ == '__main__':
	MainApp().run()
