import random
from sympy import symbols, Eq, solve

# Các thành phần để tạo câu hỏi đa dạng
objects_2 = ["vật thể", "đồ vật", "hòn đá", "trái bóng", "đồ chơi"]
actions_2 = ["rơi tự do", "bị thả rơi", "được thả từ độ cao", "bị ném từ trên cao"]
reaches_2 = ["chạm đất", "tiếp đất", "chạm mặt đất", "đập vào mặt đất"]
questions_2 = ["Hỏi vật được thả rơi từ độ cao nào?", "Vật được thả từ độ cao bao nhiêu?", "Độ cao thả vật là bao nhiêu?"]

def generate_problem_type2():
    # Chọn ngẫu nhiên thành phần trong câu hỏi
    obj = random.choice(objects_2)
    action = random.choice(actions_2)
    reach = random.choice(reaches_2)
    question = random.choice(questions_2)
    
    # Chọn ngẫu nhiên vận tốc cuối cùng khi chạm đất
    v = random.randint(15, 30)  # m/s
    g = 10  # m/s², gia tốc trọng trường

    problem = f"""
    <p><strong>Một {obj} {action} khi {reach} thì đạt vận tốc v = {v} m/s.</strong></p>
    <p><strong>{question} Biết gia tốc trọng trường g = {g} m/s<sup>2</sup>.</strong></p>
    """
    
    return problem, v, g

def calculate_solution_type2(v, g):
    # Tính thời gian rơi
    t = v / g  # t = v/g
    
    # Tính quãng đường rơi
    h = 0.5 * g * t**2  # h = 1/2 * g * t^2
    
    solution = f"""
    <p><strong>Đáp án:</strong></p>
    <p><strong>1) Tính thời gian rơi:</strong></p>
    <ul>
        <li>Vận tốc cuối v = {v} m/s</li>
        <li>Gia tốc trọng trường g = {g} m/s<sup>2</sup></li>
        <li>Thời gian rơi t = v / g = {v} / {g} = {t:.2f} giây</li>
    </ul>
    <p><strong>2) Tính quãng đường rơi:</strong></p>
    <ul>
        <li>Quãng đường rơi h = 1/2 * g * t<sup>2</sup></li>
        <li>h = 1/2 * {g} * {t:.2f}<sup>2</sup> = {h:.2f} mét</li>
    </ul>
    """
    
    solution = solution.replace(".", ",")
    return solution


# Các thành phần để tạo câu hỏi đa dạng
heights = ["100 m", "200 m", "150 m", "250 m", "300 m"]
initial_velocities = [10, 20, 15, 25, 30]
objects_3 = ["một vật", "một hòn đá", "một quả bóng", "một chiếc máy bay giấy", "một món đồ chơi"]
directions = ["thẳng đứng xuống", "từ trên cao xuống", "theo phương thẳng đứng", "theo phương thẳng"]

def generate_problem_type3():
    # Chọn ngẫu nhiên thành phần trong câu hỏi
    height = random.choice(heights)
    v0 = random.choice(initial_velocities)
    obj = random.choice(objects_3)
    direction = random.choice(directions)
    g = 10  # m/s², gia tốc trọng trường

    problem = f"""
    <p><strong>Từ độ cao {height} người ta thả {obj} {direction} với v<sub>0</sub> = {v0} m/s, g = {g} m/s<sup>2</sup>.</strong></p>
    <p><strong>a. Sau bao lâu vật chạm đất.</strong></p>
    <p><strong>b. Tính vận tốc của vật lúc vừa chạm đất.</strong></p>
    """
    
    return problem, height, v0, g

def calculate_solution_type3(height, v0, g):
    # Chuyển đổi height từ chuỗi sang số
    h = int(height.split()[0])
    
    # Biến số
    t = symbols('t')
    
    # Phương trình quãng đường rơi tự do: h = v0 * t + 0.5 * g * t^2
    eq = Eq(v0 * t + 0.5 * g * t**2, h)
    
    # Giải phương trình để tìm t
    t_sol = solve(eq)
    t_pos = [sol.evalf() for sol in t_sol if sol.evalf() > 0][0]  # Lấy nghiệm dương
    
    # Tính vận tốc lúc chạm đất: v = v0 + g * t
    v_cham_dat = v0 + g * t_pos
    
    solution = f"""
    <p><strong>Đáp án:</strong></p>
    <p><strong>a. Sau bao lâu vật chạm đất.</strong></p>
    <ul>
        <li>Độ cao thả vật: h = {h} m</li>
        <li>Vận tốc ban đầu: v<sub>0</sub> = {v0} m/s</li>
        <li>Gia tốc trọng trường: g = {g} m/s<sup>2</sup></li>
        <li>Phương trình quãng đường: h = v<sub>0</sub> * t + 0.5 * g * t<sup>2</sup></li>
        <li>Giải phương trình: {v0} * t + 0.5 * {g} * t<sup>2</sup> = {h}</li>
        <li>Thời gian t = {t_pos:.2f} giây</li>
    </ul>
    <p><strong>b. Tính vận tốc của vật lúc vừa chạm đất.</strong></p>
    <ul>
        <li>Vận tốc lúc chạm đất: v = v<sub>0</sub> + g * t</li>
        <li>v = {v0} + {g} * {t_pos:.2f} = {v_cham_dat:.2f} m/s</li>
    </ul>
    """
    
    solution = solution.replace(".", ",")
    return solution


# Các thành phần để tạo câu hỏi đa dạng
objects_4 = ["một vật", "một hòn đá", "một quả bóng", "một chiếc máy bay giấy", "một món đồ chơi"]
actions_4 = ["thả vật rơi tự do", "để vật rơi tự do", "thả vật từ trên cao", "để vật rơi từ trên cao"]

def generate_problem_type4():
    # Chọn ngẫu nhiên thành phần trong câu hỏi
    obj = random.choice(objects_4)
    action = random.choice(actions_4)
    v = random.randint(20, 50)  # m/s, vận tốc khi chạm đất ngẫu nhiên trong khoảng 20-50 m/s
    g = 9.8  # m/s², gia tốc trọng trường ngẫu nhiên trong khoảng 8-12 m/s²

    problem = f"""
    <p><strong>Một người {action}, {obj} chạm đất có v = {v} m/s, g = {g} m/s<sup>2</sup>.</strong></p>
    <p><strong>a. Tìm độ cao thả vật.</strong></p>
    <p><strong>b. Vận tốc vật khi rơi được 15 m.</strong></p>
    <p><strong>c. Độ cao của vật sau khi đi được 2,5 s.</strong></p>
    """
    
    return problem, v, g

def calculate_solution_type4(v, g):
    # Biến số
    h = symbols('h')
    v_new = symbols('v_new')

    # a. Tìm độ cao thả vật
    # Sử dụng công thức: v^2 = 2gh
    eq1 = Eq(v**2, 2 * g * h)
    h_sol = solve(eq1)[0]

    # b. Vận tốc vật khi rơi được 15 m
    h_r = 15  # m
    # Sử dụng công thức: v_new^2 = 2gh_r
    eq2 = Eq(v_new**2, 2 * g * h_r)
    v_new_sol = solve(eq2)[0]

    # c. Độ cao của vật sau khi đi được 2,5s
    t_r = 2.5  # s
    # Sử dụng công thức: h_new = 0.5 * g * t_r^2
    h_new_sol = 0.5 * g * t_r**2

    solution = f"""
    <p><strong>Đáp án:</strong></p>
    <p><strong>a. Tìm độ cao thả vật.</strong></p>
    <ul>
        <li>Vận tốc lúc chạm đất: v = {v} m/s</li>
        <li>Gia tốc trọng trường: g = {g} m/s<sup>2</sup></li>
        <li>Công thức: v<sup>2</sup> = 2gh</li>
        <li>Giải phương trình: {v}<sup>2</sup> = 2 * {g} * h</li>
        <li>Độ cao thả vật: h = {h_sol:.2f} m</li>
    </ul>
    <p><strong>b. Vận tốc vật khi rơi được 15 m.</strong></p>
    <ul>
        <li>Quãng đường rơi: h_r = 15 m</li>
        <li>Gia tốc trọng trường: g = {g} m/s<sup>2</sup></li>
        <li>Công thức: v<sub>new</sub><sup>2</sup> = 2gh<sub>r</sub></li>
        <li>Giải phương trình: v<sub>new</sub><sup>2</sup> = 2 * {g} * {h_r}</li>
        <li>Vận tốc vật khi rơi được 15 m: v<sub>new</sub> = {v_new_sol:.2f} m/s</li>
    </ul>
    <p><strong>c. Độ cao của vật sau khi đi được 2,5 s.</strong></p>
    <ul>
        <li>Thời gian rơi: t<sub>r</sub> = 2,5 s</li>
        <li>Gia tốc trọng trường: g = {g} m/s<sup>2</sup></li>
        <li>Công thức: h<sub>new</sub> = 0.5 * g * t<sub>r</sub><sup>2</sup></li>
        <li>Độ cao của vật sau khi đi được 2,5 s: h<sub>new</sub> = {h_new_sol:.2f} m</li>
    </ul>
    """
    
    solution = solution.replace(".", ",")
    return solution


objects_5 = ["một vật", "một hòn đá", "một quả bóng", "một chiếc máy bay giấy", "một món đồ chơi"]
locations = ["tại một địa điểm", "ở một vị trí", "ở một nơi"]

def generate_problem_type5():
    # Chọn ngẫu nhiên thành phần trong câu hỏi
    obj = random.choice(objects_5)
    loc = random.choice(locations)
    g = 9.8  # m/s², gia tốc trọng trường ngẫu nhiên trong khoảng 8-12 m/s²
    t = random.randint(4, 6)   # thời gian ngẫu nhiên từ 4-6 giây

    problem = f"""
    <p><strong>{obj.capitalize()} rơi tự do {loc} có g = {g} m/s<sup>2</sup>.</strong></p>
    <p><strong>a. Tính quãng đường vật rơi được trong {t}s đầu tiên.</strong></p>
    <p><strong>b. Tính quãng đường vật rơi trong giây thứ {t-1} và giây thứ {t}.</strong></p>
    """
    
    return problem, g, t

def calculate_solution_type5(g, t):
    # a. Quãng đường vật rơi được trong t giây đầu tiên
    # Sử dụng công thức: S = 0.5 * g * t^2
    S = 0.5 * g * t**2

    # b. Quãng đường vật rơi trong giây thứ (t-1) và giây thứ t
    t1 = t - 1
    S1 = 0.5 * g * t1**2  # Quãng đường rơi trong (t-1) giây
    S2 = 0.5 * g * t**2  # Quãng đường rơi trong t giây
    S_t1 = S2 - S1  # Quãng đường rơi trong giây thứ t
    S_t2 = 0.5 * g * (t**2 - (t1**2))  # Quãng đường rơi trong giây thứ t2 = S_t1

    solution = f"""
    <p><strong>Đáp án:</strong></p>
    <p><strong>a. Tính quãng đường vật rơi được trong {t}s đầu tiên.</strong></p>
    <ul>
        <li>Gia tốc trọng trường: g = {g} m/s<sup>2</sup></li>
        <li>Thời gian: t = {t} s</li>
        <li>Công thức: S = 0,5 * g * t<sup>2</sup></li>
        <li>Quãng đường rơi trong {t}s đầu tiên: S = 0,5 * {g} * {t}<sup>2</sup> = {S:.2f} m</li>
    </ul>
    <p><strong>b. Tính quãng đường vật rơi trong giây thứ {t-1} và giây thứ {t}.</strong></p>
    <ul>
        <li>Quãng đường rơi trong giây thứ {t-1}:</li>
        <li>Thời gian: t1 = {t-1} s</li>
        <li>Quãng đường rơi trong {t-1} giây: S1 = 0,5 * {g} * ({t-1})<sup>2</sup> = {S1:.2f} m</li>
        <li>Quãng đường rơi trong {t} giây: S2 = 0,5 * {g} * {t}<sup>2</sup> = {S2:.2f} m</li>
        <li>Quãng đường rơi trong giây thứ {t}: S_t1 = S2 - S1 = {S_t1:.2f} m</li>
        <li>Quãng đường rơi trong giây thứ {t} = 0,5 * {g} * ({t}<sup>2</sup> - ({t-1})<sup>2</sup>) = {S_t2:.2f} m</li>
    </ul>
    """
    
    solution = solution.replace(".", ",")
    return solution



# Hàm chính để tạo đề bài và giải pháp
def generate_problem_and_solution_3():
    problem_generators = [calculate_solution_type5, generate_problem_type4, generate_problem_type2, generate_problem_type3]
    solution_generators = [calculate_solution_type5,calculate_solution_type4, calculate_solution_type2, calculate_solution_type3]

    # Chọn ngẫu nhiên một mô típ
    idx = random.randint(0, len(problem_generators) - 1)
    
    problem_generator = problem_generators[idx]
    solution_generator = solution_generators[idx]

    # Tạo đề bài và các thông số liên quan
    problem, *params = problem_generator()
    
    # Tính giải pháp
    solution = solution_generator(*params)

    return problem, solution

# Tạo đề bài mới và tính đáp án
problem, solution = generate_problem_and_solution_3()


