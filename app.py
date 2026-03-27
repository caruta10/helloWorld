from flask import Flask, render_template, request, redirect, url_for
from models import db, Student

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///university.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def hello_world():
    return "Hello World from Caden! I am adding my first code change!"

@app.route('/hello')
def hello():
    return render_template("hello.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/about-css')
def about_css():
    return render_template("about-css.html")

@app.route('/favorite-course')
def favorite_course():
    subject = request.args.get('subject', '')
    course_number = request.args.get('course_number', '')
    return render_template("favorite-course.html", subject=subject, course_number=course_number)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        email = request.form.get('email', '')
        message = request.form.get('message', '')
        return render_template("contact.html", submitted=True,
                               first_name=first_name, last_name=last_name,
                               email=email, message=message)
    return render_template("contact.html", submitted=False)



@app.route('/student/view')
def student_view():
    students = Student.query.order_by(Student.last_name).all()
    success = request.args.get('success', '')
    return render_template("student_view_all.html", students=students, success=success)

@app.route('/student/view/<int:student_id>')
def student_view_one(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template("student_view_one.html", student=student)

@app.route('/student/create', methods=['GET', 'POST'])
def student_create():
    if request.method == 'POST':
        student = Student(
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            birth_date=request.form.get('birth_date'),
            major=request.form.get('major'),
            credits_completed=int(request.form.get('credits_completed', 0)),
            gpa=float(request.form.get('gpa', 0.0)),
            is_honors=request.form.get('is_honors') == 'on',
            email=request.form.get('email')
        )
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('student_view', success=f"{student.first_name} {student.last_name} was successfully added!"))
    return render_template("student_entry.html", student=None, action="create")

@app.route('/student/update/<int:student_id>', methods=['GET', 'POST'])
def student_update(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.first_name = request.form.get('first_name')
        student.last_name = request.form.get('last_name')
        student.birth_date = request.form.get('birth_date')
        student.major = request.form.get('major')
        student.credits_completed = int(request.form.get('credits_completed', 0))
        student.gpa = float(request.form.get('gpa', 0.0))
        student.is_honors = request.form.get('is_honors') == 'on'
        student.email = request.form.get('email')
        db.session.commit()
        return redirect(url_for('student_view', success=f"{student.first_name} {student.last_name} was successfully updated!"))
    return render_template("student_entry.html", student=student, action="update")

@app.route('/student/delete/<int:student_id>', methods=['POST'])
def student_delete(student_id):
    student = Student.query.get_or_404(student_id)
    name = f"{student.first_name} {student.last_name}"
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('student_view', success=f"{name} was successfully deleted!"))

if __name__ == '__main__':
    app.run()