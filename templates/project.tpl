% include('templates/frontmatter.tpl', task=uuids[uuid])
# TODO: sort
```
contents = sorted(contents, key=lambda t: t['today_index'])
sorted(heading_contents, key=lambda t: t['index']):
```

## {{uuids[uuid]['title']}}
% notes = uuids[uuid]['notes'].strip()
% if notes:

{{notes}}
% end  # if

% for item in [uuids[project_item['uuid']] for project_item in uuids[uuid]['items']]:
% if item['type'] == 'to-do':
- [{{' ' if item['status'] == 'incomplete' else 'x'}}] {{item['title']}}
    - ![Open ToDo...]({{item['fullpath']}})
% else:  # item['type']
### {{item['title']}}
% heading_contents = [uuids[heading_item['uuid']] for heading_item in item['items']]
% for heading_todo in heading_contents:
- [{{' ' if heading_todo['status'] == 'incomplete' else 'x'}}] {{heading_todo['title']}}
    - ![Open ToDo...]({{heading_todo['fullpath']}})
% end  # for heading_todo
% end  # if item['type']
% end  # for item
