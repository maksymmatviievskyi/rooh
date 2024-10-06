import sqlite3
from utils import hash_password
# Function to create the database and table
def generateTestData(cursor):
    cursor.execute("INSERT INTO Users (Username, Email, Password) VALUES (?, ?, ?)", ('testuser', 'email@example.com', hash_password("password1")))
    cursor.execute("INSERT INTO Exercises (Name, Difficulty, MuscleGroup) VALUES (?, ?, ?)", ('Pushups', "Hard", 'Chest'))
    cursor.execute("INSERT INTO Exercises (Name, Difficulty, MuscleGroup) VALUES (?, ?, ?)", ('Squats', "Easy", 'Hamstrings'))
    cursor.execute("INSERT INTO Exercises (Name, Difficulty, MuscleGroup) VALUES (?, ?, ?)", ('Lunges', "Medium", 'Hamstrings'))
    cursor.execute("INSERT INTO Library (UserID, ExerciseID) VALUES (?, ?)", (1, 1))
    cursor.execute("INSERT INTO Library (UserID, ExerciseID) VALUES (?, ?)", (1, 2))
    cursor.execute("INSERT INTO Library (UserID, ExerciseID) VALUES (?, ?)", (1, 3))
    cursor.execute("INSERT INTO Sessions (UserID, ExerciseID, Repetitions, Date) VALUES (?, ?, ?, ?)", (1, 1, 5, "2024-02-04"))
    cursor.execute("INSERT INTO Sessions (UserID, ExerciseID, Repetitions, Date) VALUES (?, ?, ?, ?)", (1, 1, 7, "2024-03-16"))
    cursor.execute("INSERT INTO Sessions (UserID, ExerciseID, Repetitions, Date) VALUES (?, ?, ?, ?)", (1, 1, 8, "2024-04-16"))
    cursor.execute("INSERT INTO Sessions (UserID, ExerciseID, Repetitions, Date) VALUES (?, ?, ?, ?)", (1, 2, 5, "2024-01-11"))
    cursor.execute("INSERT INTO Sessions (UserID, ExerciseID, Repetitions, Date) VALUES (?, ?, ?, ?)", (1, 2, 5, "2024-01-12"))
    cursor.execute("INSERT INTO Sessions (UserID, ExerciseID, Repetitions, Date) VALUES (?, ?, ?, ?)", (1, 2, 9, "2024-04-16"))

def create_database():
    conn = sqlite3.connect('RoohDB.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users
                    (UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Username TEXT VARCHAR(30) CHECK(LENGTH(Username) >= 5) UNIQUE,
                    Email TEXT VARCHAR(40) NOT NULL UNIQUE,
                    Password TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Sessions
                    (SessionID INTEGER PRIMARY KEY AUTOINCREMENT,
                    UserID INTEGER,
                    ExerciseID INTEGER,
                    Repetitions INTEGER,
                    Date DATE,
                    FOREIGN KEY (UserID) REFERENCES Users(UserID),
                    FOREIGN KEY (ExerciseID) REFERENCES Exercises(ExerciseID))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Exercises
                    (ExerciseID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT VARCHAR(40) NOT NULL UNIQUE,
                    Difficulty TEXT VARCHAR(40) NOT NULL,
                    MuscleGroup TEXT VARCHAR(40) NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Library
                    (UserID INTEGER,
                    ExerciseID INTEGER,
                    PRIMARY KEY (UserID, ExerciseID),
                    FOREIGN KEY (UserID) REFERENCES Users(UserID),
                    FOREIGN KEY (ExerciseID) REFERENCES Exercises(ExerciseID)) ''')

    generateTestData(cursor)

    conn.commit()
    conn.close()
    