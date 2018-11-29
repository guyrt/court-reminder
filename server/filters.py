from flask_admin.model.filters import BaseFilter


class EqualFilter(BaseFilter):
    def __init__(self, column, name, options=None, data_type=None):
        super(EqualFilter, self).__init__(name, options, data_type)
        self.column = column

    def apply(self, query, value):
        raise NotImplementedError('Search is not implemeted in Azure Table')

    def operation(self):
        return 'equals'

    def validate(self, value):
        return True

    def clean(self, value):
        return value.strip()
