#!/usr/bin/python2

import gobject
import dbus
import dbus.mainloop.glib

from subprocess import call

def activeChangedHandler(active):
	if (active):
		print("Locking other screen")
		call(["ssh", "-n", "-f", "3rd_screen", "DISPLAY=:0.0", "nohup", "/usr/bin/slock", "2>&1", ">", "/dev/null", "<", "/dev/null", "&"])
	else:
		print("Unlocking other screen")
		call(["ssh", "3rd_screen", "/usr/bin/killall", "slock"])

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


