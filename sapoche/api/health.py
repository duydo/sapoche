from flask_restful import Resource
from . import api

__author__ = 'duydo'


@api.resource('/health')
class HealthCheck(Resource):

    def get(self):
        return {
            'status': 'OK'
        }
