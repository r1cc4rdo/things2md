% area = uuids[uuid]
% area_projects = [content_uuid for content_uuid in area['items'] if uuids[content_uuid]['type'] == 'project']
% area_todos = [content_uuid for content_uuid in area['items'] if uuids[content_uuid]['type'] == 'to-do']
% include('templates/frontmatter.tpl', task=area)
# TODO
* projects: sorted(contents, key=lambda t: t['index']):
* todos: sorted(contents, key=lambda t: t['today_index']):

## {{area['title']}}
% if area_projects:

% for project_uuid in area_projects:
* [{{uuids[project_uuid]['title']}}]({{uuids[project_uuid]['fullpath']}})
% end  # for project_uuid
% end  # if area_projects
% if area_todos:

% for todo_uuid in area_todos:
% include('templates/todoentry.tpl', todo=uuids[todo_uuid])
% end  # for uuid
% end  # if area_todos
