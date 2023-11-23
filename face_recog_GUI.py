import os
import tkinter as tk
from tkinter import ttk, messagebox

def convert_windows_path_to_unix(windows_path):
    unix_path = windows_path.replace("\\", "/")
    return unix_path

def run_script(script_path, method, args):
    try:
        module = __import__(script_path[:-3])  # Remove ".py" extension
        function_to_call = getattr(module, method)
        result = function_to_call(*args)
        return f"Success: {result}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def on_button_click(script_path, method, entries, run_status_var, buttons):
    user_inputs = [convert_windows_path_to_unix(entry.get()) for entry in entries]

    if not all(user_inputs):
        messagebox.showerror("Error", "Please enter all required details.")
        return

    result = run_script(script_path, method, user_inputs)
    show_popup("Running Anaconda !!", result)

    run_status_var.set(True)
    disable_buttons(buttons, script_path)

def show_popup(title, message):
    popup = tk.Toplevel()
    popup.title(title)

    label = tk.Label(popup, text=message)
    label.pack(padx=20, pady=10)

    ok_button = tk.Button(popup, text="OK", command=popup.destroy, width=10)
    ok_button.pack(pady=10)

def disable_buttons(buttons, active_script):
    for script_path, button, status_var in buttons:
        if script_path != active_script and not status_var.get():
            button["state"] = tk.DISABLED

def create_script_widget(script_path, script_label, method, parent, run_status_var, buttons, num_user_inputs, input_labels):
    frame = tk.Frame(parent, bd=2, relief=tk.RAISED)
    label = tk.Label(frame, text=script_label, font=('Arial', 12, 'bold'))
    label.pack(pady=5)

    entries = []
    for i in range(num_user_inputs):
        entry_label = tk.Label(frame, text=f"{input_labels[i]}:", font=('Arial', 10))
        entry_label.pack()

        entry = tk.Entry(frame, font=('Arial', 10), width=60)  # Adjusted width
        entry.pack()
        entries.append(entry)

    run_status_var = tk.BooleanVar()
    button = ttk.Button(frame, text=f"Run", command=lambda: on_button_click(script_path, method, entries, run_status_var, buttons))
    button.pack(pady=10)

    buttons.append((script_path, button, run_status_var))
    return frame

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Face Recognition")

    # Screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    script1_path = "Detect_face_frm_video_file_save_csv.py"
    script2_path = "detect_face_frm_webcam_save_csv.py"
    script3_path = "capture_img_frm_video.py"
    script4_path = "capture_img_frm_webCam.py"

    script1_widget = create_script_widget(script1_path, "   Detect Faces From A Video File  ", "recognize_faces_from_images_and_video", root, tk.BooleanVar(), [], 3, ["Enter Known Face(png or jpg only) Dir Path", "Enter video file path", "Enter path to store csv file"])
    script2_widget = create_script_widget(script2_path, "   Detect Faces From Webcam    ", "detect_faces_from_webcam", root, tk.BooleanVar(), [], 2, ["Known faces(png or jpg only) dir Path", "Enter path to store csv file"])
    script3_widget = create_script_widget(script3_path, "   Capture Image From Video    ", "capture_img_frm_video", root, tk.BooleanVar(), [], 3, ["Enter video file path", "Enter dir where images are to be saved", "Enter faces/images per second to save"])
    script4_widget = create_script_widget(script4_path, "   Capture Image From Webcam  ", "capture_image_from_webcam", root, tk.BooleanVar(), [], 2, ["Enter dir where images are to be saved", "Enter faces/images per second to save"])

    # Place widgets in the four corners
    script1_widget.grid(row=0, column=0, padx=20, pady=20, sticky=tk.W)
    script2_widget.grid(row=1, column=0, padx=20, pady=20, sticky=tk.E)
    script3_widget.grid(row=0, column=1, padx=20, pady=20, sticky=tk.W)
    script4_widget.grid(row=1, column=1, padx=20, pady=20, sticky=tk.E)

    root.mainloop()
