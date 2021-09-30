from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, AddFeedbackForm, EditFeedbackForm
from secret import SECRET_KEY
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = SECRET_KEY
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
# db.drop_all()
# db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route("/")
def home_page():
    """Home page of site redirect to register page"""
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Show user registiration and save the user in db"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Please use different username or email')
            return render_template('/users/register.html', form=form)

        session['username'] = new_user.username

        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(f"/users/{new_user.username}")

    return render_template("users/register.html", form = form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """User login form and handle login"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Invalid username or password.']

    return render_template("users/login.html", form = form)

@app.route("/logout")
def logout_user():
    """Logout"""
    if "username" in session:
        session.pop("username")
        flash("Goodbye!", "info")
        return redirect('/')


@app.route("/users/<username>")
def detail_user(username):

    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    if username != session["username"]:
        raise Unauthorized()

    user = User.query.get_or_404(username)

    return render_template("users/detail.html", user=user)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):

    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    if username != session["username"]:
        raise Unauthorized()

    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")


###### Feedback #####

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """Add feedback form and add feedback to form related to specific user"""
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    if username != session["username"]:
        raise Unauthorized()

    form = AddFeedbackForm()
    user = User.query.get_or_404(username)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title, content=content, username=user.username)
        db.session.add(feedback)
        db.session.commit()

        flash('Feedback is Created Successfully', "success")
        return redirect(f"/users/{user.username}")

    return render_template("feedbacks/add.html", form=form)

@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show Edit form and update feedback on db"""

    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    feedback = Feedback.query.get_or_404(feedback_id)
    if feedback.user.username != session["username"]:
        raise Unauthorized()

    form = EditFeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()
        flash(f"{feedback.title} Updated!", "success")
        return redirect(f"/users/{feedback.user.username}")

    return render_template("feedbacks/edit.html", form=form)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete Feedback from who has wwritten by"""
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    feedback = Feedback.query.get_or_404(feedback_id)
    if feedback.user.username != session["username"]:
        raise Unauthorized()

    db.session.delete(feedback)
    db.session.commit()
    flash(f"{feedback.title} Deleted!", "success")
    return redirect(f"/users/{feedback.user.username}")


#### if page not found ####

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

 




