def create_areas(areas, projects, todos):
    for uuid, area in areas.items():
        with Path(f'{area["path"].name}.md').open('w') as fout:
            contents = [project for project in projects.values() if project['area'] == uuid]
            for project in sorted(contents, key=lambda t: t['index']):
                fout.write(f'* [{project["title"]}]({project["path"]})\n')

            fout.write('\n')
            contents = [todo for todo in todos.values() if todo['path'].parent == area['path']]
            for todo in sorted(contents, key=lambda t: t['today_index']):
                fout.write(f'- [ ] [{todo["title"]}]({todo["path"]})\n')