from typing import List
from algorithms.template_worker import template_task


def rwa_status_check(id_list: List[str]):
    result = []
    for id in id_list:
        task = template_task.AsyncResult(id)

        if task.state == 'PENDING':
            response = {
                'id': id,
                'state': task.state,
                'current': 0,
                'total': 1,
                'status': 'Pending...'
            }
        elif task.state != 'FAILURE':
            response = {
                'id': id,
                'state': task.state,
                'current': task.info.get('current', 0),
                'total': task.info.get('total', 1),
                'status': task.info.get('status', '')
            }
            if 'result' in task.info:
                response['result'] = task.info['result']
        else:
            # something went wrong in the background job
            response = {
                'id': id,
                'state': task.state,
                'current': 1,
                'total': 1,
                'status': str(task.info),  # this is the exception raised
            }
        result.append(response)
    return result

