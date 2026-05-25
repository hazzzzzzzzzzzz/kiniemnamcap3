import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash
import vercel_blob

# Xác định đường dẫn gốc của dự án bằng Pathlib
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"

app = Flask(__name__, template_folder=str(TEMPLATE_DIR))
app.secret_key = "chuoi_bao_mat_he_thong_2026"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Không tìm thấy file!')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('Bạn chưa chọn ảnh!')
            return redirect(request.url)
        
        if file:
            try:
                file_bytes = file.read()
                vercel_blob.put(file.filename, file_bytes, {"access": "public"})
                flash('Tải ảnh lên đám mây thành công!')
                return redirect(url_for('upload_file'))
            except Exception as e:
                flash(f'Lỗi hệ thống: {str(e)}')
                return redirect(request.url)

    images = []
    try:
        blob_list = vercel_blob.list()
        for b in blob_list.get('blobs', []):
            images.append(b.get('url'))
    except Exception as e:
        print(f"Lỗi kết nối bộ lưu trữ: {e}")
        
    return render_template('index.html', images=images)