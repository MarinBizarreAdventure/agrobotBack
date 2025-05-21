class Robot:
    def __init__(self, name: str):
        self.name = name
        self.position = (0, 0)  # Starting position at the origin
        self.battery_level = 100  # Battery level in percentage

    def move(self, x: int, y: int):
        if self.battery_level > 0:
            self.position = (x, y)
            self.battery_level -= 1  # Decrease battery level with each move
            print(
                f"{self.name} moved to {self.position}. Battery level: {self.battery_level}%"
            )
        else:
            print(f"{self.name} cannot move. Battery is empty.")

    def charge(self):
        self.battery_level = 100
        print(f"{self.name} is fully charged.")
