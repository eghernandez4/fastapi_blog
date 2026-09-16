from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

posts: list[dict] = [
  {
    "id": 1,
    "author": "John",
    "title": "FastAPI is awesome",
    "content": "This framework is really easy to use and fast",
    "date_posted": "April 20, 2025"
  },
  {
    "id": 2,
    "author": "Jane",
    "title": "Python is Great for web development",
    "content": "Python is a great language for web development, and FastAPI makes it easy to build APIs",
    "date_posted": "April 21, 2025"
  }
]

@app.get("/", response_class=HTMLResponse)
async def root():
    return f"<h1>{posts[0]['title']}</h1>"


@app.get("/hello/{name}", include_in_schema=False)
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/api/posts")
async def get_posts():
    return posts
