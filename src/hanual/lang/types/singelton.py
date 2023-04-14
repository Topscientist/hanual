"""
There caon only be one instance of any child class, if you try
to instantiate it will just return an already made instance.

>>> class ExampleSingleton:
...     instance: ExampleSingleton = None
...
...     def on_making_a_new_instance(self):
...         if self.instance is None:
...             inst = type(self).__init__()
...             self.instance = inst
...             return inst
...         return self.instance

>>> a = ExampleSingleton()
>>> a.abc = 10
>>> b = ExampleSingleton()
>>> b.abc
10
"""


class Singleton:
    _instances = {}

    def get_instance(self, *args, **kwargs):
        if type(self).__name__ in Singleton._instances.keys():
            return Singleton._instances[type(self).__name__]

        instance = type(self).__init__(*args, **kwargs)
        Singleton._instances[type(self).__name__] = instance
        return instance