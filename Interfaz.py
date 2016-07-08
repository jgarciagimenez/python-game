#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import juego
import MySQLdb as db

Name = None


# Database 
db_host = "localhost"
db_user = "jose"
db_pass = "juego"
db_data = "DBjuego"

Conexion = db.connect(db_host,db_user,db_pass,db_data)
micursor = Conexion.cursor(db.cursors.DictCursor)



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
						  "on_top_score_activate": self.on_top_score_activate,
						  "on_btn_top_close_clicked": self.on_btn_top_close_clicked,
						  "on_btn_info_comenzar_clicked": self.on_btn_info_comenzar_clicked,
						  "on_btn_info_cancel_clicked": self.on_btn_info_cancel_clicked,
						  "on_btn_main_accept_clicked": self.on_btn_main_accept_clicked,            
						  "on_btn_main_cancel_clicked": self.on_btn_main_cancel_clicked }

		self.builder.connect_signals(self.handlers)
		self.window = self.builder.get_object("window")
		self.info_dialog = self.builder.get_object("info_dialog")
		self.about_dialog = self.builder.get_object("about_dialog") 
		self.entry_name = self.builder.get_object("entry_name")
		self.top_score = self.builder.get_object("top_score")

		self.label1 = self.builder.get_object("label1")
		self.label2 = self.builder.get_object("label2")
		self.label3 = self.builder.get_object("label3")
		self.label4 = self.builder.get_object("label4")
		self.label5 = self.builder.get_object("label5")

		self.labels_top = [self.label1, self.label2, self.label3, self.label4, self.label5]

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

	def on_btn_top_close_clicked(self,*args):
		self.top_score.hide()


	def on_top_score_activate(self,*args):
		self.top_score.show()

		query = "SELECT * FROM Puntuaciones  ORDER BY Puntuacion DESC"
		micursor.execute(query)
		registros= micursor.fetchmany(size = 4)
		Conexion.commit()
		a = 0
		for registro in registros:
			self.labels_top[a].set_text(registro['Nombre'] + ":  " + str(registro['Puntuacion']))
			a+=1


def main():
    window = Handler()
    Gtk.main()
    return 0

if __name__ == '__main__':
    main()