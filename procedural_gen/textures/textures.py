from procedural_gen.textures.color_ramp import ColorRamp, rgb, ColorTreshold, Color, rgb_float


class Textures:
    @staticmethod
    def rgb():
        return ColorRamp(
            name='rgb',
            colors=[
                rgb(0, 255, 0, 0),
                rgb(0, 0, 0, .5),
                rgb(0, 0, 255, 1),
            ],

        )

    @staticmethod
    def colorize(color: Color):
        return ColorRamp(
            name='colorize',
            colors=[
                rgb(0, 0, 0, 0),
                ColorTreshold(color=color, treshold=1)
            ]
        )

    @staticmethod
    def gray():
        return ColorRamp(name='gray')

    @staticmethod
    def natural():
        water = .4
        coastline = .05
        grass = water + 2 * coastline

        mountains = .9

        # https://www.google.com/search?channel=fs&client=ubuntu&q=color+picker
        return ColorRamp(
            name='natural',
            colors=[
                # water
                rgb(10, 36, 200, 0),
                rgb(33, 56, 237, water),

                # coastline
                rgb(247, 225, 82, water + coastline),

                # grassland
                rgb(10, 138, 1, grass),
                rgb(15, 200, 1, (grass + mountains) * .5),
                rgb(15, 74, 1, mountains - .05),

                # mountain
                rgb(92, 32, 2, mountains),

                rgb(255, 255, 255, 1),

            ]
        )

    @staticmethod
    def hill_shaded():
        return ColorRamp(
            name='hill_shaded',
            colors=[
                # water
                rgb_float(0.15, 0.3, 0.15, 0),
                rgb_float(0.3, 0.45, 0.3, .25),
                rgb_float(0.5, 0.5, 0.35, .5),
                rgb_float(0.4, 0.36, 0.33, .8),
                rgb_float(1.0, 1.0, 1.0, 1),
            ]
        )

    @staticmethod
    def mountains():
        water = .1
        coastline = .05
        grass = water + 2 * coastline

        mountains = .5

        # https://www.google.com/search?channel=fs&client=ubuntu&q=color+picker
        return ColorRamp(
            name='mountains',
            colors=[
                # water
                rgb(10, 36, 200, 0),
                rgb(33, 56, 237, water),

                # coastline
                rgb(247, 225, 82, water + coastline),

                # grassland
                rgb(10, 138, 1, grass),
                rgb(15, 200, 1, (grass + mountains) * .5),
                rgb(15, 74, 1, mountains - .05),

                # mountain
                rgb(92, 32, 2, mountains),

                rgb(255, 255, 255, 1),

            ]
        )

    @staticmethod
    def mars():
        # https://www.color-hex.com/color-palette/7175
        return ColorRamp(
            name='mars',
            colors=[
                rgb(240, 231, 231),
                rgb(69, 24, 4),
                rgb(193, 68, 14),
                rgb(231, 125, 17),
                rgb(253, 166, 0),
            ]
        )

    @staticmethod
    def grass():
        return ColorRamp(
            name='grass',
            colors=[
                # grassland
                rgb(10, 70, 1, 0),
                rgb(15, 110, 1, .33),
                rgb(33, 90, 1, .5),

                rgb(45, 120, 1, .75),

                rgb(75, 130, 1, 1.),
            ]
        )

    @staticmethod
    def earth():
        water = .4
        coastline = .05
        grass = water + 2 * coastline

        mountains = .9

        # https://www.google.com/search?channel=fs&client=ubuntu&q=color+picker
        return ColorRamp(
            name='earth',
            colors=[
                # water
                rgb(10, 36, 200, 0),
                rgb(33, 56, 237, water),

                # coastline
                rgb(247, 225, 82, water + coastline),

                # grassland
                rgb(10, 138, 1, grass),
                rgb(15, 200, 1, (grass + mountains) * .5),
                rgb(15, 74, 1, mountains - .05),

                # mountain
                rgb(92, 32, 2, mountains),

                rgb(255, 255, 255, 1),

            ]
        )

    @staticmethod
    def debug():
        # https://www.google.com/search?channel=fs&client=ubuntu&q=color+picker
        return ColorRamp(
            name='earth',
            colors=[
                rgb(0, 0, 255, 0),
                rgb(0, 0, 0, .5),
                rgb(0, 255, 0, 1),
            ]
        )
