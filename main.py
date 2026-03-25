import pygame
import os
import random
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog

def get_image_path_from_gui():
    """Avab failidialoogi, et valida pilt ja tagastab selle asukoha."""
    root = tk.Tk()
    root.withdraw()  # Peida peamine tkinter aken
    path = filedialog.askopenfilename(
        title="Vali pildifail",
        filetypes=[("Pildifailid", "*.jpg *.jpeg *.png *.bmp"), ("Kõik failid", "*.*")]
    )
    root.destroy()
    return path

def get_color_bucket(color, bins_per_channel):
    """Jaotab värvi "ämbrisse", et sarnaseid värve grupeerida."""
    bin_size = 256 // bins_per_channel
    return (color.r // bin_size, color.g // bin_size, color.b // bin_size)

# --- Põhiprogramm ---

# 1. Küsi kasutajalt pilti GUI kaudu
source_image_path = get_image_path_from_gui()

# Kui kasutaja sulgeb failidialoogi, on path tühi. Välju programmist.
if not source_image_path:
    print("Pilti ei valitud. Programm sulgub.")
    exit()

pygame.init()

# 2. Lae pildid
try:
    target_image = pygame.image.load("President_Barack_Obama.jpg")
    source_image = pygame.image.load(source_image_path)
except pygame.error as e:
    print(f"Pildi laadimisel tekkis viga: {e}")
    exit()

# 3. Määra uus, väiksem resolutsioon
ASPECT_RATIO = target_image.get_height() / target_image.get_width()
NEW_WIDTH = 300
NEW_HEIGHT = int(NEW_WIDTH * ASPECT_RATIO)
NEW_SIZE = (NEW_WIDTH, NEW_HEIGHT)

target_image_scaled = pygame.transform.scale(target_image, NEW_SIZE)
source_image_scaled = pygame.transform.scale(source_image, NEW_SIZE)

# 4. Ekraani seadistus
screen = pygame.display.set_mode(NEW_SIZE)
pygame.display.set_caption("Värvipõhine Piksli Animatsioon")

# 5. Jaga pikslid värviämbritesse
BINS = 8
source_buckets = defaultdict(list)
target_buckets = defaultdict(list)

for y in range(NEW_HEIGHT):
    for x in range(NEW_WIDTH):
        color = source_image_scaled.get_at((x, y))
        bucket = get_color_bucket(color, BINS)
        source_buckets[bucket].append({'color': color, 'original_pos': (x, y)})

        target_color = target_image_scaled.get_at((x, y))
        bucket = get_color_bucket(target_color, BINS)
        target_buckets[bucket].append((x, y))

# 6. Sobita pikslid ja loo osakesed
particles = []
unmatched_sources = []
unmatched_targets = []
all_buckets = set(source_buckets.keys()) | set(target_buckets.keys())

for bucket in all_buckets:
    sources = source_buckets[bucket]
    targets = target_buckets[bucket]
    random.shuffle(sources)
    random.shuffle(targets)
    match_count = min(len(sources), len(targets))

    for i in range(match_count):
        particles.append({
            'start_pos': sources[i]['original_pos'],
            'end_pos': targets[i],
            'color': sources[i]['color'],
            'start_time': pygame.time.get_ticks() + random.randint(0, 1000)
        })
    unmatched_sources.extend(sources[match_count:])
    unmatched_targets.extend(targets[match_count:])

random.shuffle(unmatched_sources)
random.shuffle(unmatched_targets)
match_count = min(len(unmatched_sources), len(unmatched_targets))
for i in range(match_count):
    particles.append({
        'start_pos': unmatched_sources[i]['original_pos'],
        'end_pos': unmatched_targets[i],
        'color': unmatched_sources[i]['color'],
        'start_time': pygame.time.get_ticks() + random.randint(0, 1000)
    })

# 7. Animatsiooni tsükkel
running = True
clock = pygame.time.Clock()
animation_duration = 4000

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    current_time = pygame.time.get_ticks()

    for p in particles:
        time_since_start = current_time - p['start_time']
        t = max(0, min(1, time_since_start / animation_duration))
        t = 1 - (1 - t)**3

        current_x = p['start_pos'][0] + (p['end_pos'][0] - p['start_pos'][0]) * t
        current_y = p['start_pos'][1] + (p['end_pos'][1] - p['start_pos'][1]) * t

        screen.set_at((int(current_x), int(current_y)), p['color'])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
