binaryfile = ''

originaldata = {
				'filename': '',
                'sheetname': '',
                'originaldata_list': [],
                'comment': 'You can erase and input multi lines Comment here!\nYou can hit return key for new line'
				}
extracteddata = {
				'temp_list': [],
                'extracted_h_dic': {},
				'extracted_dic': {}
				}
parameters = {
				'shift_dic': {},
                'shift_list': []
				}

yourdata_dic = {
				'originaldata': originaldata, 
				'extracteddata': extracteddata,
				'parameters': parameters
				}

datalabel_dic = {
			'Temp.':'温度', 
			'Ang. Freq.':'角周波数', 
			'Str. Mod.':'貯蔵弾性率', 
			'Loss Mod.':'損失弾性率', 
			'Tan_d':'損失正接'
			}
skip = 1

temp_list = []

shift_dic= {}
param_list = []
wlf_param = {
			'c1': 17.44,
			'c2': 51.60,
			't0': 0.0,
			}
bt = 1.0
ref_temp = 0.