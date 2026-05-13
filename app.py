from flask import Flask, jsonify, request

app = Flask(__name__)

# Standardized to lowercase keys for consistency
students = [
    {'id': 1, 'name': 'Basil', 'grade': 'A'},
    {'id': 2, 'name': 'Yahya', 'grade': 'A'},
]
next_id = 3

@app.route('/api/students', methods=['GET'])
def get_students():
    return jsonify(students)

@app.route('/api/students/<int:s_id>', methods=['GET'])
def get_student(s_id):
    s = next((s for s in students if s['id'] == s_id), None)
    # Changed error code to 404 for 'Not Found'
    return (jsonify(s), 200) if s else (jsonify({'error': 'Not found'}), 404)

@app.route('/api/students', methods=['POST'])
def add_student():
    global next_id
    valid_grade = ['A','B','C','D','F']

    data = request.get_json()
    
    if not data or 'name' not in data or 'grade' not in data:
        return jsonify({'error': 'Data not complete'}), 400 # 400 is better for Bad Request

    if data['grade'].upper() not in valid_grade:
        return jsonify({'error' : 'Invalid grade'}) ,400
    new_student = {
        'id': next_id, 
        'name': data['name'], 
        'grade': data['grade']
    }
    students.append(new_student)
    next_id += 1

    return jsonify(new_student), 201 # 201 Created is standard for POST

@app.route('/api/students/count', methods = ['GET'])
def student_count():    
    return jsonify({"count" : len(students)}), 200

@app.route('/api/students/search' , methods=['GET'])
def search_students():
    grade_query = request.args.get('grade')
    if not grade_query:
        return jsonify({'error' : 'Provide a grade'}), 400
    filtered = [s for s in students if s.get('grade',' ').upper() == grade_query.upper()]
    return jsonify(filtered), 200

@app.route('/api/health' , methods = ['GET'])
def health_check():
    return jsonify({'status' : 'ok' , "message" : 'Flask is running'})
@app.route('/api/students/<int:s_id>', methods=['PUT'])
def update_student(s_id):
    # Fixed the '=' to '==' and ensured the variable name matches (s_id)
    s = next((s for s in students if s['id'] == s_id), None)
    
    if not s:
        return jsonify({'error': 'Not found'}), 404
        
    data = request.get_json()
    s['name'] = data.get('name', s['name'])
    s['grade'] = data.get('grade', s['grade'])    
    
    return jsonify(s), 200

@app.route('/api/students/<int:sid>', methods=['DELETE'])
def delete_students(sid):
    global students
    original_len = len(students)
    students = [s for s in students if s['id'] != sid]
    
    if len(students) == original_len:
        return jsonify({'error': 'Not found'}), 404
        
    return jsonify({'message': 'Deleted Successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True,host = '0.0.0.0', port=5000)
