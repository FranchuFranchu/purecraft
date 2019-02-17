from os import listdir
__all__ = []
for i in listdir(__file__.split('plugins')[0]+'plugins'):
	__all__.append(i)
f = {}
print(__all__)