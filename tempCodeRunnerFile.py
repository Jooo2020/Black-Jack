    # Buttons zeichnen
        for btn in buttons:
            btn.draw(screen)

        restart_button.draw(screen)
        if status_message != "":
            text_surf = FONT.render(status_message, True, (255, 255, 255))
            screen.blit(text_surf, (1000, 50))


        pygame.display.flip()
        clock.tick(30)