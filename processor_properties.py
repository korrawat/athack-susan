class ProcessorProperty:
    def __init__(self, label, default_value, min_value=None, max_value=None):
        self.label = label
        self.value = default_value
        self.default_value = default_value
        self._type = type(default_value)
        self.min_value = min_value
        self.max_value = max_value


    def update(self, value):
        if self._type == float:
            self.value = min(max(value, self.min_value), self.max_value)
        else:
            self.value = value


class ProcessorProperties:
    def __init__(self):
        self.brightness_factor = ProcessorProperty("Brightness", 1.0, 0.5, 2.0)
        self.contrast_factor = ProcessorProperty("Contrast", 1.0, 0.5, 2.0)
        self.grayscale = ProcessorProperty("Grayscale", False)


# example usage:
# props = ProcessorProperties()
#
# updating value
# props.brightness_factor.update(1.5)
# 
# reading value
# brightness_factor = props.brightness_factor.value
