import browser_cookie3

def get_specific_cookies(domain_name, cookie_names):
    # Load cookies from the browser
    cookies = browser_cookie3.load(domain_name=domain_name)

    # Extract specific cookies and format them into a dictionary
    cookie_dict = {}
    for cookie in cookies:
        if cookie.name in cookie_names:
            cookie_dict[cookie.name] = cookie.value

    return cookie_dict

# Replace 'example.com' with the domain you want to extract cookies from
domain = 'bard.google.com/'
cookie_names = ['__Secure-1PSID', '__Secure-1PSIDTS', '__Secure-1PSIDCC']
specific_cookies = get_specific_cookies(domain, cookie_names)

# Print the specific cookies
print(specific_cookies)