from cx_Freeze import setup,Executable
packages = ['idna']
setup(name='Vk bot',
	version='0.18',
	executables=[Executable(script='VK-Bot.py')])
