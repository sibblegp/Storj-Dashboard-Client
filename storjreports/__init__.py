from storjreports import send_storj_reports
from storjreports import register_server

def run_reports():
    send_storj_reports.main()

def register():
    register_server.gather_information()