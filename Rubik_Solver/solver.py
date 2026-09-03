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
            if len(queue_start) > 100000:
                return None
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


def assert_good_path(start: rubik.Position, end: rubik.Position, path: List[rubik.Permutation]):
    """Verify that a path correctly transforms start to end."""
    current = start
    for move in path:
        current = rubik.perm_apply(move, current)
    assert current == end, f"Path does not lead from start to end"


if __name__ == "__main__":
    print("Running all tests...\n")
    
    # Test 0: Length 0 path
    print("Test 0: Length 0 path")
    start = rubik.I
    end = rubik.I
    ans = shortest_path(start, end)
    assert len(ans) == 0, f"Expected length 0, got {len(ans)}"
    print("✓ Test 0 passed\n")
    
    # Test 1: Length 1 path
    print("Test 1: Length 1 path")
    start = rubik.I
    end = rubik.perm_apply(rubik.F, start)
    ans = shortest_path(start, end)
    assert len(ans) == 1, f"Expected length 1, got {len(ans)}"
    assert ans == [rubik.F], f"Expected [F], got {ans}"
    print("✓ Test 1 passed\n")
    
    # Test 2: Length 2 path
    print("Test 2: Length 2 path")
    start = rubik.I
    middle = rubik.perm_apply(rubik.F, start)
    end = rubik.perm_apply(rubik.L, middle)
    ans = shortest_path(start, end)
    assert len(ans) == 2, f"Expected length 2, got {len(ans)}"
    assert ans == [rubik.F, rubik.L], f"Expected [F, L], got {ans}"
    print("✓ Test 2 passed\n")
    
    # Test 3: Length 3 path
    print("Test 3: Length 3 path")
    start = rubik.I
    middle1 = rubik.perm_apply(rubik.F, start)
    middle2 = rubik.perm_apply(rubik.F, middle1)
    end = rubik.perm_apply(rubik.Li, middle2)
    ans = shortest_path(start, end)
    assert len(ans) == 3, f"Expected length 3, got {len(ans)}"
    assert_good_path(start, end, ans)
    print("✓ Test 3 passed\n")
    
    # Test 4: Length 4 path
    print("Test 4: Length 4 path")
    start = rubik.I
    middle1 = rubik.perm_apply(rubik.F, start)
    middle2 = rubik.perm_apply(rubik.L, middle1)
    middle3 = rubik.perm_apply(rubik.F, middle2)
    end = rubik.perm_apply(rubik.L, middle3)
    ans = shortest_path(start, end)
    assert len(ans) == 4, f"Expected length 4, got {len(ans)}"
    assert_good_path(start, end, ans)
    print("✓ Test 4 passed\n")
    
    # Test 5: Length 14 path
    print("Test 5: Length 14 path (this may take a while...)")
    start = (6, 7, 8, 20, 18, 19, 3, 4, 5, 16, 17, 15, 0, 1, 2, 14, 12, 13, 10, 11, 9, 21, 22, 23)
    end = rubik.I
    ans = shortest_path(start, end)
    assert len(ans) == 14, f"Expected length 14, got {len(ans)}"
    assert_good_path(start, end, ans)
    print("✓ Test 5 passed\n")
    
    # Test 6: No solution (bad position)
    print("Test 6: No solution (invalid position)")
    start = (7, 8, 6, 20, 18, 19, 3, 4, 5, 16, 17, 15, 0, 1, 2, 14, 12, 13, 10, 11, 9, 21, 22, 23)
    end = rubik.I
    ans = shortest_path(start, end)
    assert ans is None, f"Expected None, got {ans}"
    print("✓ Test 6 passed\n")
    
    print("All tests passed! ✓")