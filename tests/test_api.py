import requests

def test_media_endpoint():
    # Test basic GET request
    response = requests.get('http://127.0.0.1:5000/api/media')
    print("Status Code:", response.status_code)
    print("Response:", response.json())
    
    # Test with media type filter
    response = requests.get('http://127.0.0.1:5000/api/media?media_type=video')
    print("\nFiltered by video:")
    print("Status Code:", response.status_code)
    print("Response:", response.json())

if __name__ == "__main__":
    test_media_endpoint() 