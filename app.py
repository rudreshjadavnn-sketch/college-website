from config import Config
from models import db, Admission, Gallery, Course, Faculty
from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.security import check_password_hash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():

    faculty_list = Faculty.query.order_by(Faculty.id.desc()).all()

    return render_template(
        "about.html",
        faculty_list=faculty_list
    )


@app.route("/courses")
def courses():

    courses = Course.query.order_by(Course.id.desc()).all()

    return render_template(
        "courses.html",
        courses=courses
    )


@app.route("/gallery")
def gallery():

    images = Gallery.query.order_by(Gallery.id.desc()).all()

    return render_template(
        "gallery.html",
        images=images
    )


@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        student = Admission(

            name=request.form["name"],

            email=request.form["email"],

            phone=request.form["phone"],

            course=request.form["course"],

            address=request.form["address"],

            message=request.form["message"]

        )

        db.session.add(student)

        db.session.commit()

        flash("Admission form submitted successfully!")

        return redirect("/contact")

    return render_template("contact.html")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":

            session["admin"] = True

            return redirect("/admin/dashboard")

        flash("Invalid Username or Password")

    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():

    session.pop("admin", None)

    return redirect("/admin/login")

@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect("/admin/login")

    total_forms = Admission.query.count()
    total_images = Gallery.query.count()

    return render_template(
        "admin_dashboard.html",
        total_forms=total_forms,
        total_images=total_images
    )

@app.route("/admin/forms")
def admin_forms():

    if "admin" not in session:
        return redirect("/admin/login")

    forms = Admission.query.order_by(Admission.id.desc()).all()

    return render_template(
        "admin_forms.html",
        forms=forms
    )


@app.route("/admin/forms/delete/<int:id>")
def delete_form(id):

    if "admin" not in session:
        return redirect("/admin/login")

    form = Admission.query.get_or_404(id)

    db.session.delete(form)

    db.session.commit()

    return redirect("/admin/forms")

@app.route("/admin/gallery", methods=["GET", "POST"])
def admin_gallery():

    if "admin" not in session:
        return redirect("/admin/login")

    if request.method == "POST":

        file = request.files["image"]

        if file:

            filename = secure_filename(file.filename)

            path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            file.save(path)

            image = Gallery(

                image_name=filename,

                image_path="uploads/" + filename

            )

            db.session.add(image)

            db.session.commit()

            return redirect("/admin/gallery")

    images = Gallery.query.order_by(Gallery.id.desc()).all()

    return render_template(
        "admin_gallery.html",
        images=images
    )

@app.route("/admin/courses", methods=["GET", "POST"])
def admin_courses():

    if "admin" not in session:
        return redirect("/admin/login")

    if request.method == "POST":

        file = request.files["image"]

        filename = ""

        if file and file.filename != "":

            filename = secure_filename(file.filename)

            os.makedirs("static/uploads", exist_ok=True)

            file.save(os.path.join("static/uploads", filename))

        course = Course(

            course_name=request.form["course_name"],

            duration=request.form["duration"],

            fees=request.form["fees"],

            description=request.form["description"],

            image_path="uploads/" + filename if filename else ""

        )

        db.session.add(course)

        db.session.commit()

        return redirect("/admin/courses")

    courses = Course.query.order_by(Course.id.desc()).all()

    return render_template(
        "admin_courses.html",
        courses=courses
    )

@app.route("/admin/gallery/delete/<int:id>")
def delete_image(id):

    if "admin" not in session:
        return redirect("/admin/login")

    image = Gallery.query.get_or_404(id)

    file_path = os.path.join(
        "static",
        image.image_path
    )

    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(image)

    db.session.commit()

    return redirect("/admin/gallery")

@app.route("/admin/course/delete/<int:id>")
def delete_course(id):

    if "admin" not in session:
        return redirect("/admin/login")

    course = Course.query.get_or_404(id)

    if course.image_path:

        path = os.path.join("static", course.image_path)

        if os.path.exists(path):
            os.remove(path)

    db.session.delete(course)

    db.session.commit()

    return redirect("/admin/courses")

@app.route("/admin/faculty", methods=["GET", "POST"])
def admin_faculty():

    if "admin" not in session:
        return redirect("/admin/login")

    if request.method == "POST":

        file = request.files["image"]

        filename = ""

        if file and file.filename != "":

            filename = secure_filename(file.filename)

            os.makedirs("static/uploads", exist_ok=True)

            file.save(os.path.join("static/uploads", filename))

        faculty = Faculty(

            name=request.form["name"],
            designation=request.form["designation"],
            qualification=request.form["qualification"],
            department=request.form["department"],
            experience=request.form["experience"],
            image_path="uploads/" + filename

        )

        db.session.add(faculty)
        db.session.commit()

        return redirect("/admin/faculty")

    faculty_list = Faculty.query.order_by(Faculty.id.desc()).all()

    return render_template(
        "admin_faculty.html",
        faculty_list=faculty_list
    )

@app.route("/admin/faculty/delete/<int:id>")
def delete_faculty(id):

    if "admin" not in session:
        return redirect("/admin/login")

    faculty = Faculty.query.get_or_404(id)

    path = os.path.join("static", faculty.image_path)

    if os.path.exists(path):
        os.remove(path)

    db.session.delete(faculty)
    db.session.commit()

    return redirect("/admin/faculty")



if __name__ == "__main__":
    app.run(debug=True)