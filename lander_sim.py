
import gymnasium as gym
import pygame
import numpy as np
import sys
import os

def main():
    if sys.platform == 'win32':
        import ctypes
        myappid = 'syedimad.lunarlander.simulator.1'
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except:
            pass

    pygame.init()
    pygame.display.set_caption("Lunar Lander: Manual Override")

    icon_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(icon_surf, (255, 255, 255), (16, 16), 14)
    pygame.draw.polygon(icon_surf, (255, 75, 75), [(16, 6), (8, 22), (24, 22)])
    pygame.display.set_icon(icon_surf)

    screen = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 24, bold=True)
    large_font = pygame.font.SysFont('Arial', 40, bold=True)

    env = gym.make("LunarLander-v3", render_mode="rgb_array")
    obs, info = env.reset()

    done = False
    waiting_for_start = True
    total_reward = 0.0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and waiting_for_start:
                    waiting_for_start = False
                elif event.key == pygame.K_ESCAPE:
                    done = True

        action = 0
        if not waiting_for_start:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]: action = 2
            elif keys[pygame.K_LEFT]: action = 1
            elif keys[pygame.K_RIGHT]: action = 3

            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            if terminated or truncated:
                done = True

        frame = env.render()
        surf = pygame.surfarray.make_surface(np.swapaxes(frame, 0, 1))
        screen.blit(surf, (0, 0))

        score_color = (0, 255, 0) if total_reward >= 0 else (255, 100, 100)
        score_text = font.render(f"SCORE: {total_reward:.1f}", True, score_color)
        screen.blit(score_text, (20, 20))

        if waiting_for_start:
            txt = large_font.render("PRESS SPACE TO START", True, (255, 255, 0))
            rect = txt.get_rect(center=(300, 200))
            pygame.draw.rect(screen, (0, 0, 0), rect.inflate(30, 20))
            screen.blit(txt, rect)

        pygame.display.flip()
        clock.tick(30)

    screen.fill((20, 20, 30))
    msg = large_font.render("SIMULATION COMPLETE", True, (255, 255, 255))
    s1 = font.render(f"Your Final Score: {total_reward:.1f}", True, score_color)
    s2 = font.render("AI Elite Benchmark: 267.0", True, (0, 255, 255))
    screen.blit(msg, msg.get_rect(center=(300, 130)))
    screen.blit(s1, s1.get_rect(center=(300, 200)))
    screen.blit(s2, s2.get_rect(center=(300, 250)))
    pygame.display.flip()
    pygame.time.wait(4000)

    env.close()
    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()
