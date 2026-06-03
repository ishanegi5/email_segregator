import streamlit as st

from classifier import classify_email
from extractors import (
    extract_tonnage,
    extract_vc,
    extract_tc
)

st.title("Shipping Email Segregation System")

email_text = st.text_area(
    "Paste Shipping Email Here"
)

if st.button("Process Email"):

    category = classify_email(email_text)

    if category == "TONNAGE":

        data = extract_tonnage(email_text)

    elif category == "CARGO_VC":

        data = extract_vc(email_text)

    else:

        data = extract_tc(email_text)

    st.subheader("Detected Category")
    st.write(category)

    st.subheader("Extracted Information")
    st.json(data)