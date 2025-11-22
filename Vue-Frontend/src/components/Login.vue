<template>
  <div class="login-container">
    <div class="page">
      <div class="card">
        <div class="title">Choose Your Identity</div>

        <div class="role-tabs">
          <button
            class="role-tab"
            :class="{ active: currentRole === 'reader' }"
            @click="selectRole('reader')"
          >
            Reader
          </button>
          <button
            class="role-tab"
            :class="{ active: currentRole === 'librarian' }"
            @click="selectRole('librarian')"
          >
            Librarian
          </button>
          <button
            class="role-tab"
            :class="{ active: currentRole === 'director' }"
            @click="selectRole('director')"
          >
            Library Director
          </button>
        </div>

        <div class="form">
          <div class="form-group">
            <label id="id-label">ID</label>
            <input 
              type="text" 
              id="user-id"
              v-model="userId" 
              :placeholder="idPlaceholder"
            >
          </div>
          <div class="form-group">
            <label>Password</label>
            <input 
              type="password" 
              id="password"
              v-model="password" 
              placeholder="Enter your password"
            >
          </div>
        </div>

        <div class="actions">
          <button
            class="btn btn-login"
            @click="handleLogin"
          >
            LOG IN
          </button>
          <button
            class="btn btn-secondary"
            id="signup-btn"
            @click="handleSignup"
            :disabled="currentRole !== 'reader'"
          >
            LOG UP
          </button>
        </div>

        <!-- Login status message -->
        <div v-if="loginMessage" :class="['login-message', loginMessageType]">
          {{ loginMessage }}
        </div>

        <div class="hint" id="hint-text">{{ hintText }}</div>
      </div>
    </div>
  </div>

  <!-- Registration Modal -->
  <div v-if="showRegistration" class="modal-overlay" @click="closeRegistration">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>Reader Registration</h2>
        <button class="close-btn" @click="closeRegistration">&times;</button>
      </div>

      <form @submit.prevent="registerReader" class="register-form">
        <div class="form-group">
          <label>Student ID (9 digits)</label>
          <input
            type="text"
            v-model="registerData.studentId"
            placeholder="Enter 9-digit student ID"
            maxlength="9"
            required
          >
        </div>

        <div class="form-group">
          <label>Password</label>
          <input
            type="password"
            v-model="registerData.password"
            placeholder="Enter password"
            required
          >
        </div>

        <div class="form-group">
          <label>Confirm Password</label>
          <input
            type="password"
            v-model="registerData.confirmPassword"
            placeholder="Confirm password"
            required
          >
        </div>

        <div v-if="registerMessage" class="register-message" :class="registerMessage.type">
          {{ registerMessage.text }}
        </div>

        <button type="submit" class="btn btn-register" :disabled="registerData.submitting">
          {{ registerData.submitting ? 'Registering...' : 'Register' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import P5Background from './Common/P5Background.vue';

export default {
  name: 'Login',
  components: {
    P5Background
  },
  emits: ['login-success'], // 定义组件事件
  data() {
    return {
      currentRole: 'reader',
      userId: '',
      password: '',
      loginMessage: null,
      loginMessageType: '', // 'success' or 'error'
      showRegistration: false,
      registerData: {
        studentId: '',
        password: '',
        confirmPassword: '',
        submitting: false
      },
      registerMessage: null
    }
  },
  computed: {
    idPlaceholder() {
      if (this.currentRole === 'reader') {
        return 'Enter your Student ID';
      } else if (this.currentRole === 'librarian') {
        return 'Enter your Librarian ID';
      } else {
        return 'Enter your Director ID';
      }
    },
    hintText() {
      if (this.currentRole === 'reader') {
        return 'Readers can login or register for a new account.';
      } else if (this.currentRole === 'librarian') {
        return 'For Librarian, Registration is disabled. Ask the directior for a new account.';
      } else {
        return ' ';
      }
    }
  },
  methods: {
    selectRole(role) {
      this.currentRole = role;
      this.updateRoleUI();
    },
    updateRoleUI() {
      // Update the disabled state based on role
      // This is handled by the disabled attribute in the template
    },
    async handleLogin() {
      // First, try actual API call
      try {
        const response = await fetch('http://127.0.0.1:8000/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            id: this.userId,
            password: this.password,
            identity: this.currentRole
          })
        });

        const result = await response.json();

        if (response.ok) {
          alert(result.message);
          // Store user data and redirect based on role
          localStorage.setItem('userToken', result.token);
          localStorage.setItem('userRole', this.currentRole);
          localStorage.setItem('userId', this.userId); // Store the actual user ID

          // Redirect to appropriate dashboard based on role
          this.redirectBasedOnRole(result);
        } else {
          alert(result.message || 'Login failed');
        }
      } catch (error) {
        console.error('Login error:', error);
        // Fallback to original behavior if backend is not running
        alert(`Logging in as ${this.currentRole} with ID: ${this.userId}\n(Backend not accessible, using fallback)`);
      }
    },
    async handleLogin() {
      // Try actual API call
      try {
        const response = await fetch('http://127.0.0.1:8000/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            id: this.userId,
            password: this.password,
            identity: this.currentRole
          })
        });

        const result = await response.json();

        if (response.ok) {
          // Login successful
          // Store user data and emit success event
          localStorage.setItem('userToken', result.token);
          localStorage.setItem('userRole', result.role);  // 使用返回的角色，而不是当前选择的角色
          localStorage.setItem('userId', result.user_id); // Store the actual user ID from the response

          // 使用用户返回的全名作为用户名存储
          localStorage.setItem('username', result.full_name || result.user_id);

          // Set success message
          this.loginMessage = result.message;
          this.loginMessageType = 'success';

          // Emit login success event to parent component with the confirmed role immediately
          this.$emit('login-success', result.role);
        } else {
          // Login failed
          // Set error message
          this.loginMessage = result.detail || result.message || 'Login failed';
          this.loginMessageType = 'error';
        }
      } catch (error) {
        console.error('Login error:', error);
        // Fallback to original behavior if backend is not running
        this.loginMessage = `Error: ${error.message}`;
        this.loginMessageType = 'error';
      }
    },
    selectRole(role) {
      this.currentRole = role;
      this.updateRoleUI();
    },
    updateRoleUI() {
      // This method updates UI based on role, but since we're using Vue reactivity,
      // the template will automatically update based on computed properties
    },
    clearLoginMessage() {
      this.loginMessage = null;
      this.loginMessageType = '';
    },
    handleSignup() {
      if (this.currentRole === 'reader') {
        this.showRegistration = true;
      }
    },

    closeRegistration() {
      this.showRegistration = false;
      this.registerData = {
        studentId: '',
        password: '',
        confirmPassword: '',
        submitting: false
      };
      this.registerMessage = null;
    },

    async registerReader() {
      // Validate inputs
      if (this.registerData.password !== this.registerData.confirmPassword) {
        this.registerMessage = {
          type: 'error',
          text: 'Passwords do not match'
        };
        return;
      }

      if (this.registerData.studentId.length !== 9) {
        this.registerMessage = {
          type: 'error',
          text: 'Student ID must be 9 digits'
        };
        return;
      }

      this.registerData.submitting = true;
      this.registerMessage = null;

      try {
        const response = await fetch(`http://127.0.0.1:8000/api/reader-log-up?student_id=${encodeURIComponent(this.registerData.studentId)}&password=${encodeURIComponent(this.registerData.password)}`, {
          method: 'GET'
        });

        const data = await response.json();

        if (response.ok) {
          this.registerMessage = {
            type: 'success',
            text: 'Registration successful! You can now login.'
          };

          // Clear form after successful registration
          setTimeout(() => {
            this.closeRegistration();
          }, 2000);
        } else {
          // Check if the error is about duplicate ID
          if (data.detail && data.detail.toLowerCase().includes('already')) {
            this.registerMessage = {
              type: 'error',
              text: 'This ID already has an account'
            };
          } else {
            this.registerMessage = {
              type: 'error',
              text: data.detail || 'Registration failed'
            };
          }
        }
      } catch (error) {
        console.error('Registration error:', error);
        this.registerMessage = {
          type: 'error',
          text: 'Network error. Please try again.'
        };
      } finally {
        this.registerData.submitting = false;
      }
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  color: white;
  overflow: hidden;
}

.login-container {
  position: relative;
  min-height: 100vh;
}

.page {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.card {
  width: 680px;
  border-radius: 28px;
  padding: 50px 60px;
  background: rgba(255, 255, 255, 0.1); /* 降低透明度 */
  backdrop-filter: blur(10px);

}

.login-message {
  margin-top: 15px;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  text-align: center;
}

.login-message.success {
  background: rgba(46, 204, 113, 0.3);
  border: 1px solid rgba(46, 204, 113, 0.5);
  color: #2ecc71;
}

.login-message.error {
  background: rgba(231, 76, 60, 0.3);
  border: 1px solid rgba(231, 76, 60, 0.5);
  color: #e74c3c;
}

.title {
  font-size: 28px;
  margin-bottom: 30px;
  letter-spacing: 1px;
  color: white; /* 设置为白色 */
}

.role-tabs {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
}

.role-tab {
  flex: 1;
  padding: 14px 0;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid transparent;
  color: rgba(255, 255, 255, 0.8);
  font-size: 15px;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: all 0.3s;
}

.role-tab.active {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.4);
  color: #fff;
}

.form-group {
  margin-bottom: 24px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  letter-spacing: 0.3px;
}

input {
  width: 100%;
  padding: 14px 16px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.25);
  background: rgba(0, 0, 0, 0.35);
  color: white;
  font-size: 15px;
}

input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.actions {
  display: flex;
  gap: 20px;
  margin-top: 30px;
}

.btn {
  flex: 1;
  padding: 14px 0;
  border-radius: 12px;
  border: none;
  font-size: 15px;
  letter-spacing: 0.8px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.btn-login {
  background: rgba(255, 255, 255, 0.85);
  color: #333;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.4);
  color: #fff;
}

.btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.hint {
  margin-top: 18px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  letter-spacing: 0.3px;
}

/* Registration Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.modal-content {
  width: 450px;
  max-width: 90%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 30px;
  position: relative;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h2 {
  margin: 0;
  color: white;
  font-size: 24px;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.register-form .form-group {
  margin-bottom: 0;
}

.register-form input {
  width: 100%;
  padding: 14px 16px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.25);
  background: rgba(0, 0, 0, 0.35);
  color: white;
  font-size: 15px;
}

.register-form input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.btn-register {
  padding: 14px 0;
  border-radius: 12px;
  border: none;
  background: rgba(255, 255, 255, 0.85);
  color: #333;
  font-size: 15px;
  letter-spacing: 0.8px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.btn-register:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.register-message {
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  text-align: center;
  margin-top: 10px;
  margin-bottom: 10px;
}

.register-message.success {
  background: rgba(46, 204, 113, 0.3);
  border: 1px solid rgba(46, 204, 113, 0.5);
  color: #2ecc71;
}

.register-message.error {
  background: rgba(231, 76, 60, 0.3);
  border: 1px solid rgba(231, 76, 60, 0.5);
  color: #e74c3c;
}
</style>