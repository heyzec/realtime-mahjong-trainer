from typing import Dict
from .objects.tile import Tile
from .objects.tile_collection import TileCollection
from .utils.shanten import calculate_shanten
from .utils.ukeire import calculate_ukeire

class Trainer:
    def __init__(self, hand: TileCollection):
        self.hand = hand

    def get_shanten(self):
        return calculate_shanten(self.hand)

    def calculate_discards(self) -> Dict[Tile, int]:
        hand = self.hand
        output: Dict[Tile, int] = {}

        base_shanten = calculate_shanten(hand)
        for tile in hand.unique:
            new_hand = hand.remove_tile(tile)
            new_shanten = calculate_shanten(new_hand)
            if new_shanten > base_shanten:
                continue
            output[tile] = calculate_ukeire(hand.remove_tile(tile))

        return output

    def discard(self, tile: Tile) -> str:
        valid_discards = self.calculate_discards()
        best_ukeire = max(valid_discards.values())
        if tile not in valid_discards:
            message = ("Increases your shanten - you are now further from ready.")
        elif valid_discards[tile] != best_ukeire:
            message = ("Could be better")
        else:
            message = ("That was the best choice!")

        self.hand = self.hand.remove_tile(tile)
        return message

    def draw(self, tile: Tile):
        self.hand = self.hand.add_tile(tile)






