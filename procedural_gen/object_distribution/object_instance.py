from pydantic import Field

from easy_config.my_model import MyModel
from easy_raster.model.position import Position


class ObjectInstance(MyModel):
    object_id: int = 0
    position: Position = Field(default_factory=Position)
    radius: float = 1.0
