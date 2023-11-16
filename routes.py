import os
import secrets
from flask import render_template, url_for, flash, redirect, request

from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func, update


def getLoginDetails():
    if current_user.is_authenticated:
        noOfItems = Cart.query.filter_by(buyer = current_user).count()
    else:
        noOfItems = 0
    return noOfItems
@app.route("/")
@app.route("/home")
