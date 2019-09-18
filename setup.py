from distutils.core import setup

setup(

    name='blip_report_requisitor',
    packages=['blip_report_requisitor'],
    version='0.0.4',
    license='MIT',
    description='Wrapper to get blip reports information easily',
    author='Gabriel Rodrigues dos Santos',
    author_email='gabrielr@take.net',
    url='https://github.com/chr0m1ng/blip-report-requisitor',
    download_url='https://github.com/chr0m1ng/blip-report-requisitor/archive/v0.0.4.tar.gz',
    keywords=['report', 'blip', 'analytics'],
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
)
