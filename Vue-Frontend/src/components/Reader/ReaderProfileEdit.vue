<template>
  <div class="profile-edit-container">
    <div class="profile-header">
      <button class="back-btn" @click="goBack">← Back to Home</button>
      <h1>Edit Profile</h1>
    </div>
    
    <div class="profile-content">
      <div class="profile-left">
        <!-- Avatar section -->
        <div class="avatar-section">
          <img :src="avatarSrc" alt="Avatar" class="avatar" />
          <button class="change-avatar-btn">Change Avatar</button>
        </div>
        
        <!-- Reading activity calendar -->
        <div class="calendar-section">
          <ReadingCalendar />
        </div>
      </div>
      
      <div class="profile-right">
        <!-- Profile form -->
        <form class="profile-form" @submit.prevent="updateProfile">
          <div class="form-group">
            <label for="name">Name</label>
            <input 
              type="text" 
              id="name" 
              v-model="profile.name" 
              :disabled="!isEditing"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="email">Email</label>
            <input 
              type="email" 
              id="email" 
              v-model="profile.email" 
              :disabled="!isEditing"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="phone">Phone</label>
            <input 
              type="text" 
              id="phone" 
              v-model="profile.phone" 
              :disabled="!isEditing"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="studentId">Student ID</label>
            <input 
              type="text" 
              id="studentId" 
              v-model="profile.student_id" 
              disabled
              class="form-input"
            />
          </div>
          
          <!-- Action buttons -->
          <div class="form-actions" v-if="!isEditing">
            <button type="button" class="edit-btn" @click="enableEditing">Edit Profile</button>
          </div>
          
          <div class="form-actions" v-else>
            <button type="submit" class="save-btn">Save Changes</button>
            <button type="button" class="cancel-btn" @click="cancelEditing">Cancel</button>
          </div>
        </form>
        
        <!-- Message display -->
        <div v-if="message" class="message" :class="message.type">
          {{ message.text }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import defaultAvatar from '../../assets/default_avatar1.png';
import ReadingCalendar from '../Reader/Calendar/ReadingCalendar.vue';

export default {
  name: 'ReaderProfileEdit',
  components: {
    ReadingCalendar
  },
  emits: ['back-to-home'],
  data() {
    return {
      avatarSrc: defaultAvatar,
      isEditing: false,
      profile: {
        name: '',
        email: '',
        phone: '',
        student_id: ''
      },
      originalProfile: {}, // Store original values for cancel
      message: null
    }
  },
  async mounted() {
    await this.loadProfileData();
  },
  methods: {
    async loadProfileData() {
      try {
        // Get student ID from localStorage
        const studentId = localStorage.getItem('userId');
        if (!studentId) {
          console.error('No student ID found');
          this.showMessage('error', 'User not authenticated. Please login again.');
          return;
        }

        // Call backend API to get profile information
        const response = await fetch(`http://127.0.0.1:8000/api/reader-information?student_id=${encodeURIComponent(studentId)}`);
        const data = await response.json();

        if (response.ok && data.information) {
          const info = data.information;
          this.profile = {
            name: info.name || localStorage.getItem('username') || 'Unknown',
            email: info.email || 'N/A',
            phone: info.phone || 'N/A',
            student_id: studentId
          };
        } else {
          // Fallback to basic info if API call fails
          this.profile = {
            name: localStorage.getItem('username') || 'Unknown',
            email: 'N/A',
            phone: 'N/A',
            student_id: studentId
          };
          console.warn('Could not fetch complete profile information');
        }

        // Store original values for cancellation
        this.originalProfile = { ...this.profile };
      } catch (error) {
        console.error('Error loading profile data:', error);
        // Set basic profile info even if API fails
        const studentId = localStorage.getItem('userId');
        this.profile = {
          name: localStorage.getItem('username') || 'Unknown',
          email: 'N/A',
          phone: 'N/A',
          student_id: studentId || ''
        };
        this.originalProfile = { ...this.profile };
        this.showMessage('error', 'Failed to load profile data.');
      }
    },
    
    enableEditing() {
      this.isEditing = true;
    },
    
    cancelEditing() {
      // Restore original values
      this.profile = { ...this.originalProfile };
      this.isEditing = false;
      this.clearMessage();
    },
    
    async updateProfile() {
      try {
        // Get student ID from localStorage
        const studentId = localStorage.getItem('userId');
        if (!studentId) {
          console.error('No student ID found');
          this.showMessage('error', 'User not authenticated. Please login again.');
          return;
        }

        // Prepare update data
        const updateData = {
          student_id: studentId,
          name: this.profile.name,
          email: this.profile.email,
          phone: this.profile.phone
        };

        // Call backend API to update profile information
        const response = await fetch('http://127.0.0.1:8000/api/update-reader-information', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(updateData)
        });

        const data = await response.json();

        if (response.ok) {
          // Show success message
          this.showMessage('success', 'Profile updated successfully!');

          // Exit editing mode
          this.isEditing = false;

          // Update original values
          this.originalProfile = { ...this.profile };

          // Update username in localStorage
          localStorage.setItem('username', this.profile.name);

          // Clear message after 3 seconds
          setTimeout(() => {
            this.clearMessage();
          }, 3000);
        } else {
          this.showMessage('error', data.detail || 'Failed to update profile.');
        }
      } catch (error) {
        console.error('Error updating profile:', error);
        this.showMessage('error', 'Network error. Failed to update profile.');
      }
    },
    
    goBack() {
      this.$emit('back-to-home');
    },
    
    showMessage(type, text) {
      this.message = { type, text };
    },
    
    clearMessage() {
      this.message = null;
    }
  }
}
</script>

<style scoped>
.profile-edit-container {
  min-height: 100vh;
  padding: 40px 20px;
  background: rgba(0, 0, 0, 0.4);
  color: white;
}

.profile-header {
  max-width: 1200px;
  margin: 0 auto 30px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.profile-header h1 {
  flex: 1;
  text-align: center;
  font-size: 28px;
  margin: 0;
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

.profile-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  gap: 50px;
  min-height: 60vh;
}

.profile-left {
  flex: 0 0 500px;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.avatar-section {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.avatar {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}

.change-avatar-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
}

.calendar-section {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 20px;
}

.profile-right {
  flex: 1;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 30px;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-input {
  padding: 15px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(0, 0, 0, 0.3);
  color: white;
  font-size: 16px;
}

.form-input:disabled {
  background: rgba(0, 0, 0, 0.2);
  color: rgba(255, 255, 255, 0.6);
  cursor: not-allowed;
}

.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 20px;
}

.edit-btn, .save-btn, .cancel-btn {
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  font-size: 16px;
  cursor: pointer;
  flex: 1;
}

.edit-btn {
  background: rgba(52, 152, 219, 0.7);
  color: white;
}

.save-btn {
  background: rgba(46, 204, 113, 0.7);
  color: white;
}

.cancel-btn {
  background: rgba(231, 76, 60, 0.7);
  color: white;
}

.message {
  margin-top: 20px;
  padding: 12px;
  border-radius: 8px;
  text-align: center;
  font-weight: 500;
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

@media (max-width: 900px) {
  .profile-content {
    flex-direction: column;
  }
  
  .profile-left {
    flex: none;
  }
}
</style>