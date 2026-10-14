from setuptools import find_packages, setup

package_name = 'kinova_examples'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='alexander',
    maintainer_email='alexander.ceron@unimilitar.edu.co',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
           'example01_joint_states = kinova_examples.example01_joint_states:main',
           'example02_move_joint = kinova_examples.example02_move_joint:main',
           'example03_gripper = kinova_examples.example03_gripper:main',
           'example04_presets = kinova_examples.example04_presets:main',
           'example05_offsets = kinova_examples.example05_offsets:main',
           'example06_poses = kinova_examples.example06_poses:main',       
           'example07A_yaml_poses = kinova_examples.example07A_yaml_poses:main',    
           'example07B_yaml_poses = kinova_examples.example07B_yaml_poses:main',          
           'example08_sequence = kinova_examples.example08_sequence:main', 
           'example09_inverse_kinematics = kinova_examples.example09_inverse_kinematics:main',
           'example10_cartesian = kinova_examples.example10_cartesian:main',           
        ],
    },
)
