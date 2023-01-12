from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data_retriever import main
import sqlite3

app = FastAPI(title="bike API")

# CORS configuration
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# gets all the trips' info from the bikes database
for i in range(100):
    @app.get(f"/{i}")
    def get_drones():
        conn = sqlite3.connect(f'trips_{i}.db')
        c = conn.cursor()
        c.execute("SELECT * FROM trips")
        rows = c.fetchall()
        conn.close()
        return rows
