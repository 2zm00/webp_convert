from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
import os

class WebPConverterPro:
    def __init__(self, root):
        self.root = root
        self.root.title("WebP 변환기")
        self.input_path = None
        self.output_path = None
        
        self.create_ui()

    def create_ui(self):
        tk.Label(self.root, text="이미지 변환기", font=('맑은 고딕', 14)).pack(pady=10)
        
        # 버튼 프레임
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="파일 선택", command=self.select_file).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="저장 경로", command=self.select_save).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="변환 실행", command=self.convert).pack(side=tk.LEFT, padx=5)

    def select_file(self):
        file_types = [
            ('이미지 파일', '*.jpg *.jpeg *.png *.gif'),
            ('모든 파일', '*.*')
        ]
        self.input_path = filedialog.askopenfilename(filetypes=file_types)
        if self.input_path:
            messagebox.showinfo("로드 완료", f"선택 파일:\n{os.path.basename(self.input_path)}")

    def select_save(self):
        self.output_path = filedialog.asksaveasfilename(
            defaultextension=".webp",
            filetypes=[('WebP 파일', '*.webp')]
        )

    def handle_gif(self, img):
        """애니메이션 GIF 처리 함수"""
        frames = []
        durations = []
        
        for frame_idx in range(img.n_frames):
            img.seek(frame_idx)
            frame = img.convert('RGBA')
            
            # 투명 배경 처리
            if frame.mode == 'RGBA':
                background = Image.new('RGB', frame.size, (255, 255, 255))
                background.paste(frame, mask=frame.split()[-1])
                frame = background
            
            frames.append(frame.convert('RGB'))
            durations.append(img.info['duration'])
        
        return frames, durations

    def convert(self):
        if not all([self.input_path, self.output_path]):
            messagebox.showerror("오류", "파일과 저장 경로를 선택하세요")
            return

        try:
            img = Image.open(self.input_path)
            is_animated = getattr(img, 'is_animated', False)

            # GIF 애니메이션 처리
            if img.format == 'GIF' and is_animated:
                frames, durations = self.handle_gif(img)
                frames[0].save(
                    self.output_path,
                    'webp',
                    save_all=True,
                    append_images=frames[1:],
                    duration=durations,
                    loop=0,
                    quality=90
                )
                
            # 일반 이미지 처리
            else:
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255,255,255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                
                img.save(self.output_path, 'webp', quality=85)
            
            messagebox.showinfo("성공", f"변환 완료!\n{self.output_path}")
            
        except Exception as e:
            messagebox.showerror("에러", f"처리 실패:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x250")
    WebPConverterPro(root)
    root.mainloop()
