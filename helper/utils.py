import requests

def checkdata():
    pass

def gettoken():
    try:
        # Define the payload
        payload = {
            "email": "thedeveloperspace17@gmail.com",
            "password": "nopass"
        }

        # Send the POST request
        response = requests.post("https://api-dev.momenttrack.com/auth/default/system/login", data=payload)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("data"):
                return data["data"].get("access_token")
                return {
                    "access_token": data["data"].get("access_token"),
                    "org_slug": data["data"].get("org_slug"),
                    "refresh_token": data["data"].get("refresh_token"),
                }
            else:
                print(f"Error: {data.get('message', 'Unknown error occurred')}")
        else:
            print(f"HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"Exception occurred: {e}")
    return None



def perform_move( data):
    token=gettoken()
    headers = {
            "Authorization": f"Bearer {token}"
        }
    print(data)
    resp=requests.post("https://api-dev.momenttrack.com/api/lexcorp/license_plates/move_many",headers=headers, json=data )
    print(resp.text)