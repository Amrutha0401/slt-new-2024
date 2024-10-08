import cv2
import streamlit as st
import numpy as np
from ultralytics import YOLO

def app():
    st.set_page_config(page_title="Sign Language Translator", page_icon=":camera:", layout="wide")

    st.markdown("""
    <style>
    body {
        background-color: #33FFD1;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: #00698f;'>Sign Language Detection</h1>", unsafe_allow_html=True)
   
    model = YOLO('best.pt')
    object_names = list(model.names.values())

    col1, col2 = st.columns(2)

    with col1:
        st.write("Upload Image")
        uploaded_file = st.file_uploader("Select an image", type=['jpg', 'jpeg', 'png'])


    submitted = st.button("Submit")

    if submitted:
        if uploaded_file is not None:
            file_bytes = uploaded_file.getvalue()
            image = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)

            with st.spinner('Processing image...'):
                result = model(image)
                for detection in result[0].boxes.data:
                    x0, y0 = (int(detection[0]), int(detection[1]))
                    x1, y1 = (int(detection[2]), int(detection[3]))
                    score = round(float(detection[4]), 2)
                    cls = int(detection[5])
                    object_name = model.names[cls]
                    label = f'{object_name} {score}'
                    cv2.rectangle(image, (x0, y0), (x1, y1), (255, 0, 0), 2)
                    cv2.putText(image, label, (x0, y0 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 3)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                st.image(image, caption='Detected objects', width=400)  

if __name__ == "__main__":
    app()
