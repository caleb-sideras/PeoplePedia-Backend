from setuptools import setup, find_packages

setup(
    name='getmesummerizer',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'autopep8==1.6.0',    
        'beautifulsoup4==4.11.2',    
        'django-cors-headers==3.14.0',    
        'django-environ==0.10.0',    
        'djangorestframework==3.14.0',    
        'json5==0.9.11',    
        'openai==0.27.2',    
        'pip-chill==1.0.1',    
        'pipenv==2023.2.18',    
        'scrapy==2.8.0',    
        'transformers==4.27.1',    
        'wincertstore==0.2',
    ],
)