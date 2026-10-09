import pygame


class HUD:
    def __init__(self):
        self.small_font = pygame.font.Font(None, 26) #police des petits titres
        self.font = pygame.font.Font(None, 36) #police principale du HUD
        self.game_over_title_font = pygame.font.Font(None, 42) #police du message de fin
        self.large_font = pygame.font.Font(None, 72) #police des grands titres

        self.text_color = (255, 235, 180) #couleur principale du texte
        self.accent_color = (210, 155, 65) #couleur des accents
        self.shadow_color = (35, 20, 15) #couleur des ombres
        self.warning_color = (190, 55, 45) #couleur des messages importants

    def draw_text(self, screen, font, value, position, color=None): #affiche un texte avec une ombre
        color = color or self.text_color #utilise la couleur standard si aucune couleur n'est fournie
        shadow_position = (position[0] + 2, position[1] + 2) #décale l'ombre du texte
        screen.blit(font.render(value, True, self.shadow_color), shadow_position)
        screen.blit(font.render(value, True, color), position)

    def draw_centered(self, screen, font, value, y, color=None): #affiche un texte centré horizontalement
        rectangle = font.render(value, True, color or self.text_color).get_rect(
            center=(screen.get_width() // 2, y),
        )
        self.draw_text(screen, font, value, rectangle.topleft, color)

    def draw_frame(self, screen, rectangle, fill_alpha=70, width=2): #affiche un encadré
        fill = pygame.Surface(rectangle.size, pygame.SRCALPHA) #surface transparente de l'encadré
        fill.fill((*self.shadow_color, fill_alpha))
        screen.blit(fill, rectangle.topleft)
        pygame.draw.rect(screen, self.accent_color, rectangle, width, border_radius=6)

    def draw_overlay(self, screen, alpha=235): #assombrit l'écran derrière un menu
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA) #surface de l'overlay
        overlay.fill((0, 0, 0, alpha))
        screen.blit(overlay, (0, 0))

    def draw(self, screen, score_value, elapsed_time, seated_clients, top): #affiche les informations pendant la partie
        self.draw_text(screen, self.small_font, "SCORE", (30, top + 18), self.accent_color)
        self.draw_text(screen, self.font, str(score_value), (30, top + 48))
        self.draw_text(
            screen,
            self.small_font,
            "TEMPS DE SURVIE",
            (390, top + 18),
            self.accent_color,
        )
        self.draw_text(
            screen,
            self.font,
            f"{int(elapsed_time)} s",
            (390, top + 48),
        )
        self.draw_text(
            screen,
            self.small_font,
            "CLIENTS ASSIS",
            (850, top + 18),
            self.accent_color,
        )
        self.draw_text(
            screen,
            self.font,
            f"{seated_clients} / 5",
            (850, top + 48),
        )

    def draw_start_screen(self, screen): #affiche l'écran de démarrage
        self.draw_overlay(screen)
        self.draw_frame(screen, pygame.Rect(250, 160, 780, 330), fill_alpha=110, width=3)
        title = "Bursti's TAVERN"
        controls = "ZQSD / Fleches : se deplacer | Clic gauche : lancer"
        objective = "Servez les clients avant que 5 tables soient occupees."
        start = "Appuyez sur Entree pour commencer"
        self.draw_text(
            screen,
            self.large_font,
            title,
            self.large_font.render(title, True, self.accent_color).get_rect(
                center=(640, 220),
            ).topleft,
            self.accent_color,
        )
        self.draw_centered(screen, self.font, controls, 310)
        self.draw_centered(screen, self.font, objective, 350)
        self.draw_centered(screen, self.font, start, 430)

    def draw_pause(self, screen): #affiche le menu pause
        self.draw_overlay(screen, alpha=245)
        self.draw_frame(screen, pygame.Rect(370, 180, 540, 190), fill_alpha=110, width=3)
        self.draw_centered(screen, self.large_font, "PAUSE", 250, self.accent_color)
        self.draw_centered(screen, self.font, "Echap : reprendre | R : recommencer", 320)

    def draw_game_over(self, screen, score_value, elapsed_time, seated_clients, name, entries): #affiche l'écran de fin et le leaderboard
        self.draw_overlay(screen, alpha=240)
        self.draw_frame(screen, pygame.Rect(150, 35, 980, 535), fill_alpha=110, width=3)
        score_text = self.font.render(f"Score final: {score_value}", True, self.text_color)
        clients_text = self.font.render(
            f"Clients assis: {seated_clients}/5",
            True,
            self.text_color,
        )
        timer_text = self.font.render(
            f"Temps: {int(elapsed_time)} s",
            True,
            self.text_color,
        )
        name_text = self.font.render(f"Pseudo: {name or 'entrez votre pseudo'}", True, self.text_color)
        self.draw_centered(
            screen,
            self.game_over_title_font,
            "La taverne s'est faite beuirstée,",
            70,
            self.warning_color,
        )
        self.draw_centered(
            screen,
            self.game_over_title_font,
            "vous êtes débordé...",
            108,
            self.warning_color,
        )
        score_rect = score_text.get_rect(center=(screen.get_width() // 2, 160))
        timer_rect = timer_text.get_rect(center=(screen.get_width() // 2, 195))
        clients_rect = clients_text.get_rect(center=(screen.get_width() // 2, 230))
        name_rect = name_text.get_rect(center=(screen.get_width() // 2, 270))

        screen.blit(score_text, score_rect)
        screen.blit(timer_text, timer_rect)
        screen.blit(clients_text, clients_rect)
        screen.blit(name_text, name_rect)

        for index, entry in enumerate(entries[:5]):
            entry_text = self.font.render(
                f"{index + 1}. {entry['name']} - {entry['score']}",
                True,
                self.text_color,
            )
            screen.blit(entry_text, (450, 310 + index * 30))

        help_text = self.font.render(
            "Entree: enregistrer | Ctrl+R: recommencer | Echap: quitter",
            True,
            self.text_color,
        )
        screen.blit(help_text, (300, 500))