<template>
  <div class="book-detail-container">
    <div class="detail-content">
      <div class="detail-header">
        <button class="back-btn" @click="goBack">← Back to Search</button>
      </div>
      
      <div class="book-detail">
        <img :src="coverImage" alt="Book Cover" class="book-cover" />
        <div class="book-info">
          <h2>{{ book.book_name }}</h2>
          <div class="info-grid">
            <div class="info-item">
              <label>Author:</label>
              <span>{{ book.author }}</span>
            </div>
            <div class="info-item">
              <label>Publisher:</label>
              <span>{{ book.publisher }}</span>
            </div>
            <div class="info-item">
              <label>Location:</label>
              <span>{{ book.location }}</span>
            </div>
            <div class="info-item">
              <label>Availability:</label>
              <span :class="book.if_available ? 'available' : 'unavailable'">
                {{ book.if_available ? 'Available' : 'Not Available' }}
              </span>
            </div>
            <div class="info-item">
              <label>Year:</label>
              <span>{{ book.publish_year }}</span>
            </div>
          </div>
          
          <div class="actions">
            <button 
              v-if="userRole === 'reader'" 
              class="borrow-btn" 
              @click="handleBorrow"
              :disabled="!book.if_available"
            >
              Borrow
            </button>
            <button 
              v-if="userRole === 'librarian' || userRole === 'director'" 
              class="edit-btn" 
              @click="handleEdit"
            >
              Edit
            </button>
            <button 
              v-if="userRole === 'librarian' || userRole === 'director'" 
              class="delete-btn" 
              @click="handleDelete"
            >
              Delete
            </button>
            <button class="back-btn-secondary" @click="goBack">Back to Search</button>
          </div>
        </div>

        <!-- Borrow success message -->
        <div v-if="borrowMessage" class="borrow-message" :class="borrowMessage.type">
          {{ borrowMessage.text }}
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="cancelEdit">
      <div class="modal-content">
        <h3>Edit Book Information</h3>
        <div class="edit-form">
          <div class="form-group">
            <label>Book Name:</label>
            <input type="text" v-model="editForm.book_name" placeholder="Book name">
          </div>
          <div class="form-group">
            <label>Author:</label>
            <input type="text" v-model="editForm.author" placeholder="Author">
          </div>
          <div class="form-group">
            <label>Publisher:</label>
            <input type="text" v-model="editForm.publisher" placeholder="Publisher">
          </div>
          <div class="form-group">
            <label>Publish Year:</label>
            <input type="number" v-model="editForm.publish_year" placeholder="Publish year">
          </div>
          <div class="form-group">
            <label>Location:</label>
            <input type="text" v-model="editForm.location" placeholder="Location">
          </div>
          <div class="form-group">
            <label>Availability:</label>
            <select v-model="editForm.if_available">
              <option :value="1">Available</option>
              <option :value="0">Not Available</option>
            </select>
          </div>
        </div>
        <div class="modal-actions">
          <button class="save-btn" @click="saveEdit">Save</button>
          <button class="cancel-btn" @click="cancelEdit">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import coverImage from '../../assets/cover.png';

export default {
  name: 'BookDetail',
  props: {
    book: {
      type: Object,
      required: true
    },
    userRole: {
      type: String,
      required: true
    }
  },
  emits: ['back-to-search', 'borrow', 'edit', 'delete'],
  data() {
    return {
      coverImage: coverImage,
      borrowMessage: null,
      showEditModal: false,
      editForm: {
        book_name: '',
        author: '',
        publisher: '',
        publish_year: '',
        location: '',
        if_available: 1
      }
    }
  },
  methods: {
    goBack() {
      this.$emit('back-to-search');
    },
    async handleBorrow() {
      try {
        // Get student ID from localStorage
        const studentId = localStorage.getItem('userId');
        if (!studentId) {
          this.borrowMessage = {
            type: 'error',
            text: 'User not authenticated. Please login again.'
          };
          return;
        }

        // Call the backend API to borrow the book
        const response = await fetch(`http://127.0.0.1:8000/api/borrow-book?student_id=${encodeURIComponent(studentId)}&book_id=${this.book.book_id}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        });

        const data = await response.json();

        if (response.ok) {
          // Show success message
          this.borrowMessage = {
            type: 'success',
            text: `Successfully borrowed "${this.book.book_name}"! Due date: ${data.due_date}`
          };

          // Update the book availability in the UI
          this.book.if_available = 0;

          // Emit the borrow event to parent component
          this.$emit('borrow');

          // Clear the message after 5 seconds
          setTimeout(() => {
            this.borrowMessage = null;
          }, 5000);
        } else {
          // Show error message
          this.borrowMessage = {
            type: 'error',
            text: data.detail || 'Failed to borrow book. Please try again.'
          };
        }
      } catch (error) {
        console.error('Error borrowing book:', error);
        this.borrowMessage = {
          type: 'error',
          text: 'Network error. Please try again.'
        };
      }
    },
    handleEdit() {
      // 初始化编辑表单
      this.editForm = {
        book_name: this.book.book_name || '',
        author: this.book.author || '',
        publisher: this.book.publisher || '',
        publish_year: this.book.publish_year || '',
        location: this.book.location || '',
        if_available: this.book.if_available !== undefined ? this.book.if_available : 1
      };
      this.showEditModal = true;
    },
    async saveEdit() {
      try {
        const updateData = {
          book_id: this.book.book_id
        };

        // 只添加有值的字段
        if (this.editForm.book_name) updateData.book_name = this.editForm.book_name;
        if (this.editForm.author) updateData.author = this.editForm.author;
        if (this.editForm.publisher) updateData.publisher = this.editForm.publisher;
        if (this.editForm.publish_year) updateData.publish_year = parseInt(this.editForm.publish_year);
        if (this.editForm.location) updateData.location = this.editForm.location;
        if (this.editForm.if_available !== undefined) updateData.if_available = parseInt(this.editForm.if_available);

        const response = await fetch('http://127.0.0.1:8000/api/update-book', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(updateData)
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
          // 更新本地 book 对象
          Object.assign(this.book, updateData);
          this.showEditModal = false;
          this.borrowMessage = {
            type: 'success',
            text: 'Book information updated successfully!'
          };
          setTimeout(() => {
            this.borrowMessage = null;
          }, 3000);
        } else {
          this.borrowMessage = {
            type: 'error',
            text: data.detail || 'Failed to update book'
          };
        }
      } catch (error) {
        console.error('Error updating book:', error);
        this.borrowMessage = {
          type: 'error',
          text: 'Error updating book. Please try again.'
        };
      }
    },
    cancelEdit() {
      this.showEditModal = false;
    },
    async handleDelete() {
      if (!confirm(`Are you sure you want to delete book "${this.book.book_name}"?`)) {
        return;
      }

      try {
        const response = await fetch(`http://127.0.0.1:8000/api/delete-book?book_id=${this.book.book_id}`, {
          method: 'DELETE'
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
          this.$emit('delete');
        } else {
          this.borrowMessage = {
            type: 'error',
            text: data.detail || 'Failed to delete book'
          };
        }
      } catch (error) {
        console.error('Error deleting book:', error);
        this.borrowMessage = {
          type: 'error',
          text: 'Error deleting book. Please try again.'
        };
      }
    }
  }
}
</script>

<style scoped>
.book-detail-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  background: rgba(0, 0, 0, 0.4);
}

.detail-content {
  width: 800px;
  max-width: 90%;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 30px;
  backdrop-filter: blur(10px);
}

.detail-header {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.back-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 10px 15px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
}

.book-detail {
  display: flex;
  gap: 30px;
  align-items: flex-start;
}

.book-cover {
  width: 180px;
  height: 240px;
  border-radius: 10px;
  object-fit: cover;
  flex-shrink: 0;
}

.book-info {
  flex: 1;
}

.book-info h2 {
  margin-bottom: 25px;
  font-size: 24px;
  color: white;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 30px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-item label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 5px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-item span {
  font-size: 16px;
  color: white;
  font-weight: 500;
}

.available {
  color: #2ecc71;
}

.unavailable {
  color: #e74c3c;
}

.actions {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.actions button {
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 14px;
  transition: opacity 0.3s;
}

.borrow-btn {
  background: rgba(46, 204, 113, 0.7);
}

.borrow-btn:disabled {
  background: rgba(150, 150, 150, 0.5);
  cursor: not-allowed;
}

.edit-btn {
  background: rgba(241, 196, 15, 0.7);
}

.delete-btn {
  background: rgba(231, 76, 60, 0.7);
}

.back-btn-secondary {
  background: rgba(255, 255, 255, 0.2);
}

.actions button:hover:not(:disabled) {
  opacity: 0.8;
}

.borrow-message {
  margin-top: 15px;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  text-align: center;
}

.borrow-message.success {
  background: rgba(46, 204, 113, 0.2);
  color: #2ecc71;
  border: 1px solid rgba(46, 204, 113, 0.3);
}

.borrow-message.error {
  background: rgba(231, 76, 60, 0.2);
  color: #e74c3c;
  border: 1px solid rgba(231, 76, 60, 0.3);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: rgba(20, 20, 20, 0.95);
  border-radius: 12px;
  padding: 30px;
  width: 500px;
  max-width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.modal-content h3 {
  color: white;
  margin-bottom: 20px;
  font-size: 20px;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-group label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
}

.form-group input,
.form-group select {
  padding: 10px;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(0, 0, 0, 0.5);
  color: white;
  font-size: 14px;
}

.form-group input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.modal-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  justify-content: flex-end;
}

.save-btn,
.cancel-btn {
  padding: 10px 20px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  transition: opacity 0.3s;
}

.save-btn {
  background: rgba(46, 204, 113, 0.7);
  color: white;
}

.cancel-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.save-btn:hover,
.cancel-btn:hover {
  opacity: 0.8;
}

@media (max-width: 768px) {
  .book-detail {
    flex-direction: column;
  }

  .book-cover {
    align-self: center;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .actions {
    flex-direction: column;
  }
}
</style>