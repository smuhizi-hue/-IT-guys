import base64
import urllib.error
import urllib.request

BASE_URL = "http://127.0.0.1:8000/"


def request_with_auth(username=None, password=None):
    req = urllib.request.Request(BASE_URL)

    if username is not None and password is not None:
        credentials = f"{username}:{password}".encode("utf-8")
        auth_header = base64.b64encode(credentials).decode("utf-8")
        req.add_header("Authorization", f"Basic {auth_header}")

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode("utf-8")
            return response.status, body
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8")


def main():
    no_auth_status, no_auth_body = request_with_auth()
    print("No auth:", no_auth_status, no_auth_body)
    assert no_auth_status == 401

    valid_status, valid_body = request_with_auth("admin", "12345")
    print("Valid auth:", valid_status, valid_body)
    assert valid_status == 200

    wrong_pass_status, wrong_pass_body = request_with_auth("admin", "wrongpass")
    print("Wrong password:", wrong_pass_status, wrong_pass_body)
    assert wrong_pass_status == 401

    print("Step 3 auth checks passed.")


if __name__ == "__main__":
    main()
