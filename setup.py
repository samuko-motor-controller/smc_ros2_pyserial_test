from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'smc_ros2_pyserial_test'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('lib/' + package_name, [package_name+'/smc_arduino_pyserial_comm.py']),
        (os.path.join('share', package_name), glob('launch/*launch.[pxy][yma]*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='samuko',
    maintainer_email='samuel.c.agba@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # 'executable_name = package_name.python_file_name:main'
            'keyboard_drive_client = smc_ros2_pyserial_test.keyboard_drive_client:main',
            'smc_drive_server = smc_ros2_pyserial_test.smc_drive_server:main',
            'smc_arduino_pyserial_comm = smc_ros2_pyserial_test.smc_arduino_pyserial_comm:main',
        ],
    },
)
