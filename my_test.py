from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from Do_Its import Day_of_the_week_student

import re
import bcrypt
import os

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
GROUP_NAME = {'051': 'ЕК', '073': 'МН', '054': 'СЦ','061': 'ЖР','153': 'СТ','151': 'КТ','275': 'ТТ','011': 'ОН','125': 'КБ','121': 'ПІ','122': 'КН','172': 'ІК'}

eng = create_engine('sqlite:///Do_Its.db')
Base = declarative_base()

'''
session_maker = sessionmaker(bind=eng)
db_session = session_maker()

schedule = {'Понеділок':{'1':[], '2':[]}, 'Вівторок':{'1':[], '2':[]}}
subject_request = db_session.query(Day_of_the_week_student).all()
for subject in subject_request:
    print(subject)

for subject in subject_request:
    print(subject.day)
    print(schedule.items())
    if list(schedule.keys())[0] == subject.day:
        if list(schedule['Понеділок'].keys())[0] == subject.lesson_number:
            schedule['Понеділок']['1'] = [subject.subject_name, subject.teacher_name, subject.room_number, subject.work_type, subject.week_type]
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
print(schedule)

@app.route('/', methods=['GET', 'POST'])
def test():
    return render_template('test.html', schedule={schedule})

if __name__ == "__main__":
    app.run()
'''
'''
year_of_study = ['1', '2', '3', '4', '5', '6']
for number_of_speciality in GROUP_NAME:
    for year in year_of_study:
        group_name = year + GROUP_NAME[number_of_speciality]
        print(group_name)
'''

'''
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
	_group_name = Column(String, default='some')
	_headman = Column(String, default=False)
	_email = Column(String)
	telephone = Column(String)
	_password = Column(String) 


	def __init__(self, second_name, first_name, patronymic, number_of_student_ticket, institute, speciality, year_of_study, group_name, email, telephone, password):
		self.second_name = second_name
		self.first_name = first_name
		self.patronymic = patronymic
		self.number_of_student_ticket = number_of_student_ticket
		self.institute = institute
		self.speciality = speciality
		self.year_of_study = year_of_study
		self.group_name = None
		self.headman = None
		self.email = None
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
		number_of_speciality = self.speciality[0]
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


Base.metadata.bind = eng        
Base.metadata.create_all()        
        
session_maker = sessionmaker(bind=eng)
session = session_maker()  

session.add_all(
   [Student(id_student=1, second_name='student1', first_name='student1', patronymic='student1', number_of_student_ticket='VN12345', institute='IKPI', speciality=['172', 'Телекомунікацї та радіотехніка'], year_of_study='1', group_name='IK5', email='student1@sharaga.com', telephone='+3806574839', password='1234')])
session.commit()

student_request = session.query(Student).all()

for student in student_request:
    print(student.second_name, student.first_name, student.group_name, student.password)

'''





'''
import re



email_address = 'katyaklem@i.ua'


#Step 1: Check email
#Check using Regex that an email meets minimum requirements, throw an error if not

addressToVerify = email_address
match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
if match == None:
    print('Bad Syntax in ' + addressToVerify)
    raise ValueError('Bad Syntax')

'''


'''
import bcrypt

password = '12345'
print(password)
hashAndSalt = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(hashAndSalt)


second_name = 'klimenko'
print(second_name.title())
print(second_name)

ss = 'Klimenko'
print(ss.title())
print(ss)

sss = 'KLIMENKO'
print(sss.title())
print(sss)


year_of_study = '1'
speciality = ['172', 'Телекомунікацї та радіотехніка']
GROUP_NAME = {'051': 'ЕК', '073': 'МН', '054': 'СЦ','061': 'ЖР','153': 'СТ','151': 'КТ','275': 'ТТ','011': 'ОН','125': 'КБ','121': 'ПІ','122': 'КН','172': 'ІК'}

number_of_speciality = speciality[0]
group_nickname = GROUP_NAME[number_of_speciality]
group_name = group_nickname + year_of_study
print(group_name)
'''

