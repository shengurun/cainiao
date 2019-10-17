from setuptools import find_packages, setup

setup(
    name="cainiao",
    version="0.1.0",
    description="Cainiao Waybill SDK.",
    author="shengurun",
    author_email="shengurun@gmail.com",
    url='https://github.com/shengurun/cainiao',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'requests',
        'websocket-client'
    ],
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
)
