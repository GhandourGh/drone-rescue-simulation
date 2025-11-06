"""
Parallel Track Search Algorithm
Systematic back-and-forth coverage pattern for maximum area coverage
"""


class ParallelTrackSearch:
    """
    Moves in straight lines, turning at boundaries like a lawnmower.
    """
    def __init__(self, grid_size, start_position, environment=None):
        """
        Initialize parallel track search pattern.

        Args:
            grid_size (tuple): (rows, cols) of search area
            start_position (tuple): (row, col) starting position
        """
        self.grid_size = grid_size
        self.current_position = start_position
        self.direction = 'right'  # Start moving right
        self.visited_positions = {start_position}
        self.environment = environment
        self.attempt_count = 0

    def get_next_position(self, current_position):
        """
        Calculate next position, avoiding obstacles.
        """
        self.attempt_count += 1
        if self.attempt_count > 100:  # Safety limit
            return None

        row, col = current_position
        rows, cols = self.grid_size

        if self.direction == 'right':
            # Try moving right
            if col + 1 < cols:
                next_pos = (row, col + 1)
                if self._is_position_valid(next_pos):
                    return next_pos
            # Hit right boundary or obstacle, try moving down
            self.direction = 'left'
            if row + 1 < rows:
                next_pos = (row + 1, col)
                if self._is_position_valid(next_pos):
                    return next_pos
            return None

        else:  # direction == 'left'
            # Try moving left
            if col - 1 >= 0:
                next_pos = (row, col - 1)
                if self._is_position_valid(next_pos):
                    return next_pos
            # Hit left boundary or obstacle, try moving down
            self.direction = 'right'
            if row + 1 < rows:
                next_pos = (row + 1, col)
                if self._is_position_valid(next_pos):
                    return next_pos
            return None

    def _is_position_valid(self, position):
        """
        Check if position is valid (within grid and not obstacle).
        """
        if self.environment:
            return self.environment.is_valid_position(position)
        else:
            # Fallback if no environment provided
            row, col = position
            rows, cols = self.grid_size
            return 0 <= row < rows and 0 <= col < cols


