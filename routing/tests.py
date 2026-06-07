from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Node, Edge, RouteQueryHistory

class RoutingAPITests(APITestCase):
    def setUp(self):
        self.node_a = Node.objects.create(name="ServerA")
        self.node_b = Node.objects.create(name="ServerB")
        self.node_c = Node.objects.create(name="ServerC")
        self.node_d = Node.objects.create(name="ServerD")

        Edge.objects.create(source=self.node_a, destination=self.node_b, latency=10.0)
        Edge.objects.create(source=self.node_b, destination=self.node_d, latency=20.0)
        Edge.objects.create(source=self.node_a, destination=self.node_c, latency=5.0)
        Edge.objects.create(source=self.node_c, destination=self.node_d, latency=30.0)

    def test_create_node(self):
        url = reverse('node-list-create')
        data = {'name': 'ServerE'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Node.objects.count(), 5)

    def test_duplicate_node(self):
        url = reverse('node-list-create')
        data = {'name': 'ServerA'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_edge(self):
        url = reverse('edge-list-create')
        data = {
            'source': 'ServerA',
            'destination': 'ServerD',
            'latency': 50.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Edge.objects.count(), 5)

    def test_duplicate_edge(self):
        url = reverse('edge-list-create')
        data = {
            'source': 'ServerA',
            'destination': 'ServerB',
            'latency': 15.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_shortest_path_success(self):
        url = reverse('route-shortest')
        data = {
            'source': 'ServerA',
            'destination': 'ServerD'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_latency'], 30.0)
        self.assertEqual(response.data['path'], ['ServerA', 'ServerB', 'ServerD'])
        self.assertEqual(RouteQueryHistory.objects.count(), 1)

    def test_shortest_path_no_route(self):
        # ServerD has no outgoing edges connecting back to ServerA
        url = reverse('route-shortest')
        data = {
            'source': 'ServerD',
            'destination': 'ServerA'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_history_endpoint(self):
        RouteQueryHistory.objects.create(
            source_name='ServerA', destination_name='ServerD',
            total_latency=30.0, path=['ServerA', 'ServerB', 'ServerD']
        )
        url = reverse('route-history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_history_endpoint(self):
        RouteQueryHistory.objects.create(
            source_name='ServerA', destination_name='ServerD',
            total_latency=30.0, path=['ServerA', 'ServerB', 'ServerD']
        )
        RouteQueryHistory.objects.create(
            source_name='ServerA', destination_name='ServerC',
            total_latency=5.0, path=['ServerA', 'ServerC']
        )
        url = reverse('route-history')
        # Check filtering on destination ServerD
        response = self.client.get(url, {'destination': 'ServerD'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['destination_name'], 'ServerD')
