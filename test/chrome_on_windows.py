import os
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Selenium Grid - Test Chrome on Windows
g_driver = webdriver.Remote(
   command_executor = "http://192.168.1.167:4444/wd/hub",
   desired_capabilities = {
        "browserName": "chrome",
        "platform": "Windows"
    }
)

# Global variable initialization
g_total_tests = 14
g_tests_ran = 0
g_passed_tests = 0
g_failed_tests = 0
g_summary_details = []

"""# Global profile/driver setup for Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
g_driver = webdriver.Chrome(options=chrome_options)
"""

"""# Global profile/driver setup for Firefox
g_profile = webdriver.FirefoxProfile()
g_profile.accept_untrusted_certs = True
g_driver = webdriver.Firefox(firefox_profile=g_profile)
"""

# Dummy admin account for testing
g_admin_username = os.getenv('TEST_ADMIN_USERNAME')
g_admin_password = os.getenv('TEST_ADMIN_PASSWORD')

def new_random_string(length=10):
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join((random.choice(alphabet) for i in range(length)))

def main():
    global g_summary_details, g_driver
    # Test #1: Confirm we are on the log_in page before continuing
    g_driver.get('https://u1910-dev:5000/')
    test_comparison(g_driver.title, "Log In", "Reached /log_in route")
    # Test #2: Go to sign_up page
    g_driver.find_element_by_id("sign_up_link").click()
    test_comparison(g_driver.title, "Sign Up", "Reached /sign_up route")
    # Generate new random test user info
    print("\nGenerating Random User Info...")
    username = new_random_string()
    email = username + "@selenium.test"
    password = new_random_string()
    print("Email:\t\t" + email + "\nUsername:\t" + username + "\nPassword:\t" + password)
    # Test #3: Create new test user account
    g_driver.find_element_by_id("email_input").send_keys(email)
    g_driver.find_element_by_id("username_input").send_keys(username)
    g_driver.find_element_by_id("password_input").send_keys(password)
    g_driver.find_element_by_id("confirm_password_input").send_keys(password)
    g_driver.find_element_by_id("agree_to_terms_input").click()
    g_driver.find_element_by_id("submit_button").click()
    test_comparison(g_driver.title, "Dashboard", "Created new user " + username + " and was auto logged in")
    # Test #4: Log out
    g_driver.find_element_by_id("log_out_link").click()
    test_comparison(g_driver.title, "Log In", "Logged out and was auto returned to the log_in page")
    # Test #5: Log in as test user
    g_driver.find_element_by_id("username_input").send_keys(username)
    g_driver.find_element_by_id("password_input").send_keys(password)
    g_driver.find_element_by_id("submit_button").click()
    test_comparison(g_driver.title, "Dashboard", "Logged in to existing user " + username)
    # Test #6: Go to profile page
    g_driver.find_element_by_id("profile_link").click()
    test_comparison(g_driver.title, "Profile", "Reached /profile route")
    # Test #7: Go to change_password page
    g_driver.find_element_by_id("change_password_link").click()
    test_comparison(g_driver.title, "Change Password", "Reached /change_password route")
    # Test #8: Change password
    g_driver.find_element_by_id("old_password_input").send_keys(password)
    old_password = password
    password = new_random_string()
    g_driver.find_element_by_id("new_password_input").send_keys(password)
    g_driver.find_element_by_id("confirm_new_password_input").send_keys(password)
    g_driver.find_element_by_id("submit_button").click()
    test_comparison(g_driver.title, "Profile", "Changed password and auto returned to profile")
    # Test #9: Log out and attempt to log back in with old password
    g_driver.find_element_by_id("log_out_link").click()
    g_driver.find_element_by_id("username_input").send_keys(username)
    g_driver.find_element_by_id("password_input").send_keys(old_password)
    g_driver.find_element_by_id("submit_button").click()
    test_comparison(g_driver.title, "Log In", "Not allowed to log back in with old password")
    # Test #10: Log in with new password
    g_driver.find_element_by_id("username_input").send_keys(username)
    g_driver.find_element_by_id("password_input").send_keys(password)
    g_driver.find_element_by_id("submit_button").click()
    test_comparison(g_driver.title, "Dashboard", "Logged in with new password")
    # Test #11-12: Submit network request
    g_driver.find_element_by_id("network_request_input").click()
    g_driver.find_element_by_id("submit_button").click()
    g_driver.find_element_by_id("log_out_link").click()
    g_driver.find_element_by_id("username_input").send_keys(g_admin_username)
    g_driver.find_element_by_id("password_input").send_keys(g_admin_password)
    g_driver.find_element_by_id("submit_button").click()
    request_usernames = g_driver.find_elements_by_name("request_username")
    request_approval_boxes = g_driver.find_elements_by_css_selector("input[type='checkbox']")
    i = 0
    for e in request_usernames:
        if e.text == username:
            test_comparison(request_approval_boxes[i].is_selected(), False, "Submitted test network request")
            request_approval_boxes[i].click()
            break
        else:
            i += 1
    g_driver.find_element_by_id("submit_button").click()
    request_usernames = g_driver.find_elements_by_name("request_username")
    request_approval_boxes = g_driver.find_elements_by_name("approved")
    test_comparison(request_approval_boxes[i].is_selected(), True, "Logged in as test_admin and approved test network request")
    g_driver.find_element_by_id("log_out_link").click()
    # Test #13: Reset password
    g_driver.find_element_by_id("reset_password_link").click()
    g_driver.find_element_by_id("email_input").send_keys(email)
    g_driver.find_element_by_id("submit_button").click()
    old_password = password
    password = g_driver.find_element_by_id("new_password").text
    g_driver.find_element_by_id("log_in_link").click()
    g_driver.find_element_by_id("username_input").send_keys(username)
    g_driver.find_element_by_id("password_input").send_keys(password)
    g_driver.find_element_by_id("submit_button").click()
    test_comparison(g_driver.title, "Dashboard", "Reset password of " + username + " and logged in")
    # Test #14: Delete account and clean up
    g_driver.find_element_by_id("profile_link").click()
    g_driver.find_element_by_id("delete_account_link").click()
    test_comparison(g_driver.title, "Log In", "Deleted test account " + username)
    g_driver.close()
    print_summary()

def test_comparison(found, expected, test_details):
    global g_tests_ran, g_passed_tests, g_failed_tests, g_summary_details, g_driver
    g_tests_ran += 1
    print("\nTest #" + str(g_tests_ran) + "\n" + str(type(found)).split("'")[1].capitalize() + " Found:\t" + str(found) + "\n" + str(type(expected)).split("'")[1].capitalize() + " Expected:\t" + str(expected))
    if found == expected:
        g_passed_tests += 1
        g_summary_details.append([1, test_details])
        print("[PASS] " + test_details)
    else:
        g_failed_tests += 1
        g_summary_details.append([0, test_details])
        #print("[FAIL] " + test_details + "\n\nStopping Execution of Further tests")
        #g_driver.close()
        #print_summary()
        #exit(1)

def print_summary():
    global g_tests_ran, g_passed_tests, g_failed_tests, g_summary_details
    print("\nRecap:")
    for d in g_summary_details:
        if d[0]:
            print("[PASS] " + d[1])
        else:
            print("[FAIL] " + d[1])
    print("\nSummary:\n" + str(g_tests_ran) + "/" + str(g_total_tests) + " tests were ran\n" + str(g_total_tests-g_tests_ran) + "/" + str(g_total_tests) + " tests were skipped\n" + str(g_passed_tests) + "/" + str(g_tests_ran) + " tests that ran passed\n" + str(g_failed_tests) + "/" + str(g_tests_ran) + " tests that ran failed")
    

if __name__ == "__main__":
    main()