from fern import Transformation 
       
T1 = [[0,0],
        [0, 0.16]]
T2 = [[0.85, 0.04],
    [-0.04, 0.85]]
T3 = [[0.2, -0.26],
    [0.23, 0.22]]
T4 = [[-0.15, 0.28],
    [0.26, 0.24]]
offset1 = [0,0]
offset2 = [0, 1.6]
offset3 = [0, 1.6]
offset4 = [0, 0.44]
p1 = 0.01
p2 = 0.85
p3 = 0.07
p4 = 0.07
trans_list = []
for T, offset,prob in zip([T1, T2, T3, T4], [offset1, offset2, offset3, offset4], [p1,p2,p3,p4]):
    trans = Transformation(T, offset,prob)
    trans_list.append(trans)