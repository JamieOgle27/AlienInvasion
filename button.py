import pygame.font

class Button:

    def __init__(self, ai_game, msg, button_pos_y = '', button_pos_x = '', button_width = '', button_height = ''):
        """Initialize button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #Set dimesions and properties of button
        if button_width:
            self.width = button_width
        else:
            self.width = 400
        if button_height:
            self.height = button_height
        else:
            self.height = 80
        self.button_color = (0,255,0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #Build the button's rect object and center it
        self.rect = pygame.Rect(0,0,self.width, self.height)
        if not button_pos_y:
            button_pos_y = 1.5 #position between top of screen (0) and bottom (2)
        if not button_pos_x:
            button_pos_x = 1 #position between the left of screen (0) and right (2)
        self.rect.center = (button_pos_x * self.screen_rect.center[0],  button_pos_y * self.screen_rect.center[1])
        #Button message needs to be prepper once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #Draw blank button and then draw message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

        