import requests
from dotenv import load_dotenv
import os

# Get from .env
load_dotenv()
API_KEY = os.getenv('TOKEN')
# URL for the MyAnimeList API
BASE_URL = 'https://api.myanimelist.net/v2/'

# Get the user's anime list
def get_anime_list(user_name, limit=5, sort='list_score', status='completed', offset=0, api_key=API_KEY):
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    params = {
        'nsfw': 'true',
        'fields': 'list_status',
        'status': status,
        'limit': limit,
        'sort': sort,
        'offset': offset,
    }

    # Make a get request
    response = requests.get(f'{BASE_URL}users/{user_name}/animelist', headers=headers, params=params)

    if response.status_code == 200:
        anime_list = response.json().get('data')
        scores = [anime['list_status']['score'] for anime in anime_list]
        titles = [anime['node']['title'] for anime in anime_list]
        anime_list = 'Your Anime List:'
        for score, title in zip(scores, titles):
            anime_list += f'\n{title} - {score}'
        return anime_list
    else:
        print(f'Error: {response.status_code} - {response.text}')
        return None

# Update the user's anime status in their list
def update_anime_status(anime_title, status = None, score = None, is_rewatching = None, api_key=API_KEY):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    params = {
        'status': status,
        'score': score,
        'is_rewatching': int(is_rewatching) if is_rewatching is not None else None,
    }
    
    # Get anime ID from title
    anime_id = get_anime_id(anime_title)
    if anime_id is None:
        print('Anime not found - Invalid title or API key.')
    
    # Make a put request    
    response = requests.put(f'{BASE_URL}anime/{anime_id}/my_list_status', headers=headers, data=params)
    
    if response.status_code == 200:
        output = 'Anime status updated successfully!'
        for param, value in params.items():
            if value is not None:
                output += f'\n{param}: {value}'
        return output
    else:
        print(f'Error: {response.status_code} - {response.text}')
        return None

# Helper function to get the anime ID from the title        
def get_anime_id(anime_title, api_key=API_KEY):
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    params = {
        'nsfw': 'true',
        'q': anime_title,
        'limit': 15,
    }
    
    # Make a get request
    response = requests.get(f'{BASE_URL}anime', headers=headers, params=params)
    
    if response.status_code == 200:
        # Only get the ID of the closest match
        anime_id = response.json().get('data')[0]['node']['id']
        for anime in response.json().get('data'):
            if anime['node']['title'].lower() == anime_title.lower():
                anime_id = anime['node']['id']
                break
        return anime_id
    else:
        print(f'Error: {response.status_code} - {response.text}')
        return None

# Get the seasonal anime list
def get_seasonal_anime(year, season, limit=5, sort='list_score', api_key=API_KEY):
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    params = {
        'nsfw': 'true',
        'fields': 'list_status',
        'limit': limit,
        'sort': sort,
    }
    
    response = requests.get(f'{BASE_URL}anime/season/{year}/{season}', headers=headers, params=params)
    
    if response.status_code == 200:
        anime_list = response.json().get('data')
        titles = [anime['node']['title'] for anime in anime_list]
        anime_list = 'Seasonal Anime List:'
        for title in (titles):
            anime_list += f'\n{title}'
        return anime_list
    else:
        print(f'Error: {response.status_code} - {response.text}')
        return None

# Get anime rankings
def get_anime_rankings(limit=5, ranking_type='all', offset=0, api_key=API_KEY):
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    params = {
        'nsfw': 'true',
        'limit': limit,
        'ranking_type': ranking_type,
        'offset': offset,
    }
    
    response = requests.get(f'{BASE_URL}anime/ranking', headers=headers, params=params)
    
    if response.status_code == 200:
        anime_list = response.json().get('data')
        titles = [anime['node']['title'] for anime in anime_list]
        rankings = [anime['ranking']['rank'] for anime in anime_list]
        anime_list = 'Anime Rankings:'
        for title, rank in zip(titles, rankings):
            anime_list += f'\n{rank}. {title}'
        return anime_list
    else:
        print(f'Error: {response.status_code} - {response.text}')
        return None
    
# Get suggestions based on the user's anime list
def get_suggestions(limit=5, offset=0, api_key=API_KEY):
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    params = {
        'nsfw': 'true',
        'limit': limit,
        'offset': offset,
    }
    
    response = requests.get(f'{BASE_URL}anime/suggestions', headers=headers, params=params)
    
    if response.status_code == 200:
        anime_list = response.json().get('data')
        titles = [anime['node']['title'] for anime in anime_list]
        anime_list = 'Anime Suggestions:'
        for title in titles:
            anime_list += f'\n{title}'
        return anime_list
    else:
        print(f'Error: {response.status_code} - {response.text}')
        return None
    
# Get anime details
def get_anime_details(anime_title, api_key=API_KEY):
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    params = {
        'nsfw': 'true',
        'fields': 'alternative_titles,genres,mean,rank,popularity,num_episodes,start_season,studios,related_anime,synopsis',
    }
    
    # Get anime ID from title
    anime_id = get_anime_id(anime_title, api_key)
    if anime_id is None:
        print('Anime not found - Invalid title or API key.')
        return None
    
    response = requests.get(f'{BASE_URL}anime/{anime_id}', headers=headers, params=params)
    
    if response.status_code == 200:
        anime_details = response.json()
        title = anime_details['title']
        details = f"Details of {title}:"
        for key, value in anime_details.items():
            # Skip some keys
            if key == 'main_picture' or key == 'id' or key == 'title' or value is None:
                continue
            # Handle nested dictionaries
            if key == 'related_anime':
                details += f'\n{key}:'
                for related in value[:5]:
                    details += f'\n\t{related["node"]["title"]}'
            elif key == 'alternative_titles':
                details += f'\n{key}:'
                for title in value['synonyms']:
                    details += f'\n\t{title}'
            elif key == 'genres':
                details += f'\n{key}:'
                for genre in value:
                    details += f'\n\t{genre["name"]}'
            elif key == 'studios':
                details += f'\n{key}:'
                for studio in value:
                    details += f'\n\t{studio["name"]}'
            elif key == 'start_season':
                details += f'\n{key}: {value["year"]} {value["season"]}'
            elif key == 'synopsis':
                details += f'\n{key}: {value[:-26]}'
            else:
                details += f'\n{key}: {value}'
        return details
    else:
        print(f'Error: {response.status_code} - {response.text}')
        return None