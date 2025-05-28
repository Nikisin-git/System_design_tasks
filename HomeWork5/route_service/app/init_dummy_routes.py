import asyncio
import os

from faker import Faker
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGODB_URL", "mongodb://mongo_db:27017")
DB_NAME = os.getenv("MONGODB_DB", "route_db")

NUM_ROUTES = 20

fake = Faker()


async def init_dummy_routes():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    col = db.routes

    count = await col.count_documents({})
    if count > 10:
        print(f"📦 Найдено {count} маршрутов — инициализация не требуется.")
        client.close()
        return

    print(f"🚀 Генерация {NUM_ROUTES} тестовых маршрутов...")
    docs = []
    for i in range(NUM_ROUTES):
        start = fake.city()
        end = fake.city()
        # 0–3 промежуточных точек
        waypoints = [fake.city() for _ in range(fake.random_int(min=0, max=3))]
        distance = fake.random_int(min=10, max=750)
        docs.append({
            "start_point": start,
            "end_point": end,
            "waypoints": waypoints,
            "distance": distance
        })

    result = await col.insert_many(docs)
    print(f"✅ Вставлено маршрутов: {len(result.inserted_ids)}")
    client.close()


if __name__ == "__main__":
    asyncio.run(init_dummy_routes())