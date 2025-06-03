# handle uploading / downloading images for map marker information
import cloudinary
import cloudinary.uploader
from PIL import Image

import requests
from io import BytesIO

# setup
cloudinary.config(
    cloud_name = 'dqi4aknwh',
    api_key = '538149618275621',
    api_secret = 'HrAthKWVq_OrAjJ5NZ4Cj81qy1w',
    secure = True
)

# Upload
def upload_image(filename: str):
    # generate an ID based on file name
    fileID = filename.replace('/','_').replace('\\','_').replace('.','_')

    # do the upload
    upload_result = cloudinary.uploader.upload(filename, public_id = fileID)

    # return the URL to go in the database
    return upload_result['secure_url']


# Download an image as a PIL.Image object
def download_image(url: str):
    # get url content
    res = requests.get(url)

    img = Image.open(BytesIO(res.content)) # done this way to avoid saving the file locally

    # show the image (for testing)
    #img.show()

    return img