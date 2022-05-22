from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.book_scraper import NaverBookScraper
from app.models.book import BookModel
from app.models import mongodb


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI()
templates = Jinja2Templates(directory=f"{BASE_DIR}/templates")

# 강의에서는 사용하지 않음
# from fastapi.staticfiles import StaticFiles
# app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "콜렉터스 북북이"}
    )


@app.get("/test")
async def test():
    from app.models.book import BookModel

    book = BookModel(
        keyword="python", publisher="inflearn", price=55000, image="inflearn.png"
    )
    await mongodb.engine.save(book)

    return book


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    keyword = q

    if not keyword:
        templates.TemplateResponse(
            "index.html",
            {"request": request, "title": "콜렉터스 :: 결과 없음"},
        )

    if await mongodb.engine.find_one(BookModel, BookModel.keyword == keyword):
        books = await mongodb.engine.find(BookModel, BookModel.keyword == keyword)
        print(books)
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": f"콜렉터스 :: {keyword} 검색 결과",
                "books": books,
            },
        )

    scraper = NaverBookScraper()
    books = await scraper.search(keyword, 10)

    models = []
    for book in books:
        model = BookModel(
            keyword=keyword,
            publisher=book["publisher"],
            price=int(float(book["price"])),
            image=book["image"],
        )
        models.append(model)

    await mongodb.engine.save_all(models)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": f"콜렉터스 :: {keyword} 검색 결과",
            "books": books,
        },
    )


@app.on_event("startup")
def on_app_start():
    mongodb.connect()


@app.on_event("shutdown")
def on_app_shutdown():
    mongodb.close()
