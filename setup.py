from distutils.core import setup

setup(
    name='telebotty',
    packages=['telebotty'],
    version='0.0.2',
    description='TeleBotty is a framework in python for making Telegram Bot',
    author='Bardia Heydari nejad',
    author_email='bardia@heydarinejad@gmail.com',
    url='https://github.com/risheco/telebotty',
    download_url='https://github.com/risheco/telebotty/releases/tag/init',
    keywords=['telegram', 'bot', 'framework', 'full stack'],
    classifiers=[],
    install_requires=[
        'pony==0.7',
        'python-telegram-bot==5.2.0',
        'urllib3==1.18',
    ]
)
