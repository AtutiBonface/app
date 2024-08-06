import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
}

#'Accept-Encoding': 'identity;q=1, *;q=0',    
63311740 # test 1
63278972 # browser
63311740 # test2


response = requests.get(r'https://images-assets.nasa.gov/video/Breaking%20Barriers%20Dorothy%20J.%20Vaughan%20(Narrated%20by%20Octavia%20Spencer)/Breaking%20Barriers%20Dorothy%20J.%20Vaughan%20(Narrated%20by%20Octavia%20Spencer)~large.mp4', headers=headers, stream=True)
print(response.headers)

'86364539'
86364539

