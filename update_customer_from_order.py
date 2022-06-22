order_id = self.get_map_field_by_src(self.TYPE_ORDER, convert['id'], convert['code'])
		########### update customer theo order
		id_group = 1
		gender = 0
		customer=convert["customer"]
		customer_address=convert["customer_address"]
		# neu customer khong co email thi return true 
		if not customer['email'] and not customer_address['email']:
			return True
		# goi xem email cua customer da ton tai hay chua
		select = self.create_select_query_connector('customer', {'email': customer['email']})
		customer_data = self.select_data_connector(select)
		self.log(customer_data,'customer_data')
		#neu email chua ton tai thi tao mot customer moi roi insert len
		if not customer_data['data']:
			customer_data = {
				'id_default_group': id_group,
				'id_gender': gender,
				'id_lang': self._notice['target']['language_default'],
				'firstname': customer['first_name'] if customer['first_name'] else '',
				'lastname': customer['last_name'] if customer['last_name'] else '',
				'company':customer_address["company"] if customer_address['company'] else '', 
				'email': customer['email'] if customer['email'] else customer_address['email'],
				'passwd': '',
				'last_passwd_gen': get_current_time(),
				'birthday': None,
				'newsletter': 0,
				'date_add': get_current_time(),
				'date_upd': get_current_time(),
				'active': 1 ,}
			id_customer = self.import_data_connector(self.create_insert_query_connector('customer', customer_data), 'import_customer',convert['id'])
			# sau khi insert len target thi insert vao map
			if id_customer:
				self.insert_map(self.TYPE_CUSTOMER, None, id_customer, customer['email'])
				id_address = self.get_map_field_by_src(self.TYPE_ADDRESS, to_int(customer_address['id']), customer_address['code'])
				if not id_address:
					self.insert_address(id_customer,customer_address)
			else:
				return response_error(self.warning_import_entity(self.TYPE_CUSTOMER, convert['id'], convert['code']))
		# neu email da ton tai thi lay ra id_customer
		else:
			id_customer = customer_data['data'][0]['id_customer']
		# dung id_customer de map voi oder
		response = self.import_data_connector(self.create_update_query_connector('orders', {"id_customer":id_customer},{"id_order":order_id}), 'update_link_customer', convert['id'])
		response = self.import_data_connector(self.create_update_query_connector('customer_thread', {"id_customer":id_customer},{"id_order":order_id}), 'update_customer_thread', convert['id'])
