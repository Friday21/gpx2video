#!/usr/bin/env python
# -*- coding: utf-8 -*-


map_path = '/Users/friday/娱乐/google_map/西湖/satellite'
level_list = [10, 11, 12, 13, 14, 15, 16, 17, 18]

indexes = {
    "10": {
        "row": 2,
        "col": 1,
        "left_top_latitude": 30.44867367928756,
        "left_top_longitude": 119.8828125,
        "right_down_latitude": 29.84064389983441,
        "right_down_longitude": 120.234375,
        "row_step": 0.3044832835417033,
        "col_step": 0.3515625,
        "start_row_num": 421,
        "start_col_num": 853,
        "end_row_num": 422,
        "end_col_num": 853
    },
    "11": {
        "row": 2,
        "col": 2,
        "left_top_latitude": 30.29701788337205,
        "left_top_longitude": 119.8828125,
        "right_down_latitude": 29.99300228455107,
        "right_down_longitude": 120.234375,
        "row_step": 0.15212489882504343,
        "col_step": 0.17578125,
        "start_row_num": 843,
        "start_col_num": 1706,
        "end_row_num": 844,
        "end_col_num": 1707
    },
    "12": {
        "row": 3,
        "col": 4,
        "left_top_latitude": 30.29701788337205,
        "left_top_longitude": 119.8828125,
        "right_down_latitude": 30.06909396443886,
        "right_down_longitude": 120.234375,
        "row_step": 0.07603321893725479,
        "col_step": 0.087890625,
        "start_row_num": 1686,
        "start_col_num": 3412,
        "end_row_num": 1688,
        "end_col_num": 3415
    },
    "13": {
        "row": 5,
        "col": 7,
        "left_top_latitude": 30.29701788337205,
        "left_top_longitude": 119.9267578125,
        "right_down_latitude": 30.10711788709237,
        "right_down_longitude": 120.234375,
        "row_step": 0.038009296283743055,
        "col_step": 0.0439453125,
        "start_row_num": 3372,
        "start_col_num": 6825,
        "end_row_num": 3376,
        "end_col_num": 6831
    },
    "14": {
        "row": 9,
        "col": 14,
        "left_top_latitude": 30.29701788337205,
        "left_top_longitude": 119.9267578125,
        "right_down_latitude": 30.12612436422458,
        "right_down_longitude": 120.234375,
        "row_step": 0.019002819151534567,
        "col_step": 0.02197265625,
        "start_row_num": 6744,
        "start_col_num": 13650,
        "end_row_num": 6752,
        "end_col_num": 13663
    },
    "15": {
        "row": 17,
        "col": 26,
        "left_top_latitude": 30.29701788337205,
        "left_top_longitude": 119.937744140625,
        "right_down_latitude": 30.135626231134587,
        "right_down_longitude": 120.223388671875,
        "row_step": 0.009500952241527472,
        "col_step": 0.010986328125,
        "start_row_num": 13488,
        "start_col_num": 27301,
        "end_row_num": 13504,
        "end_col_num": 27326
    },
    "16": {
        "row": 33,
        "col": 51,
        "left_top_latitude": 30.29701788337205,
        "left_top_longitude": 119.9432373046875,
        "right_down_latitude": 30.140376821599734,
        "right_down_longitude": 120.223388671875,
        "row_step": 0.004750361776380885,
        "col_step": 0.0054931640625,
        "start_row_num": 26976,
        "start_col_num": 54603,
        "end_row_num": 27008,
        "end_col_num": 54653
    },
    "17": {
        "row": 65,
        "col": 100,
        "left_top_latitude": 30.29701788337205,
        "left_top_longitude": 119.94598388671875,
        "right_down_latitude": 30.142752031075375,
        "right_down_longitude": 120.22064208984375,
        "row_step": 0.0023751523007398134,
        "col_step": 0.00274658203125,
        "start_row_num": 53952,
        "start_col_num": 109207,
        "end_row_num": 54016,
        "end_col_num": 109306
    },
    "18": {
        "row": 129,
        "col": 199,
        "left_top_latitude": 30.295832146790435,
        "left_top_longitude": 119.94735717773438,
        "right_down_latitude": 30.142752031075375,
        "right_down_longitude": 120.22064208984375,
        "row_step": 0.0011875832974048706,
        "col_step": 0.001373291015625,
        "start_row_num": 107905,
        "start_col_num": 218415,
        "end_row_num": 108033,
        "end_col_num": 218613
    },
    "19": {
        "row": 256,
        "col": 397,
        "left_top_latitude": 30.295239273123183,
        "left_top_longitude": 119.94735717773438,
        "right_down_latitude": 30.14334582451081,
        "right_down_longitude": 120.21995544433594,
        "row_step": 0.0005937898619698956,
        "col_step": 0.0006866455078125,
        "start_row_num": 215811,
        "start_col_num": 436830,
        "end_row_num": 216066,
        "end_col_num": 437226
    },
    "20": {
        "row": 511,
        "col": 793,
        "left_top_latitude": 30.294942834945473,
        "left_top_longitude": 119.94735717773438,
        "right_down_latitude": 30.14334582451081,
        "right_down_longitude": 120.21961212158203,
        "row_step": 0.00029689537766586227,
        "col_step": 0.00034332275390625,
        "start_row_num": 431623,
        "start_col_num": 873660,
        "end_row_num": 432133,
        "end_col_num": 874452
    }
}