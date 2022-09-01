import arcade

SIRINA_PROZORA = 1024
VISINA_PROZORA = 768
NASLOV_PROZORA = "Arcade Platformer"

# konstante za skaliranje spriteova iz njihove originalne velicine
PODESAVANJE_PLOCICE = 0.5
PODESAVANJE_LIKA = PODESAVANJE_PLOCICE * 2
SPRITE_PIXEL_SIZE = 128
MREZA_PIXEL_SIZE = SPRITE_PIXEL_SIZE * PODESAVANJE_PLOCICE

MAPA = ":resources:tiled_maps/map_with_ladders.json"

# konstante za pucanje
PODESAVANJE_METKA = 0.8
BRZINA_ISPUCANOG = 15
BRZINA_METKA = 12
STETA_METKA = 25

# brzina kretanja igraca u pixels/frame
BRZINA_KRETANJA_IGRACA = 7
GRAVITACIJA = 1.5
BRZINA_SKOKA_IGRACA = 30

SLIKA_IGRACA = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"

# konstante za pracenje je li igrca okrenut lijevo ili desno
DESNO_OKRENUT = 0
LIJEVO_OKRENUT = 1

IGRAC_START_X = 2
IGRAC_START_Y = 1

# imena slojeva iz tilemape
POMICUCE_PLATFORME = "Moving Platforms"
PLATFORME = "Platforms"
NOVCICI = "Coins"
SLOJ_POZADINA = "Background"
LJESTVE = "Ladders"
IGRAC = "Player"
NEPRIJATELJI = "Enemies"
METCI = "Bullets"