from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

if __name__ == '__main__':
	app.run(debug=True)

@app.route('/')
def homepage():
	return app.send_static_file("index.html")

#retrieve products from eBay API
@app.route('/api/v1.0/search', methods=['GET'])
def get_products():

	with open("token.txt", "r") as file:
		ebay_app_id = file.readline()

	ebay_api_url = 'https://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsAdvanced&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=' + ebay_app_id + '&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&paginationInput.entriesPerPage=5'
	item_filter_number = 0


	if request.args.get('keyword') is not None:
		ebay_api_url += '&keywords=' + request.args.get('keyword')

	if request.args.get('sortOrder') is not None:
		ebay_api_url += '&sortOrder=' + request.args.get('sortOrder')
 
 	if request.args.get('maxPrice') is not None:
 		ebay_api_url += '&itemFilter(' + str(item_filter_number) + ').name=MaxPrice&itemFilter(' + str(item_filter_number) + ').value=' + request.args.get('maxPrice') + '&itemFilter(0).paramName=Currency&itemFilter(0).paramValue=USD'
 		item_filter_number += 1

 	if request.args.get('minPrice') is not None:
 		ebay_api_url += '&itemFilter(' + str(item_filter_number) + ').name=MinPrice&itemFilter(' + str(item_filter_number) + ').value=' + request.args.get('minPrice') + '&itemFilter(1).paramName=Currency&itemFilter(1).paramValue=USD'
 		item_filter_number += 1

 	if request.args.get('returnsAccepted') is not None:
 		ebay_api_url += '&itemFilter(' + str(item_filter_number) + ').name=ReturnsAcceptedOnly&itemFilter(' + str(item_filter_number) + ').value=' + request.args.get('returnsAccepted')
 		item_filter_number += 1
	 
	if request.args.get('freeShipping') is not None:
		ebay_api_url += '&itemFilter(' + str(item_filter_number) + ').name=FreeShippingOnly&itemFilter(' + str(item_filter_number) + ').value=' + request.args.get('freeShipping')
		item_filter_number += 1

	#only add item filter if value is Expedited
	if request.args.get('expeditedShipping') == 'Expedited': 
		ebay_api_url += '&itemFilter(' + str(item_filter_number) + ').name=ExpeditedShippingType&itemFilter(' + str(item_filter_number) + ').value=' + request.args.get('expeditedShipping')
		item_filter_number += 1

	if request.args.get('condition') is not None:
		condition_value_number = 0
		
		conditions_dict = {
			"New": "1000",
			"Used": "3000",
			"Very Good": "4000",
			"Good": "5000",
			"Acceptable": "6000"
		}

		ebay_api_url += '&itemFilter(' + str(item_filter_number) + ').name=Condition'
		conditions = request.args.get('condition').split(',')

		for condition in conditions:
			ebay_api_url += '&itemFilter(' + str(item_filter_number) + ').value(' + str(condition_value_number) + ')=' + conditions_dict[condition]
			condition_value_number += 1

	print ebay_api_url
	r = requests.get(ebay_api_url)

	return jsonify(r.text)
