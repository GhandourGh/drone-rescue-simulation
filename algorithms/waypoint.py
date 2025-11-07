import numpy as np


class WaypointNavigator:
    """Handles drone navigation between waypoints with proper rectangle avoidance"""

    def __init__(self, grid_size, start_position, environment=None, drone=None):
        self.drone = drone
        self.environment = environment
        self.grid_size = grid_size
        self.rows, self.cols = grid_size
        self.bypass_route = []
        self.current_bypass_index = 0
        self.visited_positions = set()
        self.stuck_count = 0

    def get_next_position(self, current_position):
        """Get next position with proper NFZ avoidance"""
        # Track visited positions to detect loops
        self.visited_positions.add(current_position)
        if len(self.visited_positions) > 20:
            self.visited_positions = set([current_position])

        # If we're following a bypass route, continue it
        if self.bypass_route and self.current_bypass_index < len(self.bypass_route):
            next_pos = self.bypass_route[self.current_bypass_index]
            self.current_bypass_index += 1
            return next_pos

        # Get normal waypoint position
        next_pos = self.drone.get_next_waypoint_position(current_position)
        if next_pos is None:
            return None

        # Check if we're stuck (revisiting same positions)
        if next_pos in self.visited_positions:
            self.stuck_count += 1
            if self.stuck_count > 3:
                print("🔄 Detected stuck condition, using direct pathfinding")
                return self._get_direct_safe_path(current_position, next_pos)
        else:
            self.stuck_count = 0

        # Check if path is blocked by any NFZ
        if not self.environment.is_valid_position(next_pos):
            print(f"🚧 Path blocked to {next_pos}, calculating safe route...")
            safe_route = self._find_safe_route_to_waypoint(current_position)
            if safe_route:
                self.bypass_route = safe_route
                self.current_bypass_index = 1
                return safe_route[0]
            else:
                print("🚨 No safe route found, moving to next waypoint")
                self.drone.current_waypoint_index += 1
                return self.get_next_position(current_position)

        return next_pos

    def _find_safe_route_to_waypoint(self, current_position):
        """Find a complete safe route to the current waypoint"""
        if self.drone.current_waypoint_index >= len(self.drone.waypoints):
            return None

        target_waypoint = self.drone.waypoints[self.drone.current_waypoint_index]
        print(f"🎯 Finding safe route from {current_position} to waypoint {target_waypoint}")

        # Try different strategies to reach the waypoint
        strategies = [
            self._try_direct_approach,
            self._try_perimeter_approach,
            self._try_edge_approach,
            self._try_opposite_side_approach
        ]

        for strategy in strategies:
            route = strategy(current_position, target_waypoint)
            if route and self._is_route_valid(route):
                return route

        return None

    def _try_direct_approach(self, current_pos, target_pos):
        """Try to find a direct path avoiding NFZs - Optimized with NumPy"""
        route = []
        current = np.array(current_pos)  # Use NumPy for position math
        target = np.array(target_pos)

        while not np.array_equal(current, target):
            # Get all possible next moves using NumPy directions
            directions = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])
            possible_moves = [tuple(current + dir) for dir in directions]

            # Filter valid moves and prioritize moves toward target
            valid_moves = [move for move in possible_moves
                           if self._is_position_valid(move) and move not in route]

            if not valid_moves:
                break

            # Choose move that gets us closest to target using NumPy distance
            best_move = min(valid_moves,
                            key=lambda move: np.sum(np.abs(np.array(move) - target)))

            route.append(best_move)
            current = np.array(best_move)

            if len(route) > 20:
                break

        return route if np.array_equal(current, target) else []

    def _try_perimeter_approach(self, current_pos, target_pos):
        """Go around NFZs by following their perimeter"""
        route = []
        current = current_pos

        # Find all NFZs between current and target
        blocking_nfzs = []
        for nfz in self.environment.nfz_rectangles:
            if self._line_intersects_rectangle(current_pos, target_pos, nfz):
                blocking_nfzs.append(nfz)

        if not blocking_nfzs:
            return []

        # Use the largest blocking NFZ for perimeter routing
        main_nfz = max(blocking_nfzs,
                       key=lambda nfz: (nfz['bottom_right'][0] - nfz['top_left'][0]) *
                                       (nfz['bottom_right'][1] - nfz['top_left'][1]))

        top_row, left_col = main_nfz['top_left']
        bottom_row, right_col = main_nfz['bottom_right']

        # Determine which side to go around based on positions
        if current_pos[0] < top_row:  # Current is above NFZ
            # Go around the top
            waypoint = (top_row - 1, left_col - 1)
        elif current_pos[0] > bottom_row:  # Current is below NFZ
            # Go around the bottom
            waypoint = (bottom_row + 1, left_col - 1)
        elif current_pos[1] < left_col:  # Current is left of NFZ
            # Go around the left
            waypoint = (top_row - 1, left_col - 1)
        else:  # Current is right of NFZ
            # Go around the right
            waypoint = (top_row - 1, right_col + 1)

        # Build route to perimeter waypoint
        if self._is_position_valid(waypoint):
            route1 = self._build_direct_route(current_pos, waypoint)
            route2 = self._build_direct_route(waypoint, target_pos)
            if route1 and route2:
                return route1 + route2

        return []

    def _try_edge_approach(self, current_pos, target_pos):
        """Go to grid edges and then to target"""
        routes = []

        # Try top edge route
        top_route = self._build_direct_route(current_pos, (0, target_pos[1]))
        if top_route:
            final_route = self._build_direct_route(top_route[-1], target_pos)
            if final_route:
                routes.append(top_route + final_route)

        # Try bottom edge route
        bottom_route = self._build_direct_route(current_pos, (self.rows - 1, target_pos[1]))
        if bottom_route:
            final_route = self._build_direct_route(bottom_route[-1], target_pos)
            if final_route:
                routes.append(bottom_route + final_route)

        # Try left edge route
        left_route = self._build_direct_route(current_pos, (target_pos[0], 0))
        if left_route:
            final_route = self._build_direct_route(left_route[-1], target_pos)
            if final_route:
                routes.append(left_route + final_route)

        # Try right edge route
        right_route = self._build_direct_route(current_pos, (target_pos[0], self.cols - 1))
        if right_route:
            final_route = self._build_direct_route(right_route[-1], target_pos)
            if final_route:
                routes.append(right_route + final_route)

        # Return shortest valid route
        valid_routes = [r for r in routes if r and self._is_route_valid(r)]
        return min(valid_routes, key=len) if valid_routes else []

    def _try_opposite_side_approach(self, current_pos, target_pos):
        """Go to the opposite side of NFZs and approach from there"""
        # Find direction to target using NumPy
        current_arr = np.array(current_pos)
        target_arr = np.array(target_pos)
        direction = np.sign(target_arr - current_arr)

        # Try approaching from different angles
        approach_points = [
            (target_pos[0], current_pos[1]),  # Same column, target row
            (current_pos[0], target_pos[1]),  # Same row, target column
            (target_pos[0] + 2 * int(direction[0]), target_pos[1]),  # Beyond target row
            (target_pos[0], target_pos[1] + 2 * int(direction[1])),  # Beyond target column
        ]

        for approach_point in approach_points:
            if self._is_position_valid(approach_point):
                route1 = self._build_direct_route(current_pos, approach_point)
                route2 = self._build_direct_route(approach_point, target_pos)
                if route1 and route2 and self._is_route_valid(route1 + route2):
                    return route1 + route2

        return []

    def _build_direct_route(self, start, end):
        """Build a direct route between two points - Optimized with NumPy"""
        route = []
        current = np.array(start)
        target = np.array(end)

        while not np.array_equal(current, target):
            # Simple direction-based movement using NumPy
            direction = np.sign(target - current)

            # Handle case where we're aligned on one axis
            if direction[0] == 0 and direction[1] == 0:
                break

            if direction[0] != 0:
                next_pos = current + np.array([direction[0], 0])
            else:
                next_pos = current + np.array([0, direction[1]])

            next_pos_tuple = tuple(next_pos)

            if self._is_position_valid(next_pos_tuple):
                route.append(next_pos_tuple)
                current = next_pos
            else:
                break

            if len(route) > 30:
                break

        return route if np.array_equal(current, target) else []

    def _get_direct_safe_path(self, current_pos, target_pos):
        """Get a single safe move toward target - Optimized with NumPy"""
        current_arr = np.array(current_pos)
        target_arr = np.array(target_pos)

        possible_moves = [
            (current_pos[0] + 1, current_pos[1]),  # down
            (current_pos[0] - 1, current_pos[1]),  # up
            (current_pos[0], current_pos[1] + 1),  # right
            (current_pos[0], current_pos[1] - 1),  # left
        ]

        # Filter valid moves that make progress toward target
        valid_moves = [move for move in possible_moves
                       if self._is_position_valid(move)]

        if not valid_moves:
            # If no valid moves, try to move away to escape stuck situation
            escape_moves = [move for move in possible_moves
                            if 0 <= move[0] < self.rows and 0 <= move[1] < self.cols]
            return escape_moves[0] if escape_moves else current_pos

        # Choose move that minimizes distance to target using NumPy
        best_move = min(valid_moves,
                        key=lambda move: np.sum(np.abs(np.array(move) - target_arr)))

        return best_move

    def _line_intersects_rectangle(self, start, end, nfz):
        """Check if line from start to end intersects the NFZ rectangle"""
        start_row, start_col = start
        end_row, end_col = end
        top_row, left_col = nfz['top_left']
        bottom_row, right_col = nfz['bottom_right']

        # Check if either endpoint is inside rectangle
        if (top_row <= start_row <= bottom_row and left_col <= start_col <= right_col):
            return True
        if (top_row <= end_row <= bottom_row and left_col <= end_col <= right_col):
            return True

        return False

    def _is_route_valid(self, route):
        """Check if all positions in the route are valid"""
        if not route:
            return False
        for pos in route:
            if not self._is_position_valid(pos):
                return False
        return True

    def _is_position_valid(self, position):
        """Validate position is within grid and NFZ-free"""
        if self.environment:
            return self.environment.is_valid_position(position)

        row, col = position
        return 0 <= row < self.rows and 0 <= col < self.cols