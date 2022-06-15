---
---
## ⭐ Today

% for x in range(5):
    {{x}}
% end

```
today_uuids = [todo['uuid'] for todo in things_db['Today']]
today_todos = [todo for todo in todos.values() if todo['uuid'] in today_uuids]
projects_paths = [todo['path'].parent for todo in today_todos]
today_projects = [project for project in sorted(projects.values(), key=lambda x: x['index']) if project['path'] in projects_paths]
for area in areas:

    area_todos = [t for t in today_todos if 'area' in t and t['area'] == area]
    if area_todos:
        fout.write(f'\n# {areas[area]["title"]}\n')
        for todo in area_todos:
            fout.write(f'- [ ] [{todo["title"]}]({todo["path"]})\n')

    for project in today_projects:
        if project['area'] != area:
            continue

        fout.write(f'\n# {project["title"]}\n')
        for todo in [t for t in today_todos if t['path'].parent == project['path']]:
            fout.write(f'- [ ] [{todo["title"]}]({todo["path"]})\n')
```
