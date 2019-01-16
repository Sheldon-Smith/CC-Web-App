from django.db.models import BooleanField


class UniqueBooleanField(BooleanField):
    def pre_save(self, model_instance, add):
        objects = model_instance.__class__.objects
        # If True set all others to False
        if getattr(model_instance, self.attname):
            objects.update(**{self.attname: False})
        # If no true object exists that is saved, set as true
        elif not objects.exclude(id=model_instance.id).filter(**{self.attname: True}):
            return True
        return getattr(model_instance, self.attname)
