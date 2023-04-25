class SoyUnico(object):
    class __NoSoyUnico:
        def __init__(self):
            self.nombre = None
        def __str__(self):
            return 'self' + ' ' + self.nombre

	instance = None
	def __new__(cls):
		if not SoyUnico.instance:
			SoyUnico.instance = SoyUnico.__SoyUnico()
		return SoyUnico.instance
	def __getattr__(self, nombre):
		return getattr(self.instance, nombre)
	def __setattr__(self, nombre, valor):
		return setattr(self.instance, nombre, valor)