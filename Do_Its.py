from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship

import re
import bcrypt
import os
import jinja2

INSTALLED_APPS = ['django.contrib.sessions']

MIDDLEWARE = ['django.contrib.sessions.middleware.SessionMiddleware']


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
GROUP_NAME = {'051': 'ЕК', '073': 'МН', '054': 'СЦ', '061': 'ЖР', '153': 'СТ', '151': 'КТ', '275': 'ТТ', '011': 'ОН',
              '125': 'КБ', '121': 'ПІ', '122': 'КН', '172': 'ІК'}
DAYS = ['Понеділок', 'Вівторок', 'Середа', 'Четверг', 'П`ятниця']
LESSON_NUMBER = ['1','2', '3', '4', '5', '6']

eng = create_engine('sqlite:///Do_Its.db')
Base = declarative_base()

schedule_table = {'Понеділок': {'1': [], '2': []}, 'Вівторок': {'1': [], '2': []}}



class Students_groups(Base):

    __tablename__ = 'Students_groups'

    id = Column(Integer, primary_key=True)
    # institute = Column(String)
    # speciality = Column(String)
    # year_of_study = Column(String)
    group_name = Column(String)

    def __init__(self, group_name):
        self.group_name = group_name

    Student =relationship('Student')


def add_students_groups(db_session):
    year_of_study = ['1', '2', '3', '4', '5', '6']
    for number_of_speciality in GROUP_NAME:
        for year in year_of_study:
            group_name = year + GROUP_NAME[number_of_speciality]
            new_group = Students_groups(group_name=group_name)
            db_session.add(new_group)
    db_session.commit()
    db_session.close()


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

    Students_groups = relationship('Students_groups')

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

    Day_of_the_week_student = relationship('Day_of_the_week_student')

    def __init__(self, group_name):
        self.group_name= group_name

    def __str__(self):
        return f'{self.group_name}'

def add_students_schedule(db_session):
    students_group_request = db_session.query(Students_groups).all()
    week = ['Понеділок', 'Вівторок', 'Середа', 'Четверг', 'П`ятниця']
    for group in students_group_request:
        group_name = group.group_name
        for day in week:
            new_group_schedule = Student_schedule(group_name=group_name, day=day )
            db_session.add(new_group_schedule)
    db_session.commit()
    db_session.close()

class Day_of_the_week_student(Base):
    __tablename__ = 'Day_of_the_week_student'
    group_name = Column(String, ForeignKey(Student_schedule.group_name))
    id = Column(Integer, primary_key=True)
    day = Column(String)
    lesson_number = Column(String)
    subject_name = Column(String, default=' ')
    teacher_name = Column(String, default=' ')
    room_number = Column(String, default=' ')
    work_type = Column(String, default=' ')
    week_type = Column(String, default=' ')

    Student_schedule = relationship('Student_schedule')


    def __init__(self, group_name,day, lesson_number, subject_name, teacher_name, room_number, work_type, week_type):
        self.group_name = group_name
        self.day = day
        self.lesson_number = lesson_number
        self.subject_name = subject_name
        self.teacher_name = teacher_name
        self.room_number = room_number
        self.work_type = work_type
        self.week_type = week_type

    def __str__(self):
        return f'{self.group_name, self.day, self.lesson_number, self.subject_name, self.teacher_name, self.room_number, self.work_type, self.week_type}'

def print_schedule(schedule):
    schedule_subject_request = db_session.query(Day_of_the_week_student).all()
    for subject in schedule_subject_request:
        if list(schedule.keys())[0] == subject.day:
            if list(schedule['Понеділок'].keys())[0] == subject.lesson_number:
                schedule['Понеділок']['1'] = [subject.subject_name, subject.teacher_name, subject.room_number,
                                                  subject.work_type, subject.week_type]
            else:
                schedule['Понеділок']['2'] = [subject.subject_name, subject.teacher_name, subject.room_number,
                                                  subject.work_type, subject.week_type]
        else:
            if schedule['Вівторок']['1'] == subject.lesson_number:
                schedule['Вівторок']['1'] = [subject.subject_name, subject.teacher_name, subject.room_number,
                                                 subject.work_type, subject.week_type]
            else:
                schedule['Вівторок']['2'] = [subject.subject_name, subject.teacher_name, subject.room_number,
                                                 subject.work_type, subject.week_type]
    db_session.close()
    return schedule


Base.metadata.bind = eng
Base.metadata.create_all()
session_maker = sessionmaker(bind=eng)
db_session = session_maker()

'''
add_students_groups(db_session)
add_students_schedule(db_session)
students_schedule_request = db_session.query(Student_schedule).all()
for group in students_schedule_request:
    print(group)
db_session.close()
'''
new_admin = Admin(admin_name = 'Do_Katya', password = '2311')
print(new_admin)
db_session.add(new_admin)
db_session.commit()
db_session.close()

'''
admin_request = db_session.query(Admin).all()
for admin in admin_request:
    print(admin.admin_name)
    print(admin.password)
'''
'''
print('sodau group')
ex_group_name = 'ІК5'
bana_group = Students_groups(ex_group_name)
db_session.add(bana_group)
db_session.commit()
group_in_table = db_session.query(Students_groups).all()
print('beru group')
for group in group_in_table:
    print(group.group_name)
db_session.close()
print('posla na huy')
'''
@app.route('/')
def index():
    return render_template('start_page.html')

@app.route('/start_page_student', methods=['GET', 'POST'])
def start_page_student():
    return render_template('start_page_student.html')

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

        speciality_list = speciality.split(', ')
        number_of_speciality = speciality_list[0]
        group_nickname = GROUP_NAME[number_of_speciality]
        correct_group_name = group_nickname + year_of_study

        group_in_table = db_session.query(Students_groups).filter(
            Students_groups.group_name == correct_group_name).first()

        if str(group_in_table) == correct_group_name:
            print('group est')
            new_student = Student(second_name, first_name, patronymic, number_of_student_ticket, institute, speciality,
                                  year_of_study, group_name, email, telephone, password)
            print(new_student)

            db_session.add(new_student)
            db_session.commit()
            db_session.close()
        else:
            print('Sozdal group')
            group_for_new_student = Students_groups(correct_group_name)
            db_session.add(group_for_new_student)
            db_session.commit()
            db_session.close()

            check_sozdal = db_session.query(Students_groups).all()
            for g in check_sozdal:
                print(g.group_name)

            new_student = Student(second_name, first_name, patronymic, number_of_student_ticket, institute, speciality,
                                  year_of_study, group_name, email, telephone, password)
            print(new_student)

            db_session.add(new_student)
            db_session.commit()
            db_session.close()
        '''
        for group in group_in_table:
            print(group.group_name)
        for group in group_in_table:
            print('check est group')
            if group.group_name == group_name:
                print('group uge est')
            else:
                print('group net')
                group_for_new_student = Students_groups(group_name)
                print('sozdal element')
                db_session.add(group_for_new_student)
                db_session.commit()
                print('dobavil v db')
        '''

        student_request = db_session.query(Student).all()

        for student in student_request:
            print(student.second_name, student.first_name, student.group_name, student.password)
        db_session.close()
        return redirect('start_page_student')
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
                    session['group_name'] = student.group_name
                    session['first_name'] = student.first_name
                    db_session.close()
                    return redirect('home_student')
                    break
    return render_template('login_student.html')

@app.route('/home_student', methods=['GET', 'POST'])
def home_student():
    return render_template('home_student.html', username=session['first_name'])

@app.route("/show_student_in_group", methods=['GET', 'POST'])
def show_student_in_group():
    my_group = {'Прізвище': [], 'Імя': [], 'Побатькове': [], 'Номер телефону':[]}
    number_of_students = []
    student_counter = 0
    student_group_request = db_session.query(Student).all()
    for student in student_group_request:
        if session['email']==student.email:
            session['group_name']=student.group_name
            db_session.close()
    need_group = session['group_name']
    print(need_group)
    stud_gr = db_session.query(Students_groups).all()
    for s in stud_gr:
        print(s.group_name)
    student_detail = db_session.query(Students_groups).filter(Students_groups.group_name == need_group).first()
    print(str(student_detail))
    for student in student_detail.Student:
        number_of_students.append(student_counter)
        student_counter = student_counter + 1
        my_group['Прізвище'].append(student.second_name)
        my_group['Імя'].append(student.first_name)
        my_group['Побатькове'].append(student.patronymic)
        my_group['Номер телефону'].append(student.telephone)
    print(my_group)
    print(my_group['Прізвище'][0])
    db_session.close()
    return render_template('show_student_in_group.html', number_of_students=number_of_students, my_group=my_group)

@app.route('/show_student_schedule', methods=['GET', 'POST'])
def show_student_schedule():
    schedule_subject_request = db_session.query(Student_schedule).filter(
        Student_schedule.group_name == session['group_name']).first()
    schedule = schedule_subject_request.Day_of_the_week_student
    db_session.close()
    return render_template('show_student_schedule.html', schedule=schedule)

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
                    db_session.close()
                    return render_template('admin_home.html', username=admin.admin_name)
                    break
    return render_template('login_admin.html')

@app.route('/admin_student_work', methods=['GET', 'POST'])
def admin_student_work():
    if request.method == 'POST':
        speciality = request.form['speciality']
        year_of_study = request.form['year_of_study']
        speciality_list = speciality.split(', ')
        number_of_speciality = speciality_list[0]
        group_nickname = GROUP_NAME[number_of_speciality]
        group_name = group_nickname + year_of_study
        check_group_schedule = db_session.query(Student_schedule).filter(Student_schedule.group_name == group_name).first()
        session['group_name'] = group_name
        print(check_group_schedule)
        print(group_name)
        if str(check_group_schedule) == group_name:
            print('if no work')
            schedule_subject_request = db_session.query(Student_schedule).filter(
                Student_schedule.group_name == group_name).first()
            schedule = schedule_subject_request.Day_of_the_week_student
            db_session.close()
            return redirect('admin_student_schedule')
        else:
            new_schedule = Student_schedule(group_name=group_name)
            db_session.add(new_schedule)
            db_session.commit()
            db_session.close()
            for day in DAYS:
                for lesson in LESSON_NUMBER:
                    window = Day_of_the_week_student(group_name=group_name, day=day, lesson_number=lesson, subject_name='', teacher_name='', room_number='', work_type='', week_type='')
                    db_session.add(window)
                    db_session.commit()
                    db_session.close()
            schedule_subject_request = db_session.query(Student_schedule).filter(Student_schedule.group_name == group_name).first()
            schedule = schedule_subject_request.Day_of_the_week_student
            db_session.close()
            return redirect('admin_student_schedule')
    return render_template('admin_student_work.html')

@app.route('/admin_student_schedule', methods=['GET', 'POST'])
def admin_student_schedule():


    if request.method == 'POST':

        print('nu hot zapustu')
        day = request.form['day']
        lesson_number = request.form['lesson_number']
        subject_name = request.form['subject_name']
        teacher_name = request.form['teacher_name']
        room_number = request.form['room_number']
        work_type = request.form['work_type']
        week_type = request.form['week_type']
        print(subject_name)

        update_windo = db_session.query(Day_of_the_week_student).filter(Day_of_the_week_student.group_name == session['group_name'], Day_of_the_week_student.day == day, Day_of_the_week_student.lesson_number == lesson_number).first()
        print(update_windo)
        update_windo.subject_name = subject_name
        update_windo.teacher_name = teacher_name
        update_windo.room_number = room_number
        update_windo.work_type = work_type
        update_windo.week_type = week_type
        db_session.commit()
        db_session.close()
        #new_day_lesson = Day_of_the_week_student(session['group_name'], day, lesson_number, subject_name, teacher_name, room_number, work_type,
                                                 #week_type)
        #print(new_day_lesson)

        #db_session.add(new_day_lesson)
        #db_session.commit()
        #db_session.close()
        print('IN BAZA')

        #check_subject_request = db_session.query(Day_of_the_week_student).all()
        #for subject in check_subject_request:
            #print(subject.subject_name)
            #print(subject.teacher_name)

        #print_schedule(schedule_table)
        schedule_subject_request = db_session.query(Student_schedule).filter(
            Student_schedule.group_name == session['group_name']).first()
        schedule = schedule_subject_request.Day_of_the_week_student
        for sub in schedule_subject_request.Day_of_the_week_student:
            print(sub)
        db_session.close()
        return render_template('admin_student_schedule.html', schedule=schedule, group_name=session['group_name'])

    #print_schedule(schedule_table)
    schedule_subject_request = db_session.query(Student_schedule).filter(
        Student_schedule.group_name == session['group_name']).first()
    schedule = schedule_subject_request.Day_of_the_week_student
    db_session.close()
    return render_template('admin_student_schedule.html', schedule=schedule, group_name=session['group_name'])

'''
@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html', schedule=schedule, some_some=some_some)
'''



if __name__ == "__main__":
    app.run()

'''
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
'''

