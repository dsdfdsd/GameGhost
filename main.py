from time import sleep

import pygame

clock = time.Clock()

init()
screen = display.set_mode((950, 555))
display.set_caption("GameGhost от Саши")

bg = image.load('images/bg.jpg').convert_alpha()
player = image.load('images/player_front.png').convert_alpha()
ghost = image.load('images/ghost.png').convert_alpha()

player_speed = 5
player_x = 450
player_y = 400

is_jump = False
jump_count = 8

walk_left = [
    image.load('images/player_left/player_left1.png').convert_alpha(),
    image.load('images/player_left/player_left2.png').convert_alpha(),
    image.load('images/player_left/player_left3.png').convert_alpha(),
    image.load('images/player_left/player_left3.png').convert_alpha(),
]

walk_right = [
    image.load('images/plaler_right/player_right1.png').convert_alpha(),
    image.load('images/plaler_right/player_right2.png').convert_alpha(),
    image.load('images/plaler_right/player_right3.png').convert_alpha(),
    image.load('images/plaler_right/player_right4.png').convert_alpha(),
]

ghost_list = []

player_anim_count = 0
bg_x = 0


bg_sound = mixer.Sound('sounds/bg.mp3')
bg_sound.play(-1)

ghost_timer = USEREVENT + 1
time.set_timer(ghost_timer, 3000)



label = font.Font('fonts/font.ttf', 60)
lose_label = label.render("You lose!", False, (216, 22, 22))
restart_label = label.render("Play?",False, (50, 212, 18))
restart_label_rect = restart_label.get_rect(topleft=(360, 260))

bullets_left = 5
bullet = image.load('images/bullet.png').convert_alpha()
bullets = []

gameplay = True

running = True
while running == True:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x  + 950, 0))

    if gameplay:

        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if ghost_list:
            for (i,el) in enumerate(ghost_list):
                screen.blit(ghost, el)
                el.x -= 10

                if el.x < -10:
                    ghost_list.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = key.get_pressed()
        if keys[K_a]:
            screen.blit(walk_left[int(player_anim_count)], (player_x, player_y))
        elif keys[K_d]:
            screen.blit(walk_right[int(player_anim_count)], (player_x, player_y))
        else:
            screen.blit(player, (player_x, player_y))

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -618:
            bg_x = 0

        if bullets:
            for (i,el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4
                if el.x > 970:
                    bullets.pop(i)

                if ghost_list:
                    for (index, ghosts) in enumerate(ghost_list):
                        if el.colliderect(ghosts):
                            ghost_list.pop(index)
                            bullets.pop(i)

        if keys[K_a] and player_x > 50:
            player_x -= player_speed
        elif keys[K_d] and player_x < 700:
            player_x += player_speed

        if not is_jump:
            if keys[K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8
    else:
        screen.fill((87, 88, 89))
        bg_sound.stop()
        screen.blit(lose_label, (360, 200))
        screen.blit(restart_label, restart_label_rect)
        bullets_left = 5

        mouse = mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and mouse.get_pressed()[0]:
            gameplay = True
            player_x = 450
            ghost_list.clear()
            bg_sound.play()
            bullets.clear()


    display.update()

    clock.tick(10)


    for event in event.get(): #хз
        if event.type == QUIT:
            running = False
            quit()
        if event.type == ghost_timer:
            ghost_list.append(ghost.get_rect(topleft=(920, 400)))
        if gameplay and event.type == KEYUP and event.key == K_f and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y - 15)))
            bullets_left -= 1

