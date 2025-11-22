<template>
  <div class="librarian-home-container">
    <div class="content">
      <!-- 侧边栏 - 总是显示 -->
      <div class="sidebar">
        <img :src="avatarSrc" alt="Librarian Avatar" class="avatar" />
        <h2>Hi, {{ username }} ^^</h2>
        <button @click="viewReport">view library report</button>
        <button @click="editProfile">edit my information</button>
        <button @click="handleLogout">Log Out</button>
      </div>

      <!-- 主内容区域 - 根据状态显示不同内容 -->
      <div class="main" v-if="!showLibraryReport">
        <div class="nav">
          <button
            :class="['nav-btn', { active: activeTab === 'manage-books' }]"
            @click="switchTab('manage-books')"
          >
            Manage Books
          </button>
          <button
            :class="['nav-btn', { active: activeTab === 'manage-readers' }]"
            @click="switchTab('manage-readers')"
          >
            Manage Readers
          </button>
        </div>

        <div v-if="activeTab === 'manage-books'">
          <!-- Search bar for books -->
          <div class="search-row">
            <input
              type="text"
              class="search-input"
              placeholder="searching for books...."
              v-model="searchQuery"
              @keypress="handleSearchKeyPress"
            />
            <button class="search-btn" @click="performSearch">Search</button>
          </div>

          <!-- Books list and add panel -->
          <div class="books-wrapper">
            <!-- Search Results Section -->
            <div v-if="searchResults.length > 0" class="book-list">
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
                  <button class="view-details-btn" @click="selectBook(book)">view details</button>
                </div>
              </div>
            </div>

            <!-- No Search Results -->
            <div v-else-if="showNoResults" class="no-results">
              No search results
            </div>

            <!-- Default book list if no search has been performed -->
            <div v-else class="book-list">
              <div
                v-for="book in books"
                :key="book.book_id"
                class="book-card"
              >
                <img :src="coverImage" alt="Book Cover" class="book-cover" />
                <div class="book-info">
                  <h3>{{ book.book_name }}</h3>
                  <p><strong>Author:</strong> {{ book.author }}</p>
                  <p><strong>ISBN:</strong> {{ book.isbn }}</p>
                  <p><strong>Status:</strong> {{ book.status }}</p>
                  <p><strong>Location:</strong> {{ book.location }}</p>
                </div>
                <div class="book-actions">
                  <button class="view-details-btn" @click="selectBook(book)">view details</button>
                </div>
              </div>
            </div>

            <!-- Add Book Panel -->
            <div class="add-panel">
              <h3>Add Book</h3>
            <div class="form-group">
              <label>Book Name</label>
              <input type="text" v-model="newBook.title" placeholder="Book name">
            </div>
            <div class="form-group">
              <label>Author</label>
              <input type="text" v-model="newBook.author" placeholder="Author">
            </div>
            <div class="form-group">
              <label>Publisher</label>
              <input type="text" v-model="newBook.publisher" placeholder="Publisher">
            </div>
            <div class="form-group">
              <label>Publish Year</label>
              <input type="text" v-model="newBook.publishYear" placeholder="Publish year">
            </div>
            <div class="form-group">
              <label>Location</label>
              <input type="text" v-model="newBook.location" placeholder="Location">
            </div>
              <button @click="addNewBook">Add Book</button>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'manage-readers'">
          <!-- Search bar for readers -->
          <div class="search-row">
            <input
              type="text"
              class="search-input"
              placeholder="search for readers..."
              v-model="searchQuery"
              @keypress="handleSearchKeyPress"
            />
            <button class="search-btn" @click="performSearch">Search</button>
          </div>

          <div class="readers-wrapper">
            <!-- Search Results Section -->
            <div v-if="searchResults.length > 0" class="reader-list">
              <div
                v-for="reader in searchResults"
                :key="reader.id"
                class="reader-card"
              >
                <div class="reader-avatar">
                  <img :src="readerAvatarSrc" alt="Reader Avatar" class="reader-avatar-img" />
                </div>
                <div class="reader-info">
                  <h3>{{ reader.name }}</h3>
                  <p><strong>Email:</strong> {{ reader.email }}</p>
                  <p><strong>Phone:</strong> {{ reader.phone }}</p>
                </div>
                <div class="reader-actions">
                  <button class="view-details-btn" @click="selectReader(reader)">view details</button>
                </div>
              </div>
            </div>

            <!-- No Search Results -->
            <div v-else-if="showNoResults" class="no-results">
              No search results
            </div>

            <!-- Default reader list if no search has been performed -->
            <div v-else class="reader-list">
              <div
                v-for="reader in readers"
                :key="reader.id"
                class="reader-card"
              >
                <div class="reader-avatar">
                  <img :src="readerAvatarSrc" alt="Reader Avatar" class="reader-avatar-img" />
                </div>
                <div class="reader-info">
                  <h3>{{ reader.name }}</h3>
                  <p><strong>Email:</strong> {{ reader.email }}</p>
                  <p><strong>Phone:</strong> {{ reader.phone }}</p>
                </div>
                <div class="reader-actions">
                  <button class="view-details-btn" @click="selectReader(reader)">view details</button>
                </div>
              </div>
            </div>

            <!-- Add Reader Panel -->
            <div class="add-panel">
              <h3>Add Reader</h3>
              <div class="form-group">
                <label>Reader ID</label>
                <input type="text" v-model="newReader.id" placeholder="ID">
              </div>
              <div class="form-group">
                <label>Name</label>
                <input type="text" v-model="newReader.name" placeholder="Full name">
              </div>
              <div class="form-group">
                <label>Email</label>
                <input type="email" v-model="newReader.email" placeholder="Email address">
              </div>
              <div class="form-group">
                <label>Phone</label>
                <input type="text" v-model="newReader.phone" placeholder="Phone number">
              </div>
              <div class="form-group">
                <label>Password</label>
                <input type="password" v-model="newReader.password" placeholder="Password">
              </div>
            <div class="form-group">
              <label>Department</label>
              <input type="text" v-model="newReader.department" placeholder="Department">
            </div>
            <div class="form-group">
              <label>Major</label>
              <input type="text" v-model="newReader.major" placeholder="Major">
            </div>
              <button @click="addReader">Add Reader</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Library Report View - Replaces the main content area when active -->
      <div v-else-if="showLibraryReport" class="report-content">
        <LibraryReport
          @back="handleReportBack"
        />
      </div>
    </div>
  </div>
</template>

<script>
import librarianAvatar from '../../assets/librarian_avatar.png';
import ReaderAvatar from '../../assets/default_avatar1.png';
import coverImage from '../../assets/cover.png';
import LibraryReport from '../Common/LibraryReport.vue';

export default {
  name: 'LibrarianHome',
  emits: ['logout', 'view-book-detail', 'view-reader-detail', 'view-profile-edit', 'navigate-to-report'],
  components: {
    LibraryReport
  },
  data() {
    return {
      username: 'Luoyin', // Default username
      avatarSrc: librarianAvatar,
      readerAvatarSrc: ReaderAvatar,
      coverImage: coverImage,
      activeTab: 'manage-books', // Default to manage books
      books: [],
      readers: [],
      newBook: {
        title: '',
        author: '',
        publisher: '',
        publishYear: '',
        location: '',
        ifAvailable: 1  // 默认可用
      },
      newReader: {
        id: '',
        name: '',
        email: '',
        phone: '',
        password: '',
        department: '',
        major: ''
      },
      searchQuery: '',
      searchResults: [],
      showNoResults: false,
      selectedBook: null,
      showAddReaderForm: false,
      selectedReader: null,
      showLibraryReport: false // To control showing the library report view
    }
  },
  mounted() {
    this.loadUserInfo();
  },
  methods: {
    // 加载用户信息
    loadUserInfo() {
      const username = localStorage.getItem('username');
      if (username) {
        this.username = username;
      }
    },
    
    viewReport() {
      console.log('viewReport clicked');
      this.showLibraryReport = true;
      console.log('showLibraryReport set to:', this.showLibraryReport);
    },
    
    editProfile() {
      this.$emit('view-profile-edit');
    },
    
    switchTab(tabName) {
      this.activeTab = tabName;
    },
    
    handleLogout() {
      this.$emit('logout');
    },

    handleReportBack() {
      this.showLibraryReport = false;
    },
    
    // Add new book
    async addNewBook() {
      if (!this.newBook.title || !this.newBook.author) {
        alert('Please fill in at least Book Name and Author');
        return;
      }

      try {
        const params = new URLSearchParams({
          book_name: this.newBook.title,
          author: this.newBook.author,
          publisher: this.newBook.publisher || '',
          publish_year: this.newBook.publishYear || '',
          location: this.newBook.location || '',
          if_available: this.newBook.ifAvailable || 1
        });

        const response = await fetch(`http://127.0.0.1:8000/api/libarian-add-books?${params.toString()}`);
        const data = await response.json();

        if (response.ok && data.status === 'success') {
          alert('Book added successfully!');
          // Reset form
          this.newBook = { 
            title: '', 
            author: '', 
            publisher: '', 
            publishYear: '', 
            location: '',
            ifAvailable: 1
          };
        } else {
          alert(`Error: ${data.detail || 'Failed to add book'}`);
        }
      } catch (error) {
        console.error('Error adding book:', error);
        alert('Error adding book. Please try again.');
      }
    },
    
    // Add new reader
    async addReader() {
      if (!this.newReader.id || !this.newReader.name || !this.newReader.password) {
        alert('Please fill in at least Student ID, Name, and Password');
        return;
      }

      if (this.newReader.id.length !== 9) {
        alert('Student ID must be 9 digits');
        return;
      }

      try {
        const params = new URLSearchParams({
          student_id: this.newReader.id,
          name: this.newReader.name,
          password: this.newReader.password,
          email: this.newReader.email || '',
          phone: this.newReader.phone || '',
          department: this.newReader.department || '',
          major: this.newReader.major || ''
        });

        const response = await fetch(`http://127.0.0.1:8000/api/add-new-reader?${params.toString()}`);
        const data = await response.json();

        if (response.ok && data.status === 'success') {
          alert('Reader added successfully!');
          // Reset form
          this.newReader = { 
            id: '', 
            name: '', 
            email: '', 
            phone: '', 
            password: '',
            department: '',
            major: ''
          };
        } else {
          alert(`Error: ${data.detail || 'Failed to add reader'}`);
        }
      } catch (error) {
        console.error('Error adding reader:', error);
        alert('Error adding reader. Please try again.');
      }
    },
    
    // Delete reader
    deleteReader(readerId) {
      console.log(`Deleting reader with ID: ${readerId}`);
      // In actual application, this would call API to delete the reader
    },

    // Perform book/reader search based on active tab
    async performSearch() {
      if (!this.searchQuery.trim()) {
        this.searchResults = [];
        this.showNoResults = false;
        this.selectedBook = null;
        this.selectedReader = null;
        return;
      }

      try {
        if (this.activeTab === 'manage-books') {
          // Search for books
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
        } else if (this.activeTab === 'manage-readers') {
          // Search for readers using the librarianReaderOperation API
          const response = await fetch(`http://127.0.0.1:8000/api/search-readers?query=${encodeURIComponent(this.searchQuery)}`);
          const data = await response.json();

          if (data.readers && data.readers.length > 0) {
            this.searchResults = data.readers;
            this.showNoResults = false;
          } else {
            this.searchResults = [];
            this.showNoResults = true;
          }
          this.selectedReader = null;
        }
      } catch (error) {
        console.error('Search error:', error);
        this.searchResults = [];
        this.showNoResults = true;
      }
    },

    // Select reader for details - emit to parent component
    selectReader(reader) {
      this.$emit('view-reader-detail', reader);
    },

    // Handle search key press
    handleSearchKeyPress(event) {
      if (event.key === 'Enter') {
        this.performSearch();
      }
    },

    // Select book for details - emit to parent component
    selectBook(book) {
      this.$emit('view-book-detail', book);
    },

    // Toggle add reader form
    toggleAddReaderForm() {
      this.showAddReaderForm = !this.showAddReaderForm;
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
  gap: 40px;
  padding: 40px 60px;
}

.sidebar {
  width: 220px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.sidebar img {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid rgba(255, 255, 255, 0.3);
}

.sidebar button {
  width: 100%;
  padding: 12px 16px;
  border-radius: 10px;
  border: none;
  background: rgba(40, 40, 40, 0.5);
  color: white;
  cursor: pointer;
}

.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.nav {
  display: flex;
  gap: 20px;
}

.nav-btn {
  flex: 1;
  padding: 14px;
  border-radius: 10px;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.4);
  background: rgba(255, 255, 255, 0.15);
  color: white;
  cursor: pointer;
}

.nav-btn.active {
  background: rgba(255, 255, 255, 0.35);
  color: #111;
}

.books-wrapper,
.readers-wrapper {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

.book-list,
.reader-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 60vh;
  overflow-y: auto;
  flex: 1;
  padding-right: 10px;
}

.book-card, .reader-card {
  display: flex;
  gap: 16px;
  padding: 16px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.book-cover, .reader-avatar-img {
  width: 90px;
  height: 130px;
  border-radius: 8px;
  object-fit: cover;
  background: url('../../assets/cover.png') center/cover no-repeat;
}

.reader-avatar-img {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: url('../../assets/default_avatar1.png') center/cover no-repeat;
}

.book-info, .reader-info {
  flex: 1;
}

.book-info h3, .reader-info h3 {
  margin-bottom: 8px;
}

.book-info h3,
.book-info p {
  color: #ffffff;
}

.reader-info h3,
.reader-info p {
  color: #ffffff;
}

.book-info p, .reader-info p {
  margin-bottom: 12px;
  line-height: 1.6;
}

.book-actions, .reader-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.book-actions button, .reader-actions button {
  padding: 10px 16px;
  border-radius: 8px;
  border: none;
  color: white;
  cursor: pointer;
}

.view-details-btn { 
  background: rgba(255, 255, 255, 0.2); 
}
.edit-btn { 
  background: rgba(255, 165, 0, 0.7); 
}
.delete-btn { 
  background: rgba(255, 77, 79, 0.7); 
}

.add-panel {
  width: 360px;
  padding: 26px 24px;
  border-radius: 18px;
  background: rgba(10, 10, 10, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.25);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45);
  position: sticky;
  top: 40px;
}

.add-panel h3 {
  margin-bottom: 20px;
  letter-spacing: 1px;
}

.form-group {
  margin-bottom: 18px;
}

label {
  display: block;
  margin-bottom: 6px;
  font-size: 13px;
  letter-spacing: 0.5px;
}

input {
  width: 100%;
  padding: 12px 15px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.25);
  background: rgba(0, 0, 0, 0.45);
  color: white;
}

input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.add-panel button {
  width: 100%;
  padding: 13px;
  border-radius: 12px;
  border: none;
  background: rgba(255, 255, 255, 0.25);
  color: white;
  cursor: pointer;
  letter-spacing: 0.5px;
}

/* Search styles for librarian home */
.search-row {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  padding: 14px 20px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.25);
  background: rgba(0, 0, 0, 0.4);
  color: white;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.search-btn {
  padding: 14px 20px;
  border-radius: 10px;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  cursor: pointer;
}

.nav-btn {
  padding: 14px;
  border-radius: 10px;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.4);
  background: rgba(255, 255, 255, 0.15);
  color: white;
  cursor: pointer;
}

.nav-btn.active {
  background: rgba(255, 255, 255, 0.35);
  color: #111;
}

.search-results {
  margin-top: 20px;
  max-height: 60vh;
  overflow-y: auto;
}

.search-results .book-card {
  display: flex;
  gap: 15px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  margin-bottom: 15px;
  cursor: pointer;
  transition: background 0.3s;
}

.search-results .book-cover {
  width: 60px;
  height: 80px;
  border-radius: 8px;
  object-fit: cover;
}

.search-results .book-info {
  flex: 1;
}

.search-results .book-info h3 {
  margin-bottom: 8px;
}

.search-results .book-info p {
  margin-bottom: 4px;
  font-size: 14px;
}

.search-results .book-actions {
  display: flex;
  flex-direction: column;
  gap: 5px;
  min-width: 100px;
}

.no-results {
  text-align: center;
  padding: 40px 0;
  font-size: 18px;
  color: rgba(255, 255, 255, 0.7);
  margin-top: 20px;
}

.book-detail {
  display: flex;
  gap: 20px;
  margin-top: 20px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
}

.book-cover-container {
  flex: 0 0 auto;
}

.book-cover-full {
  width: 120px;
  height: 160px;
  border-radius: 8px;
  object-fit: cover;
}

.book-detail-info {
  flex: 1;
}

.book-detail-info h3 {
  margin-bottom: 15px;
  font-size: 20px;
}

.book-detail-info p {
  margin-bottom: 10px;
  line-height: 1.5;
}

.detail-actions {
  margin-top: 20px;
}

.detail-actions button {
  margin-right: 10px;
  margin-bottom: 10px;
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  color: white;
  cursor: pointer;
}

.detail-actions .edit-btn {
  background: rgba(255, 165, 0, 0.7);
}
.detail-actions .delete-btn {
  background: rgba(255, 77, 79, 0.7);
}
.detail-actions .back-btn {
  background: rgba(255, 255, 255, 0.2);
}

.report-content {
  flex: 1;
  min-width: 0; /* Allow flex item to shrink below content size */
}
</style>