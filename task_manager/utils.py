from schemas import ChainTaskID, ChainProgressReport
from celery.result import AsyncResult

def status_check(chain_task_id: ChainTaskID):
    chain_task_id = chain_task_id.dict()
    status = {
        'total': 0,
        'pending': 0,
        'started': 0,
        'retry': 0,
        'progress': 0,
        'failure': 0,
        'success': 0,
    }
    progress_report = {
        'id': chain_task_id['chain_id'],
        'progress': 0,
        'total_subtasks': 0,
    }

    for level in sorted(chain_task_id['chain_info']):
        multiprocess_task_list = chain_task_id['chain_info'][level]['task_id_list']
        for task in multiprocess_task_list:
            task_id = task['id']
            task_result = AsyncResult(task_id)
            if task_result.state == 'PENDING':
                status['total'] += 1
                status['pending'] += 1
            elif task_result.state == 'STARTED':
                status['total'] += 1
                status['started'] += 1
            elif task_result.state == 'RETRY':
                status['total'] += 1
                status['retry'] += 1
            elif task_result.state == 'PROGRESS':
                status['total'] += 1
                status['progress'] += 1
                try:
                    if isinstance(task_result.info, dict):
                        progress_report['progress'] += task_result.info.get('current', 0)
                        progress_report['total_subtasks'] += task_result.info.get('total', 1)
                    else:
                        progress_report['progress'] += 0
                        progress_report['total_subtasks'] += 1
                except AttributeError:
                    print('Progress task has no attribute info:')
                    print(task_result)
            elif task_result.state == 'FAILURE':
                status['total'] += 1
                status['failure'] += 1
            elif task_result.state == 'SUCCESS':
                status['total'] += 1
                status['success'] += 1
                try:
                    if isinstance(task_result.info, dict):
                        progress_report['progress'] += task_result.info.get('total', 1)
                        progress_report['total_subtasks'] += task_result.info.get('total', 1)
                    else:
                        progress_report['progress'] += 1
                        progress_report['total_subtasks'] += 1
                except AttributeError:
                    print('Success task has no attribute info:')
                    print(task_result)

    progress_report['status'] = status

    return ChainProgressReport(**progress_report)