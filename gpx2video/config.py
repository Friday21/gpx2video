#!/usr/bin/env python
# -*- coding: utf-8 -*-


map_path = '/Users/friday/娱乐/google_map/杭州10-18'
level_list = [10, 11, 12, 13, 14, 15, 16, 17, 18]

indexes = {
    "10": {
        "row": 3,
        "col": 4,
        "left_top_latitude": 30.751277776257812,
        "left_top_longitude": 118.125,
        "right_down_latitude": 28.927205456293777,
        "right_down_longitude": 120.9375,
        "row_step": 0.6080241066546783,
        "col_step": 0.703125,
        "start_row_num": 211,
        "start_col_num": 425,
        "end_row_num": 213,
        "end_col_num": 428
    },
    "11": {
        "row": 6,
        "col": 8,
        "left_top_latitude": 30.751277776257812,
        "left_top_longitude": 118.125,
        "right_down_latitude": 28.924412480981513,
        "right_down_longitude": 120.9375,
        "row_step": 0.3044775492127165,
        "col_step": 0.3515625,
        "start_row_num": 421,
        "start_col_num": 849,
        "end_row_num": 426,
        "end_col_num": 856
    },
    "12": {
        "row": 10,
        "col": 14,
        "left_top_latitude": 30.600093873550065,
        "left_top_longitude": 118.30078125,
        "right_down_latitude": 29.076534047599136,
        "right_down_longitude": 120.76171875,
        "row_step": 0.15235598259509292,
        "col_step": 0.17578125,
        "start_row_num": 842,
        "start_col_num": 1698,
        "end_row_num": 851,
        "end_col_num": 1711
    },
    "13": {
        "row": 19,
        "col": 28,
        "left_top_latitude": 30.600093873550065,
        "left_top_longitude": 118.30078125,
        "right_down_latitude": 29.152712038896684,
        "right_down_longitude": 120.76171875,
        "row_step": 0.07617799129754646,
        "col_step": 0.087890625,
        "start_row_num": 1683,
        "start_col_num": 3395,
        "end_row_num": 1701,
        "end_col_num": 3422
    },
    "14": {
        "row": 38,
        "col": 55,
        "left_top_latitude": 30.600093873550065,
        "left_top_longitude": 118.30078125,
        "right_down_latitude": 29.15243658793632,
        "right_down_longitude": 120.7177734375,
        "row_step": 0.038096244358256384,
        "col_step": 0.0439453125,
        "start_row_num": 3365,
        "start_col_num": 6789,
        "end_row_num": 3402,
        "end_col_num": 6789
    },
    "15": {
        "row": 74,
        "col": 109,
        "left_top_latitude": 30.581179257386978,
        "left_top_longitude": 118.32275390625,
        "right_down_latitude": 29.171482881265916,
        "right_down_longitude": 120.7177734375,
        "row_step": 0.019049951028662998,
        "col_step": 0.02197265625,
        "start_row_num": 6730,
        "start_col_num": 13578,
        "end_row_num": 6803,
        "end_col_num": 13686
    },
    "16": {
        "row": 146,
        "col": 217,
        "left_top_latitude": 30.57172056519988,
        "left_top_longitude": 118.333740234375,
        "right_down_latitude": 29.181007399653854,
        "right_down_longitude": 120.7177734375,
        "row_step": 0.009525432640726205,
        "col_step": 0.010986328125,
        "start_row_num": 13460,
        "start_col_num": 27156,
        "end_row_num": 13605,
        "end_col_num": 27372
    },
    "17": {
        "row": 290,
        "col": 433,
        "left_top_latitude": 30.566990873153333,
        "left_top_longitude": 118.3392333984375,
        "right_down_latitude": 29.18577000170337,
        "right_down_longitude": 120.7177734375,
        "row_step": 0.0047628305912067615,
        "col_step": 0.0054931640625,
        "start_row_num": 26920,
        "start_col_num": 54312,
        "end_row_num": 27209,
        "end_col_num": 54744
    },
    "18": {
        "row": 579,
        "col": 866,
        "left_top_latitude": 30.566990873153333,
        "left_top_longitude": 118.3392333984375,
        "right_down_latitude": 29.188151416998977,
        "right_down_longitude": 120.7177734375,
        "row_step": 0.0023814152956033808,
        "col_step": 0.00274658203125,
        "start_row_num": 53839,
        "start_col_num": 108623,
        "end_row_num": 54417,
        "end_col_num": 109488
    }
}