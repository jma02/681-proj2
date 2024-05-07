from typing import List, Dict, Tuple, Union
import copy
from constraints.sudoku_constraint9x9 import boxes_9x9, boxes_9x9_reversed, constraint9x9, constraint9x9_queue

class SudokuCSP:
    def __init__(self, variables: Dict):
        self.variables = variables 

def create_variables(board: List[List[int]]) -> Dict:
    n = len(board[0])
    return {
        int(f'{i}{j}'): [board[i - 1][j - 1]] if board[i - 1][j - 1] else list(range(1, n + 1))
        for i in range(1, n + 1)
        for j in range(1, n + 1)
    }

def revise(csp: SudokuCSP, x: int, y: int) -> bool:
    removed = False
    if (x,y) in constraint9x9:
        domain = copy.deepcopy(csp.variables[x])
        for val_x in domain:
            ok = False
            for val_y in csp.variables[y]:
                if val_x != val_y:
                    ok = True
                    break
            if not ok:
                csp.variables[x] = list(filter(lambda x: x != val_x, csp.variables[x]))
                removed = True
    return removed

def add_neighbor_arcs(x: int, y: int, queue: List[Tuple[int,int]]) -> None:
    for i in range(1,10):
        col_neighbor = int(f'{i}{x%10}')
        row_neighbor = int(f'{x//10}{i}')
        if col_neighbor != y and col_neighbor != x:
            queue.append((col_neighbor, x))
        if row_neighbor != y and row_neighbor != x:
            queue.append((row_neighbor, x))
    for box_neighbor in boxes_9x9[boxes_9x9_reversed[x]]:
        if box_neighbor != x and box_neighbor != y:
            queue.append((box_neighbor, x))

def find_neighbor_arcs(csp: SudokuCSP, x: int) -> List[Tuple[int,int]]:
    ret = []
    for i in range(1,10):
        col_neighbor = int(f'{i}{x%10}')
        row_neighbor = int(f'{x//10}{i}')
        if row_neighbor != x and len(csp.variables[row_neighbor]) > 1:
            ret.append((row_neighbor, x))
        if col_neighbor != x and len(csp.variables[col_neighbor]) > 1:
            ret.append((col_neighbor, x))
    for box_neighbor in boxes_9x9[boxes_9x9_reversed[x]]:
        if box_neighbor != x and len(csp.variables[box_neighbor]) > 1:
            ret.append((box_neighbor, x))
    return ret



def ac3(csp: SudokuCSP, queue: List[Tuple[int,int]]) -> bool:
    while len(queue):
        x, y = queue.pop(0)
        if(revise(csp, x, y)):
            if(len(csp.variables[x]) == 0):
                return False
            add_neighbor_arcs(x, y, queue)
    return True

def minimum_remaining_values(csp: SudokuCSP) -> int:
    return min(list(filter(lambda x: len(x[1]) > 1, csp.variables.items())), key=lambda x: len(x[1]))

def backtracking_search(csp: SudokuCSP) -> Union[bool, Tuple[Dict, Dict, List[Tuple[int,int]], List[Tuple[int,int]]]]:
    failed = {}
    queue = copy.deepcopy(constraint9x9_queue)
    initial_variables = copy.deepcopy(csp.variables)
    if not ac3(csp, queue):
        return False

    assignments = [(x, True) for x in filter(lambda x: len(x[1]) == 1 and len(initial_variables[x[0]]) > 1, csp.variables.items())]
    # Special case if initial AC3 solves board
    if len(list(filter(lambda x : len(x[1]) > 1, csp.variables.items()))) == 0:
        return csp.variables, [], assignments, []

    result = backtrack(csp, copy.deepcopy(assignments), [], failed)
    
    if result:
        variables, intermediate_domains, assignments = result
        return variables, intermediate_domains, assignments, failed
    else:
        return result


# Perform AC3 before first call
def backtrack(csp: SudokuCSP, 
              assignment: List[Tuple[Tuple[int, int], bool]], 
              intermediate_domains:List[Dict],
              failed: dict) -> Union[bool, Tuple[Dict, Dict, List[Tuple[int,int]]]]:
    if len(list(filter(lambda x : len(x[1]) > 1, csp.variables.items()))) == 0:
        return csp.variables, intermediate_domains, assignment
    next_var, next_var_domain = minimum_remaining_values(csp)
    for value in next_var_domain:
        assignment.append(((next_var, [value]), True))
        next_csp = SudokuCSP(copy.deepcopy(csp.variables))
        next_csp.variables[next_var] = [value]
        # For visualization
        copy_next_csp = copy.deepcopy(next_csp.variables)
        consistent = ac3(next_csp, find_neighbor_arcs(next_csp, next_var))
        intermediate_domains.append(next_csp.variables)
        for var, domain in next_csp.variables.items():
            if len(domain) == 1 and len(copy_next_csp[var]) > 1:
                assignment.append(((var,domain), False))
        # After MAC, we should have an updated list of assignments
        if consistent:
            result = backtrack(next_csp, assignment, intermediate_domains, failed)
            if result:
                return result
        # For visualization
        ok = False
        guessed = None
        while not ok:
            guessed, ok = assignment.pop()
        var, val = guessed
        failed.setdefault(var, []).append(val)
        intermediate_domains.pop()
    return False
