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
import locale
import gettext
from pathlib import Path


_ = gettext.gettext
N_ = gettext.ngettext



class View:
    WINDOW_PADDING: int = 24

    label: Gtk.Label = None
    comboBox: Gtk.ComboBoxText = None
    stack: Gtk.Stack = None
    spinner: Gtk.Spinner = None

    def build(self, app: Gtk.Application, presenter: 'Presenter') -> None:
        win = Gtk.ApplicationWindow(
            title= "cheat.sh",
        )    
        app.add_window(win)
        win.connect("destroy", lambda win: win.close())
        win.add(self.counter(presenter))
        win.show_all()
        win.set_size_request(1000, 500)

    def counter(self, presenter: 'Presenter') -> Gtk.Widget:
    	#creacion de las distintas cajas usadas para almacenar los widgets
        box = Gtk.Box(
            orientation= Gtk.Orientation.VERTICAL,
            homogeneous= False,
            spacing= 20,
            margin_top= 0,
            margin_end= View.WINDOW_PADDING,
            margin_bottom= View.WINDOW_PADDING,
            margin_start= View.WINDOW_PADDING
        )
        boxChange1 = Gtk.Box(
            orientation= Gtk.Orientation.VERTICAL,
            homogeneous= False,
            spacing= 0
        )
        boxChange2 = Gtk.Box(
            orientation= Gtk.Orientation.VERTICAL,
            homogeneous= False,
            spacing= 50
        )
        boxChange3 = Gtk.Box(
            orientation= Gtk.Orientation.VERTICAL,
            homogeneous= False,
            spacing= 20
        )
        boxBusqueda = Gtk.Box(
            orientation= Gtk.Orientation.HORIZONTAL,
            homogeneous= False,
            spacing= 0
        )
        boxBotones = Gtk.Box(
            orientation= Gtk.Orientation.HORIZONTAL,
            homogeneous= False,
            spacing= 0
        )
        boxLabel = Gtk.Box(
            orientation= Gtk.Orientation.VERTICAL,
            homogeneous= False,
            spacing= 20,
             margin_start= View.WINDOW_PADDING
        )
        
        #creacion de los distintos mensajes de error y el texto del resultado de busqueda
        label = Gtk.Label()
        labelRed = Gtk.Label (label = _("\nThere are connection problems"))
        textAyuda = Gtk.Label(label = _("This application shows all the information available about the uses of the linux commands and their different options. \nYou have to write the name of the command and be connected to the internet. \nIf you need more information, go to https://cheat.sh"))
        
        
        
        #creacion de los distintos botones
        
        #boton ayuda
        buttonAyuda = Gtk.Button.new_with_label(
            label= _("Help"),
        )
        buttonAyuda.connect("clicked", self.on_clickAyuda)
        
        #boton reintentar
        buttonReintentar = Gtk.Button(
            label= _("Retry"),
            vexpand = False,
            hexpand = False
        )
        buttonReintentar.connect("clicked", presenter.on_ClickRedError)
        
        #boton inicio
        buttonOpciones = Gtk.Button.new_with_label(label= _("Beginning"))
        buttonOpciones.connect("clicked", self.on_ClickInicio)
        
        
        
        
        #titulo
        labelTitle = Gtk.Label()
        labelTitle.set_markup('<b><span size = "xx-large"> CHEAT.SH></span></b>')
        
        #titulo
        labelTitle2 = Gtk.Label()
        labelTitle2.set_markup('<b><span size = "xx-large"> CHEAT.SH></span></b>')
        
        #texto ayuda
        labelAyuda = Gtk.Label()
        labelAyuda.set_markup('<b><span size = "xx-large">' + _("HELP") + '</span></b>')
        
        #barra de busqueda
        entry = Gtk.Entry(
            hexpand = True,
            vexpand = False)
        entry.set_size_request(200, 50)
        entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "system-search-symbolic")
        entry.connect('activate', presenter.on_enter)
        
        #desplegable con el historial de busqueda
        comboBox=Gtk.ComboBoxText()
        comboBox.connect("changed", presenter.on_select)
        
        #caja con los botones y el titulo
        boxBotones.pack_end(buttonAyuda, False, True, 0)
        boxBotones.pack_end(buttonOpciones, False, True, 0)
        
        #caja con los widgets barra de busqueda y desplegable de historial
        boxBusqueda.pack_start(entry, False, True, 0)
        boxBusqueda.pack_start(comboBox, False, True, 0)
        
        #creacion del spinner de espera de busqueda
        spinner = Gtk.Spinner(hexpand= False)
        spinner.hide()
        
        #caja con el texto resultante de la busqueda
        boxLabel.pack_start(spinner, False, True, 0)
        boxLabel.pack_start(label, False, True, 0)
        
        #anadido la barra de scroll a la caja del texto
        scrolled_window = Gtk.ScrolledWindow(vexpand = True)
        scrolled_window.add(boxLabel)
        scrolled_window.show()
        
        #caja con los widget de la pantalla de busqueda
        boxChange1.pack_start(labelTitle, False, True, 0)
        boxChange1.pack_start(boxBusqueda, False, True, 0)
        boxChange1.pack_start(scrolled_window, False, True, 0)
        
        #caja con los widget de la pantalla de ayuda
        boxChange2.pack_start(labelAyuda, False, True, 0)
        boxChange2.pack_start(textAyuda, False, True, 0)
        
        #caja con los widget de la pantalla de error de red
        boxChange3.pack_start(labelTitle2, False, True, 0)
        boxChange3.pack_start(labelRed, False, False, 0)
        boxChange3.pack_start(buttonReintentar, False, False, 0)
        
        #creacion del stack para cambiar entre pantallas
        stack = Gtk.Stack()
        stack.add_named(boxChange1, "busqueda")
        stack.add_named(boxChange2, "ayuda")
        stack.add_named(boxChange3, "redError")
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        stack.set_visible_child_name("busqueda")
        
        #caja principal donde estan los widgets que siempre estan presentes, en nuestro caso el stack con la pantalla visible y los botones
        box.pack_start(boxBotones, False, True, 0)
        box.pack_start(stack_switcher, False, True, 0)
        box.pack_start(stack, False, True, 0)
        
        self.comboBox = comboBox
        self.label = label
        self.stack = stack
        self.spinner = spinner
        return box 
        
    def show_saying_indicator(self, showing: bool) -> None:
        if showing:
            self.label.set_label(_("Counting ..."))
            self.spinner.show()
            self.spinner.start()
        else:
            self.spinner.stop()
            self.spinner.hide()
        
    def update_label(self,entrada: str, command) -> None:
        self.label.set_label(command)
        self.comboBox.insert_text(1, entrada)
        self.stack.set_visible_child_name("busqueda")
     
    def on_clickAyuda(self,button):
        self.stack.set_visible_child_name("ayuda")
       
    def on_ClickInicio(self,button):
        self.stack.set_visible_child_name("busqueda")
        
    def error_red(self):
        self.stack.set_visible_child_name("redError")

