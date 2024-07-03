import random
import math

def generate_problem_type2():
    angle = random.choice([15, 30, 45, 60, 75])  # Chọn góc ném ngẫu nhiên
    initial_velocity = random.randint(10, 50)  # Vận tốc ban đầu từ 10 đến 50 m/s
    gravity = random.choice([9.8, 10])  # Gia tốc trọng trường (m/s²)
    initial_height = random.randint(0, 10)  # Độ cao ban đầu từ 0 đến 10 m
    
    problem = f"""
    <p><strong>Một vật được ném xiên từ độ cao {initial_height} m với góc {angle}° và vận tốc ban đầu là {initial_velocity} m/s. 
    Lấy gia tốc trọng trường g = {gravity} m/s². Hãy viết phương trình chuyển động của vật và tính độ cao tối đa mà vật có thể đạt được.</strong></p>
    """
    
    return problem, angle, initial_velocity, gravity, initial_height

def calculate_solution_type2(angle, initial_velocity, gravity, initial_height):
    angle_rad = math.radians(angle)  # Chuyển đổi góc sang radian
    
    # Tính các thành phần vận tốc theo trục x và y
    vx0 = initial_velocity * math.cos(angle_rad)
    vy0 = initial_velocity * math.sin(angle_rad)
    
    # Phương trình chuyển động của vật
    x_t = f"x(t) = {vx0:.2f}t"
    y_t = f"y(t) = {initial_height} + {vy0:.2f}t - 0,5 \\cdot {gravity} \\cdot t^2"
    
    # Tính thời gian đạt độ cao tối đa
    t_max_height = vy0 / gravity
    
    # Tính độ cao tối đa
    max_height = initial_height + vy0 * t_max_height - 0.5 * gravity * t_max_height**2
    
    solution = f"""
    <p><strong>Đáp án:</strong></p>
    <ul>
        <li>Chọn hệ quy chiếu Oxy như hình vẽ.</li>
        <li>Thời điểm ban đầu:
            <ul>
                <li>Chiếu lên trục ox có \\(x_0 = 0\\)</li>
                <li>\\(v_{{0x}} = v_0 \\cos \\alpha = {initial_velocity} \\cos {angle}° = {vx0:.2f} \\; (m/s)\\)</li>
                <li>Chiếu lên trục oy có \\(y_0 = {initial_height}\\)</li>
                <li>\\(v_{{0y}} = v_0 \\sin \\alpha = {initial_velocity} \\sin {angle}° = {vy0:.2f} \\; (m/s)\\)</li>
            </ul>
        </li>
        <li>Xét tại thời điểm t có:
            <ul>
                <li>\\(a_x = 0\\)</li>
                <li>\\(a_y = -g\\)</li>
            </ul>
        </li>
        <li>Chiếu lên trục ox có:
            <ul>
                <li>\\(v_x = {vx0:.2f}\\)</li>
                <li>\\(x = {vx0:.2f}t\\)</li>
            </ul>
        </li>
        <li>Chiếu lên trục oy có:
            <ul>
                <li>\\(v_y = {vy0:.2f} - {gravity}t\\)</li>
                <li>\\(y = {initial_height} + {vy0:.2f}t - 0,5 \\cdot {gravity} \\cdot t^2\\)</li>
            </ul>
        </li>
        <li>Vậy quỹ đạo của vật là một parabol: \\(y = x - \\frac{{x^2}}{{2 \\cdot \\frac{{v_{{0x}}^2}}{{g}}}}\\)</li>
        <li>Khi lên đến độ cao cực đại thì \\(v_y = 0\\):
            <ul>
                <li>\\({vy0:.2f} - {gravity}t = 0\\)</li>
                <li>\\(t = \\frac{{{vy0:.2f}}}{{{gravity}}} = {t_max_height:.2f} \\; (s)\\)</li>
            </ul>
        </li>
        <li>Độ cao cực đại:
            <ul>
                <li>\\(h_{{max}} = {initial_height} + {vy0:.2f} \\cdot {t_max_height:.2f} - 0,5 \\cdot {gravity} \\cdot ({t_max_height:.2f})^2 = {max_height:.2f} \\; (m)\\)</li>
            </ul>
        </li>
    </ul>
    """
    solution = solution.replace(".", ",").replace("\\cdot", " . ")
    return solution
    
# Ví dụ sinh bài toán và tính lời giải
problem, angle, initial_velocity, gravity, initial_height = generate_problem_type2()
solution = calculate_solution_type2(angle, initial_velocity, gravity, initial_height)

# Danh sách các đối tượng và ngữ cảnh
objects = ["một quả bóng", "một viên đá", "một chiếc phi tiêu", "một tên lửa nhỏ", "một quả cầu"]
contexts = [
    "từ một ngọn đồi cao",
    "từ một tòa nhà",
    "từ một vách đá",
    "từ một cây cầu",
    "từ một tháp cao"
]

def generate_problem_type3():
    obj = random.choice(objects)
    context = random.choice(contexts)
    height = random.randint(30, 50)  # Độ cao ban đầu từ 30 đến 50 m
    initial_velocity = random.randint(10, 30)  # Vận tốc ban đầu từ 10 đến 30 m/s
    angle = random.choice([30, 45, 60])  # Chọn góc ném 30, 45 hoặc 60 độ
    gravity = random.choice([9.8, 10, 10.5])  # Chọn gia tốc trọng trường 9.8, 10 hoặc 10.5 m/s²
    
    problem = f"""
    <p><strong>{obj.capitalize()} được ném {context} ở độ cao h = {height} m với vận tốc ban đầu v<sub>0</sub> = {initial_velocity} m/s lên trên theo phương hợp với phương nằm ngang một góc {angle}°. 
    Lấy g = {gravity} m/s², bỏ qua lực cản của không khí. Hãy tính tầm bay xa của {obj} và vận tốc của {obj} khi chạm đất.</strong></p>
    """
    
    return problem, height, initial_velocity, angle, gravity, obj, context

def calculate_solution_type3(height, initial_velocity, angle, gravity, obj, context):
    angle_rad = math.radians(angle)  # Chuyển đổi góc sang radian
    
    # Tính các thành phần vận tốc theo trục x và y
    vx0 = initial_velocity * math.cos(angle_rad)
    vy0 = initial_velocity * math.sin(angle_rad)
    
    # Thời gian để vật đạt đến điểm cao nhất (chỉ phần lên trên)
    t_up = vy0 / gravity
    
    # Độ cao cực đại so với điểm ném
    max_height = vy0 * t_up - 0.5 * gravity * t_up**2
    
    # Tổng độ cao cực đại so với mặt đất
    total_max_height = height + max_height
    
    # Thời gian rơi từ độ cao cực đại xuống mặt đất
    t_down = math.sqrt(2 * total_max_height / gravity)
    
    # Tổng thời gian bay
    total_time = t_up + t_down
    
    # Tầm bay xa của vật (quãng đường theo trục x)
    range_x = vx0 * total_time
    
    # Vận tốc khi chạm đất (tính thành phần vận tốc tại thời điểm chạm đất)
    vy_final = vy0 - gravity * total_time
    final_velocity = math.sqrt(vx0**2 + vy_final**2)
    
    solution = f"""
    <p><strong>Đáp án:</strong></p>
    <ul>
        <li>Chọn hệ quy chiếu Oxy như hình vẽ.</li>
        <li>Thời điểm ban đầu:
            <ul>
                <li>Chiếu lên trục ox có \\(x_0 = 0\\)</li>
                <li>\\(v_{{0x}} = v_0 \\cos \\alpha = {initial_velocity} \\cos {angle}° = {vx0:.2f} \\; (m/s)\\)</li>
                <li>Chiếu lên trục oy có \\(y_0 = {height}\\)</li>
                <li>\\(v_{{0y}} = v_0 \\sin \\alpha = {initial_velocity} \\sin {angle}° = {vy0:.2f} \\; (m/s)\\)</li>
            </ul>
        </li>
        <li>Thời gian để {obj} đạt đến điểm cao nhất:
            <ul>
                <li>\\(t_{{up}} = \\frac{{v_{{0y}}}}{{g}} = \\frac{{{vy0:.2f}}}{{{gravity}}} = {t_up:.2f} \\; (s)\\)</li>
            </ul>
        </li>
        <li>Độ cao cực đại so với điểm ném:
            <ul>
                <li>\\(h_{{max}} = v_{{0y}} \\cdot t_{{up}} - 0,5 \\cdot g \\cdot t_{{up}}^2 = {vy0:.2f} \\cdot {t_up:.2f} - 0,5 \\cdot {gravity} \\cdot ({t_up:.2f})^2 = {max_height:.2f} \\; (m)\\)</li>
            </ul>
        </li>
        <li>Tổng độ cao cực đại so với mặt đất:
            <ul>
                <li>\\(H_{{max}} = h + h_{{max}} = {height} + {max_height:.2f} = {total_max_height:.2f} \\; (m)\\)</li>
            </ul>
        </li>
        <li>Thời gian rơi từ độ cao cực đại xuống mặt đất:
            <ul>
                <li>\\(t_{{down}} = \\sqrt{{\\frac{{2 \\cdot H_{{max}}}}{{g}}}} = \\sqrt{{\\frac{{2 \\cdot {total_max_height:.2f}}}{{{gravity}}}}} = {t_down:.2f} \\; (s)\\)</li>
            </ul>
        </li>
        <li>Tổng thời gian bay:
            <ul>
                <li>\\(T_{{total}} = t_{{up}} + t_{{down}} = {t_up:.2f} + {t_down:.2f} = {total_time:.2f} \\; (s)\\)</li>
            </ul>
        </li>
        <li>Tầm bay xa của {obj}:
            <ul>
                <li>\\(R = v_{{0x}} \\cdot T_{{total}} = {vx0:.2f} \\cdot {total_time:.2f} = {range_x:.2f} \\; (m)\\)</li>
            </ul>
        </li>
        <li>Vận tốc khi {obj} chạm đất:
            <ul>
                <li>Thành phần vận tốc theo trục x vẫn là \\(v_{{0x}} = {vx0:.2f} \\; (m/s)\\)</li>
                <li>Thành phần vận tốc theo trục y khi chạm đất là \\(v_{{y,final}} = v_{{0y}} - g \\cdot T_{{total}} = {vy0:.2f} - {gravity} \\cdot {total_time:.2f} = {vy_final:.2f} \\; (m/s)\\)</li>
                <li>Vận tốc khi chạm đất là \\(v_{{final}} = \\sqrt{{v_{{0x}}^2 + v_{{y,final}}^2}} = \\sqrt{{{vx0:.2f}^2 + {vy_final:.2f}^2}} = {final_velocity:.2f} \\; (m/s)\\)</li>
            </ul>
        </li>
    </ul>
    """
    solution = solution.replace(".", ",").replace("\\cdot", " . ")
    return solution
    
# Ví dụ sinh bài toán và tính lời giải
problem, height, initial_velocity, angle, gravity, obj, context = generate_problem_type3()
solution = calculate_solution_type3(height, initial_velocity, angle, gravity, obj, context)





recent_problem_indices = []

def generate_problem_and_solution_7():
    problem_generators = [generate_problem_type3, generate_problem_type2]
    solution_generators = [calculate_solution_type3, calculate_solution_type2]

    while True:
        idx = random.randint(0, len(problem_generators) - 1)
        if len(recent_problem_indices) < 3 or idx not in recent_problem_indices:
            break

    if len(recent_problem_indices) >= 3:
        recent_problem_indices.pop(0)
    recent_problem_indices.append(idx)
    
    problem_generator = problem_generators[idx]
    solution_generator = solution_generators[idx]

    problem, *params = problem_generator()
    solution = solution_generator(*params)

    return problem, solution

# Tạo đề bài mới và tính đáp án
problem, solution = generate_problem_and_solution_7()
print(problem, solution)
