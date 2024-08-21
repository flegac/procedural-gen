from easy_lib.timing import time_func
from image_io.resolution import Resolution
from procedural_gen.object_distribution.object_instance import ObjectInstance
from procedural_gen.object_distribution.occupation_mask import OccupationMask
from procedural_gen.object_distribution.shape import Shape


class ItemMap:
    def __init__(self, resolution: int = 1024):
        self.resolution = Resolution.square(resolution)
        self.mask = OccupationMask.from_resolution(self.resolution)

    @time_func
    def place_items(self, template: ObjectInstance, n: int) -> list[ObjectInstance]:

        shape = Shape.circle(self.resolution.rescale_size(template.radius))
        item_size_mask = self.mask.dilate(shape)

        items = []
        while len(items) < n:
            item = self._place_item(template, buffer=item_size_mask)
            if not item:
                break
            items.append(item)

        return items

    def _place_item(self, template: ObjectInstance, buffer: OccupationMask):
        position = buffer.search_position()
        if position:
            item = template.clone(update={'position': position})
            self.mask.circle(item)
            buffer.circle(item, extra_radius=template.radius)
            return item
