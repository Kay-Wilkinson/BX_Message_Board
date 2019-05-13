import unittest
from mock import Mock, patch
from werkzeug.datastructures import Headers
from flask.ext.testing import TestCase 
from MessageBoard.unit_tests.base_test import BaseTestCase 

#Rewrite this as a class decoractor so I can simulate connection for other testcase classes
class Connect_API_Test(BaseTestCase):
    def create_mock_connection():
    	# some code here to mock connection
    	# test connection to api's like: https://api.spotxchange.com/1.0/Publisher(1234)/Deal(1234.5678)/DealReport?date_range=last_month
    	# see docs on developer.spotxchange.com/content/local/docs/apiDocs/platform/specs/campaign.md


class Data_Parsing_Test(Connect_API_Test):
	def mock_api_data(self):
		mock_api_name = Mock(name='get_reporting_api_data')
        mock_api_name.return_value = {
            {
			    "value": {
			        "data": [
			            {
			                "ad_errors": 0,
			                "ad_inits": 0,
			                "ad_start_fails": 0,
			                "ad_timeouts": 0,
			                "bid_class_name": "dynamic",
			                "clicks": 0,
			                "cpm": 0,
			                "ctr": 0,
			                "cvr": 0,
			                "date": "2016-12-27 00:00:00",
			                "deal_id": "1.2.3.4.5",
			                "deal_name": "A deal name",
			                "impressions": 0,
			                "media_timeouts": 0,
			                "publisher_id": 1234,
			                "revenue": 0,
			                "sell_through_rate": 0,
			                "tech_error_rate": 0,
			                "tech_errors": 0,
			                "total_connections": 7504,
			                "total_requests": 5365,
			                "total_responses": 0,
			                "uncovered_rate": 1,
			                "vast_opt_out_rate": 0.71,
			                "vast_opt_outs": 5365,
			                "vast_timeouts": 2139,
			                "vpaid_opt_out_rate": 0,
			                "vpaid_opt_outs": 0,
			                "wins": null
			            }
			        ]
			    }
		}
    }

    url = url_for('tracking.add_visit', site_id=site.id)
        wsgi_environment = {'REMOTE_ADDR': '1.2.3.4'}
        headers = Headers([('Referer', '/some/url')])
        #Rewrite the patch as a class decoractor so I can simulate this for other testcase classes
        with patch.object(views, 'get_geodata', mock_geodata):
            with self.client:
                self.client.get(url, environ_overrides=wsgi_environment,
                                headers=headers)

                visits = Visit.query.all()

                mock_geodata.assert_called_once_with('1.2.3.4')
                self.assertEqual(1, len(visits))

                first_visit = visits[0]
                self.assertEqual("/some/url", first_visit.url)
                self.assertEqual('Los Angeles, 90001', first_visit.location)
                self.assertEqual(34.05, first_visit.latitude)
                self.assertEqual(-118.25, first_visit.longitude)

