# TODO
* projects: sorted(contents, key=lambda t: t['index']):
* todos: sorted(contents, key=lambda t: t['today_index']):

% area = uuids[uuid]
% include('templates/frontmatter.tpl', task=area)
## {{area['title']}}
% area_projects = [p['uuid'] for p in area['items'] if p['type'] == 'project']
% if area_projects:

% for uuid in area_projects:
% project = uuids[uuid]
* [{{project['title']}}]({{project['fullpath']}})
% end  # for uuid
% end  # if area_projects
% area_todos = [t['uuid'] for t in area['items'] if t['type'] == 'to-do']
% if area_todos:

% for uuid in area_todos:
% todo = uuids[uuid]
- [{{' ' if todo['status'] == 'incomplete' else 'x'}}] {{todo['title']}}
    - ![Open ToDo...]({{todo['fullpath']}})
% end  # for uuid
% end  # if area_todos
