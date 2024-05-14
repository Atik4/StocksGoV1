from fyers_apiv3 import fyersModel
import os

# Replace these values with your actual API credentials
client_id = "7M3R3OH9FL-100"
secret_key = "IJOJE3EO40"
redirect_uri = "https://www.google.com/"
grant_type = "authorization_code"
response_type = "code"
state = "sample_state"

auth_token_file_name = "/Users/atik.agarwal/Projects/personal/StocksGo/StocksGo/access_token.txt"

def login():
    login_token = ""
    if os.path.exists(auth_token_file_name):
        with open(auth_token_file_name, "r") as f:
            login_token = f.read()
        return login_token
    # Create a session model with the provided credentials
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type=response_type,
        grant_type=grant_type
    )

    # Generate the auth code using the session model
    response = session.generate_authcode()

    # Print the auth code received in the response
    print(response)

    auth_code = input("Enter auth code: ")
    session.set_token(auth_code)

    login_token = session.generate_token()["access_token"]
    with open(auth_token_file_name, "w") as f:
        f.write(login_token)

    return login_token

print(login())

fyers = fyersModel.FyersModel(is_async=False, client_id=client_id, token=login(), log_path="/Users/atik.agarwal/Projects/personal/trading/logs/")
# print(fyers.get_profile())