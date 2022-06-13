---
---
## Inbox

% for todo in uuids[uuid]['items']:
- [{{' ' if todo['status'] == 'incomplete' else 'x'}}] {{todo['title']}}
    - ![Open ToDo...]({{todo['fullpath']}})
% end
