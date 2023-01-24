from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection
from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel
from starlette.requests import Request
from fastapi.background import BackgroundTasks
import requests, time

app =FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
redis=get_redis_connection(
    host="redis-18270.c301.ap-south-1-1.ec2.cloud.redislabs.com",
    port="18270",
    password="AKPUlqvhLncSS1lKIrqObQYiUMASKpTH",
    decode_responses=True
)


class Order(HashModel):
    product_id : str
    price :float
    fee : float
    total : float
    quantity: int
    status :str

    class Meta:
        database = redis

@app.get("/order/{pk}")
def get_order(pk:str):
    return Order.get(pk)

@app.post("/orders")
async def create (request:Request, background_tasks: BackgroundTasks):
    body=await request.json()
    res=requests.get('http://127.0.0.1:8000/product/%s' %body['id'])
    product=res.json()
    order=Order(
        product_id=product['id'],
        price = product['price'],
        fee = 0.2 * product['price'],
        total = 1.2 *product['price'],
        quantity= body['quantity'],
        status = "pending"
    )
    order.save()
    background_tasks.add_task(order_complete, order)
    return order

def order_complete(order : Order):
    time.sleep(5)
    order.status="completed"
    order.save()
    redis.xadd("order_completed", order.dict(), "*")