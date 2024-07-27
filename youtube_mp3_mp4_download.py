import tkinter as tk
from tkinter import ttk, messagebox
import yt_dlp
from threading import Thread

class YouTubeDownloader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader")
        self.geometry("400x200")
        self.create_widgets()
        self.create_context_menu()

    def create_widgets(self):
        tk.Label(self, text="YouTube URL:").pack(pady=5)
        self.url_entry = tk.Entry(self, width=50)
        self.url_entry.pack(pady=5)
        
        self.download_type = tk.StringVar(value="mp4")
        tk.Radiobutton(self, text="MP4", variable=self.download_type, value="mp4").pack(pady=5)
        tk.Radiobutton(self, text="MP3", variable=self.download_type, value="mp3").pack(pady=5)
        
        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=5)
        
        tk.Button(self, text="Download", command=self.start_download).pack(pady=5)

    def create_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Paste", command=self.paste)

        self.url_entry.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def paste(self):
        try:
            self.url_entry.insert(tk.END, self.clipboard_get())
        except tk.TclError:
            pass

    def start_download(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return

        Thread(target=self.download, args=(url, self.download_type.get())).start()

    def download(self, url, download_type):
        try:
            ydl_opts = {
                'format': 'bestaudio/best' if download_type == 'mp3' else 'bestvideo+bestaudio/best',
                'progress_hooks': [self.progress_hook],
                'outtmpl': '%(title)s.%(ext)s',
                'ffmpeg_location': 'C:/ffmpeg/bin',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4'
                }] if download_type == 'mp4' else [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            messagebox.showinfo("Success", "Download completed successfully")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes', 0)
            if total > 0:
                percentage = (downloaded / total) * 100
                self.progress["value"] = percentage
                self.update_idletasks()
                print(f"Downloaded: {downloaded}, Total: {total}, Percentage: {percentage}")

if __name__ == "__main__":
    app = YouTubeDownloader()
    app.mainloop()