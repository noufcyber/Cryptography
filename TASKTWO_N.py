
import hashlib, random, string, time

def gener_string():
    str = ''.join(random.choices(string.ascii_letters, k=8))

    return str

def gener_sha60v(txt):
    hash_v = hashlib.sha1(txt.encode()).hexdigest()
    return hash_v[:6]  # 60 

def f_collision():

    hash_values = set()
    while True:
        txt = gener_string()
        txt_h = gener_sha60v(txt)
        if txt_h in hash_values:
            return txt, txt_h
        hash_values.add(txt_h)

start = time.time()
t_return, h_return = f_collision()
t_return_2 = ""
while gener_sha60v(t_return_2) != h_return:
    t_return_2 = gener_string()
end = time.time()
execution_time = end - start

print("There is a Collision !!!")
print("Message ->", t_return)
print("Collision -> ", t_return_2)
print("Hash -> ", h_return)
print(f"executed in {execution_time} seconds ")
