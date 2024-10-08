from setuptools import setup, find_packages

setup(
    name='auto-video-maker',
    version='0.1.0',
    author='Fernando Pujaico Rivera',
    author_email='fernando.pujaico.rivera@gmail.com',
    description='A tool to automatically create videos from images and text',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/seu-usuario/auto-video-maker',  # Link para o repositório do projeto (se houver)
    packages=find_packages(),
    install_requires=[
        'PyMuPDF',
        'Pillow',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'auto-video-maker=auto_video_maker.main:main',  # Define o comando `auto-video-maker`
        ],
    },
)

