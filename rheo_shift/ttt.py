datalabel_dic = {
            'Temp.':'温度', 
            'Ang. Freq.':'角周波数', 
            'Str. Mod.':'貯蔵弾性率', 
            'Loss. Mod.':'損失弾性率', 
            'Tan_d':'損失正接',
            }
for t in data_dic.items():
    print(t[1], t[0])


if set(data_dic.values()).issubset(set(line)) :