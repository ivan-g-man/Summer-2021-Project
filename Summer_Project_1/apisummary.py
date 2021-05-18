import requests

params = {'SM_API_KEY': '947A045DFD', 
'SM_URL': 'https://www.nytimes.com/2021/03/24/us/atlanta-shooting-spa-owners.html'}
response = requests.get('https://api.smmry.com',
            params=params)
print(response.json())