class SimulationEngine:
    """Controls the simulation execution and mission progress"""

    def __init__(self, drone, environment, navigator):
        self.drone = drone
        self.environment = environment
        self.navigator = navigator
        self.mission_completed = False
        self.step_count = 0

    def run_step(self):
        """Execute one simulation step"""
        self.step_count += 1

        next_position = self.navigator.get_next_position(self.drone.position)

        if next_position is None:
            print("✅ Mission complete")
            self.mission_completed = True
            return False

        if self.environment.is_valid_position(next_position):
            self.drone.move_to(next_position)
            self.drone.scan_area(self.environment)

            if self.drone.check_battery_status() == "critical":
                print("🔋 Critical battery - mission terminated")
                self.mission_completed = True
                return False

            return True
        else:
            return True  # Skip invalid positions

    def get_mission_stats(self):
        """Return current mission statistics"""
        return {
            'steps': self.step_count,
            'targets_found': len(self.drone.found_targets),
            'targets_remaining': len(self.environment.targets),
            'battery_remaining': self.drone.battery,
            'mission_completed': self.mission_completed
        }