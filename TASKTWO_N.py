
import hashlib, random, string

def gener_string():
    str = ''.join(random.choices(string.ascii_letters, k=6))

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

t_return, h_return = f_collision()
t_return_2 = ""
while gener_sha60v(t_return_2) != h_return:
    t_return_2 = gener_string()

print("There is a Collision !!!")
print("Message ->", t_return)
print("Collision -> ", t_return_2)
print("Hash -> ", h_return)
