import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE subjects (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL
)
''')

cursor.execute('''
CREATE TABLE student_subjects (
    id INTEGER PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES student (id),
    FOREIGN KEY (subject_id) REFERENCES subject (id)
)
''')

conn.commit()

cursor.execute("INSERT INTO student (name, age) VALUES ('John Smith', 20)")
cursor.execute("INSERT INTO student (name, age) VALUES ('Alice Johnson', 22)")
cursor.execute("INSERT INTO student (name, age) VALUES ('Bob Anderson', 21)")

cursor.execute("INSERT INTO subject (name) VALUES ('Math')")
cursor.execute("INSERT INTO subject (name) VALUES ('Science')")
cursor.execute("INSERT INTO subject (name) VALUES ('History')")
cursor.execute("INSERT INTO subject (name) VALUES ('English')")

cursor.execute("INSERT INTO student_subject (student_id, subject_id) VALUES (1, 1)")
cursor.execute("INSERT INTO student_subject (student_id, subject_id) VALUES (2, 2)")
cursor.execute("INSERT INTO student_subject (student_id, subject_id) VALUES (3, 3)")

conn.commit()
conn.close()


engine = create_engine('sqlite:///my_database.db')
Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class StudentSubject(Base):
    __tablename__ = 'student_subjects'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    subject_id = Column(Integer, ForeignKey('subject.id'))

    student = relationship("Student", back_populates="subjects")
    subject = relationship("Subject", back_populates="students")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.add_all([
    Student(name='John Smith', age=20),
    Student(name='Alice Johnson', age=22),
    Student(name='Bob Anderson', age=21),
])
session.commit()

session.add_all([
    Subject(name='Math'),
    Subject(name='Science'),
    Subject(name='History'),
    Subject(name='English'),
])
session.commit()

session.add_all([
    StudentSubject(student_id=1, subject_id=1),
    StudentSubject(student_id=2, subject_id=2),
    StudentSubject(student_id=3, subject_id=3),
])
session.commit()

students_with_english = session.query(Student).join(StudentSubject).join(Subject).filter(Subject.name == 'English').all()

print("Students who visited 'English' classes:")
for student in students_with_english:
    print(student.name)

session.close()