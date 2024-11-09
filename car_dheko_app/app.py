import streamlit as st
import joblib
import base64
import numpy as np
from datetime import datetime

current_year = datetime.now().year

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

left_image = "logo/download.jpeg"
right_image = "logo/download.jpeg"

left_img_base64 = image_to_base64(left_image)
right_img_base64 = image_to_base64(right_image)

header_html = f"""
<div style="display: flex; align-items: center; justify-content: space-between; background-color: white; padding: 1px; border-radius: 5px;">
    <img src="data:image/jpeg;base64,{left_img_base64}" alt="Left Image" style="height: 100px;">
    <h1 style="font-size: 46px; font-weight: bold; color:#0000FF; margin: 0;">car_dheko car price Prediction</h1>
    <img src="data:image/jpeg;base64,{right_img_base64}" alt="Right Image" style="height: 100px;">
</div>
"""

model = joblib.load('model/model.pkl') 
label_encoders = joblib.load('model/label_encoders.pkl')


with open('model/my_list.txt', 'r') as f:
    feature = [line.strip() for line in f]
with open('model/transmission.txt', 'r') as f:
    trans = [line.strip() for line in f]
with open('model/Gear_Box.txt', 'r') as f:
    gear = [line.strip() for line in f]
with open('model/city.txt', 'r') as f:
    city = [line.strip() for line in f]
with open('model/insurance.txt', 'r') as f:
    insurance = [line.strip() for line in f]
with open('model/bodytype.txt', 'r') as f:
    bt = [line.strip() for line in f]
with open('model/fuel.txt', 'r') as f:
    ft = [line.strip() for line in f]

st.markdown(header_html, unsafe_allow_html=True)

inputs = []

info1 = st.selectbox(feature[0], trans)
encoder = label_encoders['transmission']
value1 = encoder.transform([info1])[0]

value2 = st.number_input(feature[1], min_value=2007, step=1,max_value=current_year)

info3 = st.selectbox(feature[2], gear)
encoder = label_encoders['misc_Gear Box']
value3 = encoder.transform([info3])[0]

info4 = st.selectbox(feature[3], city)
encoder = label_encoders['city']
value4 = encoder.transform([info4])[0]

info5 = st.selectbox(feature[4], insurance)
encoder = label_encoders['insurance_validity']
value5 = encoder.transform([info5])[0]

value6 = st.number_input(feature[5], min_value=0, step=1,max_value=6)

value7 = st.number_input(feature[6], min_value=0, step=1,max_value=2000000)

info8 = st.selectbox(feature[7],bt)
encoder = label_encoders['bt']
value8 = encoder.transform([info8])[0]

value9 = st.number_input(feature[8], min_value=7.0, step=0.01,max_value=40.0)

info10 = st.selectbox(feature[9], ft)
encoder = label_encoders['fuel_type']
value10 = encoder.transform([info10])[0]


inputs.extend([value1, value2, value3,value4, value5, value6, value7, value8, value9, value10])


if st.button("Predict"):
    input_array = np.array(inputs).reshape(1, -1)
    
    prediction = model.predict(input_array)

    st.write("Predicted Output:", prediction[0])
