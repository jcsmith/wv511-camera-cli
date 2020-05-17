#!/usr/bin/env python3

import json
import requests
from prettytable import PrettyTable


def get_resource_info():
    r = requests.get('http://wv511.org/rest/unifiedEntityService/ids')

    results = json.loads(r.text)['result']

    return(results)

def get_camera_ids(resource_info):
    return ([f['serverId'] for f in [d['ids'] for d in resource_info if 'CameraBean' in d['entityName']][0]])


def get_camera_info(camera_ids):

    #Create haders
    http_headers = { 
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.5',
            'X-HTTP-Method-Override': 'POST',
            'Content-Type': 'application/json',
            'Origin': 'http://wv511.org',
            'Connection': 'keep-alive',
            'Referer': 'http://wv511.org/',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
            }


    #Craete update list from camera_ids
    update_list = [{"routeInfo":"queue://CameraBean.rpc", "serverId":camera_id} for camera_id in camera_ids]

    #build payload for post request
    post_data = {}
    post_data['descriptors'] = {}
    post_data['descriptors']['com.orci.opentms.web.public511.components.camera.shared.data.CameraBean'] = {}
    post_data['descriptors']['com.orci.opentms.web.public511.components.camera.shared.data.CameraBean']['timestamp'] = 0
    post_data['descriptors']['com.orci.opentms.web.public511.components.camera.shared.data.CameraBean']['adds'] = []
    post_data['descriptors']['com.orci.opentms.web.public511.components.camera.shared.data.CameraBean']['updates'] = update_list
    post_data['descriptors']['com.orci.opentms.web.public511.components.camera.shared.data.CameraBean']['deletes'] = []

    r = requests.post('http://wv511.org/rest/unifiedEntityService/updateByDescriptor', data=json.dumps(post_data), headers=http_headers)

    return (json.loads(r.text)['changes']['com.orci.opentms.web.public511.components.camera.shared.data.CameraBean']['changes'])


resource_info = get_resource_info()
camera_info = get_camera_info(get_camera_ids(resource_info))


camera_url_list = [{ 'Description': entity['entity']['description'], 'streamURL': entity['entity']['realTimeStreamUrl']} for entity in camera_info]

print (camera_url_list)

PT= PrettyTable()
PT.field_names = ['Description', 'Stream URL' ]
PT.align['Description'] = 'l'
PT.align['Stream URL'] = 'l'

for cam in camera_url_list:
    PT.add_row([cam['Description'], cam['streamURL']])

print (PT)
