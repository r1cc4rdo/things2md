def create_todos(areas, headings, projects, todos):
    for todo in todos.values():  # create todos' files
        if 'heading' in todo:
            parent = headings[todo['heading']]
        elif 'project' in todo:
            parent = projects[todo['project']]
        elif 'area' in todo:
            parent = areas[todo['area']]
        else:
            parent = {'path': Path('inbox')}

        todo['path'] = parent['path'] / f'{sanitize_name(todo["title"])}.md'
        if todo['path'].exists():  # resolve name clashes with UUID
            todo['path'] = todo['path'].with_suffix(f'.{todo["uuid"]}.md')

        todo['path'].touch(exist_ok=False)
        with todo['path'].open('w') as fout:
            fout.write('---\n')
            for key in 'uuid title project_title start_date created modified'.split():
                if key in todo:
                    fout.write(f'{key}: {todo[key]}\n')
            fout.write('---\n')
            fout.write(todo['notes'])
