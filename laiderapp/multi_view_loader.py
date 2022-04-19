import sys

from bs4 import BeautifulSoup
#!pip install bs4
from zipfile import ZipFile
import os
import re
import shutil
# merge = False
# task_list = ['U5','TRT','U5']
# files = ['D:/U5.las',
#          'D:/TRT.las']
#
# new_task_name = 'tets'
#
# lasfile_path = 'D:/' + new_task_name + '.las'
#
# zip_path = 'D:/'+new_task_name+'.zip'


def lasmerger(lasfile_path,files):
    # print('Entered the lasmerger')
    input = ''
    for file in files:
        input +=file + ' '

    print(lasfile_path)
    os.system('D:/LASTools/bin/lasmerge.exe -i ' + input +' -o ' + lasfile_path)

    return lasfile_path



def zipper(files,zip_path):
    # print('Entered the zipper')
    zipObj = ZipFile(zip_path, 'w')
    # Add multiple files to the zip

    for i in range(len(files)):

        zipObj.write(files[i])
    # zipObj.write('test_2.log')
    # close the Zip File
    zipObj.close()

    return zip_path


def multiviewloader(new_task_name,task_list,files,lasfile_path,zip_path,merge):
    # print('Enteredmultiviewloader with -- ',files,lasfile_path,zip_path,merge)
    # print("task_list",task_list)
    # task_name = task_list[-1].replace("'","")
    task_name = task_list[-1]
    copy_path = 'D:/potree-develop/examples/' + task_name + '.html'
    # print("copy_path",copy_path)
    copy_path1 = 'D:/potree-develop/public/' + new_task_name + '.html'
    output_path = 'D:/potree-develop/examples/' + new_task_name + '.html'
    try:
        with open(copy_path) as inf:
            txt = inf.read()

            # print(txt)

        soup = BeautifulSoup(txt, 'html.parser')
        tag = soup.find_all('script')[-1]
        for i in range(len(task_list)-1):
            loader = """
        Potree.loadPointCloud("../pointclouds/"""+task_list[i]+"""/metadata.json",""" +"""'"""+task_list[i] +"""'"""+ """, e => {
            let scene = viewer.scene;
            let pointcloud = e.pointcloud;

            let material = pointcloud.material;
            material.size = 1;
            material.pointSizeType = Potree.PointSizeType.ADAPTIVE;
            material.shape = Potree.PointShape.SQUARE;

            scene.addPointCloud(pointcloud);

            viewer.fitToScreen();
            // scene.view.setView(
            // 	[589974.341, 231698.397, 986.146],
            // 	[589851.587, 231428.213, 715.634],
            // );
        });
    
        """

            tag.append(loader)

            print("tag",tag)

        # print(soup)

        # Creating an HTML file
        Func = open(output_path, "w")

        # Adding input data to the HTML file
        Func.write(str(soup))

        # Saving the data into the HTML file
        Func.close()

        shutil.copy('D:/potree-develop/public/example.html', copy_path1)
        with open(copy_path1) as inf1:
            txt1 = inf1.read()
            response1 = re.sub('public', task_name, txt1)

            # print(txt)

        # Creating an HTML file
        Func = open(copy_path1, "w")

        # Adding input data to the HTML file
        Func.write(response1)

        # Saving the data into the HTML file
        Func.close()


        if merge == True:
            las_path = lasmerger(lasfile_path,files)
            return las_path
        else:
            zip_path = zipper(files,zip_path)
            return zip_path
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(type(e))  # the exception instance
        print(e.args)  # arguments stored in .args
        print('error', e)

# return

# xx = multiviewloader(new_task_name,task_list,files,lasfile_path,zip_path,merge)
# print(xx)

