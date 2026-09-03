import copy
from tkinter import Button, Canvas, NORMAL, Tk
# import time  # No longer needed for sleeps

from convex_hull import compute_hull, compute_hull_steps

paused = False
step_iterator = None


def draw_point(canvas, x, y):
    r = 3  # radius of the dot
    canvas.create_oval(x - r, y - r, x + r, y + r, fill='blue', outline='blue')  # draw dot
    canvas.create_text(x + 10, y - 10, text=f"({x}, {y})", anchor="nw", font=("Arial", 8))  # coordinates


def add_point(event):
    draw_point(w, event.x, event.y)
    points.append((event.x, event.y))


def toggle_pause():
    global paused
    paused = not paused
    pause_button.config(text="Resume" if paused else "Pause")
    if not paused:
        master.after(100, process_step)  # Resume drawing steps


def process_step():
    global step_iterator

    if paused:
        return  # If paused, just stop processing steps

    try:
        step = next(step_iterator)
    except StopIteration:
        # Finished all steps
        submit_button.config(state=NORMAL)
        pause_button.config(state='disabled')
        return

    w.delete("all")

    # Draw all points
    for x, y in points:
        draw_point(w, x, y)

    if isinstance(step, dict):
        # Highlight tangent lines
        left = step["left"]
        right = step["right"]
        ul, ur = step["upper_tangent"]
        ll, lr = step["lower_tangent"]

        # Draw left hull in blue
        left_loop = left + [left[0]]
        for i in range(len(left_loop) - 1):
            x1, y1 = left_loop[i]
            x2, y2 = left_loop[i + 1]
            w.create_line(x1, y1, x2, y2, width=2, fill='blue')

        # Draw right hull in green
        right_loop = right + [right[0]]
        for i in range(len(right_loop) - 1):
            x1, y1 = right_loop[i]
            x2, y2 = right_loop[i + 1]
            w.create_line(x1, y1, x2, y2, width=2, fill='green')

        # Draw tangent lines in orange and purple
        w.create_line(ul[0], ul[1], ur[0], ur[1], width=3, fill='orange', dash=(4, 2))
        w.create_line(ll[0], ll[1], lr[0], lr[1], width=3, fill='purple', dash=(4, 2))

        # Label hull points
        for x, y in left:
            w.create_text(x + 10, y - 10, text=f"({x}, {y})", anchor="nw", font=("Arial", 8), fill='blue')
        for x, y in right:
            w.create_text(x + 10, y - 10, text=f"({x}, {y})", anchor="nw", font=("Arial", 8), fill='green')

    else:
        # Draw final merged hull in red
        hull = step + [step[0]]
        for i in range(len(hull) - 1):
            x1, y1 = hull[i]
            x2, y2 = hull[i + 1]
            w.create_line(x1, y1, x2, y2, width=2, fill='red')
        for x, y in step:
            w.create_text(x + 10, y - 10, text=f"({x}, {y})", anchor="nw", font=("Arial", 8), fill='red')

    w.update()

    # Schedule the next step after 700 ms
    master.after(700, process_step)


def draw_hull_steps():
    global step_iterator, paused
    if len(points) < 3:
        return  # Not enough points to compute hull

    step_iterator = iter(compute_hull_steps(points))
    paused = False
    pause_button.config(text="Pause", state='normal')
    submit_button.config(state='disabled')
    process_step()


if __name__ == '__main__':
    master, points = Tk(), []

    submit_button = Button(master, text="Draw Hull", command=draw_hull_steps)
    submit_button.pack()

    pause_button = Button(master, text="Pause", command=toggle_pause, state='disabled')
    pause_button.pack()

    quit_button = Button(master, text="Quit", command=master.quit)
    quit_button.pack()

    canvas_width = 1000
    canvas_height = 800
    w = Canvas(master, width=canvas_width, height=canvas_height, bg="white")
    w.pack()

    w.bind('<Button-1>', add_point)

    master.mainloop()
