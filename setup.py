from setuptools import setup, find_packages

setup(
    name='image_overlay_app',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'PyQt6',
    ],
    entry_points={
        'console_scripts': [
            'image-overlay-app = image_overlay_app.main:main',
        ],
    },
    include_package_data=True,
    description='A draggable image overlay application with zoom and opacity controls.',
    author='Your Name',
    url='https://your-repo-url.com',
)