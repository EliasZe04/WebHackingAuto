import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin


def get_forms(url):
    """finds the whole forms from the page and returns them"""
    soup = bs(requests.get(url).content, "html.parser") # gives the HTML page
    forms = soup.find_all("form") # find the form elements in a list
    return forms


def get_form_details(form):
    """extracts all the HTML form's details such as action/method/input field into a dict and returns the dict"""
    details = {}  # would contain the form details
    action_attribute = form.attrs.get("action").lower()  # find action attribute
    form_method = form.attrs.get("method", "get").lower() # find form method (GET, POST etc.)
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})  # loads the name and the type of the inputs into the list
    details["action"] = action_attribute
    details["method"] = form_method
    details["inputs"] = inputs # loads the inputs list into the dict
    return details


def send_requests(forms_details, url, value):
    """sends requests using the forms from the website and returns the HTTP response"""
    target_url = urljoin(url, forms_details["action"])  # constructs the full URL from the action attribute
    inputs = forms_details["inputs"]  # finds the input elements
    data = {}  
    for input in inputs:
        if input["type"] == "text" or input["type"] == "search":
            input["type"] = value  # Puts the script in the text and search parameter values
        input_name = input.get("name")
        if input_name: # if input name is not none, add him to the form submission
            data[input_name] = value  # loads the parameters as a key with the script as a value in the dictionary
            
    # submits the form submission to the target url
    if forms_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)


def scan_xss(url):
    """scans the website and returns True if xss vulnerabilities are found, False otherwise"""
    forms = get_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.") # numbers of forms
    demo_virus_script = "<script>alert('hey')</script>"
    is_vulnerable = False
    for form in forms:
        form_details = get_form_details(form)
        content = send_requests(form_details, url, demo_virus_script).content.decode() # the HTML response after sending the xss request
        if demo_virus_script in content:
            print(f"[+] XSS detected on {url}")
            print(f"[*] Form details:")
            pprint(form_details)
            is_vulnerable = True

    return f"\nREFLECTED XSS VULNERABILITY STATUS; {is_vulnerable}"


if __name__ == "__main__":
    try:
        print("\t-- REFLECTED XSS ATTACK --\n")
        url = input("Enter url address: ")
        print(scan_xss(url))
    except:
        print("SYSTEM MESSAGE:\n\t[X] Automatic test failed...")
