import os
from flask import Flask, render_template, request, redirect, url_for, flash
import vercel_blob

# Định vị thư mục templates chính xác tuyệt đối cho Vercel
current_dir = os.path.dirname(__file__)
template_dir = os.path.abspath(os.path.join(current_dir, '..', 'templates'))

app = Flask(__name__, template_folder=template_dir)
app.secret_key = "chuoi_bi_mat_khong_the_doan_duoc"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Không tìm thấy file!')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('Bạn chưa chọn ảnh nào!')
            return redirect(request.url)
        
        if file:
            try:
                # Đọc dữ liệu ảnh và đẩy thẳng lên Vercel Blob vĩnh viễn
                file_bytes = file.read()
                vercel_blob.put(file.filename, file_bytes, {"access": "public"})
                flash('Tải ảnh lên đám mây thành công!')
                return redirect(url_for('upload_file'))
            except Exception as e:
                flash(f'Lỗi tải ảnh: {str(e)}')
                return redirect(request.url)

    # Lấy danh sách ảnh đã lưu từ kho Vercel Blob
    images = []
    try:
        blob_list = vercel_blob.list()
        for b in blob_list.get('blobs', []):
            images.append(b.get('url'))
    except Exception as e:
        print(f"Lỗi hiển thị danh sách ảnh: {e}")
        
    return render_template('index.html', images=images)