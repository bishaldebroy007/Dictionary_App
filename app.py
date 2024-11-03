import pygame
import json
from difflib import get_close_matches

# Load data
data = json.load(open("data.json"))

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (230, 230, 250)
TEXT_COLOR = (30, 30, 30)
INPUT_BOX_COLOR = (255, 255, 255)
RESULT_COLOR = (0, 100, 250)
BUTTON_COLOR = (100, 149, 237)
BUTTON_HOVER_COLOR = (65, 105, 225)
FONT = pygame.font.Font(None, 32)
LARGE_FONT = pygame.font.Font(None, 48)

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dictionary App")

# Helper function to render text on the screen
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(topleft=(x, y))
    surface.blit(textobj, textrect)

# Button class
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BUTTON_COLOR
        self.hover_color = BUTTON_HOVER_COLOR
        self.text = text
        self.font = FONT

    def draw(self, surface):
        color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(surface, color, self.rect)
        draw_text(self.text, self.font, (255, 255, 255), surface, self.rect.x + 10, self.rect.y + 10)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# Function to get meaning or suggestion
def translate(word):
    word = word.lower()
    if word in data:
        return data[word]
    elif word.title() in data:
        return data[word.title()]
    elif word.upper() in data:
        return data[word.upper()]
    elif len(get_close_matches(word, data.keys())) > 0:
        return {"suggestion": get_close_matches(word, data.keys())[0]}
    else:
        return "Sorry, the word you're looking for doesn't exist!"

# Main function
def main():
    input_box = pygame.Rect(50, 100, 700, 50)
    user_text = ""
    result_text = ""
    suggestion_text = ""
    is_suggestion = False

    search_button = Button(680, 160, 70, 40, "Search")
    yes_button = Button(50, 400, 70, 40, "Yes")
    no_button = Button(150, 400, 70, 40, "No")

    clock = pygame.time.Clock()
    active = True

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    meaning = translate(user_text)
                    if isinstance(meaning, list):
                        result_text = "\n".join(meaning)
                        suggestion_text = ""
                        is_suggestion = False
                    elif isinstance(meaning, dict) and "suggestion" in meaning:
                        suggestion_text = f"Did you mean '{meaning['suggestion']}'?"
                        result_text = ""
                        is_suggestion = True
                    else:
                        result_text = meaning
                        suggestion_text = ""
                        is_suggestion = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

            if search_button.is_clicked(event):
                meaning = translate(user_text)
                if isinstance(meaning, list):
                    result_text = "\n".join(meaning)
                    suggestion_text = ""
                    is_suggestion = False
                elif isinstance(meaning, dict) and "suggestion" in meaning:
                    suggestion_text = f"Did you mean '{meaning['suggestion']}'?"
                    result_text = ""
                    is_suggestion = True
                else:
                    result_text = meaning
                    suggestion_text = ""
                    is_suggestion = False

            if is_suggestion:
                if yes_button.is_clicked(event):
                    meaning = data[get_close_matches(user_text, data.keys())[0]]
                    result_text = "\n".join(meaning) if isinstance(meaning, list) else meaning
                    suggestion_text = ""
                    is_suggestion = False
                elif no_button.is_clicked(event):
                    result_text = "Sorry, the word you're looking for doesn't exist!"
                    suggestion_text = ""
                    is_suggestion = False

        # Fill background
        screen.fill(BACKGROUND_COLOR)

        # Draw UI elements
        draw_text("Dictionary App", LARGE_FONT, TEXT_COLOR, screen, 50, 20)
        draw_text("Enter a word:", FONT, TEXT_COLOR, screen, 50, 70)

        # Draw input box
        pygame.draw.rect(screen, INPUT_BOX_COLOR, input_box)
        draw_text(user_text, FONT, TEXT_COLOR, screen, input_box.x + 5, input_box.y + 5)

        # Draw buttons
        search_button.draw(screen)
        if is_suggestion:
            yes_button.draw(screen)
            no_button.draw(screen)

        # Display result or suggestion
        if result_text:
            draw_text("Meaning:", FONT, RESULT_COLOR, screen, 50, 220)
            for i, line in enumerate(result_text.split("\n")):
                draw_text(line, FONT, RESULT_COLOR, screen, 50, 260 + i * 30)
        elif suggestion_text:
            draw_text(suggestion_text, FONT, RESULT_COLOR, screen, 50, 220)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
