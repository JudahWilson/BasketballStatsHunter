import os
from dotenv import load_dotenv 
load_dotenv()
import time
import subprocess
import tkinter as tk

if 'METABASE_PATH' in os.environ:
    METABASE_PATH = os.environ['METABASE_PATH']
else:
    METABASE_PATH = r"C:\Users\Judah\My Drive\Programming\StatBucketWebApp\backend\metabase\metabase.jar"
metabase_popen: subprocess.Popen
ngrok_popen: subprocess.Popen
def start_frontend():
    # Run this in the background
    metabase_popen = subprocess.Popen(f'java -jar "{METABASE_PATH}"', shell=True)
    ngrok_popen = subprocess.Popen('ngrok http --domain=judahwilson.ngrok.io 3000')
    
def stop_frontend():
    metabase_popen.terminate()
    ngrok_popen.terminate()
    
# TODO implement tkinter GUI