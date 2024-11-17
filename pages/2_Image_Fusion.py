import google.generativeai as genai
import streamlit as st

def gen_image(path,query):

    # Upload the file and print a confirmation.
    sample_file = genai.upload_file(path=path)

    # Choose a Gemini API model.
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

    # Prompt the model with text and the previously uploaded image.
    response = model.generate_content([sample_file, query])
    print("Response: "+response.text)
    return response.text


st.title("Fusion Chat 🤖")
st.page_link("pages/1_Text_Fusion.py", label="Text Fusion", icon="1️⃣")
st.page_link("pages/2_Image_Fusion.py", label="Image Fusion", icon="2️⃣")
st.subheader("Image Fusion")


with st.sidebar:
    st.title("Menu:")
    global img_file_name
    img_file = st.file_uploader("Upload your Image File", accept_multiple_files=False)
    
    if img_file is not None:
        img_file_name = img_file.name
        st.write(f"Uploaded file name: {img_file_name}")

        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                # Add your image processing code here
                st.success("Processing complete. You can now ask questions!")
                st.image(img_file_name)
    else:
        st.write("No file uploaded.")

    

# user_question = st.chat_input("Ask a Question Related to Image File")
if img_file:
    st.image(img_file_name)
    user_question = st.chat_input("Ask a Question Related to "+img_file_name+" Image File")
    if user_question:
        # show_img(img_file_name)
        st.write("**👤:** " + user_question)
        A = gen_image(img_file_name,user_question)
        st.write("**🤖:** "+A)