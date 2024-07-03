import random
from sympy import symbols, Eq, solve
import math
# Danh sách vật thể và các cách diễn đạt khác nhau
objects = ["tàu", "xe", "người", "máy bay", "tàu vũ trụ"]
descriptions = ["đang chuyển động", "đang di chuyển", "đang tiến tới", "đang lao nhanh", "đang chạy"]
brake_actions = ["hãm phanh", "giảm tốc", "đạp phanh", "phanh gấp"]
objects_2 = ["tàu", "xe", "xe đạp", "xe gắn máy", "xe ô tô"]
mountain = ["đường đồi", "dốc núi", "dốc", "đường đèo"]
danger = ["bị mất phanh", "bị đứt phanh", "phanh có vấn đề", "phanh bị trục trặc", "bị trục trặc về phanh"]
duo = ["nên", "vì thế", "nên là", "vì thế nên là", "do đó"]

def generate_problem_type1():
    obj = random.choice(objects)
    desc = random.choice(descriptions)
    brake = random.choice(brake_actions)

    v0 = random.randint(40, 100) * 1.0  # km/h
    v1 = random.randint(20, int(v0 - 10)) * 1.0  # km/h
    time1 = random.randint(5, 20)  # giây
    a = (v1 - v0) / (time1 * 1000 / 3600)  # m/s^2
    a = round(a, 2)  # làm tròn gia tốc
    v = random.randint(10, int(v1 - 10)) * 1.0  # km/h

    problem = f"""
    <p><strong>Một {obj} {desc} với v<sub>0</sub> = {v0} km/h thì {brake} chuyển động chậm dần đều, sau {time1} giây đạt v<sub>1</sub> = {v1} km/h.</strong></p>
    <p><strong>a) Sau bao lâu kể từ lúc {brake} thì {obj} đạt v = {v} km/h và sau bao lâu thì dừng hẳn.</strong></p>
    <p><strong>b) Tính quãng đường {obj} đi được cho đến lúc dừng lại.</strong></p>
    """

    return problem, v0, v1, time1, a, v, obj, brake, desc

def calculate_solution_type1(v0, v1, time1, a, v, obj, brake, desc):
    t = symbols('t')
    eq1 = Eq(v0 * 1000 / 3600 + a * t, v * 1000 / 3600)
    t2 = solve(eq1)[0]
    t2 = max(t2.evalf(), 0)  # đảm bảo thời gian không âm

    eq2 = Eq(v0 * 1000 / 3600 + a * t, 0)
    t_stop = solve(eq2)[0]
    t_stop = max(t_stop.evalf(), 0)  # đảm bảo thời gian không âm

    s = (v0 * 1000 / 3600 * t_stop + 0.5 * a * t_stop**2) / 1000  # đổi sang km
    s = round(s, 2)  # làm tròn quãng đường

    t2_hours = t2 * 3600
    t_stop_hours = t_stop * 3600

    solution = f"""
    <p><strong>Đáp án:</strong></p>
    <p><strong>a) Sau bao lâu kể từ lúc {brake} thì {obj} đạt v = {v} km/h và sau bao lâu thì dừng hẳn.</strong></p>
    <ul>
        <li>Tốc độ ban đầu v<sub>0</sub> = {v0} km/h = {v0 * 1000 / 3600:.2f} m/s</li>
        <li>Tốc độ sau {time1} giây v<sub>1</sub> = {v1} km/h = {v1 * 1000 / 3600:.2f} m/s</li>
        <li>Gia tốc a = \\( \\frac{{v_1 - v_0}}{{t}} = \\frac{{{v1 * 1000 / 3600:.2f} - {v0 * 1000 / 3600:.2f}}}{{{time1}}} = {a:.2f} \\; \\text{{m/s}}^2 \\)</li>
        <li>Thời gian để đạt v = {v} km/h:</li>
        <ul>
            <li>Giải phương trình \\( v_0 + a \\cdot t_2 = v \\) để tìm \( t_2 \):</li>
            <li>\\( {v0 * 1000 / 3600:.2f} + {a:.2f} \\cdot t_2 = {v * 1000 / 3600:.2f} \\)</li>
            <li>\\( t_2 = \\frac{{{v * 1000 / 3600:.2f} - {v0 * 1000 / 3600:.2f}}}{{{a:.2f}}} \\) giây = {t2:.2f} giây = {t2_hours:.2f} giờ</li>
        </ul>
        <li>Thời gian để dừng hẳn:</li>
        <ul>
            <li>Giải phương trình \\( v_0 + a \\cdot t_\\text{{stop}} = 0 \\) để tìm \( t_\\text{{stop}} \):</li>
            <li>\\( {v0 * 1000 / 3600:.2f} + {a:.2f} \\cdot t_\\text{{stop}} = 0 \\)</li>
            <li>\\( t_\\text{{stop}} = \\frac{{-{v0 * 1000 / 3600:.2f}}}{{{a:.2f}}} \\) giây = {t_stop:.2f} giây = {t_stop_hours:.2f} giờ</li>
        </ul>
    </ul>
    <p><strong>b) Tính quãng đường {obj} đi được cho đến lúc dừng lại.</strong></p>
    <ul>
        <li>Quãng đường \\( S = v_0 \\cdot t_\\text{{stop}} + \\frac{{1}}{{2}} \\cdot a \\cdot t_\\text{{stop}}^2 \\)</li>
        <li>\\( S = ({v0 * 1000 / 3600:.2f} \\cdot {t_stop:.2f}) + \\frac{{1}}{{2}} \\cdot {a:.2f} \\cdot ({t_stop:.2f})^2 = {s:.2f} \\; \\text{{km}} \\)</li>
    </ul>
    """

    solution = solution.replace(".", ",").replace("\\cdot", " . ")
    return solution

def generate_problem_type2():
    obj = random.choice(objects_2)
    desc = random.choice(descriptions)
    mount = random.choice(mountain)
    dan = random.choice(danger)
    dou_1 = random.choice(duo)
    v0 = random.randint(20, 80) * 1.0  # km/h
    a = random.uniform(0.1, 1.0)  # m/s^2
    a = round(a, 2)  # làm tròn gia tốc
    s = random.randint(500, 2000)  # m

    problem = f"""
    <p><strong>Khi {desc} với vận tốc {v0} km/h thì {obj} bắt đầu chạy xuống {mount}. Nhưng do {dan} {dou_1} {obj} chuyển động thẳng nhanh dần đều với gia tốc {a} m/s<sup>2</sup> xuống hết {mount} có độ dài {s} m.</strong></p>
    <p><strong>Khoảng thời gian {obj} chạy xuống hết đoạn {mount} là bao nhiêu?</strong></p>
    """

    return problem, v0, a, s

def calculate_solution_type2(v0, a, s):
    v0_ms = v0 * 1000 / 3600  # đổi v0 sang m/s
    t = symbols('t')
    eq = Eq(v0_ms * t + 0.5 * a * t**2, s)
    t_solutions = solve(eq)
    
    # Lấy nghiệm dương
    t_sol = max(t.evalf() for t in t_solutions if t.evalf() > 0)

    t_hours = t_sol / 3600  # chuyển sang giờ

    solution = f"""
    <p><strong>Đáp án:</strong></p>
    <ul>
        <li>Vận tốc ban đầu v<sub>0</sub> = {v0} km/h = {v0_ms:.2f} m/s</li>
        <li>Gia tốc a = {a} m/s<sup>2</sup></li>
        <li>Quãng đường s = {s} m</li>
        <li>Giải phương trình \\( v_0 t + \\frac{{1}}{{2}} a t^2 = s \\) để tìm t:</li>
        <li>\\( {v0_ms:.2f} t + \\frac{{1}}{{2}} {a} t^2 = {s} \\)</li>
        <li>t = {t_sol:.2f} giây = {t_hours:.2f} giờ</li>
    </ul>
    """

    solution = solution.replace(".", ",").replace("\\cdot", " . ")
    return solution

# Mô típ thứ 3
def generate_problem_type3():
    v0 = 3  # m/s
    a = -2  # m/s^2, chậm dần đều nên gia tốc âm
    problem = f"""
    <p><strong>Một vật chuyển động thẳng chậm dần đều với tốc độ ban đầu {v0} m/s và gia tốc có độ lớn {abs(a)} m/s<sup>2</sup>. Biết thời điểm ban đầu vật ở gốc tọa độ và chuyển động ngược chiều dương của trục tọa độ.</strong></p>
    <p><strong>Viết phương trình chuyển động của vật.</strong></p>
    """
    return problem, v0, a

def calculate_solution_type3(v0, a):
    t = symbols('t')
    x = symbols('x')
    # Phương trình chuyển động: x = x0 + v0*t + 0.5*a*t^2
    x_eq = Eq(x, v0 * t + 0.5 * a * t**2)
    solution = f"""
    <p><strong>Đáp án:</strong></p>
    <ul>
        <li>Phương trình chuyển động của vật:</li>
        <li>x = {v0}t + 0,5({a}) . t<sup>2</sup></li>
        <li>= {v0}t + ({0.5 * a})t<sup>2</sup></li>
        <li>= {v0}t + ({0.5 * a:.1f})t<sup>2</sup></li>
    </ul>
    """
    solution = solution.replace(".", ",").replace("\\cdot", " . ")
    return solution

# Hàm chính để tạo đề bài và giải pháp
def generate_problem_and_solution():
    problem_generators = [generate_problem_type1, generate_problem_type2, generate_problem_type3]
    solution_generators = [calculate_solution_type1, calculate_solution_type2, calculate_solution_type3]

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
problem, solution = generate_problem_and_solution()


