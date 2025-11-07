import numpy as np


class RescueDrone:
    """Autonomous drone for waypoint navigation and target rescue operations"""

    def __init__(self, start_position=(0, 0), battery=2000, drone_id=1, color='blue'):
        self.drone_id = drone_id
        self.color = color
        self.position = start_position  # Keep as tuple
        self.battery = battery
        self.path_history = [start_position]
        self.found_targets = []
        self.waypoints = []
        self.current_waypoint_index = 0
        self.total_distance = 0

    def move_to(self, new_position):
        """Move drone to new grid position and update tracking metrics"""
        # Convert to numpy arrays for calculation
        old_pos = np.array(self.position)
        new_pos = np.array(new_position)

        # Calculate Manhattan distance using NumPy
        distance = int(np.sum(np.abs(new_pos - old_pos)))  # Convert back to int

        self.position = new_position  # Store as tuple
        self.path_history.append(new_position)
        self.total_distance += distance
        self.battery -= distance

        print(f"🚁 Drone {self.drone_id} moved to {new_position} | Battery: {self.battery}")
        return True

    def scan_area(self, environment):
        """Scan current position for targets and collect if found"""
        if environment.has_target(self.position):
            print(f"🎯 Drone {self.drone_id} found target at {self.position}")
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
        self.waypoints = [wp['position'] for wp in waypoint_list]  # Keep as tuples

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

        # Convert to numpy arrays for direction calculation
        current_pos = np.array(current_position)
        target_pos = np.array(target)

        # Move one step toward target waypoint using NumPy
        direction = np.sign(target_pos - current_pos)

        # Handle the case where one coordinate is already at target
        if direction[0] == 0 and direction[1] == 0:
            return current_position  # Already at target

        # Move in the first non-zero direction (prioritize row movement)
        if direction[0] != 0:
            next_pos = current_pos + np.array([direction[0], 0])
        else:
            next_pos = current_pos + np.array([0, direction[1]])

        return tuple(next_pos.astype(int))  # Convert back to tuple

    def get_status(self):
        """Return current drone status metrics"""
        return {
            'Drone Id': self.drone_id,
            'Position': self.position,
            'Battery': self.battery,
            'Targets Found': len(self.found_targets),
            'Distance Traveled': self.total_distance
        }

    # Bonus: NumPy utility methods (optional)
    def distance_to_target(self, target_position):
        """Calculate Manhattan distance to a target position"""
        current_pos = np.array(self.position)
        target_pos = np.array(target_position)
        return int(np.sum(np.abs(target_pos - current_pos)))

    def get_neighbors(self):
        """Get all valid neighboring positions (useful for pathfinding)"""
        current_pos = np.array(self.position)
        directions = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])
        neighbors = current_pos + directions
        return [tuple(pos) for pos in neighbors]





