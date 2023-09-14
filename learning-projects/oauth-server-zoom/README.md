# Zoom OAuth Server

This was to see if we could feasibly make something that supports User OAuth.

## Installation

### Set up an OAuth Server
 
  1. I used NGrok to make a public-facing domain.  Run it and copy the HTTPS URL it provides.
  2. Create a Zoom OAuth App in the Zoom Marketplace, fill in the Redirect App with the NGrok info (/oauth)
  3. Modify the `main.py`'s constants with the appropriate, including Zoom's Client Id and Secret
  4. Run the FastAPI server through Uvicorn : `uvicorn main:app --host 0.0.0.0 --port 80`
  5. Test it out with "Local Test".  If everything works, you should get the access token needed for Zoom API!



## Conclusions

Yes, this seems feasible, at least initially.  We'd need a server, but that's not terrible.

A good follow up on this would be to see what is needed for when an already-registered user needs another token.  How do they initiate the request? 

