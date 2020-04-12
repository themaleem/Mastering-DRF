from django.utils.http import urlencode
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from drones import views
from drones.models import DroneCategory,Pilot
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class DroneCategoryTests(APITestCase):
    def post_drone_category(self, name):
        url = reverse(views.DroneCategoryList.name)
        data = {'name': name}
        response = self.client.post(url, data, format='json')
        return response

    def test_post_and_get_drone_category(self):
        """
        Ensure we can create a new DroneCategory and then retrieve it
        """
        new_drone_category_name = 'Hexacopter'
        response = self.post_drone_category(new_drone_category_name)
        print("PK {0}".format(DroneCategory.objects.get().pk))
        assert response.status_code == status.HTTP_201_CREATED
        assert DroneCategory.objects.count() == 1
        assert DroneCategory.objects.get().name == new_drone_category_name

    def test_post_existing_drone_category_name(self):
        """
        Ensure we cannot create a DroneCategory with an existing name
        """
        url = reverse(views.DroneCategoryList.name)
        new_drone_category_name = 'Duplicated Copter'
        data = {'name': new_drone_category_name}
        response1 = self.post_drone_category(new_drone_category_name)
        # print(response1.data)
        assert response1.status_code == status.HTTP_201_CREATED
        response2 = self.post_drone_category(new_drone_category_name)
        print(response2)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST

    def test_filter_drone_category_by_name(self):
        """
        Ensure we can filter a drone category by name
        """
        drone_category_name1 = 'Hexacopter'
        self.post_drone_category(drone_category_name1)
        drone_caregory_name2 = 'Octocopter'
        self.post_drone_category(drone_caregory_name2)
        filter_by_name = { 'name' : drone_category_name1 }
        url = '{0}?{1}'.format(
            reverse(views.DroneCategoryList.name),
            urlencode(filter_by_name))
        print(url)
        response = self.client.get(url, format='json')
        # print(response.data)
        assert response.status_code == status.HTTP_200_OK
        # Make sure we receive only one element in the response
        assert response.data['count'] == 1
        assert response.data['results'][0]['name'] == drone_category_name1

    def test_get_drone_categories_collection(self):
        """
        Ensure we can retrieve the drone categories collection
        """
        new_drone_category_name = 'Super Copter'
        self.post_drone_category(new_drone_category_name)
        url = reverse(views.DroneCategoryList.name)
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        # Make sure we receive only one element in the response
        assert response.data['count'] == 1
        assert response.data['results'][0]['name'] == new_drone_category_name

    def test_update_drone_category(self):
        """
        Ensure we can update a single field for a drone category
        """
        drone_category_name = 'Category Initial Name'
        response = self.post_drone_category(drone_category_name)
        url = reverse(
            views.DroneCategoryDetail.name,
            None,
            {response.data['pk']})
        updated_drone_category_name = 'Updated Name'
        data = {'name': updated_drone_category_name}
        patch_response = self.client.patch(url, data, format='json')
        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data['name'] == updated_drone_category_name

    def test_get_drone_category(self):
        """
        Ensure we can get a single drone category by id
        """
        drone_category_name = 'Easy to retrieve'
        response = self.post_drone_category(drone_category_name)
        url = reverse(
            views.DroneCategoryDetail.name,
            None,
            {response.data['pk']})
        get_response = self.client.get(url, format='json')
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data['name'] == drone_category_name

class PilotTests(APITestCase):
    def post_pilot(self,name,gender,races_count):
        url = reverse(views.PilotList.name)
        data = {
            'name': name,
            'gender': gender,
            'races_count': races_count,
            }
        response = self.client.post(url, data, format='json')
        return response

    def create_user_and_set_token_credentials(self):
        user = User.objects.create_user(
            'olumide', 
            'olu@example.com', 
            'P4ssw0rD'
            )
        token = Token.objects.create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token {0}'.format(token.key)
            )
    def test_post_get_patch_and_delete_pilot(self):
        """
        Ensure we can create a new Pilot and then retrieve it
        Ensure we cannot retrieve the persisted pilot without a token
        Ensure we can partially update existing pilot instance
        Ensure we can delete existing pilot instance
        """
        self.create_user_and_set_token_credentials()
        pilot_name = 'Olumide'
        pilot_gender = Pilot.MALE
        pilot_races_count = 5
        response = self.post_pilot(
            pilot_name,
            pilot_gender,
            pilot_races_count
            )
        print("PK {0}".format(Pilot.objects.get().pk))
        assert response.status_code == status.HTTP_201_CREATED
        assert Pilot.objects.count() == 1

        # retrieve pilot
        saved_pilot = Pilot.objects.get()
        assert saved_pilot.name == pilot_name
        assert saved_pilot.gender == pilot_gender
        assert saved_pilot.races_count == pilot_races_count
        # retrieve pilot detail with pk
        url= reverse(
            views.PilotDetail.name,
            None,
            {saved_pilot.pk})
        authorized_get_response=self.client.get(url,format='json')
        assert authorized_get_response.status_code == status.HTTP_200_OK
        assert authorized_get_response.data['name'] == pilot_name
        assert authorized_get_response.data['gender'] == pilot_gender
        
        # patching pilot instance
        new_pilot_name = "Olu Bello"
        data={
            'name': new_pilot_name
        }
        updated_pilot_response = self.client.patch(
            url,
            data,
            format='json'
            )
        assert updated_pilot_response.status_code == status.HTTP_200_OK
        assert updated_pilot_response.data['name'] == new_pilot_name
        # delete instance
        delete_instance=self.client.delete(url,format='json')
        assert delete_instance.status_code == status.HTTP_204_NO_CONTENT
        assert Pilot.objects.count()==0
        
        # This cleans up the set credentials
        self.client.credentials()
        
        unauthorized_get_response= self.client.get(url,format='json')
        assert unauthorized_get_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_try_post_pilot_without_token(self):
        """
        Ensure we cannot post pilot 
        without token
        """
        pilot_name='maleem'
        pilot_gender=Pilot.MALE
        races_count= 6
        response=self.post_pilot(
            pilot_name,
            pilot_gender,
            races_count
        )
        assert response.status_code==status.HTTP_401_UNAUTHORIZED
        assert Pilot.objects.count() == 0
    
    def test_try_to_post_existing_pilot(self):
        """
        Ensure we cannot post pilot
        with same name twice
        """
        pilot_name_1="maleem"
        pilot_name_2="maleem"
        gender=Pilot.FEMALE
        races_count= 7
        self.create_user_and_set_token_credentials()
        response=self.post_pilot(
            pilot_name_1,
            gender,
            races_count
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Pilot.objects.get().name == pilot_name_1

        new_response = self.post_pilot(
            pilot_name_2,
            gender,
            races_count
        )
        assert new_response.status_code != status.HTTP_201_CREATED
    
    def test_search_existing_pilots(self):
        """
        Ensure we can filter pilots
        with search query parameter
        """
        pilot_name_1="maleem"
        pilot_name_2="maleem2"
        pilot_name_3="olumide"
        gender=Pilot.FEMALE
        races_count= 7
        self.create_user_and_set_token_credentials()
        response=self.post_pilot(
            pilot_name_1,
            gender,
            races_count
        )
        assert response.status_code == status.HTTP_201_CREATED

        response2 = self.post_pilot(
            pilot_name_2,
            gender,
            races_count
        )
        assert response2.status_code == status.HTTP_201_CREATED
        response3 = self.post_pilot(
            pilot_name_3,
            gender,
            races_count
        )
        assert response3.status_code == status.HTTP_201_CREATED
        assert Pilot.objects.count() == 3
        assert response.data['name'] == pilot_name_1 
        assert response2.data['name'] == pilot_name_2 
        assert response3.data['name'] == pilot_name_3

        search_startswith = { 'search' : 'ma' }
        url = '{0}?{1}'.format(
            reverse(views.PilotList.name),
            urlencode(search_startswith))

        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        # Make sure we receive only two element in the response
        assert response.data['count'] == 2
