def create_projects(headings, projects, todos):
    for project in projects.values():
        with (project["path"].parent / f'{project["path"].name}.md').open('w') as fout:

            contents = [heading for heading in headings.values() if heading['path'] == project['path']]
            contents.extend(todo for todo in todos.values() if todo['path'].parent == project['path'] and 'heading' not in todo)
            contents = sorted(contents, key=lambda t: t['today_index'])

            fout.write('---\n')
            for key in 'uuid title area_title start_date created modified'.split():
                if key in project:
                    fout.write(f'{key}: {project[key]}\n')
            fout.write('---\n')
            fout.write(f'# {project["title"]}')
            if project["notes"].strip():
                fout.write(f'\n')
                fout.write(project["notes"].strip())
                if contents and contents[0]['type'] == 'to-do':
                    fout.write(f'\n')

            for content in contents:
                if content['type'] == 'to-do':
                    fout.write(f'\n- [ ] [{content["title"]}]({content["path"]})')
                    fout.write(f'\n\t- ![Open ToDo...]({content["path"]})')
                else:  # it's a heading
                    fout.write(f'\n\n## {content["title"]}')
                    heading_contents = [todo for todo in todos.values() if 'heading' in todo and todo['heading'] == content['uuid']]
                    for todo in sorted(heading_contents, key=lambda t: t['index']):
                        fout.write(f'\n- [ ] [{todo["title"]}]({todo["path"]})')
                        fout.write(f'\n\t- ![Open ToDo...]({todo["path"]})')
