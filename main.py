import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_watsonx_ai


page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background: rgb(255,243,217);
background: linear-gradient(90deg, rgba(255,243,217,0.4) 0%, rgba(249,255,213,0.3) 80%);
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Streamlit UI
st.title("ReviewMinds AI")
url = st.text_input("Enter Product URL")


if "dom_content" not in st.session_state:
    st.session_state.dom_content = ""
if "parsed_result" not in st.session_state:
    st.session_state.parsed_result = ""
if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""
if "response_received" not in st.session_state:
    st.session_state.response_received = False
if "second_url" not in st.session_state:
    st.session_state.second_url = ""
if "second_dom_content" not in st.session_state:
    st.session_state.second_dom_content = ""
if "second_parsed_result" not in st.session_state:
    st.session_state.second_parsed_result = ""
if "second_chat_input" not in st.session_state:
    st.session_state.second_chat_input = ""
if "add_second_site" not in st.session_state:
    st.session_state.add_second_site = False

# Website Data Extraction
if st.button("Analyze Reviews"):
    if url:
        with st.spinner("Fetching Reviews..."):
            dom_content = scrape_website(url)
            body_content = extract_body_content(dom_content)
            cleaned_content = clean_body_content(body_content)

            # Store the first DOM content in session state
            st.session_state.dom_content = cleaned_content

        if st.session_state.dom_content and not st.session_state.parsed_result:
            with st.spinner("Analyzing and generating response..."):
                dom_chunks = split_dom_content(st.session_state.dom_content)
                parse_description = "Extract the specific information as per the e-commerce review template."
                # Parse the data with WatsonX AI
                st.session_state.parsed_result = parse_with_watsonx_ai(dom_chunks, parse_description, is_first_scrape=True)
                st.session_state.response_received = True


if st.session_state.parsed_result:
    st.write(st.session_state.parsed_result)


if st.session_state.response_received and st.session_state.parsed_result and not st.session_state.add_second_site:
    with st.form(key='chat_form'):
        chat_input = st.text_area("How can I assist you further?", value=st.session_state.chat_input)
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            st.session_state.chat_input = chat_input
            
            with st.spinner("Generating chat response..."):
                response = parse_with_watsonx_ai([st.session_state.dom_content], st.session_state.chat_input, is_first_scrape=False)
                st.write("Chat Response:")
                st.write(response)

# Add option to analyze a second website
if st.session_state.response_received:
    if st.button("Add Another Product"):
        st.session_state.add_second_site = True



if st.session_state.add_second_site:
    st.session_state.second_url = st.text_input("Enter Second Product URL")
    
    if st.button("Submit", key="second_analyze_button"):
        if st.session_state.second_url:
            with st.spinner("Fetching Reviews..."):
                second_dom_content = scrape_website(st.session_state.second_url)
                second_body_content = extract_body_content(second_dom_content)
                second_cleaned_content = clean_body_content(second_body_content)
                st.session_state.second_dom_content = second_cleaned_content

            if st.session_state.second_dom_content and not st.session_state.second_parsed_result:
                with st.spinner("Analyzing and generating response..."):
                    second_dom_chunks = split_dom_content(st.session_state.second_dom_content)
                    second_parse_description = "Extract the specific information as per the e-commerce review template."
                    # Parse the data with WatsonX AI
                    st.session_state.second_parsed_result = parse_with_watsonx_ai(second_dom_chunks, second_parse_description, is_first_scrape=True)


if st.session_state.second_parsed_result:
    st.write("Analysis:")
    st.write(st.session_state.second_parsed_result)

# Chat with both parsed data sets using WatsonX AI
if st.session_state.response_received and st.session_state.second_parsed_result:
    with st.form(key='comparison_chat_form'):
        combined_chat_input = st.text_area("Ask any question in relation to both products:", value=st.session_state.second_chat_input)
        submit_comparison_button = st.form_submit_button("Submit")
        
        if submit_comparison_button:
            st.session_state.second_chat_input = combined_chat_input
            
            combined_content = {
                "Website 1 Data": st.session_state.parsed_result,
                "Website 2 Data": st.session_state.second_parsed_result,
            }
            comparison_prompt = f"""
            Compare the reviews and data from two different e-commerce websites:
            
            - Website 1 Data: {st.session_state.parsed_result}
            - Website 2 Data: {st.session_state.second_parsed_result}
            
            {st.session_state.second_chat_input}
            """
            with st.spinner("Generating chat response..."):
                response = parse_with_watsonx_ai([combined_content], comparison_prompt, is_first_scrape=False)
                st.write("Chat Response:")
                st.write(response)

