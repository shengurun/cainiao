from setuptools import find_packages, setup

with open("README.md", mode="r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="cainiao",
    version="0.2.0",
    description="Cainiao Waybill SDK.",
    long_description=readme,
    long_description_content_type='text/markdown',
    author="shengurun",
    author_email="shengurun@gmail.com",
    url='https://github.com/shengurun/cainiao',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        'aiohttp',
        'xmltodict'
    ],
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
)
