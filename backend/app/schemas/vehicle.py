from pydantic import BaseModel
from typing import Optional

class VehicleIn(BaseModel):
    make: str
    model: str
    vin: Optional[str]  # VIN номер автомобиля
    plate_number: Optional[str]  # Номерной знак
    engine: Optional[str]  # Тип двигателя
    fuel_type: Optional[str]  # Тип топлива
    engine_volume: Optional[int]  # Объем двигателя
    year: Optional[int]  # Год выпуска автомобиля

class VehicleOut(VehicleIn):
    id: str
    year: Optional[int]  # Добавлено для вывода года выпуска

    class Config:
        orm_mode = True
