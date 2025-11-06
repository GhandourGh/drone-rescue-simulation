class SimulationEngine:
    """Controls the simulation execution and mission progress"""

    def __init__(self, drones, environment, navigators):
        self.drones = drones if isinstance(drones, list) else [drones]
        self.environment = environment
        self.navigators = navigators if isinstance(navigators, list) else [navigators]
        self.mission_completed = False
        self.step_count = 0

    def run_step(self):
        """Execute one simulation step for all drones"""
        self.step_count += 1
        all_drones_completed = True
        any_drone_moved = False

        # Process each drone
        for i, drone in enumerate(self.drones):
            navigator = self.navigators[i]

            next_position = navigator.get_next_position(drone.position)

            if next_position is None:
                print(f"✅ Drone {drone.drone_id} completed its mission")
                continue  # This drone is done, but others might still be working

            all_drones_completed = False  # At least one drone still working

            if self.environment.is_valid_position(next_position):
                drone.move_to(next_position)
                drone.scan_area(self.environment)
                any_drone_moved = True

                if drone.check_battery_status() == "critical":
                    print(f"🔋 Drone {drone.drone_id} critical battery - mission terminated")
                    # Don't set mission_completed=True yet - other drones may continue
            else:
                # Drone tried to move to invalid position, but still active
                any_drone_moved = True

        # Mission complete only when ALL drones are done
        if all_drones_completed:
            print("✅ All drones completed mission")
            self.mission_completed = True
            return False

        return any_drone_moved  # Continue if any drone is still active

    def get_mission_stats(self):
        """Return current mission statistics"""
        total_targets_found = sum(len(drone.found_targets) for drone in self.drones)
        total_battery = sum(drone.battery for drone in self.drones)

        return {
            'steps': self.step_count,
            'targets_found': total_targets_found,
            'targets_remaining': len(self.environment.targets),
            'battery_remaining': total_battery,
            'mission_completed': self.mission_completed,
            'active_drones': len([d for d in self.drones if d.battery > 0])
        }