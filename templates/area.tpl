% area = uuids[uuid]
% include('templates/frontmatter.tpl', task=area)
# TODO
* projects: sorted(contents, key=lambda t: t['index']):
* todos: sorted(contents, key=lambda t: t['today_index']):

## {{area['title']}}
% area_projects = [content_uuid for content_uuid in area['items'] if uuids[content_uuid]['type'] == 'project']
% if area_projects:

% for project_uuid in area_projects:
% project = uuids[project_uuid]
* [{{project['title']}}]({{project['fullpath']}})
% end  # for project_uuid
% end  # if area_projects
% area_todos = [content_uuid for content_uuid in area['items'] if uuids[content_uuid]['type'] == 'to-do']
% if area_todos:

% for todo_uuid in area_todos:
% include('templates/todoentry.tpl', todo=uuids[todo_uuid])
% end  # for uuid
% end  # if area_todos
