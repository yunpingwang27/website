from setuptools import find_packages
from setuptools import setup
 
setup(
    name='phystudy',  # 项目名字
    version='1.0.0',  # 项目版本号
    packages=find_packages(),  # 告诉Python需要包含哪些目录，find_packages自动找到这些文件目录
    include_package_data=True,  # 为了包含其他文件夹，如静态文件和模板文件所在的文件夹,需要设置include_package_data为True
    # 这些包含的文件需要新建MANIFEST.in文件进行说明
    zip_safe=False,
    install_requires=[
        'flask',
        'flask_mongoengine',
        'flask_socketio'
    ],
)