def analyze_all_patterns(data):
    patterns = {}
    n = len(data)

    # Cầu 1-1: dạng T-X-T-X...
    if n >= 4:
        count_1_1 = sum(data[i] != data[i + 1] for i in range(n - 1))
        ratio_1_1 = count_1_1 / (n - 1)
        patterns['Cầu 1-1 (T-X luân phiên)'] = f"{ratio_1_1*100:.2f}% phù hợp"

    # Cầu 2-2: T-T-X-X...
    if n >= 6:
        count_2_2 = sum(data[i] == data[i + 1] and data[i + 2] == data[i + 3] and data[i] != data[i + 2] 
                        for i in range(0, n - 3, 2))
        total = (n - 3) // 2
        ratio_2_2 = count_2_2 / total if total > 0 else 0
        patterns['Cầu 2-2 (T-T-X-X)'] = f"{ratio_2_2*100:.2f}% phù hợp"

    # Cầu 3-1: T-T-T-X...
    if n >= 5:
        count_3_1 = sum(data[i] == data[i + 1] == data[i + 2] and data[i + 3] != data[i] 
                        for i in range(n - 3))
        patterns['Cầu 3-1 (3 giống, 1 khác)'] = f"{count_3_1} mẫu phù hợp"

    # Cầu 2-1: T-T-X...
    if n >= 4:
        count_2_1 = sum(data[i] == data[i + 1] and data[i + 2] != data[i] 
                        for i in range(n - 2))
        patterns['Cầu 2-1 (2 giống, 1 khác)'] = f"{count_2_1} mẫu phù hợp"

    # Cầu 1-2: T-X-X...
    if n >= 4:
        count_1_2 = sum(data[i] != data[i + 1] and data[i + 1] == data[i + 2] 
                        for i in range(n - 2))
        patterns['Cầu 1-2 (1 khác, 2 giống)'] = f"{count_1_2} mẫu phù hợp"

    # Cầu đôi (2 kết quả liên tiếp giống nhau):
    if n >= 4:
        count_doi = sum(data[i] == data[i+1] for i in range(n-1))
        patterns['Cầu đôi (T-T hoặc X-X)'] = f"{count_doi} cặp giống nhau"

    # Cầu đối xứng (mirror)
    if n >= 6:
        mirror_count = 0
        for i in range(n - 5):
            if data[i] == data[i+4] and data[i+1] == data[i+3]:
                mirror_count += 1
        patterns['Cầu đối xứng (T-X-X-T hoặc ngược lại)'] = f"{mirror_count} mẫu phù hợp"

    # Cầu 3-3 (3 T / 3 X luân phiên)
    if n >= 8:
        count_3_3 = sum(data[i] == data[i+1] == data[i+2] and data[i+3] == data[i+4] == data[i+5] and data[i] != data[i+3]
                        for i in range(n - 5))
        patterns['Cầu 3-3 (3 T / 3 X luân phiên)'] = f"{count_3_3} mẫu phù hợp"

    # Tỷ lệ Tài/Xỉu
    count_t = sum(data)
    count_x = n - count_t
    patterns['Tỷ lệ Tài/Xỉu'] = f"Tài: {count_t} ({count_t/n*100:.1f}%), Xỉu: {count_x} ({count_x/n*100:.1f}%)"

    return patterns
