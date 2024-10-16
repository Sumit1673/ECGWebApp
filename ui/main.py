import streamlit as st
import requests

# st.set_option('deprecation.showfileUploaderEncoding', False)

st.title("ECG WebApp")

with st.form("my_form"):
    username = st.text_input("User Name")
    email = st.text_input("Email")
    image = st.file_uploader("Choose and image")
    submit_button = st.form_submit_button('Submit')  

    if submit_button:
        if image and username and email:
            try:
                file = {"file": image.getvalue()}
                res = requests.post("http://backend:8080/predict",
                                    files=file, timeout=50)
                res.raise_for_status()  # Raises an HTTPError for bad responses
                st.success(f"Predictions: {res.json()}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred while making the request: {str(e)}")
            except ValueError as e:
                st.error(f"Error processing the response: {str(e)}")
        else:
            st.warning("Please fill in all fields and upload an image.")