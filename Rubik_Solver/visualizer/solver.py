from typing import List, Optional, Tuple
import rubik

def apply_all_perms(position):
    """Apply all 6 basic permutations to a position."""
    perms = []
    perms.append((rubik.perm_apply(rubik.F, position), rubik.F))
    perms.append((rubik.perm_apply(rubik.Fi, position), rubik.Fi))
    perms.append((rubik.perm_apply(rubik.L, position), rubik.L))
    perms.append((rubik.perm_apply(rubik.Li, position), rubik.Li))
    perms.append((rubik.perm_apply(rubik.U, position), rubik.U))
    perms.append((rubik.perm_apply(rubik.Ui, position), rubik.Ui))
    return perms

def shortest_path(
        start: rubik.Position,
        end: rubik.Position,
) -> Optional[List[rubik.Permutation]]:
    """
    Using 2-way BFS, finds the shortest path from start to end.
    Returns a list of Permutations representing that shortest path.
    If there is no path to be found, return None instead of a list.
    """
    if start == end:
        return []
    
    # Queue stores (position, path_from_start)
    queue_start = [(start, [])]
    queue_end = [(end, [])]
    
    # Visited stores position -> path taken to reach it
    start_visited = {start: []}
    end_visited = {end: []}
    
    while queue_start or queue_end:
        # Expand from start
        if queue_start:
            current_pos, path = queue_start.pop(0)
            
            # Check if we've met the end search
            if current_pos in end_visited:
                # Reconstruct path: start_path + reverse(end_path with inverses)
                end_path = end_visited[current_pos]
                # Reverse the end path and invert the moves
                reversed_end = []
                for move in reversed(end_path):
                    # Find the inverse of the move
                    if move == rubik.F:
                        reversed_end.append(rubik.Fi)
                    elif move == rubik.Fi:
                        reversed_end.append(rubik.F)
                    elif move == rubik.L:
                        reversed_end.append(rubik.Li)
                    elif move == rubik.Li:
                        reversed_end.append(rubik.L)
                    elif move == rubik.U:
                        reversed_end.append(rubik.Ui)
                    elif move == rubik.Ui:
                        reversed_end.append(rubik.U)
                return path + reversed_end
            
            # Explore neighbors
            perms = apply_all_perms(current_pos)
            for new_pos, move in perms:
                if new_pos not in start_visited:
                    new_path = path + [move]
                    start_visited[new_pos] = new_path
                    queue_start.append((new_pos, new_path))
        
        # Expand from end
        if queue_end:
            current_pos, path = queue_end.pop(0)
            
            # Check if we've met the start search
            if current_pos in start_visited:
                # Reconstruct path
                start_path = start_visited[current_pos]
                reversed_end = []
                for move in reversed(path):
                    if move == rubik.F:
                        reversed_end.append(rubik.Fi)
                    elif move == rubik.Fi:
                        reversed_end.append(rubik.F)
                    elif move == rubik.L:
                        reversed_end.append(rubik.Li)
                    elif move == rubik.Li:
                        reversed_end.append(rubik.L)
                    elif move == rubik.U:
                        reversed_end.append(rubik.Ui)
                    elif move == rubik.Ui:
                        reversed_end.append(rubik.U)
                return start_path + reversed_end
            
            # Explore neighbors
            perms = apply_all_perms(current_pos)
            for new_pos, move in perms:
                if new_pos not in end_visited:
                    new_path = path + [move]
                    end_visited[new_pos] = new_path
                    queue_end.append((new_pos, new_path))
    
    return None