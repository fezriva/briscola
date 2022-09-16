import setuptools

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitline()

setuptools.setup(name='briscola',
                 packages=['briscola'],
                 install_requires=install_requires)