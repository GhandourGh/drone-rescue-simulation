


class RescueDrone:
    """ This class represents the drone position, battery, found targets and path history"""
    def __init__(self, start_position=(0,0), battery=100):
        self.distance = 0
        self.position = start_position # drone current position on the grid
        self.battery = battery # Initial drone battery (mission duration limit)
        self.found_targets = [] # Empty list to store found targets - to be filled during the mission
        self.path_history = [start_position] # Track every position of the drone for path analysis (Start at initial position)


    def move_to(self, new_position):
        """Move the drone to new grid position and updates all tracking systems
           This is the core navigation method for the drone
            Arg: new_position (tuple): Target coordinates(row, col) to move to
            Returns: bool: Success statues of the movement operation
        """

        old_row, old_col = self.position
        new_row, new_col = new_position
        distance = abs(new_row - old_row) + abs(new_col - old_col)

        self.position = new_position
        self.path_history.append(new_position)
        self.distance = distance

        battery_remaining = round(self.battery - self.distance / 12)
        battery_drained = round(self.distance / 12)
        self.battery = battery_remaining

        print(f"🚁 Drone moved from ({old_row},{old_col}) to {new_position} (distance: {distance})")
        print(f"🔋 Battery drained: {battery_drained} units, Remaining: {battery_remaining} units")


        return True# Indicating successful movement (will add validation later)

    def scan_area(self):
        """
        Stimulate the drones scanning procedure around current position
        Uses sensors to detect targets
        """
        print(f"Scanning area: {self.position}")

        return [] # return empty for now = will implement actual target detection later

    def get_status(self):
        """
        generate statue report of drones current state
        """
        return{ #retun dictionary will all critical drone metrics
            'Position': self.position, #cirrent coordinates (Key: Position) (Value: whatever self.position is)
            'battery': f"{self.battery} units left", # Remaining time
            'targets_found': len(self.found_targets), # success metric
            'distance_traveled': len(self.path_history) - 1 # Path efficiency
        }



