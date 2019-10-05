import os
import json
import time
from base64 import b64encode
import requests
import argparse

parser = argparse.ArgumentParser(description='Read images from directory and send them as bulmapsaur body')

parser.add_argument('-d','--dir', type=str, required=True,
                   help='Directory of images')
parser.add_argument('-u','--url', type=str, required=True,
                   help='Url to post data')
parser.add_argument('-s','--sec', type=int,required=True,
                   help='Seconds to wait between images to send')
parser.add_argument('-ia','--idAssay', type=str,required=True,
                   help='Assay identifier')
parser.add_argument('-ie','--idExperiment', type=str, required=True,
                   help='Experiment identifier identifier')     

args = vars(parser.parse_args())
images_directory = args["dir"]
destination_url = args["url"]
wait_seconds = args["sec"]
id_assay = args["idAssay"]
id_experiment = args["idExperiment"]

ENCODING = 'utf-8'

with os.scandir(images_directory) as images_names:

    for image_name in images_names:
        
        with open(image_name, "rb") as image:
           
            print('Building b64 ...')
            base64_bytes = b64encode(image.read())
            base64_string = base64_bytes.decode(ENCODING)
            
            print('Requesting to', destination_url)
            try:
                resp = requests.post(destination_url, 
                        json={
                                'idAssay': id_assay,
                                'idExperiment': id_experiment,
                                'base64': base64_string
                            })
                print(resp)
            except Exception as e:
                print(e)
            
            #Espero unos minutos para volver a enviar otra imagen
            print('Waiting', wait_seconds, 'seconds')
            time.sleep(wait_seconds)
