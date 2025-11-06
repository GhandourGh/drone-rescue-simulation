


class RescueDrone:
    """ This class represents the drone position, battery, found targets and path history"""
    def __init__(self, start_position=(0,0), battery=100):
        self.total_distance = 0
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
        self.total_distance += distance


        battery_drained = distance # 1 unit per cell
        self.battery -= battery_drained
        battery_remaining = self.battery

        print(f"🚁 Drone moved from ({old_row},{old_col}) to {new_position} (distance: {distance})")
        print(f"🔋 Battery drained: {battery_drained} unit/s, Remaining: {battery_remaining} units")


        return True# Indicating successful movement (will add validation later)

    def scan_area(self, environment):
        """
        Scan current position for targets and rescue them.
        """
        print(f"🔍 Scanning area at position {self.position}")

        if environment.has_target(self.position):
            print(f"🎯 TARGET FOUND at {self.position}!")
            self.found_targets.append(self.position)
            environment.remove_target(self.position)
            return True
        else:
            print("No targets found!")
            return False

    def check_battery_status(self):
        """
        Check battery status and return appropriate warning level.
        """
        if self.battery <= 0:
            return "dead ☠︎︎ "
        elif self.battery <= 20:
            return "critical ‼️"
        elif self.battery <= 50:
            return "low 🚨"
        else:
            return "normal"

    def return_to_base(self, base_position):
        """
        Emergency return to base when battery is critical.

        Args:
            base_position (tuple): (row, col) of home base

        Returns:
            bool: True if successful, False if not enough battery
        """
        distance_to_base = abs(self.position[0] - base_position[0]) + abs(self.position[1] - base_position[1])

        if distance_to_base > self.battery:
            print("❌ CRITICAL: Not enough battery to return to base!")
            return False

        print(f"🔋 CRITICAL BATTERY - RETURNING TO BASE {base_position}")
        self.move_to(base_position)
        return True



    def get_status(self):
        """
        generate statue report of drones current state
        """
        return{ #retun dictionary will all critical drone metrics
            'Position': self.position, #cirrent coordinates (Key: Position) (Value: whatever self.position is)
            'Battery': f"{self.battery} unit/s", # Remaining time
            'Targets Found': len(self.found_targets), # success metric
            'Total Distance Traveled': self.total_distance # Path efficiency
        }




