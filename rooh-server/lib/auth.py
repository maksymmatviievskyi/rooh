
import sqlite3
from aiohttp import web
from utils import verify_password, hash_password
from itertools import chain

def check_user_exists(username):
    conn = sqlite3.connect('RoohDB.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

async def register(request):
    try:
        data = await request.json()
        username = data['username']
        email = data['email']
        password = data['password']
        chest = data['chest']
        hamstrings = data['hamstrings']
        if not check_user_exists(username):
            conn = sqlite3.connect('RoohDB.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Users (Username, Email, Password) VALUES (?, ?, ?)", (username, email, hash_password(password)))
            cursor.execute("SELECT UserID FROM Users WHERE Email = ?", (email,))
            userid = cursor.fetchone()[0]
            exerciseids = []
            if chest:
                cursor.execute("SELECT ExerciseID FROM Exercises WHERE MuscleGroup = 'Chest'")
                exerciseids.append(cursor.fetchall())
            if hamstrings:
                cursor.execute("SELECT ExerciseID FROM Exercises WHERE MuscleGroup = 'Hamstrings'")
                exerciseids.append(cursor.fetchall())
            exerciseids = list(chain.from_iterable(exerciseids))
            for id in exerciseids:
                cursor.execute("INSERT INTO library (UserID, ExerciseID) VALUES (?, ?)", (userid, *id))    
            conn.commit()
            conn.close()
            return web.Response(status=200)
        return web.Response(status=403) 
    except Exception as error:
        print("Register error", error)
        return web.Response(status=500)

async def login(request):
    try:
        data = await request.json()
        email = data['email']
        password = data['password']
        
        conn = sqlite3.connect('RoohDB.db')
        cursor = conn.cursor()
        cursor.execute("SELECT Username, Password FROM Users WHERE Email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and verify_password(user[1], password): return web.json_response({"username": user[0]}, status=200)
        elif not user: return web.Response(status=404)
        return web.Response(status=403)
    except Exception as error:
        print("Authentication error: ", error)
        return web.Response(status=501)
