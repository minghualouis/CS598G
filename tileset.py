class TileMap():
    def __init__(self, file_name, prefix):
        self.tiles = {}
        with open(file_name) as tile_list:
            for line in tile_list:
                parts = line.split()
                images = [prefix + "{0}".format(i.strip()) for i in parts[1:]]
                self.tiles[parts[0]] = images
