import os
import logging
import webbrowser

from requests_oauthlib import OAuth2Session
from flask import Flask, request, make_response

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


def oauth_process(
    *, client_id, client_secret, auth_url, token_url, name="the application", **kwargs
):

    oauth = OAuth2Session(client_id, redirect_uri="http://localhost:61337/callback")
    authorization_url, state = oauth.authorization_url(auth_url)

    print(
        f"Please authorize stream-vcr for accessing {name}: \n\n{authorization_url}"
        "\n\nYour browser should open automatically. "
        "If that does not work please open the above URL manually. ",
        end="",
    )

    webbrowser.open(authorization_url, new=2, autoraise=True)

    app = Flask(__name__)
    app.secret_key = str(os.urandom(16))

    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)
    app.logger.setLevel(logging.ERROR)

    @app.route("/callback", methods=["GET"])
    def callback():
        try:
            token = oauth.fetch_token(
                token_url,
                client_secret=client_secret,
                authorization_response=request.url,
                include_client_id=True,
            )
            app.config["OAUTH_TOKEN"] = token
        except Exception:
            import traceback

            tb = "".join(traceback.format_exc())
            return _shutdown(f"Something went wrong:\n\n{tb}\n\nPlease try again.", 500)

        return _shutdown("All good. You may now close this window.", 200)

    def _shutdown(msg, code):
        shutdown = request.environ.get("werkzeug.server.shutdown")
        if shutdown is None:
            raise RuntimeError("Not running with the Werkzeug Server")
        shutdown()

        response = make_response(msg, code)
        response.mimetype = "text/plain"
        return response

    from werkzeug.serving import run_simple

    run_simple("localhost", 61337, app)
    print("Success!")

    return app.config["OAUTH_TOKEN"]
