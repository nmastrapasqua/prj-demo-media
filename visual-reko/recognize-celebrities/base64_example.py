import requests
import base64
import os
import json

api_url = f'{os.environ["API_URL"]}/celebrities'
rapidapi_host = os.environ["RAPIDAPI_HOST"]
rapidapi_key = os.environ["RAPIDAPI_KEY"]


def send_base64_image():
    with open('RapidAPI/tutorial/data/image.jpg', 'rb') as binary_file:
        binary_file_data = binary_file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        base64_message = base64_encoded_data.decode('utf-8')

    # Call Visual Recognition API
    headers = {
        'content-type': "application/json",
        'x-rapidapi-host': rapidapi_host,
        'x-rapidapi-key': rapidapi_key,
    }
    body = {
        "ImageUrl": f'data:image/jpg;base64,{base64_message}'
    }
    response = requests.post(
        url=api_url, headers=headers, data=json.dumps(body))
    response.raise_for_status()

    return response.json()


def main():
    response = send_base64_image()
    for celebrity in response['CelebrityFaces']:
        print(f'Name: {celebrity["Name"]}')
        print(f'MatchConfidence: {celebrity["MatchConfidence"]}')
        for emotion in celebrity["Face"]["Emotions"]:
            if emotion['Confidence'] >= 70:
                print(f"Emotion: {emotion['Type']}")


if __name__ == "__main__":
    main()
