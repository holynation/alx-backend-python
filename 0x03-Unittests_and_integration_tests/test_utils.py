#!/usr/bin/env python3
"""
This section of the module contains a python unit test for utils
"""
import requests
import unittest
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized
from unittest.mock import patch


class TestAccessNestedMap(unittest.TestCase):
    """
    this class is for testing access_nested_map method/function
    """
    @parameterized.expand([
        ({"a": 3}, ("a",), 3),
        ({"a": {"b": 4}}, ("a",), {"b": 4}),
        ({"a": {"b": 6}}, ("a", "b"), 6)
    ])
    def test_access_nested_map(self, nested_map, path, result):
        """
        this method test the access_nested_map function
        """
        self.assertEqual(access_nested_map(nested_map, path), result)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        this method tests wrong/invalid inputs that raise Exception
        """
        with self.assertRaises(Exception) as ex:
            access_nested_map(nested_map, path)


class TestMemoize(unittest.TestCase):
    """Test class for memoize function"""
    def test_memoize(self):
        """function to test memoize method"""
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock:
            test = TestClass()
            test.a_property()
            test.a_property()
            mock.assert_called_once()


class TestGetJson(unittest.TestCase):
    """
    This is test class for get_json() function
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, url, payload):
        """this function test the get_json() method"""
        with patch('requests.get') as mock_req:
            mock_req.return_value.json.return_value = payload
            self.assertEqual(get_json(url), payload)
