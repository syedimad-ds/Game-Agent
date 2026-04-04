
import gymnasium as gym
import pygame
import numpy as np
import sys
import os

def main():
    pygame.init()
    
    # 1. FIX ICON AND TITLE (Loading actual image file)
    pygame.display.set_caption("Lunar Lander: Manual Override")
    
    # Try to load a real image file for the icon
    # MAKE SURE YOU HAVE A 'rocket_icon.png' IN YOUR FOLDER!
    if os.path.exists("rocket_icon.png"):
        try:
            icon_img = pygame.image.load("rocket_icon.png")
            pygame.display.set_icon(icon_img)
        except:
            pass # Fallback if image loading fails
    else:
        # Fallback dynamic icon if image is missing
        icon_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(icon_surf, (255, 255, 255), (16, 16), 14)
        pygame.draw.polygon(icon_surf, (255, 75, 75), [(16, 6), (8, 22), (24, 22)])
        pygame.display.set_icon(icon_surf)
        
    # 2. SETUP SCREEN
    screen = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 24, bold=True)
    large_font = pygame.font.SysFont('Arial', 40, bold=True)
    
    # 3. LOAD ENV (rgb_array prevents flickering)
    env = gym.make("LunarLander-v3", render_mode="rgb_array")
    obs, info = env.reset()
    
    done = False
    waiting_for_start = True
    total_reward = 0.0
    
    # 4. GAME ENGINE
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

        # Render background
        frame = env.render()
        surf = pygame.surfarray.make_surface(np.swapaxes(frame, 0, 1))
        screen.blit(surf, (0, 0))
        
        # UI Overlays (Live Score)
        score_color = (0, 255, 0) if total_reward >= 0 else (255, 100, 100)
        score_text = font.render(f"SCORE: {total_reward:.1f}", True, score_color)
        screen.blit(score_text, (20, 20))
        
        # Solid "Press Space" Prompt
        if waiting_for_start:
            prompt_text = large_font.render("PRESS SPACE TO START", True, (255, 255, 0))
            rect = prompt_text.get_rect(center=(300, 200))
            pygame.draw.rect(screen, (0, 0, 0), rect.inflate(30, 20))
            screen.blit(prompt_text, rect)
            
        pygame.display.flip()
        clock.tick(30)
        
    # 5. GAME OVER SCREEN (Compares to 267.00)  
    screen.fill((20, 20, 30))
    go_text = large_font.render("SIMULATION TERMINATED", True, (255, 255, 255))
    score_res = font.render(f"Your Score: {total_reward:.1f}", True, score_color)
    ai_res = font.render("AI Elite Score: 267.00", True, (0, 255, 255))
    
    screen.blit(go_text, go_text.get_rect(center=(300, 130)))
    screen.blit(score_res, score_res.get_rect(center=(300, 200)))
    screen.blit(ai_res, ai_res.get_rect(center=(300, 250)))
    
    pygame.display.flip()
    
    # Wait 4.5 seconds safely
    wait_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - wait_time < 4500:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        clock.tick(30)

    env.close()
    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()
