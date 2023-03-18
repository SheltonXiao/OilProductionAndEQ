# -*- coding:utf-8 -*-
'''
@File    :   featureGenerator.py
@Time    :   2023/03/14 14:08:40
@Author  :   SheltonXiao
@Version :   1.0
@Contact :   pi620903@163.com
@Desc    :   None
@License :

    (c) Copyright 2022 SheltonXiao

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or(at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY;without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
    GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with this program.If not, see < https: //www.gnu.org/licenses/>.
'''

# here put the import lib
import os
import numpy as np
import pandas as pd
from tqdm import trange
from IPython.display import clear_output
import matplotlib.pyplot as plt
import datetime

TS_COL = ['Water or Steam Injected (bbl)',
            'Gas or Air Injected (Mcf)',
            'Oil Produced (bbl)',
            'Water Produced (bbl)',
            'Gas Produced (Mcf)',
            'Last_Water or Steam Injected (bbl)',
            'Last_Gas or Air Injected (Mcf)',
            'Last_Oil Produced (bbl)',
            'Last_Water Produced (bbl)',
            'Last_Gas Produced (Mcf)',
            'Total_Water or Steam Injected (bbl)',
            'Total_Gas or Air Injected (Mcf)',
            'Total_Oil Produced (bbl)',
            'Total_Water Produced (bbl)',
            'Total_Gas Produced (Mcf)']

EQ_COL = ['ET',
            'GT',
            'MAG',
            'M',
            'LAT',
            'LON',
            'DEPTH',
            'Q',
            'EVID',
            'NPH',
            'NGRM','BUFF_DIST','Time',]


def EQdataLoader(filename = "eq_1977h_linear1.xls"):
    # raw earthquake for timestamp
    eq_data = pd.read_csv(os.path.join(r"data/processed","earthquake.csv"),parse_dates=["Time"])
    eq_data.index = eq_data["EVID"]

    eqbelong = pd.read_excel(os.path.join(r"data/processed",filename),parse_dates=["Time_"])
    eqbelong,eq_slice,oil = bufferDataModifier(eq_data,eqbelong)
    EVID_dict = EVIDwithOFGenerator(eqbelong)

    dist1 = pd.read_csv(os.path.join(r"data/processed","eqdata_distance.csv"),parse_dates=True)
    dist2 = pd.read_csv(os.path.join(r"data/processed","eqdata_distance_p.csv"),parse_dates=True)
    dist2["NEAR_FID"] = dist2["NEAR_FID"]+1
    dist1.index = dist1["EVID"]
    dist2.index = dist2["EVID"]

    eq_data2 = pd.read_csv(os.path.join(r"data/processed","eqdata.csv"),parse_dates=["Time"])
    eq_data2.index = eq_data2["EVID"]
    eq_sub = None#pd.read_csv(os.path.join(r"data/processed","eqdata_withbuffer.csv"),parse_dates=True)
    eq_neg = EQoutsideBufferDataModifier(eq_data,eq_data2,eqbelong,eq_sub,oil,dist1,dist2)
    

    return eq_slice,eq_neg,oil,EVID_dict

def OFdataLoader():
    of_info = pd.read_csv(os.path.join(r"data\forfeature","oil_info.csv"),parse_dates=True)
    OFID = np.unique(of_info["OID_"])
    ts = dict()
    ts_past = dict()
    ts_cum = dict()
    for eachid in OFID:
        ts[eachid] = pd.read_csv(os.path.join(r"data\forfeature\wellts",f"{eachid}.csv"),parse_dates=True,index_col=0).fillna(0)
        ts_past[eachid] = ts[eachid].shift(1).fillna(0)
        ts_cum[eachid] = ts[eachid].cumsum()
    return ts,ts_past,ts_cum

def bufferDataModifier(eq_data,eqbelong):
    col = ['ET', 'GT', 'MAG', 'M', 'LAT', 'LON', 'DEPTH', 'Q',
       'EVID', 'NPH', 'NGRM', 'Time_', 'Year_','OID_', 'BUFF_DIST', 
       ]
    eqbelong = eqbelong[col]
    eqbelong.rename(columns={"Year_":"Year",#"Time_":"Time"
                            },inplace = True)
    ind = eqbelong['EVID']
    eqbelong['Time'] = eq_data.loc[ind]["Time"].values

    eq_slice = eqbelong.copy()
    oil = eqbelong.drop_duplicates(subset=['OID_'], keep='first')
    oil.index = oil["OID_"]
    oil = oil[["BUFF_DIST"]]
    eq_slice = eq_slice.sort_values('BUFF_DIST', 
                                    ascending=True).drop_duplicates(subset=['EVID'], keep='first')
    eq_slice["Month"] = [each.month for each in eq_slice["Time"]]
    eq_slice["Month"] = eq_slice["Month"].ffill().astype(np.int64)
    eq_slice["TimeMonth"] = [datetime.datetime(eq_slice.loc[each,"Year"], 
                            eq_slice.loc[each,"Month"], 1) for each in eq_slice.index]
    eq_slice.index = eq_slice["EVID"]
    return eqbelong,eq_slice,oil

def EVIDwithOFGenerator(eqbelong):
    OID = np.unique(eqbelong["OID_"])
    EVID_dict = {}
    g = eqbelong.groupby(by=["EVID"]).groups
    for each in g.keys():
        EVID_dict[each] = eqbelong.loc[g[each]]["OID_"].values.tolist()
    return EVID_dict

def EQoutsideBufferDataModifier(eq_data,eq_data2,eqbelong,eq_sub,oil,dist1,dist2):
    ind = eqbelong['EVID']
    ind2 = eq_data2[eq_data2["Year"]>=1977].index.tolist()
    ind20 = eq_data2[eq_data2["Year"]>=2018].index.tolist()
    ind3 = list(set(ind2)-set(ind)-set(ind20))
    #ind4 = eq_sub["EVID"]
    #ind5 = list(set(ind3)-set(ind4))
    outsideLA = eq_data.loc[list(set(eq_data.index.tolist())-set(eq_data2.index.tolist()))]
    outsideLA = outsideLA[(outsideLA["LON"]>=-118.955)&(outsideLA["LON"]<=-117.648)]
    outsideLA = outsideLA[(outsideLA["LAT"]>=32.802)&(outsideLA["LAT"]<=34.289)]
    outsideLA = outsideLA.loc[list(set(outsideLA.index.tolist())-set(ind))].copy().dropna()

    eq_neg = eq_data2.loc[ind3].copy().dropna()
    eq_neg = pd.concat([eq_neg,outsideLA],axis=0)
    eq_neg["BUFF_DIST"]=999999

    eq_neg["OID"] = dist2["NEAR_FID"]
    eq_neg["polygon_D"] = dist2['NEAR_DIST']

    # consider the oil with data
    blis = [each in oil.index.tolist() for each in eq_neg["OID"]]
    eq_neg2 = eq_neg[blis]
    eq_neg2["BUFF"] = eq_neg2["OID"].apply(lambda x:oil.loc[int(x),"BUFF_DIST"])
    eq_neg2["Month"] = [each.month for each in eq_neg2["Time"]]
    eq_neg2["Month"] = eq_neg2["Month"].ffill().astype(np.int64)
    eq_neg2["TimeMonth"] = [datetime.datetime(eq_neg2.loc[each,"Year"], eq_neg2.loc[each,"Month"], 1) for each in eq_neg2.index]
    return eq_neg2

# TS data dict
def TSdataModifierMulti(evid,ts,ts_past,ts_cum,EVID_dict,eq_slice):
    t = eq_slice.loc[evid,"TimeMonth"]
    for each in EVID_dict[evid]:
        try:
            tnow_sli = tnow_sli + ts[each].loc[t]
            tpast_sli = tpast_sli + ts_past[each].loc[t]
            tcum_sli = tcum_sli + ts_cum[each].loc[t]
        except:
            tnow_sli = ts[each].loc[t]
            tpast_sli = ts_past[each].loc[t]
            tcum_sli = ts_cum[each].loc[t]
    tpast_sli.index = ["Last_"+each for each in tpast_sli.index.to_list()]
    tcum_sli.index = ["Total_"+each for each in tcum_sli.index.to_list()]
    tnow_sli = pd.concat([tnow_sli,tpast_sli])
    tnow_sli = pd.concat([tnow_sli,tcum_sli])
    return tnow_sli

def TSdataModifierSingle(evid,ts,ts_past,ts_cum,EVID_dict,eq_neg):
    t = eq_neg.loc[evid,"TimeMonth"]
    each = eq_neg.loc[evid,"OID"]
    
    tnow_sli = ts[each].loc[t]
    tpast_sli = ts_past[each].loc[t]
    tcum_sli = ts_cum[each].loc[t]
    
    tpast_sli.index = ["Last_"+each for each in tpast_sli.index.to_list()]
    tcum_sli.index = ["Total_"+each for each in tcum_sli.index.to_list()]
    tnow_sli = pd.concat([tnow_sli,tpast_sli])
    tnow_sli = pd.concat([tnow_sli,tcum_sli])
    return tnow_sli

def TSdataModifier(evid,ts,ts_past,ts_cum,EVID_dict,eq_slice,label=True):
    if label:
        return TSdataModifierMulti(evid,ts,ts_past,ts_cum,EVID_dict,eq_slice)
    else:
        return TSdataModifierSingle(evid,ts,ts_past,ts_cum,EVID_dict,eq_slice)

# feature generation
def TSfeatureGeneratorPos(eq_slice,ts,ts_past,ts_cum,EVID_dict,label):
    new = dict()
    for each in EVID_dict.keys():
        try:
            new[each] = TSdataModifier(each,ts,ts_past,ts_cum,EVID_dict,eq_slice,label)
        except:
            #print(each)
            pass
    ts_eq = pd.DataFrame(new).T
    return ts_eq

def TSfeatureGeneratorNeg(eq_slice,ts,ts_past,ts_cum,EVID_dict,label):
    new = dict()
    for each in eq_slice.index:
        try:
            new[each] = TSdataModifier(each,ts,ts_past,ts_cum,EVID_dict,eq_slice,label)
        except:
            #print(each)
            pass
    ts_eq = pd.DataFrame(new).T
    for each in ts_eq.columns:
        ts_eq[each] = ts_eq[each]*(eq_slice["BUFF"]/eq_slice["polygon_D"])
    return ts_eq

def TSfeatureGenerator(eq_slice,ts,ts_past,ts_cum,EVID_dict,label = True):
    if label:
        return TSfeatureGeneratorPos(eq_slice,ts,ts_past,ts_cum,EVID_dict,label)
    else:
        return TSfeatureGeneratorNeg(eq_slice,ts,ts_past,ts_cum,EVID_dict,label)


def featureGenerator(eq_slice,ts,ts_past,ts_cum,EVID_dict,label = True):
    ts_eq = TSfeatureGenerator(eq_slice,ts,ts_past,ts_cum,EVID_dict,label)
    if label:
        eq_record = pd.concat([eq_slice[EQ_COL],ts_eq],axis = 1).dropna(how = "any",axis = 0)
    else:
        eq_record  = pd.concat([eq_slice[EQ_COL],ts_eq],axis = 1).fillna(0)
    eq_record["Label"] = int(label)
    return eq_record

if __name__ == '__main__':
    eq_slice,eq_neg,oil,EVID_dict = EQdataLoader(filename = "tables_0317_BUFFER_EQ\step3_0317_eq.xls")
    ts,ts_past,ts_cum = OFdataLoader()

    eq_positive = featureGenerator(eq_slice,ts,ts_past,ts_cum,EVID_dict,label = True)
    #eq_positive.to_csv(os.path.join(r"data/final","eq_pos_test.csv"))
    eq_negative = featureGenerator(eq_neg,ts,ts_past,ts_cum,EVID_dict,label = False)
    #eq_negative.to_csv(os.path.join(r"data/final","eq_neg_test.csv"))
    eq_dataset = pd.concat([eq_positive,eq_negative],axis=0)
    eq_dataset.to_csv(os.path.join(r"data/final","eq_step3.csv"))

    print("The size of positive set is %d"%(len(eq_positive)))
    print("The size of negative set is %d"%(len(eq_negative)))