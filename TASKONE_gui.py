import tkinter
import tkinter.messagebox
import customtkinter
from customtkinter import END
import hashlib
import random
import time
import sys

print("RSA ENCRYPTION/DECRYPTION APPLIACATION")
print("***************")


class RSA(customtkinter.CTk):
    def __init__(self):
        self.selection = None
        self.message = None
        self.pub_key = None
        self.priv_key = None
        super().__init__()
#window
        self.title('RSA Program')
        self.geometry(f'{800}x{500}')

#grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

#sideBar
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, height=100, corner_radius=0 , bg_color="#95B9C7")
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.label = customtkinter.CTkLabel(self.sidebar_frame,
                                            text="Hello!!\nThis is a RSA program \nencryption/decryption using Python",
                                            font=customtkinter.CTkFont(size=15))
        self.label.grid(row=0, column=0, padx=20, pady=10)

#text box
        self.textbox = customtkinter.CTkTextbox(self, width = 500, fg_color = "#BCC6CC" , text_color = "#00008B")
        self.textbox.grid(row = 0, column = 1, rowspan = 4, sticky = "nsew", padx = (20, 0), pady = (20, 0))

#input dialog
        self.selection_button = customtkinter.CTkButton(self.sidebar_frame, text="Start", command=self.main , fg_color = "#95B9C7", text_color="#5A5A5A")
        self.selection_button.grid(row=1, column=0, padx=20, pady=(10, 10))

    # Input: generate Two Prime Numbers
    def euclidean(self, a, b):  # return the GCD using Eucliden algorithm
        if a == 0:
            return b
        return self.euclidean(b % a, a)

    # Check using Miller Rabin algorithm
    def prime_check(self, a):
        if (a == 2):
            return True
        elif ((a < 2) or ((a % 2) == 0)):
            return False
        elif (a > 2):
            for i in range(2, a):
                if not (a % i):
                    return False
        return True

    def generate_keys(self):
        p_isprime = False
        q_isprime = False
        while (p_isprime and q_isprime) != True:
            p = random.getrandbits(10)
            q = random.getrandbits(10)

            # print(f'Generated key {p} and {q} randomly\n')
            p_isprime = self.prime_check(p)
            q_isprime = self.prime_check(q)
        return p, q

    # find e using eucliden algorithm
    def egcd(self, e, r):
        while (r != 0):
            e, r = r, e % r
        return e

    # Extended Euclidean Algorithm:
    def eea(self, a, b):
        if a == 0:
            return b, 0, 1
        gcd, x, y = self.eea(b % a, a)
        x1 = y - (b // a) * x
        y1 = x
        return gcd, x1, y1

    # Multiplicative Inverse
    def mult_inv(self, e, r):
        gcd, s, _ = self.eea(e, r)
        if (gcd != 1):
            return None
        else:
            d = int((int(s) + r) % r)
            return d

    def encrypt(self):
        e, n = self.pub_key
        x = []
        m = 0
        for i in self.message:
            if (i.isupper()):
                m = ord(i) - 65
                c = (m ** e) % n
                x.append(c)
            elif (i.islower()):
                m = ord(i) - 97
                c = (m ** e) % n
                x.append(c)
            elif (i.isspace()):
                spc = 400
                x.append(400)

        message_sig = hashlib.sha256((self.message).encode()).hexdigest()
        return x, message_sig

    def decrypt(self):
        d, n = self.priv_key

        txt = self.message.split(',')
        x = ''
        m = 0
        for i in txt:
            if (i == '400'):
                x += ' '
            else:
                m = (int(i) ** d) % n
                m += 65
                c = chr(m)
                x += c
        return x

    def capitalize_all(self):
        return ''.join(c.upper() for c in self.message)


    def main(self):
        choose = 3
        while (choose != 0):
            selection = customtkinter.CTkInputDialog(text="Type '1' for encryption and '2' for decrytion.. 0 for exit",
                                                     title="RSA Selection", fg_color="#6D7B8D", button_fg_color="#3C565B")
            self.selection = selection.get_input()
            if int(self.selection) == 1:
                p, q = self.generate_keys()
                self.textbox.insert(END, "THE 'p' AND 'q' VALUES : \n")
                self.textbox.insert(END, f" 'p' VALUE : {p} \n")
                self.textbox.insert(END, f" 'q' VALUE : {q} \n ")
                n = (p * q)
                self.textbox.insert(END, f" 'N' VALUE : {n} \n ")
                r = (p - 1) * (q - 1)
                for i in range(1, 1000):
                    if (self.egcd(i, r) == 1):
                        e = i
                self.textbox.insert(END, f" 'e' VALUE : {e} \n ")
                d = self.mult_inv(e, r)
                self.textbox.insert(END, f" 'd' VALUE : {d} \n")
                self.pub_key = (e, n)
                self.priv_key = (d, n)


                m = customtkinter.CTkInputDialog(text='What is the message?', title='Message Input', fg_color="#6D7B8D", button_fg_color="#3C565B")
                self.message = (m.get_input()).strip()
                self.message = self.capitalize_all()
                enc_msg, sig_msg = self.encrypt()
                self.textbox.insert(END, f"The Encrypted text is \n{enc_msg}\n Signature is  {sig_msg}\n")

            elif int(self.selection) == 2:
                dec_m = customtkinter.CTkInputDialog(text = 'what is the encrypted message you would like to decrypt?', title = 'Encrypted text input',
                                                     fg_color="#6D7B8D", button_fg_color="#3C565B")
                self.message = (dec_m.get_input()).strip()
                s = customtkinter.CTkInputDialog(text='what is the signature?', title='Message signature', fg_color="#6D7B8D", button_fg_color="#3C565B")
                sig_m = (s.get_input()).strip()
                dec_message = self.decrypt()
                dec_message = dec_message.strip()
                dec_hash = hashlib.sha256(dec_message.encode()).hexdigest()

                self.textbox.insert(END, f'Your decrypted text is \n {dec_message}\n The hash is : {sig_m == dec_hash}\n')
            else:
                self.textbox.insert(END, f' \n program will terminate in 5 seconds')
                self.textbox.insert(END, '\n Thank you for using the RSA Encryptor')
                time.sleep(15)
                sys.exit(0)

if __name__ == '__main__':
    r = RSA()
    r.main()

