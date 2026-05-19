"""
Serializers for the Personnel API using Django REST Framework.
"""

from rest_framework import serializers
from personnel.models import Person, Role


class RoleSerializer(serializers.ModelSerializer):
    job_type = serializers.StringRelatedField()
    organization = serializers.StringRelatedField()

    class Meta:
        model = Role
        fields = ['job_type', 'organization', 'start_date', 'end_date']


class PersonSerializer(serializers.ModelSerializer):
    lab_roles = RoleSerializer(many=True, read_only=True)
    publications = serializers.SerializerMethodField()
    absolute_url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Person
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'biography',
            'image',
            'website',
            'orcid_id',
            'lab_roles',
            'publications',
            'absolute_url',
        ]

    def get_publications(self, obj):
        from papers.models import Publication
        pubs = Publication.objects.filter(
            authors__author=obj,
            laboratory_paper=True,
        ).distinct().order_by('-year')
        return [
            {
                'id': p.id,
                'title': p.title,
                'year': p.year,
                'journal': p.journal,
                'doi': p.doi,
                'absolute_url': p.get_absolute_url(),
            }
            for p in pubs
        ]


class PersonListSerializer(PersonSerializer):
    """Optimized serializer for person lists — omits biography."""

    class Meta(PersonSerializer.Meta):
        fields = [
            'id',
            'first_name',
            'last_name',
            'image',
            'website',
            'orcid_id',
            'lab_roles',
            'absolute_url',
        ]
