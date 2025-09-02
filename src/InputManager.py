# input_manager.py (новый файл)

from pynput import keyboard
import threading

class InputManager:
    def __init__(self):
        self.held_keys = {}
        self._listener_thread = threading.Thread(target=self._run_listener, daemon=True)
        self._listener_thread.start()

    def _on_press(self, key):
        """Обработчик нажатия клавиши."""
        key_name = self._get_key_name(key)
        self.held_keys[key_name] = True

    def _on_release(self, key):
        """Обработчик отпускания клавиши."""
        key_name = self._get_key_name(key)
        if key_name in self.held_keys:
            del self.held_keys[key_name]

    def _get_key_name(self, key):
        """Получает унифицированное имя клавиши."""
        if isinstance(key, keyboard.KeyCode):
            return key.char
        elif isinstance(key, keyboard.Key):
            # Возвращаем имя спец. клавиши без префикса 'Key.'
            return key.name
        return None

    def _run_listener(self):
        """Запускает слушателя событий в этом потоке."""
        with keyboard.Listener(on_press=self._on_press, on_release=self._on_release) as listener:
            listener.join()

    def is_pressed(self, key_name):
        """
        Проверяет, нажата ли клавиша по ее имени ('w', 'a', 'space', etc.).
        Метод нечувствителен к регистру.
        """
        return key_name.lower() in self.held_keys

# Создаем глобальный экземпляр менеджера, который будет использоваться в игре
input_manager = InputManager()
