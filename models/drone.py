class RescueDrone:
    """Autonomous drone for waypoint navigation and target rescue operations"""

    def __init__(self, start_position=(0, 0), battery=200):
        self.position = start_position
        self.battery = battery
        self.path_history = [start_position]
        self.found_targets = []
        self.waypoints = []
        self.current_waypoint_index = 0
        self.total_distance = 0

    def move_to(self, new_position):
        """Move drone to new grid position and update tracking metrics"""
        old_row, old_col = self.position
        new_row, new_col = new_position

        distance = abs(new_row - old_row) + abs(new_col - old_col)
        self.position = new_position
        self.path_history.append(new_position)
        self.total_distance += distance
        self.battery -= distance

        print(f"🚁 Moved to {new_position} | Battery: {self.battery}")
        return True

    def scan_area(self, environment):
        """Scan current position for targets and collect if found"""
        if environment.has_target(self.position):
            print(f"🎯 Target found at {self.position}")
            self.found_targets.append(self.position)
            environment.remove_target(self.position)
            return True
        return False

    def check_battery_status(self):
        """Return current battery status level"""
        if self.battery <= 0:
            return "dead"
        elif self.battery <= 20:
            return "critical"
        elif self.battery <= 50:
            return "low"
        else:
            return "normal"

    def set_waypoints(self, waypoint_list):
        """Assign waypoints for navigation mission"""
        self.waypoints = [wp['position'] for wp in waypoint_list]

    def get_next_waypoint_position(self, current_position):
        """Calculate next position toward current waypoint"""
        if self.current_waypoint_index >= len(self.waypoints):
            print("✅ Mission complete - all waypoints visited")
            return None

        target = self.waypoints[self.current_waypoint_index]

        # Advance to next waypoint if current reached
        if current_position == target:
            print(f"📍 Reached waypoint {self.current_waypoint_index + 1}")
            self.current_waypoint_index += 1
            return self.get_next_waypoint_position(current_position)

        # Move one step toward target waypoint
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
        """Return current drone status metrics"""
        return {
            'Position': self.position,
            'Battery': self.battery,
            'Targets Found': len(self.found_targets),
            'Distance Traveled': self.total_distance
        }





