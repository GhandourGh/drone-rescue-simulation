class SearchEnvironment:
    """Manages the simulation environment including grid, targets, and obstacles"""

    def __init__(self, grid_size=(10, 10)):
        self.grid_size = grid_size  # (rows, columns)
        self.targets = []
        self.obstacles = []

    def add_target(self, position):
        """Add target to environment at specified position"""
        self.targets.append(position)

    def add_obstacle(self, position):
        """Add obstacle to environment at specified position"""
        self.obstacles.append(position)

    def is_valid_position(self, position):
        """Check if position is within grid bounds and not obstructed"""
        row, col = position
        rows, cols = self.grid_size

        return (0 <= row < rows and
                0 <= col < cols and
                position not in self.obstacles)

    def has_target(self, position):
        """Check if target exists at specified position"""
        return position in self.targets

    def remove_target(self, position):
        """Remove target from environment when collected"""
        if position in self.targets:
            self.targets.remove(position)
            return True
        return False

    def get_environment_stats(self):
        """Return environment statistics"""
        rows, cols = self.grid_size
        return {
            'grid_size': f"{rows}x{cols}",
            'targets_remaining': len(self.targets),
            'obstacles': len(self.obstacles)
        }


