import io
import requests
import json
import os
from PIL import Image, ImageDraw

api_url = f'{os.environ["API_URL"]}/equipment'
rapidapi_host = os.environ["RAPIDAPI_HOST"]
rapidapi_key = os.environ["RAPIDAPI_KEY"]


def show_faces():

    image_url = 'https://github.com/nmastrapasqua/prj-demo-media/blob/main/visual-reko/ppe/test_ok.jpg?raw=true'

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
        "ImageUrl": image_url,
        "RequiredEquipment": ["HEAD_COVER"]
    }
    response = requests.post(
        url=api_url, headers=headers, data=json.dumps(body))
    response.raise_for_status()
    response = response.json()

    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)

    # calculate and display bounding boxes for each detected PPE
    print('Detected PPEs for ' + image_url)
    # Summary is available only if 'RequiredEquipment' is provided
    # in the input request
    person_ok = response['Summary']['PersonsWithRequiredEquipment']
    person_ko = response['Summary']['PersonsWithoutRequiredEquipment']
    for person in response['Persons']:
        id = person['Id']
        box = person['BoundingBox']
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
        color = '#00d400' if id in person_ok else '#ff0000'
        draw.line(points, fill=color, width=2)

        # Draw PPE
        body_parts = person['BodyParts']
        for part in body_parts:
            for ppe in part['EquipmentDetections']:
                if not ppe['CoversBodyPart']['Value']:
                    continue
                box = ppe['BoundingBox']
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
                draw.line(points, fill=color, width=2)

    image.show()

    return len(response['Persons'])


def main():
    faces_count = show_faces()
    print("Persons detected: " + str(faces_count))


if __name__ == "__main__":
    main()
