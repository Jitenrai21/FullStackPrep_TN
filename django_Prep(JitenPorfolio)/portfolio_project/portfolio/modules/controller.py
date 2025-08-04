import pyautogui # Lets you move the mouse and simulate mouse clicks.
import time

class CursorController:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.last_click_time = 0
        self.click_cooldown = 1  # seconds

    def move_cursor_to_iris(self, iris_x_norm, iris_y_norm): # normalized coordinates of the detected iris position
        x = int(iris_x_norm * self.screen_width) 
        y = int(iris_y_norm * self.screen_height)
        pyautogui.moveTo(x, y, duration=0.05) # animates the movement over 50 milliseconds

    def click_if_wink(self, wink_type):
        now = time.time()
        if now - self.last_click_time < self.click_cooldown:
            return
        if wink_type == "left":
            pyautogui.click(button='left')
        elif wink_type == "right":
            pyautogui.click(button='right')
        self.last_click_time = now

# import pyautogui
# import time

# class CursorController:
#     DEFAULT_SMOOTHING = 0.2
#     DEFAULT_CLICK_COOLDOWN = 1.0
#     DEFAULT_SENSITIVITY = 1.0

#     def __init__(
#         self,
#         screen_width: int,
#         screen_height: int,
#         smoothing: float = DEFAULT_SMOOTHING,
#         click_cooldown: float = DEFAULT_CLICK_COOLDOWN,
#         sensitivity: float = DEFAULT_SENSITIVITY,
#         debug: bool = False,
#     ):
#         """
#         Controls the mouse cursor based on normalized iris coordinates and wink input.

#         Args:
#             screen_width (int): Width of the screen in pixels.
#             screen_height (int): Height of the screen in pixels.
#             smoothing (float): How much to smooth cursor movement [0,1]. 0 = no smoothing, 1 = no movement.
#             click_cooldown (float): Minimum time in seconds between clicks.
#             sensitivity (float): Multiplier for cursor movement speed.
#             debug (bool): If True, print debug info.
#         """
#         self.screen_width = screen_width
#         self.screen_height = screen_height
#         self.smoothing = max(0.0, min(smoothing, 1.0))
#         self.click_cooldown = max(0.0, click_cooldown)
#         self.sensitivity = max(0.1, sensitivity)  # prevent zero or negative sensitivity
#         self.debug = debug

#         self.last_click_time = 0.0
#         self.last_x = screen_width // 2
#         self.last_y = screen_height // 2

#     def move_cursor_to_iris(self, iris_x_norm: float, iris_y_norm: float) -> None:
#         """
#         Moves the mouse cursor based on normalized iris coordinates with smoothing and sensitivity.

#         Args:
#             iris_x_norm (float): Normalized iris x-coordinate [0, 1].
#             iris_y_norm (float): Normalized iris y-coordinate [0, 1].

#         Returns:
#             None
#         """
#         # Sanity check: ignore obviously invalid coordinates (like exactly 1.0 or out of bounds)
#         if not (0.0 <= iris_x_norm <= 1.0) or not (0.0 <= iris_y_norm <= 1.0):
#             if self.debug:
#                 print(f"Warning: Ignoring out-of-bounds iris coordinates: ({iris_x_norm}, {iris_y_norm})")
#             return
#         # Optional: ignore exact edges to avoid fail-safe triggers
#         if iris_x_norm >= 0.99:
#             iris_x_norm = 0.99
#         if iris_y_norm >= 0.99:
#             iris_y_norm = 0.99

#         # Apply sensitivity and clamp between 0 and 1
#         iris_x_norm = min(iris_x_norm * self.sensitivity, 1.0)
#         iris_y_norm = min(iris_y_norm * self.sensitivity, 1.0)

#         # Calculate target screen coordinates
#         target_x = int(iris_x_norm * self.screen_width)
#         target_y = int(iris_y_norm * self.screen_height)

#         # Smooth movement: interpolate between last position and target
#         new_x = int(self.last_x + (target_x - self.last_x) * (1 - self.smoothing))
#         new_y = int(self.last_y + (target_y - self.last_y) * (1 - self.smoothing))

#         # Clamp final coordinates to screen bounds
#         new_x = max(0, min(new_x, self.screen_width - 1))
#         new_y = max(0, min(new_y, self.screen_height - 1))

#         if self.debug:
#             print(f"Normalized iris coords: ({iris_x_norm:.3f}, {iris_y_norm:.3f})")
#             print(f"Target coords before smoothing: ({target_x}, {target_y})")
#             print(f"Smoothed coords after clamp: ({new_x}, {new_y})")

#         # Move the cursor
#         pyautogui.moveTo(new_x, new_y, duration=0.05)

#         # Update last position
#         self.last_x, self.last_y = new_x, new_y

#     def click_if_wink(self, wink_type: str) -> None:
#         """
#         Simulate mouse clicks based on detected wink type with cooldown.

#         Args:
#             wink_type (str): "left" or "right" indicating which wink detected.

#         Returns:
#             None
#         """
#         now = time.time()
#         if now - self.last_click_time < self.click_cooldown:
#             return  # Ignore clicks too close to last click time

#         if wink_type == "left":
#             pyautogui.click(button="left")
#             if self.debug:
#                 print("Left wink detected: Left click performed.")
#         elif wink_type == "right":
#             pyautogui.click(button="right")
#             if self.debug:
#                 print("Right wink detected: Right click performed.")

#         self.last_click_time = now
