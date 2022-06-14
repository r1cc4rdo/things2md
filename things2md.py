import json
import argparse
from pathlib import Path
from collections import defaultdict, Counter

from bottle import template


def load_db(db_path, all_todos=False):
    """
    Returns a dictionary of items indexed by UUID, including to-dos, projects, areas, headings and a
    dictionary of lists containing UUIDs for Inbox, Today, Upcoming, Anytime, Someday, No Area, Areas.

    The purpose of this function is then to transform the .json output of things-cli into a more
    pythonic, less redundant data structure, and to assign filenames and paths to tasks and projects.

    Talking about filenames, the only two invalid characters in a macOS path name are '\0' and ':'.
    We ignore the first and substitute the second with a unicode lookalike, U+A789 (i.e '꞉').
    See https://charbase.com/a789-unicode-modifier-letter-colon, U+A789: MODIFIER LETTER COLON.
    Technically forward slashes '/' can appear in a filename in macOS, but they wreak havoc on
    Python's path handling routines, so we substitute them with U+2215 '/'.

    I've read the sources for both things.py and things-cli. IMO, there is little advantage in using
    the python library directly as of now, plus I see value in decoupling through the filesystem.

    The following are the 21 fields than CAN appear in a task definition:
    uuid, area, heading, project: UUIDs, 22 case-sensitive alphanumeric.
    title, area_title, heading_title, project_title: titles for current items and parent.
    index, today_index: relative ordering within a list and in Today's view. Can be negative.
    start: either 'Someday', 'Inbox', 'Anytime'
    created, modified, deadline, start_date, stop_date: date strings like '2021-03-28 12:15:20' or None
    notes: string, to-do or project notes
    status: either 'incomplete', 'completed', 'canceled'
    type: either 'project', 'area', 'to-do', 'heading'. This function adds a fifth type: 'inbox'
    items, checklist: list of items for either a project or a to-do
    """
    with Path(db_path).open() as json_in:
        db = json.load(json_in)

    uuids = {}  # master dictionary of UUIDs, including to-dos, projects, areas, headings
    lists = defaultdict(list)  # list of UUIDS for areas, projects, inbox, upcoming, etc.
    for task_list in db:
        title = task_list['title']
        for task in task_list['items']:
            if (not all_todos) and ('status' in task) and (task['status'] != 'incomplete'):
                continue  # filter everything but 'incomplete'

            uuid = task['uuid']
            lists[title].append(uuid)
            if uuid in uuids:
                assert task == uuids[uuid], 'sanity check failed: found discrepancy between duplicates'
            else:
                uuids[uuid] = task

    for task_list in lists.values():
        assert len(task_list) == len(set(task_list)), 'sanity check failed: found duplicates within task lists'

    inbox_uuid = 'InboxInboxInboxInbox42'
    assert inbox_uuid not in uuids, 'sanity check failed: the probability of this happening by chance is ~3.67 * 10^-40'
    inbox_items = sorted([uuids[uuid] for uuid in lists['Inbox']], key=lambda t: t['index'])
    inbox = {'uuid': inbox_uuid, 'type': 'inbox', 'title': 'Inbox', 'items': inbox_items}
    uuids[inbox_uuid] = inbox  # add item to represent the inbox

    for task in uuids.values():  # add filename, collect parent
        filename = str(task['title']).replace(':', '\uA789').replace('/', '\u2215')
        task['filename'] = filename if task['type'] != 'heading' else ''
        match task:
            case {'heading': uuid} | {'project': uuid} | {'area': uuid}:
                task['parent'] = uuid
            case {'uuid': uuid} if uuid in lists['Inbox']:
                task['parent'] = inbox['uuid']
            case _:
                task['parent'] = None

    for task in uuids.values():  # build filepaths
        if task['type'] == 'heading':
            task['fullpath'] = None  # make sure we don't use this by mistake
            continue

        fullpath, current = Path(task['filename']), task
        while uuid := current['parent']:
            current = uuids[uuid]
            if current['type'] != 'heading':  # might still walk up to a heading
                fullpath = current['filename'] / fullpath
        task['fullpath'] = fullpath

    all_paths = [task['fullpath'] for task in uuids.values() if task['fullpath']]  # dedupe duplicate paths with UUID
    path_counts = Counter(all_paths)
    deduped = Counter(set(all_paths))
    duplicates = [p for p in path_counts - deduped]
    if duplicates:
        for task in uuids.values():
            if task['fullpath'] in duplicates:
                task['fullpath'] = task['fullpath'].with_name(f'{task["fullpath"].name}-{task["uuid"]}')

    for task in uuids.values():  # max path length is 255 chars on macOS Monterey, APFS
        assert len(str(task['fullpath'])) < 256, f'sanity check fail: path too long\nPath: {str(task["fullpath"])}'

    return uuids, lists


def convert(input_json, output_dir, all_todos=False):
    """
    Most logic for creating .md files is contained in the templates under the directory with the same name.
    Templates are instances of the SimpleTemplate format, from the Bottle project. Syntax and docs can be
    found here: https://bottlepy.org/docs/dev/stpl.html#bottle.SimpleTemplate
    """
    uuids, lists = load_db(input_json, all_todos)

    for task in uuids.values():  # create directories
        if task['type'] in ('project', 'area', 'inbox'):
            (output_dir / task['fullpath']).mkdir(parents=True, exist_ok=True)

    for uuid, item in uuids.items():  # write out to-do, projects, areas, inbox markdown files
        if item['type'] != 'heading':
            with (output_dir / item['fullpath'].with_suffix('.md')).open('w') as md_out:
                md_out.write(template(f'templates/{item["type"]}.tpl', {'uuid': uuid, 'uuids': uuids}))

    # project
    # create_upcoming(things_db, todos)
    # create_today(areas, projects, things_db, todos)
    # create Anytime markdown
    # create Someday markdown

    # TODO: sort in area, project, etc


if __name__ == '__main__':

    import os
    os.system('rm -rf test')
    os.system('rm -rf vault')

    parser = argparse.ArgumentParser(
        usage='python things2md -i things_dump.json -o vault_directory',
        description='Converts a Things3 database in json format to a collection of markdown files and directories')
    parser.add_argument('-i', '--input', required=True, help='Source Things3 database in json format')
    parser.add_argument('-o', '--output', required=True, help='Target directory for generated files')
    parser.add_argument('-a', '--all', action='store_true', help='Also dump completed/cancelled')
    args = parser.parse_args()

    convert(args.input, args.output, args.all)
    print('All done.')

    # TODO: items to list of only UUIDs >> refactor templates
    # TODO: rename uuid variable in templates
    # TODO: add template for single item
    # TODO: add tags to end

    # TODO: ignore today upcoming etc, make your own from dates
    # TODO: add hierarchy for Breadcrumbs plugin: https://github.com/SkepticMystic/breadcrumbs
    # TODO: test / use creases https://github.com/liamcain/obsidian-creases

    # TODO: contact things-cli
    # TODO: contact things skin

    # TODO check on my own db
    # for index, a in enumerate(lists):
    #     for b in list(lists)[index + 1:]:
    #         if a == b:
    #             continue
    #
    #         common = set(lists[a]).intersection(set(lists[b]))
    #         if not common:
    #             continue
    #
    #         print(a, b, len(common))

    # TODO collect all fields and values, on my own db
    # field_names = []
    # for task in uuids.values():
    #     field_names.extend(list(task))
    # field_names = sorted(set(field_names))
    #
    # for index, field_name in enumerate(field_names):
    #     if field_name == 'checklist' or field_name == 'items':
    #         continue
    #
    #     values = []
    #     for task in uuids.values():
    #         if field_name in task:
    #             values.append(task[field_name])
    #     print(index, field_name, set(values))
