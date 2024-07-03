import random

# Danh sách mở rộng các từ đồng nghĩa và các đối tượng
synonyms_time = ["thời gian", "khoảng thời gian", "giai đoạn", "khoảng khắc", "thời điểm", "chu kỳ", "quãng thời gian", "phiên", "lúc", "đoạn", "kỳ", "khoảng", "thời khắc", "mùa", "chu trình", "phút giây", "giờ phút", "giây phút", "khung giờ", "quãng"]
synonyms_speed = ["tốc độ", "vận tốc", "tốc lực", "tốc độ di chuyển", "vận tốc chạy", "tốc lực hành trình", "tốc độ đi", "vận tốc hành trình", "nhanh độ", "vận tốc đi", "tốc hành", "tốc độ hành trình", "vận tốc nhanh", "tốc độ xe", "tốc lực xe", "tốc độ chạy", "vận tốc di chuyển", "tốc độ phương tiện", "tốc độ giao thông", "vận tốc xe"]
synonyms_car = ["ô tô", "xe hơi", "xe", "phương tiện", "xe cộ", "chiếc xe", "chiếc ô tô", "chiếc xe hơi", "xe bốn bánh", "xe chạy", "xe du lịch", "xe con", "xe vận tải", "xe lăn bánh", "xe gầm thấp", "xe di chuyển", "xe chở", "xe ngựa sắt", "xe xế hộp", "phương tiện giao thông"]
locations = [
    ("địa điểm A", "địa điểm B"), ("điểm X", "điểm Y"), ("nơi M", "nơi N"), 
    ("trạm P", "trạm Q"), ("cổng E", "cổng F"), ("bến T", "bến U"), 
    ("khu vực G", "khu vực H"), ("trung tâm K", "trung tâm L"), ("điểm xuất phát R", "điểm đích S"), 
    ("trạm dừng V", "trạm dừng W"), ("vị trí I", "vị trí J"), ("khu vực Z", "khu vực W"), 
    ("nơi đây", "nơi kia"), ("chỗ đứng P", "chỗ đứng Q"), ("trạm xe buýt M", "trạm xe buýt N"), 
    ("ga tàu hỏa H", "ga tàu hỏa I"), ("bãi đỗ xe B", "bãi đỗ xe C"), ("cổng ra vào E", "cổng ra vào F"), 
    ("vị trí khởi hành S", "vị trí đến D"), ("khu công nghiệp K", "khu công nghiệp L")
]

def random_ratios():
    ratio1 = random.uniform(0.1, 0.4)
    ratio2 = random.uniform(0.1, 0.4)
    ratio3 = 1 - ratio1 - ratio2
    if ratio3 <= 0:
        return random_ratios()  # Ensure valid ratios
    return ratio1, ratio2, ratio3

def generate_problem_type2():
    # Chọn ngẫu nhiên từ đồng nghĩa và địa điểm
    time_word = random.choice(synonyms_time)
    speed_word = random.choice(synonyms_speed)
    car_word = random.choice(synonyms_car)
    location = random.choice(locations)
    
    # Các giá trị ngẫu nhiên cho thời gian
    t = random.randint(60, 180)  # phút, từ 1 giờ đến 3 giờ
    
    # Các giá trị ngẫu nhiên cho tốc độ ở mỗi đoạn
    speed1 = random.randint(40, 80)  # km/h cho đoạn đầu
    speed2 = random.randint(40, 80)  # km/h cho đoạn tiếp theo
    speed3 = random.randint(70, 90)  # km/h cho đoạn còn lại
    
    # Chọn ngẫu nhiên tỉ lệ thời gian cho mỗi đoạn
    ratio1, ratio2, ratio3 = random_ratios()

    # Chuyển đổi tỉ lệ thành phần cụ thể
    part1 = f"{int(ratio1*100)}%"
    part2 = f"{int(ratio2*100)}%"
    part3 = f"{int(ratio3*100)}%"

    problem = f"""
    <p><strong>Một {car_word} chạy trên một đoạn đường thẳng từ {location[0]} đến {location[1]} phải mất một {time_word} {t} phút. 
    {speed_word} của {car_word} trong {part1} đầu của {time_word} này là {speed1} km/h, trong {part2} tiếp theo của {time_word} này là {speed2} km/h và trong {part3} còn lại là {speed3} km/h. 
    {speed_word} trung bình của {car_word} trên đoạn đường từ {location[0]} đến {location[1]} gần giá trị nào nhất sau đây?</strong></p>
    """

    return problem, t, speed1, speed2, speed3, ratio1, ratio2, ratio3

def calculate_solution_type2(t, speed1, speed2, speed3, ratio1, ratio2, ratio3):
    # Chuyển đổi thời gian từ phút sang giờ
    t_hours = t / 60.0

    # Tính thời gian cho từng đoạn
    t1 = t_hours * ratio1  # Thời gian đoạn đầu
    t2 = t_hours * ratio2  # Thời gian đoạn tiếp theo
    t3 = t_hours * ratio3  # Thời gian đoạn còn lại

    # Tính quãng đường từng đoạn
    d1 = speed1 * t1  # quãng đường đoạn đầu
    d2 = speed2 * t2  # quãng đường đoạn tiếp theo
    d3 = speed3 * t3  # quãng đường còn lại

    # Tổng quãng đường
    total_distance = d1 + d2 + d3

    # Tốc độ trung bình
    average_speed = total_distance / t_hours

    # Làm tròn tốc độ trung bình
    average_speed_rounded = round(average_speed, 2)

    solution = f"""
    <p><strong>Đáp án:</strong></p>
    <ul>
        <li>Tổng {synonyms_time[0]} \( t = {t} \) phút = {t_hours:.2f} giờ</li>
        <li>Thời gian {int(ratio1*100)}% đầu: \( t_1 = {ratio1:.2f} \\times t = {t1:.2f} \) giờ</li>
        <li>Thời gian {int(ratio2*100)}% tiếp theo: \( t_2 = {ratio2:.2f} \\times t = {t2:.2f} \) giờ</li>
        <li>Thời gian {int(ratio3*100)}% còn lại: \( t_3 = {ratio3:.2f} \\times t = {t3:.2f} \) giờ</li>
        <li>Quãng đường {int(ratio1*100)}% đầu: \( d_1 = {speed1} \\cdot t_1 = {speed1} \\cdot {t1:.2f} = {d1:.2f} \) km</li>
        <li>Quãng đường {int(ratio2*100)}% tiếp theo: \( d_2 = {speed2} \\cdot t_2 = {speed2} \\cdot {t2:.2f} = {d2:.2f} \) km</li>
        <li>Quãng đường {int(ratio3*100)}% còn lại: \( d_3 = {speed3} \\cdot t_3 = {speed3} \\cdot {t3:.2f} = {d3:.2f} \) km</li>
        <li>Tổng quãng đường: \( d = d_1 + d_2 + d_3 = {d1:.2f} + {d2:.2f} + {d3:.2f} = {total_distance:.2f} \) km</li>
        <li>Tốc độ trung bình: \( \\bar{{v}} = \\frac{{d}}{{t}} = \\frac{{{total_distance:.2f}}}{{{t_hours:.2f}}} = {average_speed_rounded} \) km/h</li>
    </ul>
    """

    solution = solution.replace(".", ",")
    return solution

# Tạo bài tập mẫu và lời giải
problem, t, speed1, speed2, speed3, ratio1, ratio2, ratio3 = generate_problem_type2()
solution = calculate_solution_type2(t, speed1, speed2, speed3, ratio1, ratio2, ratio3)




import random

# Danh sách từ đồng nghĩa
synonyms_distance_2 = [
    "quãng đường", "khoảng cách", "độ dài", "lộ trình", "khoảng cách di chuyển", "quãng đường di chuyển",
    "đoạn đường", "đường đi", "đường bay", "đường chim bay", "hành trình", "quãng hành trình", "lộ tuyến"
]
synonyms_time_2 = [
    "thời gian", "khoảng thời gian", "giai đoạn", "khoảng khắc", "thời điểm", "chu kỳ", "đoạn thời gian",
    "giờ giấc", "phút giây", "khoảnh khắc", "khoảng lúc", "lúc", "thời khắc"
]
synonyms_speed_2 = [
    "tốc độ", "vận tốc", "tốc lực", "tốc độ di chuyển", "vận tốc chạy", "tốc độ hành trình", "nhanh độ",
    "tốc lực hành trình", "tốc độ đi", "vận tốc hành trình", "tốc độ xe", "tốc độ chạy", "tốc lực xe", "tốc hành"
]
synonyms_train_2 = [
    "tàu", "con tàu", "xe lửa", "tàu hỏa", "tàu chạy", "tàu nhanh", "tàu tốc hành", "tàu vận tải", "tàu chở hàng",
    "tàu chở khách", "tàu đêm", "tàu sáng", "tàu điện", "tàu sắt"
]
synonyms_bird_2 = [
    "chim", "con chim", "chim bay", "chim nhỏ", "chim bay nhanh", "chim sẻ", "chim ưng", "chim bồ câu", "chim cắt",
    "chim đại bàng", "chim oanh", "chim yến", "chim họa mi", "cú mèo", "chim hải âu", "chim cánh cụt",
    "bướm", "con bướm", "chuồn chuồn", "con chuồn chuồn", "ong", "con ong", "dơi", "con dơi"
]
def generate_problem_type3_2():
    # Chọn ngẫu nhiên từ đồng nghĩa
    distance_word = random.choice(synonyms_distance_2)
    time_word = random.choice(synonyms_time_2)
    speed_word = random.choice(synonyms_speed_2)
    train_word = random.choice(synonyms_train_2)
    bird_word = random.choice(synonyms_bird_2)

    # Các giá trị ngẫu nhiên
    train_speed = random.randint(30, 50)  # km/h, trong khoảng từ 30 đến 50 km/h
    bird_speed = random.randint(50, 70)  # km/h, trong khoảng từ 50 đến 70 km/h
    initial_distance = random.randint(30, 50)  # km, trong khoảng từ 30 đến 50 km
    
    problem = f"""
    <p><strong>Hai {train_word} có cùng {speed_word} {train_speed} km/h, do lỗi kỹ thuật của trung tâm điều khiển nên chúng chuyển động trên cùng một đường ray theo hướng gặp nhau. 
    Một con {bird_word} có {speed_word} bay {bird_speed} km/h. Khi 2 {train_word} cách nhau {initial_distance} km thì con {bird_word} rời đầu {train_word} nọ để bay sang đầu {train_word} kia, 
    khi tới đầu {train_word} kia nó bay ngay trở lại đầu {train_word} nọ, và cứ tiếp tục như thế (dường như con {bird_word} muốn báo hiệu cho 2 người lái {train_word} biết điều nguy hiểm sắp xảy ra). 
    Hỏi đến khi 2 {train_word} va vào nhau thì con {bird_word} bay được {distance_word} là bao nhiêu?</strong></p>
    """
    
    return problem, train_speed, bird_speed, initial_distance

def calculate_solution_type3_2(train_speed, bird_speed, initial_distance):
    # Tính thời gian cho đến khi hai tàu gặp nhau
    time_until_collision = initial_distance / (2 * train_speed)  # giờ

    # Tính quãng đường chim bay
    bird_distance = bird_speed * time_until_collision  # km
    
    solution = f"""
    <p><strong>Đáp án:</strong></p>
    <ul>
        <li>Thời gian đến khi hai tàu gặp nhau: {time_until_collision:.2f} giờ</li>
        <li>Quãng đường con chim bay được: {bird_distance:.2f} km</li>
    </ul>
    """

    solution = solution.replace(".", ",")
    return solution

# Tạo bài toán và giải pháp
problem, train_speed_2, bird_speed_2, initial_distance_2 = generate_problem_type3_2()
solution = calculate_solution_type3_2(train_speed_2, bird_speed_2, initial_distance_2)


# Danh sách từ đồng nghĩa
synonyms_distance_3 = [
    "quãng đường", "khoảng cách", "độ dài", "lộ trình", "khoảng cách di chuyển", "quãng đường di chuyển",
    "đoạn đường", "đường đi", "khoảng cách đường thẳng", "đường di chuyển"
]
synonyms_time_3 = [
    "thời gian", "khoảng thời gian", "giai đoạn", "khoảnh khắc", "thời điểm", "chu kỳ", "đoạn thời gian",
    "giờ giấc", "phút giây", "khoảnh khắc", "khoảng lúc", "lúc", "thời khắc"
]
synonyms_speed_3 = [
    "tốc độ", "vận tốc", "tốc lực", "tốc độ di chuyển", "vận tốc chuyển động", "tốc độ hành trình", "nhanh độ",
    "tốc lực hành trình", "tốc độ đi", "vận tốc hành trình", "tốc độ chạy", "tốc lực xe", "tốc hành"
]
synonyms_object_3 = [
    "vật", "vật thể", "đối tượng", "hạt", "khối", "điểm", "mặt phẳng", "điểm sáng", "điểm di chuyển"
]
synonyms_points = [
    "A", "B", "C", "D", "E", "F"
]
synonyms_time_instances = [
    10, 12, 15, 20
]

# Danh sách ngữ cảnh ngẫu nhiên
contexts = [
    "Hai {object_word} bắt đầu di chuyển từ hai điểm {point_A} và {point_B} cách nhau {distance} m trên một đường thẳng và di chuyển về phía nhau.",
    "{object_word} tại {point_A} di chuyển về phía {point_B} và ngược lại. Khoảng cách giữa hai điểm là {distance} m.",
    "Xuất phát từ {point_A} và {point_B}, hai {object_word} di chuyển ngược chiều nhau trên quãng đường dài {distance} m."
]

def generate_problem_type4_2():
    # Chọn ngẫu nhiên từ đồng nghĩa và ngữ cảnh
    distance_word = random.choice(synonyms_distance_3)
    time_word = random.choice(synonyms_time_3)
    speed_word = random.choice(synonyms_speed_3)
    object_word = random.choice(synonyms_object_3)
    point_A = random.choice(synonyms_points)
    point_B = random.choice([p for p in synonyms_points if p != point_A])
    time_instance = random.choice(synonyms_time_instances)
    context = random.choice(contexts)

    # Các giá trị ngẫu nhiên
    distance = random.randint(50, 70)  # m, trong khoảng từ 50 đến 70 m
    time_to_meet = random.randint(3, 5)  # s, trong khoảng từ 3 đến 5 giây
    speed_ratio = random.randint(2, 3)  # tốc độ của vật từ A gấp 2 đến 3 lần tốc độ của vật từ B

    problem = f"""
    <p><strong>{context.format(object_word=object_word, point_A=point_A, point_B=point_B, distance=distance)}</strong></p>
    <p><strong>{speed_word.capitalize()} của {object_word} đi từ {point_A} gấp {speed_ratio} lần {speed_word} của {object_word} đi từ {point_B} và sau {time_to_meet} giây thì hai {object_word} gặp nhau.</strong></p>
    <p><strong>a. Viết phương trình chuyển động của hai {object_word}. Chọn {point_A} làm gốc tọa độ, chiều dương từ {point_A} đến {point_B}.</strong></p>
    <p><strong>b. Tìm biểu thức thể hiện sự phụ thuộc của {distance_word} giữa hai {object_word} theo {time_word}, từ đó tính {distance_word} giữa hai {object_word} tại thời điểm t = {time_instance} s.</strong></p>
    """
    
    return problem, distance, time_to_meet, speed_ratio, time_instance, point_A, point_B, object_word

def calculate_solution_type4_2(distance, time_to_meet, speed_ratio, time_instance, point_A, point_B, object_word):
    # Tính tốc độ của hai vật
    speed_B = round(distance / ((speed_ratio + 1) * time_to_meet), 2)  # m/s
    speed_A = round(speed_ratio * speed_B, 2)  # m/s

    # Phương trình chuyển động
    eq_A = f"x_{{{point_A}}} = {speed_A}t"
    eq_B = f"x_{{{point_B}}} = {distance} - {speed_B}t"
    
    # Tính khoảng cách giữa hai vật tại t = time_instance s
    t = time_instance  # s
    x_A_t = round(speed_A * t, 2)
    x_B_t = round(distance - speed_B * t, 2)
    distance_at_t = round(abs(x_B_t - x_A_t), 2)  # m

    # Giải chi tiết
    solution = f"""
    <p><strong>Đáp án chi tiết:</strong></p>
    <ol>
        <li><strong>Tính tốc độ của hai {object_word}:</strong></li>
        <ul>
            <li>Giả sử tốc độ của {object_word} đi từ {point_B} là v<sub>B</sub> (m/s).</li>
            <li>Tốc độ của {object_word} đi từ {point_A} là v<sub>A</sub> = {speed_ratio} * v<sub>B</sub> (m/s).</li>
            <li>Theo đề bài, hai {object_word} gặp nhau sau {time_to_meet} giây, do đó ta có phương trình: $$ {distance} = (v_{{A}} + v_{{B}}) * {time_to_meet} $$</li>
            <li>Thay v<sub>A</sub> = {speed_ratio} * v<sub>B</sub> vào phương trình: $$ {distance} = ({speed_ratio} * v_{{B}} + v_{{B}}) * {time_to_meet} $$</li>
            <li>Giải phương trình ta được: $$ v_{{B}} = \\frac{{{distance}}}{{({speed_ratio} + 1) * {time_to_meet}}} = {speed_B} \, {{m/s}} $$</li>
            <li>Và: $$ v_{{A}} = {speed_ratio} * v_{{B}} = {speed_ratio} * {speed_B} = {speed_A} \, {{m/s}} $$</li>
        </ul>
        <li><strong>Phương trình chuyển động của hai {object_word}:</strong></li>
        <ul>
            <li>Phương trình chuyển động của {object_word} đi từ {point_A}: $$ x_{{{point_A}}} = {speed_A} * t $$</li>
            <li>Phương trình chuyển động của {object_word} đi từ {point_B}: $$ x_{{{point_B}}} = {distance} - {speed_B} * t $$</li>
        </ul>
        <li><strong>Tính khoảng cách giữa hai {object_word} tại thời điểm t = {time_instance} giây:</strong></li>
        <ul>
            <li>Vị trí của {object_word} đi từ {point_A} tại t = {time_instance} giây: $$ x_{{{point_A}}}({time_instance}) = {speed_A} * {time_instance} = {x_A_t} \, {{m}} $$</li>
            <li>Vị trí của {object_word} đi từ {point_B} tại t = {time_instance} giây: $$ x_{{{point_B}}}({time_instance}) = {distance} - {speed_B} * {time_instance} = {x_B_t} \, {{m}} $$</li>
            <li>Khoảng cách giữa hai {object_word} tại t = {time_instance} giây: $$ |x_{{{point_B}}}({time_instance}) - x_{{{point_A}}}({time_instance})| = |{x_B_t} - {x_A_t}| = {distance_at_t} \, {{m}} $$</li>
        </ul>
    </ol>
    """

    return solution

# Tạo bài toán và giải pháp
problem, distance_2, time_to_meet_2, speed_ratio_2, time_instance_2, point_A_2, point_B_2, object_word_2 = generate_problem_type4_2()
solution = calculate_solution_type4_2(distance_2, time_to_meet_2, speed_ratio_2, time_instance_2, point_A_2, point_B_2, object_word_2)




def generate_problem_and_solution_5():
    problem_generators = [generate_problem_type3_2, generate_problem_type4_2, generate_problem_type2]
    solution_generators = [calculate_solution_type3_2, calculate_solution_type4_2, calculate_solution_type2]


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
problem, solution = generate_problem_and_solution_5()
