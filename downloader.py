#used in pythonanywhere.com to download the model file from google drive (overcome the 100MB limit)
import gdown, sys

url = 'https://drive.google.com/file/d/1SUgryGaKm0QDnVb9Kltahy6lWgv-77ln/view?usp=sharing'

file_id = url.split('/')[-2]

prefix = 'https://drive.google.com/uc?/export=download&id='

gdown.download(prefix+file_id)