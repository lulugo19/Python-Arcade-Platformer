"""
Platformer Template

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.template_platformer
"""
import arcade
from arcade.types import Color

from spieler import Spieler

# --- Konstanten
FENSTER_TITEL = "Platformer"
FENSTER_WEITE = 1280
FENSTER_HÖHE = 720

# Constants used to scale our sprites from their original size
SPIELER_SKALIERUNG = 1
TILE_SKALIERUNG = 1
MÜNZEN_SKALIERUNG = 1
SPRITE_PIXEL_GRÖßE = 64
GRID_PIXEL_SIZE = SPRITE_PIXEL_GRÖßE * TILE_SKALIERUNG

# Movement speed of player, in pixels per frame
SPIELER_GESCHWINDIGKEIT = 10
SCHWERKRAFT = 1
SPIELER_SPRUNGKRAFT = 20
SPIELER_KLETTER_GESCHWINDIGKEIT = 5

# Camera constants
KAMERA_GESCHWINDIGKEIT = 0.3  # get within 1% of the target position within 2 seconds


class Spiel(arcade.View):
    """
    Haupt Spiele-Klasse
    """

    def __init__(self):
        super().__init__()

        # A Camera that can be used for scrolling the screen
        self.kamera = arcade.Camera2D()

        # A rectangle that is used to constrain the camera's position.
        # we update it when we load the tilemap
        self.kamera_grenzen = self.window.rect

        # A non-scrolling camera that can be used to draw GUI elements
        self.kamera_gui = arcade.Camera2D()

        # The level which helps draw multiple spritelists in order.
        self.level = self.create_level()

        # Set up the player, specifically placing it at these coordinates.
        self.spieler = Spieler()

        # Setze die Hintergrundfarbe
        self.background_color = arcade.color.AERO_BLUE

        # Lade den Hintergrund
        self.hintergrund = arcade.load_texture("assets/hintergründe/bäume.png")

        self.hintergrund_rect = arcade.rect.LBWH(0, 0, FENSTER_WEITE, FENSTER_HÖHE)

        # Unsere Physik Engine
        self.physik = arcade.PhysicsEnginePlatformer(
            self.spieler, gravity_constant=SCHWERKRAFT, walls=self.level["Boden"]
        )

        # Spieler bekommt Punkte
        self.punkte = 0

        # What key is pressed down?
        self.linke_taste_unten = False
        self.rechte_taste_unten = False
        self.obere_taste_unten = False
        self.untere_taste_unten = False

        # Text object to display the punkte
        self.punkte_text = arcade.Text(
            "Punkte: 0",
            x=FENSTER_WEITE-150,
            y=FENSTER_HÖHE-50,
            color=arcade.csscolor.BLUE,
            font_size=18,
        )

    def create_level(self) -> arcade.Scene:
        """Load the tilemap and create the level object."""
        # Our TileMap Object
        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for collision detection.
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
        }
        tile_map = arcade.load_tilemap(
            "levels/test.tmx",
            scaling=TILE_SKALIERUNG,
            layer_options=layer_options,
        )

        # Set the window background color to the same as the map if it has one
        if tile_map.background_color:
            self.window.background_color = Color.from_iterable(tile_map.background_color)

        # Use the tilemap's size to correctly set the camera's bounds.
        # Because how how shallow the map is we don't offset the bounds height
        self.kamera_grenzen = arcade.LRBT(
            self.window.width/2.0,
            tile_map.width * GRID_PIXEL_SIZE - self.window.width/2.0,
            self.window.height/2.0,
            tile_map.height * GRID_PIXEL_SIZE
        )


        # Our level Object
        # Initialize level with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the level in the proper order.
        return arcade.Scene.from_tilemap(tile_map)

    def reset(self):
        """Reset the game to the initial state."""
        self.punkte = 0
        # Load a fresh level to get the coins back
        self.level = self.create_level()

        # Move the player to start position
        self.spieler.position = (500, 500)
        # Add the player to the level
        self.level.add_sprite("Player", self.spieler)

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Male den Hintergrund
        arcade.draw_texture_rect(self.hintergrund, self.hintergrund_rect)

        # Draw the map with the sprite camera
        with self.kamera.activate():
            # Draw our level
            # Note, if you a want pixelated look, add pixelated=True to the parameters
            self.level.draw()

        # Draw the punkte with the gui camera
        with self.kamera_gui.activate():
            # Draw our punkte on the screen. The camera keeps it in place.
            self.punkte_text.text = f"Punkte: {self.punkte}"
            self.punkte_text.draw()

    def update_player_speed(self):
        # Calculate speed based on the keys pressed
        self.spieler.change_x = 0

        if self.linke_taste_unten and not self.rechte_taste_unten:
            self.spieler.change_x = -SPIELER_GESCHWINDIGKEIT
        elif self.rechte_taste_unten and not self.linke_taste_unten:
            self.spieler.change_x = SPIELER_GESCHWINDIGKEIT

        if self.spieler.klettert:
            if self.obere_taste_unten and not self.untere_taste_unten:
                self.spieler.change_y = SPIELER_KLETTER_GESCHWINDIGKEIT
            if self.untere_taste_unten and not self.obere_taste_unten:
                self.spieler.change_y = -SPIELER_KLETTER_GESCHWINDIGKEIT



    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        # Jump
        if key == arcade.key.UP or key == arcade.key.W:
            self.obere_taste_unten = True
            if not self.spieler.klettert and self.physik.can_jump():
                self.spieler.change_y = SPIELER_SPRUNGKRAFT

        # Left
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.linke_taste_unten = True

        # Right
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.rechte_taste_unten = True

        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.untere_taste_unten = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.linke_taste_unten = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.rechte_taste_unten = False
        elif key == arcade.key.UP or key == arcade.key.W:
            self.obere_taste_unten = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.untere_taste_unten = False


    def center_camera_to_player(self):
        # Bewege die Kamera zum Spieler hin
        self.kamera.position = arcade.math.smerp_2d(
            self.kamera.position,
            (self.spieler.position[0], self.spieler.position[1] +100),
            self.window.delta_time,
            KAMERA_GESCHWINDIGKEIT,
        )

        # Die Kamera darf die Bildgrenzen nicht überschreiten
        self.kamera.view_data.position = arcade.camera.grips.constrain_xy(
            self.kamera.view_data, self.kamera_grenzen
        )

        # Spieler soll horizontal sich nicht außerhalb der Kamera bewegen
        screen_x, _ = self.kamera.project(self.spieler.position)
        if screen_x <= 0:
            self.spieler.change_x = 0
            self.spieler.position = (self.spieler.position[0]+1, self.spieler.position[1])
        if screen_x >= FENSTER_WEITE:
            self.spieler.change_x = 0
            self.spieler.position = (self.spieler.position[0]-1, self.spieler.position[1])


    def sammel_münzen(self):
        # Berühren wir irgendwelche Münzen
        coin_hit_list = arcade.check_for_collision_with_list(
            self.spieler, self.level["Münzen"]
        )

        # Die berührten Münzen werden entfernt
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Add one to the punkte
            self.punkte += 1

    def benutze_leitern(self):
        if arcade.check_for_collision_with_list(self.spieler, self.level["Leitern"]):
            self.spieler.klettert = True
        else:
            self.spieler.klettert = False

    def on_update(self, delta_time: float):
        """Movement and game logic"""

        self.spieler.update_animation()

        # Move the player with the physics engine
        self.physik.update()
        self.sammel_münzen()
        self.benutze_leitern()
        self.update_player_speed()
        

        # Position the camera
        self.center_camera_to_player()

    def on_resize(self, width: int, height: int):
        """ Resize window """
        super().on_resize(width, height)
        # Update the cameras to match the new window size
        self.kamera.match_window()
        # The position argument keeps `0, 0` in the bottom left corner.
        self.kamera_gui.match_window(position=True)


def main():
    """Main function"""
    window = arcade.Window(FENSTER_WEITE, FENSTER_HÖHE, FENSTER_TITEL)
    spiel = Spiel()
    spiel.reset()

    window.show_view(spiel)
    arcade.run()


if __name__ == "__main__":
    main()