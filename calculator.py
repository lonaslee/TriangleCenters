def GetInputs() -> tuple:
    in1 = CleanInputs(input('A:\n'))
    in2 = CleanInputs(input('B:\n'))
    in3 = CleanInputs(input('C:\n'))
    if len(in1) != 2 or len(in2) != 2 or len(in3) != 2:
        raise IndexError('the inputs are not correctly formatted')
    a = {'x':float(in1[0]), 'y':float(in1[1])}
    b = {'x':float(in2[0]), 'y':float(in2[1])}
    c = {'x':float(in3[0]), 'y':float(in3[1])}
    return (a, b, c)


def CleanInputs(inp) -> list:
    inp = inp.strip('()')
    inp = inp.replace(',', ' ')
    while '  ' in inp:
        inp = inp.replace('  ', ' ')
    inp = inp.strip()
    return inp.split(' ')


def Slope(x1, y1, x2, y2) -> float:
    if x2-x1 == 0:
        return 0
    elif y2-y1 == 0:
        return ''
    else:
        M = (y2-y1)/(x2-x1)
        return DeciMate(M)


def Solve(eq1, eq2) -> tuple:
    x1M, x2M = FindM(eq1, eq2)
    x1B, x2B = FindB(eq1, eq2)
    M, Xside = OneSideX(x1M, x2M)
    B = OneSideB(x1B, x2B, Xside)
    FinalX = DeciMate(B/M)
    FinalY1 = DeciMate(PlugIn(x1M, FinalX, x1B))
    FinalY2 = DeciMate(PlugIn(x2M, FinalX, x2B))
    return (FinalX, Average(FinalY1, FinalY2))


def FindM(eq1, eq2) -> tuple:
    x1M, x2M = eq1[0:eq1.index('x')], eq2[0:eq2.index('x')]
    if x1M == '-':
        x1M = '-1.0'
    if x2M == '-':
        x2M == '-1.0'
    if x1M == '':
        x1M = '1.0'
    if x2M == '':
        x2M == '1.0'
    return (DeciMate(float(x1M)), DeciMate(float(x2M)))


def FindB(eq1, eq2) -> tuple:
    x1B, x2B = eq1[eq1.index('x')+1:], eq2[eq2.index('x')+1:]
    if x1B == '':
        x1B = '0.0'
    if x2B == '':
        x2B = '0.0'
    return (DeciMate(float(x1B)), DeciMate(float(x2B)))


def OneSideX(x1M, x2M) -> tuple:
    if x1M > 0 and x2M > 0: #pos pos
        if x1M > x2M:
            M = DeciMate(x1M-x2M)
            MSide = 'L'
        else:
            M = DeciMate(x2M-x1M)
            MSide = 'R'
    elif x1M < 0:
        if x2M > 0: #neg pos
            M = DeciMate(x2M+x1M*-1)
            MSide = 'R'
        else: #neg neg
            if x1M < x2M:
                M = DeciMate(x1M+x2M*-1)
                MSide = 'L'
            else:
                M = DeciMate(x2M+x1M*-1)
                MSide = 'R'
    else: #pos neg
        M = DeciMate(x1M+x2M*-1)
        MSide = 'L'
    return (M, MSide)


def OneSideB(x1B, x2B, XSide) -> float:
    if x1B > 0 and x2B > 0:
        if XSide == 'L': #pos pos left
            B = x2B-x1B
        else: #pos pos right
            B = x1B-x2B
    elif x1B < 0:
        if x2B > 0:
            if XSide == 'L': #neg pos left   
                B = x1B*-1+x2B
            else: #neg pos right
                B = x1B-x2B
        else:
            if XSide == 'L': #neg neg left
                B = x2B+x1B*-1
            else: #neg neg right
                B = x1B+x2B*-1
    else:
        if XSide == 'L': #pos neg left
            B = x2B-x1B
        else: # pos neg right
            B = x1B+x2B*-1
    return B


def PlugIn(M, xVal, B) -> float:
    return DeciMate(M*xVal)+B


def Average(*nums: tuple) -> float:
    Sum = 0
    for onenum in nums:
        Sum += onenum
    return DeciMate((Sum)/len(nums))


def Clean(dusty: str) -> str:
    dusty = dusty.replace('--', '+')
    dusty = dusty.removesuffix('-0.0')
    dusty = dusty.removesuffix('+0.0')
    dusty = dusty.replace('x0.0', 'x')
    dusty = dusty.replace('0.0x+', '')
    dusty = dusty.replace('0.0x-', '')
    return dusty


def DeciMate(num) -> float:
    return round(num, 3)


def Coords(Point='O', **kpoints) -> tuple:
    if Point == 'O':
        hLine = (
            'A' if kpoints['eq1']['pr'] == f'y={kpoints["a"]["y"]}' else
            'B' if kpoints['eq2']['pr'] == f'y={kpoints["b"]["y"]}' else
            'C' if kpoints['eq3']['pr'] == f'y={kpoints["c"]["y"]}' else None
        )
        vLine = (
            'A' if kpoints['eq1']['pr'] == f'x={kpoints["a"]["x"]}' else
            'B' if kpoints['eq2']['pr'] == f'x={kpoints["b"]["x"]}' else
            'C' if kpoints['eq3']['pr'] == f'x={kpoints["c"]["x"]}' else None
        )
    else:
        hLine = (
            'A' if 'x+' not in kpoints['eq1']['pr']
                and 'x-' not in kpoints['eq1']['pr']
                and 'y=' in kpoints['eq1']['pr'] else
            'B' if 'x+' not in kpoints['eq2']['pr']
                and 'x-' not in kpoints['eq2']['pr']
                and 'y=' in kpoints['eq2']['pr'] else
            'C' if 'x+' not in kpoints['eq3']['pr']
                and 'x-' not in kpoints['eq3']['pr']
                and 'y=' in kpoints['eq3']['pr'] else None
        )
        vLine = (
            'A' if 'x=' in kpoints['eq1']['pr'] else
            'B' if 'x=' in kpoints['eq2']['pr'] else
            'C' if 'x=' in kpoints['eq3']['pr'] else None
        )
    if hLine == None:
        if vLine == None: # straight to solve
            Solve1 = Solve(kpoints['eq1']['eq'], kpoints['eq2']['eq'])
            Solve2 = Solve(kpoints['eq2']['eq'], kpoints['eq3']['eq'])
            Solve3 = Solve(kpoints['eq3']['eq'], kpoints['eq1']['eq'])
            return (Average(Solve1[0], Solve2[0], Solve3[0]), 
                    Average(Solve1[1], Solve2[1], Solve3[1]))
        elif vLine == 'A': # solve with B and C
            return (Solve(kpoints['eq2']['eq'], kpoints['eq3']['eq']))
        elif vLine == 'B': # sw A C
            return (Solve(kpoints['eq1']['eq'], kpoints['eq3']['eq']))
        else: # 'C' sw A B
            return (Solve(kpoints['eq1']['eq'], kpoints['eq2']['eq']))
    elif hLine == 'A':
        if vLine == None:
            return (Solve(kpoints['eq2']['eq'], kpoints['eq3']['eq']))
        elif vLine == 'B': # y of A, x of B
            return (
                DeciMate(kpoints['b']['x']), DeciMate(kpoints['a']['y'])
                if Point == 'O' else 
                DeciMate(float(kpoints['eq2']['eq'])),
                DeciMate(float(kpoints['eq1']['eq']))
            )
        else: # 'C'
            return (
                DeciMate(kpoints['c']['x']), DeciMate(kpoints['a']['y'])
                if Point == 'O' else
                DeciMate(float(kpoints['eq3']['eq'])),
                DeciMate(float(kpoints['eq1']['eq']))
            )
    elif hLine == 'B':
        if vLine == None:
            return Solve(kpoints['eq1']['eq'], kpoints['eq3']['eq'])
        elif vLine == 'A': # y of b
            return (
                DeciMate(kpoints['a']['x']), DeciMate(kpoints['b']['y'])
                if Point == 'O' else
                DeciMate(float(kpoints['eq1']['eq'])),
                DeciMate(float(kpoints['eq2']['eq']))
            )
        else: # 'C'
            return (
                DeciMate(kpoints['c']['x']), DeciMate(kpoints['b']['y'])
                if Point == 'O' else 
                DeciMate(float(kpoints['eq3']['eq'])),
                DeciMate(float(kpoints['eq2']['eq']))
            )
    else: # 'C'
        if vLine == None:
            return Solve(kpoints['eq1']['eq'], kpoints['eq2']['eq'])
        elif vLine == 'A': # y of c
            return (
                DeciMate(kpoints['a']['x']), DeciMate(kpoints['c']['y'])
                if Point == 'O' else 
                DeciMate(float(kpoints['eq1']['eq'])),
                DeciMate(float(kpoints['eq3']['eq']))
            )
        else: # 'B'
            return (
                DeciMate(kpoints['b']['x']), DeciMate(kpoints['c']['y'])
                if Point == 'O' else
                DeciMate(float(kpoints['eq2']['eq'])),
                DeciMate(float(kpoints['eq3']['eq']))
            )


def SlopeEquation(m, x1, y1, per=False) -> dict:
    if m == '':
        ForPrint, ForEq = f'x={x1}', f'{x1}'
    elif m == 0:
        ForPrint, ForEq = f'y={y1}', f'{y1}'
    else:
        m = (m*-1)**-1 if per == False else m # perpendicular
        if m*x1*-1 + y1 < 0:
            ForPrint = f'y={DeciMate(m)}x{DeciMate(m*x1*-1+y1)}'
            ForEq = f'{m}x{m*x1*-1+y1}'
        else:
            ForPrint = f'y={DeciMate(m)}x+{DeciMate(m*x1*-1+y1)}'
            ForEq = f'{m}x+{m*x1*-1+y1}'
    ForPrint, ForEq = Clean(ForPrint), Clean(ForEq)
    return {'pr':ForPrint, 'eq':ForEq}


def Orthocenter(a, b, c) -> str:
    AltA = SlopeEquation(Slope(b['x'], b['y'], c['x'], c['y']), a['x'], a['y'])
    AltB = SlopeEquation(Slope(a['x'], a['y'], c['x'], c['y']), b['x'], b['y'])
    AltC = SlopeEquation(Slope(a['x'], a['y'], b['x'], b['y']), c['x'], c['y'])
    Ortho = Coords(eq1=AltA, eq2=AltB, eq3=AltC, a=a, b=b, c=c)
    return (
        f'Altitude A: {AltA["pr"]}\nAltitude B: {AltB["pr"]}\n'
        f'Altitude C: {AltC["pr"]}\nOrthocenter: {Ortho}\n\n'
    )


def Circumcenter(a, b, c) -> str:
    PerA = (SlopeEquation(Slope(b['x'], b['y'], c['x'], c['y']),
            Average(b['x'], c['x']), Average(b['y'], c['y'])))
    PerB = (SlopeEquation(Slope(a['x'], a['y'], c['x'], c['y']),
            Average(a['x'], c['x']), Average(a['y'], c['y'])))
    PerC = (SlopeEquation(Slope(a['x'], a['y'], b['x'], b['y']),
            Average(a['x'], b['x']), Average(a['y'], b['y'])))
    Circum = Coords('C', eq1=PerA, eq2=PerB, eq3=PerC, a=a, b=b, c=c)
    return (
        f'Perpendicular Bisector of AB: {PerC["pr"]}\n'
        f'Perpendicular Bisector of AC: {PerB["pr"]}\n'
        f'Perpendicular Bisector of BC: {PerA["pr"]}\n'
        f'Circumcenter: {Circum}\n\n'
    )


def Centroid(a, b, c) -> str:
    MedA = (SlopeEquation(Slope((b["x"]+c["x"])/2, (b["y"]+c["y"])/2,
            a["x"], a["y"]), a['x'], a['y'], True))
    MedB = (SlopeEquation(Slope((a["x"]+c["x"])/2, (a["y"]+c["y"])/2,
            b["x"], b["y"]), b['x'], b['y'], True))
    MedC = (SlopeEquation(Slope((a["x"]+b["x"])/2, (a["y"]+b["y"])/2,
            c["x"], c["y"]), c['x'], c['y'], True))
    Centro = (Average(a['x'], b['x'], c['x']), Average(a['y'], b['y'], c['y']))
    return (
        f'Median A: {MedA["pr"]}\nMedian B: {MedB["pr"]}\n'
        f'Median C: {MedC["pr"]}\nCentroid: {Centro}'
    )


def Execute() -> str:
    a, b, c = GetInputs()
    ABSlope = (SlopeEquation(Slope(a["x"], a["y"], b["x"], b["y"]),
                a["x"], a["y"], True)["pr"])
    ACSlope = (SlopeEquation(Slope(a["x"], a["y"], c["x"], c["y"]),
                a["x"], a["y"], True)["pr"])
    BCSlope = (SlopeEquation(Slope(b["x"], b["y"], c["x"], c["y"]),
                b["x"], b["y"], True)["pr"])
    FinalString = (
        f'A({a["x"]}, {a["y"]}) B({b["x"]}, {b["y"]}) C({c["x"]}, {c["y"]})\n'
        f'Slope of AB: {ABSlope}\nSlope of AC: {ACSlope}\n'
        f'Slope of BC: {BCSlope}\n\n'
    )
    for cent in (Orthocenter, Circumcenter, Centroid):
        FinalString = FinalString+cent(a, b, c)
    return FinalString


print(Execute())
