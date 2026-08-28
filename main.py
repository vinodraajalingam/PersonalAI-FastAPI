from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json

#Creating FastAPI App
app = FastAPI()

class Book(BaseModel):
    id:int
    title:str
    language:str
    price:int

with open("book.txt","r") as file:
    books = json.load(file)

@app.get("/")
def greetUser():
    return "Welcome User"

@app.get("/html",response_class=HTMLResponse)
def greetUser():
    return """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>My FastAPI App</title>
                </head>
                <body>
                    <h1>Hello World!</h1>
                    <p>This HTML page is returned by FastAPI.</p>
                </body>
                </html>
           """

@app.get("/file",response_class=FileResponse)
def greetUser():
    return FileResponse("index.html")

@app.get("/books")
def getBooks():
    return books

@app.get("/books/{title}")
def getBook(title:str):
    for book in books:
        if (book['title'] == title):
            return book
    return "Book Coming Soon... Stay Tuned!"

@app.post("/books/addbook")
def addBook(book: Book):
  books.append(book.model_dump())
  with open("book.txt","w") as file:
      json.dump(books,file,indent=4)
  return books

@app.put("/book/{id}")
def updateBook(id:int,title:str,language:str,price:int):
    for book in books:
        if (book["id"] == id):
            books[id-1]['title'] = title
            books[id-1]['language'] = language
            books[id-1]['price'] = price
    with open("book.txt","w") as file:
        json.dump(books,file,indent=2)

@app.delete("/book/{id}")
def deleteBook(id:int):
    for book in books:
        if (id == book['id']):
            books.pop(id-1)
            with open("book.txt","w") as file:
                json.dump(books,file,indent=2)
            return books
    return "Nothing to Delete"
