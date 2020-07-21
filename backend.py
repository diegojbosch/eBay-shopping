from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

if __name__ == '__main__':
	app.run(debug=True)

@app.route('/search')
def homepage():
	return app.send_static_file("index.html")

#retrieve products from eBay API
@app.route('/api/v1.0/search', methods=['GET'])
def get_products():

	with open("token.txt", "r") as file:
		ebay_app_id = file.readline()

	ebay_api_url = 'https://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsAdvanced&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=' + ebay_app_id + '&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&paginationInput.entriesPerPage=5'
	item_filter_number = 0


	if request.args.get('keywords') is not None:
		ebay_api_url += '&keywords=' + request.args.get('keywords')

	if request.args.get('sort_order') is not None:
		ebay_api_url += '&sortOrder=' + request.args.get('sort_order')

 	if request.args.get('max_price') is not None:
 		ebay_api_url += '&itemFilter(' + str(item_filter_number) + ').name=MaxPrice&itemFilter(' + str(item_filter_number) + ').value=' + request.args.get('max_price') + '&itemFilter(0).paramName=Currency&itemFilter(0).paramValue=USD'
 		item_filter_number += 1

 	if request.args.get('min_price') is not None:
 		ebay_api_url += '&itemFilter(' + str(item_filter_number) + ').name=MinPrice&itemFilter(' + str(item_filter_number) + ').value=' + request.args.get('min_price') + '&itemFilter(1).paramName=Currency&itemFilter(1).paramValue=USD'
 		item_filter_number += 1

 	if request.args.get('return_accepted') == 'true':
 		ebay_api_url += '&itemFilter(' + str(item_filter_number) + ').name=ReturnsAcceptedOnly&itemFilter(' + str(item_filter_number) + ').value=true'
 		item_filter_number += 1

	if request.args.get('free_shipping') == 'true':
		ebay_api_url += '&itemFilter(' + str(item_filter_number) + ').name=FreeShippingOnly&itemFilter(' + str(item_filter_number) + ').value=true'
		item_filter_number += 1

	if request.args.get('expedited_shipping') == 'true':
		ebay_api_url += '&itemFilter(' + str(item_filter_number) + ').name=ExpeditedShippingType&itemFilter(' + str(item_filter_number) + ').value=Expedited'
		item_filter_number += 1

	condition_value_number = 0
	conditions_dict = {
		"new": "1000",
		"used": "3000",
		"very_good": "4000",
		"good": "5000",
		"acceptable": "6000"
	}

	for condition in conditions_dict:
		if request.args.get('condition_' + condition) == 'true':
			if condition_value_number == 0:
				ebay_api_url += '&itemFilter(' + str(item_filter_number) + ').name=Condition'

			ebay_api_url += '&itemFilter(' + str(item_filter_number) + ').value(' + str(condition_value_number) + ')=' + conditions_dict[condition]
			condition_value_number += 1

	response = requests.get(ebay_api_url)
	resp_json = response.json()
	findItems = resp_json.get('findItemsAdvancedResponse')

	if findItems[0].get('ack')[0] == 'Success':
		searchResult = findItems[0].get('searchResult')[0]
		paginationOutput = findItems[0].get('paginationOutput')[0]
		return jsonify({'status': 'Success', 'searchResult': searchResult, 'paginationOutput': paginationOutput})

	return jsonify({'status': 'Error', 'info': resp_json})
