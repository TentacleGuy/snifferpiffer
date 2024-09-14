import dearpygui.dearpygui as dpg
import pyfiglet
import time
#import serial
import set

# ASCII-Kunst mit pyfiglet
ascii_art = pyfiglet.figlet_format("SnifferPiffer v1.0")

# Funktion zum Beenden der Anwendung
def quit_app(sender, app_data):
    dpg.stop_dearpygui()

# Funktion zur Aktualisierung der Uhrzeit
def update_status():
    current_time = time.strftime("%H:%M:%S")
    current_frame = dpg.get_frame_count()
    dpg.set_value("status_time", f"Uhrzeit: {current_time}")
    dpg.set_value("status_frame", f"Frame: {current_frame}")

# Fenster erstellen
dpg.create_context()

# Hauptfenster mit Toolbar und Statusleiste
with dpg.window(label="SnifferPiffer v1.0", width=800, height=600, no_resize=False, no_close=True, no_collapse=True) as main_window:
    
    # Toolbar erstellen
    with dpg.menu_bar():
        with dpg.menu(label="Datei"):
            dpg.add_menu_item(label="Neu")
            dpg.add_menu_item(label="Öffnen")
            dpg.add_menu_item(label="Speichern")
            dpg.add_menu_item(label="Beenden", callback=quit_app)
        with dpg.menu(label="Bearbeiten"):
            dpg.add_menu_item(label="Einstellungen")
        with dpg.menu(label="Ansicht"):
            dpg.add_menu_item(label="Zoom")
            dpg.add_menu_item(label="Volle Bildschirmgröße")

    # Scrollbarer Bereich für den Inhalt
    with dpg.child_window(autosize_x=True, height=-25, border=True, horizontal_scrollbar=False):  # Höhe anpassen, um Platz für Statusleiste zu lassen
        with dpg.group(horizontal=False):
            dpg.add_text(ascii_art, tag="ascii_text", wrap=780)  # Anpassen der Breite

    # Statusleiste unten (immer sichtbar)
    with dpg.group(horizontal=True):
        dpg.add_text("SnifferPiffer v1.0", tag="status_info")
        dpg.add_spacer(width=100)  
        dpg.add_text("Frame ", tag="status_frame")
        dpg.add_spacer(width=100)  
        dpg.add_text("Uhrzeit: --:--:--", tag="status_time")

    
# Starten des Fensters
dpg.create_viewport(title='SnifferPiffer v1.0', width=800, height=600)
dpg.setup_dearpygui()
dpg.set_primary_window(main_window, True)
dpg.show_viewport()

#MAINLOOP
while dpg.is_dearpygui_running():
    if dpg.get_frame_count() % set.FRAMERATE == 0:
        update_status()

    dpg.render_dearpygui_frame()

dpg.destroy_context()
