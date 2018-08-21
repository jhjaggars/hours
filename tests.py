from days_parser import days_parser

def test_Su():
    assert days_parser("Su") == [0]
    assert days_parser("su") == [0]

def test_M():
    assert days_parser("M") == [1]
    assert days_parser("m") == [1]

def test_Tu():
    assert days_parser("Tu") == [2]
    assert days_parser("tu") == [2]

def test_W():
    assert days_parser("W") == [3]
    assert days_parser("w") == [3]

def test_Th():
    assert days_parser("Th") == [4]
    assert days_parser("th") == [4]

def test_F():
    assert days_parser("F") == [5]
    assert days_parser("f") == [5]

def test_Sa():
    assert days_parser("Sa") == [6]
    assert days_parser("sa") == [6]

def test_multiple_days():
    assert days_parser("Su,M") == [0, 1]
    assert days_parser("Su, M") == [0, 1]
    assert days_parser("MWF") == [1, 3, 5]

def test_day_range():
    assert days_parser("M-F") == [1,2,3,4,5]
