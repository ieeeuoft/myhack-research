import uvicorn
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI

from backend.api.routes import auth
from backend.db.firebase import connect_to_firebase
from backend.services.api.discover import fetch_utoronto_discover
from backend.utils.scheduler import SchedulerManager


scheduler = SchedulerManager()


def setup_server():
    global scheduler
    connect_to_firebase()

    scheduler.start()


app = FastAPI()
setup_server()
app.include_router(auth.router, prefix='/auth')

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8002)
