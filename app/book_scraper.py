import asyncio
from aiohttp import ClientSession

from app.config import NAVER_API_CLIENT_ID, NAVER_API_CLIENT_SECRET


class NaverBookScraper:

    NAVER_API_BASE_URL = "https://openapi.naver.com/v1/search/book"

    @staticmethod
    async def fetch(session: ClientSession, url, headers):
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                return result["items"]

    def unit_url(self, keyword: str, start: int):
        return {
            "url": f"{self.NAVER_API_BASE_URL}?query={keyword}&display=10&start={start}",
            "headers": {
                "X-Naver-Client-id": NAVER_API_CLIENT_ID,
                "X-Naver-Client-Secret": NAVER_API_CLIENT_SECRET,
            },
        }

    async def search(self, keyword: str, total_page: int):
        apis = [self.unit_url(keyword, 1 + i * 10) for i in range(total_page)]
        async with ClientSession() as session:
            all_data = await asyncio.gather(
                *[
                    NaverBookScraper.fetch(session, api["url"], api["headers"])
                    for api in apis
                ]
            )

            result = [item for items in all_data for item in items]

            return result


if __name__ == "__main__":
    print(asyncio.run(NaverBookScraper().search("python", 10)))
