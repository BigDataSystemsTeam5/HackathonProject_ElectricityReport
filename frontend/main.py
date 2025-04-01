import streamlit as st
import requests


# Set FastAPI URL
base_url = "http://127.0.0.1:8000"


st.title("Mini Manus")

st.subheader("An AI Research Assistant")

st.divider()

years_quarters_list = ['2020', '2023', '2024', '2025']

years_quarters = st.multiselect("Select the years", years_quarters_list)

agents_list = ['RAG Agent', 'Web Search Agent']
agents_names = st.multiselect("Select the agents", agents_list)

question = st.text_input("Enter a query to get report")

if st.button("Get the Reasearch Report") and question:

    try:
        params = {"question": question, "agents_names": agents_names, "years_quarters": years_quarters}
        response = requests.get(f"{base_url}/ask_question", params=params)

        if response.status_code == 200:
            #st.write(response.json())
            st.write("Research Report ready to download")

            st.download_button(label="Download Report", 
                               data=response.content, 
                               file_name="mini_manus_report.pdf", 
                               mime="application/pdf")
        else:
            st.error("Failed to generate Report")

    except Exception as e:
        st.error(f"Connection error: {str(e)}")
