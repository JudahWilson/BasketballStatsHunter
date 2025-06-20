'''Fire up metabase and ngrok for the frontend to be public.'''
import subprocess
import os 
os.chdir('metabase')
subprocess.Popen(['java', '-jar', 'metabase.jar'])
subprocess.Popen(['ngrok', 'http', '--domain=judahwilson.ngrok.io', '3000'])