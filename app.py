from flask import Flask, render_template, request, jsonify
from sudoku import backtracking_search, create_variables, SudokuCSP

app = Flask(__name__)

@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)

@app.route('/solve', methods=['POST'])
def solve():
    table_data = request.json
    sudoku_grid = []
    for i in range(1, 10):
        row = []
        for j in range(1, 10):
            cell_name = f"{i}{j}"
            cell_value = table_data.get(cell_name, '')
            if cell_value.strip():
                row.append(int(cell_value)) 
            else:
                row.append(0)
        sudoku_grid.append(row)
    result = backtracking_search(SudokuCSP(create_variables(sudoku_grid)))
    if result:
       variables, intermediate_domains, assignment, failed = result 
       return jsonify({
            'variables': variables,
            'intermediate_domains': intermediate_domains,
            'assignment': assignment,
            'failed': failed,
            'solvable': True,
        })
    else:
        return jsonify({
            'solvable': False
        })