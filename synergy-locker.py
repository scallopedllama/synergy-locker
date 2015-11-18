#!/usr/bin/python2

import gobject
import dbus
import dbus.mainloop.glib

from subprocess import call

def activeChangedHandler(active):
	if (active):
		print("Locking other screen")
		call(["ssh", "-n", "-f", "3rd_screen", "/usr/bin/loginctl list-sessions | grep seat | awk '{print $1}' | xargs -l1 loginctl lock-session"])
		call(["ssh", "-n", "-f", "3rd_screen", "DISPLAY=:0.0 xset dpms force off"])
	else:
		print("Unlocking other screen")
		call(["ssh", "-n", "-f", "3rd_screen", "/usr/bin/loginctl list-sessions | grep seat | awk '{print $1}' | xargs -l1 loginctl unlock-session"])
		call(["ssh", "-n", "-f", "3rd_screen", "DISPLAY=:0.0 xset dpms force on"])

if __name__ == '__main__':
	
	dbus.mainloop.glib.DBusGMainLoop(set_as_default = True)
	
	bus = dbus.SessionBus()
	
	try:
		object = bus.get_object("org.freedesktop.ScreenSaver", "/org/freedesktop/ScreenSaver")
		object.connect_to_signal("ActiveChanged", activeChangedHandler, dbus_interface="org.freedesktop.ScreenSaver")
	except dbus.DBusException:
		traceback.print_exc()
		sys.exit(1)
	
	loop = gobject.MainLoop()
	loop.run()


