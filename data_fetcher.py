import requests
import os 
from dotenv import load_dotenv
load_dotenv()
MiR_Token = os.getenv("MiR_Token")
import time
from PyQt5.QtCore import QThread, pyqtSignal

class DataFetcher(QThread):
    dataFetched = pyqtSignal(dict)

    def __init__(self, ip_address):
        super().__init__()
        self.ip_address = ip_address
        self.host = f'http://{self.ip_address}/api/v2.0.0/'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic  {MiR_Token}'
        }
        self.running = True

    def fetch_data(self, endpoint):
        try:
            response = requests.get(f'{self.host}{endpoint}', headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'Error fetching {endpoint}: {response.status_code} - {response.text}')
                return None
        except requests.exceptions.RequestException as e:
            print(f'An error occurred fetching {endpoint}: {e}')
            return None

    def run(self):
        while self.running:
            status_data = self.fetch_data('status')
            if status_data:
                # Assuming the endpoint returns a flat dictionary; modify as necessary
                data = {
                    #"joystick_low_speed_mode_enabled": status_data.get('joystick_low_speed_mode_enabled', False),
                    #"mission_queue_url": status_data.get('mission_queue_url', ''),
                    #"mode_id": status_data.get('mode_id', 0),
                    #"moved": status_data.get('moved', 0),
                    #"mission_queue_id": status_data.get('mission_queue_id', 0),
                    #"robot_name": status_data.get('robot_name', 'Unknown'),
                    #"joystick_web_session_id": status_data.get('joystick_web_session_id', ''),
                    #"uptime": status_data.get('uptime', 0),
                    "errors": status_data.get('errors', []),
                    #"unloaded_map_changes": status_data.get('unloaded_map_changes', 0),
                    #"distance_to_next_target": status_data.get('distance_to_next_target', 0.0),
                    #"serial_number": status_data.get('serial_number', 'N/A'),
                    #"mode_key_state": status_data.get('mode_key_state', 'N/A'),
                    "battery_percentage": status_data.get('battery_percentage', 0.0),
                    #"map_id": status_data.get('map_id', 0),
                    #"safety_system_muted": status_data.get('safety_system_muted', False),
                    "mission_text": status_data.get('mission_text', 'N/A'),
                    "state_text": status_data.get('state_text', 'N/A'),
                    "velocity": status_data.get('velocity', 0.0),
                    #"footprint": status_data.get('footprint', 'N/A'),
                    #"user_prompt": status_data.get('user_prompt', 'N/A'),
                    #"allowed_methods": status_data.get('allowed_methods', []),
                    #"robot_model": status_data.get('robot_model', 'N/A'),
                    #"mode_text": status_data.get('mode_text', 'N/A'),
                    #"session_id": status_data.get('session_id', 'N/A'),
                    #"state_id": status_data.get('state_id', 0),
                    #"battery_time_remaining": status_data.get('battery_time_remaining', 0),
                    "position": status_data.get('position', {"x": 0.0, "y": 0.0})
                }
                self.dataFetched.emit(data)
            time.sleep(2)  # Adjust the sleep interval as needed

    def stop(self):
        self.running = False
