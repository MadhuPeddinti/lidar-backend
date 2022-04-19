import os
import shutil
import re


file_path = 'D:/TRT.las'
task_name = 'TRT'
def las_convertor(file_path,task_name):
    output_path = 'D:/potree-develop/pointclouds/'+task_name
    os.system('D:/PotreeConverter_2.1_x64_windows/PotreeConverter.exe ' + file_path+' -o '+output_path)
    copy_path = 'D:/potree-develop/examples/' + task_name + '.html'
    copy_path1 = 'D:/potree-develop/public/' + task_name + '.html'
    shutil.copy('D:/potree-develop/examples/example.html', copy_path)
    shutil.copy('D:/potree-develop/public/example.html', copy_path1)
    # print(copy_path)

    # load the file
    with open(copy_path) as inf:
        txt = inf.read()
        response = re.sub('example',task_name,txt)
        #response = re.sub('sigeom.sa', task_name, txt)
        # print(response)

    # Creating an HTML file
    Func = open(copy_path, "w")

    # Adding input data to the HTML file
    Func.write(response)

    # Saving the data into the HTML file
    Func.close()
    # return

    with open(copy_path1) as inf1:
        txt1 = inf1.read()
        response1 = re.sub('public',task_name,txt1)
        #response = re.sub('sigeom.sa', task_name, txt)
        # print(response)

    # Creating an HTML file
    Func = open(copy_path1, "w")

    # Adding input data to the HTML file
    Func.write(response1)

    # Saving the data into the HTML file
    Func.close()
    # return

#xx=las_convertor(file_path,task_name)
# print('##################################################################',xx)
