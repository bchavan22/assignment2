"""
Image Handler Functions
=========================
A set of functions to download data, images, and process images.

Usage:

``` py
import images

# downloads data in JSON format
images.download_data()
```
"""
# system imports
import json
import pathlib
import requests
import datetime
import configparser

# local imports
import utils


def download_data():
    """
    Downloads images meta information from unsplash website as JSON.
    """
    images_list = []

    config = configparser.ConfigParser()

    if len(config.read('config.ini')) == 0:
        raise Exception('No config file found, you must create config first.')

    client_id = config.get('UNSPLASH', 'access_key', fallback='no_key')
    
    if client_id in (None, '', 'no_key'):
        raise Exception('No key is provided, please get your key.')

    try:
        for cnt in utils.progressbar(it=range(0, 1500, 30), prefix='Downloading '):
            response = requests.get(
                f'https://api.unsplash.com/photos/random/?count=30', 
                headers={
                    'Accept-Version': 'v1',
                    'Authorization': f'Client-ID {client_id}'
                },
                stream=True
            )
            
            if response.status_code == 200:
                raw_json = json.loads(response.content)
                images_list.extend(raw_json)

            elif response.status_code == 403:
                print('Api limit reached!')
                break
            else:
                print('Something went wrong!')
                break
        
    except KeyboardInterrupt:
        print('Operation interrupted by user.')
    except Exception as ex:
        print('Something went wrong', ex)
    finally:
        append_timestamp = round(datetime.datetime.now().timestamp())
        with open(f'data/json/data_{append_timestamp}.json', 'w+') as writer:
            json.dump(images_list, writer, indent=4)


def download_images():
    """
    Downloads images from given image 
    """
    images_list = []
    
    # find all images
    json_files = list(pathlib.Path('data/json').glob('data*.json'))
    for json_file in json_files:
        with open(json_file, 'r') as reader:
            raw_json = json.load(reader)
            images_list.extend(raw_json)
    
    # print information
    print('Found {0} images in {1} files. Starting to download...'.format(
        len(images_list), len(json_files)))
    print('This may take a while.')

    # download images
    for image in utils.progressbar(it=images_list, prefix='Downloading '):
        id = image['id']
        url_raw = image['urls']['raw']
        response = requests.get(url_raw, stream=True)
        if response.status_code == 200:
            with open(pathlib.Path(f'data/images/{id}.jpg'), 'wb') as f:
                f.write(response.content)

    return images_list