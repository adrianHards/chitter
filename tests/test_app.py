from playwright.sync_api import Page, expect
import time

"""
I visit the landing page and try to peep
I see that I am not able to without an account
"""


def test_failed_peep(db_connection, page, test_web_address):
    db_connection.seed("seeds/chitter.sql")
    page.goto(f"http://{test_web_address}/")
    page.locator("#message").fill("peep")
    page.click("text=Peep")
    time.sleep(1)
    flash_message = page.wait_for_selector(".flash-message")
    assert flash_message.inner_text() == "Please log in to peep"


"""
I navigate from the landing page to the sign in page
I select the option to sign up
I create an account
I am redirected to the landing page
"""


def test_sign_up(db_connection, page, test_web_address):
    db_connection.seed("seeds/chitter.sql")
    page.goto(f"http://{test_web_address}/")
    page.screenshot(path="screenshot.png")
    # the navbar is overlaying the sign-in button
    page.eval_on_selector(".logo", "element => element.remove()")
    page.click(".sign-in a")
    assert page.url == f"http://{test_web_address}/sign_in/"
    page.click('text="Sign Up"')
    page.screenshot(path="screenshot.png")
    assert page.url == f"http://{test_web_address}/sign_up/"
    page.fill("input[name='username']", "test")
    page.fill("input[name='email']", "test@email.com")
    page.fill("input[name='password']", "password")
    page.click('text="Sign Up"')
    assert page.url == f"http://{test_web_address}/"
    time.sleep(1)
    flash_message = page.wait_for_selector(".flash-message")
    assert flash_message.inner_text() == "You are logged in as test"


"""
I select the option to sign up and create an account
I then log out, and try to create an account with an existing username
I am unable to make a new account
"""


def test_fail_to_sign_up_with_existing_username(db_connection, page, test_web_address):
    db_connection.seed("seeds/chitter.sql")
    page.goto(f"http://{test_web_address}/sign_up")
    page.fill("input[name='username']", "test")
    page.fill("input[name='email']", "test@email.com")
    page.fill("input[name='password']", "password")
    page.click('text="Sign Up"')
    page.eval_on_selector(".logo", "element => element.remove()")
    page.click(".sign-out a")
    page.goto(f"http://{test_web_address}/sign_up")
    page.fill("input[name='username']", "test")
    page.fill("input[name='email']", "test@email.com")
    page.fill("input[name='password']", "password")
    page.click('text="Sign Up"')
    flash_message = page.wait_for_selector(".flash-message")
    assert flash_message.inner_text() == "That username is already taken"


"""
After creating an account
I am able to peep
And immediately see my peep
"""


def test_successful_peep(db_connection, page, test_web_address):
    db_connection.seed("seeds/chitter.sql")
    page.goto(f"http://{test_web_address}/sign_up")
    page.fill("input[name='username']", "test")
    page.fill("input[name='email']", "test@email.com")
    page.fill("input[name='password']", "password")
    page.click('text="Sign Up"')
    page.screenshot(path="screenshot.png")
