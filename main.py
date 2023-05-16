import pygame
import sys
import csv

def charger_niveau(nom_fichier):
    briques = []
    with open(nom_fichier) as fichier:
        lecteur_csv = csv.reader(fichier, delimiter=',')
        for y, ligne in enumerate(lecteur_csv):
            for x, colonne in enumerate(ligne):
                if colonne == '1':
                    brique = {
                        "rect": pygame.Rect(x * (BRIQUE_WIDTH + 2) + 50, y * (BRIQUE_HEIGHT + 2) + 50, BRIQUE_WIDTH, BRIQUE_HEIGHT),
                        "coups": 1,
                        "couleur": (0, 255, 0)
                    }
                    briques.append(brique)
                elif colonne == '2':
                    brique = {
                        "rect": pygame.Rect(x * (BRIQUE_WIDTH + 2) + 50, y * (BRIQUE_HEIGHT + 2) + 50, BRIQUE_WIDTH, BRIQUE_HEIGHT),
                        "coups": 2,
                        "couleur": (0, 255, 0)
                    }
                    briques.append(brique)
                elif colonne == '3':
                    brique = {
                        "rect": pygame.Rect(x * (BRIQUE_WIDTH + 2) + 50, y * (BRIQUE_HEIGHT + 2) + 50, BRIQUE_WIDTH, BRIQUE_HEIGHT),
                        "coups": -1,
                        "couleur": (0, 0, 255)
                    }
                    briques.append(brique)
    return briques


# Initialiser Pygame
pygame.init()

# Cacher le curseur de la souris
pygame.mouse.set_visible(False)

# Créer une horloge
clock = pygame.time.Clock()

# Créer une font pour le texte
font = pygame.font.Font(None, 36)

# Initialiser le score
score = 0

# Définir la taille de l'écran et obtenir la résolution de l'écran
infoObject = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Créer l'écran en plein écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Définir les propriétés de la raquette
RAQUETTE_WIDTH, RAQUETTE_HEIGHT = 100, 10
raquette = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, RAQUETTE_WIDTH, RAQUETTE_HEIGHT)

# Définir les propriétés de la balle
BALLE_RADIUS = 10
balle = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALLE_RADIUS, BALLE_RADIUS)
balle_vx = 1
balle_vy = -1

# Définir les propriétés des briques
BRIQUE_WIDTH, BRIQUE_HEIGHT = 50, 20

# Créer les briques
# Charger le niveau depuis un fichier
briques = charger_niveau("niveau1.txt")

# Boucle principale du jeu
while True:
    # Régler le taux de rafraîchissement
    clock.tick(300)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    # Déplacer la raquette avec la souris
    x, _ = pygame.mouse.get_pos()
    if x < RAQUETTE_WIDTH // 2:  # la souris est trop à gauche
        x = RAQUETTE_WIDTH // 2
        pygame.mouse.set_pos((x, _))
    elif x > SCREEN_WIDTH - RAQUETTE_WIDTH // 2:  # la souris est trop à droite
        x = SCREEN_WIDTH - RAQUETTE_WIDTH // 2
        pygame.mouse.set_pos((x, _))
    raquette.centerx = x

    # Déplacer la balle
    balle.x += balle_vx
    balle.y += balle_vy

    # Gérer les collisions avec les bords de l'écran
    if balle.left < 0:
        balle.left = 0
        balle_vx *= -1
    if balle.right > SCREEN_WIDTH:
        balle.right = SCREEN_WIDTH
        balle_vx *= -1
    if balle.top < 0:
        balle.top = 0
        balle_vy *= -1
    if balle.bottom > SCREEN_HEIGHT:
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, (SCREEN_HEIGHT - game_over_text.get_height()) // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    # Gérer les collisions avec la raquette
    if balle.colliderect(raquette):
        balle_vy *= -1
        # ajuster vx en fonction de l'endroit où la balle frappe la raquette
        balle_vx = (balle.centerx - raquette.centerx) / (RAQUETTE_WIDTH / 2) * 2

    # Gérer les collisions avec les briques
    for brique in briques:
        if balle.colliderect(brique["rect"]):
            # Vérifier si la brique est incassable
            if not brique["coups"] == -1:
                # Réduire le nombre de coups restants
                brique["coups"] -= 1
                if brique["coups"] == 0:
                    briques.remove(brique)
                    score += 1
                elif brique["coups"] == 1:
                    brique["couleur"] = (255, 255, 0)
            # Gérer la collision de la balle avec la brique
            if balle.centerx < brique["rect"].left or balle.centerx > brique["rect"].right:
                balle_vx *= -1
            if balle.centery < brique["rect"].top or balle.centery > brique["rect"].bottom:
                balle_vy *= -1
            break

    # Dessiner tout
    screen.fill((0, 0, 0))  # remplir l'écran avec du noir
    pygame.draw.rect(screen, (255, 255, 255), raquette)  # dessiner la raquette
    pygame.draw.circle(screen, (255, 0, 0), balle.center, BALLE_RADIUS)  # dessiner la balle
    # Dessiner les briques
    for brique in briques:
        pygame.draw.rect(screen, brique["couleur"], brique["rect"])

    # Dessiner le score
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    pygame.display.flip()  # mettre à jour l'affichage
