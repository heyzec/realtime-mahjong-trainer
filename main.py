from objects.tile import Tile
from objects.tile_collection import TileCollection
from trainer import Trainer

hand = TileCollection.from_tenhou_string("3568889m238p3678s")
trainer = Trainer(hand)

trainer.discard(Tile('2p'))









