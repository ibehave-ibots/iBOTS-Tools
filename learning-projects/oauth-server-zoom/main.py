from fastapi import FastAPI, Request
import httpx
import json
from base64 import b64encode


# Replace these with your Zoom OAuth app's client ID and secret
CLIENT_ID = "R7eKNreHQMGPWp5kCjdmng"
CLIENT_SECRET = "E9jnb4OldYeWmkb8gXI6PYs01hxnzrkk"
REDIRECT_URI = "https://094a-131-220-35-163.ngrok-free.app/oauth"  # Replace with your redirect URI

app = FastAPI()

@app.get("/oauth")
async def read_callback(code: str):
    print('Code: ', code)
    # Prepare data for POST request to Zoom OAuth endpoint
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    secret = b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {secret}"
    }
    print('headers: ', headers)

    # Make POST request to Zoom OAuth endpoint to get access token
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://zoom.us/oauth/token",
            data=data,
            headers=headers
        )
    
    # Parse the JSON response
    token_data = response.json()
    print("token_data: ", token_data)

    # Extract the access token (you should save this token for future use)
    access_token = token_data.get("access_token", "No access token received")

    return {"access_token": access_token}
