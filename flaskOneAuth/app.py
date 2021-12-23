# imports for Flask
from flask import Flask, Response
from flask import redirect, g, url_for
from os import environ
from flask_oidc import OpenIDConnect

app = Flask(__name__)

# è¿ç»å° OneAuth æå¡çFlaskåæ°è®¾ç½®
app.config["OIDC_CLIENT_SECRETS"] = "openidconnect_secrets.json"
# å¿é¡»å¨çäº§ç¯å¢ä¸­å°æ­¤è®¾ç½®ä¸º True
app.config["OIDC_COOKIE_SECURE"] = False
# Webåºç¨ä¸­ç¨äºå¤çç¨æ·ç»å½ç URL
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
# ç¨æ·ç»å½æ¶è¦è¯·æ±çæå³ç¨æ·çæ°æ®ï¼æ­¤å¤æä»¬è¦æ±æä¾åºæ¬ççµå­é®ä»¶ãå§ååä¸ªäººèµæä¿¡æ¯
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
# è¿æ¯ä¸ä¸ª Flask è®¾ç½®ï¼ç¨äºç¡®ä¿ä¼è¯å®å¨ï¼ç»ä¸è½å¬å¼å®
app.config["SECRET_KEY"] = environ.get("SECRET_KEY")
app.config["OIDC_ID_TOKEN_COOKIE_NAME"] = "oidc_token"

oidc = OpenIDConnect(app)


@app.before_request
def before_request():
    """å®ç°æ£æ¥ç¨æ·æ¯å¦å¨æ¯æ¬¡è¯·æ±ä¹åç»å½è¿"""
    if oidc.user_loggedin:
        g.user = oidc.user_getfield("sub")
        print(g.user)
    else:
        g.user = None

@app.route("/protectme")
@oidc.require_login
def protect_me():
    return Response("I should be protected!")

@app.route("/")
def landing_page():
    return Response("I am open for any visitors")

@app.route("/login")
@oidc.require_login
def login():
    return redirect(url_for(".protectme"))

@app.route("/logout")
def logout():
    oidc.logout()
    return redirect(url_for(".landing_page"))

