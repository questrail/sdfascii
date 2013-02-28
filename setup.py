from distutils.core import setup
setup(
    name='sdfascii',
    version='0.1.0',
    author='Matthew Rankin',
    author_email='matthew@questrail.com',
    py_modules=['sdfascii'],
    url='http://github.com/questrail/sdfascii',
    license='LICENSE.txt',
    description='Read HP SDF binary and ASCII files',
    requires=['numpy (>=1.6.0)'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
