import streamlit as st
import streamfy as sy
import base64

def image_carousel(images, urls):
    # Convert local image paths to displayable format
    image_urls = [f"data:image/jpg;base64,{base64.b64encode(open(image, 'rb').read()).decode()}" for image in images]
    final_urls = image_urls + urls
    # Use the Streamfy component for the image carousel
    image_carousel = sy.carousel(
        items = final_urls
    )
    return image_carousel 


@st.dialog("Book details")
def view_more_details(name, author, filename):
    st.title(f"**{name}** - {author}")
    cols = st.columns(2)
    cols[0].image(f"assets/{filename}1.png", use_column_width = True)
    cols[1].image(f"assets/{filename}2.png", use_column_width = True)