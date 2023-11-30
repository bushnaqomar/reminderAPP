from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)

reminders = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/set_reminder', methods=['POST'])
def set_reminder_endpoint():
    task = request.form.get('task')
    date_time = request.form.get('date_time')
    
    if task and date_time:
        try:
            reminder_time = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M')
            if reminder_time > datetime.datetime.now():
                if reminder_time not in reminders:
                    reminders[reminder_time] = [task]
                else:
                    reminders[reminder_time].append(task)
                return jsonify({'message': f"Reminder set for '{task}' on {reminder_time}"})
            else:
                return jsonify({'error': "Please provide a future date and time for the reminder."}), 400
        except ValueError:
            return jsonify({'error': "Invalid date/time format. Use 'YYYY-MM-DD HH:MM'."}), 400
    else:
        return jsonify({'error': "Task and date_time parameters are required."}), 400

def check_reminders():
    current_time = datetime.datetime.now()
    for reminder_time, tasks in list(reminders.items()):
        if current_time >= reminder_time:
            print(f"Reminder! Tasks to be done: {', '.join(tasks)}")
            del reminders[reminder_time]

# This function should be part of your main loop or application logic
check_reminders()

if __name__ == '__main__':
    app.run(debug=True)
