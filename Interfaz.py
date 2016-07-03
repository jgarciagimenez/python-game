#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import MySQLdb as db
import juego
Name = None


class Handler:

	Builder = None


	def __init__(self):
		
		self.Create = None        
		self.Read = None       
		self.Update = None        
		self.Delete = None

		self.builder = Gtk.Builder()
		self.builder.add_from_file("Interfaz.glade")

		self.handlers = { "on_window_destroy": self.on_window_destroy,
						  "onHelpActivate": self.onHelpActivate,       
						  "on_accept_dialog": self.on_accept_dialog,
						  "on_btn_info_comenzar_clicked": self.on_btn_info_comenzar_clicked,
						  "on_btn_info_cancel_clicked": self.on_btn_info_cancel_clicked,
						  "on_btn_main_accept_clicked": self.on_btn_main_accept_clicked,            
						  "on_btn_main_cancel_clicked": self.on_btn_main_cancel_clicked }

		self.builder.connect_signals(self.handlers)
		self.window = self.builder.get_object("window")
		self.info_dialog = self.builder.get_object("info_dialog")
		self.about_dialog = self.builder.get_object("about_dialog") 
		self.entry_name = self.builder.get_object("entry_name")

		self.window.show_all()

	def on_window_destroy(self, *args):
		print 'Se ha cerrado la ventana'
		Gtk.main_quit(*args)

	def onHelpActivate(self,*args):
		self.about_dialog.show()
	
	def on_accept_dialog(self,*args):
		self.about_dialog.hide()

	def on_btn_main_accept_clicked(self,*args):
		global Name
		Name = self.entry_name.get_text()
		self.entry_name.set_text('')
		self.info_dialog.show()

	def on_btn_main_cancel_clicked(self,*args):
		self.entry_name.set_text('')

	def on_btn_info_comenzar_clicked(self,*args):
		print "Se lanza el juego"
		juego.nivel1(Name)

	def on_btn_info_cancel_clicked(self,*args):
		self.info_dialog.hide()


def main():
    window = Handler()
    Gtk.main()
    return 0

if __name__ == '__main__':
    main()