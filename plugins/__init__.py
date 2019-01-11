from os import listdir
__all__ = []
for i in listdir('./plugins'):
	__all__.append(i)
f = {}
print(__all__)