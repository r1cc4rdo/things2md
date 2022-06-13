% include('templates/frontmatter.tpl', task=uuids[uuid])
## {{uuids[uuid]['title']}}
% if 'notes' in uuids[uuid] and uuids[uuid]['notes']:

{{uuids[uuid]['notes']}}
% end
% if 'checklist' in uuids[uuid] and uuids[uuid]['checklist']:

### Checklist
% for item in uuids[uuid]['checklist']:
- [{{' ' if item['status'] == 'incomplete' else 'x'}}] {{item['title']}}
% end
% end
