from bs4 import BeautifulSoup
#!pip install bs4
from zipfile import ZipFile
import os

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

    input = ''
    for file in files:
        input +=file + ' '

    print(lasfile_path)
    os.system('D:/LASTools/bin/lasmerge.exe -i ' + input +' -o ' + lasfile_path)

    return lasfile_path



def zipper(files,zip_path):

    zipObj = ZipFile(zip_path, 'w')
    # Add multiple files to the zip

    for i in range(len(files)):

        zipObj.write(files[i])
    # zipObj.write('test_2.log')
    # close the Zip File
    zipObj.close()

    return zip_path


def multiviewloader(new_task_name,task_list,files,lasfile_path,zip_path,merge):
    task_name = task_list[-1]
    copy_path = 'D:/potree-develop/examples/' + task_name + '.html'
    output_path = 'D:/potree-develop/examples/' + new_task_name + '.html'

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

        print(tag)

    # print(soup)

    # Creating an HTML file
    Func = open(output_path, "w")

    # Adding input data to the HTML file
    Func.write(str(soup))

    # Saving the data into the HTML file
    Func.close()

    if merge == True:
        las_path = lasmerger(lasfile_path,files)
        return las_path
    else:
        zip_path = zipper(files,zip_path)
        return zip_path
# return

# xx = multiviewloader(new_task_name,task_list,files,lasfile_path,zip_path,merge)
# print(xx)

