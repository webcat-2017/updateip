import sys
import logging
import win32event
import win32serviceutil
import win32service
import servicemanager
import configparser
import time
import winreg as reg
import requests

class UpdateIP(win32serviceutil.ServiceFramework):
    _svc_name_ = 'AgentLA'
    _svc_display_name_ = 'AgentLA'
    _svc_description_ = 'Lazy admin agent 1.0'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.isAlive = True

        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Services\\UpdateIP") as h:
            self.path = reg.EnumValue(h, 3)[1].strip("uip_service.exe")

        self.config = configparser.ConfigParser()
        self.config.read(self.path + 'config.ini', encoding='utf-8')

        logging.basicConfig(
            level=logging.INFO,
            filename=self.path + "logfile.log",
            format='[UpdateIP] %(asctime)s %(levelname)s %(message)s')

    def main(self):
        while self.isAlive:
            try:
                url = self.config['settings']["url"]
                res = requests.get(url)
                logging.info(res.status_code)

            except Exception as e:
                logging.error(e)
            time.sleep(60)

    def SvcDoRun(self):
        self.isAlive = True
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        logging.info('start Service')
        self.main()
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def SvcStop(self):
        self.isAlive = False
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        logging.info('stop Service')
        win32event.SetEvent(self.hWaitStop)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(UpdateIP)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(UpdateIP)
