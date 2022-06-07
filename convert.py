import json
from pathlib import Path
from datetime import datetime
import unicodedata
import re


def sanitize_path(value, allow_unicode=False, max_length=232):
    """
    Modified from stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
    originally from Django's  github.com/django/django/blob/master/django/utils/text.py
    max_lenght is set to 232 because a things uuid is 22 characters long, plus a separator
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    value = re.sub(r'[-\s]+', '-', value).strip('-_')
    return value[:max_length]


def load_db(db_path=None):
    """
    Create with: things-cli -j all > things.json
    """
    with Path(db_path or 'things.json').open() as json_in:
        return{x['title']: x['items'] for x in json.load(json_in)}


def collect_by_type(things_db):
    areas = {area['uuid']: area for area in things_db['Areas']}
    projects = {project['uuid']: project for project in things_db['No Area']}

    keys = 'Inbox Today Upcoming Anytime Someday Logbook'.split()
    active_items = [item for key in keys for item in things_db[key] if item['status'] == 'incomplete']
    headings = {item['uuid']: item for item in active_items if item['type'] == 'heading'}
    todos = {item['uuid']: item for item in active_items if item['type'] == 'to-do'}

    return areas, projects, headings, todos


def create_directories(areas, headings, projects):
    Path('inbox').mkdir(parents=False, exist_ok=False)

    for area in areas.values():  # create area directories
        area['path'] = Path(sanitize_path(area['title']))
        if area['path'].exists():  # resolve name clashes with UUID
            area['path'] = Path(sanitize_path(f'{area["title"]}-{area["uuid"]}'))
        area['path'].mkdir(parents=False, exist_ok=False)

    for project in projects.values():  # create project directories
        area_path = areas[project['area']]['path']
        project['path'] = area_path / sanitize_path(project['title'])
        if project['path'].exists():  # resolve name clashes with UUID
            project['path'] = area_path / sanitize_path(f'{project["title"]}-{project["uuid"]}')
        project['path'].mkdir(parents=False, exist_ok=False)

    for heading in headings.values():  # collect headings' paths
        heading['path'] = projects[heading['project']]['path']


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

        todo['path'] = parent['path'] / f'{sanitize_path(todo["title"])}.md'
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


def create_areas(areas, projects, todos):
    for uuid, area in areas.items():
        with Path(f'{area["path"].name}.md').open('w') as fout:
            contents = [project for project in projects.values() if project['area'] == uuid]
            for project in sorted(contents, key=lambda t: t['index']):
                fout.write(f'* [{project["title"]}]({project["path"]})\n')

            fout.write('\n')
            contents = [todo for todo in todos.values() if todo['path'].parent == area['path']]
            for todo in sorted(contents, key=lambda t: t['today_index']):
                fout.write(f'* [{todo["title"]}]({todo["path"]})\n')


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
                    fout.write(f'\n* [{content["title"]}]({content["path"]})')
                else:  # it's a heading
                    fout.write(f'\n\n## {content["title"]}')
                    heading_contents = [todo for todo in todos.values() if 'heading' in todo and todo['heading'] == content['uuid']]
                    for todo in sorted(heading_contents, key=lambda t: t['index']):
                        fout.write(f'\n* [{todo["title"]}]({todo["path"]})')


def create_inbox(todos):
    Path('inbox.md').touch(exist_ok=False)  # create inbox markdown
    with Path('inbox.md').open('w') as fout:
        contents = [todo for todo in todos.values() if todo['path'].parent == Path('inbox')]
        for todo in sorted(contents, key=lambda t: t['index']):
            fout.write(f'* [{todo["title"]}]({todo["path"]})\n')


def create_upcoming(things_db, todos):
    Path('upcoming.md').touch(exist_ok=False)  # create inbox markdown
    with Path('upcoming.md').open('w') as fout:
        prev_date = datetime.now()
        prev_date = [prev_date.year, prev_date.month, prev_date.day]
        for todo in sorted(things_db['Upcoming'], key=lambda x: x['today_index']):
            todo = [t for t in todos.values() if t['uuid'] == todo['uuid']][0]  # cannot trust items in things_db to have 'path' because it contains duplicates

            todo_dt = datetime.strptime(todo['start_date'], '%Y-%m-%d')
            todo_date = [todo_dt.year, todo_dt.month, todo_dt.day]
            if prev_date[0] != todo_date[0]:  # year changed
                fout.write(f'\n# {todo_date[0]}\n')
                prev_date[1:] = None, None
            elif prev_date[1] and prev_date[1] != todo_date[1]:  # month changed
                fout.write(f'\n# {todo_dt.strftime("%B")}\n')
                prev_date[2] = None
            elif prev_date[2] and prev_date[2] != todo_date[2]:  # day changed
                fout.write(f'\n# {todo_date[2]} {todo_dt.strftime("%B")}\n')
            fout.write(f'* [{todo["title"]}]({todo["path"]})\n')
            prev_date = [(p and t) for p, t in zip(prev_date, todo_date)]


def create_today(areas, projects, things_db, todos):
    Path('today.md').touch(exist_ok=False)  # create today markdown
    with Path('today.md').open('w') as fout:
        today_uuids = [todo['uuid'] for todo in things_db['Today']]
        today_todos = [todo for todo in todos.values() if todo['uuid'] in today_uuids]
        projects_paths = [todo['path'].parent for todo in today_todos]
        today_projects = [project for project in sorted(projects.values(), key=lambda x: x['index']) if project['path'] in projects_paths]
        for area in areas:

            area_todos = [t for t in today_todos if 'area' in t and t['area'] == area]
            if area_todos:
                fout.write(f'\n# {areas[area]["title"]}\n')
                for todo in area_todos:
                    fout.write(f'* [{todo["title"]}]({todo["path"]})\n')

            for project in today_projects:
                if project['area'] != area:
                    continue

                fout.write(f'\n# {project["title"]}\n')
                for todo in [t for t in today_todos if t['path'].parent == project['path']]:
                    fout.write(f'* [{todo["title"]}]({todo["path"]})\n')


def convert(db_path=None):

    things_db = load_db(db_path)
    areas, projects, headings, todos = collect_by_type(things_db)

    create_directories(areas, headings, projects)
    create_todos(areas, headings, projects, todos)
    create_projects(headings, projects, todos)
    create_areas(areas, projects, todos)

    create_inbox(todos)
    create_upcoming(things_db, todos)
    create_today(areas, projects, things_db, todos)

    # create Anytime markdown
    # create Someday markdown


if __name__ == '__main__':

    # import os
    # os.system('rm *.md')
    # os.system('rm -rf inbox learning personal time travel work')

    convert()
    print('All done.')
