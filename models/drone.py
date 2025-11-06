class RescueDrone:
    """This class represents the drone for waypoint navigation"""
    def __init__(self, start_position=(0,0), battery=200):
        self.total_distance = 0
        self.position = start_position
        self.battery = battery
        self.found_targets = []
        self.path_history = [start_position]
        self.waypoints = []
        self.current_waypoint_index = 0

    def move_to(self, new_position):
        old_row, old_col = self.position
        new_row, new_col = new_position
        distance = abs(new_row - old_row) + abs(new_col - old_col)

        self.position = new_position
        self.path_history.append(new_position)
        self.total_distance += distance

        battery_drained = distance
        self.battery -= battery_drained

        print(f"🚁 Drone moved from ({old_row},{old_col}) to {new_position} (distance: {distance})")
        print(f"🔋 Battery drained: {battery_drained} units, Remaining: {self.battery} units")
        return True

    def scan_area(self, environment):
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
        if self.battery <= 0:
            return "dead ☠︎︎ "
        elif self.battery <= 20:
            return "critical ‼️"
        elif self.battery <= 50:
            return "low 🚨"
        else:
            return "normal"

    def return_to_base(self, base_position):
        distance_to_base = abs(self.position[0] - base_position[0]) + abs(self.position[1] - base_position[1])

        if distance_to_base > self.battery:
            print("❌ CRITICAL: Not enough battery to return to base!")
            return False

        print(f"🔋 CRITICAL BATTERY - RETURNING TO BASE {base_position}")
        self.move_to(base_position)
        return True

    def set_waypoints(self, waypoint_list):
        self.waypoints = [wp['position'] for wp in waypoint_list]
        print(f"🎯 Drone assigned {len(self.waypoints)} waypoints")

    def get_next_waypoint_position(self, current_position):
        if self.current_waypoint_index >= len(self.waypoints):
            print("✅ All waypoints visited!")
            return None

        target = self.waypoints[self.current_waypoint_index]

        if current_position == target:
            print(f"🎯 Reached waypoint {self.current_waypoint_index + 1} at {target}")
            self.current_waypoint_index += 1
            return self.get_next_waypoint_position(current_position)

        current_row, current_col = current_position
        target_row, target_col = target

        if current_row < target_row:
            return current_row + 1, current_col
        elif current_row > target_row:
            return current_row - 1, current_col
        elif current_col < target_col:
            return current_row, current_col + 1
        elif current_col > target_col:
            return current_row, current_col - 1

        return current_position

    def get_status(self):
        return {
            'Position': self.position,
            'Battery': f"{self.battery} units",
            'Targets Found': len(self.found_targets),
            'Total Distance Traveled': self.total_distance
        }





