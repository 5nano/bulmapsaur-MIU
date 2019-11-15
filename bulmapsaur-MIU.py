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

args = vars(parser.parse_args())
images_directory = args["dir"]
destination_url = args["url"]
wait_seconds = args["sec"]


ENCODING = 'utf-8'

headers = {'content-type': 'application/json','origin':'localhost'}

def get_files_sorted_by_modified(dirpath):
    a = [s for s in os.listdir(dirpath)
         if os.path.isfile(os.path.join(dirpath, s))]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return a                


for image_name in get_files_sorted_by_modified(images_directory):

       with open(os.path.join(images_directory,image_name), "rb") as image:
            
            print('Image name:', image_name)

            full_path = images_directory.split("/")
            date_position = len(full_path) - 1
            date = full_path[date_position]
            idAssay = full_path[date_position -1 ]
            
            idExperiment = image_name.split(".jpg")[0]
            print("Date directory " + date)
            print("IdAssay " + idAssay)
            print('Id experiment:', idExperiment)
           
            print('Building b64 ...')
            base64_bytes = b64encode(image.read())
            base64_string = base64_bytes.decode(ENCODING)
            
            print('Requesting to', destination_url)
            body = {
                  'idAssay': idAssay,
                  'idExperiment': idExperiment,
                  'base64': base64_string,
                  'optionalTime': date + " " + "08:15:27.243860"
                }
            try:
                resp = requests.post(destination_url, 
                        json=body,
                       headers=headers)
                print(resp)
            except Exception as e:
                print(e)
            
            #Espero unos minutos para volver a enviar otra imagen
            print('Waiting', wait_seconds, 'seconds')
            time.sleep(wait_seconds)
