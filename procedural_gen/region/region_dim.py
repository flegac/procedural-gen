from dataclasses import dataclass

from procedural_gen.region.region import Region


@dataclass
class RegionDim:
    size_x: float
    size_y: float
    size_z: float = 1.

    @staticmethod
    def square(horizontal: float, vertical: float = 1.):
        return RegionDim(size_x=horizontal, size_y=horizontal, size_z=vertical)

    def from_region(self, region: Region):
        return RegionDim(
            size_x=self.size_x / region.x.size,
            size_y=self.size_y / region.y.size,
            size_z=self.size_z
        )

    @property
    def horizontal(self):
        return (self.size_x + self.size_y) * .5
