#!/usr/bin/python2

import gobject
import dbus
import dbus.mainloop.glib

def activeChangedHandler(active):
	if (active):
		print("Screen Locked")
	else:
		print("Screen Unlocked")

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


