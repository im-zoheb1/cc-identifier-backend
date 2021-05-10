"""Helper utilities and decorators."""

import smtplib
from validate_email import validate_email
from itsdangerous import URLSafeTimedSerializer
from flask import Flask, url_for, render_template
from config import BaseConfig


SECRET_KEY = BaseConfig.SECRET_KEY
SALT = BaseConfig.SECURITY_PASSWORD_SALT
MAIL_SERVER = BaseConfig.MAIL_SERVER


def generate_confirmation_token(username):
    # confirmation email token
    serializer = URLSafeTimedSerializer( SECRET_KEY )
    return serializer.dumps({'username': username}, salt=SALT)


def confirm_token(token, expiration=3600):
    # plausibility check for confirmation token
    serializer = URLSafeTimedSerializer( SECRET_KEY )
    try:
        result = serializer.loads(token, salt=SALT, max_age=expiration)
    except:
        return False

    return result


def check_email_validation(email):
    # validating the email
	return validate_email(email)


def send_mail(email, template):
    # sending the email
	with open('./assets/email.txt', 'r') as f1:
		with open('./assets/key.txt', 'r') as f2:
			username = f1.readline()
			password = f2.readline()
			_from = f1.readline()
			_to  = email

	msg = "\r\n".join([
	  "From: " + _from,
	  "To: " + email,
	  "Subject: confirm email",
	  "",
	  "send for activate account",
	  template
	  ])
	server = smtplib.SMTP( MAIL_SERVER )
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(_from, _to, msg)
	server.quit()
	return


def send_confirmation_mail(email, username):
    # send confirmation token to the user
	token = generate_confirmation_token(username)
	confirm_url = url_for('userverification', token=token, _external=True)
	html = render_template('confirmation.html', confirm_url=confirm_url)
	send_mail(email, html)
	return 