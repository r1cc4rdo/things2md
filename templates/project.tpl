% project = uuids[uuid]
% include('templates/frontmatter.tpl', task=project)
# TODO: sort
```
contents = sorted(contents, key=lambda t: t['today_index'])
sorted(heading_contents, key=lambda t: t['index']):
```

## {{project['title']}}
% notes = project['notes'].strip()
% if notes:

{{notes}}
% end  # if

% for project_content_uuid in project['items']:
% project_content = uuids[project_content_uuid]
% if project_content['type'] == 'to-do':
% include('templates/todoentry.tpl', todo=project_content)
% else:  # project_content['type'] == 'heading'

### {{project_content['title']}}
% heading_contents = [uuids[heading_content_uuid] for heading_content_uuid in project_content['items']]
% for heading_content in heading_contents:
% include('templates/todoentry.tpl', todo=heading_content)
% end  # for heading_content
% end  # if project_content['type']
% end  # for project_content_uuid
