% todo = uuids[uuid]
% include('templates/frontmatter.tpl', task=uuids[uuid])
## {{todo['title']}}
% if 'notes' in todo and todo['notes']:

{{todo['notes']}}
% end
% if 'checklist' in todo and todo['checklist']:

### Checklist
% for item in todo['checklist']:
- [{{' ' if item['status'] == 'incomplete' else 'x'}}] {{item['title']}}
% end
% end
