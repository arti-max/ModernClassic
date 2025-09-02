class AABB:
    """
    Класс для работы с Axis-Aligned Bounding Box (ограничивающий параллелепипед).
    Используется для обнаружения столкновений и физических вычислений.
    """
    
    def __init__(self, min_x, min_y, min_z, max_x, max_y, max_z):
        """
        Конструктор ограничивающего параллелепипеда
        
        Args:
            min_x (float): Минимальная координата по оси X
            min_y (float): Минимальная координата по оси Y
            min_z (float): Минимальная координата по оси Z
            max_x (float): Максимальная координата по оси X
            max_y (float): Максимальная координата по оси Y
            max_z (float): Максимальная координата по оси Z
        """
        self.epsilon = 1e-6  # Исправлено: было 0.0F в оригинале
        
        self.min_x = min_x
        self.min_y = min_y
        self.min_z = min_z
        self.max_x = max_x
        self.max_y = max_y
        self.max_z = max_z
    
    def clone(self):
        """
        Копирует текущий объект ограничивающего параллелепипеда
        
        Returns:
            AABB: Клон ограничивающего параллелепипеда
        """
        return AABB(self.min_x, self.min_y, self.min_z, 
                   self.max_x, self.max_y, self.max_z)
    
    def expand(self, x, y, z):
        """
        Расширяет ограничивающий параллелепипед. Положительные и отрицательные числа 
        контролируют, какая сторона коробки должна расти.
        
        Args:
            x (float): Величина расширения для min_x или max_x
            y (float): Величина расширения для min_y или max_y  
            z (float): Величина расширения для min_z или max_z
            
        Returns:
            AABB: Расширенный ограничивающий параллелепипед
        """
        min_x = self.min_x
        min_y = self.min_y
        min_z = self.min_z
        max_x = self.max_x
        max_y = self.max_y
        max_z = self.max_z
        
        # Обработка расширения min/max по X
        if x < 0.0:
            min_x += x
        else:
            max_x += x
        
        # Обработка расширения min/max по Y
        if y < 0.0:
            min_y += y
        else:
            max_y += y
        
        # Обработка расширения min/max по Z
        if z < 0.0:
            min_z += z
        else:
            max_z += z
        
        # Создание нового ограничивающего параллелепипеда
        return AABB(min_x, min_y, min_z, max_x, max_y, max_z)
    
    def grow(self, x, y, z):
        """
        Расширяет ограничивающий параллелепипед с обеих сторон.
        Центр всегда фиксирован при использовании grow.
        
        Args:
            x (float): Величина расширения по оси X
            y (float): Величина расширения по оси Y
            z (float): Величина расширения по оси Z
            
        Returns:
            AABB: Расширенный ограничивающий параллелепипед
        """
        return AABB(self.min_x - x, self.min_y - y, self.min_z - z,
                   self.max_x + x, self.max_y + y, self.max_z + z)
    
    def clip_x_collide(self, other_bounding_box, x):
        """
        Проверка столкновения по оси X
        
        Args:
            other_bounding_box (AABB): Другой ограничивающий параллелепипед
            x (float): Позиция по оси X при столкновении
            
        Returns:
            float: Скорректированная позиция x после столкновения
        """
        # Проверяем столкновение по оси Y
        if (other_bounding_box.max_y <= self.min_y or 
            other_bounding_box.min_y >= self.max_y):
            return x
        
        # Проверяем столкновение по оси Z
        if (other_bounding_box.max_z <= self.min_z or 
            other_bounding_box.min_z >= self.max_z):
            return x
        
        # Проверка столкновения если ось X текущего блока больше
        if x > 0.0 and other_bounding_box.max_x <= self.min_x:
            max_val = self.min_x - other_bounding_box.max_x - self.epsilon
            if max_val < x:
                x = max_val
        
        # Проверка столкновения если ось X текущего блока меньше
        if x < 0.0 and other_bounding_box.min_x >= self.max_x:
            max_val = self.max_x - other_bounding_box.min_x + self.epsilon
            if max_val > x:
                x = max_val
        
        return x
    
    def clip_y_collide(self, other_bounding_box, y):
        """
        Проверка столкновения по оси Y
        
        Args:
            other_bounding_box (AABB): Другой ограничивающий параллелепипед
            y (float): Позиция по оси Y при столкновении
            
        Returns:
            float: Скорректированная позиция y после столкновения
        """
        # Проверяем столкновение по оси X
        if (other_bounding_box.max_x <= self.min_x or 
            other_bounding_box.min_x >= self.max_x):
            return y
        
        # Проверяем столкновение по оси Z
        if (other_bounding_box.max_z <= self.min_z or 
            other_bounding_box.min_z >= self.max_z):
            return y
        
        # Проверка столкновения если ось Y текущего блока больше
        if y > 0.0 and other_bounding_box.max_y <= self.min_y:
            max_val = self.min_y - other_bounding_box.max_y - self.epsilon
            if max_val < y:
                y = max_val
        
        # Проверка столкновения если ось Y текущего блока больше
        if y < 0.0 and other_bounding_box.min_y >= self.max_y:
            max_val = self.max_y - other_bounding_box.min_y + self.epsilon
            if max_val > y:
                y = max_val
        
        return y
    
    def clip_z_collide(self, other_bounding_box, z):
        """
        Проверка столкновения по оси Z
        
        Args:
            other_bounding_box (AABB): Другой ограничивающий параллелепипед
            z (float): Позиция по оси Z при столкновении
            
        Returns:
            float: Скорректированная позиция z после столкновения
        """
        # Проверяем столкновение по оси X
        if (other_bounding_box.max_x <= self.min_x or 
            other_bounding_box.min_x >= self.max_x):
            return z
        
        # Проверяем столкновение по оси Y
        if (other_bounding_box.max_y <= self.min_y or 
            other_bounding_box.min_y >= self.max_y):
            return z
        
        # Проверка столкновения если ось Z текущего блока больше
        if z > 0.0 and other_bounding_box.max_z <= self.min_z:
            max_val = self.min_z - other_bounding_box.max_z - self.epsilon
            if max_val < z:
                z = max_val
        
        # Проверка столкновения если ось Z текущего блока больше
        if z < 0.0 and other_bounding_box.min_z >= self.max_z:
            max_val = self.max_z - other_bounding_box.min_z + self.epsilon
            if max_val > z:
                z = max_val
        
        return z
    
    def intersects(self, other_bounding_box):
        """
        Проверяет, пересекаются ли два параллелепипеда
        
        Args:
            other_bounding_box (AABB): Другой ограничивающий параллелепипед
            
        Returns:
            bool: True, если параллелепипеды пересекаются
        """
        # Проверка по оси X
        if (other_bounding_box.max_x <= self.min_x or 
            other_bounding_box.min_x >= self.max_x):
            return False
        
        # Проверка по оси Y
        if (other_bounding_box.max_y <= self.min_y or 
            other_bounding_box.min_y >= self.max_y):
            return False
        
        # Проверка по оси Z
        return not (other_bounding_box.max_z <= self.min_z or 
                   other_bounding_box.min_z >= self.max_z)
    
    def move(self, x, y, z):
        """
        Перемещает ограничивающий параллелепипед относительно текущей позиции
        
        Args:
            x (float): Относительное смещение по X
            y (float): Относительное смещение по Y
            z (float): Относительное смещение по Z
        """
        self.min_x += x
        self.min_y += y
        self.min_z += z
        self.max_x += x
        self.max_y += y
        self.max_z += z
    
    def offset(self, x, y, z):
        """
        Создает новый ограничивающий параллелепипед с заданным смещением
        
        Args:
            x (float): Относительное смещение по X
            y (float): Относительное смещение по Y
            z (float): Относительное смещение по Z
            
        Returns:
            AABB: Новый ограничивающий параллелепипед со смещением
        """
        return AABB(self.min_x + x, self.min_y + y, self.min_z + z,
                   self.max_x + x, self.max_y + y, self.max_z + z)
    
    def __str__(self):
        """
        Строковое представление AABB для отладки
        
        Returns:
            str: Строковое представление координат
        """
        return (f"AABB[({self.min_x:.2f}, {self.min_y:.2f}, {self.min_z:.2f}) - "
                f"({self.max_x:.2f}, {self.max_y:.2f}, {self.max_z:.2f})]")
    
    def __repr__(self):
        """
        Представление объекта для разработчика
        
        Returns:
            str: Конструктор объекта
        """
        return (f"AABB({self.min_x}, {self.min_y}, {self.min_z}, "
                f"{self.max_x}, {self.max_y}, {self.max_z})")
