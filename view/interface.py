import streamlit as st
from pydantic import StrictStr, EmailStr


class WebApp:
    """
    WebApp class is used to accomodate any changes into UI functionality.
    Current Functionality
    * Takes Users name and email
    * Display the images

    """
    def __init__(self, config, ENV: StrictStr):
        
        st.title(config.get(ENV, "APP_TITLE"))

        self.user_name = st.text_input("Enter your name")
        self.user_email = st.text_input("Enter your email")
        cols = st.columns(3)

        # Image upload
        self.uploaded_files = st.file_uploader("Upload ECG images",
                                               type=config.get(ENV, "IMG_FORMAT"),
                                               accept_multiple_files=True)

    def display_image(self, image_file, prediction_result: StrictStr):
        """Displays the image and its prediction score

        Args:
            image_file (_type_): _description_
            prediction_result (StricStr): _description_
        """
        st.image(image_file, caption=image_file.name)
        st.image(image_file, caption=f"Uploaded Image", use_column_width=True)
        st.write(f"Prediction: {prediction_result}")


