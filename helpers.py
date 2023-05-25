from flask import abort, flash, redirect, render_template, request, session, url_for
from functools import wraps
from lib.user import User


def auth_user(user):
    session["logged_in"] = True
    session["user_id"] = user.id
    session["username"] = user.username
    flash("You are logged in as %s" % (user.username))


def get_current_user():
    if session.get("logged_in"):
        return User.get(User.id == session["user_id"])


def login_required(func):
    # func is the function being wrapped
    @wraps(func)
    def inner(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("sign_in"))
        return func(*args, **kwargs)

    return inner


def object_list(template_name, qr, var_name="object_list", **kwargs):
    kwargs.update(page=int(request.args.get("page", 1)), pages=qr.count() / 20 + 1)
    kwargs[var_name] = qr.paginate(kwargs["page"])
    kwargs["user"] = get_current_user().username if get_current_user() else None
    return render_template(template_name, **kwargs)


def get_object_or_404(model, *expressions):
    try:
        return model.get(*expressions)
    except model.DoesNotExist:
        abort(404)
