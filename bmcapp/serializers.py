from rest_framework import serializers
from .models import Passenger


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        exclude = ('id',)

    def to_internal_value(self, data):
        """csv fields with empty values are imported as blank string, which is a problem for integer fields,
        this handles empty string as null"""
        age = data.get('Age', '')
        if not age:
            data['Age'] = None
        return super().to_internal_value(data)

    def get_fields(self):
        fields = super().get_fields()
        selected_fields = self.context.get('selected_fields')

        if selected_fields:
            filtered_fields = {}
            for field_name in selected_fields:
                if field_name in fields:
                    filtered_fields[field_name] = fields[field_name]
            fields = filtered_fields

        return fields
