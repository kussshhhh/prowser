import socket
from tkinter import *
from tkinter import ttk
import re
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup

def clean(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    body_content = soup.body.get_text(separator='\n', strip=True)
    return body_content


def show(self):
     self = clean(self) 
     root = Tk()
     text_widget = Text(root, wrap='word')
     text_widget.insert(END, self)
     text_widget.pack(expand=True, fill='both')

     root.mainloop()

def request(site):
    try:
            s = socket.socket(         # socket.gaierror : address related error, jo url hai woh galat hai 
            socket.AF_INET,            #  socket.gethostbyname(hostname) // string return karta hai of IP addreess
            socket.SOCK_STREAM         #  socket.connect(address) : takes a tuple of ("ip address", port) ;
            )
            url = "www." + site +".com"
        
            address = socket.gethostbyname(url)  
            print(address)
            port = 80
        
            s.connect((address, port) )
            s.send(f"GET / HTTP/1.1\r\nHost: {url}\r\n\r\n".encode("utf8"))
            response = s.makefile("r", encoding = "utf8", newline = "\r\n")
            totaldata = ""
            try: 
                 while(True):
                    data = response.readline()
                    totaldata += data
                    if ( data == "0\r\n"or data == "</html>\r\n"): break                 
                    print(data)
            finally:
                  s.close()
            print(type(totaldata))
            return totaldata
            # printbody( response.read())
           
    except socket.gaierror as e:
        print(f"Unable to resolve hostname: {e}")



   

if __name__ == "__main__":
    site = input("site: ")
    
    response_data = request(site)
    show(response_data)    