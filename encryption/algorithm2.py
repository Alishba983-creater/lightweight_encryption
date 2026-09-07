def generate_image_shuffling_pattern(x: float, r0: float, R: int, C: int) -> list:
    """
    Generates a shuffled index pattern using a chaotic sequence generator
    and a custom sorting/swapping procedure.
    """
    index = []
    k = []
    
    total_elements = R * C

    # 1. Generate chaotic map sequence k and initial index list
    for i in range(total_elements):
        x = ((r0 ** 2) * (x ** 2 - 5) * (1 - r0 * (x ** 2 - 5))) % 1
        k.append(x)
        index.append(i)

    # 2. Custom swapping loop based on conditions
    for i in range(total_elements - 1):
        for j in range(total_elements - 1):
            
            if (i + 1) % C == 0:
                if k[i] > k[j]:
                    if i + C != total_elements - 1:
                        k[i], k[i + C] = k[i + C], k[i]
                        index[i], index[i + C] = index[i + C], index[i]

            elif (j + 1) % C == 0:
                if k[i] > k[j]:
                    if (j + C) != total_elements - 1:
                        k[j], k[j + C] = k[j + C], k[j]
                        index[j], index[j + C] = index[j + C], index[j]

            elif i >= (R - 1) * C:
                if k[i] > k[j]:
                    if i + 1 != total_elements - 1:
                        k[i], k[i + 1] = k[i + 1], k[i]
                        index[i], index[i + 1] = index[i + 1], index[i]

            elif j >= (R - 1) * C:
                if k[i] > k[j]:
                    if j + 1 != total_elements - 1:
                        k[j], k[j + 1] = k[j + 1], k[j]
                        index[j], index[j + 1] = index[j + 1], index[j]

            else:
                if k[i] > k[j]:
                    k[i], k[j] = k[j], k[i]
                    index[i], index[j] = index[j], index[i]

    return index