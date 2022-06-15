---
---
## 📅 Upcoming

prev_date = datetime.now()
prev_date = [prev_date.year, prev_date.month, prev_date.day]
for todo in sorted(things_db['Upcoming'], key=lambda x: x['today_index']):
    todo = [t for t in todos.values() if t['uuid'] == todo['uuid']][0]  # cannot trust items in things_db to have 'path' because it contains duplicates

    todo_dt = datetime.strptime(todo['start_date'], '%Y-%m-%d')
    todo_date = [todo_dt.year, todo_dt.month, todo_dt.day]
    if prev_date[0] != todo_date[0]:  # year changed
        fout.write(f'\n# {todo_date[0]}\n')
        prev_date[1:] = None, None
    elif prev_date[1] and prev_date[1] != todo_date[1]:  # month changed
        fout.write(f'\n# {todo_dt.strftime("%B")}\n')
        prev_date[2] = None
    elif prev_date[2] and prev_date[2] != todo_date[2]:  # day changed
        fout.write(f'\n# {todo_date[2]} {todo_dt.strftime("%B")}\n')
    fout.write(f'- [ ] [{todo["title"]}]({todo["path"]})\n')
    prev_date = [(p and t) for p, t in zip(prev_date, todo_date)]
