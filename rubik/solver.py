from typing import List
from typing import Optional

import rubik


def shortest_path(
        start: rubik.Position,
        end: rubik.Position,
) -> Optional[List[rubik.Permutation]]:
    """
    Using 2-way BFS, finds the shortest path from start to end.
    Returns a list of Permutations representing that shortest path.
    If there is no path to be found, return None instead of a list.

    You can use the rubik.quarter_twists move 6-tuple.
    Each move can be applied using rubik.perm_apply.
    """
    if start == end:
        return []

    start_configs = {}
    end_configs   = {}

    start_current_states = []
    end_current_states   = []
    
    start_configs.update( {start: () } )
    end_configs.update(   {end:   () } )

    start_current_states.append( start )
    end_current_states.append(    end  )

#     For loop 7 times
    start_new_states = []
    end_new_states   = []
#     Record past moves & current node for start
    for current in start_current_states:
        past_moves = start_configs.get(current)

        for move in rubik.quarter_twists:
            new_cube = rubik.perm_apply(move, current)
            current_moves = past_moves + tuple(move)

            # Saving the shortest path
            if new_cube not in start_configs:
                start_configs.update({new_cube: current_moves})
                start_new_states.append(new_cube)

            # Checking if we found and answer
            if new_cube in end_configs:
                start_list = start_configs.get(new_cube)
                inverted_list = tuple(map(rubik.perm_inverse, end_configs.get(new_cube)))
                return [start_list + inverted_list]


#     Record past moves & current nodes for end
    for current in end_current_states:
        past_moves = end_configs.get(end)

        for move in rubik.quarter_twists:
            new_cube = rubik.perm_apply(move, current)
            current_moves = past_moves + move

            # Saving the shortest path
            if new_cube not in end_configs:
                end_configs.update({new_cube: current_moves})
                end_new_states.append(new_cube)

            # Checking if we found and answer
            if new_cube in start_configs:
                start_list = start_configs.get(new_cube)
                print(end_configs.get(new_cube))
                inverted_list = tuple(map(rubik.perm_inverse, end_configs.get(new_cube)))
                return [start_list + inverted_list]

    # Make new states the current states

    raise NotImplementedError
