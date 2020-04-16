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

# package imports
from PIL import Image
import pandas as pd

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


def _get_image_files_list():
    """
    Get a list of all images from `data/json` folder.
    """
    images_list = []
    
    # find all images
    json_files = sorted(pathlib.Path('data/json').glob('data*.json'))
    for json_file in json_files:
        with open(json_file, 'r') as reader:
            raw_json = json.load(reader)
            images_list.extend(raw_json)
    
    return images_list, json_files


def get_df():
    """
    Returns a dataframe of the json in data/json folder.
    """
    images_list, json_files = _get_image_files_list()
    
    return pd.DataFrame(images_list)


def download_images(quality='regular'):
    """
    Downloads images from given image quality.
    
    Parameters:
    quality : Options are raw | full | regular | small | thumb

    For more information about quality, check unsplash documentation at
    https://unsplash.com/documentation#example-image-use
    """
    images_list, json_files = _get_image_files_list()
    
    # print information
    print('Found {0} images in {1} files. Starting to download...'.format(
        len(images_list), len(json_files)))
    print('This may take a while.')

    # download images -  this is where downloading happens
    for image in utils.progressbar(it=images_list, prefix='Downloading '):
        id = image['id']
        url_quality = image['urls'][quality]
        image_path = pathlib.Path(f'data/images/{id}.jpg')
        if image_path.exists():
            image_path.unlink()
        response = requests.get(url_quality, stream=True)
        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                f.write(response.content)

    # final
    print('Done!')


def create_thumbnail(size=(128, 128)):
    """
    Create resized version of the image path given, with the same name 
    extended with _thumbnail.
    """
    images_list, json_files = _get_image_files_list()
    Image.MAX_IMAGE_PIXELS = None

    # print information
    print('Found {0} images in {1} files. Starting for processing...'.format(
        len(images_list), len(json_files)))
    print('This may take a while.')

    # processing - this is where processing of an image happens
    for image in utils.progressbar(it=images_list, prefix='Processing '):        
        id = image['id']
        image_path = pathlib.Path(f'data/images/{id}.jpg')

        if image_path.exists():
            # create thumbnail
            image = Image.open(image_path.absolute())
            image.thumbnail(size)

            # save thumbnail
            new_filename = image_path.parent.joinpath(
                '{0}_thumbnail{1}'.format(image_path.stem, image_path.suffix))
            image.convert('RGB').save(new_filename)
    
    # final
    print('Done!')
