import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Student, Major
from datetime import datetime as dt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'university.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'beyond_course_scope'
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
def student_view_all():
    students = Student.query.outerjoin(Major, Student.major_id == Major.major_id) \
        .add_entity(Major) \
        .order_by(Student.last_name, Student.first_name) \
        .all()
    return render_template('student_view_all.html', students=students)


@app.route('/student/view/<int:student_id>')
def student_view(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    majors = Major.query.order_by(Major.major).all()
    if student:
        return render_template('student_entry.html', student=student, majors=majors, action='read')
    else:
        flash('Student attempting to be viewed could not be found!', 'error')
        return redirect(url_for('student_view_all'))


@app.route('/student/create', methods=['GET', 'POST'])
def student_create():
    if request.method == 'GET':
        majors = Major.query.order_by(Major.major).all()
        return render_template('student_entry.html', majors=majors, action='create')
    elif request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        major_id = request.form['major_id']
        birth_date = request.form['birth_date']
        is_honors = True if 'is_honors' in request.form else False
        email = request.form['email']

        student = Student(first_name=first_name, last_name=last_name, major_id=major_id,
                          birth_date=dt.strptime(birth_date, '%Y-%m-%d'),
                          is_honors=is_honors, email=email)
        db.session.add(student)
        db.session.commit()
        flash(f'{first_name} {last_name} was successfully added!', 'success')
        return redirect(url_for('student_view_all'))

    flash('Invalid action. Please try again.', 'error')
    return redirect(url_for('student_view_all'))


@app.route('/student/update/<int:student_id>', methods=['GET', 'POST'])
def student_edit(student_id):
    if request.method == 'GET':
        student = Student.query.filter_by(student_id=student_id).first()
        majors = Major.query.order_by(Major.major).all()
        if student:
            return render_template('student_entry.html', student=student, majors=majors, action='update')
        else:
            flash('Student attempting to be edited could not be found!', 'error')

    elif request.method == 'POST':
        student = Student.query.filter_by(student_id=student_id).first()
        if student:
            student.first_name = request.form['first_name']
            student.last_name = request.form['last_name']
            student.major_id = request.form['major_id']
            student.birth_date = dt.strptime(request.form['birth_date'], '%Y-%m-%d')
            student.num_credits_completed = request.form['num_credits_completed']
            student.gpa = request.form['gpa']
            student.is_honors = True if 'is_honors' in request.form else False
            student.email = request.form['email']
            db.session.commit()
            flash(f'{student.first_name} {student.last_name} was successfully updated!', 'success')
        else:
            flash('Student attempting to be edited could not be found!', 'error')

        return redirect(url_for('student_view_all'))

    return redirect(url_for('student_view_all'))


@app.route('/student/delete/<int:student_id>')
def student_delete(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    if student:
        db.session.delete(student)
        db.session.commit()
        flash(f'{student} was successfully deleted!', 'success')
    else:
        flash('Delete failed! Student could not be found.', 'error')
    return redirect(url_for('student_view_all'))


if __name__ == '__main__':
    app.run()