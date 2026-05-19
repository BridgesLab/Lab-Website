"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from datetime import date

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from personnel.models import Person, JobPosting, Organization, Role, JobType, Degree
from personnel.admin import CurrentLabMemberAdmin, CurrentLabMember
from personnel.serializers import PersonSerializer, PersonListSerializer, RoleSerializer
from lab_website.tests import BasicTests
from personnel.sitemap import LabPersonnelSitemap
from django.test import RequestFactory

MODELS = [Person, JobPosting]

class PersonnelModelTests(BasicTests):
    """Tests the model attributes of ::class:`Personnel` objects contained in the ::mod:`personnel` app."""
    
    fixtures = ['test_personnel']
    
    def test_full_name(self):
        '''This is a test for the rendering of the full name from a ::class:`Person` object.'''
        fixture_personnel = Person.objects.get(first_name='John', last_name='Doe') 
        self.assertEqual(fixture_personnel.full_name(), 'John Doe')        
    
    def test_name_slug(self):
        '''This is a test for the rendering of the name_slug field from a ::class:`Person` object.'''
        fixture_personnel = Person.objects.get(first_name='John', last_name='Doe') 
        self.assertEqual(fixture_personnel.name_slug, 'john-doe')   

    def test_personnel_permalink(self):
        '''This is a test that the permalink for a ::class:`Person` object is correctly rendered as **/personnel/<name_slug>**'''
        fixture_personnel = Person.objects.get(first_name='John', last_name='Doe') 
        self.assertEqual(fixture_personnel.get_absolute_url(), '/people/john-doe/')          
    
    def test_create_labmember_minimal(self):
        '''This is a test for creating a new ::class:`Person` object, with only the minimum fields being entered'''
        test_labmember = Person(first_name = 'Joe',
        	last_name = 'Blow', alumni=False, current_lab_member=True)
        test_labmember.save()
        #test that the slugfiy function works correctly
        self.assertEqual(test_labmember.name_slug, 'joe-blow')

class JobTypeModelTests(BasicTests):

    fixtures = ['test_personnel.json', 'test_roles.json']
    
    def test_jobtype_str_representation(self):
        """Test string representation of JobType"""
        job_type = JobType.objects.create(
            job_title="Research Assistant",
            trainee_status=True,
            student_status=True,
            employee_status=False
        )
        self.assertEqual(str(job_type), "Research Assistant")
    
    def test_jobtype_creation_with_all_fields(self):
        """Test JobType creation with all boolean fields"""
        job_type = JobType.objects.create(
            job_title="Graduate Student",
            trainee_status=True,
            student_status=True,
            employee_status=False
        )
        self.assertEqual(job_type.job_title, "Graduate Student")
        self.assertTrue(job_type.trainee_status)
        self.assertTrue(job_type.student_status)
        self.assertFalse(job_type.employee_status)
    
    def test_jobtype_employee_status(self):
        """Test JobType for employee positions"""
        job_type = JobType.objects.create(
            job_title="Lab Manager",
            trainee_status=False,
            student_status=False,
            employee_status=True
        )
        self.assertEqual(str(job_type), "Lab Manager")
        self.assertFalse(job_type.trainee_status)
        self.assertFalse(job_type.student_status)
        self.assertTrue(job_type.employee_status)


class RoleModelTests(BasicTests):

    fixtures = ['test_personnel.json', 'test_roles.json']
    
    def setUp(self):
        """Set up test dependencies"""
        # Create test JobType
        self.job_type = JobType.objects.create(
            job_title="Research Assistant",
            trainee_status=True,
            student_status=True,
            employee_status=False
        )
        
        # Create test Organization
        self.organization = Organization.objects.create(name="Test University")
    
    def test_role_str_with_start_date_only(self):
        """Test string representation with only start date"""
        role = Role.objects.create(
            job_type=self.job_type,
            organization=self.organization,
            start_date=date(2023, 1, 15),
            end_date=None,
            public=True
        )
        expected = f"<strong>{self.job_type}</strong>, {self.organization} since 2023-01-15"
        self.assertEqual(str(role), expected)
    
    def test_role_str_with_end_date_only(self):
        """Test string representation with only end date"""
        role = Role.objects.create(
            job_type=self.job_type,
            organization=self.organization,
            start_date=None,
            end_date=date(2023, 12, 31),
            public=True
        )
        expected = f"<strong>{self.job_type}</strong>, {self.organization} until 2023-12-31"
        self.assertEqual(str(role), expected)
    
    def test_role_str_with_both_dates(self):
        """Test string representation with both start and end dates"""
        role = Role.objects.create(
            job_type=self.job_type,
            organization=self.organization,
            start_date=date(2023, 1, 15),
            end_date=date(2023, 12, 31),
            public=True
        )
        expected = f"<strong>{self.job_type}</strong>, {self.organization} from 2023-01-15 to 2023-12-31"
        self.assertEqual(str(role), expected)
    
    def test_role_str_with_no_dates(self):
        """Test string representation with no dates"""
        role = Role.objects.create(
            job_type=self.job_type,
            organization=self.organization,
            start_date=None,
            end_date=None,
            public=True
        )
        expected = f"<strong>{self.job_type}</strong>, {self.organization}"
        self.assertEqual(str(role), expected)            

class PersonnelViewTests(BasicTests):
    """Tests the views of ::class:`Personnel` objects contained in the ::mod:`personnel` app."""
    
    fixtures = ['test_personnel','test_address','test_labaddress']

    def test_fixture_loaded(self):
        people = Person.objects.filter(current_lab_member=True)
        self.assertTrue(people.exists())
    
    def test_laboratory_personnel(self):
        '''This function tests the laboratory-personnel view.''' 
        
        test_response = self.client.get('/people/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('personnel' in test_response.context)
        self.assertTemplateUsed(test_response, 'personnel_list.html')
        self.assertEqual(test_response.context['personnel_type'], 'current')
        self.assertEqual(test_response.context['personnel'][0].pk, 1)
        self.assertEqual(test_response.context['personnel'][0].first_name, 'John')        
        self.assertEqual(test_response.context['personnel'][0].last_name, 'Doe')  

    def test_personnel_detail(self):
        '''This function tests the personnel-details view.''' 
        
        test_response = self.client.get('/people/john-doe/')

        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('person' in test_response.context)
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'personnel_detail.html')
        self.assertEqual(test_response.context['person'].pk, 1)
        self.assertEqual(test_response.context['person'].first_name, 'John')        
        self.assertEqual(test_response.context['person'].last_name, 'Doe')

          
class JobPostingModelTests(BasicTests):
    """Tests the model attributes of ::class:`JobPosting` objects contained in the ::mod:`personnel` app."""
   
    fixtures = ['test_organization',]

    def test_create_jobposting_minimal(self):
        '''This is a test for creating a new ::class:`JobPosting` object, with only the minimum fields being entered'''
        test_jobposting = JobPosting(title = 'Postdoctoral Researcher',
                              description = 'Some description',
                              link = 'http:/jobs.com/awesomejob',
                              active=True)
        test_jobposting.save()
        self.assertEqual(test_jobposting.pk, 1)    

    def test_create_jobposting_all(self):
        '''This is a test for creating a new ::class:`JobPosting` object, with only the minimum fields being entered'''
        test_jobposting = JobPosting(title = 'Postdoctoral Researcher',
                              description = 'Some description',
                              link = 'http:/jobs.com/awesomejob',
                              hiringOrganization = Organization.objects.get(pk=1),
                              education = "An educational requirement",
                              qualifications = "Some qualifications",
                              responsibilities = "Some responsibilities",
                              active = True)
        test_jobposting.save()
        self.assertEqual(test_jobposting.pk, 1)

    def test_jobposting_string(self):
        '''This test creates a new :class:`~personnel.models.JobPosting` object, then tests for the string representation of it.'''
        test_jobposting = JobPosting(title = 'Postdoctoral Researcher',
                              description = 'Some description',
                              link = 'http:/jobs.com/awesomejob',
                              active=True)
        test_jobposting.save()
        self.assertEqual(str(test_jobposting), 'Postdoctoral Researcher Job Posting (%s)' %(date.today()) )

    def test_jobposting_expiry_default(self):
        """expiry() defaults to 30 days when duration is None."""
        import datetime
        org = Organization.objects.get(pk=1)
        posting = JobPosting(title='Test', description='desc', link='http://example.com',
                             hiringOrganization=org, active=True)
        posting.save()
        self.assertEqual(posting.expiry(), posting.created + datetime.timedelta(30))

    def test_jobposting_expiry_with_duration(self):
        """expiry() uses duration when set."""
        import datetime
        org = Organization.objects.get(pk=1)
        posting = JobPosting(title='Test2', description='desc', link='http://example.com',
                             hiringOrganization=org, active=True, duration=60)
        posting.save()
        self.assertEqual(posting.expiry(), posting.created + datetime.timedelta(60))

    def test_jobposting_base_salary_term_upper_none(self):
        """base_salary_term_upper() returns None when base_salary_term is not set."""
        org = Organization.objects.get(pk=1)
        posting = JobPosting(title='Test3', description='desc', link='http://example.com',
                             hiringOrganization=org, active=True)
        posting.save()
        self.assertIsNone(posting.base_salary_term_upper())

    def test_jobposting_base_salary_term_upper(self):
        """base_salary_term_upper() returns the uppercased salary term."""
        org = Organization.objects.get(pk=1)
        posting = JobPosting(title='Test4', description='desc', link='http://example.com',
                             hiringOrganization=org, active=True, base_salary_term='yearly')
        posting.save()
        self.assertEqual(posting.base_salary_term_upper(), 'YEARLY')


class DegreeModelTests(BasicTests):
    """Tests for the Degree model."""

    fixtures = ['test_organization']

    def test_degree_string(self):
        """Degree __str__ returns abbreviation and organization."""
        org = Organization.objects.get(pk=1)
        degree = Degree(degree='Doctor of Philosophy', field_of_study='Biochemistry',
                        abbreviation='Ph.D.', organization=org)
        degree.save()
        self.assertEqual(str(degree), 'Ph.D. (%s)' % str(org))


class AlumniViewTests(BasicTests):
    """Tests for the LaboratoryAlumniList view."""

    fixtures = ['test_personnel', 'test_address', 'test_labaddress']

    def test_alumni_view_returns_200(self):
        """Alumni list view returns 200."""
        response = self.client.get('/people/alumni/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_alumni_view_uses_correct_template(self):
        """Alumni list view uses the personnel-list template."""
        response = self.client.get('/people/alumni/', follow=True)
        self.assertTemplateUsed(response, 'personnel_list.html')

    def test_alumni_view_context_personnel_type(self):
        """Alumni list view sets personnel_type to 'alumni' in context."""
        response = self.client.get('/people/alumni/', follow=True)
        self.assertEqual(response.context['personnel_type'], 'alumni')


class PersonnelSitemapTests(BasicTests):
    """Tests for the LabPersonnelSitemap."""

    fixtures = ['test_personnel']

    def test_sitemap_items_only_current_members(self):
        """LabPersonnelSitemap.items() returns only current lab members."""
        sitemap = LabPersonnelSitemap()
        items = list(sitemap.items())
        self.assertTrue(all(p.current_lab_member for p in items))

    def test_sitemap_items_excludes_former_members(self):
        """LabPersonnelSitemap.items() excludes non-current members."""
        sitemap = LabPersonnelSitemap()
        all_people = Person.objects.count()
        sitemap_count = sitemap.items().count()
        current_count = Person.objects.filter(current_lab_member=True).count()
        self.assertEqual(sitemap_count, current_count)

    def test_sitemap_lastmod_returns_updated(self):
        """LabPersonnelSitemap.lastmod() returns person.updated."""
        sitemap = LabPersonnelSitemap()
        person = Person.objects.filter(current_lab_member=True).first()
        if person:
            self.assertEqual(sitemap.lastmod(person), person.updated)


class CurrentLabMemberAdminTests(BasicTests):
    """Tests for CurrentLabMemberAdmin custom methods."""

    fixtures = ['test_personnel.json', 'test_roles.json']

    def setUp(self):
        super().setUp()
        self.admin = CurrentLabMemberAdmin(CurrentLabMember, None)
        self.job_type = JobType.objects.create(
            job_title="Research Assistant",
            trainee_status=True,
            student_status=True,
            employee_status=False,
        )
        self.organization = Organization.objects.create(name="Test University")

    def test_get_queryset_only_current_members(self):
        """get_queryset returns only current lab members."""
        request = RequestFactory().get('/')
        qs = self.admin.get_queryset(request)
        self.assertTrue(all(p.current_lab_member for p in qs))

    def test_get_queryset_excludes_alumni(self):
        """get_queryset excludes people where current_lab_member=False."""
        alumni = Person.objects.create(
            first_name="Former", last_name="Member",
            current_lab_member=False, alumni=True,
        )
        request = RequestFactory().get('/')
        qs = self.admin.get_queryset(request)
        self.assertNotIn(alumni, qs)

    def test_lab_roles_display_with_roles(self):
        """lab_roles_display returns comma-separated role strings."""
        person = Person.objects.get(first_name="John", last_name="Doe")
        role = Role.objects.create(
            job_type=self.job_type,
            organization=self.organization,
            public=True,
        )
        person.lab_roles.add(role)
        result = self.admin.lab_roles_display(person)
        self.assertIn(str(role), result)

    def test_lab_roles_display_no_roles(self):
        """lab_roles_display returns 'None' when person has no lab roles."""
        person = Person.objects.get(first_name="John", last_name="Doe")
        person.lab_roles.clear()
        result = self.admin.lab_roles_display(person)
        self.assertEqual(result, "None")


class PersonViewSetTest(APITestCase):
    """Tests for the PersonViewSet API at /api/v2/people/."""

    def setUp(self):
        self.org = Organization.objects.create(
            name="University of Michigan",
            department="Nutritional Sciences",
            type="Academic",
        )
        self.job_type = JobType.objects.create(
            job_title="Graduate Student",
            trainee_status=True,
            student_status=True,
            employee_status=False,
        )
        self.current_member = Person.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            biography="A biography.",
            current_lab_member=True,
            alumni=False,
        )
        self.former_member = Person.objects.create(
            first_name="Bob",
            last_name="Jones",
            current_lab_member=False,
            alumni=True,
        )

    def test_list_returns_200(self):
        """GET /api/v2/people/ returns 200."""
        url = reverse('api-person-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_only_current_members(self):
        """List endpoint excludes non-current lab members."""
        url = reverse('api-person-list')
        response = self.client.get(url)
        ids = [r['id'] for r in response.data['results']]
        self.assertIn(self.current_member.pk, ids)
        self.assertNotIn(self.former_member.pk, ids)

    def test_list_excludes_biography(self):
        """List endpoint uses PersonListSerializer — no biography field."""
        url = reverse('api-person-list')
        response = self.client.get(url)
        self.assertNotIn('biography', response.data['results'][0])

    def test_detail_returns_200(self):
        """GET /api/v2/people/{id}/ returns 200 for a current member."""
        url = reverse('api-person-detail', kwargs={'pk': self.current_member.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_includes_biography(self):
        """Detail endpoint uses PersonSerializer — includes biography."""
        url = reverse('api-person-detail', kwargs={'pk': self.current_member.pk})
        response = self.client.get(url)
        self.assertIn('biography', response.data)
        self.assertEqual(response.data['biography'], 'A biography.')

    def test_detail_404_for_former_member(self):
        """Detail endpoint returns 404 for a non-current lab member."""
        url = reverse('api-person-detail', kwargs={'pk': self.former_member.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_404_for_nonexistent(self):
        """Detail endpoint returns 404 for a non-existent pk."""
        url = reverse('api-person-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_json_format(self):
        """List endpoint serves JSON content type."""
        url = reverse('api-person-list')
        response = self.client.get(url, {'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_list_ordered_by_last_name(self):
        """List endpoint returns people ordered by last_name by default."""
        Person.objects.create(first_name="Alice", last_name="Aardvark",
                              current_lab_member=True, alumni=False)
        url = reverse('api-person-list')
        response = self.client.get(url)
        last_names = [r['last_name'] for r in response.data['results']]
        self.assertEqual(last_names, sorted(last_names))

    def test_detail_includes_lab_roles(self):
        """Detail endpoint includes lab_roles with job_type and organization."""
        role = Role.objects.create(
            job_type=self.job_type,
            organization=self.org,
            public=True,
        )
        self.current_member.lab_roles.add(role)
        url = reverse('api-person-detail', kwargs={'pk': self.current_member.pk})
        response = self.client.get(url)
        self.assertIn('lab_roles', response.data)
        self.assertEqual(len(response.data['lab_roles']), 1)
        self.assertEqual(response.data['lab_roles'][0]['job_type'], 'Graduate Student')

    def test_detail_publications_only_lab_papers(self):
        """Publications in the detail response only include laboratory_paper=True."""
        from papers.models import Publication, AuthorDetails
        lab_pub = Publication.objects.create(
            title="Lab Paper", year=2023, laboratory_paper=True,
            interesting_paper=False, preprint=False,
        )
        non_lab_pub = Publication.objects.create(
            title="External Paper", year=2022, laboratory_paper=False,
            interesting_paper=False, preprint=False,
        )
        author_detail_lab = AuthorDetails.objects.create(
            author=self.current_member, order=1,
            corresponding_author=True, equal_contributors=False,
        )
        author_detail_ext = AuthorDetails.objects.create(
            author=self.current_member, order=1,
            corresponding_author=False, equal_contributors=False,
        )
        lab_pub.authors.add(author_detail_lab)
        non_lab_pub.authors.add(author_detail_ext)

        url = reverse('api-person-detail', kwargs={'pk': self.current_member.pk})
        response = self.client.get(url)
        pub_titles = [p['title'] for p in response.data['publications']]
        self.assertIn('Lab Paper', pub_titles)
        self.assertNotIn('External Paper', pub_titles)

    def test_detail_includes_absolute_url(self):
        """Detail endpoint includes absolute_url for the person."""
        url = reverse('api-person-detail', kwargs={'pk': self.current_member.pk})
        response = self.client.get(url)
        self.assertIn('absolute_url', response.data)
        self.assertIn('jane-smith', response.data['absolute_url'])


class PersonSerializerTest(APITestCase):
    """Unit tests for PersonSerializer and PersonListSerializer."""

    def setUp(self):
        self.person = Person.objects.create(
            first_name="Jane",
            last_name="Smith",
            biography="Bio text.",
            current_lab_member=True,
            alumni=False,
        )

    def test_list_serializer_excludes_biography(self):
        """PersonListSerializer does not include biography."""
        serializer = PersonListSerializer(self.person)
        self.assertNotIn('biography', serializer.data)

    def test_detail_serializer_includes_biography(self):
        """PersonSerializer includes biography."""
        serializer = PersonSerializer(self.person)
        self.assertIn('biography', serializer.data)
        self.assertEqual(serializer.data['biography'], 'Bio text.')

    def test_detail_serializer_includes_publications_field(self):
        """PersonSerializer includes a publications list."""
        serializer = PersonSerializer(self.person)
        self.assertIn('publications', serializer.data)
        self.assertIsInstance(serializer.data['publications'], list)

    def test_role_serializer_fields(self):
        """RoleSerializer exposes job_type, organization, start_date, end_date."""
        org = Organization.objects.create(
            name="UM", department="Nutritional Sciences", type="Academic"
        )
        job_type = JobType.objects.create(
            job_title="Postdoc", trainee_status=True,
            student_status=False, employee_status=True,
        )
        role = Role.objects.create(
            job_type=job_type, organization=org,
            start_date=date(2022, 1, 1), public=True,
        )
        serializer = RoleSerializer(role)
        self.assertEqual(serializer.data['job_type'], 'Postdoc')
        self.assertIn('start_date', serializer.data)
        self.assertIn('end_date', serializer.data)
