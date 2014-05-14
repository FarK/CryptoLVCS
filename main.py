from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

class MainWidget(BoxLayout):

	def generateShadows(button):
		print "Shadows generated:"
		print "\tn = " + button.ids.id_n.text
		print "\tk = " + button.ids.id_k.text
		print "\tm = " + button.ids.id_m.text

	def loadImage(button, text):
		print "Image \"" + text + "\" loaded"

class MainApp(App):
	def build(self):
		return MainWidget()

if __name__ == '__main__':
	MainApp().run()
