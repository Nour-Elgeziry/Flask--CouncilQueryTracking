""" UserService to UserAPI"""
import requests


class AdvisorService:
    @staticmethod
    def get_advisors():
        response = requests.get('http://localhost:5001')
        advisors = response.json()
        return advisors

    @staticmethod
    def get_advisor(key):
        response = requests.request(method="GET", url='http://localhost:5001/' + key)
        advisor = response.json()
        return advisor




