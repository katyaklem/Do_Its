from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

import re
import bcrypt
import os
import jinja2

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
GROUP_NAME = {'051': 'ЕК', '073': 'МН', '054': 'СЦ', '061': 'ЖР', '153': 'СТ', '151': 'КТ', '275': 'ТТ', '011': 'ОН',
              '125': 'КБ', '121': 'ПІ', '122': 'КН', '172': 'ІК'}

eng = create_engine('sqlite:///Do_Its.db')
Base = declarative_base()


class Students_groups(Base):
    __tablename__ = 'Students_groups'

    id = Column(Integer, primary_key=True)
    # institute = Column(String)
    # speciality = Column(String)
    # year_of_study = Column(String)
    group_name = Column(String)


def add_students_groups(db_session):
    year_of_study = ['1', '2', '3', '4', '5', '6']
    for number_of_speciality in GROUP_NAME:
        for year in year_of_study:
            group_name = year + GROUP_NAME[number_of_speciality]
            new_group = Students_groups(group_name=group_name)
            db_session.add(new_group)
    db_session.commit()


class Student(Base):
    __tablename__ = 'Students'

    id_student = Column(Integer, primary_key=True)
    _second_name = Column(String)
    _first_name = Column(String)
    _patronymic = Column(String)
    number_of_student_ticket = Column(String)
    institute = Column(String)
    speciality = Column(String)
    year_of_study = Column(String)
    _group_name = Column(String, ForeignKey(Students_groups.group_name), default='some')
    _headman = Column(String, default=False)
    _email = Column(String)
    telephone = Column(String)
    _password = Column(String)

    def __init__(self, second_name, first_name, patronymic, number_of_student_ticket, institute, speciality,
                 year_of_study, group_name, email, telephone, password):
        self.second_name = second_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.number_of_student_ticket = number_of_student_ticket
        self.institute = institute
        self.speciality = speciality
        self.year_of_study = year_of_study
        self.group_name = group_name
        self.headman = None
        self.email = email
        self.telephone = telephone
        self.password = password

    def __str__(self):
        return f'{self.first_name} {self.second_name}'

    @property
    def second_name(self):
        return self._second_name

    @second_name.setter
    def second_name(self, second_name):
        self._second_name = second_name.capitalize()
        return self._second_name

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        self._first_name = first_name.capitalize()
        return self._first_name

    @property
    def patronymic(self):
        return self._patronymic

    @patronymic.setter
    def patronymic(self, patronymic):
        self._patronymic = patronymic.capitalize()
        return self._patronymic

    @property
    def group_name(self):
        return self._group_name

    @group_name.setter
    def group_name(self, group_name):
        speciality_list = self.speciality.split(', ')
        number_of_speciality = speciality_list[0]
        group_nickname = GROUP_NAME[number_of_speciality]
        group_name = group_nickname + self.year_of_study
        self._group_name = group_name
        return self._group_name

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        addressToVerify = email
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
        if match == None:
            print('Bad Syntax in ' + addressToVerify)
            raise ValueError('Bad Syntax')
        self._email = email
        return self._email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        hashAndSalt = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self._password = hashAndSalt
        return self._password


class Admin(Base):
    __tablename__ = 'Admin'

    id_admin = Column(Integer, primary_key=True)
    admin_name = Column(String)
    _password = Column(String)

    def __init__(self, admin_name, password):
        self.admin_name = admin_name
        self.password = password

    def __str__(self):
        return f'{self.admin_name, self._password}'

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        hashAndSalt = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self._password = hashAndSalt
        return self._password


class Student_schedule(Base):
    __tablename__ = 'Student_schedule'

    id = Column(Integer, primary_key=True)
    group_name = Column(String, ForeignKey(Students_groups.group_name))
    schedule = Column(String)


class Student_group_schedule(Base):
    __tablename__ = 'Student_group_schedule'

    id = Column(Integer, primary_key=True)
    schedule = Column(String, ForeignKey(Student_schedule.schedule))
    day = Column(String)


class Day_of_the_week_student(Base):
    __tablename__ = 'Day_of_the_week_student'

    id = Column(Integer, primary_key=True)
    day = Column(String, ForeignKey(Student_group_schedule.day))
    lesson_number = Column(String)
    subject_name = Column(String)
    teacher_name = Column(String)
    room_number = Column(String)
    work_type = Column(String)
    week_type = Column(String)

    def __init__(self, day, lesson_number, subject_name, teacher_name, room_number, work_type, week_type):
        self.day = day
        self.lesson_number = lesson_number
        self.subject_name = subject_name
        self.teacher_name = teacher_name
        self.room_number = room_number
        self.work_type = work_type
        self.week_type = week_type

    def __str__(self):
        return f'{self.day, self.lesson_number, self.subject_name, self.teacher_name, self.room_number, self.work_type, self.week_type}'


Base.metadata.bind = eng
Base.metadata.create_all()
session_maker = sessionmaker(bind=eng)
db_session = session_maker()

'''
add_students_groups(db_session)
'''
'''
new_admin = Admin(admin_name = 'Do_Katya', password = '2311')
print(new_admin)
db_session.add(new_admin)
db_session.commit()

admin_request = db_session.query(Admin).all()
for admin in admin_request:
    print(admin.admin_name)
    print(admin.password)
'''


@app.route('/')
def index():
    return render_template('start_page.html')


@app.route('/registration_student', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        second_name = request.form['second_name']
        first_name = request.form['first_name']
        patronymic = request.form['patronymic']
        number_of_student_ticket = request.form['number_of_student_ticket']
        institute = request.form['institute']
        speciality = request.form['speciality']
        year_of_study = request.form['year_of_study']
        group_name = request.form['group_name']
        email = request.form['email']
        telephone = request.form['telephone']
        password = request.form['password']

        new_student = Student(second_name, first_name, patronymic, number_of_student_ticket, institute, speciality,
                              year_of_study, group_name, email, telephone, password)
        print(new_student)
        db_session.add(new_student)
        db_session.commit()

        student_request = db_session.query(Student).all()

        for student in student_request:
            print(student.second_name, student.first_name, student.group_name, student.password)

        return render_template('start_page.html')
    else:
        return render_template('registration_student.html')


@app.route('/login_student', methods=['GET', 'POST'])
def login_student():
    if request.method == 'POST':
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        print(session['email'])
        print(session['password'])
        student_request = db_session.query(Student).all()
        for student in student_request:
            if session['email'] == student.email:
                print(student.email)
                print(bcrypt.checkpw(session['password'].encode(), student.password))
                if bcrypt.checkpw(session['password'].encode(), student.password) == True:
                    return render_template('home_student.html', username={student.first_name})
                    break
    return render_template('login_student.html')


@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        session['admin_name'] = request.form['admin_name']
        session['password'] = request.form['password']
        print(session['admin_name'])
        print(session['password'])
        admin_request = db_session.query(Admin).all()
        for admin in admin_request:
            print(admin.admin_name)
            print(admin.password)
            if session['admin_name'] == admin.admin_name:
                print('нейм прошел')
                print(bcrypt.checkpw(session['password'].encode(), admin.password))
                if bcrypt.checkpw(session['password'].encode(), admin.password) == True:
                    return render_template('admin_home.html', username={admin.admin_name})
                    break
    return render_template('login_admin.html')


@app.route('/admin_student_work', methods=['GET', 'POST'])
def admin_student_work():
    return render_template('admin_student_work.html')


@app.route('/admin_student_schedule', methods=['GET', 'POST'])
def admin_student_schedule():

    subject_request = db_session.query(Day_of_the_week_student).all()

    if request.method == 'POST':
        day = request.form['day']
        lesson_number = request.form['lesson_number']
        subject_name = request.form['subject_name']
        teacher_name = request.form['teacher_name']
        room_number = request.form['room_number']
        work_type = request.form['work_type']
        week_type = request.form['week_type']
        print(subject_name)
        new_day_lesson = Day_of_the_week_student(day, lesson_number, subject_name, teacher_name, room_number, work_type,
                                                 week_type)
        print(new_day_lesson)
        db_session.add(new_day_lesson)
        db_session.commit()

        for subject in subject_request:
            print(subject.subject_name)
            print(subject.teacher_name)
        return render_template('admin_student_schedule.html')


    for subject in subject_request:
        return render_template('admin_student_schedule.html', lesson_number={subject.lesson_number},
                               subject_name={subject.subject_name}, teacher_name={subject.teacher_name},
                               room_number={subject.room_number}, work_type={subject.work_type},
                               week_type={subject.week_type})



if __name__ == "__main__":
    app.run()

'''
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
'''
