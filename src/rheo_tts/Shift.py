#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import variables as var

#####
def show_tune():
	fig = ''
	tune_initialize()
	# make window
	shift_window = make_shift_window()
	# main loop
	while True:
		event, values = shift_window()
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		elif event == '-wlf-':
			if fig != '':
				plt.close()
			var.wlf_param['c1'] = float(values['-input_c1-'])
			var.wlf_param['c2'] = float(values['-input_c2-'])
			var.wlf_param['t0'] = float(values['-input_t0-'])
			fig = wlf_t0()
			shift_window['-param-'].update(var.shift_list)
		elif event == '-plot_ud-':
			if fig != '':
				plt.close()
			fig = plot_freq()	
		elif event == '-plot_at-':
			if fig != '':
				plt.close()
			fig = plot_at()	
		elif event == '-save_data-':
			save_data()
		elif event == '-tune-': 
			if values['-temp-'] != []:
				shift_window['-param-'].update(var.shift_list)
				if fig != '':
					plt.close()
				shift_window.hide()
				var.ref_temp = values['-temp-'][0]
				move_man()
				shift_window.un_hide()
				shift_window['-param-'].update(var.shift_list)
			else:
				sg.popup_error('Select proper Temperature !')
	plt.close('all')
	shift_window.close()
	return

def tune_initialize():
	var.extracteddata = var.yourdata_dic['extracteddata']
	var.temp_list = var.extracteddata['temp_list']
	var.shiftdata = var.yourdata_dic['shiftdata']
	var.shift_dic = var.shiftdata['shift_dic']
	var.shift_list = var.shiftdata['shift_list']
	var.modified_dic = var.shiftdata['modified_dic']
	if var.shift_dic == {} and var.shift_list == []:
		for temperature in var.temp_list:
			at = 1.0
			bt = 1.0
			shift_init = {'at': at, 'bt': bt}
			var.shift_dic[temperature] = shift_init
			var.shift_list.append([temperature, at, bt])
	return

def make_shift_window():
	# ウィンドウのレイアウト
	col_param = sg.Column([
							[sg.Text('C1', size = (8,1)), 
							sg.InputText(var.wlf_param["c1"], key = '-input_c1-', size = (5,1))], 
							[sg.Text('C2:', size = (8,1)), 
							sg.InputText(var.wlf_param["c2"], key = '-input_c2-', size = (5,1))],
							[sg.Text('T0 (°C):', size = (8,1)), 
							sg.InputText(var.wlf_param["t0"], key = '-input_t0-', size = (5,1))]
						])
	col_right = sg.Column([
				[sg.Text('Default parameter are C1 = 17.44 and C2 = 51.6.', size = (50,1))],
				[sg.Text('With this parameter set, T0 should be set as Tg in Celsius.', size = (50,1))],
				[sg.Button('Guess aT using Shown Parameters', 
		  					key = '-wlf-', 
							size=(30, 1))]
				])
	frame_wlf = sg.Frame('Initial Guess by WLF',
						[
							[col_param, col_right]
						]
						)
	frame_parameters = sg.Frame('Updated Parameters',
			     				[
									[sg.Table(
										var.shift_list, 
										headings=['Temperature (°C)', 'aT', 'bT'], 
										key='-param-', 
										def_col_width=20, 
										auto_size_columns=False, 
										vertical_scroll_only=True, 
										num_rows = len(var.shift_list), 
										justification='center')],
									[sg.Button('Plot Updated', 
										key = '-plot_ud-', 
										size=(21,1)),
									sg.Button('aT and bT vs. Temp.', 
										key = '-plot_at-', 
										size=(21,1)),
									sg.Button('Save Data', 
										key = '-save_data-', 
										size=(21,1))]
									]
								)
	col_select = [
					[
					sg.Text('Select Reference Temperature'),
					sg.Listbox(var.temp_list, key='-temp-', size=(8,3)),
					sg.Button('Tune Manually using Reference Temperature.',
	                            key='-tune-', 
				                size=(35,1))
					]
				]
	frame_mantune = sg.Frame('Manually Tune Parameters',
			  				[
							[sg.Column(col_select, justification='l')]
							]
							)
	
	shift_layout=[
				[frame_wlf],
				[frame_parameters],
				[frame_mantune],
				[sg.Button('Back to MAIN', key = '-exit-', size=(20,1))]
				]
	window = sg.Window('Tune the shift parameters', 
			                shift_layout, 
			                finalize=True)
	
	return window

def wlf_t0():
	tmp = []
	for temperature in var.temp_list:
		at = 10**(-1*var.wlf_param["c1"]*(temperature - var.wlf_param["t0"])/
	    							(var.wlf_param["c2"] + temperature - var.wlf_param["t0"]))
		var.shift_dic[temperature]['at'] = at
		tmp.append([temperature, f"{at:.2E}", var.shift_dic[temperature]['bt']])
		var.shift_list = tmp
	fig = plot_freq()
	return fig

def plot_freq():
	fig, ax = plt.subplots()
	for temperature in var.temp_list:
		at = var.shift_dic[temperature]['at']
		mfreq = [freq*at for freq in var.extracteddata['extracted_dic'][temperature]['Ang. Freq.']]
		ax.plot(mfreq, var.extracteddata['extracted_dic'][temperature]['Tan_d'], 
	            label='T='+str(temperature))
	ax.set_xlabel('Freq.')
	ax.set_ylabel(r'Tan $\delta$')
	ax.set_title(f'Guess for all Temperature for T0={var.wlf_param["t0"]:}')
	ax.semilogx(base=10)
	ax.semilogy(base=10)
	ax.legend(borderaxespad=0, ncol=2)
	plt.show(block=False)
	return fig

def plot_at():
	fig, ax = plt.subplots()
	at_list = [var.shift_dic[temp]['at'] for temp in var.temp_list]
	bt_list = [var.shift_dic[temp]['bt'] for temp in var.temp_list]
	ax.plot(var.temp_list, at_list, label=r'a$_{T}$')
	ax.plot(var.temp_list, bt_list, label=r'b$_{T}$')
	ax.set_xlabel('Temperature')
	ax.set_ylabel(r'a$_{T}$')
	ax.set_title(f'aT for T0={var.wlf_param["t0"]:}')
	ax.semilogy(base=10)
	ax.legend(borderaxespad=0, ncol=2)
	plt.show(block=False)
	return fig

def save_data():
	with open(var.fileroot + '_shift_param.dat', 'w') as f:
		f.write(f"# Temp.\taT\tbT\n\n\n")
		for temperature in var.temp_list:
			f.write(f"{temperature:.1f}\t{var.shift_dic[temperature]['at']:.2e}\t{var.shift_dic[temperature]['bt']:.2f}\n")

	with open(var.fileroot + '_modified.dat', 'w') as f:
		for temperature in var.temp_list:
			at = var.shift_dic[temperature]['at']
			bt = var.shift_dic[temperature]['bt']
			mfreq = [freq*at for freq in var.extracteddata['extracted_dic'][temperature]['Ang. Freq.']]
			storage = [bt*data for data in var.extracteddata['extracted_dic'][temperature]['Str. Mod.']]
			loss = [bt*data for data in var.extracteddata['extracted_dic'][temperature]['Loss Mod.']]
			tand = var.extracteddata['extracted_dic'][temperature]['Tan_d']
			f.write(f"# Temperature = {temperature:.1f}\n# Mod.Freq.\tG'\tG''\ttan d\n\n\n")
			for i in range(len(var.extracteddata['extracted_dic'][temperature]['Ang. Freq.'])):
				f.write(f"{mfreq[i]:.2e}\t{storage[i]:.2e}\t{loss[i]:.2e}\t{tand[i]:.2e}\n")
			f.write("\n")

	var.shiftdata = var.yourdata_dic['shiftdata']
	var.shiftdata['shift_dic'] = var.shift_dic
	var.shiftdata['shift_list'] = var.shift_list
	var.shiftdata['modified_dic'] = var.modified_dic

	return











# tune manually
def move_man():
	fig = ''
	mod_param()
	lower_temp = [x for x in var.temp_list if x < var.ref_temp]
	upper_temp = [x for x in var.temp_list if x > var.ref_temp]
	target_row = var.temp_list.index(var.ref_temp)

	frame_reftemp = sg.Frame('Modified Parameters',
							[
								[sg.Table(
								var.shift_list, 
								headings=['Temperature (°C)', 'aT', 'bT'], 
								key='-param-', 
								def_col_width=18, 
								auto_size_columns=False, 
								vertical_scroll_only=True, 
								row_colors = [(target_row, 'red', 'white')],
								num_rows = len(var.shift_list), 
								justification='center'
								)],
							]	
			  				)
	col_upper = sg.Column([
					# [sg.Text('Upper')],
					[sg.Listbox(upper_temp, key='-temp_u-', size=(6,3)), 
      				sg.Button('Move Upper Data', key='-upper-', size=(15,1))]
				], justification='c', vertical_alignment='c')
	col_lower = sg.Column([
					# [sg.Text('Lower')],
      				[sg.Listbox(lower_temp, key='-temp_l-', size=(6,3)),
					sg.Button('Move Lower Data', key='-lower-', size=(15,1))]
				], justification='c', vertical_alignment='c')
	col_reference = sg.Column([
						[sg.Text('Ref. Temp.', size=(8,1))],
		                [sg.Text(f'  {var.ref_temp:.1f}°C',
									relief=sg.RELIEF_RAISED, 
									border_width=2, 
									size=(8,1))]
					], justification='c', vertical_alignment='c')
	frame_target = sg.Frame('Target Temperature',
								[
									[col_upper, col_reference, col_lower]
								]
							)
	frame_move_at = sg.Frame('Tune aT manually !!',
			     			[
							[sg.Text('Previous aT:', size=(8,1)),
							sg.Text('', key='-p_at-', size=(8,1)),
							sg.Text('Modified aT:', size=(8,1)),
							sg.InputText('', key='-mod_at-', size=(8,1))
							],
							[sg.Text("Fine", size=(5,1)),
							sg.Slider(range=(-1.,1.),
								default_value = 0.0,
								resolution=0.01,
								orientation='h',
								disable_number_display=True,
								size=(50, None),
								enable_events=True,
								key='-slidera1-')],
							[sg.Text("Rough", size=(5,1)),
							sg.Slider(range=(-50.,50.),
								default_value =0.,
								resolution=1.,
								orientation='h',
								disable_number_display=True,
								size=(50, None),
								enable_events=True,
								key='-slidera2-')],
							[sg.Button('Move aT', key='-move_at-', size=(20,1)),
							sg.Button('Set aT', key='-set_at-', size=(20,1))
							]
							]
							)
	frame_move_bt = sg.Frame('Tune bT manually !!',
			     			[
							[sg.Text('Previous bT:', size=(8,1)),
							sg.Text(1.0, key='-p_bt-', size=(8,1)),
							sg.Text('Modified bT:', size=(8,1)),
							sg.InputText('', key='-mod_bt-', size=(8,1))],
							[sg.Text("Fine", size=(5,1)),
							sg.Slider(range=(-0.1,0.1),
								default_value = 0.0,
								resolution=0.001,
								orientation='h',
								disable_number_display=True,
								size=(50, None),
								enable_events=True,
								key='-sliderb1-')],
							[sg.Text("Rough", size=(5,1)),
							sg.Slider(range=(-1.,1.),
								default_value = 0.0,
								resolution=0.01,
								orientation='h',
								disable_number_display=True,
								size=(50, None),
								enable_events=True,
								key='-sliderb2-')],
							[sg.Button('Move bT', key='-move_bt-', size=(20,1)),
							sg.Button('Set bT', key='-set_bt-', size=(20,1))
							]
							]
							)
	move_layout=[
				[frame_reftemp],
				[frame_target],
				[frame_move_at],
				[frame_move_bt],
				[sg.Button('Back to Prev. Window', key = '-exit-', size=(20,1))]
				]
	move_window = sg.Window('Tune the shift parameters', move_layout, finalize=True)

	while True:
		event, values = move_window()
		if event in [sg.WIN_CLOSED, '-exit-']:
			break
		elif event == '-upper-' and values['-temp_u-'] !=[]:
			if fig != '':
				plt.close()
			target = values['-temp_u-'][0]
			at = var.shift_dic[target]['at']
			bt = var.shift_dic[target]['bt']
			move_window['-p_at-'].Update(f"{at:.2e}")
			move_window['-p_bt-'].Update(f"{bt:.2f}")
			move_window['-mod_at-'].Update(f"{at:.2e}")
			move_window['-mod_bt-'].Update(f"{bt:.2f}")
			fig = plot_mod_at(target, at)
		elif event == '-lower-' and values['-temp_l-'] !=[]:
			if fig != '':
				plt.close()
			target = values['-temp_l-'][0]
			at = var.shift_dic[target]['at']
			bt = var.shift_dic[target]['bt']
			move_window['-p_at-'].Update(f"{at:.2e}")
			move_window['-p_bt-'].Update(f"{bt:.2f}")
			move_window['-mod_at-'].Update(f"{at:.2e}")
			move_window['-mod_bt-'].Update(f"{bt:.2f}")
			fig = plot_mod_at(target, at)
		elif event == "-slidera1-" or event == "-slidera2-":
			amp = 10**(float(values['-slidera1-'])+float(values['-slidera2-']))
			move_window['-mod_at-'].Update(f"{amp*float(var.shift_dic[target]['at']):.2e}")
		elif event == "-move_at-":
			if fig != '':
				plt.close()
			mod_at = float(values['-mod_at-'])
			fig = plot_mod_at(target, mod_at)
		elif event == '-set_at-':
			move_window['-slidera1-'].Update(0.)
			move_window['-slidera2-'].Update(0.)
			move_window['-p_at-'].Update(f"{float(values['-mod_at-']):.2e}")
			move_window['-param-'].Update()
			var.shift_dic[target]['at'] = float(values['-mod_at-'])
			var.shift_list = [[temp, f"{float(var.shift_dic[temp]['at']):.2E}", 
		      								float(var.shift_dic[temp]['bt'])] 
		    					for temp in var.temp_list]
			move_window['-param-'].Update(var.shift_list,
				 					row_colors = [(target_row, 'red', 'white')])
		elif event == "-sliderb1-" or event == "-sliderb2-":
			amp = 10**(float(values['-sliderb1-'])+float(values['-sliderb2-']))
			move_window['-mod_bt-'].Update(f"{amp*float(var.shift_dic[target]['bt']):.2e}")
		elif event == "-move_bt-":
			if fig != '':
				plt.close()
			mod_bt = float(values['-mod_bt-'])
			fig = plot_mod_bt(target, mod_bt)
		elif event == '-set_bt-':
			move_window['-sliderb1-'].Update(0.)
			move_window['-sliderb2-'].Update(0.)
			move_window['-p_bt-'].Update(float(values['-mod_bt-']))
			var.shift_dic[target]['bt'] = float(values['-mod_bt-'])
			var.shift_list = [[temp, f"{float(var.shift_dic[temp]['at']):.2E}", 
		      								float(var.shift_dic[temp]['bt'])] 
		    					for temp in var.temp_list]
			move_window['-param-'].Update(var.shift_list,
				 							row_colors = [(target_row, 'red', 'white')])
	move_window.close()
	return

def mod_param():
	at_ref = var.shift_dic[var.ref_temp]["at"]
	bt_ref = var.shift_dic[var.ref_temp]["bt"]
	mod_shift_dic = {temp:{'at': var.shift_dic[temp]["at"]/at_ref, 
			            'bt': var.shift_dic[temp]["bt"]/bt_ref} for temp in var.shift_dic.keys()}
	var.shift_dic.update(mod_shift_dic)
	var.shift_list = [[temp, f'{var.shift_dic[temp]["at"]:.2e}', 
		                var.shift_dic[temp]["bt"]] for temp in var.shift_dic.keys()]
	return 

def plot_mod_at(target, mod_at):
	if target > var.ref_temp:
		target_range = [x for x in var.temp_list if x <= target and x >= var.ref_temp]
	elif target < var.ref_temp:
		target_range = [x for x in var.temp_list if x >= target and x <= var.ref_temp]
	fig, ax = plt.subplots()
	for temperature in target_range:
		if temperature == target:
			at = mod_at
		else:
			at = float(var.shift_dic[temperature]['at']) 
		mfreq = [freq*at for freq in var.extracteddata['extracted_dic'][temperature]['Ang. Freq.']]
		if temperature == var.ref_temp:
			ax.plot(mfreq, var.extracteddata['extracted_dic'][temperature]['Tan_d'], 
	        label='Tr='+str(temperature), lw=3, color='red', ls=':')
		else:
			ax.plot(mfreq, var.extracteddata['extracted_dic'][temperature]['Tan_d'], 
	        label='T='+str(temperature))
	ax.set_xlabel('Freq.')
	ax.set_ylabel(r'Tan $\delta$')
	ax.set_title(f'Modified based on Tr={var.ref_temp:}')
	ax.semilogx(base=10)
	ax.semilogy(base=10)
	ax.legend(borderaxespad=0, ncol=2)
	plt.show(block=False)
	return fig

def plot_mod_bt(target, mod_bt):
	if target > var.ref_temp:
		target_range = [x for x in var.temp_list if x <= target and x >= var.ref_temp]
	elif target < var.ref_temp:
		target_range = [x for x in var.temp_list if x >= target and x <= var.ref_temp]
	fig, ax = plt.subplots()
	for temperature in target_range:
		at = float(var.shift_dic[temperature]['at']) 
		if temperature == target:
			bt = mod_bt
		else:
			bt = float(var.shift_dic[temperature]['bt']) 
		mfreq = [freq*at for freq in var.extracteddata['extracted_dic'][temperature]['Ang. Freq.']]
		storage = [bt*data for data in var.extracteddata['extracted_dic'][temperature]['Str. Mod.']]
		loss = [bt*data for data in var.extracteddata['extracted_dic'][temperature]['Loss Mod.']]
		if temperature == var.ref_temp:
			ax.plot(mfreq, storage, label='G\':'+str(temperature), lw=3, color='red', ls=':')
			ax.plot(mfreq, loss, label='G":'+str(temperature), lw=3, color='red', ls=':')
		else:
			ax.plot(mfreq, storage, label='G\':'+str(temperature))
			ax.plot(mfreq, loss, label='G":'+str(temperature))
	ax.set_xlabel('Freq.')
	ax.set_ylabel('G\', G"')
	ax.set_title(f'Modified based on Tr={var.ref_temp:}')
	ax.semilogx(base=10)
	ax.semilogy(base=10)
	ax.legend(borderaxespad=0, ncol=2)
	plt.show(block=False)
	return fig


