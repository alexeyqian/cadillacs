class LaneSystem:
    def __init__(self, lane_top, lane_bottom, lane_count=4):
        self.lane_top = lane_top
        self.lane_bottom = lane_bottom
        self.lane_count = lane_count
        self.lane_height = (lane_bottom - lane_top) / lane_count

    def get_lane_index(self, y):
        raw_index = int((y - self.lane_top) / self.lane_height)
        return max(0, min(self.lane_count - 1, raw_index))

    def get_lane_center(self, lane_index):
        lane_index = max(0, min(self.lane_count - 1, lane_index))
        return self.lane_top + self.lane_height * (lane_index + 0.5)

    def get_lane_distance(self, y_a, y_b):
        return abs(self.get_lane_index(y_a) - self.get_lane_index(y_b))

    def get_lane_bounds(self, lane_index):
        lane_index = max(0, min(self.lane_count - 1, lane_index))
        top = self.lane_top + self.lane_height * lane_index
        bottom = top + self.lane_height
        return top, bottom