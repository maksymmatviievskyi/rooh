import asyncio
import json
import os
import aiohttp
import sqlite3
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription
import aiohttp_cors
from process import Process
from lib.auth import login, register

ROOT = os.path.dirname(__file__)
pcs = set()

process = None
analyze = None
data_channel = None
ws = None

async def get_user_library(request):
    try:
        data = await request.json()
        username = data.get('username')

        if not username:
            return web.Response(status=404)

        conn = sqlite3.connect('RoohDB.db')
        cursor = conn.cursor()
        # Get the userID in the database by their username
        cursor.execute("SELECT UserID FROM users WHERE Username = ?", (username,))
        userID = cursor.fetchone()

        # Get the exerciseIDs that belong to the user and format the array
        cursor.execute("SELECT ExerciseID FROM library WHERE UserID = ?", (userID))
        exerciseIDs = cursor.fetchall()
        exerciseIDs = [id[0] for id in exerciseIDs]

        cursor.execute("SELECT name FROM exercises WHERE ExerciseID IN (%s)" % ",".join("?"*len(exerciseIDs)), exerciseIDs)
        exerciseNames=cursor.fetchall()
        conn.close()
        return web.json_response({'exerciseNames': exerciseNames})
    except Exception as error:
        print("Fetching error: ", error)
        return web.Response(status=500)

async def get_user_sessions(request):
    try:
        data = await request.json()
        username = data.get('username')

        if not username:
            return web.Response(status=404)

        conn = sqlite3.connect('RoohDB.db')
        cursor = conn.cursor()
        # Get the UserID in the database by their username
        cursor.execute("SELECT UserID FROM users WHERE Username = ?", (username,))
        userID = cursor.fetchone()[0]

        # Get the most recent and the ealiest sessions by UserID
        cursor.execute("""SELECT s1.Repetitions, s1.Date, e1.name
                            FROM sessions AS s1
                            JOIN exercises AS e1 ON s1.ExerciseID = e1.ExerciseID
                            WHERE s1.UserID = ?
                            AND s1.Date = (SELECT MAX(Date) FROM sessions WHERE UserID = ? AND ExerciseID = s1.ExerciseID)

                            UNION

                            SELECT s2.Repetitions, s2.Date, e2.name
                            FROM sessions AS s2
                            JOIN exercises AS e2 ON s2.ExerciseID = e2.ExerciseID
                            WHERE s2.UserID = ?
                            AND s2.Date = (SELECT MIN(Date) FROM sessions WHERE UserID = ? AND ExerciseID = s2.ExerciseID)

""", (userID, userID, userID, userID))
        
        sessions = cursor.fetchall()
        conn.close()
        return web.json_response({'sessions': sessions})
    except Exception as error:
        print("Fetching error: ", error)
        return web.Response(status=500)

async def offer(request):
    global ws
    params = await request.json()

    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
    pc = RTCPeerConnection()
    pcs.add(pc)

    # Listen to any changes on the RTC tunnel
    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    # Listen to a track received from a user
    @pc.on("track")
    def on_track(track):
        process = Process(track, ws,params["workout"][0].split(", "))
        try:
            pc.addTrack(process)
        except Exception as err:
            print("Error declaring the processing class:", err)
            pc.addTrack(track)

    # Handle offer
    await pc.setRemoteDescription(offer)

    # Send answer
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )

async def websocket_handler(request):
    global ws
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            if msg.data == "2init":
                await ws.send_str('init')
                print('sent')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())
            
    print('websocket connection open')

    return ws

async def on_shutdown(app):
    # Сlose peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()

app = web.Application()
app.on_shutdown.append(on_shutdown)
app.router.add_post("/offer", offer)
app.router.add_post('/register', register)
app.router.add_post('/login', login)
app.router.add_post('/library', get_user_library)
app.router.add_post('/sessions', get_user_sessions)
app.add_routes([web.get('/ws', websocket_handler)])

# Enable CORS
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        expose_headers="*",
        allow_headers="*",
    )
})

for route in list(app.router.routes()):
    cors.add(route)

web.run_app(
    app, access_log=None,
)

# adev runserver server.py 2>/dev/null