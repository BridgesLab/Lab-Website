"""
Serializers for the Papers API using Django REST Framework.

This module provides serializers for the Publication model, converting
between Django model instances and JSON representations.
"""

from rest_framework import serializers
from papers.models import Publication

class PublicationSerializer(serializers.ModelSerializer):
    """
    Serializer for Publication model instances.
    
    Provides JSON representation of Publication objects with all relevant
    fields including metadata, identifiers, and publication details.
    
    Fields:
        - id: Database primary key
        - title: Publication title
        - title_slug: URL-friendly title
        - abstract: Publication abstract/summary
        - authors: List of publication authors
        - journal: Journal name
        - year: Publication year
        - volume: Journal volume
        - issue: Journal issue
        - pages: Page range
        - type: Publication type (journal-article, book-section, etc.)
        - doi: Digital Object Identifier
        - pmid: PubMed ID
        - pmcid: PubMed Central ID
        - mendeley_id: Mendeley identifier
        - mendeley_url: Mendeley URL
        - laboratory_paper: Whether paper is from this laboratory
        - interesting_paper: Whether paper is marked as interesting
        - date_added: Date added to database
        - date_last_modified: Last modification date
        - absolute_url: URL path to publication page
    """
    
    absolute_url = serializers.CharField(read_only=True)
    
    class Meta:
        model = Publication
        fields = [
            'id',
            'title',
            'title_slug',
            'abstract',
            'journal',
            'year',
            'volume',
            'issue',
            'pages',
            'type',
            'doi',
            'pmid',
            'pmcid',
            'mendeley_id',
            'mendeley_url',
            'laboratory_paper',
            'interesting_paper',
            'date_added',
            'date_last_modified',
            'absolute_url',
        ]
        read_only_fields = [
            'id',
            'title_slug',
            'date_added',
            'date_last_modified',
            'absolute_url',
        ]


class PublicationListSerializer(PublicationSerializer):
    """
    Optimized serializer for Publication lists.
    
    Excludes large text fields like abstract for better performance
    when returning multiple publications.
    """
    
    class Meta(PublicationSerializer.Meta):
        fields = [
            'id',
            'title',
            'title_slug',
            'journal',
            'year',
            'volume',
            'issue',
            'pages',
            'type',
            'doi',
            'pmid',
            'pmcid',
            'laboratory_paper',
            'interesting_paper',
            'date_added',
            'date_last_modified',
            'absolute_url',
        ]