import streamlit as st
import requests

# Function to call AWS API Gateway
def generate_aws_creds(userid, apiid):
    url = f"https://{apiid}.execute-api.us-west-2.amazonaws.com/v1/token"  # Replace with your API Gateway URL
    headers = {
        "Authorization": "Bearer JWT_TOKEN"  # Replace JWT_TOKEN with your actual token
    }
    body = {
        "userid": userid
    }
    
    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

# Streamlit UI
st.title("AWS Credentials Generator")

userid = st.text_input("Enter User ID")
apiid = st.text_input("aws_apiid")

if st.button("Generate AWS creds"):
    if userid:
        result = generate_aws_creds(userid, apiid)
        st.json(result)
    else:
        st.error("User ID cannot be empty")

