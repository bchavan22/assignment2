import json
import requests
import configparser


def create_config_file(access_key='', secret_key=''):
    """
    Creates a config file for secret stuff. Option to provide keys.

    Parameters:
    access_key: Unsplash access key.
    secret_key: Unsplash secret key.
    """
    config = configparser.ConfigParser()
    config['UNSPLASH'] = dict(access_key=access_key, secret_key=secret_key)

    with open('config.ini', 'w+') as configfile:
        config.write(configfile)
    
    print('A new file is created. Please fill your access_key.')


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
        cnt = 0
        while(cnt < 1500):
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
                cnt += len(raw_json)
                images_list.extend(raw_json)
                print(f'raw: {len(raw_json)} list: {len(images_list)}')

            elif response.status_code == 403:
                print('api limit reached!')
                break
            else:
                print('something went wrong!')
                break
        
    except KeyboardInterrupt:
        print('Operation interrupted by user.')
    except Exception as ex:
        print('Something went wrong', ex)
    finally:
        with open('data/data3.json', 'w+') as writer:
            json.dump(images_list, writer, indent=4)