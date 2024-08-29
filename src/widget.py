import pygame

class Widget:
    def __init__(self, surface: pygame.Surface, top_left_x: int, top_left_y: int, width: int, height: int, 
                 font: pygame.font.Font = None, color: tuple = (0, 0, 0), textures: dict = None):
        self.surface = surface
        self.xpos = top_left_x
        self.ypos = top_left_y
        self.width = width
        self.height = height
        self.font = font if font else pygame.font.Font(None, 24)
        self.color = color
        self.textures = textures if textures else {}

    def draw(self):
        pass

    def handle_event(self, event):
        pass

    def draw_texture(self, texture):
        scaled_texture = pygame.transform.scale(texture, (self.width, self.height))
        self.surface.blit(scaled_texture, (self.xpos, self.ypos))

class Button(Widget):
    def __init__(self, surface: pygame.Surface, top_left_x: int, top_left_y: int, width: int, height: int, 
                 label: str, on_click_function: callable, font: pygame.font.Font = None, 
                 color: tuple = (0, 0, 0), textures: dict = None):
        super().__init__(surface, top_left_x, top_left_y, width, height, font, color, textures)
        self.label = label
        self.on_click_function = on_click_function
        self.is_hovered = False
        self.is_pressed = False

    def draw(self):
        if self.is_pressed and "pressed" in self.textures:
            texture = self.textures["pressed"]
        elif self.is_hovered and "hovered" in self.textures:
            texture = self.textures["hovered"]
        else:
            texture = self.textures.get("normal")

        if texture:
            self.draw_texture(texture)
        else:
            pygame.draw.rect(self.surface, self.color, (self.xpos, self.ypos, self.width, self.height), 2)

        text_surface = self.font.render(self.label, True, self.color)
        text_rect = text_surface.get_rect(center=(self.xpos + self.width // 2, self.ypos + self.height // 2))
        self.surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._is_hovered(event.pos):
                self.is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_pressed and self._is_hovered(event.pos):
                self.on_click_function()
            self.is_pressed = False
        elif event.type == pygame.MOUSEMOTION:
            self.is_hovered = self._is_hovered(event.pos)

    def _is_hovered(self, mouse_pos):
        return (self.xpos <= mouse_pos[0] <= self.xpos + self.width and
                self.ypos <= mouse_pos[1] <= self.ypos + self.height)

class Checkbox(Widget):
    def __init__(self, surface: pygame.Surface, top_left_x: int, top_left_y: int, width: int, height: int, 
                 checked: bool = False, font: pygame.font.Font = None, color: tuple = (0, 0, 0), 
                 textures: dict = None):
        super().__init__(surface, top_left_x, top_left_y, width, height, font, color, textures)
        self.checked = checked

    def draw(self):
        if self.checked and "checked" in self.textures:
            texture = self.textures["checked"]
        else:
            texture = self.textures.get("unchecked")

        if texture:
           self.draw_texture(texture)
        else:
            pygame.draw.rect(self.surface, self.color, (self.xpos, self.ypos, self.width, self.height), 2)
            if self.checked:
                pygame.draw.line(self.surface, self.color, (self.xpos, self.ypos), 
                                 (self.xpos + self.width, self.ypos + self.height), 2)
                pygame.draw.line(self.surface, self.color, (self.xpos + self.width, self.ypos), 
                                 (self.xpos, self.ypos + self.height), 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._is_hovered(event.pos):
                self.checked = not self.checked

    def _is_hovered(self, mouse_pos):
        return (self.xpos <= mouse_pos[0] <= self.xpos + self.width and
                self.ypos <= mouse_pos[1] <= self.ypos + self.height)

class Slider(Widget):
    def __init__(self, surface: pygame.Surface, top_left_x: int, top_left_y: int, width: int, height: int, 
                 min_value: int = 0, max_value: int = 100, initial_value: int = 50, 
                 font: pygame.font.Font = None, color: tuple = (0, 0, 0), textures: dict = None):
        super().__init__(surface, top_left_x, top_left_y, width, height, font, color, textures)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.slider_xpos = self.xpos + int((self.value - self.min_value) / (self.max_value - self.min_value) * self.width)
        self.is_dragging = False

    def draw(self):
        if "track" in self.textures:
            self.surface.blit(self.textures["track"], (self.xpos, self.ypos + self.height // 2 - 2))
        else:
            pygame.draw.rect(self.surface, (150, 150, 150), (self.xpos, self.ypos + self.height // 2 - 2, self.width, 4))
        
        if "handle" in self.textures:
            handle_width = self.textures["handle"].get_width()
            handle_height = self.textures["handle"].get_height()
            self.surface.blit(self.textures["handle"], (self.slider_xpos - handle_width // 2, self.ypos + self.height // 2 - handle_height // 2))
        else:
            pygame.draw.circle(self.surface, self.color, (self.slider_xpos, self.ypos + self.height // 2), self.height // 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._is_hovered(event.pos):
                self.is_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self.slider_xpos = max(self.xpos, min(event.pos[0], self.xpos + self.width))
            self.value = self.min_value + (self.slider_xpos - self.xpos) / self.width * (self.max_value - self.min_value)
            self.value = int(self.value)

    def _is_hovered(self, mouse_pos):
        return (self.xpos <= mouse_pos[0] <= self.xpos + self.width and
                self.ypos <= mouse_pos[1] <= self.ypos + self.height)

class TextInput(Widget):
    def __init__(self, surface: pygame.Surface, top_left_x: int, top_left_y: int, width: int, height: int, 
                 default_text: str = '', font: pygame.font.Font = None, color: tuple = (0, 0, 0), 
                 active_color: tuple = (0, 0, 255), textures: dict = None):
        super().__init__(surface, top_left_x, top_left_y, width, height, font, color, textures)
        self.text = default_text
        self.active = False
        self.cursor_visible = True
        self.cursor_position = len(default_text)
        self.active_color = active_color
        self.selection_start = None

    def draw(self):
        box_color = self.active_color if self.active else self.color

        if "box" in self.textures:
            self.draw_texture(self.textures["box"])
        else:
            pygame.draw.rect(self.surface, box_color, (self.xpos, self.ypos, self.width, self.height), 2)

        text_surface = self.font.render(self.text, True, self.color)
        self.surface.blit(text_surface, (self.xpos + 5, self.ypos + (self.height - text_surface.get_height()) // 2))

        if self.active and self.cursor_visible:
            cursor_xpos = self.xpos + 5 + self.font.size(self.text[:self.cursor_position])[0]
            pygame.draw.line(self.surface, box_color, (cursor_xpos, self.ypos + 5), 
                             (cursor_xpos, self.ypos + self.height - 5), 2)

        if self.active and self.selection_start is not None:
            selection_end = self.cursor_position
            if self.selection_start != selection_end:
                start, end = sorted((self.selection_start, selection_end))
                selection_width = self.font.size(self.text[start:end])[0]
                selection_xpos = self.xpos + 5 + self.font.size(self.text[:start])[0]
                pygame.draw.rect(self.surface, (0, 0, 150), (selection_xpos, self.ypos + 5, selection_width, self.height - 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._is_hovered(event.pos):
                self.active = True
                self.cursor_position = self._get_cursor_from_click(event.pos[0])
            else:
                self.active = False
            self.selection_start = None
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                if self.selection_start is not None and self.selection_start != self.cursor_position:
                    self._delete_selection()
                elif self.cursor_position > 0:
                    self.text = self.text[:self.cursor_position-1] + self.text[self.cursor_position:]
                    self.cursor_position -= 1
            elif event.key == pygame.K_DELETE:
                if self.selection_start is not None and self.selection_start != self.cursor_position:
                    self._delete_selection()
                elif self.cursor_position < len(self.text):
                    self.text = self.text[:self.cursor_position] + self.text[self.cursor_position+1:]
            elif event.key == pygame.K_LEFT:
                if self.cursor_position > 0:
                    self.cursor_position -= 1
            elif event.key == pygame.K_RIGHT:
                if self.cursor_position < len(self.text):
                    self.cursor_position += 1
            elif event.key == pygame.K_RETURN:
                print(f"Entered text: {self.text}")
                self.active = False
            elif event.key == pygame.K_a and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.selection_start = 0
                self.cursor_position = len(self.text)
            else:
                if self.selection_start is not None and self.selection_start != self.cursor_position:
                    self._delete_selection()
                self.text = self.text[:self.cursor_position] + event.unicode + self.text[self.cursor_position:]
                self.cursor_position += 1
            self.selection_start = None

    def _get_cursor_from_click(self, click_x):
        relative_x = click_x - (self.xpos + 5)
        text_before_click = ''
        for i, char in enumerate(self.text):
            if self.font.size(text_before_click + char)[0] > relative_x:
                return i
            text_before_click += char
        return len(self.text)

    def _delete_selection(self):
        start, end = sorted((self.selection_start, self.cursor_position))
        self.text = self.text[:start] + self.text[end:]
        self.cursor_position = start
        self.selection_start = None

    def _is_hovered(self, mouse_pos):
        return (self.xpos <= mouse_pos[0] <= self.xpos + self.width and
                self.ypos <= mouse_pos[1] <= self.ypos + self.height)

class Dropdown(Widget):
    def __init__(self, surface: pygame.Surface, top_left_x: int, top_left_y: int, width: int, height: int, 
                 options: list, font: pygame.font.Font = None, color: tuple = (0, 0, 0), textures: dict = None):
        super().__init__(surface, top_left_x, top_left_y, width, height, font, color, textures)
        self.options = options
        self.selected_index = 0
        self.is_expanded = False

    def draw(self):
        current_text = self.options[self.selected_index]
        if self.is_expanded and "expanded" in self.textures:
            texture = self.textures["expanded"]
        else:
            texture = self.textures.get("normal")

        if texture:
            self.draw_texture(texture)
        else:
            pygame.draw.rect(self.surface, self.color, (self.xpos, self.ypos, self.width, self.height), 2)

        text_surface = self.font.render(current_text, True, self.color)
        self.surface.blit(text_surface, (self.xpos + 5, self.ypos + (self.height - text_surface.get_height()) // 2))

        if self.is_expanded:
            for i, option in enumerate(self.options):
                option_ypos = self.ypos + (i + 1) * self.height
                if "option" in self.textures:
                    self.surface.blit(self.textures["option"], (self.xpos, option_ypos))
                else:
                    pygame.draw.rect(self.surface, self.color, (self.xpos, option_ypos, self.width, self.height), 2)

                option_surface = self.font.render(option, True, self.color)
                self.surface.blit(option_surface, (self.xpos + 5, option_ypos + (self.height - option_surface.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._is_hovered(event.pos):
                self.is_expanded = not self.is_expanded
            elif self.is_expanded:
                for i in range(len(self.options)):
                    option_rect = pygame.Rect(self.xpos, self.ypos + (i + 1) * self.height, self.width, self.height)
                    if option_rect.collidepoint(event.pos):
                        self.selected_index = i
                        self.is_expanded = False
                        break
                else:
                    self.is_expanded = False

    def _is_hovered(self, mouse_pos):
        return (self.xpos <= mouse_pos[0] <= self.xpos + self.width and
                self.ypos <= mouse_pos[1] <= self.ypos + self.height)
