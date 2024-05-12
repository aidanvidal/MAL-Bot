import secrets
import sys

# 1. Generate a new Code Verifier / Code Challenge.
def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]

if __name__ == '__main__':
    if len(sys.argv) != 1:
        print('Usage: python code_verifier.py')
        sys.exit(1)
    code_verifier = get_new_code_verifier()
    print(code_verifier)