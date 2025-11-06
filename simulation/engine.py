"""
The Simulation Engine is the "brain" that controls everything:
Asks algorithm: "Where should the drone go next?"
Moves drone to that position
Scans for targets
Checks battery
Tracks progress
"""

class SimulationEngine:
    def __init__(self, drone, environment, search_algorithm):

        self.drone = drone
        self.environment = environment
        self.search_algorithm = search_algorithm
        self.mission_completed = False
        self.step_count = 0

    def run_step(self):
        self.step_count += 1

        # Get next position from search algorithm
        next_position = self.search_algorithm.get_next_position(self.drone.position)

        if next_position is None:
            print("🎯 MISSION COMPLETE: Entire area searched!")
            self.mission_completed = True
            return False

        # Move drone to next position
        if self.environment.is_valid_position(next_position):
            self.drone.move_to(next_position)

            # Scan for targets at new position
            self.drone.scan_area(self.environment)

            #Check battery Statues
            battery_status = self.drone.check_battery_status()
            if battery_status == "critical":
                print("🔋 CRITICAL BATTERY - Mission terminated!")
                self.mission_completed = True
                return False

            return True
        else:
            print(f"❌ Invalid position {next_position} - skipping")
            return True

    def get_mission_stats(self):
        return {
            'steps': self.step_count,
            'targets_found': len(self.drone.found_targets),
            'targets_remaining': len(self.environment.targets),
            'battery_remaining': self.drone.battery,
            'mission_completed': self.mission_completed,
        }