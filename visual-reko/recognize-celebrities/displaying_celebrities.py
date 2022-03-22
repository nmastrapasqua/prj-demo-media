import io
import requests
import json
import os
from PIL import Image, ImageDraw, ImageFont

api_url = f'{os.environ["API_URL"]}/celebrities'
rapidapi_host = os.environ["RAPIDAPI_HOST"]
rapidapi_key = os.environ["RAPIDAPI_KEY"]


def show_faces():

    image_url = 'https://github.com/nmastrapasqua/prj-demo-media/blob/main/visual-reko/recognize-celebrities/test_ok.jpeg?raw=true'

    # Download the image
    response = requests.get(image_url)
    response.raise_for_status()
    stream = io.BytesIO(response.content)
    image = Image.open(stream)

    # Call Visual Recognition API
    headers = {
        'content-type': "application/json",
        'x-rapidapi-host': rapidapi_host,
        'x-rapidapi-key': rapidapi_key,
    }
    body = {
        "ImageUrl": image_url
    }
    response = requests.post(
        url=api_url, headers=headers, data=json.dumps(body))
    response.raise_for_status()
    response = response.json()

    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)

    # calculate and display bounding boxes for each detected face
    print('Detected faces for ' + image_url)
    for celebrity in response['CelebrityFaces']:
        name = celebrity['Name']
        faceDetail = celebrity['Face']
        box = faceDetail['BoundingBox']
        left = imgWidth * box['Left']
        top = imgHeight * box['Top']
        width = imgWidth * box['Width']
        height = imgHeight * box['Height']

        points = (
            (left, top),
            (left + width, top),
            (left + width, top + height),
            (left, top + height),
            (left, top)

        )
        draw.line(points, fill='#00d400', width=2)
        font = ImageFont.truetype("arial.ttf", 20)
        draw.text((left, top), name, font=font, fill='#00d400')

        for landmark in faceDetail['Landmarks']:
            px = imgWidth * landmark['X']
            py = imgHeight * landmark['Y']
            draw.ellipse((px-3, py-3, px+3, py+3),
                         fill="#00d400", outline="red")

    image.show()

    return response['CelebrityFaces']


def main():
    celebrity_faces = show_faces()
    for celebrity in celebrity_faces:
        print(f'Name: {celebrity["Name"]}')
        print(f'MatchConfidence: {celebrity["MatchConfidence"]}')
        print(f'Urls: {celebrity["Urls"]}')
        for emotion in celebrity['Face']['Emotions']:
            if emotion['Confidence'] >= 70:
                print(f'Emotion: {emotion["Type"]}')


if __name__ == "__main__":
    main()
