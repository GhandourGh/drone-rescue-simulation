"""
Parallel Track Search Algorithm
Systematic back-and-forth coverage pattern for maximum area coverage
"""


class ParallelTrackSearch:
    """
    Moves in straight lines, turning at boundaries like a lawnmower.
    Navigates around obstacles intelligently.
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
        # Obstacle avoidance state
        self.in_avoidance = False
        self.original_row = None
        self.avoidance_step = 0  # 1=forward, 2=up

    def get_next_position(self, current_position):
        """
        Calculate next position, intelligently avoiding obstacles.
        Pattern: right/left, down (if obstacle), right/left, up, right/left
        """
        self.attempt_count += 1
        if self.attempt_count > 1000:  # Safety limit
            return None

        row, col = current_position
        rows, cols = self.grid_size

        # Handle obstacle avoidance state machine
        if self.in_avoidance:
            return self._handle_avoidance(row, col)

        # Normal lawnmower pattern
        if self.direction == 'right':
            # Try moving right
            if col + 1 < cols:
                next_pos = (row, col + 1)
                if self._is_position_valid(next_pos):
                    return next_pos
                else:
                    # Hit an obstacle, initiate avoidance
                    return self._initiate_avoidance(row, col, 'right')
            # Reached right boundary, move to next row
            self.direction = 'left'
            if row + 1 < rows:
                next_pos = (row + 1, col)
                if self._is_position_valid(next_pos):
                    return next_pos
                return self._find_valid_position_in_row(row + 1, col, 'left')
            return None

        else:  # direction == 'left'
            # Try moving left
            if col - 1 >= 0:
                next_pos = (row, col - 1)
                if self._is_position_valid(next_pos):
                    return next_pos
                else:
                    # Hit an obstacle, initiate avoidance
                    return self._initiate_avoidance(row, col, 'left')
            # Reached left boundary, move to next row
            self.direction = 'right'
            if row + 1 < rows:
                next_pos = (row + 1, col)
                if self._is_position_valid(next_pos):
                    return next_pos
                return self._find_valid_position_in_row(row + 1, col, 'right')
            return None

    def _initiate_avoidance(self, row, col, direction):
        """
        Start obstacle avoidance maneuver.
        Step 1: Go down
        """
        rows, cols = self.grid_size
        
        # Try to go down
        if row + 1 < rows and self._is_position_valid((row + 1, col)):
            self.in_avoidance = True
            self.original_row = row
            self.avoidance_step = 1  # Next step: move forward
            return (row + 1, col)
        
        # Can't go down, give up on this row and move to next
        if direction == 'right':
            self.direction = 'left'
        else:
            self.direction = 'right'
        
        if row + 1 < rows:
            return self._find_valid_position_in_row(row + 1, col, self.direction)
        return None

    def _handle_avoidance(self, row, col):
        """
        Handle obstacle avoidance state machine.
        Step 1 (avoidance_step=1): Try to move forward (right or left)
        Step 2 (avoidance_step=2): Try to move up to original row
        """
        rows, cols = self.grid_size
        
        if self.avoidance_step == 1:
            # Try to move in the current direction
            if self.direction == 'right':
                if col + 1 < cols and self._is_position_valid((row, col + 1)):
                    self.avoidance_step = 2  # Next: try to go up
                    return (row, col + 1)
                # Can't move right, stay in step 1 and go down more
                if row + 1 < rows and self._is_position_valid((row + 1, col)):
                    return (row + 1, col)
                # Can't proceed, abandon avoidance
                self._abandon_avoidance()
                return self.get_next_position((row, col))
            else:  # direction == 'left'
                if col - 1 >= 0 and self._is_position_valid((row, col - 1)):
                    self.avoidance_step = 2  # Next: try to go up
                    return (row, col - 1)
                # Can't move left, stay in step 1 and go down more
                if row + 1 < rows and self._is_position_valid((row + 1, col)):
                    return (row + 1, col)
                # Can't proceed, abandon avoidance
                self._abandon_avoidance()
                return self.get_next_position((row, col))
        
        elif self.avoidance_step == 2:
            # Try to move up towards original row
            if row > self.original_row:
                if self._is_position_valid((row - 1, col)):
                    # Keep trying to go up
                    if row - 1 == self.original_row:
                        # Back at original row, complete avoidance
                        self._complete_avoidance()
                    return (row - 1, col)
                else:
                    # Can't go up, try to continue in current direction instead
                    self.avoidance_step = 1  # Go back to forward movement
                    return self._handle_avoidance(row, col)
            else:
                # Already at or above original row, complete avoidance
                self._complete_avoidance()
                return self.get_next_position((row, col))
        
        # Shouldn't reach here
        self._abandon_avoidance()
        return self.get_next_position((row, col))

    def _complete_avoidance(self):
        """Successfully completed obstacle avoidance."""
        self.in_avoidance = False
        self.original_row = None
        self.avoidance_step = 0

    def _abandon_avoidance(self):
        """Abandon obstacle avoidance and move to next row."""
        self.in_avoidance = False
        self.original_row = None
        self.avoidance_step = 0
        # Switch direction for next row
        self.direction = 'left' if self.direction == 'right' else 'right'

    def _find_valid_position_in_row(self, row, start_col, direction):
        """
        Find a valid position in the specified row, searching from start_col.
        """
        rows, cols = self.grid_size
        
        if row >= rows:
            return None
        
        # Limit search depth to prevent excessive recursion
        max_rows_to_search = min(5, rows - row)
        for row_offset in range(max_rows_to_search):
            current_row = row + row_offset
            if current_row >= rows:
                break
            
            # Try the start column first
            if self._is_position_valid((current_row, start_col)):
                return (current_row, start_col)
            
            # Search in the direction we're moving
            if direction == 'right':
                for col in range(start_col + 1, cols):
                    if self._is_position_valid((current_row, col)):
                        return (current_row, col)
                # No valid position found going right, try left
                for col in range(start_col - 1, -1, -1):
                    if self._is_position_valid((current_row, col)):
                        return (current_row, col)
            else:  # direction == 'left'
                for col in range(start_col - 1, -1, -1):
                    if self._is_position_valid((current_row, col)):
                        return (current_row, col)
                # No valid position found going left, try right
                for col in range(start_col + 1, cols):
                    if self._is_position_valid((current_row, col)):
                        return (current_row, col)
        
        # No valid position found within search range
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


