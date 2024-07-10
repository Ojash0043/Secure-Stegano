import streamlit as st
from PIL import Image
from stegano import lsb
import base64

st.title("SecureStegano")

def hide_message(image, message, passcode):
    # Encode the passcode to bytes
    passcode_bytes = passcode.encode("utf-8")

    # Combine the message and passcode
    combined_message = f"{message}\n{passcode}"

    # Hide the combined message in the image using LSB steganography
    secret_image = lsb.hide(image, combined_message)
    
    # Save the modified image with the hidden message
    output_path = "hidden_image.png"
    secret_image.save(output_path)
    
    return output_path

def extract_message(image, passcode):
    # Extract the combined message from the image
    secret_image = Image.open(image)
    combined_message = lsb.reveal(secret_image)

    # Split the combined message into message and passcode
    message, stored_passcode = combined_message.split('\n', 1)

    # Check if the provided passcode matches the stored passcode
    if passcode == stored_passcode:
        return message
    else:
        return "Passcode does not match. Cannot extract message."

def main():
    st.sidebar.header("Options")

    action = st.sidebar.radio("Choose Action", ["Hide Message", "Extract Message"])

    if action == "Hide Message":
        st.subheader("Hide Message")
        message = st.text_input("Enter the secret message:")
        passcode = st.text_input("Enter a passcode for encryption:", type="password")
        image_file = st.file_uploader("Choose an image:", type=["jpg", "jpeg", "png"])

        if message and passcode and image_file and st.button("Submit"):
            # Convert the image file to a PIL Image
            image = Image.open(image_file)

            # Hide the message using the passcode and save the modified image
            output_path = hide_message(image, message, passcode)
            st.image(output_path, caption="Hidden Image", use_column_width=True)

    elif action == "Extract Message":
        st.subheader("Extract Message")
        passcode = st.text_input("Enter the passcode for decryption:", type="password")
        image_file = st.file_uploader("Choose the image to extract message:", type=["png"])

        if passcode and image_file and st.button("Submit"):
            # Extract the message using the passcode
            extracted_message = extract_message(image_file, passcode)
            st.success(f"Extracted Message: {extracted_message}")

if __name__ == "__main__":
    main()
