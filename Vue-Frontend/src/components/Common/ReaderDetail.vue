<template>
  <teleport to="body">
    <div class="reader-detail-container">
      <div class="detail-content">
      <div class="detail-header">
        <button class="back-btn" @click="goBack">← Back to Search</button>
      </div>
      
      <div class="reader-detail">
        <img :src="avatarSrc" :alt="reader.name" class="reader-avatar" />
        <div class="reader-info">
          <h2>{{ reader.name }}</h2>
          <div class="info-grid">
            <div class="info-item">
              <label>Reader ID:</label>
              <span>{{ reader.reader_id }}</span>
            </div>
            <div class="info-item">
              <label>Student ID:</label>
              <span>{{ reader.student_id }}</span>
            </div>
            <div class="info-item">
              <label>Email:</label>
              <span>{{ reader.email }}</span>
            </div>
            <div class="info-item">
              <label>Phone:</label>
              <span>{{ reader.phone }}</span>
            </div>
            <div class="info-item">
              <label>Department:</label>
              <span>{{ reader.department }}</span>
            </div>
            <div class="info-item">
              <label>Major:</label>
              <span>{{ reader.major }}</span>
            </div>
          </div>
          
          <div class="actions" v-if="userRole === 'librarian' || userRole === 'director'">
            <button class="edit-btn" @click="handleEdit">Edit</button>
            <button class="delete-btn" @click="handleDelete">Delete</button>
            <button class="back-btn-secondary" @click="goBack">Back to Search</button>
          </div>

          <!-- Message -->
          <div v-if="message" class="message" :class="message.type">
            {{ message.text }}
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="cancelEdit">
      <div class="modal-content">
        <h3>Edit Reader Information</h3>
        <div class="edit-form">
          <div class="form-group">
            <label>Name:</label>
            <input type="text" v-model="editForm.name" placeholder="Name">
          </div>
          <div class="form-group">
            <label>Email:</label>
            <input type="email" v-model="editForm.email" placeholder="Email">
          </div>
          <div class="form-group">
            <label>Phone:</label>
            <input type="text" v-model="editForm.phone" placeholder="Phone">
          </div>
          <div class="form-group">
            <label>Password (leave empty to keep current):</label>
            <input type="password" v-model="editForm.password" placeholder="Password">
          </div>
          <div class="form-group">
            <label>Department:</label>
            <input type="text" v-model="editForm.department" placeholder="Department">
          </div>
          <div class="form-group">
            <label>Major:</label>
            <input type="text" v-model="editForm.major" placeholder="Major">
          </div>
        </div>
        <div class="modal-actions">
          <button class="save-btn" @click="saveEdit">Save</button>
          <button class="cancel-btn" @click="cancelEdit">Cancel</button>
        </div>
      </div>
      </div>
    </div>
  </teleport>
</template>

<script>
import defaultAvatar from '../../assets/default_avatar1.png';

export default {
  name: 'ReaderDetail',
  props: {
    reader: {
      type: Object,
      required: true
    },
    userRole: {
      type: String,
      required: true
    }
  },
  emits: ['back-to-search', 'edit', 'delete'],
  data() {
    return {
      avatarSrc: defaultAvatar,
      showEditModal: false,
      editForm: {
        name: '',
        email: '',
        phone: '',
        password: '',
        department: '',
        major: ''
      },
      message: null
    }
  },
  methods: {
    goBack() {
      this.$emit('back-to-search');
    },
    handleEdit() {
      // 初始化编辑表单
      this.editForm = {
        name: this.reader.name || '',
        email: this.reader.email || '',
        phone: this.reader.phone || '',
        password: '',
        department: this.reader.department || '',
        major: this.reader.major || ''
      };
      this.showEditModal = true;
    },
    async saveEdit() {
      try {
        const updateData = {
          student_id: this.reader.student_id
        };

        // 只添加有值的字段
        if (this.editForm.name) updateData.name = this.editForm.name;
        if (this.editForm.email) updateData.email = this.editForm.email;
        if (this.editForm.phone) updateData.phone = this.editForm.phone;
        if (this.editForm.password) updateData.password = this.editForm.password;
        if (this.editForm.department) updateData.department = this.editForm.department;
        if (this.editForm.major) updateData.major = this.editForm.major;

        const response = await fetch('http://127.0.0.1:8000/api/update-reader', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(updateData)
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
          // 更新本地 reader 对象
          Object.assign(this.reader, updateData);
          this.showEditModal = false;
          this.message = {
            type: 'success',
            text: 'Reader information updated successfully!'
          };
          // Notify parent that reader was edited so lists can update
          this.$emit('edit', updateData);
          setTimeout(() => {
            this.message = null;
          }, 3000);
        } else {
          this.message = {
            type: 'error',
            text: data.detail || 'Failed to update reader'
          };
        }
      } catch (error) {
        console.error('Error updating reader:', error);
        this.message = {
          type: 'error',
          text: 'Error updating reader. Please try again.'
        };
      }
    },
    cancelEdit() {
      this.showEditModal = false;
    },
    async handleDelete() {
      if (!confirm(`Are you sure you want to delete reader "${this.reader.name}" (${this.reader.student_id})?`)) {
        return;
      }

      try {
        const response = await fetch(`http://127.0.0.1:8000/api/delete-reader?student_id=${encodeURIComponent(this.reader.student_id)}`, {
          method: 'DELETE'
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
          this.$emit('delete', this.reader);
        } else {
          this.message = {
            type: 'error',
            text: data.detail || 'Failed to delete reader'
          };
        }
      } catch (error) {
        console.error('Error deleting reader:', error);
        this.message = {
          type: 'error',
          text: 'Error deleting reader. Please try again.'
        };
      }
    }
  }
}
</script>

<style scoped>
.reader-detail-container {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  background: rgba(0, 0, 0, 0.6);
  z-index: 99999;
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

.reader-detail {
  display: flex;
  gap: 30px;
  align-items: flex-start;
}

.reader-avatar {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.reader-info {
  flex: 1;
}

.reader-info h2 {
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

.message {
  margin-top: 15px;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  text-align: center;
}

.message.success {
  background: rgba(46, 204, 113, 0.2);
  color: #2ecc71;
  border: 1px solid rgba(46, 204, 113, 0.3);
}

.message.error {
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

.form-group input {
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
  .reader-detail {
    flex-direction: column;
    text-align: center;
  }
  
  .reader-avatar {
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