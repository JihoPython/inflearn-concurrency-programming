import aiohttp
import asyncio
import aiofiles
from os import getenv, mkdir


def init():
    from dotenv import load_dotenv

    load_dotenv(verbose=False)


NAVER_API_BASE_URL = "https://openapi.naver.com/v1/search/image"
__HEADERS = {
    "X-Naver-Client-id": getenv("NAVER_API_CLIENT_ID"),
    "X-Naver-Client-Secret": getenv("NAVER_API_CLIENT_SECRET"),
}


async def download_image(session: "aiohttp.ClientSession", image: str):
    name = image.split("/")[-1].split("?")[0]

    try:
        mkdir("./images")
    except FileExistsError:
        pass

    async with session.get(image) as response:
        if response.status == 200:
            async with aiofiles.open(f"./images/{name}", mode="wb") as file:
                await file.write(await response.read())


async def fetch(session: "aiohttp.ClientSession", url, i):
    print(i + 1)
    async with session.get(url, headers=__HEADERS) as response:
        result = await response.json()
        items = result["items"]
        images = [item["link"] for item in items]

        await asyncio.gather(*[download_image(session, image) for image in images])


async def main(keyword: str):
    urls = [
        f"{NAVER_API_BASE_URL}?query={keyword}&display=20&start={1 + i * 10}"
        for i in range(1, 10)
    ]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, url, i) for i, url in enumerate(urls)])


if __name__ == "__main__":
    asyncio.run(main("cat"))
