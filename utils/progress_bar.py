# -*- coding: utf-8 -*-


def draw_progress_bar(value, range_max=100, units=20):
    if value < 0 or range_max < 0:
        raise ValueError('contains invalid value (less than 0).')
        
    text = '['
    
    if range_max < units:
        unit_len = units / range_max
        finished_units = round(value * unit_len)
    else:
        unit_len = range_max / units
        finished_units = round(value / unit_len)
    
    if value < range_max:
        text = text + '=' * min(finished_units, units-1)
        text = text + '>'
    else:
        text = text + '=' * units
        
    text = text + ' ' * max(units - finished_units - 1, 0) + ']'

    # print(value, range_max, unit_len, units, finished_units)

    return text

