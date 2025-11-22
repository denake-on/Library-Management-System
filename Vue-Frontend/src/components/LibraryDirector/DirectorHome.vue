<template>
  <div class="director-home-container">
    <div class="content">
      <!-- 侧边栏 - 总是显示 -->
      <div class="sidebar">
        <img :src="avatarSrc" alt="Director Avatar" class="avatar" />
        <h2>Hi, {{ username }} ^^</h2>
        <button @click="viewLibraryReport">view library report</button>
        <button @click="editProfile">edit my information</button>
        <button @click="handleLogout">Log Out</button>
      </div>

      <!-- 主内容区域 - 根据状态显示不同内容 -->
      <div class="main" v-if="!showLibraryReport">
        <div class="nav">
          <button
            :class="['nav-btn', { active: activeSection === 'books' }]"
            @click="switchTab('books')"
          >
            Manage Books
          </button>
          <button
            :class="['nav-btn', { active: activeSection === 'readers' }]"
            @click="switchTab('readers')"
          >
            Manage Readers
          </button>
          <button
            :class="['nav-btn', { active: activeSection === 'librarians' }]"
            @click="showSection('librarians')"
          >
            Manage Librarians
          </button>
        </div>

        <div v-if="activeSection === 'books'">
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

        <div v-else-if="activeSection === 'readers'">
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
                  <img :src="studentImage" alt="Reader Avatar" class="reader-avatar-img" />
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
                  <img :src="studentImage" alt="Reader Avatar" class="reader-avatar-img" />
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
          <!-- Render ReaderDetail when a reader is selected -->
          <ReaderDetail
            v-if="selectedReader"
            :reader="selectedReader"
            userRole="director"
            @back-to-search="selectedReader = null"
            @delete="onReaderDeleted"
            @edit="onReaderEdited"
          />
        </div>

        <!-- Librarians Management Area -->
        <div v-show="activeSection === 'librarians'" class="librarians-area">
          <!-- Search bar for librarians -->
          <div class="search-row">
            <input
              type="text"
              class="search-input"
              :placeholder="searchPlaceholder"
              v-model="searchQuery"
              @keypress="handleLibrarianSearchKeyPress"
            />
            <button class="search-btn" @click="performLibrarianSearch">Search</button>
          </div>

          <div class="readers-wrapper">
            <!-- Search Results Section -->
            <div v-if="searchResults.length > 0 && activeSection === 'librarians'" class="reader-list">
              <div
                v-for="librarian in searchResults"
                :key="librarian.id"
                class="librarian-card"
              >
                <div class="reader-avatar">
                  <img :src="librarianAvatar" alt="Librarian Avatar" class="reader-avatar-img" />
                </div>
                <div class="reader-info">
                  <h3>{{ librarian.name }} (ID: {{ librarian.id }})</h3>
                  <p><strong>Department:</strong> {{ librarian.department }}</p>
                  <p><strong>Email:</strong> {{ librarian.email }}</p>
                  <p><strong>Phone:</strong> {{ librarian.phone }}</p>
                </div>
                <div class="reader-actions">
                  <button @click="deleteLibrarian(librarian.id)" class="delete-btn">Delete</button>
                </div>
              </div>
            </div>

            <!-- No Search Results -->
            <div v-else-if="showNoResults && activeSection === 'librarians'" class="no-results">
              No search results
            </div>

            <!-- Default librarian list if no search has been performed -->
            <div v-else-if="activeSection === 'librarians'" class="reader-list">
              <div
                v-for="librarian in librarians"
                :key="librarian.id"
                class="librarian-card"
              >
                <div class="reader-avatar">
                  <img :src="librarianAvatar" alt="Librarian Avatar" class="reader-avatar-img" />
                </div>
                <div class="reader-info">
                  <h3>{{ librarian.name }} (ID: {{ librarian.id }})</h3>
                  <p><strong>Department:</strong> {{ librarian.department }}</p>
                  <p><strong>Email:</strong> {{ librarian.email }}</p>
                  <p><strong>Phone:</strong> {{ librarian.phone }}</p>
                </div>
                <div class="reader-actions">
                  <button @click="deleteLibrarian(librarian.id)" class="delete-btn">Delete</button>
                </div>
              </div>
            </div>

            <div class="add-panel">
              <h3>Add Librarian</h3>
              <div class="form-group">
                <label>Password</label>
                <input type="password" v-model="newLibrarian.password" placeholder="Password">
              </div>
              <div class="form-group">
                <label>Department</label>
                <input type="text" v-model="newLibrarian.department" placeholder="Department">
              </div>
              <div class="form-group">
                <label>Name</label>
                <input type="text" v-model="newLibrarian.name" placeholder="Full name">
              </div>
              <div class="form-group">
                <label>Email</label>
                <input type="email" v-model="newLibrarian.email" placeholder="Email address">
              </div>
              <div class="form-group">
                <label>Phone</label>
                <input type="text" v-model="newLibrarian.phone" placeholder="Phone number">
              </div>
              <button @click="addLibrarian">Add Librarian</button>
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
import directorAvatar from '../../assets/director_avatar.png'
import coverImage from '../../assets/cover.png';
import studentImage from '../../assets/default_avatar1.png';
import ReaderDetail from '../Common/ReaderDetail.vue';
import LibraryReport from '../Common/LibraryReport.vue';

export default {
  name: 'DirectorHome',
  emits: ['logout', 'view-book-detail', 'view-reader-detail', 'view-profile-edit', 'navigate-to-report'],
  components: {
    ReaderDetail,
    LibraryReport
  },
  data() {
    return {
      username: 'Luoyin', // Default username
      avatarSrc: directorAvatar, // Use director's avatar for the profile
      coverImage: coverImage,
      studentImage: studentImage,
      librarianAvatar: librarianAvatar, // Librarian avatar for librarian cards
      showLibraryReport: false, // To control showing the library report view
      activeSection: 'books', // Default to manage books
      books: [], // Empty array instead of mock data
      readers: [], // Empty array instead of mock data
      librarians: [],
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
      newLibrarian: {
        password: '', // ID will be generated by backend
        department: '',
        name: '',
        email: '',
        phone: ''
      },
      searchQuery: '',
      searchResults: [],
      showNoResults: false,
      selectedBook: null,
        selectedReader: null
    }
  },
  computed: {
    searchPlaceholder() {
      if (this.activeSection === 'books') {
        return 'searching for books....';
      } else if (this.activeSection === 'readers') {
        return 'search for readers...';
      } else if (this.activeSection === 'librarians') {
        return 'search for librarians...';
      }
      return 'search...';
    }
  },
  mounted() {
    this.loadUserInfo();
    this.loadLibrarians(); // Load librarians on component mount
  },
  methods: {
    // 加载用户信息
    loadUserInfo() {
      const username = localStorage.getItem('username');
      if (username) {
        this.username = username;
      }
    },

    viewLibraryReport() {
      console.log('viewLibraryReport clicked');
      this.showLibraryReport = true;
      console.log('showLibraryReport set to:', this.showLibraryReport);
    },

    editProfile() {
      this.$emit('view-profile-edit');
    },

    switchTab(tabName) {
      this.activeSection = tabName;
      // Reset search when switching tabs
      this.searchQuery = '';
      this.searchResults = [];
      this.showNoResults = false;
      this.selectedBook = null;
      this.selectedReader = null;
    },

    showSection(sectionName) {
      this.activeSection = sectionName;
      // Reset search when switching tabs
      this.searchQuery = '';
      this.searchResults = [];
      this.showNoResults = false;
      this.selectedBook = null;
      this.selectedReader = null;
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
        const response = await fetch(`http://127.0.0.1:8000/api/add-new-reader?student_id=${encodeURIComponent(this.newReader.id)}&name=${encodeURIComponent(this.newReader.name)}&password=${encodeURIComponent(this.newReader.password)}&email=${encodeURIComponent(this.newReader.email || '')}&phone=${encodeURIComponent(this.newReader.phone || '')}&department=${encodeURIComponent(this.newReader.department || '')}&major=${encodeURIComponent(this.newReader.major || '')}`);
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

    // Delete librarian
    async deleteLibrarian(librarianId) {
      if (!confirm(`Are you sure you want to delete librarian with ID: ${librarianId}?`)) {
        return;
      }

      try {
        const response = await fetch(`http://127.0.0.1:8000/api/delete-librarian?admin_id=${librarianId}`, {
          method: 'DELETE'
        });
        const data = await response.json();

        if (response.ok && data.status === 'success') {
          alert(data.message);
          // Remove from librarians list
          this.librarians = this.librarians.filter(librarian => librarian.id != librarianId);
          // Also remove from search results if present
          this.searchResults = this.searchResults.filter(librarian => librarian.id != librarianId);
        } else {
          alert(`Error: ${data.detail || 'Failed to delete librarian'}`);
        }
      } catch (error) {
        console.error('Error deleting librarian:', error);
        alert('Error deleting librarian. Please try again.');
      }
    },

    // Add librarian
    async addLibrarian() {
      if (!this.newLibrarian.name || !this.newLibrarian.email || !this.newLibrarian.password) {
        alert('Please fill in at least Name, Email, and Password');
        return;
      }

      try {
        // 确保所有必需字段都有值
        const name = this.newLibrarian.name || '';
        const password = this.newLibrarian.password || '';
        const email = this.newLibrarian.email || '';
        const phone = this.newLibrarian.phone || '';
        const department = this.newLibrarian.department || '';

        const formData = new FormData();
        formData.append('name', name);
        formData.append('password', password);
        formData.append('email', email);
        formData.append('phone', phone);
        formData.append('department', department);

        const response = await fetch(`http://127.0.0.1:8000/api/add-new-librarian`, {
          method: 'POST',
          body: formData
        });

        // 检查响应是否为JSON格式
        const contentType = response.headers.get('content-type');
        let data;
        if (contentType && contentType.includes('application/json')) {
          data = await response.json();
        } else {
          // 如果不是JSON响应，可能是错误响应
          const text = await response.text();
          console.error('Non-JSON response:', text);
          throw new Error(`Non-JSON response: ${text}`);
        }

        if (response.ok && data.status === 'success') {
          alert(`Librarian added successfully! Assigned ID: ${data.ID}`);
          // Add to the librarians list
          const newLibrarian = {
            id: data.ID,
            name: this.newLibrarian.name,
            email: this.newLibrarian.email,
            phone: this.newLibrarian.phone,
            department: this.newLibrarian.department
          };
          this.librarians.push(newLibrarian);
          // Reset form
          this.newLibrarian = {
            password: '',
            department: '',
            name: '',
            email: '',
            phone: ''
          };
        } else {
          alert(`Error: ${data.detail || 'Failed to add librarian'}`);
        }
      } catch (error) {
        console.error('Error adding librarian:', error);
        // 检查是否是422错误
        if (error.message && error.message.includes('422')) {
          alert('Error: There was an issue with the submitted data. Please make sure all required fields are filled correctly.');
        } else if (error.name === 'TypeError' && error.message.includes('formData')) {
          alert('Error: There was an issue with the form data. Please check your inputs.');
        } else {
          alert('Error adding librarian. Please check the console for more details.');
        }
      }
    },

    // Load all librarians initially
    async loadLibrarians() {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/all-librarians');
        const data = await response.json();

        if (response.ok && data.librarians) {
          this.librarians = data.librarians;
        } else {
          console.error('Failed to load librarians:', data.detail);
        }
      } catch (error) {
        console.error('Error loading librarians:', error);
      }
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
        if (this.activeSection === 'books') {
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
        } else if (this.activeSection === 'readers') {
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

    // Perform librarian search
    async performLibrarianSearch() {
      if (!this.searchQuery.trim()) {
        this.searchResults = [];
        this.showNoResults = false;
        return;
      }

      try {
        const response = await fetch(`http://127.0.0.1:8000/api/search-librarian?query=${encodeURIComponent(this.searchQuery)}`);
        const data = await response.json();

        if (data.librarians && data.librarians.length > 0) {
          this.searchResults = data.librarians;
          this.showNoResults = false;
        } else {
          this.searchResults = [];
          this.showNoResults = true;
        }
      } catch (error) {
        console.error('Librarian search error:', error);
        this.searchResults = [];
        this.showNoResults = true;
      }
    },

    // Handle search key press
    handleSearchKeyPress(event) {
      if (event.key === 'Enter') {
        this.performSearch();
      }
    },

    // Handle librarian search key press
    handleLibrarianSearchKeyPress(event) {
      if (event.key === 'Enter' && this.activeSection === 'librarians') {
        this.performLibrarianSearch();
      }
    },

    // Select book for details - emit to parent component
    selectBook(book) {
      this.$emit('view-book-detail', book);
    },

    // Select reader for details - emit to parent component
    selectReader(reader) {
      // Emit for any parent listeners and also show the detail locally
        this.$emit('view-reader-detail', reader);
        this.selectedReader = reader;
    },

    // Called when ReaderDetail emits 'delete'
    onReaderDeleted(reader) {
      // Remove from readers and searchResults if present
      const remove = (arr) => {
        if (!Array.isArray(arr)) return;
        const idx = arr.findIndex(r => (r.student_id || r.id) === (reader.student_id || reader.id));
        if (idx !== -1) arr.splice(idx, 1);
      };
      remove(this.readers);
      remove(this.searchResults);
      this.selectedReader = null;
    },

    // Called when ReaderDetail emits 'edit' (or when the detail saved)
    onReaderEdited(updated) {
      const merge = (arr) => {
        if (!Array.isArray(arr)) return;
        const idx = arr.findIndex(r => (r.student_id || r.id) === (updated.student_id || updated.id));
        if (idx !== -1) Object.assign(arr[idx], updated);
      };
      merge(this.readers);
      merge(this.searchResults);
      if (this.selectedReader && (this.selectedReader.student_id || this.selectedReader.id) === (updated.student_id || updated.id)) {
        Object.assign(this.selectedReader, updated);
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

.sidebar h2 {
  color: white;
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

.book-card, .reader-card, .librarian-card {
  display: flex;
  gap: 16px;
  padding: 16px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.25); /* Slightly darker background */
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
  object-fit: cover;
  background: url('../../assets/student.png') center/cover no-repeat;
}

.book-info, .reader-info {
  flex: 1;
}

.book-info h3, .reader-info h3 {
  margin-bottom: 8px;
}

.book-info h3, .book-info p, .reader-info h3, .reader-info p {
  color: white;
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

.no-results {
  text-align: center;
  padding: 40px 0;
  font-size: 18px;
  color: rgba(255, 255, 255, 0.7);
  margin-top: 20px;
}

/* Responsive design */
@media (max-width: 900px) {
  .content {
    flex-direction: column;
    padding: 20px;
  }

  .sidebar {
    width: 100%;
    flex-direction: row;
    align-items: center;
    flex-wrap: wrap;
    gap: 20px;
  }

  .sidebar img {
    width: 100px;
    height: 100px;
  }

  .sidebar button {
    padding: 10px 12px;
    font-size: 14px;
  }

  .books-wrapper,
  .readers-wrapper {
    flex-direction: column;
  }

  .add-panel {
    width: 100%;
  }
}

.report-content {
  flex: 1;
  min-width: 0; /* Allow flex item to shrink below content size */
}
</style>