from fastapi import FastAPI
from redis_om import get_redis_connection
from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel

redis=get_redis_connection(
    host="redis-18270.c301.ap-south-1-1.ec2.cloud.redislabs.com",
    port="18270",
    password="AKPUlqvhLncSS1lKIrqObQYiUMASKpTH",
    decode_responses=True
)






app =FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:9000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
class Product(HashModel):
    name: str
    price : float
    quantity : int


    class Meta:
        database=redis

@app.get("/products")
def allproduct():
    return [format(pk) for pk in Product.all_pks()]


def format(pk :str):
    product=Product.get(pk)
    return {
        "id":product.pk,
        "name":product.name,
        "price":product.price,
        "quantity":product.quantity
    }

@app.get("/product/{pk}")
def getproduct(pk :str):
    return Product.get(pk)


@app.post("/products")
def createproduct(product : Product):
    return product.save()

@app.delete("/product/{pk}")
def deleteproduct(pk:str):
    return Product.delete(pk)

