import os
import random
from selenium import webdriver

# Global variable initialization
g_total_tests = 5
g_tests_ran = 0
g_passed_tests = 0
g_failed_tests = 0
g_summary_details = []
# Global profile/driver setup for Firefox
g_profile = webdriver.FirefoxProfile()
g_profile.accept_untrusted_certs = True
g_driver = webdriver.Firefox(firefox_profile=g_profile)
# Dummy admin account for testing
g_admin_username = "test_admin"
g_admin_password = "5v1dbq7wwu"

def new_random_string(length=10):
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join((random.choice(alphabet) for i in range(length)))

def main():
    global g_summary_details, g_driver
    # Test #1: Confirm we are on the log_in page before continuing
    g_driver.get('https://u1910-dev:5000/')
    compare(g_driver.title, "Log In", "Reached /log_in route")
    # Test #2: Go to sign_up page
    g_driver.find_element_by_id("sign_up_link").click()
    compare(g_driver.title, "Sign Up", "Reached /sign_up route")
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
    compare(g_driver.title, "Dashboard", "Created a new user and was auto logged in")
    # Test #4: Log out
    g_driver.find_element_by_id("log_out_link").click()
    compare(g_driver.title, "Log In", "Logged out and auto returned to the log_in page")
    # Test #5: Log in as test user
    g_driver.find_element_by_id("username_input").send_keys(username)
    g_driver.find_element_by_id("password_input").send_keys(password)
    g_driver.find_element_by_id("submit_button").click()
    compare(g_driver.title, "Dashboard", "Logged in to an existing user")
    # Test #6: Go to profile page
    g_driver.find_element_by_id("profile_link").click()
    compare(g_driver.title, "Profile", "Reached /profile route")
    # Test #7: Go to change_password page
    g_driver.find_element_by_id("change_password_link").click()
    compare(g_driver.title, "Change Password", "Reached /change_password route")
    # Test #8: Change password
    g_driver.find_element_by_id("old_password_input").send_keys(password)
    old_password = password
    password = new_random_string()
    g_driver.find_element_by_id("new_password_input").send_keys(password)
    g_driver.find_element_by_id("confirm_new_password_input").send_keys(password)
    g_driver.find_element_by_id("submit_button").click()
    compare(g_driver.title, "Profile", "Changed password and auto returned to profile")
    # Test #9: Log out and attempt to log back in with old password
    g_driver.find_element_by_id("log_out_link").click()
    g_driver.find_element_by_id("username_input").send_keys(username)
    g_driver.find_element_by_id("password_input").send_keys(old_password)
    g_driver.find_element_by_id("submit_button").click()
    compare(g_driver.title, "Log In", "Not allowed to log back in with old password")
    # Test #10: Log in with new password
    g_driver.find_element_by_id("username_input").send_keys(username)
    g_driver.find_element_by_id("password_input").send_keys(password)
    g_driver.find_element_by_id("submit_button").click()
    compare(g_driver.title, "Dashboard", "Logged in with new password")
    # Test #11: Submit network request
    g_driver.find_element_by_id("network_request_input").click()
    g_driver.find_element_by_id("submit_button").click()
    g_driver.find_element_by_id("log_out_link").click()
    g_driver.find_element_by_id("username_input").send_keys(g_admin_username)
    g_driver.find_element_by_id("password_input").send_keys(g_admin_password)
    g_driver.find_element_by_id("submit_button").click()
    # Clean up
    g_driver.close()
    print_summary()
    exit(0)

def compare(found, expected, test_details):
    global g_tests_ran, g_passed_tests, g_failed_tests, g_summary_details, g_driver
    g_tests_ran += 1
    print("\nTest #" + str(g_tests_ran) + "\nText Found:\t" + found + "\nText Expected:\t" + expected)
    if found == expected:
        g_passed_tests += 1
        g_summary_details.append([1, test_details])
        print("[" + u'\u2713' + "] " + test_details)
    else:
        g_failed_tests += 1
        g_summary_details.append([0, test_details])
        print("[" + u'\u2718' + "] " + test_details + "\n\nStopping Execution of Further tests")
        g_driver.close()
        print_summary()
        exit(1)

def print_summary():
    global g_tests_ran, g_passed_tests, g_failed_tests, g_summary_details
    print("\nRecap:")
    for d in g_summary_details:
        if d[0]:
            print("[" + u'\u2713' + "] " + d[1])
        else:
            print("[" + u'\u2718' + "] " + d[1])
    print("\nSummary:\n" + str(g_tests_ran) + "/" + str(g_total_tests) + " tests were ran\n" + str(g_total_tests-g_tests_ran) + "/" + str(g_total_tests) + " tests were skipped\n" + str(g_passed_tests) + "/" + str(g_tests_ran) + " tests that ran passed\n" + str(g_failed_tests) + "/" + str(g_tests_ran) + " tests that ran failed")
    

if __name__ == "__main__":
    main()