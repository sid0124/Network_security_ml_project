from setuptools import find_packages, setup  
from typing import List

def get_requirements() -> List[str]:
    requirements_list:List[str] = []
    try :
        with open('requirements.txt','r') as file:
            lines = file.readlines()

            for line in lines:
                requirements = line.strip()
                if requirements and requirements != '-e .':
                    requirements_list.append(requirements)

    except FileNotFoundError:
        print('requirements.txt file is not found')

    return requirements_list

setup(
    name = 'networksecurity',
    version = '0.0.1',
    author = 'Sidharth Arora',
    author_email = 'sidhartharora1122@example.com',
    packages = find_packages(),
    install_requires = get_requirements()
)
