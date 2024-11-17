class PricePoint:
    def __init__(self, date, value):
        self.date = date
        self.value = value


class SMA:
    def __init__(self, period, points):
        self.period = period
        self.points = points


class CupWithHandle:
    def __init__(self):
        self.right_high = None
        self.low_handle = None
        self.dip = None
        self.left_high = None


def get_nearest_cup_with_handle(sma, trace_from=-1):
    # Constants
    fluc = 0.1
    cup_depth_right_max = 0.4
    cup_depth_right_min = 0.15
    cup_depth_left_max = 0.45
    cup_depth_left_min = 0.18
    high_diff = 0.1
    handle_depth = 0.15
    max_peak_dip = 0.85

    cwh = CupWithHandle()
    n = len(sma.points)
    i = trace_from if 0 < trace_from < n else n - 1

    # Find the right high point
    rh = i
    while i > 0 and (
        sma.points[i - 1].value >= sma.points[i].value or
        (sma.points[i - 1].value < sma.points[i].value and
         sma.points[i - 1].value >= (1 - fluc) * sma.points[rh].value)
    ):
        if sma.points[i - 1].value >= sma.points[rh].value:
            rh = i - 1
        i -= 1
    if i <= 0 or rh == trace_from:
        return None
    cwh.right_high = sma.points[rh]

    # Extend low handle
    j = rh
    low_right = rh
    while j < n - 1 and (
        sma.points[j + 1].value <= sma.points[j].value or
        (sma.points[j + 1].value > sma.points[j].value and
         sma.points[j + 1].value <= (1 + fluc) * sma.points[low_right].value)
    ):
        if sma.points[j + 1].value <= sma.points[low_right].value:
            low_right = j + 1
        j += 1
    cwh.low_handle = sma.points[low_right]

    # Validate handle depth
    if (cwh.right_high.value - cwh.low_handle.value > handle_depth * cwh.right_high.value or
            cwh.right_high.value - cwh.low_handle.value <= 0):
        return None

    # Find dip point
    dip = i
    while i > 0 and (
        sma.points[i - 1].value <= sma.points[i].value or
        (sma.points[i - 1].value > sma.points[i].value and
         sma.points[i - 1].value <= (1 + fluc) * sma.points[dip].value) or
        sma.points[i - 1].value < max_peak_dip * cwh.right_high.value
    ):
        if sma.points[i - 1].value <= sma.points[dip].value:
            dip = i - 1
        i -= 1
    if i <= 0:
        return None
    cwh.dip = sma.points[dip]

    # Validate dip price
    dip_change = cwh.right_high.value - cwh.dip.value
    if dip_change < cup_depth_right_min * cwh.right_high.value or dip_change > cup_depth_right_max * cwh.right_high.value:
        return None

    # Find left high point
    lh = i
    while i > 0 and (
        sma.points[i - 1].value >= sma.points[i].value or
        (sma.points[i - 1].value < sma.points[i].value and
         sma.points[i - 1].value >= (1 - fluc) * sma.points[lh].value)
    ):
        if sma.points[i - 1].value >= sma.points[lh].value:
            lh = i - 1
        i -= 1
    cwh.left_high = sma.points[lh]

    # Validate left dip price
    dip_change = cwh.left_high.value - cwh.dip.value
    if dip_change < cup_depth_left_min * cwh.left_high.value or dip_change > cup_depth_left_max * cwh.left_high.value:
        return None

    # Validate cup width and left-right high price difference
    cup_width = rh - lh
    if cup_width < 25 or cup_width > 130:
        return None
    if abs(cwh.right_high.value - cwh.left_high.value) > high_diff * cwh.right_high.value:
        return None

    return cwh
