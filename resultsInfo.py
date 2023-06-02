class BinaryClassification:
    def __init__(self):
        self.sensitivity = None
        self.specificity = None
        self.accuracy = None
        self.precision = None
        self.f1_score = None
        self.execution_time = None
        self.result = None


class MultiClassification:
    def __init__(self):
        self.execution_time = None
        self.confusion_matrix = None
        self.mean_sensitivity = None
        self.mean_specificity = None
        self.result = None
