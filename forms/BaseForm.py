

class BaseForm:

	def __init__(self, btn_submit_text=None, has_cancel_btn=False, btn_cancel_text=None\
				, btn_cancel_url=None, action='', method='post'):
		self.btn_submit_text = btn_submit_text
		self.has_cancel_btn = has_cancel_btn
		self.btn_cancel_text = btn_cancel_text
		self.btn_cancel_url = btn_cancel_url
		self.action = action
		self.method = method

		self.field_map = {
			'string':'_input_text',
			'file':'_input_file',
			'text':'_input_textarea',
			'password':'_input_password',
		}

		for f in self.fields:
			setattr(self, f['name'], f)

	def _label(self, name):
		name = name.title()
		return '<label class="control-label" for="input%s">%s</label>' % (name, name)


	def _input_hidden(self, name, placeholder=None, class_name=None, value=None):	
		if value:	
			name = name.lower()
			_input = '<input type="hidden" id="input%s" name="%s" ' % (name, name)
			if class_name: _input += ' class="%s"' % class_name
			if value: _input += ' value="%s"' % value
			_input += ' />'

		else:
			_input = ''

		return _input


	def _input_text(self, name, placeholder=None, class_name=None, value=None):		
		name = name.lower()
		_input = '<input type="text" id="input%s" name="%s" ' % (name, name)
		if placeholder: _input += ' placeholder="%s"' % placeholder
		if class_name: _input += ' class="%s"' % class_name
		if value: _input += ' value="%s"' % value
		_input += ' />'

		return _input


	def _input_file(self, name, placeholder=None, class_name=None, value=None):		
		name = name.lower()
		_input = '<input type="file" id="input%s" name="%s" ' % (name, name)
		if class_name: _input += ' class="%s"' % class_name
		if value: _input += ' value="%s"' % value
		_input += ' />'

		return _input


	def _input_textarea(self, name, placeholder=None, class_name=None, value=None):		
		name = name.lower()
		_input = '<textarea id="input%s" name="%s" ' % (name, name)
		if class_name: _input += ' class="%s"' % class_name
		_input += '>'
		if value: _input += value
		_input += '</textarea>'

		return _input


	def _input_password(self, name, placeholder=None, class_name=None, value=None):		
		_input = '<input type="password" id="input%s" name="%s" ' % (name, name)
		if placeholder: _input += ' placeholder="%s"' % placeholder
		if class_name: _input += ' class="%s"' % class_name
		if value: _input += ' value="%s"' % value
		_input += ' />'

		return _input

	def _input_cancel(self):
		return '<a href="%s" class="btn">%s</a>' % (self.btn_cancel_url, self.btn_cancel_text)

	def _input_submit(self):
		return '<input type="submit" class="btn" value="%s" />' % (self.btn_submit_text)

	def _wrap_field(self, field):
		return '<div class="controls">%s</div>' % field

	def _wrap_row(self, row, class_name=''):
		return '<div class="control-group %s">%s</div>' % (class_name, row)

	def _wrap_form(self, form, multipart=False):
		_multipart = ' enctype="multipart/form-data" ' if multipart else ''

		return '<form class="form-horizontal" %s action="%s" method="%s">%s</form>' % (_multipart
																					,self.action\
																					,self.method\
																					,form)

	def get_html(self):
		is_multipart = False
		form = ''
		for f in self.fields:
			if f.get('type')=='file':
				is_multipart = True

			if f.get('type')=='hidden':
				if f.get('value'):
					form += self._input_hidden(name=f.get('name'), value=f['value'])
			else:
				label = self._label(f.get('label') or f.get('name'))
				field = eval('self.'+ self.field_map[f.get('type')])(name=f['name']\
																	, placeholder=f.get('placeholder')\
																	, class_name=f.get('class_name')\
																	, value=f.get('value'))
				field = self._wrap_field(field)
				row = self._wrap_row(label + field)

				form += row

		submitrow = self._input_submit()
		if self.has_cancel_btn: submitrow += self._input_cancel()
		submitrow = self._wrap_field(submitrow)
		submitrow = self._wrap_row(submitrow, class_name=' submitrow')
		form += submitrow

		form = self._wrap_form(form, multipart=is_multipart)

		return form



