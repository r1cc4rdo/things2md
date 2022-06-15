% from datetime import datetime
% prev_date = datetime.now()
% prev_year, prev_month, prev_day = prev_date.year, prev_date.month, prev_date.day
% upcoming_todos = [uuids[todo_uuid] for todo_uuid in uuids[uuid]['items']]
% upcoming_todos = sorted(upcoming_todos, key=lambda todo: todo['today_index'])
---
---
## 📅 Upcoming
% for todo in upcoming_todos:
% todo_datetime = datetime.strptime(todo['start_date'], '%Y-%m-%d')
% todo_year, todo_month, todo_day = todo_datetime.year, todo_datetime.month, todo_datetime.day
% if prev_year != todo_year:  # year granularity?

## {{todo_year}}
% prev_month, prev_day = None, None  # suppress month and day titles from now on
% elif prev_month and prev_month != todo_month:  # month granularity?

## {{todo_datetime.strftime("%B")}}
% prev_day = None  # suppress day titles from now on
% elif prev_day and prev_day != todo_day:  # day granularity?

## {{todo_day}} {{todo_datetime.strftime("%B")}}
% end  # if prev_year
% include('templates/todoentry.tpl', todo=todo)
% prev_year, prev_month, prev_day = prev_year and todo_year, prev_month and todo_month, prev_day and todo_day
% end  # for todo_uuid
