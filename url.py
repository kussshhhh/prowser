import socket
import ssl 
from tkinter import *
from tkinter import ttk
import re
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup

WIDTH, HEIGHT = 800, 600
HSTEP , VSTEP = 13 , 18

SCROLL_STEP = 100


class URL: 
    def __init__(self, url):
        self.scheme, url = url.split("://", 1) 
        assert self.scheme in ["http" , "https"]
        if self.scheme == "http":
             self.port = 80
        elif self.scheme == "https":
             self.port = 443


        if "/" not in url: 
            url = url + "/"
        self.host, url = url.split("/", 1)
        self.path = "/" + url 


    def request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host) # added support for https

        s.connect((self.host, self.port))

        s.send(("GET {} HTTP/1.0\r\n".format(self.path) + \
                "Host: {}\r\n\r\n".format(self.host)) \
                .encode("utf8"))
        response = s.makefile("r", encoding = "utf8", newline = "\r\n")

        statusline = response.readline()
        # version, status, explanation = statusline.split("", 2)

        response_headers = {}
        while True: 
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1) 
            response_headers[header.casefold()] = value.strip()
            
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        body = response.read()
        s.close()
        return body 
    
    
    def show(body):
            in_tag = False 
            for c in body: 
                if c == "<":
                    in_tag = True 
                elif c == ">":
                    in_tag = False 
                elif not in_tag:
                    print(c, end= "")

    def lex(body):
        text = ""
        
        in_tag = False 
        for c in body: 
            if c == "<":
                in_tag = True 
            elif c == ">":
                in_tag = False 
            elif not in_tag:
                text += c
        return text


class Browser:
    def __init__(self):
        self.window = Tk()
        self.canvas = Canvas(
             self.window,
             width = WIDTH,
             height=HEIGHT
        )
        self.canvas.pack()
        self.scroll = 0   
        self.window.bind("<Down>", self.scrolldown)  


    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        self.draw()
    def load(self, url):
        body = url.request()
        URL.show(body)
        text = URL.lex(body)
        display_list = Browser.layout(text) 
        Browser.draw(self, display_list)

    def layout(text):
        display_list = []
        cursor_x, cursor_y = HSTEP, VSTEP

        for c in text:
            display_list.append((cursor_x,  cursor_y, c)) 
            cursor_x += HSTEP

            if cursor_x >= WIDTH - HSTEP:
                cursor_y += VSTEP
                cursor_x = HSTEP


        return display_list
    

    def draw(self, display_list):
        cursor_x, cursor_y = HSTEP, VSTEP
        self.canvas.delete("all")
        for x, y, c in display_list:
            self.canvas.create_text(x, y - self.scroll, text=c)
            


if __name__ == "__main__":
    import sys
    Browser().load(URL(sys.argv[1]))
    mainloop()
    


