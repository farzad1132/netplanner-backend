from task_manager.schemas import ChainTaskID, ChainProgressReport
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
        'current_stage_info': '',
        'progress': 0,
        'total_subtasks': 0,
        'estimated_total_subtasks': 0,
    }
    estimated_total_subtasks = 0
    for level in sorted(chain_task_id['chain_info']):
        multiprocess_task_list = chain_task_id['chain_info'][level]['task_id_list']
        estimated_total_subtasks += chain_task_id['chain_info'][level]['task_number']
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
                        progress_report['current_stage_info'] = task_result.info.get('current_stage_info', 'Not defined')
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
    progress_report['estimated_total_subtasks'] = estimated_total_subtasks
    progress_report['status'] = status
    if status['total'] == status['success']:
        progress_report['current_stage_info']='Finished successfully.'
    return ChainProgressReport(**progress_report)