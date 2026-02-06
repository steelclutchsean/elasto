"""
Create a simple icon for Bungee Biker
Generates a PNG icon that can be converted to ICNS format
"""

import pygame
import math

def create_icon():
    """Create a simple bike icon"""
    # Icon size (1024x1024 for best quality)
    size = 1024
    surface = pygame.Surface((size, size), pygame.SRCALPHA)

    # Background gradient (sky blue to darker blue)
    for y in range(size):
        color_value = int(135 + (y / size) * 50)
        pygame.draw.line(surface, (color_value, 206, 235), (0, y), (size, y))

    # Draw a simple bike silhouette
    center_x, center_y = size // 2, size // 2

    # Wheels (large circles)
    wheel_radius = size // 6
    wheel_offset = size // 4

    # Rear wheel
    rear_wheel_pos = (center_x - wheel_offset, center_y + wheel_offset // 2)
    pygame.draw.circle(surface, (50, 50, 50), rear_wheel_pos, wheel_radius)
    pygame.draw.circle(surface, (200, 0, 0), rear_wheel_pos, wheel_radius, size // 30)

    # Front wheel
    front_wheel_pos = (center_x + wheel_offset, center_y + wheel_offset // 2)
    pygame.draw.circle(surface, (50, 50, 50), front_wheel_pos, wheel_radius)
    pygame.draw.circle(surface, (200, 0, 0), front_wheel_pos, wheel_radius, size // 30)

    # Bike frame (simplified)
    frame_width = size // 25

    # Seat to rear wheel
    pygame.draw.line(surface, (200, 0, 0),
                    (center_x - wheel_offset // 2, center_y - wheel_offset // 2),
                    rear_wheel_pos, frame_width)

    # Handlebars to front wheel
    pygame.draw.line(surface, (200, 0, 0),
                    (center_x + wheel_offset // 2, center_y - wheel_offset // 2),
                    front_wheel_pos, frame_width)

    # Top frame
    pygame.draw.line(surface, (200, 0, 0),
                    (center_x - wheel_offset // 2, center_y - wheel_offset // 2),
                    (center_x + wheel_offset // 2, center_y - wheel_offset // 2),
                    frame_width)

    # Rider head
    head_pos = (center_x, center_y - wheel_offset)
    head_radius = size // 10
    pygame.draw.circle(surface, (255, 200, 150), head_pos, head_radius)
    pygame.draw.circle(surface, (100, 50, 0), head_pos, head_radius, size // 100)

    # Helmet detail
    pygame.draw.arc(surface, (50, 50, 50),
                   (head_pos[0] - head_radius, head_pos[1] - head_radius,
                    head_radius * 2, head_radius * 2),
                   0, math.pi, size // 80)

    # Game title text
    font = pygame.font.Font(None, size // 10)
    title_text = font.render("BUNGEE", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(center_x, size // 8))

    # Text shadow
    shadow_text = font.render("BUNGEE", True, (0, 0, 0))
    surface.blit(shadow_text, (title_rect.x + 5, title_rect.y + 5))
    surface.blit(title_text, title_rect)

    subtitle_text = font.render("BIKER", True, (255, 255, 255))
    subtitle_rect = subtitle_text.get_rect(center=(center_x, size // 8 + size // 10))
    shadow_text2 = font.render("BIKER", True, (0, 0, 0))
    surface.blit(shadow_text2, (subtitle_rect.x + 5, subtitle_rect.y + 5))
    surface.blit(subtitle_text, subtitle_rect)

    return surface

def main():
    pygame.init()

    print("Creating icon...")
    icon = create_icon()

    # Save as PNG
    pygame.image.save(icon, "assets/icon.png")
    print("✓ Created assets/icon.png (1024x1024)")

    # Create smaller versions for different uses
    for size in [512, 256, 128, 64, 32, 16]:
        small_icon = pygame.transform.smoothscale(icon, (size, size))
        pygame.image.save(small_icon, f"assets/icon_{size}.png")
        print(f"✓ Created assets/icon_{size}.png")

    print("\nIcon generation complete!")
    print("\nTo convert to ICNS format on macOS:")
    print("  mkdir BungeeBiker.iconset")
    print("  cp assets/icon_16.png BungeeBiker.iconset/icon_16x16.png")
    print("  cp assets/icon_32.png BungeeBiker.iconset/icon_16x16@2x.png")
    print("  cp assets/icon_32.png BungeeBiker.iconset/icon_32x32.png")
    print("  cp assets/icon_64.png BungeeBiker.iconset/icon_32x32@2x.png")
    print("  cp assets/icon_128.png BungeeBiker.iconset/icon_128x128.png")
    print("  cp assets/icon_256.png BungeeBiker.iconset/icon_128x128@2x.png")
    print("  cp assets/icon_256.png BungeeBiker.iconset/icon_256x256.png")
    print("  cp assets/icon_512.png BungeeBiker.iconset/icon_256x256@2x.png")
    print("  cp assets/icon_512.png BungeeBiker.iconset/icon_512x512.png")
    print("  cp assets/icon.png BungeeBiker.iconset/icon_512x512@2x.png")
    print("  iconutil -c icns BungeeBiker.iconset -o assets/icon.icns")
    print("  rm -rf BungeeBiker.iconset")

if __name__ == '__main__':
    main()
