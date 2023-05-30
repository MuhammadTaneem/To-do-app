import formencode
from fastapi import APIRouter, status, Response, Depends
from core.db import create_session
from .validator import TaskValidator
from core.dependencis import get_current_user
from . import schema
from modules.pages.tasks.models import Task
from modules.users.models import User

router = APIRouter()


@router.post("/")
def create_task(task: schema.Task, response: Response, current_user: User = Depends(get_current_user)):
    try:
        task_dict = task.__dict__
        task_dict.update({'author': current_user.id})
        task_dict.update({'task_name': "Unnamed "}) if task_dict['task_name'] == "" else None
        clean_data = TaskValidator.to_python(task_dict)
        data = Task(**clean_data)
        session = create_session()
        session.add(data)
        session.commit()
        session.refresh(data)
        session.close()
        response.status_code = status.HTTP_201_CREATED
        return {'status': status.HTTP_201_CREATED, 'message': 'Task Created', 'data': data}

    except formencode.Invalid as e:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {'status': status.HTTP_406_NOT_ACCEPTABLE, 'message': 'Fix the following error ',
                'error_dict': e.unpack_errors()}

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Internal server error ',
                'error_dict': e}


@router.put("/{task_id}")
def update_task(task: schema.Task, task_id: int, response: Response, current_user: User = Depends(get_current_user)):
    try:
        session = create_session()
        task_dict = task.__dict__
        task_dict.update({'author': current_user.id})
        task_dict = TaskValidator.to_python(task_dict)
        existing_page = session.query(Task).filter(Task.id == task_id, Task.author == current_user.id).first()
        if existing_page is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'status': status.HTTP_404_NOT_FOUND, 'message': 'Page not found'}

        existing_page.author = task_dict.get('author')
        existing_page.page_name = task_dict.get('task_name')
        existing_page.page_description = task_dict.get('task_description')
        existing_page.color = task_dict.get('status')
        session.merge(existing_page)
        session.commit()
        session.refresh(existing_page)
        session.close()
        response.status_code = status.HTTP_200_OK
        return {'status': status.HTTP_200_OK, 'message': 'Task Updated', 'data': existing_page}

    except formencode.Invalid as e:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {'status': status.HTTP_406_NOT_ACCEPTABLE, 'message': 'Fix the following error ',
                'error_dict': e.unpack_errors()}

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Internal server error ',
                'error_dict': e}


@router.get("/{task_id}")
def get_task(task_id: int, response: Response, current_user: User = Depends(get_current_user)):
    try:
        session = create_session()
        existing_task = session.query(Task).filter(Task.id == task_id, Task.author == current_user.id).first()
        session.close()
        if existing_task is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'status': status.HTTP_404_NOT_FOUND, 'message': 'Task not found'}
        existing_task.status = existing_task.status_label
        # import pdb;
        # pdb.set_trace()
        task = schema.ReadTask(**existing_task.__dict__)
        response.status_code = status.HTTP_200_OK
        return {'status': status.HTTP_200_OK, 'message': 'Task details loaded',
                'data': task}

    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'status': status.HTTP_404_NOT_FOUND, 'message': 'Internal server error ', 'error_dict': e}


@router.delete("/{task_id}")
def delete_task(task_id: int, response: Response, current_user: User = Depends(get_current_user)):
    try:
        session = create_session()
        existing_task = session.query(Task).filter(Task.id == task_id, Task.author == current_user.id).first()
        if existing_task is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'status': status.HTTP_404_NOT_FOUND, 'message': 'Task not found'}
        session.delete(existing_task)
        session.commit()
        session.close()
        response.status_code = status.HTTP_200_OK
        return {'status': status.HTTP_200_OK, 'message': 'Task deleted'}
    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'status': status.HTTP_404_NOT_FOUND, 'message': 'Internal server error ', 'error_dict': e}
