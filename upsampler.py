import os, subprocess, customtkinter as ctk
from tkinter import filedialog

class HilbertDespacio(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hilbert Despacio")
        self.geometry("400x280")
        self.master_vector = ""
        
        # UI: Gold/Dark minimalist aesthetic
        ctk.CTkLabel(self, text="HILBERT DESPACIO", font=("Arial", 28, "bold"), text_color="#FFD700").pack(pady=20)
        
        self.btn_ir = ctk.CTkButton(self, text="1. SELECT SPACES", command=self.fuse, fg_color="#333333")
        self.btn_ir.pack(pady=10)
        
        self.btn_run = ctk.CTkButton(self, text="2. PROCESS ALL MUSIC", command=self.project, state="disabled")
        self.btn_run.pack(pady=10)
        
        self.status = ctk.CTkLabel(self, text="Awaiting Vectors...", text_color="gray")
        self.status.pack(pady=20)

    def fuse(self):
        folder = filedialog.askdirectory(title="Folder of IR WAVs")
        if not folder: return
        irs = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(".wav")]
        self.master_vector = os.path.join(folder, "MASTER_VECTOR.wav")
        # Summing wave functions via SoX
        subprocess.run(["sox", "-m"] + irs + [self.master_vector], stderr=subprocess.DEVNULL)
        self.btn_run.configure(state="normal", fg_color="#228B22")
        self.status.configure(text="Master Vector Ready.", text_color="white")

    def project(self):
        folder = filedialog.askdirectory(title="Music Folder")
        if not folder: return
        out = os.path.join(folder, "HILBERT_OUT")
        os.makedirs(out, exist_ok=True)
        files = [f for f in os.listdir(folder) if f.lower().endswith((".flac", ".wav"))]
        for f in files:
            self.status.configure(text=f"Projecting: {f[:15]}...")
            self.update()
            # The Despacio Ratio (10:1.5) for clarity and stadium-scale physics
            cmd = ["ffmpeg", "-y", "-i", os.path.join(folder, f), "-i", self.master_vector, 
                   "-filter_complex", "afir=dry=10:wet=1.5", os.path.join(out, f)]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.status.configure(text="Success.", text_color="#FFD700")

if __name__ == "__main__":
    app = HilbertDespacio()
    app.mainloop()
