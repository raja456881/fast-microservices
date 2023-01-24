from main import redis , Order
import time
Key="refund_order"
Group="payment_group"


try:
    redis.xgroup_create(Key, Group)
except:
    print("Groups already exists") 

while True:
    try:
        results=redis.xreadgroup(Group, Key, {Key, ">"}, None)
        if results!=[]:
            for result in results:
                obj=result[1][0][1]
                order=Order.get(obj['pk'])
                order.status="refunded"
                order.save()

    except Exception as e:
        print(str(e))
    time.sleep(1)
