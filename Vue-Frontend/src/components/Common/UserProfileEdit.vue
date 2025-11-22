<template>
  <div class="user-profile-edit-container">
    <div class="profile-header">
      <button class="back-btn" @click="goBack">← Back to Home</button>
      <h1>Edit Profile</h1>
    </div>
    
    <div class="profile-content">
      <div class="profile-left">
        <!-- Avatar section -->
        <div class="avatar-section">
          <img :src="avatarSrc" :alt="`${userRole} Avatar`" class="avatar" />
          <button class="change-avatar-btn">Change Avatar</button>
        </div>
      </div>
      
      <div class="profile-right">
        <!-- Profile form -->
        <form class="profile-form" @submit.prevent="updateProfile">
          <div class="form-group">
            <label>ID</label>
            <input 
              type="text" 
              v-model="profile.id" 
              :disabled="!isEditing"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label>Name</label>
            <input 
              type="text" 
              v-model="profile.name" 
              :disabled="!isEditing"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label>Email</label>
            <input 
              type="email" 
              v-model="profile.email" 
              :disabled="!isEditing"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label>Phone</label>
            <input 
              type="tel" 
              v-model="profile.phone" 
              :disabled="!isEditing"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label>Department</label>
            <input 
              type="text" 
              v-model="profile.department" 
              :disabled="!isEditing"
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
import librarianAvatar from '../../assets/librarian_avatar.png';
import directorAvatar from '../../assets/librarian_avatar.png';

export default {
  name: 'UserProfileEdit',
  props: {
    userRole: {
      type: String,
      required: true
    }
  },
  emits: ['back-to-home'],
  data() {
    return {
      avatarSrc: this.getUserAvatar(),
      isEditing: false,
      profile: {
        id: '',
        name: '',
        email: '',
        phone: '',
        department: ''
      },
      originalProfile: {}, // Store original values for cancel
      message: null
    }
  },
  mounted() {
    this.loadProfileData();
  },
  methods: {
    getUserAvatar() {
      if (this.userRole === 'librarian') {
        return librarianAvatar;
      } else if (this.userRole === 'director') {
        return directorAvatar;
      } else {
        // Default avatar
        return librarianAvatar;
      }
    },
    
    async loadProfileData() {
      try {
        // Get user ID from localStorage based on role
        const userId = localStorage.getItem('userId');
        if (!userId) {
          console.error('No user ID found');
          this.showMessage('error', 'User not authenticated. Please login again.');
          return;
        }
        
        // Set the user ID from localStorage
        this.profile.id = userId;
        
        // Call API to get profile information
        if (this.userRole === 'librarian' || this.userRole === 'director') {
          const response = await fetch(
            `http://127.0.0.1:8000/api/librarian-director-information?admin_id=${encodeURIComponent(userId)}&role=${this.userRole}`
          );
          
          if (response.ok) {
            const data = await response.json();
            const info = data.information;
            
            this.profile.name = info.name || '';
            this.profile.email = info.email || '';
            this.profile.phone = info.phone || '';
            this.profile.department = this.userRole === 'librarian' ? 'Library Services' : 'Library Administration';
          } else {
            // If API fails, use localStorage values as fallback
            this.profile.name = localStorage.getItem('username') || '';
            this.profile.email = '';
            this.profile.phone = '';
            this.profile.department = this.userRole === 'librarian' ? 'Library Services' : 'Library Administration';
          }
        } else {
          // For other roles, use placeholder values
          this.profile.name = localStorage.getItem('username') || '';
          this.profile.email = '';
          this.profile.phone = '';
          this.profile.department = '';
        }
        
        // Store original values for cancellation
        this.originalProfile = { ...this.profile };
      } catch (error) {
        console.error('Error loading profile data:', error);
        this.showMessage('error', 'Failed to load profile data.');
        // Use localStorage as fallback
        this.profile.name = localStorage.getItem('username') || '';
        this.profile.email = '';
        this.profile.phone = '';
        this.profile.department = '';
        this.originalProfile = { ...this.profile };
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
        // Only update for librarian and director roles
        if (this.userRole !== 'librarian' && this.userRole !== 'director') {
          this.showMessage('error', 'Profile update is only available for librarians and directors.');
          return;
        }

        const userId = localStorage.getItem('userId');
        if (!userId) {
          this.showMessage('error', 'User not authenticated. Please login again.');
          return;
        }

        // Prepare update data
        const updateData = {
          admin_id: userId,
          role: this.userRole
        };

        // Only include fields that have been changed (compare with original values)
        if (this.profile.name !== this.originalProfile.name) {
          updateData.name = this.profile.name || null;
        }
        if (this.profile.email !== this.originalProfile.email) {
          updateData.email = this.profile.email || null;
        }
        if (this.profile.phone !== this.originalProfile.phone) {
          updateData.phone = this.profile.phone || null;
        }

        // Check if there are any changes
        const hasChanges = updateData.hasOwnProperty('name') || 
                          updateData.hasOwnProperty('email') || 
                          updateData.hasOwnProperty('phone');
        
        if (!hasChanges) {
          this.showMessage('error', 'No changes to save.');
          return;
        }

        // Call API to update profile
        const response = await fetch('http://127.0.0.1:8000/api/update-librarian-director-information', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(updateData)
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
          // Show success message
          this.showMessage('success', 'Profile updated successfully!');
          
          // Update localStorage username if name changed
          if (updateData.name) {
            localStorage.setItem('username', updateData.name);
          }
          
          // Exit editing mode
          this.isEditing = false;
          
          // Update original values
          this.originalProfile = { ...this.profile };
          
          // Clear message after 3 seconds
          setTimeout(() => {
            this.clearMessage();
          }, 3000);
        } else {
          this.showMessage('error', data.detail || 'Failed to update profile.');
        }
      } catch (error) {
        console.error('Error updating profile:', error);
        this.showMessage('error', 'Failed to update profile. Please try again.');
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
.user-profile-edit-container {
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
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 40px;
  min-height: 60vh;
}

.profile-left {
  flex: 0 0 300px;
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
  width: 180px;
  height: 180px;
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
  width: 100%;
  text-align: center;
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
  text-align: center;
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