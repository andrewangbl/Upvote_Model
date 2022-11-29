import streamlit as st
import datetime
import pandas as pd
import requests
from PIL import Image
import base64
from io import BytesIO
import time


CSS = """
h1 {
    color: red;
}
.stApp {
    background-image: url(https://bestlifeonline.com/wp-content/uploads/sites/3/2019/12/shutterstock_556211362.jpg?quality=82&strip=all);
    background-size: cover;
}
"""
if st.checkbox('Inject CSS'):
    st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)



st.markdown("""
    # Reddit Upvote Model 🐶

""")




### Title
st.markdown("""

    ##### Title
""")
title = st.text_input('Post title', '')


st.markdown("""

    ##### DateTime
""")
### Datetime
d = st.date_input(
    "Date",
    datetime.date(2022, 11, 10),
    )
t = st.time_input(
    "Time",
    datetime.time(8, 00)
)
st.write('DateTime:', d, t)

### Images
st.markdown("""

    ##### Image
""")

time_string = str(d)+ " " +str(t)

time_stamp = int(time.mktime(time.strptime(time_string, '%Y-%m-%d %H:%M:%S'))) - time.timezone
st.write(time_stamp)
def load_image(image_file):
	img = Image.open(image_file)
	return img

def find_square(tuple_):
    width, height = tuple_
    if width>height:
        lower = height
        upper = 0
        delta = int((width-height)/2)
        left = delta
        right = width-delta
    elif width<height:
        left = 0
        right = width
        delta = int((height-width)/2)
        upper = delta
        lower = height-delta
    else:
        left = 0
        right = width
        upper = 0
        lower = height
    return (left, upper, right, lower)

st.set_option('deprecation.showfileUploaderEncoding', False)
uploaded_file = st.file_uploader("Choose a PNG or JPEG file", type = ['png','jpg','jpeg'], accept_multiple_files =False)
show_file = st.empty
if not uploaded_file:
    st.write('Please upload a file:'.format(''.join(['png','jpg','jpeg'])))
else:

    image = Image.open(uploaded_file)
    w, h  = image.size
    im_size = w*h
    box = find_square(image.size)
    crop_image = image.crop(box)
    img = crop_image.resize((128, 128))
    im_file = BytesIO()
    img.save(im_file, format="PNG")
    im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
    im_b64 = base64.b64encode(im_bytes)

    payload ={"title": title,
              "time_stamp": time_stamp,
              "image_size": im_size,
              "filedata": im_b64}


def show(image, title, d, t, r):
    st.markdown("""
    ## Results""")
    st.markdown(f"{title}")
    st.write('Post time:', d, t)
    st.image(image, caption='Your dog post')
    cat = r["category"]
    if cat==5:
        st.success('Congrats you will likely get more than 500 upvotes!!!')
    elif cat == 4:
        st.info('You will get between 100 and 500 upvotes')
    elif cat == 3:
        st.warning('You will get between 30 and 100 upvotes')
    else:
        st.error('Damn this post is kinda bad, you will get less than 30 upvotes')
    st.write(r["probabilities"])




if st.button('predict score'):
    st.write('Calculating...')
    r= requests.post(f"http://127.0.0.1:8000/getPrediction", data = payload).json()
    show(image, title, d, t, r)
else:
    st.write('Click the button once all the data has been inputed')





##
#### use image :image, title: title, time: t, date:  <--- from frotnend(this file)
# prediction<---- from backedn (api,json file) to show user


# with st.form(key='params_for_api'):

#     post_date = st.date_input('Date', value=datetime.datetime(2012, 10, 6, 12, 10, 20))
#     post_time = st.time_input('Time', value=datetime.datetime(2012, 10, 6, 12, 10, 20))
#     pickup_datetime = f'{post_date} {post_time}'
#     title = st.text_input('Post title')
#     # images ...
#     passenger_count = st.number_input('passenger_count', min_value=1, max_value=8, step=1, value=1)

#     st.form_submit_button('Make prediction')
