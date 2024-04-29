#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ---------------------------------------------------------------------------------------------------------------------
#%% Imports

import cv2
import numpy as np


# ---------------------------------------------------------------------------------------------------------------------
#%% Classes

class ArucoDetector:
    
    BOX_COLOR = (0, 255, 0)
    TEXT_COLOR = (0, 255, 0)
    AXIS_COLOR = (0, 0, 255)
    CENTER_COLOR = (0, 0, 255)
    
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    FONTSCALE = 1
    ARROWSCALE = 0.55
    
    def __init__(self):
        self._size_id_detectors_dict = self._make_all_detectors()
        self._num_detectors = len(self._size_id_detectors_dict)
        
        self._size_select, maxid_dict = get_first_dict_item(self._size_id_detectors_dict)
        self._maxid_select, _ = get_first_dict_item(maxid_dict)
    
    def get_model_names(self) -> list[str]:
        return list(self._name_to_model_dict.keys())
    
    def set_model_select(self, model_select: str):
        self._model_select = model_select
        return self
    
    def select_detector(self, marker_size: str, max_ids: int | str):
    
        self._size_select = marker_size
        self._maxid_select = str(max_ids)
        
        return self
    
    def process_frame(self, frame):
        
        detector = self._size_id_detectors_dict[self._size_select][self._maxid_select]
        aru_xys_px, aru_ids, _ = detector.detectMarkers(frame)
        results = (aru_xys_px, aru_ids)
        
        return results
    
    def draw_results(self, results, display_frame):
        
        # For clarity
        aru_xys_px, aru_ids = results
        
        # Bail if there are no detection results
        no_data = len(aru_xys_px) == 0
        if no_data:
            return display_frame
        
        for pt_id, pts_xy_px in zip(aru_ids, aru_xys_px):
            
            # For convenience
            pt_id = pt_id.ravel()[0]
            pts_xy_i32 = np.int32(pts_xy_px)
            min_x, min_y = np.min(pts_xy_i32, axis=1).squeeze()
            max_x, max_y = np.max(pts_xy_i32, axis=1).squeeze()
            mid_x = int((min_x + max_x) * 0.5)
            mid_y = int((min_y + max_y) * 0.5)
            
            # Draw orientation arrows
            tl,tr,br,bl = pts_xy_i32.squeeze()
            x_arrow = np.int32(br + (br - bl) * self.ARROWSCALE)
            y_arrow = np.int32(tl + (tl - bl) * self.ARROWSCALE)
            draw_line(display_frame, br, x_arrow, self.AXIS_COLOR)
            draw_line(display_frame, tl, y_arrow, self.AXIS_COLOR)
            
            # Draw center point
            circ_xy = (mid_x, mid_y)
            cv2.circle(display_frame, circ_xy, 3, self.CENTER_COLOR, -1)
            
            # Draw main detection box
            draw_polygon(display_frame, pts_xy_i32, self.BOX_COLOR)
            
            # Draw ID text
            id_txt = f"ID: {pt_id}"
            (txt_w, txt_h), txt_baseline = cv2.getTextSize(id_txt, self.FONT, self.FONTSCALE, 3)
            txt_xy = (mid_x - txt_w//2, mid_y + txt_h//2)
            draw_text(display_frame, id_txt, txt_xy, self.TEXT_COLOR)
        
        return display_frame

    def _make_all_detectors(self) -> dict:
        
        aruco_dict_lut = {
            "4x4": {
                "50": cv2.aruco.DICT_4X4_50,
                "100": cv2.aruco.DICT_4X4_100,
                "250": cv2.aruco.DICT_4X4_250,
                "1000": cv2.aruco.DICT_4X4_1000,
            },
            "5x5": {
                "50": cv2.aruco.DICT_5X5_50,
                "100": cv2.aruco.DICT_5X5_100,
                "250": cv2.aruco.DICT_5X5_250,
                "1000": cv2.aruco.DICT_5X5_1000,
            },
            "6x6": {
                "50": cv2.aruco.DICT_6X6_50,
                "100": cv2.aruco.DICT_6X6_100,
                "250": cv2.aruco.DICT_6X6_250,
                "1000": cv2.aruco.DICT_6X6_1000,
            },
            "7x7": {
                "50": cv2.aruco.DICT_7X7_50,
                "100": cv2.aruco.DICT_7X7_100,
                "250": cv2.aruco.DICT_7X7_250,
                "1000": cv2.aruco.DICT_7X7_1000,
            },
        }
        
        # Make all detectors for each marker size
        size_id_detector_lut = {}
        for marker_size_str, maxid_lut in aruco_dict_lut.items():
            
            # Make detector for each max-id count
            det_per_maxid_lut = {}
            for maxid_str, aru_code in maxid_lut.items():
                aru_dict = cv2.aruco.getPredefinedDictionary(aru_code)
                aru_params = cv2.aruco.DetectorParameters()
                aru_detector = cv2.aruco.ArucoDetector(aru_dict, aru_params)
                det_per_maxid_lut[maxid_str] = aru_detector
            size_id_detector_lut[marker_size_str] = det_per_maxid_lut
        
        return size_id_detector_lut


# ---------------------------------------------------------------------------------------------------------------------
#%% Functions

def draw_line(frame, xy1, xy2, fg_color = (0,255, 0),
              fg_thickness = 3, bg_color = (0,0,0), bg_thickness = 5, line_type = cv2.LINE_AA):
    
    ''' Helper used to draw lines with backgrounds for better contrast '''
    
    frame = cv2.line(frame, xy1, xy2, bg_color, bg_thickness, line_type)
    frame = cv2.line(frame, xy1, xy2, fg_color, fg_thickness, line_type)
    
    return frame

def draw_polygon(frame, xy_points_i32, fg_color = (0,255,0),
                 fg_thickness = 3, bg_color = (0,0,0), bg_thickness = 5, line_type = cv2.LINE_AA):
    
    ''' Helper used to draw closed polygons with backgrounds for better contrast '''
    
    frame = cv2.polylines(frame, xy_points_i32, True, bg_color, bg_thickness, line_type)
    frame = cv2.polylines(frame, xy_points_i32, True, fg_color, fg_thickness, line_type)
    
    return frame

def draw_text(frame, text_str, text_position, fg_color = (0,255,0),
              fg_thickness = 3, bg_color = (0,0,0), bg_thickness = 5,
              font = cv2.FONT_HERSHEY_SIMPLEX, font_scale = 1, line_type = cv2.LINE_AA):
    
    ''' Helper used to draw text with background '''
    
    frame = cv2.putText(frame, text_str, text_position, font, font_scale, bg_color, bg_thickness, line_type)
    frame = cv2.putText(frame, text_str, text_position, font, font_scale, fg_color, fg_thickness, line_type)
    
    return frame

def get_first_dict_item(dictionary: dict):
    return next(iter(dictionary.items()))
