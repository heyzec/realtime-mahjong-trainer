from .objects.tile import Tile
from .objects.tile_collection import TileCollection
from .utils.shanten import calculate_shanten
from .utils.ukeire import calculate_ukeire

class Trainer:
    def __init__(self, hand: TileCollection):
        self.hand = hand

    def calculate_discards(self):
        hand = self.hand
        output = {}

        base_shanten = calculate_shanten(hand)
        for tile in hand.unique:
            new_hand = hand.remove_tile(tile)
            new_shanten = calculate_shanten(new_hand)
            if new_shanten > base_shanten:
                continue
            output[tile] = calculate_ukeire(hand.remove_tile(tile))

        return output

    def discard(self, tile: Tile):
        valid_discards = self.calculate_discards()
        best_ukeire = max(valid_discards.values())
        if tile not in valid_discards:
            message = ("Increases your shanten - you are now further from ready.")
            return message
        if valid_discards[tile] != best_ukeire:
            message = ("Could be better")
            return message
        message = ("That was the best choice!")
        return message




