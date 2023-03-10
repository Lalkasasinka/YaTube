class DataMixin:
    paginate_by = 10

    def get_user_context(self, **kwargs):
        context = kwargs
        return context
