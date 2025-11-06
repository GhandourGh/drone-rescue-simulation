class ParallelTrackSearch:
    def __init__(self, grid_size, start_position, environment=None, drone=None):
        self.drone = drone
        self.environment = environment
        self.grid_size = grid_size

    def get_next_position(self, current_position):
        """Waypoint-only navigation"""
        return self.drone.get_next_waypoint_position(current_position)

    def _is_position_valid(self, position):
        if self.environment:
            return self.environment.is_valid_position(position)
        row, col = position
        rows, cols = self.grid_size
        return 0 <= row < rows and 0 <= col < cols



