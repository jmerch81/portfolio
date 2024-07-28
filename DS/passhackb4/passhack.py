import requests
import hashlib

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, please check the API and try again')
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return int(count)  # This will change count to an integer.
    return 0

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

def main():
    try:
        while True:
            password = input("I can check to see if your password has ever been exposed in a data breach. Enter a password to check (or type 'exit' to quit): ")
            if password.lower() == 'exit':
                break
            count = pwned_api_check(password)
            if count:
                print(f'{password} was found {count} times... I suggest you change your password to prevent yourself from being a victim of hacking')
            else:
                print(f'{password} was NOT found by the almighty system. Use this password and carry on!')
        print('all done!')
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    main()
