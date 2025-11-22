<template>
  <div class="reader-home-container">
    <div class="content">
      <!-- 左半边 -->
      <div class="left-panel">
        <!-- 用户头像和问候 -->
        <div class="user-section">
          <div class="avatar-container">
            <img
              id="user-avatar"
              class="avatar"
              :src="avatarSrc"
              alt="Avatar"
              style="display: none;"
              onerror="this.style.display='none'; document.getElementById('avatar-placeholder').style.display='flex';"
              onload="this.style.display='block'; document.getElementById('avatar-placeholder').style.display='none';"
            >
            <div id="avatar-placeholder" class="avatar-placeholder">👤</div>
          </div>
          <div class="greeting">Hi, <span id="user-name">{{ greetingName }}</span> ^^</div>
        </div>

        <!-- 阅读日历 -->
        <ReadingCalendar />

        <!-- 读书报告 -->
        <div class="reading-report">
          <div class="report-text" id="report-text" v-html="readingReport"></div>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <button class="action-btn" @click="navigateTo('borrowings')">Manage My Borrowings</button>
          <button class="action-btn" @click="navigateTo('profile')">edit my information</button>
          <button class="action-btn" @click="handleLogout">Log Out</button>
        </div>
      </div>

      <!-- 右半边 -->
      <div class="right-panel">
        <div class="search-section">
          <input type="text" class="search-input" id="search-input" placeholder="searching for books...."
                 v-model="searchQuery"
                 @keypress="handleSearchKeyPress">
          <button class="search-btn" @click="performSearch">Search</button>
        </div>

        <!-- Search Results Section -->
        <div v-if="searchResults.length > 0" class="search-results">
          <div
            v-for="book in searchResults"
            :key="book.book_id"
            class="book-card"
          >
            <img :src="coverImage" alt="Book Cover" class="book-cover" />
            <div class="book-info">
              <h3>{{ book.book_name }}</h3>
              <p><strong>Author:</strong> {{ book.author }}</p>
              <p><strong>Publisher:</strong> {{ book.publisher }}</p>
            </div>
            <div class="book-actions">
              <button @click="selectBook(book)" class="view-details-btn">view details</button>
            </div>
          </div>
        </div>

        <!-- No Search Results -->
        <div v-else-if="showNoResults" class="no-results">
          No search results
        </div>

      </div>
    </div>
  </div>
</template>

<script>
  import defaultAvatar from '../../assets/default_avatar1.png'
  import coverImage from '../../assets/cover.png'
  import ReadingCalendar from './Calendar/ReadingCalendar.vue'

export default {
  name: 'ReaderHome',
  components: {
    ReadingCalendar
  },
  emits: ['logout', 'view-book-detail', 'view-my-borrowings', 'view-profile-edit'], // 添加查看借阅和资料编辑事件
  data() {
    return {
      greetingName: 'Luoyin',  // 默认用户名
      avatarSrc: defaultAvatar,
      coverImage: coverImage,
      searchQuery: '',
      searchResults: [],
      showNoResults: false,
      readingReport: 'Loading reading insights...'
    }
  },
  mounted() {
    this.loadUserInfo();
    this.loadReadingReport();
  },
  methods: {

    // 加载用户信息
    loadUserInfo() {
      // 从localStorage获取用户姓名，这是在登录成功后存储的
      const username = localStorage.getItem('username');
      if (username) {
        this.greetingName = username;
      } else {
        this.greetingName = 'Luoyin';
      }
    },

    // 加载读书报告
    async loadReadingReport() {
      try {
        const userId = localStorage.getItem('userId');
        if (!userId) {
          console.error('No user ID found');
          this.readingReport = 'Unable to load reading report. Please login again.';
          return;
        }

        const response = await fetch(`http://127.0.0.1:8000/api/reader-reading-report?student_id=${encodeURIComponent(userId)}`);
        if (!response.ok) {
          throw new Error(`Request failed with status ${response.status}`);
        }

        const data = await response.json();

        if (Array.isArray(data?.reports) && data.reports.length > 0) {
          this.readingReport = data.reports.join('<br><br>');
        } else if (Array.isArray(data)) {
          this.readingReport = data.join('<br><br>');
        } else if (typeof data === 'string') {
          this.readingReport = data;
        } else {
          this.readingReport = 'please read more books';
        }
      } catch (error) {
        console.error('Error loading reading report:', error);
        this.readingReport = 'Error loading reading report.';
      }
    },

    // 搜索功能
    handleSearchKeyPress(event) {
      if (event.key === 'Enter') {
        const query = document.getElementById('search-input').value.trim();
        if (query) {
          // 在实际应用中，这里会导航到搜索结果页面
          console.log(`Searching for: ${query}`);
        }
      }
    },
    
    // 导航到其他页面
    navigateTo(page) {
      switch(page) {
        case 'borrowings':
          // 发射事件到父组件，切换到借阅页面
          this.$emit('view-my-borrowings');
          break;
        case 'profile':
          // 发射事件到父组件，切换到个人信息编辑页面
          this.$emit('view-profile-edit');
          break;
      }
    },

    // 处理登出
    handleLogout() {
      // 触发登出事件，由父组件处理
      this.$emit('logout');
    },

    // 执行搜索
    async performSearch() {
      if (!this.searchQuery.trim()) {
        this.searchResults = [];
        this.showNoResults = false;
        this.selectedBook = null;
        return;
      }

      try {
        const response = await fetch(`http://127.0.0.1:8000/api/search-books?query=${encodeURIComponent(this.searchQuery)}`);
        const data = await response.json();

        if (data.books && data.books.length > 0) {
          this.searchResults = data.books;
          this.showNoResults = false;
        } else {
          this.searchResults = [];
          this.showNoResults = true;
        }
        this.selectedBook = null;
      } catch (error) {
        console.error('Search error:', error);
        this.searchResults = [];
        this.showNoResults = true;
      }
    },

    // 处理搜索框按键事件
    handleSearchKeyPress(event) {
      if (event.key === 'Enter') {
        this.performSearch();
      }
    },

    // 选择书籍以查看详情
    selectBook(book) {
      this.$emit('view-book-detail', book);
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
  overflow-x: hidden;
  position: relative;
  color: white;
}

.content {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  display: flex;
  padding: 40px;
  gap: 40px;
}

/* 左半边 - 读者信息 */
.left-panel {
  flex: 0 0 600px;  /* 增加宽度 */
  display: flex;
  flex-direction: column;
  gap: 25px;  /* 增加间距 */
}

/* 用户头像和问候 */
.user-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  padding: 20px 0;
}

.avatar-container {
  position: relative;
}

.avatar {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 50px;
}

.greeting {
  font-size: 24px;
  font-weight: 500;
  color: white; /* 设置为白色 */
}

/* 日历视图 */
.calendar-card {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  padding: 30px;  /* 增加内边距 */
  color: #333;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.calendar-title {
  font-size: 18px;
  font-weight: 600;
  color: #000000;
}

.calendar-legend {
  display: flex;
  gap: 15px;
  font-size: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.legend-square {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.legend-less {
  background: #d3d3d3;
}

.legend-mid {
  background: #808080;
}

.legend-more {
  background: #2f2f2f;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 3px;
  margin-bottom: 10px;
}

.month-column {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.month-label {
  font-size: 11px;
  color: #000000;
  margin-bottom: 5px;
  text-align: center;
}

.day-squares {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 3px;
}

.day-square {
  width: 11px;
  height: 11px;
  border-radius: 2px;
  background: #d3d3d3;
}

.day-square.mid {
  background: #808080;
}

.day-square.more {
  background: #2f2f2f;
}

/* 读书报告 */
.reading-report {
  background: rgba(40, 40, 40, 0.8);
  border-radius: 12px;
  padding: 30px;  /* 增加内边距 */
  font-size: 15px;  /* 增加字体大小 */
  line-height: 1.8;
}

.report-text {
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 10px;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  flex-direction: row;
  gap: 12px;
}

.action-btn {
  background: rgba(40, 40, 40, 0.3);
  background-image: url('@/assets/button-bg.png');
  background-size: cover;
  background-position: center;
  color: white;
  border: none;
  padding: 18px 20px;  /* 增加按钮高度 */
  border-radius: 8px;
  font-size: 15px;    /* 增加字体大小 */
  cursor: pointer;
  transition: opacity 0.3s;
  text-align: left;
  flex: 1;
}

.action-btn:hover {
  opacity: 0.7;
}

/* 右半边 - 搜索区域 */
.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.search-section {
  background: rgba(40, 40, 40, 0.8);
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-input {
  flex: 1;
  padding: 15px 20px;
  background: rgba(60, 60, 60, 0.8);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: white;
  font-size: 16px;
}

.search-btn {
  padding: 15px 20px;
  border-radius: 8px;
  border: none;
  background: rgba(40, 40, 40, 0.3);
  background-image: url('@/assets/button-bg.png');
  background-size: cover;
  background-position: center;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: opacity 0.3s;
  white-space: nowrap;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.search-input:focus {
  outline: none;
  border-color: rgba(255, 255, 255, 0.5);
}

.search-btn {
  padding: 15px 20px;
  border-radius: 8px;
  border: none;
  background: rgba(40, 40, 40, 0.3);
  background-image: url('@/assets/button-bg.png');
  background-size: cover;
  background-position: center;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.search-btn:hover {
  opacity: 0.7;
}

.search-results {
  margin-top: 20px;
  max-height: 60vh;
  overflow-y: auto;
}

.book-card {
  display: flex;
  gap: 15px;
  padding: 15px;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 8px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: background 0.3s;
}

.book-card:hover {
  background: rgba(60, 60, 60, 0.5);
}

.book-cover {
  width: 60px;
  height: 80px;
  border-radius: 4px;
  object-fit: cover;
}

.book-info h3 {
  margin-bottom: 8px;
  color: white;
}

.book-info p {
  margin-bottom: 4px;
  font-size: 14px;
  color: white;
}

.book-actions {
  display: flex;
  flex-direction: column;
  gap: 5px;
  min-width: 100px;
}

.view-details-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
}

.no-results {
  text-align: center;
  padding: 40px 0;
  font-size: 18px;
  color: rgba(255, 255, 255, 0.7);
}

.book-detail {
  margin-top: 20px;
  padding: 20px;
  background: rgba(40, 40, 40, 0.3);
  border-radius: 8px;
}

.book-detail h3 {
  margin-bottom: 15px;
  font-size: 20px;
}

.book-detail p {
  margin-bottom: 10px;
  line-height: 1.5;
}

.borrow-btn, .back-btn {
  margin-top: 15px;
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  background: rgba(40, 40, 40, 0.3);
  background-image: url('@/assets/button-bg.png');
  background-size: cover;
  background-position: center;
  color: white;
  cursor: pointer;
  transition: opacity 0.3s;
  margin-right: 10px;
}

.borrow-btn:hover, .back-btn:hover {
  opacity: 0.7;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .content {
    flex-direction: column;
  }

  .left-panel {
    flex: 1;
  }
}
</style>