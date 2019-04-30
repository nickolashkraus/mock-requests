import requests

def main():
    resp = requests.get('https://static-website.com/')
    resp.raise_for_status()
    return resp
