from repositories.repository import Repository
from models.store import Store, StoreWithUser
from math import radians, degrees, sin, cos, asin


class StoreRepository(Repository):
    def __init__(self):
        super().__init__(Store)

    def find_by_id(self, store_id: int) -> Store:
        return self.find_query().filter_by(store_id=store_id).first()

    def create(self, store: StoreWithUser) -> Store:
        store_data = self.model(**store.dict())
        return super().create(store_data)

    def exists(self, address: str) -> bool:
        return self.find_query().filter_by(address=address).first() is not None

    def find_by_user_id(self, user_id: int) -> list[Store]:
        return self.find_query().filter_by(user_id=user_id).all()

    def find_by_coordinates(
        self,
        lat: float,
        lon: float,
        radius: float = 15,
    ) -> list[Store]:
        bbox = self.__calculate_bounding_box(lat, lon, radius)
        return (
            self.find_query()
            .filter(
                self.model.lat.between(bbox["min_lat"], bbox["max_lat"]),
                self.model.long.between(bbox["min_lon"], bbox["max_lon"]),
            )
            .all()
        )

    def __calculate_bounding_box(self, center_lat, center_lon, radius_km):
        center_lat_rad = radians(center_lat)
        center_lon_rad = radians(center_lon)
        radius_rad = radius_km / 6371.0

        min_lat = degrees(center_lat_rad - radius_rad)
        max_lat = degrees(center_lat_rad + radius_rad)

        delta_lon = asin(sin(radius_rad) / cos(center_lat_rad))
        min_lon = degrees(center_lon_rad - delta_lon)
        max_lon = degrees(center_lon_rad + delta_lon)

        return {
            "min_lat": min_lat,
            "max_lat": max_lat,
            "min_lon": min_lon,
            "max_lon": max_lon,
        }
