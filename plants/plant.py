class Plant:
    def __init__(self, *initial_data, **kwargs):
        self.name = None
        self.species = None
        self.last_watered = None
        self.watering_frequency = None
        self.watering_amount = None
        self.ph = None
        self.light = None
        self.humidity = None
        self.temperature = None

        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])
