import sys

# 2. Print the URL needed to authorise your application.
def print_new_authorisation_url(code_challenge: str, client_id: str):
    url = f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={client_id}&code_challenge={code_challenge}'
    return url

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python link_generator.py <client_id>')
        sys.exit(1)
    client_id = sys.argv[1]
    code_verifier = sys.argv[2]
    output = print_new_authorisation_url(code_verifier, client_id)
    print(output)