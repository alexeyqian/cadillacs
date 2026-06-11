def point_in_polygon(point, polygon):
    x, y = point
    inside = False
    j = len(polygon) -1
    for i in range(len(polygon)):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        
        crosses = ((yi > y) != (yj > y))
        if crosses:
            x_at_y = (xj-xi)*(y-yi)/(yj-yi) + xi
            if x < x_at_y:
                inside = not inside
        j = i
    return inside

def entity_feet_point(entity):
    return entity.x, entity.y

def entity_is_inside_walkable_area(entity, level):
    if not level.walkable_polygon:
        return True

    feet = entity_feet_point(entity)
    return point_in_polygon(feet, level.walkable_polygon)