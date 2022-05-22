from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from app.config import MONGO_DB_URL, MONGO_DB_DATABASE_NAME, logger


class MongoDB:
    client: "AsyncIOMotorClient"
    engine: "AIOEngine"

    def connect(self) -> None:
        self.client = AsyncIOMotorClient(MONGO_DB_URL)
        self.engine = AIOEngine(
            motor_client=self.client, database=MONGO_DB_DATABASE_NAME
        )
        logger.info(f"MongoDB {MONGO_DB_DATABASE_NAME} connected.")

    def close(self) -> None:
        self.client.close()
        logger.info(f"MongoDB {MONGO_DB_DATABASE_NAME} closed.")


mongodb = MongoDB()
