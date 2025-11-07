import numpy as np


class SearchEnvironment:
    """Manages the simulation environment including grid, targets, and No-Fly Zones"""

    def __init__(self, grid_size=(20, 20)):
        self.grid_size = grid_size
        self.rows, self.cols = grid_size

        # NumPy-optimized data structures
        self.nfz_mask = np.zeros(grid_size, dtype=bool)  # True where NFZs exist
        self.targets = []  # Keep as list for compatibility, but could use NumPy later

        # Backward compatibility
        self.nfz_rectangles = []  # Keep for reference, but use mask for calculations

    def add_target(self, position):
        """Add target to environment at specified position"""
        self.targets.append(position)

    def add_nfz_rectangle(self, nfz_data):
        """Add No-Fly Zone rectangle to environment and update NFZ mask"""
        # Add to list for backward compatibility
        self.nfz_rectangles.append(nfz_data)

        # Update NumPy mask for fast collision detection
        top_row, left_col = nfz_data['top_left']
        bottom_row, right_col = nfz_data['bottom_right']

        # Ensure bounds are within grid
        top_row = max(0, top_row)
        left_col = max(0, left_col)
        bottom_row = min(self.rows - 1, bottom_row)
        right_col = min(self.cols - 1, right_col)

        # Mark NFZ area in the mask
        self.nfz_mask[top_row:bottom_row + 1, left_col:right_col + 1] = True

    def is_valid_position(self, position):
        """Check if position is within grid bounds and not in any NFZ - O(1) with NumPy!"""
        row, col = position

        # Fast bounds checking
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False

        # Instant NFZ check using NumPy mask
        return not self.nfz_mask[row, col]

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
        return {
            'grid_size': f"{self.rows}x{self.cols}",
            'targets_remaining': len(self.targets),
            'nfz_count': len(self.nfz_rectangles),
            'nfz_coverage': f"{np.sum(self.nfz_mask) / (self.rows * self.cols) * 100:.1f}%"  # New stat!
        }

    # NEW: NumPy-powered utility methods
    def get_valid_neighbors(self, position):
        """Get all valid neighboring positions using NumPy"""
        row, col = position
        neighbors = [
            (row + 1, col),  # down
            (row - 1, col),  # up
            (row, col + 1),  # right
            (row, col - 1),  # left
        ]

        # Filter valid positions using NumPy-optimized check
        return [pos for pos in neighbors if self.is_valid_position(pos)]

    def distance_between(self, pos1, pos2):
        """Calculate Manhattan distance between two positions using NumPy"""
        pos1_arr = np.array(pos1)
        pos2_arr = np.array(pos2)
        return int(np.sum(np.abs(pos2_arr - pos1_arr)))

    def is_position_in_nfz(self, position):
        """Fast check if position is in any NFZ (useful for visualization)"""
        row, col = position
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.nfz_mask[row, col]
        return False

    def get_nfz_bounds(self):
        """Get bounding box of all NFZs (useful for path planning)"""
        if not np.any(self.nfz_mask):  # No NFZs
            return None

        # Find the bounds of all NFZ areas
        nfz_rows, nfz_cols = np.where(self.nfz_mask)
        if len(nfz_rows) == 0:
            return None

        return {
            'min_row': np.min(nfz_rows),
            'max_row': np.max(nfz_rows),
            'min_col': np.min(nfz_cols),
            'max_col': np.max(nfz_cols)
        }

    # Visualization helper
    def get_environment_grid(self):
        """Return a 2D grid representation for visualization"""
        grid = np.zeros(self.grid_size, dtype=int)  # 0 = empty

        # Mark NFZs as 1
        grid[self.nfz_mask] = 1

        # Mark targets as 2
        for target in self.targets:
            row, col = target
            if 0 <= row < self.rows and 0 <= col < self.cols:
                grid[row, col] = 2

        return grid



