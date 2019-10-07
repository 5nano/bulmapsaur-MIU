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

def get_files_sorted_by_modified(dirpath):
    a = [s for s in os.listdir(dirpath)
         if os.path.isfile(os.path.join(dirpath, s))]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return a

for image_name in get_files_sorted_by_modified(images_directory):

       with open(os.path.join(images_directory,image_name), "rb") as image:

            print('Image name', image_name)
           
            # print('Building b64 ...')
            # base64_bytes = b64encode(image.read())
            # base64_string = base64_bytes.decode(ENCODING)
            
            # print('Requesting to', destination_url)
            # try:
            #     resp = requests.post(destination_url, 
            #             json={
            #                     'idAssay': id_assay,
            #                     'idExperiment': id_experiment,
            #                     'base64': base64_string
            #                 })
            #     print(resp)
            # except Exception as e:
            #     print(e)
            
            # #Espero unos minutos para volver a enviar otra imagen
            # print('Waiting', wait_seconds, 'seconds')
            # time.sleep(wait_seconds)
