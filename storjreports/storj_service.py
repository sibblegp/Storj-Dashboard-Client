import win32service
import win32serviceutil
import win32event
import win32evtlog
from time import sleep
import nt
import winreg
import zipimport
import ntpath
import win32con
import winerror
import pywintypes
import _win32sysloader
import servicemanager
from storjreports import send_storj_reports


class PySvc(win32serviceutil.ServiceFramework):
    # you can NET START/STOP the service by the following name
    _svc_name_ = "StorKDashSVC"
    # this text shows up as the service name in the Service
    # Control Manager (SCM)
    _svc_display_name_ = "StorJDash Client Service"
    # this text shows up as the description in the SCM
    _svc_description_ = "StorJDash.com client service for reporting StorJ storage"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        # create an event to listen for stop requests on
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

        # core logic of the service


    def SvcDoRun(self):

        #servicemanager.LogInfoMsg('Starting to run')
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        #servicemanager.LogInfoMsg('Opening File')
        #f = open('test.dat', 'w+')
        rc = None

        #servicemanager.LogInfoMsg('Entering While Loop')
        # if the stop event hasn't been fired keep looping
        while rc != win32event.WAIT_OBJECT_0:
            send_storj_reports.windows_main()
            #sleep(1000)
            # block for 5 seconds and listen for a stop event
            rc = win32event.WaitForSingleObject(self.hWaitStop, 3600000)

        #servicemanager.LogInfoMsg('Exiting While Loop')
        #f.write('SHUTTING DOWN\n')
        #f.close()

        # called when we're being shut down

    def SvcStop(self):
        # tell the SCM we're shutting down
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # fire the stop event
        win32event.SetEvent(self.hWaitStop)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(PySvc)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(PySvc)