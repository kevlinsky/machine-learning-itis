import random
import pygame

pygame.init()
(width, height) = (200, 200)
screen = pygame.display.set_mode((width, height))
pygame.font.init()
my_font = pygame.font.SysFont('Winkle Regular', 95)


def generate(mode):
    if mode == 'test':
        labels = []
        for _ in range(10000):
            print(f'Image #{_ + 1}')
            num = str(random.randint(0, 10001))
            labels.append(num)
            screen.fill((0, 0, 0))
            text_surface = my_font.render(num, False, (255, 255, 255))
            screen.blit(text_surface, (40, 60))
            pygame.display.update()
            pygame.display.flip()
            screen_scaled = pygame.transform.scale(screen, (28, 28))
            file_name = f'test_images/sample_image_{_}.png'
            pygame.image.save(screen_scaled, file_name)

        with open('test_labels.csv', 'w') as file:
            file.truncate(0)

        with open('test_labels.csv', 'a') as file:
            for label in labels:
                file.write(f'{label}\n')
    elif mode == 'train':
        labels = []
        for _ in range(60000):
            print(f'Image #{_ + 1}')
            num = str(random.randint(0, 10001))
            labels.append(num)
            screen.fill((0, 0, 0))
            text_surface = my_font.render(num, False, (255, 255, 255))
            screen.blit(text_surface, (30, 60))
            pygame.display.update()
            pygame.display.flip()
            screen_scaled = pygame.transform.scale(screen, (28, 28))
            file_name = f'train_images/sample_image_{_}.png'
            pygame.image.save(screen_scaled, file_name)

        with open('train_labels.csv', 'w') as file:
            file.truncate(0)

        with open('train_labels.csv', 'a') as file:
            for label in labels:
                file.write(f'{label}\n')


if __name__ == '__main__':
    generate('train')
    generate('test')
