import random
from sympy import symbols, Eq, solve

# Danh sách vật thể và các cách diễn đạt khác nhau
objects = ["tàu", "xe", "người", "máy bay", "tàu vũ trụ"]
descriptions = ["đang chuyển động", "đang di chuyển", "đang tiến tới", "đang di chuyển", "đang chạy"]
brake_actions = ["hãm phanh", "giảm tốc", "đạp phanh", "phanh gấp"]
objects_2 = ["tàu", "xe", "xe đạp", "xe gắn máy", "xe ô tô"]
mountain = ["đường đồi", "dốc núi", "dốc", "đường đèo"]
danger = ["bị mất phanh", "bị đứt phanh", "phanh có vấn đề", "phanh bị trục trặc", "bị trục trặc về phanh"]
duo = ["nên", "vì thế", "nên là", "vì thế nên là", "do đó"]

def generate_problem_type1():
    obj = random.choice(objects)
    desc = random.choice(descriptions)
    brake = random.choice(brake_actions)
    time_1 = random.randint(5, 12)
    time_2 = random.randint(1, 4)
    time_3 = time_1 - time_2
    v0 = random.randint(40, 100) * 1.0  # km/h
    v1 = random.randint(20, int(v0 - 10)) * 1.0  # km/h
    time1 = random.randint(5, 20)  # giây
    a = (v1 - v0) / (time1 * 1000 / 3600)  # m/s^2
    a = round(a, 2)  # làm tròn gia tốc
    v = random.randint(10, int(v1 - 10)) * 1.0  # km/h

    problem = f"""
    <p><strong>Một {obj} {desc} trong {time_1} giờ. {time_2} giờ {obj} di chuyển với vận tốc trung bình {v0} km/h. {time_3} giờ sau {obj} chạy với vận tốc trung bình {v1} km/h. Tính tốc độ trung bình của {obj} trong suốt thời gian chuyển động.</strong></p>
    """

    return problem, v0, v1, time_1, time_2, time_3, obj, desc

def calculate_solution_type1(v0, v1, time_1, time_2, time_3, obj, desc):
    # Tính quãng đường đi được trong từng khoảng thời gian
    s1 = v0 * time_2
    s2 = v1 * time_3
    
    # Tổng quãng đường và tổng thời gian
    total_distance = s1 + s2
    total_time = time_2 + time_3
    
    # Tính tốc độ trung bình
    avg_speed = total_distance / total_time

    solution = f"""
    <p><strong>Đáp án:</strong></p>
    <p><strong>Tốc độ trung bình của {obj} trong suốt thời gian chuyển động là {avg_speed:.2f} km/h.</strong></p>
    <ul>
        <li>Quãng đường đi được trong {time_2} giờ đầu: 
            \\( S_1 = v_0 \\cdot t_2 = {v0} \\cdot {time_2} = {s1} \\; \\text{{km}} \\)
        </li>
        <li>Quãng đường đi được trong {time_3} giờ sau: 
            \\( S_2 = v_1 \\cdot t_3 = {v1} \\cdot {time_3} = {s2} \\; \\text{{km}} \\)
        </li>
        <li>Tổng quãng đường: 
            \\( S = S_1 + S_2 = {s1} + {s2} = {total_distance} \\; \\text{{km}} \\)
        </li>
        <li>Tổng thời gian: 
            \\( T = t_2 + t_3 = {time_2} + {time_3} = {total_time} \\; \\text{{giờ}} \\)
        </li>
        <li>Tốc độ trung bình: 
            \\( v = \\frac{{S}}{{T}} = \\frac{{{total_distance}}}{{{total_time}}} = {avg_speed:.2f} \\; \\text{{km/h}} \\)
        </li>
    </ul>
    """
    solution = solution.replace(".", ",").replace("\\cdot", " . ")
    return solution
# Mô típ thứ 3

cars = ["xe hơi", "xe tải", "xe buýt", "taxi"]
bikes = ["xe tay ga", "xe máy", "xe đạp", "xe đạp điện"]


#Mô típ thứ 5 / bài toán vận tốc (hai xe gặp nhau tại một điểm)
def generate_problem_type5():
    random_cars = random.choice(cars)
    random_bikes = random.choice(bikes)
    # Generate random distances and times
    total_distance = random.randint(100,500)  # Tổng khoảng cách giữa A và B
    hour_car = random.randint(2, 3)  #Giờ ô tô
    minute_car = random.randint(10,59) # Phút
    hour_bike = random.randint(3, 4)   #Giờ xe máy
    minute_bike = random.randint(10,59) # Phút
    
    problem = f"""
    <p><strong>Hai tỉnh A và B cách nhau {total_distance} km. Cùng một lúc, một {random_cars} đi từ A đến B và một {random_bikes} đi từ B về A. Hai xe gặp nhau tại C. Từ C đến B, {random_cars} đi hết {hour_car} giờ {minute_car} phút, còn từ C về A, {random_bikes} đi hết {hour_bike} giờ {minute_bike} phút. Tính vận tốc mỗi xe, biết trên đường AB hai xe đều chạy với vận tốc không đổi.</strong></p>
    """
    return problem, total_distance, hour_car, hour_bike, minute_car, minute_bike, random_cars, random_bikes

def calculate_solution_type5(total_distance, hour_car, hour_bike, minute_car, minute_bike, random_cars, random_bikes):
    time_car = round((hour_car + minute_car * (1 / 60)), 2)
    time_bike = round((hour_bike + minute_bike * (1 / 60)), 2)
    time_bike_over_time_car = round((time_bike / time_car), 2)
    sqrt_time_bike_over_time_car = round((math.sqrt(time_bike_over_time_car)), 2)
    calc_y = round((180 / ((time_car * sqrt_time_bike_over_time_car) + time_bike)),2)
    calc_x = round(((total_distance - time_bike * calc_y) / time_car), 2)


    solution = f"""
    <p><strong>Đáp án:</strong></p>
    <ul>
        <li>Đổi sang giờ</li>
        <li>{random_cars}: {hour_car} giờ {minute_car} phút = {time_car} giờ</li>
        <li>{random_bikes}: {hour_bike} giờ {minute_bike} phút = {time_bike} giờ</li>
        <li>Gọi vận tốc của {random_cars} là x (km/h), vận tốc của {random_bikes} là y (km/h) | (x, y > 0).</li>
        <li>Từ C đến B {random_cars} đi hết {time_car} giờ nên đoạn đường BC là: {time_car}x km</li>
        <li>Từ C về A {random_bikes} đi hết {time_bike} giờ nên đoạn đường AC là: {time_bike}y km</li>
        <li>Quãng đường AB {total_distance} km bằng BC + AC:</li>
        <li>{time_car}x + {time_bike}y = {total_distance} km</li>
        <li>Thời gian {random_cars} đi từ A đến C là: \\(\\frac{{{time_car}x}}{{y}} \\)</li>
        <li>Thời gian {random_bikes} đi từ B đến C là: \\(\\frac{{{time_bike}y}}{{x}} \\)</li>
        <li>Do 2 xe khởi hành ngược chiều cùng lúc và gặp nhau tại C nên thời gian của hai xe đi đến C là bằng nhau:</li>
        <li>\\(\\frac{{{time_car}x}}{{y}} \\) = \\(\\frac{{{time_bike}y}}{{x}} \\)</li>
        <li>=> {time_bike}y<sup>2</sup> = {time_car}x h<sup>2</sup> (Do x, y > 0)</li>
        <li>=> {time_bike_over_time_car}y<sup>2</sup> = x<sup>2</sup></li>
        <li>=> x = {sqrt_time_bike_over_time_car}y</li>
        <li>Thay x = {sqrt_time_bike_over_time_car}y vào phương trình:{time_car}x + {time_bike}y = {total_distance} km</li>
        <li><strong>Ta được:</strong></li>
        <li>{round(time_car, 1)}\\cdot{sqrt_time_bike_over_time_car}y + {time_bike}y = {total_distance} km</li>
        <li>Giải phương trình:</li>
        <li>x ≈ {calc_x} km/h</li>
        <li>y ≈ {calc_y} km/h</li>
        <li>Vậy vận tốc của {random_cars} là xấp xỉ {calc_x} km/h và vận tốc của {random_bikes} là xấp xỉ {calc_y} km/h.</li>
    </ul>
    """
    solution = solution.replace(".", ",").replace("\\cdot", " . ")
    return solution

# Hàm chính để tạo đề bài và giải pháp
def generate_problem_and_solution_2():
    problem_generators = [generate_problem_type1,  generate_problem_type5]
    solution_generators = [calculate_solution_type1,calculate_solution_type5]

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
problem, solution = generate_problem_and_solution_2()


