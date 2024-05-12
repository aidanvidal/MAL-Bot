import requests
import sys

# 3. Once you've authorised your application, you will be redirected to the webpage you've
#    specified in the API panel. The URL will contain a parameter named "code" (the Authorisation
#    Code). You need to feed that code to the application.
def generate_new_token(authorisation_code: str, code_verifier: str, client_id: str, client_secret: str) -> dict:
    url = 'https://myanimelist.net/v1/oauth2/token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': authorisation_code,
        'code_verifier': code_verifier,
        'grant_type': 'authorization_code'
    }

    response = requests.post(url, data)
    #response.raise_for_status()  # Check whether the request contains errors

    token = response.json()
    response.close()
    
    return token


# 4. Test the API by requesting your profile information
def print_user_info(access_token: str):
    url = 'https://api.myanimelist.net/v2/users/@me'
    response = requests.get(url, headers={
        'Authorization': f'Bearer {access_token}'
    })

    response.raise_for_status()
    user = response.json()
    response.close()


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Usage: python token_generator.py <authorisation_code> <code_verifier> <client_id> <client_secret>')
        sys.exit(1)

    authorisation_code = sys.argv[1]
    code_verifier = sys.argv[2]
    client_id = sys.argv[3]
    client_secret = sys.argv[4]

    token = generate_new_token(authorisation_code, code_verifier, client_id, client_secret)
    print(token)