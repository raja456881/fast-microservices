from main import redis , Product
import time
Key="order_completed"
Group="inventory_group"


try:
    redis.xgroup_create(Key, Group)
except:
    print("Groups already exists") 

while True:
    try:
        results=redis.xreadgroup(Group, Key, {Key, ">"}, None)
        for result in results:
                obj = result[1][0][1]
                try:
                    product = Product.get(obj['product_id'])
                    product.quantity = product.quantity - int(obj['quantity'])
                    product.save()
                except:
                    redis.xadd('refund_order', obj, '*')

    except Exception as e:
        print(str(e))
    time.sleep(1)
