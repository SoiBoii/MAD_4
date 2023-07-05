from flask import Flask, render_template, request
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')

app = Flask(__name__)

def get_student_details(student_id):
    with open('data.csv', 'r') as file:
        lines = file.readlines()[1:]  # Exclude header line
        student_data = []
        total_marks = 0
        

        for line in lines:
            row = line.strip().split(',')
            if row[0] == student_id:
                student_data.append({
                    'student_id': row[0],
                    'course_id': row[1],
                    'marks': row[2]
                })
                total_marks += int(row[2])
                
        if total_marks==0 and student_data==[]:
            return render_template('error.html')
        return render_template('student_details.html', student_data=student_data, total_marks=total_marks)


def get_course_details(course_id):
    marks = []
    max_marks = 0
    total_marks = 0
    count = 0

    with open('data.csv', 'r') as file:
        lines = file.readlines()[1:]  # Exclude header line
        

        for line in lines:
            row = line.strip().split(',')
            if row[1] == course_id:
                marks.append(int(row[2]))
                total_marks+=int(row[2])
                count+=1
                if int(row[2])>max_marks:
                    max_marks=int(row[2])
    
    plt.hist(marks)
    plt.savefig("/home/sai/MAD_prac4/static/my_plot.png")


    if count > 0:
        average_marks = total_marks / count
    else:
        average_marks = 0
    
    if count==0:
        return render_template('error.html')

    return render_template('course_details.html', marks=marks, average_marks=average_marks, max_marks=max_marks)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        id_type = request.form.get('ID')
        id_value = request.form.get('id_value')
        id_value2=" "+id_value

        if id_value:
            if id_type == 'student_id':
                return get_student_details(id_value)
            elif id_type == 'course_id':
                return get_course_details(id_value2)
            else:
                return render_template('error.html', error_message=error_message)
        else:
            return render_template('error.html', error_message=error_message)

        return render_template('error.html', error_message=error_message)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
