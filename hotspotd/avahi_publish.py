import dbus
import avahi
import threading
import gobject
from dbus.mainloop.glib import DBusGMainLoop
from misc import *

domain = "" # Domain to publish on, default to .local
host = "" # Host to publish records for, default to localhost


log_src = "AvahiPublish"

class AvahiPublisherThread(threading.Thread):
    def run(self):
        Log.i(log_src, "Starting Avahi Publisher")
        self.group = None
        self.name = avahi_service_name
        self.rename_count = 12 # Counter so we only rename after collisions a sensible number of times

        ml = DBusGMainLoop(set_as_default=False)
        self.main_loop = gobject.MainLoop()
        gobject.threads_init() # otherwise other threads will block

        self.bus = dbus.SystemBus(mainloop=ml)

        self.server = dbus.Interface(
            self.bus.get_object(avahi.DBUS_NAME, avahi.DBUS_PATH_SERVER),
            avahi.DBUS_INTERFACE_SERVER)

        self.server.connect_to_signal("StateChanged", self.server_state_changed)
        self.server_state_changed(self.server.GetState())

        try:
            self.main_loop.run()
        except Exception:
            pass

        if self.group is not None:
            self.group.Free()

    def stop(self):
        Log.i(log_src, "Stopping Avahi Publisher")
        self.main_loop.quit()
        self.join()

    def add_service(self):
        if self.group is None:
            self.group = dbus.Interface(
                    self.bus.get_object(avahi.DBUS_NAME, self.server.EntryGroupNew()),
                    avahi.DBUS_INTERFACE_ENTRY_GROUP)
            self.group.connect_to_signal('StateChanged', self.entry_group_state_changed)

        Log.d(log_src, "Adding service '{0}' of type '{1}' ...".format(self.name, avahi_service_type))

        self.group.AddService(
                avahi.IF_UNSPEC,    #interface
                avahi.PROTO_INET, #protocol
                dbus.UInt32(0),                  #flags
                self.name, avahi_service_type,
                domain, host,
                dbus.UInt16(avahi_service_port),
                avahi.string_array_to_txt_array([avahi_service_TXT]))
        self.group.Commit()

    def remove_service(self):
        if self.group is not None:
            self.group.Reset()

    def server_state_changed(self, state):
        if state == avahi.SERVER_COLLISION:
            Log.w(log_src, "WARNING: Server name collision")
            self.remove_service()
            self.stop()
        elif state == avahi.SERVER_RUNNING:
            self.add_service()

    def entry_group_state_changed(self, state, error):
        Log.d(log_src, "state change: {0}".format(state))

        if state == avahi.ENTRY_GROUP_ESTABLISHED:
            Log.d(log_src, "Service established.")

        elif state == avahi.ENTRY_GROUP_COLLISION:
            self.rename_count = self.rename_count - 1
            if self.rename_count > 0:
                self.name = self.server.GetAlternativeServiceName(self.name)
                Log.w(log_src, "WARNING: Service name collision, changing name to '{0}' ...".format(self.name))
                self.remove_service()
                self.add_service()

            else:
                Log.e(log_src, "ERROR: No suitable service name found after {0} retries, exiting.".format(12))

        elif state == avahi.ENTRY_GROUP_FAILURE:
            Log.e(log_src, "Error in group state changed {0}".format(error))
            return
