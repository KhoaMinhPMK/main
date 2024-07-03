import random
import sympy as sp
import math

# Danh sách vật thể và các cách diễn đạt khác nhau
objects = ["tàu", "đoàn tàu", "chuyến tàu"]
descriptions = ["đang chuyển động", "đang di chuyển", "đang tiến tới", "đang lao nhanh", "đang chạy"]
initial_speeds = ["vận tốc ban đầu", "tốc độ ban đầu", "vận tốc ban đầu của tàu"]

def generate_problem_type1():
    obj = random.choice(objects)
    desc = random.choice(descriptions)
    initial_speed = random.choice(initial_speeds)
    
    a = random.uniform(1.0, 5.0)
    time1 = random.randint(5, 20)
    initial_v = random.uniform(10.0, 30.0)
    distance = random.randint(100, 500)
    cars_count = random.randint(5, 15)
    
    problem = f"""
    <p><strong>Một {obj} {desc} với gia tốc a = {a:.2f} m/s² và {initial_speed} là {initial_v:.2f} m/s. Người này nhìn thấy toa đầu tiên chạy qua trước mắt mình trong {time1} giây.</strong></p>
    <p><strong>Tính thời gian toa thứ {cars_count} chạy qua người này. Giả sử chuyển động của tàu hỏa là nhanh dần đều và xem khoảng cách giữa các toa tàu là {distance} mét.</strong></p>
    """
    
    return problem, a, time1, initial_v, distance, cars_count  # Return only the needed parameters

def calculate_solution_type1(a, time1, initial_v, distance, cars_count):
    t = sp.symbols('t')
    v1 = initial_v + a * time1
    d1 = (v1**2) / (2 * a)
    d8 = 8 * d1 + (cars_count - 1) * distance
    t8 = math.sqrt((2 * d8) / a)
    d9 = cars_count * d1 + (cars_count - 1) * distance
    t9 = math.sqrt((2 * d9) / a)
    t_9_pass = t9 - t8
    
    solution = f"""
    <p><strong>Đáp án:</strong></p>
    <ul>
        <li>Vận tốc của toa đầu tiên sau khi chạy qua người này: v<sub>1</sub> = {initial_v:.2f} + a &sdot; t = {initial_v:.2f} + {a:.2f} &sdot; {time1} = {v1:.2f} m/s</li>
        <li>Độ lớn của một toa: d<sub>1</sub> = \\(\\frac{{v_1^2}}{{2a}}\\) = \\(\\frac{{{v1:.2f}^2}}{{2 \\cdot {a:.2f}}}\\) = {d1:.2f} m</li>
        <li>Độ lớn của {cars_count} toa: d<sub>{cars_count}</sub> = {cars_count} &sdot; d<sub>1</sub> + {(cars_count - 1)} &sdot; {distance} = {cars_count} &sdot; {d1:.2f} + {(cars_count - 1)} &sdot; {distance} = {d9:.2f} m</li>
        <li>Thời gian 8 toa chạy qua người là: t<sub>8</sub> = \\(\\sqrt{{\\frac{{2 \\cdot d_8}}{{a}}}}\\) = \\(\\sqrt{{\\frac{{2 \\cdot {d8:.2f}}}{{{a:.2f}}}}}\\) ≈ {t8:.2f} s</li>
        <li>Thời gian {cars_count} toa chạy qua người này: t<sub>{cars_count}</sub> = \\(\\sqrt{{\\frac{{2 \\cdot d_{cars_count}}}{{a}}}}\\) = \\(\\sqrt{{\\frac{{2 \\cdot {d9:.2f}}}{{{a:.2f}}}}}\\) = {t9:.2f} s</li>
        <li>Thời gian toa thứ {cars_count} chạy qua người này: t<sub>{cars_count}</sub> - t<sub>8</sub> = {t9:.2f} - {t8:.2f} = {t_9_pass:.2f} s</li>
    </ul>
    """
    
    solution = solution.replace(",", ".")
    return solution

# Tạo bài tập và giải bài tập
problem, a, time1, initial_v, distance, cars_count = generate_problem_type1()
solution = calculate_solution_type1(a, time1, initial_v, distance, cars_count)


objects = ["xe ô tô", "chiếc xe", "ô tô"]
descriptions = ["đi đến điểm A thì tắt máy", "tới điểm A thì tắt máy", "đến điểm A rồi tắt máy"]

def generate_problem_type2():
    obj = random.choice(objects)
    desc = random.choice(descriptions)
    
    s_diff = random.randint(3, 6)  # Quãng đường AB dài hơn quãng đường BC trong 2 giây tiếp theo (m)
    total_time = random.randint(8, 12)  # Thời gian từ A đến khi xe dừng lại (giây)
    time_interval = random.randint(1, 3)  # Thời gian mỗi đoạn (giây)
    
    problem = f"""
    <p><strong>Một {obj} {desc}. {time_interval} giây đầu tiên khi đi qua A nó đi được quãng đường AB dài hơn quãng đường BC đi được trong {time_interval} giây tiếp theo {s_diff} mét. Biết rằng qua A được {total_time} giây thì ô tô mới dừng lại.</strong></p>
    <p><strong>Tính tốc độ ô tô tại A và quãng đường AD ô tô còn đi được sau khi tắt máy.</strong></p>
    """
    
    return problem, s_diff, total_time, time_interval

def calculate_solution_type2(s_diff, total_time, time_interval):
    v0, a = sp.symbols('v0 a')
    
    # Phương trình quãng đường đi được trong thời gian t với vận tốc ban đầu v0 và gia tốc a
    s_AB = v0 * time_interval + 0.5 * a * time_interval**2
    s_BC = (v0 + a * time_interval) * time_interval + 0.5 * a * time_interval**2
    
    # Điều kiện AB - BC = s_diff
    eq1 = sp.Eq(s_AB - s_BC, s_diff)
    
    # Điều kiện dừng lại sau total_time giây
    eq2 = sp.Eq(v0 + a * total_time, 0)
    
    # Giải hệ phương trình
    solutions = sp.solve((eq1, eq2), (v0, a))
    
    # Debugging: In phương trình và nghiệm tìm được
    print(f"Phương trình 1: {eq1}")
    print(f"Phương trình 2: {eq2}")
    print(f"Nghiệm tìm được: {solutions}")
    
    if solutions:
        v0_value = solutions[v0]
        a_value = solutions[a]
        
        # Quãng đường AD
        s_AD = v0_value * total_time + 0.5 * a_value * total_time**2
        
        solution_text = f"""
        <p><strong>Đáp án:</strong></p>
        <p><strong>Tính tốc độ ô tô tại A và quãng đường AD ô tô còn đi được sau khi tắt máy:</strong></p>
        <ul>
            <li>Gia tốc của xe: \(a = {a_value:.2f}\, m/s^2\)</li>
            <li>Tốc độ ô tô tại A: \(v_0 = {v0_value:.2f}\, m/s\)</li>
            <li>Quãng đường AD ô tô còn đi được sau khi tắt máy: \({s_AD} = {s_AD:.2f}\, m\)</li>
        </ul>
        <p><strong>Giải thích chi tiết:</strong></p>
        <p>Ta có quãng đường AB và BC lần lượt là:</p>
        <p>\[
        {s_AB} = v_0 \cdot {time_interval} + \\frac{{1}}{{2}} \cdot a \cdot {time_interval}^2
        \]</p>
        <p>\[
        {s_BC} = (v_0 + a \cdot {time_interval}) \cdot {time_interval} + \\frac{{1}}{{2}} \cdot a \cdot {time_interval}^2
        \]</p>
        <p>Theo đề bài, quãng đường AB dài hơn quãng đường BC là {s_diff} mét, ta có phương trình:</p>
        <p>\[
        {s_AB} - {s_BC} = {s_diff}
        \]</p>
        <p>Thay vào các biểu thức ta có phương trình:</p>
        <p>\[
        v_0 \cdot {time_interval} + \\frac{{1}}{{2}} \cdot a \cdot {time_interval}^2 - [(v_0 + a \cdot {time_interval}) \cdot {time_interval} + \\frac{{1}}{{2}} \cdot a \cdot {time_interval}^2] = {s_diff}
        \]</p>
        <p>Đơn giản phương trình trên ta có:</p>
        <p>\[
        -a \cdot {time_interval} = {s_diff}
        \]</p>
        <p>Giải phương trình trên ta được gia tốc \(a\):</p>
        <p>\[
        a = -\\frac{{{s_diff}}}{{{time_interval}}} = {a_value:.2f} \, m/s^2
        \]</p>
        <p>Với điều kiện ô tô dừng lại sau {total_time} giây, ta có phương trình:</p>
        <p>\[
        v_0 + a \cdot {total_time} = 0
        \]</p>
        <p>Giải phương trình trên ta được vận tốc ban đầu \(v_0\):</p>
        <p>\[
        v_0 = -a \cdot {total_time} = -({a_value:.2f}) \cdot {total_time} = {v0_value:.2f} \, m/s
        \]</p>
        <p>Cuối cùng, quãng đường AD mà ô tô còn đi được sau khi tắt máy là:</p>
        <p>\[
        {s_AD} = v_0 \cdot {total_time} + \\frac{{1}}{{2}} \cdot a \cdot {total_time}^2 = {v0_value:.2f} \cdot {total_time} + \\frac{{1}}{{2}} \cdot ({a_value:.2f}) \cdot {total_time}^2 = {s_AD:.2f} \, m
        \]</p>
        """
    else:
        solution_text = "<p><strong>Không tìm được nghiệm cho bài toán này.</strong></p>"
    
    return solution_text

# Tạo bài tập và giải bài tập
problem, s_diff, total_time, time_interval = generate_problem_type2()
solution = calculate_solution_type2(s_diff, total_time, time_interval)





def generate_problem_and_solution_6():
    problem_generators = [generate_problem_type1, generate_problem_type2]
    solution_generators = [calculate_solution_type1, calculate_solution_type2]

 
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
problem, solution = generate_problem_and_solution_6()
print(problem, solution)
