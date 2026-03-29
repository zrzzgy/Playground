from collections import deque

# Numbers indexed 0-3 (representing numbers 1-4)
# Switch mappings (0-indexed switches, 0-indexed numbers)
SWITCHES = {
    0: [0, 2],       # Switch 1: numbers 1, 3
    1: [0, 3],       # Switch 2: numbers 1, 4
    2: [0, 1, 2],    # Switch 3: numbers 1, 2, 3
    3: [1, 2, 3],    # Switch 4: numbers 2, 3, 4
}

MIN_VAL, MAX_VAL = -2, 2
INITIAL = (0, 0, -1, 0)
GOAL = (0, 0, 0, 0)


def apply_switch_blocked(state, switch_idx, direction):
    """Blocked interpretation: entire move invalid if any affected number is at boundary."""
    affected = SWITCHES[switch_idx]
    for idx in affected:
        if direction == 1 and state[idx] == MAX_VAL:
            return None
        if direction == -1 and state[idx] == MIN_VAL:
            return None
    new_state = list(state)
    for idx in affected:
        new_state[idx] += direction
    return tuple(new_state)


def apply_switch_clamped(state, switch_idx, direction):
    """Clamped interpretation: numbers at boundary just stay put; others still move."""
    affected = SWITCHES[switch_idx]
    new_state = list(state)
    any_changed = False
    for idx in affected:
        if direction == 1 and state[idx] < MAX_VAL:
            new_state[idx] += 1
            any_changed = True
        elif direction == -1 and state[idx] > MIN_VAL:
            new_state[idx] -= 1
            any_changed = True
    return tuple(new_state) if any_changed else None


apply_switch = apply_switch_clamped  # try clamped interpretation first


def bfs():
    queue = deque([(INITIAL, [])])
    visited = {INITIAL}

    while queue:
        state, path = queue.popleft()

        if state == GOAL:
            return path

        for sw in range(4):
            for direction in (1, -1):
                new_state = apply_switch(state, sw, direction)
                if new_state is not None and new_state not in visited:
                    visited.add(new_state)
                    label = f"Switch {sw+1} {'(+1)' if direction == 1 else '(-1)'}"
                    queue.append((new_state, path + [(sw + 1, direction, label)]))

    return None


def simulate(path):
    state = tuple(INITIAL)
    print(f"Initial state: {list(state)}")
    for sw, direction, label in path:
        state = apply_switch(state, sw - 1, direction)
        print(f"  Apply {label}  -> {list(state)}")
    return state


solution = bfs()

if solution is None:
    print("No solution found.")
else:
    print(f"Solution found in {len(solution)} moves:\n")
    for i, (sw, direction, label) in enumerate(solution, 1):
        arrow = "+1" if direction == 1 else "-1"
        print(f"  Step {i}: {label}")
    print()
    final = simulate(solution)
    print(f"\nFinal state: {final} {'✓ SOLVED' if tuple(final) == GOAL else '✗ WRONG'}")
