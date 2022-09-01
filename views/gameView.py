'''Igra'''
import arcade
import math

from konstante import *
from entities.player import Player
from entities.robot import Robot
from entities.zombie import Zombie
from views.view import View

class GameView(View):
    def __init__(self):
        '''inicijalizacija igre i logika'''
        super().__init__()
        
        #prati koja je tipka trenutno pritisnuta
        self.lijevo_pritisnuto = False
        self.desno_pritisnuto = False
        self.gore_pritisnuto = False
        self.dolje_pritisnuto = False
        self.pucanje_pritisnuto = False
        self.reset_skoka = False
        
        #tile mapa
        self.mapa = None
        
        #scena
        self.scena = None
        
        #varijabla za igraca
        self.igrac_sprite = None
        
        #physics engine
        self.fizika = None
        
        #kamera za pomicanje backgrounda i kamera za gui elemente
        self.kamera = None
        self.gui_kamera = None
        
        self.kraj_mape = 0
        
        #za pracenje rezultata
        self.rezultat = 0
        
        #za pucanje
        self.moze_pucati = False
        self.pucanj_timer = 0
        
        #ucitaj zvukove
        self.novcic_zvuk = arcade.load_sound(":resources:sounds/coin1.wav")
        self.skok_zvuk = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.pucanj_zvuk = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.upucan_zvuk = arcade.load_sound(":resources:sounds/hit5.wav")
        
    def setup(self):
        '''setup igre i zvanje za restart'''
        super().setup()
        
        #postavljanje zastavica na false
        self.lijevo_pritisnuto = False
        self.desno_pritisnuto = False
        self.gore_pritisnuto = False
        self.dolje_pritisnuto = False
        self.pucanje_pritisnuto = False
        self.reset_skoka = False
        
        #postavljanje kamera
        self.kamera = arcade.Camera(self.window.width, self.window.height)
        self.gui_kamera = arcade.Camera(self.window.width, self.window.height)
        
        slojevi = {
            NOVCICI: {
                "use_spatial_hash": True
            },
            LJESTVE: {
                "use_spatial_hash": True
            },
            POMICUCE_PLATFORME: {
                "use_spatial_hash": True
            },
            PLATFORME: {
                "use_spatial_hash": True
            }
        }
        
        #ucitaj mapu (putanja u konstantama)
        self.mapa = arcade.load_tilemap(MAPA, PODESAVANJE_PLOCICE, slojevi)
        
        #inicijaliziraj scenu sa mapom sto ce automatski dodati slojeve
        #iz mape kao SpriteLists u secnu u pravom redoslijedu
        self.scena = arcade.Scene.from_tilemap(self.mapa)
        
        #rezultat
        self.rezultat = 0
        
        #za pucanje
        self.moze_pucati = True
        self.pucanj_timer = 0
        
        #postavi igraca
        self.igrac_sprite = Player(SLIKA_IGRACA)
        self.igrac_sprite.center_x = (
            self.mapa.tile_width * PODESAVANJE_PLOCICE * IGRAC_START_X
        )
        self.igrac_sprite.center_y = (
            self.mapa.tile_height * PODESAVANJE_PLOCICE * IGRAC_START_Y
        )
        self.scena.add_sprite(IGRAC, self.igrac_sprite)
        
        #izracunaj kraj mape u pikselima
        self.kraj_mape = self.mapa.width * MREZA_PIXEL_SIZE
        
        #postavi neprijatelje
        sloj_neprijatelja = self.mapa.object_lists[NEPRIJATELJI]
        
        for neprijateljObjekt in sloj_neprijatelja:
            koordinate = self.mapa.get_cartesian(
                neprijateljObjekt.shape[0], neprijateljObjekt.shape[1]
            )
            neprijateljTip = neprijateljObjekt.properties["type"]
            if neprijateljTip == "robot":
                neprijatelj = Robot()
            elif neprijateljTip == "zombie":
                neprijatelj = Zombie()
            neprijatelj.center_x = math.floor(
                koordinate[0] * PODESAVANJE_PLOCICE * self.mapa.tile_width
            )
            neprijatelj.center_y = math.floor(
                (koordinate[1] + 1) * (self.mapa.tile_height * PODESAVANJE_PLOCICE)
            )
            if "boundary_left" in neprijateljObjekt.properties:
                neprijatelj.boundary_left = neprijateljObjekt.properties["boundary_left"]
            if "boundary_right" in neprijateljObjekt.properties:
                neprijatelj.boundary_right = neprijateljObjekt.properties["boundary_right"]
            if "change_x" in neprijateljObjekt.properties:
                neprijatelj.change_x = neprijateljObjekt.properties["change_x"]
            self.scena.add_sprite(NEPRIJATELJI, neprijatelj)
        
        #dodaj bullet spritelist na scenu
        self.scena.add_sprite_list(METCI)
        
        #postavi pozadinsku boju
        if self.mapa.tiled_map.background_color:
            arcade.set_background_color(self.mapa.tiled_map.background_color)
            
        #kreiraj 'physics engine'
        self.fizika = arcade.PhysicsEnginePlatformer(
            self.igrac_sprite,
            platforms=self.scena[POMICUCE_PLATFORME],
            walls=self.scena[PLATFORME],
            gravity_constant=GRAVITACIJA,
            ladders=self.scena[LJESTVE],
        )
    
    def on_show_view(self):
        arcade.set_background_color(self.mapa.background_color)
        
    def on_draw(self):
        #ucitaj
        arcade.start_render()
        
        #aktiviraj kamere
        self.kamera.use()
        
        #scena
        self.scena.draw()
        
        #aktiviraj gui kameru prije postavljanja gui elementa
        self.gui_kamera.use()
        
        #rezultat
        rezultat_text = f"Score: {self.rezultat}"
        arcade.draw_text(
            rezultat_text,
            10,
            10,
            arcade.csscolor.BLACK,
            18,
        )
    
    def process_keychange(self):
        '''poziva se kada mijenjamo tipku gore/dolje, kada smo i nismo na ljestvama, kada skacemo, kada se micemo livo desno '''
        #proces gore/dolje pri skakanju ili na ljestvama
        if self.gore_pritisnuto and not self.dolje_pritisnuto:
            if self.fizika.is_on_ladder():
                self.igrac_sprite.change_y = BRZINA_KRETANJA_IGRACA
            elif (self.fizika.can_jump(y_distance=10) and not self.reset_skoka):
                self.igrac_sprite.change_y = BRZINA_SKOKA_IGRACA
                self.reset_skoka = True
                arcade.play_sound(self.skok_zvuk)
        elif self.dolje_pritisnuto and not self.gore_pritisnuto:
            if self.fizika.is_on_ladder():
                self.igrac_sprite.change_y = -BRZINA_KRETANJA_IGRACA
                
        #proces gore/dolje na ljestvama bez pomicanja
        if self.fizika.is_on_ladder():
            if not self.gore_pritisnuto and not self.dolje_pritisnuto:
                self.igrac_sprite.change_y = 0
            elif self.gore_pritisnuto and self.dolje_pritisnuto:
                self.igrac_sprite.change_y = 0
                
        #proces livo desno
        if self.desno_pritisnuto and not self.lijevo_pritisnuto:
            self.igrac_sprite.change_x = BRZINA_KRETANJA_IGRACA
        elif self.lijevo_pritisnuto and not self.desno_pritisnuto:
            self.igrac_sprite.change_x = -BRZINA_KRETANJA_IGRACA
        else:
            self.igrac_sprite.change_x = 0
        
    def on_key_press(self, key, modifiers):
        '''poziva se kad god je pritisnuta tipka'''
        if key == arcade.key.UP or key == arcade.key.W:
            self.gore_pritisnuto = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.dolje_pritisnuto = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.lijevo_pritisnuto = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.desno_pritisnuto = True
            
        if key == arcade.key.SPACE:
            self.pucanje_pritisnuto = True
            
        self.process_keychange()
        
    def on_key_release(self, key, modifiers):
        '''poziva kad se pusti tipka'''
        if key == arcade.key.UP or key == arcade.key.W:
            self.gore_pritisnuto = False
            self.reset_skoka = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.dolje_pritisnuto = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.lijevo_pritisnuto = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.desno_pritisnuto = False

        if key == arcade.key.SPACE:
            self.pucanje_pritisnuto = False

        self.process_keychange()
        
    def kamera_player(self, speed=0.2):
        prozor_centar_x = self.igrac_sprite.center_x - (self.kamera.viewport_width / 2)
        prozor_centar_y = self.igrac_sprite.center_y - (self.kamera.viewport_height / 2)
        
        if prozor_centar_x < 0:
            prozor_centar_x = 0
        if prozor_centar_y < 0:
            prozor_centar_y = 0
        
        igrac_centar = prozor_centar_x, prozor_centar_y
        
        self.kamera.move_to(igrac_centar, speed)
        
    def on_update(self, delta_time):
        '''micanje i logika'''
        #pomici igraca uz pomoc physic engina
        self.fizika.update()
        
        #updateaj animacije playera
        #skakanje
        if self.fizika.can_jump():
            self.igrac_sprite.can_jump = False
        else:
            self.igrac_sprite.can_jump = True
            
        #penjanje na skale
        if self.fizika.is_on_ladder() and not self.fizika.can_jump():
            self.igrac_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.igrac_sprite.is_on_ladder = False
            self.process_keychange()
            
        if self.moze_pucati:
            if self.pucanje_pritisnuto:
                arcade.play_sound(self.pucanj_zvuk)
                metak = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", PODESAVANJE_METKA)
                
                if self.igrac_sprite.facing_direction == DESNO_OKRENUT:
                    metak.change_x = BRZINA_METKA
                else:
                    metak.change_x = -BRZINA_METKA
                    
                metak.center_x = self.igrac_sprite.center_x
                metak.center_y = self.igrac_sprite.center_y
                
                self.scena.add_sprite(METCI, metak)
                
                self.moze_pucati = False
            
        else:
            self.pucanj_timer += 1
            if self.pucanj_timer == BRZINA_ISPUCANOG:
                self.moze_pucati = True
                self.pucanj_timer = 0
                
        #updateaj animacije ostalih slojeva
        self.scena.update_animation(
            delta_time,
            [
                NOVCICI,
                SLOJ_POZADINA,
                IGRAC,
                NEPRIJATELJI
            ]
        )
        
        #updataj platforme, neprijatelje i metke
        self.scena.update(
            [PLATFORME, NEPRIJATELJI, METCI]
        )
        
        #vidi triba li neprijatelj prominit stranu kad dode do granice
        for neprijatelj in self.scena.get_sprite_list(NEPRIJATELJI):
            if(
                neprijatelj.boundary_right
                and neprijatelj.right > neprijatelj.boundary_right
                and neprijatelj.change_x > 0
            ):
                neprijatelj.change_x *= -1
                
            if (
                neprijatelj.boundary_left
                and neprijatelj.left < neprijatelj.boundary_left
                and neprijatelj.change_x < 0
            ):
                neprijatelj.change_x *= -1
                
        # vidi triba li pomicucu platformu usmjerit u drugu stranu
        for platforma in self.scena.get_sprite_list(POMICUCE_PLATFORME):
            if (
                platforma.boundary_top 
                and platforma.top > platforma.boundary_top 
                and platforma.change_y > 0):
                platforma.change_y *= -1
            if (
                platforma.boundary_bottom
                and platforma.bottom < platforma.boundary_bottom
                and platforma.change_y < 0
            ):
                platforma.change_y *= -1
                
        for metak in self.scena.get_sprite_list(METCI):
            hit_lista = arcade.check_for_collision_with_lists(
                metak,
                [
                    self.scena.get_sprite_list(NEPRIJATELJI),
                    self.scena.get_sprite_list(PLATFORME),
                    self.scena.get_sprite_list(POMICUCE_PLATFORME),
                ],
            )
            
            if hit_lista:
                metak.remove_from_sprite_lists()

                for kolizija in hit_lista:
                    if (
                        self.scena.get_sprite_list(NEPRIJATELJI)
                        in kolizija.sprite_lists
                    ):
                        # The collision was with an enemy
                        kolizija.health -= STETA_METKA

                        if kolizija.health <= 0:
                            kolizija.remove_from_sprite_lists()
                            self.rezultat += 100

                        # Hit sound
                        arcade.play_sound(self.upucan_zvuk)
                return
            
            if (metak.right < 0) or (metak.left > (self.mapa.width * self.mapa.tile_width) * PODESAVANJE_PLOCICE):
                metak.remove_from_sprite_lists()
        
        igrac_kolizijska_lista = arcade.check_for_collision_with_lists(
            self.igrac_sprite,
            [
                self.scena.get_sprite_list(NOVCICI),
                self.scena.get_sprite_list(NEPRIJATELJI),
            ]
        )
        
        #petlja za svaki novcic koji dotaknemo i makni ga
        for kolizija in igrac_kolizijska_lista:
            if (self.scena.get_sprite_list(NEPRIJATELJI) in kolizija.sprite_lists):
                arcade.play_sound(self.game_over)
                self.window.show_view(self.window.views["game_over"])
                return
            else:
                if "Points" not in kolizija.properties:
                    print("Upozorenje, skupio novcic bez Points svojstva!")
                else:
                    points = int(kolizija.properties["Points"])
                    self.rezultat += points
                kolizija.remove_from_sprite_lists()
                arcade.play_sound(self.novcic_zvuk)
        
        if self.rezultat == 385:
            self.window.show_view(self.window.views["winner"])
            
        if self.igrac_sprite.bottom < 0:
            arcade.play_sound(self.game_over)
            self.window.show_view(self.window.views["game_over"])
            return
        
        self.kamera_player()