# The reference for the implementation is this link
# https://developers.google.com/maps/documentation/utilities/polylinealgorithm?hl=en
# it decodes and encodes some test values, have fun playing with it.


#def encode_coordinate(value):
#    value = int(value * 1E5)
#    value = ~(value << 1) if value < 0 else (value << 1)
#
#    res = []
#    while value > 0:
#        chunck = value & 0x1f
#        value >>= 5
#        if value > 0:
#            chunck |= 0x20
#        res.insert(len(res), chr(chunck + 63))
#
#    return "".join(res)
#
#
#def make_polyline(cords):
#    last_lat = 0
#    last_lng = 0
#    return_poly = ""
#    for cord in cords:
#        return_poly += encode_coordinate(cord[0] - last_lat)
#        return_poly += encode_coordinate(cord[1] - last_lng)
#        last_lat = cord[0]
#        last_lng = cord[1]
#    return return_poly
#
#
#def decode_poly(ply):
#    i = 0
#    last_coord = 0
#    all_coord = []
#    for char in ply:
#        point = ord(char) - 63
#        last_coord |= (point & 0x1f) << (i * 5)
#        if not (point & 0x20):
#            last_coord = ~last_coord if last_coord & 0x1 else last_coord
#            last_coord = (last_coord >> 1) / 1E5
#            all_coord.append(last_coord)
#            i = 0
#            last_coord = 0
#        else:
#            i += 1
#    points = []
#    for i in range(0, len(all_coord) - 1, 2):
#        if all_coord[i] == 0 and all_coord[i + 1] == 0:
#            continue
#        if i != 0:
#            all_coord[i] += all_coord[i - 2]
#            all_coord[i + 1] += all_coord[i - 1]
#        points.append((round(all_coord[i], 6), round(all_coord[i + 1], 6)))
#    return points
#
#cords = [[(44.360650, 25.924409), (48.197622, 16.300385), (52.522857, -1.849029), (42.119599, 9.050593)],]

#for cord in cords:
#    poly = make_polyline(cord)
#    print(poly, "https://www.google.com.eg/maps/dir/" + "/".join(list(map(lambda x: str(x[0]) + "," + str(x[1]), decode_poly(poly)))))
#    print(poly, "https://www.google.com.eg/maps/dir/" + "/".join(list(map(lambda x: str(x[0]) + "," + str(x[1]), cord))))


#url = "http://maps.googleapis.com/maps/api/staticmap?size=800x800&path={0}"


