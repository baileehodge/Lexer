from .parameter import Parameter
class Predicate:
    def __init__(self, name: str, parameters: list[Parameter]):
        self.name = name
        self.parameters = parameters
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if not hasattr(self, 'index'):
            self.index = 0

        if self.index < len(self.parameters):
            result = self.parameters[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
    
    def to_string(self):
        # param_count: int = 0
        # param_str: str = self.name
        # param_str += "("
        # for i in self.parameters:
        #     temp: str = str(i.value)
        #     param_str += temp
        #     param_count += 1
        #     if param_count != len(self.parameters):
        #         param_str += ","
        param_str = self.name + "("
        param_values = [str(param.value) for param in self.parameters]
        param_str += ",".join(param_values)
        param_str += ")"
        return param_str
    
    def basic_to_string(self):
        param_values = [str(param.value) for param in self.parameters]
        param_str = ",".join(param_values)
        return param_str


        # param_str += ")"
        # param_str = ','.join(self.parameters.to_string())
        # return(f'{self.name}({param_str})')
        # return param_str
