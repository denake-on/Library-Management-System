<template>
  <div class="my-borrowings-container">
    <div class="borrowings-header">
      <button class="back-btn" @click="goBack">← Back to Home</button>
      <h1>My Borrowings</h1>
      <p>Each books can be borrowed for 20 days, and be renewed once for 10 days.</p>
    </div>
    
    <!-- Loading state -->
    <div v-if="loading" class="loading">
      <p>Loading your borrowings...</p>
    </div>
    
    <!-- No borrowings -->
    <div v-else-if="borrowings.length === 0" class="no-borrowings">
      <p>You haven't borrowed any books yet.</p>
    </div>
    
    <!-- Borrowings list -->
    <div v-else class="borrowings-list">
      <div 
        v-for="borrowing in borrowings" 
        :key="borrowing.borrow_id" 
        class="borrowing-card"
      >
        <div class="book-cover-container">
          <img :src="coverImage" alt="Book Cover" class="book-cover" />
        </div>
        <div class="borrowing-info">
          <h3>{{ borrowing.book_name }}</h3>
          <p><strong>Author:</strong> {{ borrowing.author }}</p>
          <p><strong>Borrow Date:</strong> {{ formatDate(borrowing.borrow_date) }}</p>
          <p><strong>Due Date:</strong> {{ formatDate(borrowing.due_date) }}</p>
          <p v-if="borrowing.return_date"><strong>Return Date:</strong> {{ formatDate(borrowing.return_date) }}</p>
          <div class="actions">
            <button
              v-if="!borrowing.return_date"
              class="return-btn"
              @click="returnBook(borrowing)"
            >
              Return
            </button>
            <button
              v-if="!borrowing.return_date && borrowing.renew === 0"
              class="renew-btn"
              @click="renewBook(borrowing)"
            >
              Renew
            </button>
            <button
              v-else-if="!borrowing.return_date && borrowing.renew === 1"
              class="renew-btn disabled"
              :disabled="true"
            >
              Renew (Unavailable)
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Return message -->
  <div v-if="returnMessage" class="return-message" :class="returnMessage.type">
    {{ returnMessage.text }}
  </div>
</template>

<script>
import coverImage from '../../assets/cover.png';

export default {
  name: 'MyBorrowings',
  emits: ['back-to-home'],
  data() {
    return {
      coverImage: coverImage,
      borrowings: [],
      loading: true,
      returnMessage: null
    }
  },
  async mounted() {
    await this.loadBorrowings();
  },
  methods: {
    async loadBorrowings() {
      try {
        const userRole = localStorage.getItem('userRole');

        if (userRole !== 'reader') {
          console.error('Only readers can access borrowings');
          return;
        }

        // 获取存储的学生ID
        const studentId = localStorage.getItem('userId');

        if (!studentId) {
          console.error('No student ID found. Please login again.');
          alert('Student ID not found. Please login again to refresh your session.');
          return;
        }

        // 调用后端API获取借阅信息
        const response = await fetch(`http://127.0.0.1:8000/api/reader-borrowings?student_id=${encodeURIComponent(studentId)}`);
        const data = await response.json();

        if (data.borrowings && data.borrowings.length > 0) {
          this.borrowings = data.borrowings;
        } else {
          this.borrowings = [];
        }
      } catch (error) {
        console.error('Error loading borrowings:', error);
        // 处理错误
      } finally {
        this.loading = false;
      }
    },
    
    goBack() {
      this.$emit('back-to-home');
    },
    
    formatDate(dateString) {
      // 格式化日期显示
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('en-US', options);
    },
    
    
    async returnBook(borrowing) {
      if (confirm(`Are you sure you want to return "${borrowing.book_name}"?`)) {
        try {
          // 获取学生ID
          const studentId = localStorage.getItem('userId');
          if (!studentId) {
            console.error('No student ID found');
            this.returnMessage = {
              type: 'error',
              text: 'User not authenticated. Please login again.'
            };
            return;
          }

          // 调用后端API归还图书
          const response = await fetch(`http://127.0.0.1:8000/api/reader-return-books?student_id=${encodeURIComponent(studentId)}&book_id=${borrowing.book_id}`, {
            method: 'GET'
          });

          const data = await response.json();

          if (response.ok) {
            // 更新本地状态
            borrowing.return_date = data.return_date;
            // Remove the buttons after return
            borrowing.returned = true;

            // 从借阅列表中移除已归还的书籍或刷新列表
            // 这里简单更新本地状态，实际应用中可能需要重新加载数据
            this.borrowings = [...this.borrowings]; // 触发响应式更新

            // 显示成功消息
            this.returnMessage = {
              type: 'success',
              text: `Successfully returned "${borrowing.book_name}"!`
            };

            // Clear the message after 5 seconds
            setTimeout(() => {
              this.returnMessage = null;
            }, 5000);
          } else {
            this.returnMessage = {
              type: 'error',
              text: data.detail || 'Failed to return book. Please try again.'
            };
          }
        } catch (error) {
          console.error('Error returning book:', error);
          this.returnMessage = {
            type: 'error',
            text: 'Network error. Failed to return book. Please try again.'
          };
        }
      }
    },

    async renewBook(borrowing) {
      try {
        // 获取学生ID
        const studentId = localStorage.getItem('userId');
        if (!studentId) {
          console.error('No student ID found');
          this.returnMessage = {
            type: 'error',
            text: 'User not authenticated. Please login again.'
          };
          return;
        }

        // 调用后端API续借图书
        const response = await fetch(`http://127.0.0.1:8000/api/reader-renew-books?student_id=${encodeURIComponent(studentId)}&book_id=${borrowing.book_id}`, {
          method: 'GET'
        });

        const data = await response.json();

        if (response.ok) {
          // 更新本地状态
          borrowing.renew = 1; // 标记为已续借

          // 更新借阅列表
          this.borrowings = [...this.borrowings]; // 触发响应式更新

          // 显示成功消息
          this.returnMessage = {
            type: 'success',
            text: `Successfully renewed "${borrowing.book_name}"!`
          };

          // Clear the message after 5 seconds
          setTimeout(() => {
            this.returnMessage = null;
          }, 5000);
        } else {
          this.returnMessage = {
            type: 'error',
            text: data.detail || 'Failed to renew book. Please try again.'
          };
        }
      } catch (error) {
        console.error('Error renewing book:', error);
        this.returnMessage = {
          type: 'error',
          text: 'Network error. Failed to renew book. Please try again.'
        };
      }
    }
  }
}
</script>

<style scoped>
.my-borrowings-container {
  min-height: 100vh;
  padding: 40px 20px;
  background: rgba(0, 0, 0, 0.4);
  color: white;
}

.borrowings-header {
  max-width: 1000px;
  margin: 0 auto 30px;
}

.borrowings-header h1 {
  text-align: center;
  margin-bottom: 20px;
  font-size: 28px;
}

.back-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 10px 15px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 20px;
}

.loading, .no-borrowings {
  text-align: center;
  padding: 40px 0;
  font-size: 18px;
}

.borrowings-list {
  max-width: 1000px;
  margin: 0 auto;
}

.borrowing-card {
  display: flex;
  gap: 20px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  margin-bottom: 15px;
  align-items: center;
}

.book-cover-container {
  flex-shrink: 0;
}

.book-cover {
  width: 80px;
  height: 110px;
  border-radius: 6px;
  object-fit: cover;
}

.borrowing-info {
  flex: 1;
}

.borrowing-info h3 {
  margin-bottom: 10px;
  font-size: 18px;
}

.borrowing-info p {
  margin-bottom: 8px;
  font-size: 14px;
}

.status-borrowed {
  color: #f39c12;
  font-weight: bold;
}

.status-returned {
  color: #2ecc71;
  font-weight: bold;
}

.actions {
  margin-top: 15px;
}

.return-btn {
  background: rgba(243, 156, 18, 0.7);
  border: none;
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  margin-right: 10px;
}

.return-btn:hover {
  background: rgba(243, 156, 18, 1);
}

.renew-btn {
  background: rgba(52, 152, 219, 0.7);
  border: none;
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
}

.renew-btn:hover {
  background: rgba(52, 152, 219, 1);
}

.renew-btn.disabled {
  background: rgba(150, 150, 150, 0.5);
  cursor: not-allowed;
}

.return-message {
  margin: 15px auto;
  max-width: 600px;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  text-align: center;
}

.return-message.success {
  background: rgba(46, 204, 113, 0.2);
  color: #2ecc71;
  border: 1px solid rgba(46, 204, 113, 0.3);
}

.return-message.error {
  background: rgba(231, 76, 60, 0.2);
  color: #e74c3c;
  border: 1px solid rgba(231, 76, 60, 0.3);
}

@media (max-width: 768px) {
  .borrowing-card {
    flex-direction: column;
    text-align: center;
  }

  .book-cover {
    align-self: center;
  }
}
</style>