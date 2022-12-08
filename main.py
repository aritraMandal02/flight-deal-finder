from data_manager import Manager


manager = Manager()
manager.start()

# sheet = Sheety(sheet_name='prices', url=sheety_url, token=TOKEN)
# data = sheet.sheet_data
# print(data)
# city_names = sheet.get_column(col_name='city')
# flight_search = FlightSearch()
# print(flight_search.get_city_codes())
# city_codes = flight_search.get_city_codes()
# print(city_codes)
# print(city_codes)

# sheet.edit_row(args)
# print(sheet.edit_row(row_id=2, row_params=dict(city='Paris', iataCode='', lowestPrice=50)))
# sheet.get_sheet(args)
# sheet.delete_row(2)
# sheet.edit_value(arg)
# sheet.edit_column(args)
# print(sheet.get_row(row_index=4))
# sheet.edit_column(col_name='iataCode', values=city_codes)
# print(sheet.edit_value(row_id=6, col_name='lowestPrice', value=95))
