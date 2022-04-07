import datetime
import mimetypes
import os
import sys

import json

from django.contrib.sites import requests
from django.http import JsonResponse, HttpResponse, Http404
from django.template.defaulttags import url
from django.utils.encoding import smart_str
import requests
from laider.settings import MEDIA_ROOT
from laider import settings
from laiderapp import models
from django.shortcuts import render

# Create your views here.
from laiderapp.models import creatingproject, las_files
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import ensure_csrf_cookie
from wsgiref.util import FileWrapper
from laiderapp import multi_view_loader


import shutil
import re
from laiderapp import potree_automation
@csrf_exempt
def creatingProject(request):
    if request.method =="POST":
        print(request)
        try:
            data = json.loads(request.body)
            title = data['project_title']
            description = data['description']
            print("title",title)

            projects_from_db = creatingproject.objects.filter(PROJECT_TITLE=title).values('PROJECT_TITLE')
            if len(projects_from_db)>0:
                return JsonResponse({'message':'project name '+title+' is already exists', 'status':400})

            creatingproject(PROJECT_TITLE=title, DESCRIPTION=description, IS_ACTIVE=True).save()
            return JsonResponse({'message':'project created successfully', 'status': 200})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(type(e))  # the exception instance
            print(e.args)  # arguments stored in .args
            print('error',e)
            return JsonResponse({'message': 'internal server error', 'status_code': 500})
    else:
        return JsonResponse({'message':'method not allowed', 'status':405})

@csrf_exempt
def gettingAllProjects(request):
    if request.method =="GET":
        try:
            list_of_tasks=[]
            projects =list(creatingproject.objects.filter().values('PROJECT_TITLE','DESCRIPTION'))

            for i in range(len(projects)):
                tasks = list(las_files.objects.filter(PROJECT=projects[i]['PROJECT_TITLE']).values('PROJECT','id','TASK','POTREE_HTML_FILE','DATE','FILE'))
                list_of_tasks.append(tasks)

            x = 0
            for i in projects:
                i['task']= list_of_tasks[x]
                x+=1
            return JsonResponse({'projects':projects, 'status': 200})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(type(e))  # the exception instance
            print(e.args)  # arguments stored in .args
            print('error',e)
            return JsonResponse({'message': 'internal server error', 'status_code': 500})
    else:
        return JsonResponse({'message':'method not allowed', 'status':405})

@csrf_exempt
def creatingTaskAndFileUpload(request):
    if request.method =="POST":
        try:
            myfiles = request.FILES.get('files')
            project_title = request.POST.get('project')
            task = request.POST.get('task')
            date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            # date = str(date).replace(" ","_")

            task_name = task+'_'+str(date)
            dir = MEDIA_ROOT+"/media/"+str(myfiles)
            # fs = FileSystemStorage(dir)

            projects_in_db = list(creatingproject.objects.filter(PROJECT_TITLE=project_title).values('PROJECT_TITLE'))
            print("projects_in_db",projects_in_db)
            # print(myfiles.name)

            if len(projects_in_db)>0:

                file_name = myfiles.name
                las_file = file_name.endswith(('las'))
                print(las_file)
                if las_file is True:
                    # file_path = fs.path(str(myfiles))
                    # final_name = fs.save(file_path,myfiles)
                    # final_file_path = fs.path(str(final_name))
                    # print(final_file_path)
                    potree_automation.las_convertor(dir,task_name)
                    potree_html_path = "http://10.91.97.120:1234/examples/"+task_name+".html"

                    las_files(PROJECT=projects_in_db[0]['PROJECT_TITLE'],TASK=task_name,IS_ACTIVE=True,IS_CONVERTED=False,POTREE_HTML_FILE=potree_html_path, FILE=myfiles).save()


                    return JsonResponse({'message': 'task created and file uploaded successfully', 'status_code': 200})
                else:
                    return JsonResponse({'message': 'File extension does not match(las)', 'status_code': 200})
            else:
                return JsonResponse({'message': 'There is on such project avalible', 'status_code': 200})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(type(e))  # the exception instance
            print(e.args)  # arguments stored in .args
            print('error', e)
            return JsonResponse({'message': 'internal server error', 'status_code': 500})
    else:
        return JsonResponse({'message':'method not allowed', 'status':405})

@csrf_exempt
def deletingTasks(request):
    if request.method =="POST":
        print(request)
        try:
            data = json.loads(request.body)
            title = data['project_title']
            task = data['task_name']
            date_from_db = data['date']
            file = data['file']
            print("title",title)
            tasks_from_db = list(las_files.objects.filter(PROJECT=title,TASK=task))
            if len(tasks_from_db) > 0 :
                if os.path.exists(MEDIA_ROOT+'/'+file):
                    os.remove(MEDIA_ROOT+'/'+file)
                    las_files.objects.filter(PROJECT=title,TASK=task).delete()

                    return JsonResponse({'message':'deleted the task successfully', 'status': 200})
                else:
                    return JsonResponse({'message':'file not found', 'status':400})
            else:
                return JsonResponse({'message':'the task is not present', 'status':400})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(type(e))  # the exception instance
            print(e.args)  # arguments stored in .args
            print('error',e)
            return JsonResponse({'message': 'internal server error', 'status_code': 500})
    else:
        return JsonResponse({'message':'method not allowed', 'status':405})


@csrf_exempt
def deletingProject(request):
    if request.method =="POST":
        print(request)
        try:
            data = json.loads(request.body)
            project_title = data['project_title']

            pointclouds_path = 'D:/potree-develop/pointclouds/'
            html_file_path = 'D:/potree-develop/examples/'
            project_from_db = list(creatingproject.objects.filter(PROJECT_TITLE=project_title))
            tasks_from_db = list(las_files.objects.filter(PROJECT=project_title).values('TASK'))
            print('tasks_from_db',tasks_from_db)
            tasks_list = []
            for i in tasks_from_db:
                tasks_list.append(i.get('TASK'))
            print('tasks_list',tasks_list)

            if len(project_from_db) > 0:
                for i in tasks_list:
                    if os.path.exists(pointclouds_path + i) and os.path.exists(html_file_path + i + '.html'):
                        shutil.rmtree(pointclouds_path + i)
                        os.remove(html_file_path + i + '.html')
                    else:
                        return JsonResponse({'message': 'files not found', 'status': 400})

                creatingproject.objects.filter(PROJECT_TITLE=project_title).delete()
                las_files.objects.filter(PROJECT=project_title).delete()

                return JsonResponse({'message':'deleted the project successfully', 'status': 200})
            else:
                return JsonResponse({'message':'no such project exists','status':400})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(type(e))  # the exception instance
            print(e.args)  # arguments stored in .args
            print('error',e)
            return JsonResponse({'message': 'internal server error', 'status_code': 500})
    else:
        return JsonResponse({'message':'method not allowed', 'status':405})



@ensure_csrf_cookie
@csrf_exempt
def downloadingLasFiles(request):
    print(request)
    # print(path)
    if request.method =="GET":
        try:
            file_path_from_db = request.GET['las_file_path']
            path=MEDIA_ROOT+'/'+file_path_from_db
            filename = os.path.basename(path)
            if os.path.exists(path):
                file = open(path, "rb")

                response = HttpResponse(FileWrapper(file), content_type=(mimetypes.guess_type(filename)[0] or "application/zip"))
                response['Content-Disposition'] = 'attachment; filename='+filename
                return response
            else:
                return JsonResponse({'message': 'file not found', 'status_code': 400})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(type(e))  # the exception instance
            print(e.args)  # arguments stored in .args
            print('error',e)
            return JsonResponse({'message': 'internal server error', 'status_code': 500})
    else:
        return JsonResponse({'message':'method not allowed', 'status':405})

@csrf_exempt
def updatingProject(request):
    if request.method =="POST":
        try:
            data = json.loads(request.body)
            project_title = data['project_title']
            print(project_title)
            new_project_title = data['new_project_title']
            description = data['description']
            new_description = data['new_description']
            print(new_description)
            date = datetime.datetime.now()
            projects_from_db = list(creatingproject.objects.filter(PROJECT_TITLE=project_title))

            if len(projects_from_db)>0:
                if project_title != new_project_title and description != new_description :
                    creatingproject.objects.filter(PROJECT_TITLE=project_title).update(PROJECT_TITLE=new_project_title,DESCRIPTION=new_description)
                    return JsonResponse({'message':'project and description are updated', 'status':200})
                if project_title != new_project_title:
                    creatingproject.objects.filter(PROJECT_TITLE=project_title).update(PROJECT_TITLE=new_project_title)
                    return JsonResponse({'message':'project is updated to '+new_project_title, 'status':200})
                if description != new_description:
                    creatingproject.objects.filter(PROJECT_TITLE=project_title).update(DESCRIPTION=new_description)
                    return JsonResponse({'message':'project description is updated', 'status':200})
            else:
                return JsonResponse({'message':'project does not exist', 'status':400})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(type(e))  # the exception instance
            print(e.args)  # arguments stored in .args
            print('error', e)
            return JsonResponse({'message': 'internal server error', 'status_code': 500})
    else:
        return JsonResponse({'message': 'method not allowed', 'status': 405})

@csrf_exempt
def updatingTasks(request):
    if request.method =='POST':
        try:
            data = json.loads(request.body)
            project_title = data['project_title']
            old_task_name = data['old_task_name']
            print(old_task_name)
            new_task_name = data['new_task_name']

            task = old_task_name.split('_')
            task[0]= new_task_name
            task_name = '_'.join(task)

            task_from_db = list(las_files.objects.filter(PROJECT=project_title,TASK=old_task_name))
            if len(task_from_db)> 0 :
                return JsonResponse({"message":'no such task is existed', 'status':400})

            las_files.objects.filter(PROJECT=project_title,TASK=old_task_name).update(TASK=task_name)
            return JsonResponse({'message':'task name is updated successfully', 'status':200})
        except Exception as e:
            exc_type, exc_obj, exc_tb  = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(type(e))  # the exception instance
            print(e.args)  # arguments stored in .args
            print('error', e)
            return JsonResponse({'message': 'internal server error', 'status_code': 500})
        else:
            return JsonResponse({'message': 'method not allowed', 'status': 405})


@csrf_exempt
def combining_tasks(request):
    if request.method == 'POST':
        try:
            # data = json.loads(request.body)
            # new_task_name = data['task_name']
            # task_list = data['task_list']
            # files = data['lasfiles']
            # merge = data['merge']
            new_task_name = 'NEW_MERGED'
            task_list = ['test2_2022-04-06_16-38-25','test21_2022-04-06_16-38-35','test21_2022-04-06_16-38-45']
            files = [MEDIA_ROOT+'/'+'media/points.las',MEDIA_ROOT+'/'+'media/points_aMyUpmr.las',MEDIA_ROOT+'/'+'media/points_MD858HJ.las']
            lasfile_path = MEDIA_ROOT+'/media/'+new_task_name+'.las'
            zip_path = MEDIA_ROOT + '/media/' + new_task_name + '.zip'
            merge =False
            output_path = multi_view_loader.multiviewloader(new_task_name,task_list,files,lasfile_path,zip_path,merge)
            print(output_path)

            TODO:'update the response & change the input request fields'

            return JsonResponse({'path':output_path,})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(type(e))  # the exception instance
            print(e.args)  # arguments stored in .args
            print('error', e)
            return JsonResponse({'message': 'internal server error', 'status_code': 500})
    else:
        return JsonResponse({'message': 'method not allowed', 'status': 405})