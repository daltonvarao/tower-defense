INITIAL_POSITION = [
    [(75, 0),(75, 225),(225, 225)],
    [(25, 425),(75, 425),(75, 525)]
]

BASE_POSITIONS = [
    (225, 525),(425, 525),(425, 225),(475, 225),(475, 75),
    (675, 75),(675, 275),(625, 275),(625, 475),(675, 475),
    (675, 525),(825, 525),(825, 125),(1075, 125),(1075, 475)
]

def skull_positions(pos):
    return INITIAL_POSITION[pos] + BASE_POSITIONS
