from multiprocessing import Queue, Process
import asyncio
import time

q = Queue()

def get_data(q):
    while True:
        data = q.get()
        print(data)
        if str(data) == "stop":
            break

    
def put_data(q):
    time.sleep(2)
    datas = ["Work1","Work2","Work3","Work4","stop","Work6"]
    for data in datas:
        q.put(data)
    return None
    
first = Process(target=get_data, args=(q,))
second = Process(target=put_data, args=(q,))

first.start()
second.start()
first.join()
second.join()
print("complete")


# def wait(q):
#     time.sleep(5)
    

# def put(q):
    

# q = Queue()
# asyncio.gather(
#     put(q)
#     , wait(q)
# )

