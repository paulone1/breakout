import pygame
import random

# Variables
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 128, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
WIDTH = 1288
HEIGHT = 960


# --- Classes ---


class Brick(pygame.sprite.Sprite):
    """This class represents a simple brick the player collects."""

    def __init__(self, colour):
        """Constructor, create the image of the brick."""
        super().__init__()
        self.image = pygame.Surface([91, 20])
        self.image.fill(colour)
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    """This class represents the player."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([140, 20])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - 70
        self.rect.y = HEIGHT - 30

    def start(self):
        """Start new health player"""
        self.rect.x = WIDTH // 2 - 70
        self.rect.y = HEIGHT - 30

    def update(self):
        """Update the player location."""
        VELOSITY = 8
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.x + VELOSITY + 140 < WIDTH:
            self.rect.x += VELOSITY
        if keys[pygame.K_LEFT] and self.rect.x - VELOSITY > 0:
            self.rect.x -= VELOSITY


class Ball(pygame.sprite.Sprite):
    """This class represents the ball."""

    def __init__(self, colour, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.ellipse(self.image, colour, [0, 0, width, height], 10)
        self.rect = self.image.get_rect()
        self.ball_speed_x = 7 * random.choice((1, -1))
        self.ball_speed_y = -7
        self.rect.x = WIDTH // 2 - 10
        self.rect.y = HEIGHT - 50
        self.BOUNCE_SOUND = pygame.mixer.Sound("sound_breakout_brick.mp3")
        self.BOUNCE_SOUND.set_volume(0.1)

    def start(self):
        """Start new health ball"""
        self.rect.x = WIDTH // 2 - 10
        self.rect.y = HEIGHT - 50

    def update(self):
        """Update the ball location."""
        self.rect.x += self.ball_speed_x
        self.rect.y += self.ball_speed_y

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            pygame.mixer.Sound.play(self.BOUNCE_SOUND)
            self.ball_speed_y *= -1
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            pygame.mixer.Sound.play(self.BOUNCE_SOUND)
            self.ball_speed_x *= -1

    def bounce(self):
        self.ball_speed_y *= -1


class Game(object):
    """This class represents an instance of the game. If we need to
    reset the game we'd just need to create a new instance of this
    class."""

    def __init__(self):
        """Constructor. Create all our attributes and initialize
        the game."""

        self.score = 0
        self.health = 3
        self.menu = False
        self.BASIC_FONT = pygame.font.SysFont("comicsans", 30)
        self.PADDLE_SOUND = pygame.mixer.Sound("sound_breakout_paddle.mp3")
        self.PADDLE_SOUND.set_volume(0.1)
        self.SCORE_SOUND = pygame.mixer.Sound("sound_breakout_score.mp3")
        self.SCORE_SOUND.set_volume(0.1)
        self.GAME_OVER_SOUND = pygame.mixer.Sound("sound_breakout_gameover.mp3")
        self.GAME_OVER_SOUND.set_volume(0.1)
        self.LOOSE_LIFE_SOUND = pygame.mixer.Sound("sound_breakout_loselife.mp3")
        self.LOOSE_LIFE_SOUND.set_volume(0.1)

        # Create sprite lists
        self.yellow_brick_list = pygame.sprite.Group()
        self.green_brick_list = pygame.sprite.Group()
        self.orange_brick_list = pygame.sprite.Group()
        self.red_brick_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()

        # Create the brick sprites
        brick_x = 0
        brick_y = 50
        for i in range(112):
            if brick_y <= 71:
                red_brick = Brick(RED)
                red_brick.rect.x = brick_x
                red_brick.rect.y = brick_y
                self.red_brick_list.add(red_brick)
                self.all_sprites_list.add(red_brick)
            if brick_y > 71 and brick_y <= 114:
                orange_brick = Brick(ORANGE)
                orange_brick.rect.x = brick_x
                orange_brick.rect.y = brick_y
                self.orange_brick_list.add(orange_brick)
                self.all_sprites_list.add(orange_brick)
            if brick_y > 114 and brick_y <= 157:
                green_brick = Brick(GREEN)
                green_brick.rect.x = brick_x
                green_brick.rect.y = brick_y
                self.green_brick_list.add(green_brick)
                self.all_sprites_list.add(green_brick)
            if brick_y > 157:
                yellow_brick = Brick(YELLOW)
                yellow_brick.rect.x = brick_x
                yellow_brick.rect.y = brick_y
                self.red_brick_list.add(yellow_brick)
                self.all_sprites_list.add(yellow_brick)
            brick_x += 92
            if brick_x >= WIDTH:
                brick_x = 0
                brick_y += 21

        # Create the player
        self.player = Player()
        self.all_sprites_list.add(self.player)

        # Create the ball
        self.ball = Ball(WHITE, 20, 20)
        self.all_sprites_list.add(self.ball)

    def process_events(self):
        """Process all of the events. Return a "True" if we need
        to close the window."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.menu:
                    self.__init__()

        return True

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not self.menu:
            # Move all the sprites
            self.all_sprites_list.update()

        if pygame.sprite.collide_rect(
            self.ball, self.player
        ):  # See if the ball has collided with bat
            pygame.mixer.Sound.play(self.PADDLE_SOUND)
            self.ball.bounce()

        if pygame.sprite.spritecollide(
            self.ball, self.yellow_brick_list, True
        ):  # See if ball has collided with brick
            pygame.mixer.Sound.play(self.SCORE_SOUND)
            self.score += 1
            self.ball.bounce()
        if pygame.sprite.spritecollide(self.ball, self.green_brick_list, True):
            pygame.mixer.Sound.play(self.SCORE_SOUND)
            self.score += 3
            self.ball.bounce()
        if pygame.sprite.spritecollide(self.ball, self.orange_brick_list, True):
            pygame.mixer.Sound.play(self.SCORE_SOUND)
            self.score += 5
            self.ball.bounce()
        if pygame.sprite.spritecollide(self.ball, self.red_brick_list, True):
            pygame.mixer.Sound.play(self.SCORE_SOUND)
            self.score += 7
            self.ball.bounce()

        if self.ball.rect.bottom > HEIGHT:  # See if ball has hit the bottom
            pygame.mixer.Sound.play(self.LOOSE_LIFE_SOUND)
            self.health -= 1
            self.ball.start()
            self.player.start()

        if self.health == 0:  # loose
            pygame.mixer.Sound.play(self.GAME_OVER_SOUND)
            self.menu = True

    def display_frame(self, SCREEN):
        """Display everything to the screen for the game."""
        SCREEN.fill(0)

        if self.menu:
            font = pygame.font.SysFont("Arial", 25)
            start_text = font.render("Press any key to start", True, WHITE)
            instructions_text = font.render(
                "Use arrow keys left and right to move the paddle and try to destroy all the bricks",
                True,
                WHITE,
            )
            SCREEN.blit(
                start_text, [(WIDTH // 2) - (start_text.get_width() // 2), HEIGHT // 2]
            )
            SCREEN.blit(
                instructions_text,
                [
                    (WIDTH // 2) - (instructions_text.get_width() // 2),
                    (HEIGHT // 2) + 70,
                ],
            )

        if not self.menu:
            self.all_sprites_list.draw(SCREEN)
            self.score_text = self.BASIC_FONT.render(
                f"Score: {self.score}", False, WHITE
            )  # Display scores
            self.health_text = self.BASIC_FONT.render(
                f"Health: {self.health}", False, WHITE
            )
            SCREEN.blit(self.score_text, (WIDTH - 150, 10))
            SCREEN.blit(self.health_text, (30, 10))

        pygame.display.flip()


def main():
    """Main program function."""
    pygame.init()  # Initialize Pygame and set up the window
    pygame.mixer.init()  # Initialize Pygame sounds

    SIZE = [WIDTH, HEIGHT]
    SCREEN = pygame.display.set_mode(SIZE)

    pygame.display.set_caption("Breakout")

    run = True  # Create our objects and set the data
    clock = pygame.time.Clock()

    game = Game()  # Create an instance of the Game class

    while run:  # Main game loop
        run = game.process_events()  # Process events (keystrokes, mouse clicks, etc)
        game.run_logic()  # Update object positions, check for collisions
        game.display_frame(SCREEN)  # Draw the current frame
        clock.tick(60)  # Pause for the next frame

    pygame.quit()  # Close window and exit


if __name__ == "__main__":  # Call the main function, start up the game
    main()
