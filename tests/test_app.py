from playwright.sync_api import Page, expect

"""
I am unable to view my account page if I am not logged in
When I visit the index page
I can see that I am not signed in
and so navigate to the sign up
where I sign up
I am redirected back to the login page
with a flash message to say I have successfuly signed up
I try to sign up again
but am re-directed back to the index page
I am able to visit my account page
"""
def test_sign_up(db_connection, page, test_web_address):
    db_connection.seed("seeds/users.sql")
    page.goto(f"http://{test_web_address}/")
    expect(page.locator(".sign_up")).to_have_text("click here to sign up")
    page.click("text=click here to sign up")
    page.fill("input[name='email']", "test@email.com")
    page.fill("input[name='password']", "password")
    page.click("text=Sign Up")
    # page.screenshot(path='screenshot.png')
    # print(page.content())
    flash = page.locator(".t-flash")
    expect(flash).to_have_text("You successfully made an account")
    assert page.url == f"http://{test_web_address}/"
    page.goto(f"http://{test_web_address}/sign_up")
    assert page.url == f"http://{test_web_address}/"


"""
When I am not logged in
I cannot visit my account page
After I log in
I am able to
"""
def test_visit_account_page(db_connection, page, test_web_address):
    db_connection.seed("seeds/users.sql")
    page.goto(f"http://{test_web_address}/account")
    assert page.url == f"http://{test_web_address}/login"
    flash = page.locator(".t-flash")
    expect(flash).to_have_text("please log in")
    page.fill("input[name='email']", "test@gmail.com")
    page.fill("input[name='password']", "s3cretp4ss")
    # had to use this one becase of the flash message 'please log in'
    page.click('input[type="submit"][value="Log In"]')
    # page.screenshot(path='screenshot.png')
    # print(page.content())
    page.click("text=Account")
    header = page.locator(".t-message")
    expect(header).to_have_text("Your Account!")


"""
When I try to sign up using an email I've already made an account with
I am informed and redirected to the login page
"""

def test_sign_up_with_existing_account(db_connection, page, test_web_address):
    db_connection.seed("seeds/users.sql")
    page.goto(f"http://{test_web_address}/sign_up")
    page.fill("input[name='email']", "test@gmail.com")
    page.fill("input[name='password']", "password")
    page.click("text=Sign Up")
    assert page.url == f"http://{test_web_address}/login"
    flash = page.locator(".t-flash")
    expect(flash).to_have_text("You already have an account")


"""
When I visit the index page
I can see that I am not logged in
and so navigate to the login page
where I try to log in with invalid credentials
I am redirected back to the login page with errors as a result
"""
def test_login_with_invalid_password(db_connection, page, test_web_address):
    db_connection.seed("seeds/users.sql")
    page.goto(f"http://{test_web_address}/")
    expect(page.locator(".login-status")).to_have_text("click here to log in")
    page.click("text=click here to log in")
    page.fill("input[name='email']", "test@gmail.com")
    page.fill("input[name='password']", "wrong")
    page.click("text=Log In")
    errors = page.locator(".t-errors")
    expect(errors).to_have_text("invalid credentials")
    assert page.url == f"http://{test_web_address}/login"


"""
When I visit the index page
I can see that I am not logged in
and so navigate to the login page
where I log in with the correct details
and so am redirected back to the index page
where it says I am logged in
if I navigate back to the log in page
I am redirected back to the index page
where I can click log out
on which I am signed out and redirected to the index page
"""
def test_login_with_valid_password(db_connection, page, test_web_address):
    db_connection.seed("seeds/users.sql")
    page.goto(f"http://{test_web_address}/")
    expect(page.locator(".login-status")).to_have_text("click here to log in")
    page.click("text=click here to log in")
    page.fill("input[name='email']", "test@gmail.com")
    page.fill("input[name='password']", "s3cretp4ss")
    page.click("text=Log In")
    expect(page.locator(".login-status")).to_have_text("click here to log out")
    page.goto(f"http://{test_web_address}/login")
    expect(page.locator(".login-status")).to_have_text("click here to log out")
    page.click("text=click here to log out")
    expect(page.locator(".login-status")).to_have_text("click here to log in")


