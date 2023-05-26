from playwright.sync_api import Page, expect

"""
I navigate from the landing page to the sign in page
I select the option to sign up
I create an account
I am redirect to the land page
"""


def test_sign_up(db_connection, page, test_web_address):
    db_connection.seed("seeds/chitter.sql")
    page.goto(f"http://{test_web_address}/")
