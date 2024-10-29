import mysql.connector
from mysql.connector import Error
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connection settings
HOST = os.getenv('localhost')
USER = os.getenv('ecom_user')
PASSWORD = os.getenv('fifadg13')
DATABASE = os.getenv('ecommerce_shop')

def create_connection():
    """Create a database connection"""
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
        return None


def execute_query(connection, query, data):
    """Execute a single query"""
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def insert_data():
    connection = create_connection()

    if connection is None:
        return

    # Inserting data into STUDENTS table
    students_query = """
    INSERT INTO STUDENTS (ID, FIRST_NAME, LAST_NAME, EMAIL, PHONE, COURSE, EDUCATIONAL_DEGREE, SPECIALITY, ACTIVE) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    students_data = [
        (str(uuid.uuid4()), 'John', 'Doe', 'john.doe@example.com', '1234567890', 1, 'Bachelor', 'Computer Science',
         True),
        (str(uuid.uuid4()), 'Jane', 'Smith', 'jane.smith@example.com', '0987654321', 2, 'Master', 'Mathematics', True)
        # Add more student records as needed
    ]
    for data in students_data:
        execute_query(connection, students_query, data)

    # Inserting data into ROOMS table
    rooms_query = """
    INSERT INTO ROOMS (ID, BUILDING, FLOOR, NUMBER, DISPLAY_NAME, SEATS_NUMBER) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    rooms_data = [
        (str(uuid.uuid4()), 'Building A', 1, 101, 'Room 101', 30),
        (str(uuid.uuid4()), 'Building B', 2, 202, 'Room 202', 50)
        # Add more room records as needed
    ]
    for data in rooms_data:
        execute_query(connection, rooms_query, data)

    # Inserting data into COURSES table
    courses_query = """
    INSERT INTO COURSES (ID, COURSE_DISPLAY_SHORT_NAME, COURSE_DISPLAY_FULL_NAME, COURSE_DESCRIPTION, LECTURES_NUM, PRACTICES_NUM) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    courses_data = [
        (str(uuid.uuid4()), 'CS101', 'Introduction to Computer Science', 'Basic concepts of computer science', 30, 15),
        (str(uuid.uuid4()), 'MATH201', 'Advanced Mathematics', 'In-depth study of advanced mathematical concepts', 25,
         10)
        # Add more course records as needed
    ]
    for data in courses_data:
        execute_query(connection, courses_query, data)

    # Inserting data into INSTRUCTORS table
    instructors_query = """
    INSERT INTO INSTRUCTORS (ID, FIRST_NAME, LAST_NAME, EMAIL, PHONE, ACTIVE) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    instructors_data = [
        (str(uuid.uuid4()), 'Alice', 'Johnson', 'alice.johnson@example.com', '1122334455', True),
        (str(uuid.uuid4()), 'Bob', 'Williams', 'bob.williams@example.com', '5544332211', True)
        # Add more instructor records as needed
    ]
    for data in instructors_data:
        execute_query(connection, instructors_query, data)

    # Inserting data into LESSONS_SCHEDULE table
    lessons_schedule_query = """
    INSERT INTO LESSONS_SCHEDULE (ID, START_TIME, END_TIME) 
    VALUES (%s, %s, %s)
    """
    lessons_schedule_data = [
        (1, '08:00:00', '09:00:00'),
        (2, '09:00:00', '10:00:00')
        # Add more lesson schedule records as needed
    ]
    for data in lessons_schedule_data:
        execute_query(connection, lessons_schedule_query, data)

    # Inserting data into INSTRUCTORS_COURSES table
    instructors_courses_query = """
    INSERT INTO INSTRUCTORS_COURSES (INSTRUCTOR_ID, COURSE_ID) 
    VALUES (%s, %s)
    """
    instructors_courses_data = [
        (instructors_data[0][0], courses_data[0][0]),
        (instructors_data[1][0], courses_data[1][0])
        # Add more instructor-course relationships as needed
    ]
    for data in instructors_courses_data:
        execute_query(connection, instructors_courses_query, data)

    # Inserting data into STUDENTS_COURSE_GROUPS table
    students_course_groups_query = """
    INSERT INTO STUDENTS_COURSE_GROUPS (ID, COURSE_ID) 
    VALUES (%s, %s)
    """
    students_course_groups_data = [
        (str(uuid.uuid4()), courses_data[0][0]),
        (str(uuid.uuid4()), courses_data[1][0])
        # Add more student course group records as needed
    ]
    for data in students_course_groups_data:
        execute_query(connection, students_course_groups_query, data)

    # Inserting data into STUDENTS_COURSE_GROUP_STUDENTS table
    students_course_group_students_query = """
    INSERT INTO STUDENTS_COURSE_GROUP_STUDENTS (STUDENT_ID, GROUP_ID) 
    VALUES (%s, %s)
    """
    students_course_group_students_data = [
        (students_data[0][0], students_course_groups_data[0][0]),
        (students_data[1][0], students_course_groups_data[1][0])
        # Add more student-group relationships as needed
    ]
    for data in students_course_group_students_data:
        execute_query(connection, students_course_group_students_query, data)

    # Inserting data into SCHEDULE table
    schedule_query = """
    INSERT INTO SCHEDULE (ID, COURSE_ID, INSTRUCTOR_ID, STUDENTS_COURSE_GROUP_ID, WEEK_DAY, LESSON_SCHEDULE_ID, ROOM_ID) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    schedule_data = [
        (1, courses_data[0][0], instructors_data[0][0], students_course_groups_data[0][0], 'Monday', 1,
         rooms_data[0][0]),
        (2, courses_data[1][0], instructors_data[1][0], students_course_groups_data[1][0], 'Tuesday', 2,
         rooms_data[1][0])
        # Add more schedule records as needed
    ]
    for data in schedule_data:
        execute_query(connection, schedule_query, data)

    connection.close()


if __name__ == "__main__":
    insert_data()
