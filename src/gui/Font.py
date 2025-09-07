from panda3d.core import TextNode, CardMaker
from ursina import *
from PIL import Image

class Font:
    def __init__(self, atlas_path, char_spacing=1.2, size=1.0):
        self.atlas = load_texture(atlas_path)
        self.char_widths = [0] * 256
        self.char_width = 8
        self.char_height = 8
        self.atlas_width = 128
        self.atlas_height = 128
        self.char_spacing = char_spacing
        self.size = size
        
        self._calculate_char_widths(atlas_path)
        self.char_uvs = self._create_char_uvs()
    
    def _calculate_char_widths(self, atlas_path):
        try:
            img = Image.open(atlas_path).convert('RGBA')
            w, h = img.size
            pixels = list(img.getdata())
            
            for i in range(128):
                xt = i % 16
                yt = i // 16
                x = 0
                
                empty_column = False
                while x < 8 and not empty_column:
                    x_pixel = xt * 8 + x
                    empty_column = True
                    
                    for y in range(8):
                        y_pixel = (yt * 8 + y) * w + x_pixel
                        if y_pixel < len(pixels):
                            pixel_alpha = pixels[y_pixel][3] if len(pixels[y_pixel]) > 3 else 255
                            if pixel_alpha > 128:
                                empty_column = False
                                break
                    
                    if not empty_column:
                        x += 1
                
                if i == 32:
                    x = 4
                
                self.char_widths[i] = x if x > 0 else 8
                
        except Exception as e:
            print(f"Error in calculate char widths: {e}")
            for i in range(256):
                self.char_widths[i] = 8 if i != 32 else 4
    
    def _create_char_uvs(self):
        char_uvs = {}
        
        for i in range(128):
            char = chr(i)
            ix = (i % 16) * 8
            iy = (i // 16) * 8
            
            u1 = ix / self.atlas_width
            v1 = 1.0 - (iy + 8) / self.atlas_height
            u2 = (ix + 8) / self.atlas_width
            v2 = 1.0 - iy / self.atlas_height
            
            char_uvs[char] = (u1, v1, u2, v2)
        
        return char_uvs
    
    def _create_char_quad(self, char):
        if ord(char) >= 128 or char not in self.char_uvs:
            return None
        
        u1, v1, u2, v2 = self.char_uvs[char]
        
        vertices = [
            (-0.5, -0.5, 0),
            (0.5, -0.5, 0),
            (0.5, 0.5, 0),
            (-0.5, 0.5, 0)
        ]
        
        triangles = [
            (0, 1, 2),
            (0, 2, 3)
        ]
        
        uvs = [
            (u1, v1),
            (u2, v1),
            (u2, v2), 
            (u1, v2)
        ]
        
        normals = [
            (0, 0, 1),
            (0, 0, 1),
            (0, 0, 1),
            (0, 0, 1)
        ]
        
        mesh = Mesh(
            vertices=vertices,
            triangles=triangles,
            uvs=uvs,
            normals=normals,
            static=False
        )
        
        return mesh
    
    def _parse_color_codes(self, text):
        result = []
        i = 0
        current_color = color.white
        
        while i < len(text):
            if text[i] == '&' and i + 1 < len(text):
                color_char = text[i + 1]
                if color_char in "0123456789abcdef":
                    color_index = "0123456789abcdef".index(color_char)
                    brightness = (color_index & 8) * 8
                    b = (color_index & 1) * 191 + brightness
                    g = ((color_index & 2) >> 1) * 191 + brightness
                    r = ((color_index & 4) >> 2) * 191 + brightness
                    
                    current_color = color.rgb(r/255, g/255, b/255)
                    i += 2
                    continue
            
            result.append((text[i], current_color))
            i += 1
        
        return result
    
    def draw(self, text, x=0, y=0, text_color=color.white, parent=None, origin=(0, 0), size=None, text_origin=0.0):
        if size is None:
            size = self.size
        entities = []
        container = self._draw_internal(text, x, y, text_color, False, parent, origin, size, text_origin)
        if container:
            entities.append(container)
        return entities
    
    def draw_shadow(self, text, x=0, y=0, text_color=color.white, parent=None, origin=(0, 0), size=None, text_origin=0.0):
        if size is None:
            size = self.size
        entities = []
        
        pixel_size = 0.01 * size
        
        shadow_container = self._draw_internal(text, x + pixel_size, y - pixel_size, text_color, True, parent, origin, size, text_origin)
        if shadow_container:
            entities.append(shadow_container)
            
        main_container = self._draw_internal(text, x, y, text_color, False, parent, origin, size, text_origin)
        if main_container:
            entities.append(main_container)
        
        return entities
    
    def _draw_internal(self, text, x, y, text_color, darken, parent, origin=(0, 0), size=1.0, text_origin=0.0):
        if parent is None:
            parent = camera.ui
        
        # Парсим цветовые коды
        parsed_chars = self._parse_color_codes(text)
        
        if not parsed_chars:
            return None
        
        # Вычисляем размеры текста с учетом масштаба
        text_width = self.width(text) * 0.01 * size
        text_height = self.char_height * 0.01 * size
        
        # Применяем origin для вертикального позиционирования
        # И text_origin для горизонтального центрирования
        adjusted_x = x - text_origin * text_width - origin[0] * text_width
        adjusted_y = y + origin[1] * text_height
        
        # Создаем контейнер для всего текста
        text_container = Entity(parent=parent, position=(adjusted_x, adjusted_y, 0))
        
        x_offset = 0
        pixel_scale = 0.01 * size  # Масштабируем размер пикселя
        
        for idx, (char, char_color) in enumerate(parsed_chars):
            if ord(char) < 128:
                # Применяем затемнение для тени
                final_color = char_color
                if darken:
                    final_color = color.rgba(
                        char_color.r * 0.25,
                        char_color.g * 0.25,
                        char_color.b * 0.25,
                        char_color.a
                    )
                
                char_width = self.char_widths[ord(char)]
                
                # Вычисляем отступ для этого символа
                extra_spacing = (char_width * (self.char_spacing - 1.0))
                half_spacing = extra_spacing / 2.0
                
                # Добавляем половину отступа ПЕРЕД символом (кроме самого первого)
                if idx > 0:
                    x_offset += half_spacing
                
                # Если это пробел, просто добавляем смещение
                if char == ' ':
                    x_offset += char_width
                    x_offset += half_spacing
                    continue
                
                # Создаем mesh для символа
                char_mesh = self._create_char_quad(char)
                if char_mesh:
                    # Создаем Entity для символа с масштабированным размером
                    char_entity = Entity(
                        parent=text_container,
                        model=char_mesh,
                        texture=self.atlas,
                        position=(x_offset * pixel_scale, 0, 0),
                        scale=(8 * pixel_scale, 8 * pixel_scale, 1),
                        color=final_color
                    )
                
                # Смещаемся на базовую ширину символа
                x_offset += char_width
                x_offset += half_spacing
        
        return text_container
    
    def width(self, text):
        parsed_chars = self._parse_color_codes(text)
        total_width = 0
        
        for char, _ in parsed_chars:
            if ord(char) < 128:
                total_width += self.char_widths[ord(char)]
        
        return total_width

