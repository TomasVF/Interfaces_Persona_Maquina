#!/usr/bin/env python3

from __future__ import annotations
from typing import Optional
import ast
import cheathelper

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


# Vamos a aplicar el patrón MVP

# El componente estado/modelo se reduce a una clase.
class State:
    command: string= ""

   


# El componente vista se reduce a una clase y una función.
def get_command(count: int) -> str:
    return (
        "I've said hello 1 time" if count == 1 else
        f"I've said hello {count} times"
    )



class View:
    WINDOW_PADDING: int = 24

    label: Gtk.Label = None
    comboBox: Gtk.ComboBoxText = None

    # Esta no es la única forma de implementar esta parte. Por
    # ejemplo, en vez de pasar el Presenter como parámetro, podíamos
    # tener un método `View.connect_to(:Presenter)`
    def build(self, app: Gtk.Application, presenter: 'Presenter') -> None:
        win = Gtk.ApplicationWindow(
            title= "cheat.sh",
        )    
        app.add_window(win)
        win.connect("destroy", lambda win: win.close())
        win.add(self.counter(presenter))
        win.show_all()

    def counter(self, presenter: 'Presenter') -> Gtk.Widget:
        box = Gtk.Box(
            orientation= Gtk.Orientation.VERTICAL,
            homogeneous= False,
            spacing= 20,
            margin_top= 0,
            margin_end= 0,
            margin_bottom= View.WINDOW_PADDING,
            margin_start= View.WINDOW_PADDING
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
        label = Gtk.Label(
            label= "ERROR",
            halign= Gtk.Align.START,
            vexpand= True
        )
        
        label1 = Gtk.Label(
            label= "Comando no encontrado, revise si lo ha escrito correctamente",
            halign= Gtk.Align.START,
            vexpand= True
        )
       
        buttonAyuda = Gtk.Button(
            label= "Ayuda",
        )
        buttonOpciones = Gtk.Button(
            label= "Opciones",
        )
        buttonRefresh = Gtk.Button(
            label= "Refrescar",
        )
        entry = Gtk.Entry()
        entry.set_size_request(200, 50)
        entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "system-search-symbolic")
        comboBox=Gtk.ComboBoxText()
        entry.connect('activate', presenter.on_enter)
        
        boxBotones.pack_end(buttonAyuda, True, True, 0)
        boxBotones.pack_end(buttonOpciones, True, True, 0)
        boxBusqueda.pack_start(entry, True, True, 0)
        boxBusqueda.pack_start(comboBox, True, True, 0)
        box.pack_start(boxBotones, True, True, 0)
        box.pack_start(boxBusqueda, True, True, 0)
        box.pack_start(label, True, True, 0)
        box.pack_start(label1, True, True, 0)
        self.comboBox = comboBox
        self.label = label
       
        return box 
        
    def change_label(self, newLabel: string) -> None:
     self.label.set_label(newLabel)
     self.comboBox.insert_text(1, newLabel)


# Finalmente el Presenter
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
        # La vista es totalmente pasiva. El presenter se encarga de
        # actualizarla en todo momento.
       
        
        
    def on_enter(self, entry) -> None:
     entrada = entry.get_text()
    
     entrych = " " + entrada
     ast.literal_eval(entrych)
     exec(open("cheathelper.py").read(),entrych)


    def botón_ayuda(self,buttonAyuda):
        Gtk.main(quit)
   
    def botón_opciones(self,buttonOpciones):
        Gtk.main(quit)

        
if __name__ == '__main__':
    presenter = Presenter()
    presenter.run()
