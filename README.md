# Stumble Guys web automation

Automated tests for the Stumble Guys web portal (https://www.stumbleguys.com/), written in Python.
Desktop runs use Playwright on Chrome. Mobile runs use Appium on a real iPhone 15 in the BrowserStack cloud.

## What is covered

| Area | Desktop (Playwright) | Mobile (Appium, iPhone 15) |
| --- | --- | --- |
| Home page | Play Now button is shown | - |
| Login | Login form offers email login, invalid email shows an error, a valid email reaches the OTP screen, a saved session stays logged in | Login form offers email login, invalid email shows an error |
| Purchase | A visitor is asked to log in when buying, a logged-in user reaches the card form | A visitor is asked to log in when buying and reaches the card form |

The purchase test stops on the card details form. It never types card details and never clicks Pay.

## Project structure

```
pages/            page objects (desktop) and pages/mobile (Appium)
tests/desktop/    Playwright tests
tests/mobile/     Appium tests
utils/            config, session helpers, BrowserStack settings
conftest.py       shared fixtures (base URL, logged-in page)
pytest.ini        pytest settings
```

## Setup

You need Python 3.12 or newer (developed on 3.14).

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Copy `.env.example` to `.env` and fill it in:

- `TEST_EMAIL`: an email address that can receive the login code
- `BROWSERSTACK_USERNAME` and `BROWSERSTACK_ACCESS_KEY`: only needed for the mobile tests

## Running the desktop tests

```
python -m pytest --headed
```

Leave out `--headed` to run without a visible browser.

The login test with a valid email sends a real code email each time it runs. To skip it:

```
python -m pytest -k "not otp"
```

### Logged-in tests and the saved session

The site logs in with a one-time code sent by email. Tests that need a
logged-in user reuse a session saved once by hand:

```
python -m utils.save_session
```

A browser opens. Log in with your email and the code, wait until the page shows you as logged in, then press
Enter in the terminal. The session is stored in `auth/` . Without it, the logged-in tests are
skipped with a message. If they start failing with a "Session expired" dialog, save a new session.

## Running the mobile tests

```
python -m pytest tests/mobile/test_mobile_flows.py -v
```

These start sessions on a real iPhone 15 in BrowserStack and use trial minutes, so they are not part of the
default run.

There is also an interactive purchase test for iOS, which asks you to type the login code from your email:

```
python -m pytest tests/mobile/test_mobile_purchase.py -s -v
```

It is an experiment and is not part of the default run. See the limitations below.

## Supported browsers and devices

- Desktop: Chrome (Playwright Chromium)
- Mobile: iPhone 15, iOS 17 etc, real device on BrowserStack, driven with Appium

## Assumptions and limitations

- The logged-in tests depend on a session saved by hand and not on a
  fresh login to avoid getting the email address rate-limited.
- BrowserStack automation does not support Chrome itself on iOS, so the mobile tests run the Chromium
  browser on the iPhone. It runs on the same iOS browser engine as Chrome for iOS.
- The item card in the shop is found by its styling classes, which are the only handle the page offers. They
  may need updating if the site is redesigned.
- The price currency depends on the region, so the tests match any common currency symbol.
- The WebGL game (bonus) is not covered yet.
- The three iOS tests that pass cover : the login form, the invalid email error and the
  shop asking a visitor to log in.
- The iOS purchase flow (log in with a code, then reach the card form) is not part of the passing suite. The
  login redirects to Scopely's sign-in page, and on the BrowserStack iPhone the test did not get from that
  page to the code boxes. The same flow was checked by hand on an emulated iPhone (WebKit, iPhone 15 profile)
  and worked. The desktop purchase flow is fully automated.
