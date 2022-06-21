order_id = self.get_map_field_by_src(self.TYPE_ORDER, convert['id'], convert['code'])
		if order_id:
			self.delete_target_order(order_id)
			self.select_raw("DELETE FROM migration_map WHERE type = 'order' AND id_src = "+to_str(convert['id']))
