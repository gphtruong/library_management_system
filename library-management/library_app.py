import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time

# Cấu hình trang
st.set_page_config(
    page_title="Thư viện Online",
    page_icon="📚",
    layout="wide"
)

# Dữ liệu sách mẫu
if 'books_data' not in st.session_state:
    st.session_state.books_data = {
        'B001': {
            'title': 'Tôi Thấy Hoa Vàng Trên Cỏ Xanh',
            'author': 'Nguyễn Nhật Ánh',
            'category': 'Văn học',
            'isbn': '978-604-2-03456-7',
            'publisher': 'NXB Trẻ',
            'year': 2010,
            'copies_total': 5,
            'copies_available': 5,
            'description': 'Cuốn tiểu thuyết nổi tiếng về tuổi thơ miền quê Việt Nam'
        },
        'B002': {
            'title': 'Cây Cam Ngọt Của Tôi',
            'author': 'José Mauro de Vasconcelos',
            'category': 'Văn học nước ngoài',
            'isbn': '978-604-2-12345-8',
            'publisher': 'NXB Hội Nhà Văn',
            'year': 2020,
            'copies_total': 3,
            'copies_available': 3,
            'description': 'Câu chuyện cảm động về tuổi thơ của cậu bé Brazil',
        },
        'B003': {
            'title': 'Đắc Nhân Tâm',
            'author': 'Dale Carnegie',
            'category': 'Kỹ năng sống',
            'isbn': '978-604-2-98765-4',
            'publisher': 'NXB Tổng Hợp TPHCM',
            'year': 2018,
            'copies_total': 8,
            'copies_available': 8,
            'description': 'Sách kinh điển về phát triển cá nhân trong giao tiếp để thành công',
        },
        'B004': {
            'title': 'Sapiens: Lược Sử Loài Người',
            'author': 'Yuval Noah Harari',
            'category': 'Khoa học',
            'isbn': '978-604-2-55555-5',
            'publisher': 'NXB Thế Giới',
            'year': 2019,
            'copies_total': 4,
            'copies_available': 4,
            'description': 'Cuốn sách khám phá lịch sử tiến hóa của loài người'
        },
        'B005': {
            'title': 'Nhà Giả Kim',
            'author': 'Paulo Coelho',
            'category': 'Văn học nước ngoài',
            'isbn': '978-604-2-11111-1',
            'publisher': 'NXB Văn Học',
            'year': 2017,
            'copies_total': 6,
            'copies_available': 6,
            'description': 'Câu chuyện về hành trình tìm kiếm kho báu của chàng chăn cừu'
        }
    }

# Dữ liệu người dùng mẫu
if 'users_data' not in st.session_state:
    st.session_state.users_data = {
        'user001': {
            'name': 'Nguyễn Văn An',
            'email': 'anvn@email.com',
            'phone': '0123456789',
            'address': 'Quận 1, TP.HCM',
            'member_since': '2023-01-15'
        },
        'user002': {
            'name': 'Trần Thị Bình',
            'email': 'binhtt@email.com',
            'phone': '0987654321',
            'address': 'Quận 3, TP.HCM',
            'member_since': '2023-03-20'
        }
    }

# Dữ liệu mượn sách
if 'borrowing_data' not in st.session_state:
    st.session_state.borrowing_data = []

# Khởi tạo session state cho đăng nhập
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

def login_form():
    st.title("🔐 Đăng nhập Thư viện")
    
    with st.form("login_form"):
        user_id = st.selectbox(
            "Chọn tài khoản:",
            options=list(st.session_state.users_data.keys()),
            format_func=lambda x: f"{x} - {st.session_state.users_data[x]['name']}"
        )
        
        submitted = st.form_submit_button("Đăng nhập")
        
        if submitted:
            st.session_state.logged_in = True
            st.session_state.current_user = user_id
            st.rerun()

def display_book_card(book_id, book_info, context=""):
    with st.container():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.image(book_info['image_url'], width=120)
        
        with col2:
            st.subheader(book_info['title'])
            st.write(f"**Tác giả:** {book_info['author']}")
            st.write(f"**Thể loại:** {book_info['category']}")
            st.write(f"**NXB:** {book_info['publisher']} ({book_info['year']})")
            st.write(f"**ISBN:** {book_info['isbn']}")
            
            # Trạng thái sách
            if book_info['copies_available'] > 0:
                st.success(f"Còn {book_info['copies_available']}/{book_info['copies_total']} cuốn")
                if st.button(f"Mượn sách", key=f"borrow_{book_id}_{context}"):
                    borrow_book(book_id)
            else:
                st.error("Hết sách")
            
            with st.expander("Chi tiết"):
                st.write(book_info['description'])

def borrow_book(book_id):
    if st.session_state.books_data[book_id]['copies_available'] > 0:
        # Giảm số sách có sẵn
        st.session_state.books_data[book_id]['copies_available'] -= 1
        
        # Thêm vào danh sách mượn
        borrow_record = {
            'user_id': st.session_state.current_user,
            'book_id': book_id,
            'borrow_date': datetime.now().strftime("%Y-%m-%d"),
            'return_date': (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
            'status': 'Đang mượn'
        }
        st.session_state.borrowing_data.append(borrow_record)
        
        st.success(f"Mượn sách thành công! Hạn trả: {borrow_record['return_date']}")
        time.sleep(1)
        st.rerun()

def return_book(book_id):
    # Tăng số sách có sẵn
    st.session_state.books_data[book_id]['copies_available'] += 1
    
    # Cập nhật trạng thái trong danh sách mượn
    for record in st.session_state.borrowing_data:
        if (record['user_id'] == st.session_state.current_user and 
            record['book_id'] == book_id and 
            record['status'] == 'Đang mượn'):
            record['status'] = 'Đã trả'
            record['actual_return_date'] = datetime.now().strftime("%Y-%m-%d")
            break
    
    st.success("Trả sách thành công!")
    time.sleep(1)
    st.rerun()

def main_app():
    # Header
    st.title("📚 Thư viện Online")
    
    # Thông tin người dùng
    user_info = st.session_state.users_data[st.session_state.current_user]
    st.sidebar.write(f"**Xin chào:** {user_info['name']}")
    st.sidebar.write(f"**Email:** {user_info['email']}")
    
    if st.sidebar.button("Đăng xuất"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()
    
    # Menu chính
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Danh sách sách", "🔍 Tìm kiếm", "📋 Sách đã mượn", "📊 Thống kê"])
    
    with tab1:
        st.header("Danh sách tất cả sách")
        
        # Lọc theo thể loại
        categories = list(set([book['category'] for book in st.session_state.books_data.values()]))
        selected_category = st.selectbox("Lọc theo thể loại:", ["Tất cả"] + categories)
        
        # Hiển thị sách
        for book_id, book_info in st.session_state.books_data.items():
            if selected_category == "Tất cả" or book_info['category'] == selected_category:
                display_book_card(book_id, book_info, "list")
                st.divider()
    
    with tab2:
        st.header("Tìm kiếm sách")
        
        search_query = st.text_input("Nhập tên sách, tác giả hoặc từ khóa:")
        
        if search_query:
            found_books = []
            for book_id, book_info in st.session_state.books_data.items():
                if (search_query.lower() in book_info['title'].lower() or 
                    search_query.lower() in book_info['author'].lower() or
                    search_query.lower() in book_info['description'].lower()):
                    found_books.append((book_id, book_info))
            
            if found_books:
                st.write(f"Tìm thấy {len(found_books)} kết quả:")
                for i, (book_id, book_info) in enumerate(found_books):
                    display_book_card(book_id, book_info, f"search_{i}")
                    st.divider()
            else:
                st.warning("Không tìm thấy sách nào phù hợp.")
    
    with tab3:
        st.header("Sách đã mượn")
        
        user_borrowed_books = [
            record for record in st.session_state.borrowing_data 
            if record['user_id'] == st.session_state.current_user
        ]
        
        if user_borrowed_books:
            for i, record in enumerate(user_borrowed_books):
                book_info = st.session_state.books_data[record['book_id']]
                
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    st.write(f"**{book_info['title']}**")
                    st.write(f"Tác giả: {book_info['author']}")
                
                with col2:
                    st.write(f"Ngày mượn: {record['borrow_date']}")
                    st.write(f"Hạn trả: {record['return_date']}")
                
                with col3:
                    if record['status'] == 'Đang mượn':
                        # Kiểm tra quá hạn
                        return_date = datetime.strptime(record['return_date'], "%Y-%m-%d")
                        if datetime.now() > return_date:
                            st.error("Quá hạn")
                        else:
                            st.info("Đang mượn")
                    else:
                        st.success("Đã trả")
                
                with col4:
                    if record['status'] == 'Đang mượn':
                        if st.button("Trả sách", key=f"return_{record['book_id']}_{record['borrow_date']}_{i}"):
                            return_book(record['book_id'])
                
                st.divider()
        else:
            st.info("Bạn chưa mượn sách nào.")
    
    with tab4:
        st.header("Thống kê thư viện")
        
        # Thống kê tổng quan
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_books = sum([book['copies_total'] for book in st.session_state.books_data.values()])
            st.metric("Tổng số sách", total_books)
        
        with col2:
            available_books = sum([book['copies_available'] for book in st.session_state.books_data.values()])
            st.metric("Sách có sẵn", available_books)
        
        with col3:
            borrowed_books = total_books - available_books
            st.metric("Sách đang cho mượn", borrowed_books)
        
        with col4:
            total_users = len(st.session_state.users_data)
            st.metric("Tổng thành viên", total_users)
        
        # Biểu đồ thể loại sách
        st.subheader("Phân bố theo thể loại")
        category_count = {}
        for book in st.session_state.books_data.values():
            category = book['category']
            category_count[category] = category_count.get(category, 0) + book['copies_total']
        
        if category_count:
            df_category = pd.DataFrame(list(category_count.items()), columns=['Thể loại', 'Số lượng'])
            st.bar_chart(df_category.set_index('Thể loại'))
        
        # Sách phổ biến
        st.subheader("Sách được mượn nhiều nhất")
        borrow_count = {}
        for record in st.session_state.borrowing_data:
            book_id = record['book_id']
            book_title = st.session_state.books_data[book_id]['title']
            borrow_count[book_title] = borrow_count.get(book_title, 0) + 1
        
        if borrow_count:
            sorted_books = sorted(borrow_count.items(), key=lambda x: x[1], reverse=True)[:5]
            df_popular = pd.DataFrame(sorted_books, columns=['Tên sách', 'Lượt mượn'])
            st.dataframe(df_popular, use_container_width=True)

# Main execution
if not st.session_state.logged_in:
    login_form()
else:
    main_app()
