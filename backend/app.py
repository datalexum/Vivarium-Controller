from fastapi import FastAPI, status, Request
from typing import List
from apscheduler.schedulers.background import BackgroundScheduler
from dimpoint import DimPoint, DimPointORM, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from light import Light

engine = create_engine('sqlite:///database.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

import uvicorn
# import aht
from datetime import datetime, timedelta

from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from pydantic import parse_obj_as

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

sched = BackgroundScheduler()
light = Light('172.28.20.26', 1883, 'tasmota_dragl')


# aht_sensor = aht.Aht()


@app.post('/light/dimpoints/')
async def setDimpoints(dimpoints: List[DimPoint]):
    print("I am here!")
    sched.remove_all_jobs()
    session.query(DimPointORM).delete()
    for dimpoint in dimpoints:
        session.add(dimpoint.toOrm())
        sched.add_job(light.dimWhite, 'cron', hour=dimpoint.hour, minute=dimpoint.minute, args=[dimpoint.percent])
    session.commit()
    return dimpoints


@app.get('/light/dimpoints/')
async def getDimpoints():
    return parse_obj_as(List[DimPoint], session.query(DimPointORM).order_by(DimPointORM.hour, DimPointORM.minute).all())


@app.get('/light/test/')
async def testLight():
    light.setChannel(4, 88)


@app.get("/test")
async def test():
    date_inner = datetime.now() + timedelta(seconds=60)
    sched.add_job(print, 'date', run_date=date_inner, args=['test'])
    print(str(sched.get_jobs()))
    return {'status': 'done'}


@app.get("/jobs")
async def test():
    for job in sched.get_jobs():
        print(str(job.next_run_time) + '   ' + str(job.func) + '    ' + str(job.args))
    return {'jobs': str(sched.get_jobs())}


@app.get("/")
async def hello(request: Request):
    return templates.TemplateResponse('home.html', {"request": request})


@app.get("/sensors")
async def sensor_view(request: Request):
    return templates.TemplateResponse('sensor.html', {"request": request})


@app.get("/home")
async def home_view():
    response = RedirectResponse(url='/')
    return response


@app.get("/calc")
async def calc_view(request: Request):
    return templates.TemplateResponse('rechner.html', {"request": request})


@app.get("/static/<file>")
async def static_files(file, request: Request):
    return templates.TemplateResponse(file, {"request": request})


@app.get("/api/temperature/{number}")
async def temperature(number: int):
    if number > 7 | number < 0:
        return "Sensor number has to be between zero and seven", status.HTTP_400_BAD_REQUEST
    # return str(aht_sensor.getTemperature(number))
    return -1


@app.get("/api/humidity/{number}")
async def humidity(number: int):
    if number > 7 | number < 0:
        return "Sensor number has to be between zero and seven", status.HTTP_400_BAD_REQUEST
    # return str(aht_sensor.getHumidity(number))
    return -1


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    sched.start()

    dimpoints = parse_obj_as(
        List[DimPoint], session.query(DimPointORM).order_by(DimPointORM.hour, DimPointORM.minute).all())

    sched.remove_all_jobs()
    for dimpoint in dimpoints:
        sched.add_job(light.dimWhite, 'cron', hour=dimpoint.hour, minute=dimpoint.minute, args=[dimpoint.percent])

    # aht_sensor.daemon.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
