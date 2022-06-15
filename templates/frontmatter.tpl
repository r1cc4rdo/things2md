---
% for key in 'uuid title area_title project_title start_date stop_date created modified deadline'.split():
% if key in task:
{{key}}: {{task[key]}}
% end
% end
% if 'parent' in task and task['parent']:
parent: {{task['fullpath'].parent.with_suffix('.md').name}}
% end
---
