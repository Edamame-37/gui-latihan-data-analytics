import json
import customtkinter as ctk
from tkinter import messagebox
import os
from PIL import Image

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def make_table(data_list):
    if not data_list: 
        return "No Data"
    keys = list(data_list[0].keys())
    col_widths = {k: len(str(k)) for k in keys}
    for row in data_list:
        for k in keys:
            col_widths[k] = max(col_widths[k], len(str(row.get(k, ''))))
            
    header = " | ".join(str(k).ljust(col_widths[k]) for k in keys)
    sep = "-+-".join("-" * col_widths[k] for k in keys)
    
    rows = []
    for row in data_list:
        r = " | ".join(str(row.get(k, '')).ljust(col_widths[k]) for k in keys)
        rows.append(r)
        
    return f"{header}\n{sep}\n" + "\n".join(rows)

class SQLPracticeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Data Analytics - SQL Practice GUI")
        self.geometry("1100x750")
        
        self.q_file = "questions.json"
        if not os.path.exists(self.q_file):
            messagebox.showerror("Error", "questions.json tidak ditemukan. Jalankan generate_qa.py terlebih dahulu.")
            self.destroy()
            return
            
        with open(self.q_file, 'r', encoding='utf-8') as f:
            self.questions = json.load(f)
            
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.practice_frame = None
        self.dashboard_frame = DashboardFrame(self, self.questions, self.show_practice)
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")

    def show_dashboard(self):
        if self.practice_frame:
            self.practice_frame.grid_forget()
            self.practice_frame.destroy()
        
        self.dashboard_frame = DashboardFrame(self, self.questions, self.show_practice)
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")

    def show_practice(self, q_data):
        self.dashboard_frame.grid_forget()
        self.practice_frame = PracticeFrame(self, q_data, self.show_dashboard, self.save_progress)
        self.practice_frame.grid(row=0, column=0, sticky="nsew")
        
    def save_progress(self, q_id):
        for q in self.questions:
            if q["id"] == q_id:
                q["solved"] = True
                break
        with open(self.q_file, 'w', encoding='utf-8') as f:
            json.dump(self.questions, f, indent=4)


class DashboardFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, questions, on_click_callback):
        super().__init__(master)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        title = ctk.CTkLabel(self, text="Dashboard Latihan SQL (Bento UI)", font=ctk.CTkFont(size=28, weight="bold"))
        title.grid(row=0, column=0, columnspan=4, pady=(20, 30))
        
        colors = {
            "Easy": "#2ecc71",
            "Medium": "#f39c12",
            "Hard": "#e67e22",
            "Very Hard": "#e74c3c"
        }

        row = 1
        col = 0
        for q in questions:
            card = ctk.CTkFrame(self, corner_radius=15, fg_color="#2b2b2b", border_width=1, border_color="#555")
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            # Status icon
            status_text = "✅ Selesai" if q["solved"] else "❌ Belum"
            status_color = "#2ecc71" if q["solved"] else "#e74c3c"
            status_lbl = ctk.CTkLabel(card, text=status_text, text_color=status_color, font=ctk.CTkFont(size=16, weight="bold"))
            status_lbl.pack(pady=(15, 5))
            
            # Title
            t_lbl = ctk.CTkLabel(card, text=f"Q{q['id']}: {q['title']}", font=ctk.CTkFont(size=14, weight="bold"), wraplength=180)
            t_lbl.pack(pady=5, padx=10, fill="x")
            
            # Difficulty
            diff_lbl = ctk.CTkLabel(card, text=q['difficulty'], text_color=colors[q['difficulty']], font=ctk.CTkFont(size=12))
            diff_lbl.pack(pady=(0, 10))
            
            # Button
            btn = ctk.CTkButton(card, text="Mulai Kerjakan", corner_radius=8, command=lambda data=q: on_click_callback(data))
            btn.pack(pady=15)
            
            col += 1
            if col > 3:
                col = 0
                row += 1


class PracticeFrame(ctk.CTkFrame):
    def __init__(self, master, q_data, back_callback, save_callback):
        super().__init__(master)
        self.q_data = q_data
        self.back_callback = back_callback
        self.save_callback = save_callback
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        
        back_btn = ctk.CTkButton(header, text="⬅ Kembali", width=100, corner_radius=8, command=self.back_callback)
        back_btn.pack(side="left")
        
        title_lbl = ctk.CTkLabel(header, text=f"Q{q_data['id']}: {q_data['title']} ({q_data['difficulty']})", font=ctk.CTkFont(size=22, weight="bold"))
        title_lbl.pack(side="left", padx=20)
        
        # Left Panel (Info & ERD)
        left_panel = ctk.CTkFrame(self, corner_radius=10)
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=10)
        
        desc_lbl = ctk.CTkLabel(left_panel, text="Instruksi:", font=ctk.CTkFont(size=16, weight="bold"))
        desc_lbl.pack(anchor="w", padx=15, pady=(15, 0))
        
        desc_text = ctk.CTkTextbox(left_panel, height=80, wrap="word", corner_radius=8)
        desc_text.insert("0.0", q_data['description'])
        desc_text.configure(state="disabled")
        desc_text.pack(fill="x", padx=15, pady=5)
        
        # ERD Image
        erd_lbl = ctk.CTkLabel(left_panel, text="ERD Database:", font=ctk.CTkFont(size=16, weight="bold"))
        erd_lbl.pack(anchor="w", padx=15, pady=(15,0))
        
        try:
            if os.path.exists("erd.png"):
                img = Image.open("erd.png")
                # resize to fit
                img.thumbnail((450, 450))
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
                img_lbl = ctk.CTkLabel(left_panel, image=ctk_img, text="")
                img_lbl.pack(pady=10)
            else:
                ctk.CTkLabel(left_panel, text="(Gambar ERD tidak ditemukan, generate ulang erd.png)").pack(pady=20)
        except Exception as e:
            print("Error loading image:", e)
            
        # Right Panel (JSON Input & Expected Output)
        right_panel = ctk.CTkFrame(self, corner_radius=10)
        right_panel.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=10)
        
        input_lbl = ctk.CTkLabel(right_panel, text="Paste JSON Hasil Query Anda (dari Supabase):", font=ctk.CTkFont(size=16, weight="bold"))
        input_lbl.pack(anchor="w", padx=15, pady=(15,5))
        
        self.json_input = ctk.CTkTextbox(right_panel, height=200, corner_radius=8, font=ctk.CTkFont(family="Consolas", size=13))
        self.json_input.pack(fill="both", expand=True, padx=15, pady=5)
        
        submit_btn = ctk.CTkButton(right_panel, text="Check Answer", font=ctk.CTkFont(weight="bold"), fg_color="#27ae60", hover_color="#2ecc71", command=self.check_answer)
        submit_btn.pack(pady=15)
        
        # Expected Output Textbox (Table Format)
        expected_lbl = ctk.CTkLabel(right_panel, text="Expected Output (Table):", font=ctk.CTkFont(size=16, weight="bold"))
        expected_lbl.pack(anchor="w", padx=15, pady=(10,5))
        
        self.expected_text = ctk.CTkTextbox(right_panel, height=180, corner_radius=8, font=ctk.CTkFont(family="Consolas", size=12), wrap="none")
        formatted_table = make_table(q_data['expected_json'])
        self.expected_text.insert("0.0", formatted_table)
        self.expected_text.configure(state="disabled")
        self.expected_text.pack(fill="both", expand=True, padx=15, pady=(5, 15))

    def check_answer(self):
        user_input = self.json_input.get("0.0", "end").strip()
        if not user_input:
            messagebox.showerror("Error", "Harap paste kode JSON hasil dari Supabase terlebih dahulu!")
            return
            
        try:
            user_json = json.loads(user_input)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Format JSON tidak valid! Pastikan Anda mem-paste JSON yang benar.")
            return
            
        expected = self.q_data['expected_json']
        
        def normalize(obj):
            if isinstance(obj, list):
                return [normalize(item) for item in obj]
            elif isinstance(obj, dict):
                return {k.lower(): normalize(v) for k, v in obj.items()}
            elif isinstance(obj, float) or isinstance(obj, int):
                return str(round(float(obj), 2))
            else:
                return str(obj).strip().lower()

        try:
            norm_user = normalize(user_json)
            norm_expected = normalize(expected)
            
            if norm_user == norm_expected:
                messagebox.showinfo("Berhasil!", "Jawaban Anda Benar! 🎉")
                self.save_callback(self.q_data['id'])
                self.back_callback()
            else:
                messagebox.showwarning("Belum Tepat", "Jawaban Anda belum sesuai dengan Expected Output.\n\nPeriksa kembali logika Query Anda dan pastikan Alias kolom sesuai dengan judul tabel di Expected Output!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat memeriksa: {str(e)}")

if __name__ == "__main__":
    app = SQLPracticeApp()
    app.mainloop()
