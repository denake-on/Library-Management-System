<script setup>
import { ref, onMounted } from 'vue';
import Login from './components/Login.vue'
import ReaderHome from './components/Reader/ReaderHome.vue'
import LibrarianHome from './components/Librarian/LibrarianHome.vue'
import DirectorHome from './components/LibraryDirector/DirectorHome.vue'
import BookDetail from './components/Common/BookDetail.vue'
import ReaderDetail from './components/Common/ReaderDetail.vue'
import MyBorrowings from './components/Reader/MyBorrowings.vue'
import ReaderProfileEdit from './components/Reader/ReaderProfileEdit.vue'
import UserProfileEdit from './components/Common/UserProfileEdit.vue'
import P5Background from './components/Common/P5Background.vue'

// 当前显示的组件
const currentView = ref('login'); // 'login', 'reader-home', 'librarian-home', 'director-home', 'book-detail', 'reader-detail', 'profile-edit', or 'my-borrowings'
const userRole = ref('');
const selectedBook = ref(null);
const selectedReader = ref(null);

// 检查用户是否已登录
onMounted(() => {
  const storedRole = localStorage.getItem('userRole');
  const storedToken = localStorage.getItem('userToken');

  // 只有当用户已登录（有token和角色）才显示相应的主页
  if (storedRole && storedToken) {
    userRole.value = storedRole;
    // 根据角色显示相应的首页
    if (storedRole === 'reader') {
      currentView.value = 'reader-home';
    } else if (storedRole === 'librarian') {
      currentView.value = 'librarian-home';
    } else if (storedRole === 'director') {
      currentView.value = 'director-home';
    }
  } else {
    // 否则显示登录页面
    currentView.value = 'login';
  }
});

// 处理登录成功事件
const onLoginSuccess = (role) => {
  // 确认用户已登录并有有效的角色
  const storedToken = localStorage.getItem('userToken');
  if (storedToken && role) {
    userRole.value = role;
    if (role === 'reader') {
      currentView.value = 'reader-home';
    } else if (role === 'librarian') {
      currentView.value = 'librarian-home';
    } else if (role === 'director') {
      currentView.value = 'director-home';
    } else {
      // 如果角色不匹配预期值，回到登录页
      currentView.value = 'login';
    }
  } else {
    // 如果没有有效token，仍然保持在登录页面
    currentView.value = 'login';
  }
};

// 处理登出事件，返回登录页面
const logout = () => {
  localStorage.removeItem('userToken');
  localStorage.removeItem('userRole');
  currentView.value = 'login';
  userRole.value = '';
  selectedBook.value = null;
};

// 处理查看书籍详情
const onViewBookDetail = (book) => {
  selectedBook.value = book;
  currentView.value = 'book-detail';
};

// 处理返回搜索
const onBackToSearch = () => {
  currentView.value = `${userRole.value}-home`;
  selectedBook.value = null;
};

// 处理查看我的借阅
const onViewMyBorrowings = () => {
  currentView.value = 'my-borrowings';
};

// 处理查看读者详情
const onViewReaderDetail = (reader) => {
  selectedReader.value = reader;
  currentView.value = 'reader-detail';
};

// 处理查看读者档案编辑
const onViewReaderProfileEdit = () => {
  currentView.value = 'reader-profile-edit';
};

// 处理查看用户档案编辑 (for librarian and director)
const onViewProfileEdit = () => {
  currentView.value = 'profile-edit';
};

// 处理从档案编辑返回首页
const onBackFromProfileEdit = () => {
  currentView.value = `${userRole.value}-home`;
};

// 处理从读者详情返回搜索
const onBackToReaderSearch = () => {
  currentView.value = 'librarian-home';
  selectedReader.value = null;
};

// 处理从我的借阅返回首页
const onBackToHome = () => {
  currentView.value = `${userRole.value}-home`;
};

// 处理借书
const onBorrow = () => {
  if (selectedBook.value) {
    alert(`Book "${selectedBook.value.book_name}" borrowed successfully!`);
    onBackToSearch();
  }
};

// 处理编辑（BookDetail 组件自己处理，这里只是占位）
const onEdit = () => {
  // BookDetail 组件自己处理编辑
};

// 处理删除书籍（BookDetail 组件自己处理，删除成功后触发此事件）
const onDelete = () => {
  onBackToSearch();
};

// 处理编辑读者（ReaderDetail 组件自己处理，这里只是占位）
const onEditReader = () => {
  // ReaderDetail 组件自己处理编辑
};

// 处理删除读者（ReaderDetail 组件自己处理，删除成功后触发此事件）
const onDeleteReader = () => {
  onBackToReaderSearch();
};
</script>

<template>
  <P5Background />
  <div v-if="currentView === 'login'">
    <Login @login-success="onLoginSuccess" />
  </div>
  <div v-else-if="currentView === 'reader-home'">
    <ReaderHome
      @logout="logout"
      @view-book-detail="onViewBookDetail"
      @view-my-borrowings="onViewMyBorrowings"
      @view-profile-edit="onViewReaderProfileEdit"
    />
  </div>
  <div v-else-if="currentView === 'librarian-home'">
    <LibrarianHome
      @logout="logout"
      @view-book-detail="onViewBookDetail"
      @view-reader-detail="onViewReaderDetail"
      @view-profile-edit="onViewProfileEdit"
    />
  </div>
  <div v-else-if="currentView === 'director-home'">
    <DirectorHome
      @logout="logout"
      @view-book-detail="onViewBookDetail"
      @view-profile-edit="onViewProfileEdit"
    />
  </div>
  <div v-else-if="currentView === 'book-detail'">
    <BookDetail
      :book="selectedBook"
      :user-role="userRole"
      @back-to-search="onBackToSearch"
      @borrow="onBorrow"
      @edit="onEdit"
      @delete="onDelete"
    />
  </div>
  <div v-else-if="currentView === 'reader-detail'">
    <ReaderDetail
      :reader="selectedReader"
      :user-role="userRole"
      @back-to-search="onBackToReaderSearch"
      @edit="onEditReader"
      @delete="onDeleteReader"
    />
  </div>
  <div v-else-if="currentView === 'reader-profile-edit'">
    <ReaderProfileEdit
      @back-to-home="onBackFromProfileEdit"
    />
  </div>
  <div v-else-if="currentView === 'profile-edit'">
    <UserProfileEdit
      :user-role="userRole"
      @back-to-home="onBackFromProfileEdit"
    />
  </div>
  <div v-else-if="currentView === 'my-borrowings'">
    <MyBorrowings
      @back-to-home="onBackToHome"
    />
  </div>
  <div v-else-if="currentView === 'profile-edit'">
    <ReaderProfileEdit
      @back-to-home="onBackToHome"
    />
  </div>
</template>