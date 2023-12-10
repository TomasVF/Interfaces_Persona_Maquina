#!/usr/bin/env python3

from sys import argv
import string
from typing import Optional
import cheathelper
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import ast
import textwrap
from state import State
from view import View   
import threading     
import locale
import gettext
from pathlib import Path

class Presenter:
    def __init__(self, state: Optional[State]= None):
        state = state or State()
        self.state = state
        self.view = View()

    def run(self) -> None:
        app = Gtk.Application(application_id= "es.udc.fic.ipm.HelloWorld")
        app.connect('activate', self.on_activate)
        app.run(None)

    def on_activate(self, app: Gtk.Application) -> None:
        self.view.build(app, self)
        
    #función de llamada al state para realizar un cambio y de la posterior actualización de la vista
    def new_command(self, entrada) -> None:
        self.state.change_command(entrada)
        self.view.show_saying_indicator(False)
        if self.state.get_command().startswith ("\nHay problemas de conexión"):
            self.view.error_red()
        else:
            self.view.update_label(self.state.get_entrada(), self.state.get_command())
            
            
    #función del botón reintentar después de un error de red
    def on_ClickRedError(self, button):
        self.new_command(self.state.get_entrada())
        
    #función acitvada al buscar en la barra de búsqueda
    def on_enter(self, entry) -> None:
        entrada = entry.get_text()
        self.view.show_saying_indicator(True)
        threading.Thread(target=self.new_command,args=(entrada,)).start()
        #self.new_command(entrada)
        
    #función activada al seleccionar un elemento en el desplegable del historial
    def on_select(self, comboBox) -> None:
        entrada = comboBox.get_active_text()
        self.view.show_saying_indicator(True)
        threading.Thread(target=self.new_command,args=(entrada,)).start()
        #self.new_command(entrada)         
    
        
if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    LOCALE_DIR = Path(__file__).parent / "locale"
    locale.bindtextdomain('trabajoIPM', LOCALE_DIR)
    gettext.bindtextdomain('trabajoIPM', LOCALE_DIR)
    gettext.textdomain('trabajoIPM')
    presenter = Presenter()
    presenter.run()

