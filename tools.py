from PIL import Image, ImageDraw
from crossword import Crossword


def new_grid(grid: [[]]) -> [[]]:
    left = len(grid[0])
    right = 0
    top = len(grid)
    down = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == -1:
                left = min(left, j)
                right = max(right, j)
                top = min(top, i)
                down = max(down, i)

    new_grid = []
    for i in range(top, down):
        new_grid.append(grid[i][left:right])

    return new_grid


def convert_image_to_grid(image_path, num_cols):
    image = Image.open(image_path).convert("L")
    width = image.width // num_cols
    num_rows = image.height // width
    height = width

    grid = []

    for row in range(num_rows):
        row_cells = []
        for col in range(num_cols):
            left = col * width
            upper = row * height
            right = left + width
            lower = upper + height

            cell = image.crop((left, upper, right, lower))
            avg_pixel = cell.point(lambda x: 255 if x < 128 else 0).convert("1")

            if avg_pixel.getbbox():
                row_cells.append(-1)  # 1 represents a black cell
            else:
                row_cells.append(0)  # 0 represents a white cell

        grid.append(row_cells)

    grid = new_grid(grid)
    return grid


def show_grid_image(grid, len_row_values, len_col_values):
    num_rows = len(grid)
    num_cols = len(grid[0])
    cell_size = 20
    line_color = "black"
    bold_line_width = 3

    width = num_cols * cell_size
    height = num_rows * cell_size

    grid_image = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(grid_image)

    # draw pixels and numbers
    for row in range(num_rows):
        for col in range(num_cols):
            left = col * cell_size
            upper = row * cell_size
            right = left + cell_size
            lower = upper + cell_size

            if grid[row][col] == -1:
                draw.rectangle(((left, upper), (right, lower)), fill="black")
            elif grid[row][col] > 0:
                draw.rectangle(((left, upper), (right, lower)), fill="white")
                text = str(grid[row][col])
                text_bbox = draw.textbbox((left, upper), text)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                text_position = ((left + right - text_width) // 2, (upper + lower - text_height) // 2)
                draw.text(text_position, text, fill="black")

    # draw lines
    for row in range(num_rows + 1):
        y = row * cell_size
        draw.line([(0, y), (width, y)], fill=line_color)

    for col in range(num_cols + 1):
        x = col * cell_size
        draw.line([(x, 0), (x, height)], fill=line_color)

    draw.line([(0, 0), (0, num_rows * cell_size)], fill=line_color, width=bold_line_width)
    draw.line([(0, 0), (num_cols * cell_size, 0)], fill=line_color, width=bold_line_width)
    draw.line([(num_cols * cell_size, num_rows * cell_size), (0, num_rows * cell_size)], fill=line_color,
              width=bold_line_width)
    draw.line([(num_cols * cell_size, num_rows * cell_size), (num_cols * cell_size, 0)], fill=line_color,
              width=bold_line_width)

    draw.line([(len_row_values * cell_size, 0), (len_row_values * cell_size, num_rows * cell_size)], fill=line_color,
              width=bold_line_width)
    draw.line([(0, len_col_values * cell_size), (num_cols * cell_size, len_col_values * cell_size)], fill=line_color,
              width=bold_line_width)

    return grid_image


def create_crossword_image(image_path: str, button_value: str):
    num_cols = 60
    grid = convert_image_to_grid(image_path, num_cols)
    cr = Crossword(grid)
    if button_value == "Preview image":
        return show_grid_image(cr.grid, 0, 0)
    if button_value == "Crossword":
        return show_grid_image(cr.crossword_grid, cr.len_row_values, cr.len_col_values)
    if button_value == "Crossword with image":
        return show_grid_image(cr.extended_grid, cr.len_row_values, cr.len_col_values)


