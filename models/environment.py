class SearchEnvironment:
    """Manages the simulation environment including grid, targets, and No-Fly Zones"""

    def __init__(self, grid_size=(20, 20)):
        self.grid_size = grid_size
        self.targets = []
        self.nfz_rectangles = []  # Changed from obstacles to rectangles

    def add_target(self, position):
        """Add target to environment at specified position"""
        self.targets.append(position)

    def add_nfz_rectangle(self, nfz_data):
        """Add No-Fly Zone rectangle to environment"""
        self.nfz_rectangles.append(nfz_data)

    def is_valid_position(self, position):
        """Check if position is within grid bounds and not in any NFZ"""
        row, col = position
        rows, cols = self.grid_size

        # Check grid bounds
        if not (0 <= row < rows and 0 <= col < cols):
            return False

        # Check if position is inside any NFZ rectangle
        for nfz in self.nfz_rectangles:
            top_row, left_col = nfz['top_left']
            bottom_row, right_col = nfz['bottom_right']

            if (top_row <= row <= bottom_row and
                    left_col <= col <= right_col):
                return False

        return True

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
            'nfz_count': len(self.nfz_rectangles)
        }



