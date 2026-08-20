import random
import pygame

# Initialize engine & create window
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Particle Physics Engine")
clock = pygame.time.Clock()


class Particle:

    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.radius = 10
        self.vel = pygame.math.Vector2(
            random.uniform(-4, 4),  # Random horizontal spray
            random.uniform(-5, -1),  # Upward pop
        )
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )

    def update(self, dt=1.0):
        # 1. Apply Gravity (scaled by sub-step delta time)
        self.vel.y += 0.5 * dt

        # 2. Air Drag
        self.vel.x *= 0.99
        self.vel.y *= 0.99

        # 3. Update Position
        self.pos += self.vel * dt

        # 4. Floor Boundary & Ground Friction
        if self.pos.y + self.radius >= SCREEN_HEIGHT:
            self.pos.y = SCREEN_HEIGHT - self.radius
            self.vel.y *= -0.8
            self.vel.x *= 0.9

            # Micro-jitter mitigation
            if abs(self.vel.y) < 0.5:
                self.vel.y = 0
            if abs(self.vel.x) < 0.1:
                self.vel.x = 0

        # 5. Ceiling Boundary
        if self.pos.y - self.radius <= 0:
            self.pos.y = self.radius
            self.vel.y *= -0.8

        # 6. Left Wall Boundary
        if self.pos.x - self.radius <= 0:
            self.pos.x = self.radius
            self.vel.x *= -0.8

        # 7. Right Wall Boundary
        if self.pos.x + self.radius >= SCREEN_WIDTH:
            self.pos.x = SCREEN_WIDTH - self.radius
            self.vel.x *= -0.8

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.radius)


def handle_collisions(particles):
    restitution = 0.8  # Bounciness factor

    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            p1 = particles[i]
            p2 = particles[j]

            delta = p2.pos - p1.pos
            dist = delta.length()

            # Guard against zero distance (spawning on identical pixel)
            if dist == 0:
                delta = pygame.math.Vector2(0.001, 0)
                dist = 0.001

            min_dist = p1.radius + p2.radius

            # Check for overlap
            if dist < min_dist:
                normal = delta / dist
                overlap = min_dist - dist

                # 1. Positional Separation
                p1.pos -= normal * (overlap / 2)
                p2.pos += normal * (overlap / 2)

                # 2. Velocity Response
                relative_velocity = p2.vel - p1.vel
                vel_along_normal = relative_velocity.dot(normal)

                if vel_along_normal < 0:
                    j_scalar = -(1 + restitution) * vel_along_normal / 2
                    impulse = j_scalar * normal

                    p1.vel -= impulse
                    p2.vel += impulse


particles = []
font = pygame.font.SysFont(None, 24)
running = True

while running:
    # 1. EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if len(particles) < 300:  # Cap particle count for performance
                particles.append(Particle(mouse_x, mouse_y))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                particles.clear()  # Press 'C' to clear screen

    # 2. PHYSICS UPDATE (Sub-stepping loop)
    sub_steps = 8
    dt = 1.0 / sub_steps
    for _ in range(sub_steps):
        for p in particles:
            p.update(dt)
        handle_collisions(particles)

    # 3. RENDER
    screen.fill((20, 20, 20))  # Background

    for p in particles:
        p.draw(screen)

    # Render HUD
    fps_text = font.render(
        f"FPS: {int(clock.get_fps())}", True, (255, 255, 255)
    )
    count_text = font.render(
        f"Particles: {len(particles)}", True, (255, 255, 255)
    )
    clear_text = font.render("Press 'C' to clear", True, (150, 150, 150))

    screen.blit(fps_text, (10, 10))
    screen.blit(count_text, (10, 30))
    screen.blit(clear_text, (10, 50))

    # 4. REFRESH & TICK
    pygame.display.flip()
    clock.tick(60)

pygame.quit()