product_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
		for seo_url in convert['seo']:
			leurlrewrite = {
				'link_rewrite': seo_url['request_path'],
				'id_desc': product_id,
				'type': 'product',
				'lang_code': self._notice['target']['language_default']
			}
			seourl_query = self.create_insert_query_connector("lecm_rewrite", leurlrewrite)
			
			response = self.import_data_connector(seourl_query,"link_301",convert['id'])
