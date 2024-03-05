import heapq
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import font
from PIL import Image, ImageTk
from collections import deque
import random
import time
from agorithm.A_star_10_12_nearest_first import *
from agorithm.bfs_in_AI1 import *
from agorithm.bfs_in_AI import *
from agorithm.dfs_in_AI import *
from agorithm.bfs_AI import *
from agorithm.dfs_AI import *
from agorithm.dfs_AI1 import *
result = None
dust_positon = None
table_frame = None  # Biến toàn cục để lưu trữ frame chứa bảng


def random_matrix (num_rows, num_cols,num_obs,num_dust):
    
    arr = [0 for i in range(num_rows*num_cols)]
    
    obs_position = random.sample(range(num_rows*num_cols),num_obs)
    for pos in obs_position:
        arr[pos] = 1        #1 đại diện cho vật cản
    
    empty_positions = [i for i, x in enumerate(arr) if x == 0]

    dust_and_vacuum_positions = random.sample(empty_positions, num_dust + 1)
    vacuum_position = dust_and_vacuum_positions.pop()  # Lấy vị trí cuối cùng cho máy hút bụi
    for pos in dust_and_vacuum_positions:
        arr[pos] = 2

    start_position = [vacuum_position // num_cols , vacuum_position % num_cols]
    # start_position = [3, 3]

    matrix = [arr[i * num_cols:(i + 1) * num_cols] for i in range(num_rows)]

    return {
        'matrix': matrix,
        'start_position': start_position
    }

def create_table():
    global num_cols,num_rows,num_obs,num_dust,table_frame,result,vacuum_pos,dust_positions, kt
    kt = 0
    num_rows = int(row_entry.get())
    num_cols = int(column_entry.get())
    num_obs = int(obstacle_entry.get())  # Số lượng vật cản
    num_dust = int(dust_entry.get())  # Số lượng bụi
    
    result = random_matrix(num_rows, num_cols, num_obs, num_dust)
    obstacle_positions = {(i, j) for i in range(num_rows) for j in range(num_cols) if result['matrix'][i][j] == 1}
    dust_positions = {(i, j) for i in range(num_rows) for j in range(num_cols) if result['matrix'][i][j] == 2}
    vacuum_pos = result['start_position']  # Vị trí của máy hút bụi
    #print("vi tri bat dau"+str(result['start_position']))
    if table_frame:
        clear_table()

    table_frame = tk.Frame(window)
    table_frame.grid(row=0, column=2, columnspan=2)

    global vacuum_image, bg_image, dust_image, wall_image, visited_image
    global size_image
    size_image = min(900 // num_rows, 1350 // num_cols)
    
    vacuum_image = ImageTk.PhotoImage(Image.open("image//vacuum.png").resize((size_image, size_image), Image.LANCZOS))
    bg_image = ImageTk.PhotoImage(Image.open("image//rac.png").resize((size_image, size_image), Image.LANCZOS))
    dust_image = ImageTk.PhotoImage(Image.open("image//virus.jpg").resize((size_image, size_image), Image.LANCZOS))
    wall_image = ImageTk.PhotoImage(Image.open("image//wall.jpg").resize((size_image, size_image), Image.LANCZOS))
    visited_image = ImageTk.PhotoImage(Image.open("image//rac.jpg").resize((size_image, size_image), Image.LANCZOS))
    
    for i in range(num_rows):
        for j in range(num_cols):
            if [i, j] == vacuum_pos:
                image = vacuum_image
            elif (i, j) in obstacle_positions:
                image = wall_image
            elif (i, j) in dust_positions:
                image = dust_image
            else:
                image = bg_image

            cell_label = tk.Label(table_frame, image=image, borderwidth=0.1, relief='groove', width=size_image, height=size_image, bg='lightblue')
            cell_label.image = image
            cell_label.grid(row=i, column=j, padx=1, pady=1)
            cell_label.bind('<Button-1>', lambda onRightClick, row=i, col=j: update_vacuum_position(row, col))
            cell_label.bind('<Button-2>', lambda onRightClick, row=i, col=j: up_wall(row, col))
            cell_label.bind('<Button-3>', lambda onRightClick, row=i, col=j: up_virus(row, col))
            
def update_cell(row, col, image):
    # Tìm widget Label tương ứng và cập nhật hình ảnh
    cell_label = table_frame.grid_slaves(row=row, column=col)[0]
    cell_label.config(image=image)
    cell_label.image = image


def up_wall(r, c):
    global table_frame
    result['matrix'][r][c] = 1
    new_label = tk.Label(table_frame, image=wall_image, borderwidth=0.1, relief='groove', width=size_image, height=size_image, bg='lightblue')
    # new_label.image = dust_image
    new_label.grid(row=r, column=c, padx=1, pady=1)
    
def up_virus(r, c):
    global table_frame, dust_image
    result['matrix'][r][c] = 2
    new_label = tk.Label(table_frame, image=dust_image, borderwidth=0.1, relief='groove', width=size_image, height=size_image, bg='lightblue')
    # new_label.image = dust_image
    new_label.grid(row=r, column=c, padx=1, pady=1)
    
def update_vacuum_position(new_row, new_col):
    global  result
    update_cell( result['start_position'][0], result['start_position'][1], bg_image)
    result['start_position'][0] = new_row
    result['start_position'][1] = new_col
    update_cell( result['start_position'][0], result['start_position'][1], vacuum_image)

def move_vacuum(old_x, old_y, new_x, new_y):
    global vacuum_pos
    # Cập nhật vị trí máy hút bụi mới
    # vacuum_pos[0] = new_x
    # vacuum_pos[1] = new_y
    vacuum_pos = (new_x, new_y)
    # Cập nhật giao diện người dùng
    update_cell(old_x, old_y, visited_image)  # Đặt lại ô cũ thành nền
    update_cell(new_x, new_y, vacuum_image)  # Đặt máy hút bụi vào ô mới
    
def clear_table(): 
    global table_frame
    # Kiểm tra nếu table_frame đã được tạo, sau đó xóa các widget trong Frame
    if table_frame:
        for widget in table_frame.winfo_children():
            if widget != submit_button:
                widget.destroy()
                
def clean_grid(aaa):
    global vacuum_pos, num_rows, num_cols, result, table_frame, kt
    kt = 1
    dust_positions = [(i, j) for i in range(num_rows) for j in range(num_cols) if result['matrix'][i][j] == 2]
    num_speed = max(num_rows, num_cols)
    num_speed = num_speed ** 1.3
    if(aaa == 1):
        # Vòng lặp qua từng điểm bụi
        for dust in dust_positions:
            # Tính toán đường đi bằng A*
            #start_pos_tuple = tuple(vacuum_pos.values())
            vacuum_pos = result['start_position']
            path = find_path_to_closest_goal(result['matrix'], (vacuum_pos[0], vacuum_pos[1])  , dust_positions)
            # Di chuyển qua từng bước trên đường đi
            for step in path:
                move_vacuum(vacuum_pos[0], vacuum_pos[1], step[0], step[1])
                window.update()
                time.sleep(2 / num_speed)
                if(kt == 0):
                    return None
            
            # Dọn bụi tại vị trí hiện tại
            result['matrix'][dust[0]][dust[1]] = 0
            update_cell(dust[0], dust[1], visited_image)
        # Cập nhật vị trí máy hút bụi cuối cùng
        vacuum_pos = {'x': path[-1][1], 'y': path[-1][0]}
    elif(aaa == 2 or aaa == 3):
        # Vòng lặp qua từng điểm bụi
        vacuum_pos = result['start_position']
        for dust in dust_positions:
            #start_pos_tuple = tuple(vacuum_pos.values())
            if(aaa == 2):
                path = initialize_bfs(result['matrix'], vacuum_pos  , dust)
            else:
                path = initialize_dfs1(result['matrix'], vacuum_pos  , dust)
            # Di chuyển qua từng bước trên đường đi
            for step in path:
                move_vacuum(vacuum_pos[0], vacuum_pos[1], step[0], step[1])
                window.update()
                time.sleep(2 / num_speed)
                if(kt == 0):
                    return None
            
            # Dọn bụi tại vị trí hiện tại
            result['matrix'][dust[0]][dust[1]] = 0
            update_cell(dust[0], dust[1], visited_image)
            # Cập nhật vị trí máy hút bụi cuối cùng
            vacuum_pos = (path[-1][0], path[-1][1])
            # vacuum_pos = {'x': path[-1][1], 'y': path[-1][0]}
    
    else:
        if(aaa == 4):
            path = initialize_B1(result["matrix"], result["start_position"])
        else:
            path = initialize_D(result["matrix"], result["start_position"])
        # Di chuyển qua từng bước trên đường đi
        for step in path:
            move_vacuum(vacuum_pos[0], vacuum_pos[1], step[0], step[1])
            window.update()
            time.sleep(0.7 / num_speed)
            if(kt == 0):
                return None
    
    
    
def start_cleaning_A_star():
    print("Start Cleaning A")
    # Bắt đầu quá trình dọn dẹp
    clean_grid(1)
    
def start_cleaning_bfs():
    print("Start Cleaning bfs")
    # Bắt đầu quá trình dọn dẹp
    clean_grid(2)
    
def start_cleaning_dfs():
    print("Start Cleaning dfs")
    # Bắt đầu quá trình dọn dẹp
    clean_grid(3)

def start_cleaning_b():
    print("Start Cleaning BFS full")
    # Bắt đầu quá trình dọn dẹp
    clean_grid(4)
    
def start_cleaning_d():
    print("Start Cleaning DFS full")
    # Bắt đầu quá trình dọn dẹp
    clean_grid(5)
    

def run_application():
    print("Start Application")
    global row_entry, column_entry, obstacle_entry, dust_entry, window, submit_button, kt
    kt = 0
    # Tạo một cửa sổ giao diện
    window = tk.Tk()
    window.title("Thông tin")

    
    window1 = tk.Frame(window)
    window1.grid(row=0, column=0, columnspan=2)
    # Tạo một LabelFrame với tiêu đề "Nhập thông tin"
    info_frame = tk.LabelFrame(window1, text="Nhập thông tin", font=("Arial", 12, "bold"), padx=20, pady=20)
    #info_frame.pack(pady=20)
    info_frame.grid(row=0, column=0, padx=20, pady=20)

    # Tạo các Label và Entry box
    label_font = font.Font(family="Arial", size=10)

    column_label = tk.Label(info_frame, text="Nhập số cột:", font=label_font)
    column_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    column_entry = tk.Entry(info_frame, font=label_font)
    column_entry.grid(row=0, column=1, padx=10, pady=5)

    row_label = tk.Label(info_frame, text="Nhập số hàng:", font=label_font)
    row_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    row_entry = tk.Entry(info_frame, font=label_font)
    row_entry.grid(row=1, column=1, padx=10, pady=5)

    obstacle_label = tk.Label(info_frame, text="Nhập số vật cản:", font=label_font)
    obstacle_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    obstacle_entry = tk.Entry(info_frame, font=label_font)
    obstacle_entry.grid(row=2, column=1, padx=10, pady=5)

    dust_row_label = tk.Label(info_frame, text="Nhập số bụi:", font=label_font)
    dust_row_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    dust_entry = tk.Entry(info_frame, font=label_font)
    dust_entry.grid(row=3, column=1, padx=10, pady=5)
    # Tạo nút "Submit"
    submit_button = tk.Button(window1, text="Submit", font=("Arial", 12), bg="#4CAF50", fg="white", relief=tk.RAISED,
                            command=create_table)
    #submit_button.pack(pady=10)
    submit_button.grid(row=6, column=0, columnspan=2, pady=10)

    start_cleaning_A_star_button = tk.Button(window1, text="Start Cleaning A*",command=start_cleaning_A_star)
    start_cleaning_A_star_button.grid(row=7, column=0, columnspan=2, pady=10)
    start_cleaning_bfs_button = tk.Button(window1, text="Start Cleaning bfs",command=start_cleaning_bfs)
    start_cleaning_bfs_button.grid(row=8, column=0, columnspan=2, pady=10)
    start_cleaning_dfs_button = tk.Button(window1, text="Start Cleaning dfs",command=start_cleaning_dfs)
    start_cleaning_dfs_button.grid(row=9, column=0, columnspan=2, pady=10)
    start_cleaning_b_button = tk.Button(window1, text="Start Cleaning BFS full",command=start_cleaning_b)
    start_cleaning_b_button.grid(row=10, column=0, columnspan=2, pady=10)
    start_cleaning_d_button = tk.Button(window1, text="Start Cleaning DFS full",command=start_cleaning_d)
    start_cleaning_d_button.grid(row=11, column=0, columnspan=2, pady=10)


    window.mainloop()

run_application()
