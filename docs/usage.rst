=====
Usage
=====

To use lazy-object-proxy in a project::

	import lazy_object_proxy

    def heavyweight_function():
        result = "something_big"
        return result
    
    my_big_thing = lazy_object_proxy.Proxy(heavyweight_function)
    
To do lazy object initialization:: 

    class BloatedClass(object):
        def __init__(self):
            self.a = AnotherClass()
            self.b = {}
            
        def get_bloated_dict(self):
            return self.b
            
    def bloated_class_init():
        return BloatedClass()
    
    # This will not instantiate the class 
    # so to the heavyweight init will not be run yet.
    
    my_bloated_object = lazy_object_proxy.Proxy(bloated_class_init)
