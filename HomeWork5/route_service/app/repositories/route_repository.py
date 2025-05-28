from typing import List, Optional
from bson import ObjectId

from app.models import Route
from app.db import db

class RouteRepository:
    collection = db.routes

    @staticmethod
    async def create_route(start: str, end: str, waypoints: list[str], distance_length: int) -> Route:
        doc = {"start_point": start, "end_point": end, "waypoints": waypoints, "distance":distance_length}
        result = await RouteRepository.collection.insert_one(doc)
        return Route(route_id=str(result.inserted_id), start_point=start, end_point=end, waypoints=waypoints, distance=distance_length)
         
    @staticmethod
    async def get_route_by_id(route_id: str) -> Optional[Route]:
        doc = await RouteRepository.collection.find_one({"_id": ObjectId(route_id)})
        if not doc:
            return None
        return Route(
            route_id=str(doc["_id"]),
            start_point=doc["start_point"],
            end_point=doc["end_point"],
            waypoints=doc.get("waypoints", []),
            distance=int(doc["distance"])
        )

    @staticmethod
    async def get_all_routes() -> List[Route]:
        routes: List[Route] = []
        async for doc in RouteRepository.collection.find():
            routes.append(
                Route(
                    route_id=str(doc["_id"]),
                    start_point=doc["start_point"],
                    end_point=doc["end_point"],
                    waypoints=doc.get("waypoints", []),
                    distance=int(doc["distance"])
                )
            )
        return routes
    
    @staticmethod
    async def find_routes(
        start_point: Optional[str] = None,
        end_point: Optional[str] = None,
    ) -> List[Route]:
        query: dict = {}
        if start_point:
            query["start_point"] = start_point
        if end_point:
            query["end_point"] = end_point

        routes: List[Route] = []
        async for doc in RouteRepository.collection.find(query):
            routes.append(
                Route(
                    route_id=str(doc["_id"]),
                    start_point=doc["start_point"],
                    end_point=doc["end_point"],
                    waypoints=doc.get("waypoints", []),
                    distance=int(doc["distance"])
                )
            )
        return routes