# system imports
import json
import requests
import configparser

# local imports
import utils


def download_data():
    """
    Downloads images from unsplash website.
    """
    images_list = []

    config = configparser.ConfigParser()

    if len(config.read('config.ini')) == 0:
        raise Exception('No config file found, you must create config first.')

    client_id = config.get('UNSPLASH', 'access_key', fallback='no_key')
    
    if client_id in (None, '', 'no_key'):
        raise Exception('No key is provided, please get your key.')

    try:
        for cnt in utils.progressbar(it=range(0, 1500, 30), prefix='Downloading'):
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
        with open('data/data3.json', 'w+') as writer:
            json.dump(images_list, writer, indent=4)
